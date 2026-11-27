---
title: "LLM Wiki Is Not a RAG Replacement - It's a Synthesis-Time Decision"
type: "raw-source"
url: "https://ranjankumar.in/llm-wiki-synthesis-time-decision-rag-agentic-memory"
author: "Ranjan Kumar"
publication: "ranjankumar.in"
published: "2026-04-20"
archived: "2026-11-27T15:01:24Z"
---

> [!quote] Original source
> **Author(s):** Ranjan Kumar  
> **Title:** LLM Wiki Is Not a RAG Replacement - It's a Synthesis-Time Decision  
> **Published in:** ranjankumar.in  
> **Date:** 2026-04-20  
> **Original:** <https://ranjankumar.in/llm-wiki-synthesis-time-decision-rag-agentic-memory>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-llm-wiki-is-not-a-rag-replacement-it-s-a-synthesis-time-decision|Source note]]
Themes: [[Evals and agent quality]], [[Agent design patterns]]
Why it was archived: At what scale does a compiled wiki stop beating per-query RAG, and at what point do the lint and re-ingestion costs outweigh the upfront integration gains?

## Archived text

This article covers the LLM Wiki pattern as it stands in April 2026, two weeks after Karpathy's gist crossed 5,000 stars and 17 million views. The ecosystem is moving fast - implementations are shipping daily.

The week Karpathy's llm-wiki gist crossed 5,000 stars and 17 million views, my team's internal knowledge base was silently lying to us.

Not obviously. No error messages. No failed requests. Just a payment terms wiki page that said "standard net-30 terms with early-payment discounts" - a summary an LLM had written six months earlier from a vendor contract that actually specified a 2% discount if paid within 10 days. Three lint passes later, the wiki's Payment Terms page and its linked Vendor Agreements page were internally consistent. Both omitted the 2%. Consistent with each other. Inconsistent with the contract. The system had no way to know the difference.

That's not a hallucination in the traditional sense. The LLM didn't fabricate a number. It summarized accurately and lost precision. Then the summary became the source. Then the lint pass validated the summary against itself.

This is the failure mode the LLM Wiki discourse isn't naming. And it's directly caused by making the wrong synthesis-time decision.

The Thesis

The community has framed LLM Wiki as a competition with RAG: "Does it kill RAG?" The answer is no - and the debate itself is the wrong frame.

LLM Wiki and RAG are the same thing at different synthesis times - two positions on the same freeze axis, not two competing technologies. The structural benefits Karpathy's pattern adds - cross-references, entity pages, contradiction flags - are real and additive. They exist regardless of synthesis time. But the synthesis-time decision is what determines your correctness profile, your cost model, and your failure modes. The real architectural question is: when does synthesis happen - at ingest or at query time? That single decision determines your correctness profile, your cost profile, your governance model, and your failure modes. Getting it wrong for your corpus type is a compounding mistake.

The pattern Karpathy described is correct. The conclusion the community drew - that it replaces RAG - is wrong. And applying it at the wrong scale or corpus type will produce knowledge bases that look fine and drift from truth for months before anyone notices.

What Karpathy Actually Proposed

Before diagnosing the failure modes, state the pattern accurately. Karpathy's gist describes three layers:

- raw/ - immutable source documents. LLM reads, never writes.
- wiki/ - LLM-owned markdown pages. Summaries, entity pages, cross-references, synthesis.
- Schema file (CLAUDE.md or AGENTS.md) - tells the LLM how the wiki is structured, what conventions to follow, what workflows to run.

Three operations:

- Ingest - LLM reads a new source, discusses takeaways, writes a summary page, updates relevant entity pages across the wiki (typically 10-15 pages per source), updates the index, appends to the log.
- Query - LLM reads index.md first, identifies relevant pages, reads them, synthesizes an answer with citations.
- Lint - periodic health check: contradictions, stale claims, orphan pages, missing cross-references.

The key insight is the compiler analogy. RAG runs an interpreter: every query re-reads raw documents, re-derives relationships, re-synthesizes. The LLM Wiki pattern is compilation: process sources once at ingest, store the compiled output, query the output not the source.

