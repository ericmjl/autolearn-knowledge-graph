---
type: "source-note"
title: "Notes on: LLM Wiki Is Not a RAG Replacement - It's a Synthesis-Time Decision"
raw: "llm-wiki-is-not-a-rag-replacement-it-s-a-synthesis-time-decision"
url: "https://ranjankumar.in/llm-wiki-synthesis-time-decision-rag-agentic-memory"
created_at: "2026-11-27T15:02:21Z"
updated_at: "2026-11-27T15:02:21Z"
---
- Archived full text: [[llm-wiki-is-not-a-rag-replacement-it-s-a-synthesis-time-decision|Full archived text, with credits]]
- Link: <https://ranjankumar.in/llm-wiki-synthesis-time-decision-rag-agentic-memory>

## What it says

Ranjan Kumar's April 2026 essay argues that LLM Wiki and RAG are not competitors but two positions on one freeze axis: both systems must decide when synthesis happens, at ingest or at query time. The wrong choice for a corpus type causes silent drift: ingest-time synthesis loses precision in summaries that then become the indexed source, and lint validates wiki-to-wiki consistency rather than wiki-to-source fidelity. The piece names a concrete Synthesis Horizon (~100-200 pages, roughly ~100 articles and ~400,000 words for Karpathy's own personal setup) past which index.md navigation breaks and ingest can no longer find which pages to update, forcing the addition of hybrid search and quietly becoming RAG. It advocates corpus stratification (compile stable structural knowledge, query raw for authoritative and precise documents), chain-of-custody frontmatter and query routing rules, and, at team scale, write governance plus a weekly fidelity check that verifies specific claims against source spans.

## Claims drawn from this source

- **LLM Wiki and RAG are the same thing at different synthesis times.** The real architectural question is when synthesis happens, at ingest or at query time. That single decision determines correctness profile, cost model, governance model, and failure modes, and getting it wrong for your corpus type is a compounding mistake.
- **The failure mode lives at ingest: lossy summaries become the corpus.** An LLM-written summary that loses precision (e.g., a payment-terms page omitting a 2% early-payment discount) is indexed as authoritative; lint then validates the summary against itself, and the provenance trail from raw source to query answer is broken at ingest. This is invisible to all three of the wiki's operations.
- **The Synthesis Horizon is structural, not a product limitation.** Above ~100-200 pages index.md can no longer be navigated in a single context pass, and ingest can no longer identify which pages to update without search; cross that threshold and the pattern degrades to RAG without the governance RAG provides.
- **Karpathy's working scale is ~100 articles and ~400,000 words.** At that scale index.md fits in a single context window and the LLM can read it, identify relevant pages, and retrieve them in one pass. Beyond that, Karpathy recommends qmd, Shopify CEO Tobi Lutke's hybrid BM25/vector search with LLM re-ranking, which means adding embeddings, retrieval, and re-ranking: RAG.
- **Scale guidance: under 100 pages is fine, 100-500 needs hybrid search, above 500 wiki is a layer on top of RAG.** Below 100 pages index.md navigation is sufficient; 100-500 pages warrants qmd or equivalent hybrid search; above 500 pages LLM Wiki is a layer on top of RAG, not a replacement, and per Atlan's analysis the index-based model works reliably below ~50,000-100,000 tokens of compiled content.
- **Compile stable structural knowledge; never compile precise, legal, or financial documents.** Compile at ingest when knowledge is structural and stable, the corpus is bounded under ~100-200 pages, one owner reviews output, and precision on specific numbers is not critical. Synthesize at query time for documents that are authoritative, change frequently, or require exact citations; never compile documents with specific numbers, dates, legal language, or larger-than-index-navigable corpora.
- **Chain-of-custody routing rules prevent wiki pages being treated as authoritative.** Add chain_of_custody frontmatter and a claims_requiring_verification list on every wiki page synthesized from authoritative docs, plus query routing rules in the schema file: architectural questions route to the wiki, authoritative/precise questions route to raw retrieval with exact citation.
- **Team scale needs write governance and weekly fidelity checks.** At team scale with no single reviewer, multiple agents can write the same pages last-write-wins; governance requires superseded_by notes with timestamps and sources, history/, a conflicts/ page for unresolved contradictions, log.md appends, and a weekly lint-extension that samples ~10 pages, extracts specific claims (numbers, dates, percentages), and verifies them against the source spans. Lint alone validates wiki-to-wiki consistency, not fidelity to source.
