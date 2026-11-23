---
type: "source-note"
title: "Notes on: LLM Knowledge Base Freshness Scoring: Metrics and Framework"
raw: "llm-knowledge-base-freshness-scoring-metrics-and-framework"
url: "https://atlan.com/know/llm-knowledge-base-freshness-scoring/"
created_at: "2026-11-23T22:01:52Z"
updated_at: "2026-11-23T22:01:52Z"
---
- Archived full text: [[llm-knowledge-base-freshness-scoring-metrics-and-framework|Full archived text, with credits]]
- Link: <https://atlan.com/know/llm-knowledge-base-freshness-scoring/>

## What it says

Atlan's guide argues that most RAG failures are freshness failures, not retrieval failures, and that standard RAG evaluation metrics have no temporal component. Freshness is measured across four dimensions: content age, embedding lag, stale retrieval rate, and coverage drift, and requires upstream metadata (last_verified, updated_at, owner) plus retrieval logging of embedding timestamps. A composite 0-100 score with alerts below 85% and degraded-mode warnings below 70% makes governance measurable, and active metadata platforms turn scoring into remediation through source monitoring, owner notification, and certification workflows. RAG, memory systems, and knowledge graphs each fail differently: RAG through document staleness, memory through personalization drift, and knowledge graphs through entity decay.

## Claims drawn from this source

- **Most RAG failures are freshness failures, not retrieval failures.** Faithfulness, context recall, and answer relevance have no temporal component; a system can score 95% on all three while returning information superseded for the past 22 hours.
- **Freshness degrades silently with no error signal.** A stale knowledge base returns an answer that is correct in structure and confident in tone, but based on outdated information; there is no staleness flag in the retrieval response.
- **Four freshness dimensions each need separate measurement.** Content age (time since last human verification), embedding lag (delay between source update and indexed embedding), stale retrieval rate (fraction of live queries returning a document whose embedding predates its latest update), and coverage drift (fraction of the corpus past its staleness threshold).
- **Nightly batch vs streaming changes staleness by orders of magnitude.** Nightly batch produces up to 24 hours of staleness, hourly batch up to 60 minutes, and streaming CDC re-indexing low single-digit seconds, but only for documents with known change events.
- **Staleness thresholds must be set per document criticality, not uniformly.** Compliance and safety-critical documents need near-zero staleness, policies and procedures allow 24 hours, references allow 30 days, and contextual background allows 90 days.
- **Freshness scoring requires upstream metadata infrastructure.** Every document needs last_verified, updated_at, and owner fields; every retrieval response must log the embedding computation timestamp alongside the document's current updated_at. Without these, embedding lag and stale retrieval rate are untrackable.
- **Correlation between low stale retrieval rate and hidden corpus staleness.** Coverage drift is a leading indicator and stale retrieval rate is a lagging one; a system can have low stale retrieval rate today while its corpus accumulates stale documents that surface episodically.
- **Freshness fails differently across architectures.** RAG fails through document staleness and embedding lag, memory systems through personalization drift, and knowledge graphs through entity decay (outdated facts, not missing ones).
- **Freshness scoring without active metadata is measurement without remediation.** Without ownership fields, source-change monitoring, and certification workflows, the score declines but nothing fixes it; active metadata platforms close the loop by firing recertification events and pulling stale documents from retrieval.