The compiler pays upfront cost to amortize query cost. That's a sound engineering trade-off. It's also where the failure mode lives.

The Wrong-Way Pattern: Treating Compile-Time Synthesis as Ground Truth

Here's what teams are getting wrong:

# WRONG: LLM-authored content indexed as authoritative source# Missing: routing rule that forces raw/ lookup for specific claimsraw/  vendor-contract-2025.pdf          # original: "net-30, 2% discount if paid in 10 days"wiki/  payment-terms.md                  # LLM wrote: "net-30 with early-payment discounts"  vendor-agreements.md              # LLM wrote: links to payment-terms.md, no % mentionedindex.md                             # payment-terms.md: "Covers payment structure..."

When a query arrives - "what's our early-payment discount?" - the retrieval hits payment-terms.md first. It's the concept hub. Heavily backlinked. Exactly what a good index surfaces. The LLM synthesizes from the wiki page, not the contract. The wiki page doesn't have the 2%. The answer is wrong.

Run lint. The lint pass checks whether wiki pages are internally consistent. payment-terms.md and vendor-agreements.md agree with each other. Lint passes. Nothing flagged.

The original contract is still in raw/. It's immutable. It's just not being queried.

The error didn't happen at query time. It happened at ingest time, when the LLM summarized precisely but lossy, and the summary became the corpus. This is the Knowledge Chain of Custody fracture - the provenance trail from raw source to query answer is broken the moment LLM-authored content is indexed as authoritative alongside the originals.

The deeper problem: this isn't detectable from inside the system. The lint operation validates wiki-to-wiki consistency, not wiki-to-source fidelity. The chain of custody fracture is invisible to all three operations.

The Synthesis-Time Decision

Every knowledge system makes a synthesis-time decision, whether it knows it or not:

flowchart LR

    subgraph A["Ingest-time Synthesis (LLM Wiki)"]

        A1[Raw Source] --> A2[LLM Synthesis] --> A3[Wiki Page] --> A4[Index] --> A5[Query hits Wiki Page]

    end

    subgraph B["Query-time Synthesis (RAG)"]

        B1[Raw Source] --> B2[Embedding / Index] --> B3[Retrieval] --> B4[LLM Synthesis] --> B5[Answer]

    end

    style A1 fill:#4A90E2,color:#fff

    style A2 fill:#9B59B6,color:#fff

    style A3 fill:#6BCF7F,color:#fff

    style A4 fill:#98D8C8,color:#333

    style A5 fill:#6BCF7F,color:#fff

    style B1 fill:#4A90E2,color:#fff

    style B2 fill:#98D8C8,color:#333

    style B3 fill:#FFD93D,color:#333

    style B4 fill:#9B59B6,color:#fff

    style B5 fill:#6BCF7F,color:#fff

The trade-offs are different, not better/worse:

Neither is universally correct. The right choice depends on your corpus type.

The Synthesis Horizon

There's a concrete scale threshold above which ingest-time synthesis stops working.

Synthesis Horizon: the corpus size at which the ingest-time synthesis model breaks - where index.md can no longer be navigated in a single context pass, ingest can no longer identify which pages to update, and errors compound faster than lint can catch them. Cross this threshold and the pattern degrades to RAG without the governance RAG provides.

Karpathy's own data point: he reports running his system at ~100 articles and ~400,000 words. At that scale, index.md fits in a single context window. The LLM can read it, identify relevant pages, and retrieve them in one pass. It works.

Past ~100-200 pages, index.md becomes unnavigable in a single pass. More importantly, the ingest operation itself breaks: when adding a new source, the LLM needs to identify which existing pages to update - but it can't navigate a large index to find them without already having search. Karpathy's own recommendation at this scale is qmd - Shopify CEO Tobi Lutke's local hybrid BM25/vector search with LLM re-ranking.

What is qmd? 

