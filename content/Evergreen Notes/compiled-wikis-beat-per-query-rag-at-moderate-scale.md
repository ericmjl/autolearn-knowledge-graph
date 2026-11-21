---
type: "evergreen"
title: "Compiled wikis beat per-query RAG at moderate scale"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-llm-wiki-pattern-andrej-karpathy", "notes-on-retrieval-augmented-generation-wikipedia"]
provenance_urls: ["https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"]
refutation_status: "untested"
---
Agent synthesis

At moderate scale, a compiled, interlinked wiki with an index beats per-query embedding retrieval by avoiding re-derivation and surfacing contradictions. The mechanism is persistence: instead of re-discovering knowledge from raw documents on every question, the wiki is built once and kept current, with cross-references and contradictions already flagged, so each query drills into a curated artifact rather than re-reading and re-synthesizing sources. A content-oriented index.md lets the LLM read a catalog of pages with one-line summaries first and then drill in, which works well around ~100 sources and hundreds of pages. The "LLM Wiki pattern (Andrej Karpathy)" source makes this explicit, contrasting the compiled wiki with RAG's per-query rediscovery and noting that ingest touches many pages at once while lint periodically flags contradictions, stale claims, orphan pages, and missing cross-references. The "Retrieval-augmented generation (Wikipedia)" source supplies the counter-evidence: RAG grounds responses in external documents but still misinterprets context, merges outdated and updated information, struggles with conflicting sources, and may answer even when it lacks sufficient information, with chunking and vector search each trading away focus or recall. Together, the two sources show that at moderate scale the compiled wiki's upfront integration and periodic linting do work that per-query retrieval leaves to the model at answer time, which no single source states alone.

## Where it comes from

- [[notes-on-llm-wiki-pattern-andrej-karpathy|LLM Wiki pattern (Andrej Karpathy)]]
- [[notes-on-retrieval-augmented-generation-wikipedia|Retrieval-augmented generation (Wikipedia)]]

## What this builds on

- None yet.
