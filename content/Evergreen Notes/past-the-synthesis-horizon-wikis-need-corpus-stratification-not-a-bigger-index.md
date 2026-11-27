---
type: "evergreen"
title: "Past the Synthesis Horizon, wikis need corpus stratification, not a bigger index"
created_at: "2026-11-27T15:03:41Z"
updated_at: "2026-11-27T15:03:41Z"
inputs: ["notes-on-llm-wiki-is-not-a-rag-replacement-it-s-a-synthesis-time-decision", "compiled-wikis-beat-per-query-rag-at-moderate-scale"]
provenance_urls: ["https://ranjankumar.in/llm-wiki-synthesis-time-decision-rag-agentic-memory", "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"]
refutation_status: "untested"
answers_questions: ["At what scale does a compiled wiki stop beating per-query RAG, and at what point do the lint and re-ingestion costs outweigh the upfront integration gains?"]
---
Agent synthesis

The Synthesis Horizon bounds compiled wikis, so the fix is corpus stratification, not a bigger index.

The sampled note argues that a compiled wiki beats per-query RAG at moderate scale, and the new source draws the bound around that win. The mechanism is the freeze axis: RAG runs an interpreter that re-synthesizes on every query, while the wiki compiles at ingest, pays upfront, and amortizes query cost. Karpathy reports running his own system at ~100 articles and ~400,000 words, with index.md fitting one context window. Past ~100-200 pages, index.md can no longer be navigated in a single pass and ingest can no longer find which pages to update without a search layer. Karpathy's own recommendation at that point is qmd, Tobi Lutke's hybrid BM25/vector search with LLM re-ranking. Adding qmd means embeddings, retrieval, and re-ranking, so the pattern quietly becomes RAG. Per Atlan's cited analysis, the index-based model works reliably below ~50,000-100,000 tokens of compiled content.

The drift behind that ceiling is chain-of-custody fracture, not hallucination. An LLM summary loses a precise detail, like the new source's payment-terms case where a page omitted a 2% early-payment discount from a vendor contract; the summary then becomes the indexed source. Lint cannot catch it, because lint validates wiki-to-wiki consistency, never wiki-to-source fidelity. The new source's answer is corpus stratification: compile stable structural knowledge like architecture conventions and decision records, retrieve raw for authoritative documents like contracts and incident reports, route by question type in the schema file, add chain_of_custody frontmatter with a claims_requiring_verification list, and run a weekly fidelity check that extracts specific claims and verifies them against source spans. This turns the sampled evergreen's moderate-scale verdict into a bounded one: the wiki wins below the horizon, and above it the honest architecture is a wiki layer on top of RAG, not a replacement.

The synthesis adds something neither input states alone: the moderate-scale advantage has a structural ceiling, and past it the same effort is better spent naming which layer is compiled, which layer is retrieved, and how drift is detected, which is the hinge between the two notes (see: compiled wikis beat per-query RAG at moderate scale). Run the wiki below 100 pages with active review; past that, stratify the corpus by stability and precision and treat lint as a consistency check, not a truth check.

## Where it comes from

- [[notes-on-llm-wiki-is-not-a-rag-replacement-it-s-a-synthesis-time-decision|LLM Wiki Is Not a RAG Replacement - It's a Synthesis-Time Decision]]

## What this builds on

- [[compiled-wikis-beat-per-query-rag-at-moderate-scale|Compiled wikis beat per-query RAG at moderate scale]]
