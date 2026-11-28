---
type: "source-note"
title: "Notes on: LLM Wiki v2: What Breaks at Scale"
raw: "llm-wiki-v2-what-breaks-at-scale"
url: "https://rohitghumare.com/blog/llm-wiki-v2/"
created_at: "2026-11-28T12:01:23Z"
updated_at: "2026-11-28T12:01:23Z"
---
- Archived full text: [[llm-wiki-v2-what-breaks-at-scale|Full archived text, with credits]]
- Link: <https://rohitghumare.com/blog/llm-wiki-v2/>

## What it says

The source argues that the simple LLM wiki pattern (raw sources, LLM-owned pages, three operations: ingest, query, lint) works but sags at scale past a few hundred pages and across multiple writers. It builds on the original with six additions: a memory lifecycle (confidence scoring, supersession, retention decay), consolidation tiers, a typed graph, hybrid search, event-driven hooks, and quality controls (scoring, self-healing lint, contradiction resolution), with the schema document as the real product.

## Claims drawn from this source

- **The flat wiki treats every page as equally true.** The simple wiki treats every page as equally true, forever; in practice, a bug found last week matters more than one from six months ago, and a claim from a newer source should quietly weaken an older, contradicting one.
- **Facts should carry a confidence score.** Every fact should carry a confidence: how many sources support it, how recently it was confirmed, whether anything contradicts it; confidence strengthens with reinforcement and decays with time, turning a flat collection of equal claims into a model that can say 0.85 about X and less about Y.
- **New information supersedes old claims explicitly.** The new claim should explicitly supersede the old one: linked, timestamped, the old version preserved but marked stale, version control for knowledge rather than for files.
- **Forgetting is a feature, with Ebbinghaus decay.** Retention decays exponentially since a fact was last confirmed; an architecture decision holds for months, a transient bug fades in weeks; decay is by fact type and each confirmation resets the curve.
- **Consolidation tiers promote raw observations upward.** Raw observations are not established facts; a pipeline promotes information upward as evidence accumulates, each tier more compressed, more confident, and longer-lived than the one below it, and nothing moves up until the tier below it agrees.
- **A typed graph beats wikilinks for navigation.** On ingest the LLM should extract typed entities with typed relations (uses, depends on, contradicts, caused, fixed, supersedes), so a query like what breaks if we upgrade Redis becomes a traversal that surfaces downstream connections keyword search would never find.
- **Hybrid search replaces a single index file.** Index.md works to one or two hundred pages, then the model cannot read it in one pass; past that, fuse BM25 keyword matching, vector search, and graph traversal with reciprocal rank fusion, and keep index.md as a human-readable catalog.
- **Automation shifts bookkeeping into event hooks.** On new source, on session start, on session end, on query, on memory write, and on schedule: auto-ingest, context load, session compression, answer filing, contradiction checks, and periodic lint with consolidation and decay, with the human keeping curation and direction.