qmd is a local search engine for markdown files built by Tobi Lutke (CEO of Shopify). It uses hybrid BM25/vector search with LLM re-ranking, runs entirely on-device, and ships as both a CLI tool and an MCP server - meaning an agent can call it natively from Claude Code. Karpathy recommends it as the search layer once your wiki outgrows index.md navigation. The irony is deliberate: adding qmd means you now have embeddings, retrieval, and re-ranking. That is RAG. The pattern that positioned itself as a RAG replacement quietly becomes one at scale.

That's just RAG. The pattern scales up into the thing it was supposed to replace.

The Synthesis Horizon is not a product limitation. It's structural. The index-based navigation model breaks at corpus sizes that matter for team use. You hit the cliff before the wiki becomes enterprise-useful.

flowchart TD

    A{Corpus Scale?} --> B["Personal Scale\n&lt; 100 sources"]

    A --> C["Team Scale\n100 - 1000+ sources"]

    B --> B1[index.md navigation works]

    B1 --> B2[Ingest-time synthesis appropriate]

    B2 --> B3[One user reviews LLM output\ncatches errors early]

    B3 --> B4[✓ Use LLM Wiki]

    C --> C1[index.md breaks]

    C1 --> C2[Add qmd = you have RAG]

    C2 --> C3[No single reviewer\nacross all LLM output]

    C3 --> C4[Errors compound unseen]

    C4 --> C5[✗ LLM Wiki alone is wrong here]

    style A fill:#FFD93D,color:#333

    style B fill:#4A90E2,color:#fff

    style C fill:#4A90E2,color:#fff

    style B1 fill:#98D8C8,color:#333

    style B2 fill:#98D8C8,color:#333

    style B3 fill:#98D8C8,color:#333

    style B4 fill:#6BCF7F,color:#fff

    style C1 fill:#FFA07A,color:#333

    style C2 fill:#FFA07A,color:#333

    style C3 fill:#FFA07A,color:#333

    style C4 fill:#FFA07A,color:#333

    style C5 fill:#E74C3C,color:#fff

The Right-Way Pattern: Corpus-Stratified Synthesis

The correct architecture doesn't choose between LLM Wiki and RAG. It stratifies the corpus by stability and applies the right synthesis time to each layer.

# RIGHT: Synthesis time matches corpus typeArchitectural layer (compile at ingest - LLM Wiki):  wiki/    architecture/      system-overview.md            # stable; synthesized once, manually reviewed      decision-records.md           # stable; ADRs compiled, human-verified      module-boundaries.md          # stable; conventions compiled from code reviews    concepts/      domain-glossary.md            # stable; entity pages built once, lint-maintainedDocument corpus (synthesize at query time - RAG):  raw/    contracts/                      # authoritative; never compiled    vendor-agreements/              # authoritative; queried fresh per request    meeting-notes/                  # dynamic; retrieved, not compiled    incident-reports/               # authoritative; queried with citation requiredRouting layer:  "What's our architecture for X?" → wiki query  "What does our contract with Y say?" → RAG retrieval over raw/flowchart TD

    ROOT[Knowledge Base Root] --> WIKI[wiki/]

    ROOT --> RAW[raw/]

    WIKI --> ARCH[architecture/]

    WIKI --> CONCEPTS[concepts/]

    ARCH --> S1[system-overview.md\nstable · synthesized once · reviewed]

    ARCH --> S2[decision-records.md\nstable · ADRs · human-verified]

    ARCH --> S3[module-boundaries.md\nstable · compiled from code reviews]

    CONCEPTS --> S4[domain-glossary.md\nstable · entity pages · lint-maintained]

    RAW --> R1[contracts/\nauthoritative · never compiled]

    RAW --> R2[vendor-agreements/\nauthoritative · queried fresh]

    RAW --> R3[meeting-notes/\ndynamic · retrieved not compiled]

    RAW --> R4[incident-reports/\nauthoritative · citation required]

    ROUTER[Routing Layer\nCLAUDE.md] -->|Architecture query| WIKI

    ROUTER -->|Contract / authoritative query| RAW

    style ROOT fill:#95A5A6,color:#fff

    style WIKI fill:#6BCF7F,color:#fff

    style RAW fill:#9B59B6,color:#fff

    style ARCH fill:#98D8C8,color:#333

    style CONCEPTS fill:#98D8C8,color:#333

    style S1 fill:#6BCF7F,color:#fff

    style S2 fill:#6BCF7F,color:#fff

    style S3 fill:#6BCF7F,color:#fff

    style S4 fill:#6BCF7F,color:#fff

    style R1 fill:#FFA07A,color:#333

    style R2 fill:#FFA07A,color:#333

    style R3 fill:#FFA07A,color:#333

    style R4 fill:#FFA07A,color:#333

    style ROUTER fill:#FFD93D,color:#333

