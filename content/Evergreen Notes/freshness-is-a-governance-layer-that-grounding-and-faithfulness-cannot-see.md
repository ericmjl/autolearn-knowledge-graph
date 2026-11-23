---
type: "evergreen"
title: "Freshness is a governance layer that grounding and faithfulness cannot see"
created_at: "2026-11-23T22:02:37Z"
updated_at: "2026-11-23T22:02:37Z"
inputs: ["notes-on-llm-knowledge-base-freshness-scoring-metrics-and-framework", "claim-level-faithfulness-is-the-actionable-check-that-a-grounded-model-used-its-context", "compiled-wiki-trades-per-query-retrieval-for-persistent-knowledge"]
provenance_urls: ["https://atlan.com/know/llm-knowledge-base-freshness-scoring/", "https://langfuse.com/resources/engineering/rag-faithfulness-evaluation", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model", "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"]
refutation_status: "untested"
answers_questions: ["What mechanisms exist today to keep retrieved or compiled knowledge current (provenance, world-knowledge updating), and do they transfer from RAG to a compiled wiki?"]
---
Agent synthesis

Freshness is a governance layer that grounding and claim-level faithfulness cannot see. Grounding anchors the answer in external documents and claim-level faithfulness checks that the answer stayed inside the retrieved context, yet neither metric has a temporal component: the freshness framework argues a system can score 95% on faithfulness, context recall, and answer relevance while returning documents superseded for the past 22 hours. Freshness failure is silent. A broken authentication service returns a 403; a stale knowledge base returns an answer that is correct in structure, confident in tone, and weeks out of date, with no staleness flag in the retrieval response.

The fix is upstream metadata, not better retrieval. Content age, embedding lag, stale retrieval rate, and coverage drift each need separate measurement, and coverage drift is the leading indicator: it catches corpus decay before the stale documents surface in live queries, while stale retrieval rate is the lagging one. A nightly batch pipeline leaves 24 hours of staleness, an hourly pipeline 60 minutes, streaming CDC re-indexing seconds, but only for documents with detectable change events. Staleness thresholds must be set per document criticality: near-zero for compliance and pricing, 24 hours for policies, 30 days for references, 90 days for background.

This is the compiled wiki's blind spot exactly. The wiki trades per-query RAG retrieval for a persistent, cross-referenced artifact, and the RAG notes show models can misread or ignore retrieved context. The freshness source adds the piece the wiki's lint pass cannot provide: whether a source has been superseded upstream by its owner or its pipeline, not whether the wiki's own pages contradict each other. A lint pass that flags contradictions and staleness among wiki pages is a contradiction check; freshness scoring that tracks last_verified, updated_at, owner, and corpus drift across all pages turns it into a corpus-health monitor with a remediation path. Without ownership and source-change monitoring, scoring is a number with no remediation path.

Start with a last_verified timestamp, an owner, and a staleness threshold for every page, then measure coverage drift across the whole corpus rather than only the queries that surface today. (see: a compiled wiki trades per-query retrieval for persistence, not for immunity to misreading context) Block or degrade a page when its corpus-drift contribution crosses its threshold, and let consumers of the wiki see how current the source behind every answer actually is.

## Where it comes from

- [[notes-on-llm-knowledge-base-freshness-scoring-metrics-and-framework|LLM Knowledge Base Freshness Scoring: Metrics and Framework]]

## What this builds on

- [[claim-level-faithfulness-is-the-actionable-check-that-a-grounded-model-used-its-context|Claim-level faithfulness is the actionable check that a grounded model used its context]]
- [[compiled-wiki-trades-per-query-retrieval-for-persistent-knowledge|Compiled wiki trades per-query retrieval for persistent knowledge]]
