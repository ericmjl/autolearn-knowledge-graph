---
type: "evergreen"
title: "Compiled wiki trades per-query retrieval for persistent knowledge"
created_at: "2026-11-21T03:02:25Z"
updated_at: "2026-11-21T03:02:25Z"
inputs: ["notes-on-llm-wiki-pattern-andrej-karpathy", "notes-on-retrieval-augmented-generation-wikipedia"]
provenance_urls: ["https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"]
refutation_status: "untested"
---

# Compiled wiki trades per-query retrieval for persistent knowledge

Agent synthesis

An LLM-compiled wiki trades RAG's per-query rediscovery of knowledge for a persistent, cross-referenced artifact. In the "LLM Wiki pattern (Andrej Karpathy)" source, sources are read and integrated once into an LLM-owned wiki of interlinked markdown pages, with ingest writing summaries, updating entity/concept pages, and appending to a log — a single source may touch 10-15 pages — while index.md and log.md provide navigation and history, and lint periodically flags contradictions, stale claims, and gaps. RAG, by contrast, retrieves and re-incorporates external documents on every question, re-deriving knowledge from scratch each time.

The mechanism is compilation rather than retrieval: the wiki is a compounding artifact in which cross-references and contradictions are already flagged, and good query answers can be filed back as new pages instead of disappearing into chat history. The "Retrieval-augmented generation (Wikipedia)" source describes the alternative pipeline — embeddings, vector databases, retrieval, prompt augmentation, generation — which grounds responses in external documents and reduces hallucinations and retraining costs, but still requires the model to re-interpret retrieved context each query.

The combination shows something neither source states alone: the compiled wiki moves RAG's per-query work into a one-time ingest and maintenance pass, but it inherits RAG's limits — the RAG source notes models can misinterpret retrieved context, merge outdated and updated information, and fail to recognize when they lack sufficient information, and a wiki compiled from the same sources is only as reliable as that interpretation. The wiki's advantage is persistence and bookkeeping (near-zero LLM maintenance cost, cross-references kept current), not immunity to misreading context.

## Where it comes from

- [[notes-on-llm-wiki-pattern-andrej-karpathy|LLM Wiki pattern (Andrej Karpathy)]]
- [[notes-on-retrieval-augmented-generation-wikipedia|Retrieval-augmented generation (Wikipedia)]]

## What this builds on

- None yet.
