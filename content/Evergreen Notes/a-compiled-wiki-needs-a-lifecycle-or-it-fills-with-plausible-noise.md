---
type: "evergreen"
title: "A compiled wiki needs a lifecycle or it fills with plausible noise"
created_at: "2026-11-28T12:01:56Z"
updated_at: "2026-11-28T12:01:56Z"
inputs: ["notes-on-llm-wiki-v2-what-breaks-at-scale", "compiled-wiki-trades-per-query-retrieval-for-persistent-knowledge"]
provenance_urls: ["https://rohitghumare.com/blog/llm-wiki-v2/", "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"]
refutation_status: "untested"
answers_questions: ["How does a compiled wiki stay current as sources change, and what breaks when the maintenance pass lags behind the source?"]
---
Agent synthesis

A compiled wiki needs a lifecycle or it fills with plausible noise. The simple wiki treats every page as equally true, so stale claims, weak evidence, and old contradictions pile up until the model reads confident junk. The source note argues the plain pattern (raw sources, LLM-owned pages, ingest/query/lint) works but sags past a few hundred pages and across multiple writers, and names the missing layers: confidence scoring, explicit supersession, retention decay, consolidation tiers, a typed graph, hybrid search, event-driven hooks, and quality controls, with the schema document as the real product.

The sampled evergreen frames the wiki as a compounding artifact with cross-references and a lint pass over contradictions, but its lint is a remembered task, not a lifecycle. The new source fills in the mechanism: confidence (how many sources support a claim, how recently it was confirmed, whether anything contradicts it), reinforcement that strengthens and decay that weakens it; supersession, where the new claim links and timestamps the old one and marks it stale rather than stapling a note to it; and exponential retention decay by fact type, with architecture decisions lasting months and transient bugs fading in weeks, each confirmation resetting the curve. The synthesis: persistence without decay is a store of equal noise. The lifecycle turns the wiki into a ranked, dated, versioned memory, which is what compounding actually requires.

The schema is still the load-bearing piece: what entities exist, how ingest works, the quality bar, how contradictions resolve, and the consolidation schedule. The schema document, not the prompt, encodes the judgment. (see: compiled wiki trades per-query retrieval for persistent knowledge)

Start with the minimal wiki, then add confidence, supersession, and decay when the store starts feeling like a junk drawer, and graduate the flat index to hybrid search when pages cross a few hundred.

## Where it comes from

- [[notes-on-llm-wiki-v2-what-breaks-at-scale|LLM Wiki v2: What Breaks at Scale]]

## What this builds on

- [[compiled-wiki-trades-per-query-retrieval-for-persistent-knowledge|Compiled wiki trades per-query retrieval for persistent knowledge]]