The routing layer is the key addition. The schema file (CLAUDE.md or AGENTS.md) encodes which corpus layer to query based on the question type. Architectural questions route to the compiled wiki. Authoritative document questions route to raw retrieval.

Here's a minimal schema excerpt for CLAUDE.md:

## Query RoutingWhen answering a question:1. Classify the question type:   - Architecture / patterns / conventions → read wiki/architecture/ first   - Contracts / legal / financial specifics → read raw/contracts/ directly, cite the source document   - Incident history / decisions → read wiki/decisions/ first, then verify against raw/ if precision is critical2. Chain of custody rule:   - If the answer involves a specific number (amount, date, percentage, deadline),      always verify against raw/ even if wiki/ has a value.   - State: "Per [source file], [specific claim]" not "Per the wiki, [claim]"3. Never cite wiki/ pages as authoritative for claims that originated in raw/ documents.   Wiki pages are synthesis aids, not source documents.

This is the schema discipline the community is not building. The raw/wiki separation in Karpathy's pattern is correct. The missing piece is the routing rule that prevents wiki pages from being treated as authoritative for claims that live in raw documents.

Corpus Layers and Synthesis Time: A Decision Guide

Not all knowledge has the same synthesis-time requirements. Use this decision guide:

Compile at ingest time (LLM Wiki) when:

- Knowledge is structural and stable (architecture decisions, module conventions, domain glossary)
- The corpus is bounded and curated (&lt;100-200 pages)
- One owner reviews LLM output on ingest
- Query frequency is high and the same synthesis would be re-done repeatedly
- Precision on specific numbers is not critical

Synthesize at query time (RAG) when:

- Documents are authoritative and must be cited exactly (contracts, compliance docs, financial records)
- The corpus changes frequently (meeting notes, incident logs, customer calls)
- Precision matters - you need the exact clause, not the summary
- Multi-user access with no single reviewer
- Scale exceeds the Synthesis Horizon

Always synthesize at query time (never compile) when:

- Source documents are legal or financial instruments
- Specific numbers, dates, or thresholds appear in the source
- Regulatory compliance requires source citation
- The corpus is larger than what index.md can navigate

Implementation: Enforcing Chain of Custody

The practical implementation change that prevents the drift pattern:

# wiki/architecture/payment-terms.md frontmatter---title: "Payment Terms - Compiled Overview"source: "raw/contracts/vendor-master-2025.pdf"compiled: "2026-03-15"chain_of_custody: "DO NOT USE for specific amounts or deadlines - query raw source"claims_requiring_verification:  - "Early payment discount percentage"  - "Payment due dates"  - "Penalty terms"---# Payment TermsThis is a compiled synthesis for orientation. For specific amounts, dates, or thresholds, always query the source document: raw/contracts/vendor-master-2025.pdf**Overview:** Net-30 terms standard. Early payment discounts available.See source for exact percentages and qualification windows.

The frontmatter convention signals to the LLM at query time that this page is a navigation aid, not a source of truth for specific claims. The claims_requiring_verification list tells the LLM when to pass through to raw.

The Multi-User Problem Is Deeper Than You Think

Karpathy's original gist is explicit: it's a personal knowledge base. One user. He reviews ingest output in real time. He can catch when the LLM misses the 2%.

The DokuWiki founder (Andi Gutmans) stated this directly in April 2026: "What his pattern is lacking is any notion of how it would work with multiple users. How would the system evolve when prompted by different users with different needs? Who are edits attributed to when agents potentially edit and rewrite whole sections of the wiki at any time?"

At team scale:

- No single person reviews every ingest
- Multiple agents may be writing the same wiki pages from different sessions
- Last-write-wins creates silent conflict resolution
- The lint pass validates internal consistency, not truth

The governance layer most teams are skipping:

## CLAUDE.md - Multi-Agent Write GovernanceOn every wiki write:1. Check if the page already exists2. If yes: read the existing content; identify claims this update changes3. For each changed claim: add a `superseded_by` note with timestamp and source4. Never silently overwrite - old content goes to a `history/` section5. Append to log.md with: timestamp, agent_id, files_changed, sources_usedOn contradictions:1. Do not resolve automatically2. Create a `conflicts/` page listing the contradiction with both sources3. Flag for human review4. Do not update the main wiki page until a human resolves

Without this, multi-agent writes are a last-write-wins free-for-all that the lint pass will happily validate as internally consistent.

LLM Wiki Production Architecture: Corpus-Stratified Synthesis

flowchart TD

    Z[Team-Scale Architecture] --> A

    A[Raw Sources\nContracts, Documents, Notes] --> B{Synthesis-Time\nDecision}

    B -->|Stable architectural\nknowledge| C[Ingest-time Synthesis\nLLM Wiki Layer]

    B -->|Authoritative docs\nspecific claims| D[Query-time Synthesis\nRAG Layer]
    
    C --> E[wiki/architecture/\nwiki/concepts/\nwiki/decisions/]

    D --> F[raw/ retrieval\nwith citation]
    
    E --> G{Schema Router\nCLAUDE.md}

    F --> G
    
    G -->|Architecture query| H[Read wiki page\nSynthesize from compiled]

    G -->|Specific claim query| I[Retrieve raw source\nCite exact span]
    
    H --> J[Answer with\nNavigation provenance]

    I --> K[Answer with\nSource provenance]
    
    L[Lint Agent] --> E

    L -->|Validates| M[Internal consistency\nNOT truth vs source]
    
    style Z fill:#95A5A6,color:#fff

    style A fill:#4A90E2,color:#fff

    style C fill:#6BCF7F,color:#fff

    style D fill:#9B59B6,color:#fff

    style G fill:#FFD93D,color:#333

    style H fill:#6BCF7F,color:#fff

    style I fill:#9B59B6,color:#fff

    style L fill:#E74C3C,color:#fff

    style M fill:#E74C3C,color:#fff

The red box on lint is intentional. Lint validates internal wiki consistency - not fidelity to source. That's the gap most teams miss.

What to Do Right Now

If you're building or running an LLM Wiki:

Classify your corpus before you ingest anything:

- List every document type in your corpus
- Label each: architectural/stable vs. authoritative/precise
- Documents with specific numbers, dates, amounts, or legal language: never compile - always retrieve raw
- Structural knowledge - conventions, patterns, decisions: safe to compile

Add chain of custody to your schema:

- chain_of_custody frontmatter field on every wiki page
- claims_requiring_verification list on any page synthesized from authoritative docs
- Query routing rules in CLAUDE.md that distinguish wiki queries from raw source queries

If running at team scale:

- Add write governance to CLAUDE.md - explicit conflict, supersession, and log rules
- Do not rely on lint alone - lint catches wiki-to-wiki inconsistency, not source drift
- Implement a periodic fidelity check: run a lint-extension prompt weekly that samples 10 wiki pages, extracts their specific claims (numbers, dates, percentages), and verifies each against the source file listed in that page's frontmatter. A simple shell script can diff extracted claims against raw source spans to surface drift automatically - don't rely on manual review alone

Know your Synthesis Horizon:

- Below 100 pages: index.md navigation is sufficient
- 100-500 pages: add qmd or equivalent hybrid search (this is RAG, name it)
- Above 500 pages: LLM Wiki is a layer on top of RAG, not a replacement; per Atlan's analysis, the index-based model works reliably below ~50,000-100,000 tokens of compiled content

For personal use: Ship it. The pattern works at personal scale with active review.

For team use: Apply the corpus stratification. Without it, you're building a knowledge base that drifts from truth and looks fine while doing it.

Why Most Teams Will Build This Wrong

Most of the LLM Wiki discourse is cargo-culting the architecture without internalizing the correctness contract.

Karpathy's gist says this explicitly, in the final paragraph: "This document is intentionally abstract. It describes the idea, not a specific implementation. Everything mentioned above is optional and modular - pick what's useful, ignore what isn't."

The pattern is a starting point. The synthesis-time decision, the corpus stratification, the chain-of-custody rules, the write governance - none of these are in the gist. They're the production layer that the pattern doesn't define.

The failure mode is not that the LLM Wiki pattern is wrong. The failure mode is treating an idea file as a specification and shipping it to teams without the production layer.

If you're building a knowledge system that your organization will depend on in three years, the question isn't "should I use LLM Wiki or RAG?" The question is: for each corpus layer, when does synthesis happen, who verifies it, and how do you know when it drifted?

The answer to that question is your architecture.

References

- Karpathy, A. (2026, April 4). llm-wiki.md. GitHub Gist. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Lahoti, A. (2026, April 18). The Hidden Flaw in Karpathy's LLM Wiki. Medium. https://foundanand.medium.com/the-hidden-flaw-in-karpathys-llm-wiki-e3a86a94b459
- Nasternak, M. (2026, April). The LLM Wiki at Scale: From Personal Research Tool to Production RAG. Medium. https://michalnasternak.medium.com/the-llm-wiki-at-scale-from-personal-research-tool-to-production-rag-247710a1284c
- Mysore, V. (2026, April 20). RAG vs. Agent Memory vs. LLM Wiki: A Practical Comparison. Medium. https://medium.com/@visrow/rag-vs-agent-memory-vs-llm-wiki-a-practical-comparison-41a9a0dc4dec
- Nayak, P. (2026, April). Beyond RAG: How Andrej Karpathy's LLM Wiki Pattern Builds Knowledge That Actually Compounds. Level Up Coding. https://levelup.gitconnected.com/beyond-rag-how-andrej-karpathys-llm-wiki-pattern-builds-knowledge-that-actually-compounds-31a08528665e
- Denser.ai. (2026, April). From RAG to LLM Wiki: What Karpathy's Idea Means for AI Knowledge Bases. https://denser.ai/blog/llm-wiki-karpathy-knowledge-base/
- Epsilla. (2026, April 6). Did Karpathy's 'LLM Wiki' Just Kill RAG? The Enterprise Verdict. https://www.epsilla.com/blogs/llm-wiki-kills-rag-karpathy-enterprise-semantic-graph
- Rohit G. (2026, April). LLM Wiki v2 - extending Karpathy's LLM Wiki pattern with lessons from building agentmemory. GitHub Gist. https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2
- Chen, Z. et al. (2024). AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases. arXiv:2407.12784. https://arxiv.org/abs/2407.12784
- Atlan. (2026, April). LLM Wiki vs RAG: The Karpathy Concept and Enterprise Reality. https://atlan.com/know/llm-wiki-vs-rag-knowledge-base/
- DokuWiki Founder (Andi Gutmans). (2026, April 15). DokuWiki Newsletter. https://www.cosmocode.de/en/services/wiki/dokuwiki-newsletter/2026-04-15/
- MindStudio. (2026, April). LLM Wiki vs RAG for Internal Codebase Memory. https://www.mindstudio.ai/blog/llm-wiki-vs-rag-internal-codebase-memory
- HumanLayer. (2025, November). Writing a good CLAUDE.md. https://www.humanlayer.dev/blog/writing-a-good-claude-md
- Anthropic. (2026). Create custom subagents - Claude Code Docs. https://code.claude.com/docs/en/sub-agents

Related Articles

- Agent Skills Are Not Prompts. They Are Production Knowledge Infrastructure.
- Epistemic Restraint by Design: Boundary-Aware AI Systems
- Four Habits from the Creator of Claude Code That Will Change How You Ship
- Claude Code on Brownfield Codebases: The Harness Is the Product
