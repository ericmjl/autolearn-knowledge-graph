---
title: "LLM Wiki v2: What Breaks at Scale"
type: "raw-source"
url: "https://rohitghumare.com/blog/llm-wiki-v2/"
author: "Rohit Ghumare"
publication: "Rohit Ghumare"
published: "2026-08-03"
archived: "2026-11-28T12:01:06Z"
---

> [!quote] Original source
> **Author(s):** Rohit Ghumare  
> **Title:** LLM Wiki v2: What Breaks at Scale  
> **Published in:** Rohit Ghumare  
> **Date:** 2026-08-03  
> **Original:** <https://rohitghumare.com/blog/llm-wiki-v2/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-llm-wiki-v2-what-breaks-at-scale|Source note]]
Themes: [[Context, memory and tools]], [[Loop engineering]]
Why it was archived: How a compiled wiki stays current as sources change, and what breaks when the maintenance pass lags behind the source?

## Archived text

LLM Wiki v2: What Breaks at Scale

The LLM wiki pattern is clean, and the clean version works. Raw sources, LLM-owned pages, a schema, and the three operations: ingest, query, lint. Start there. But run it hard, across thousands of sessions and past a few hundred pages, with more than one agent writing, and a flat pile of markdown starts to sag in specific, predictable ways. This is what I learned patching those failures while building agentmemory, a persistent memory engine for coding agents. I collected the lessons into an extended idea file, LLM Wiki v2, that builds on the original; this essay walks its mechanisms one at a time. Everything in the original still applies. This is what it leaves out.

The missing layer: a memory lifecycle

The simple wiki treats every page as equally true, forever. In practice, knowledge has a lifecycle. A bug you found last week matters more than one from six months ago. A pattern you have seen twelve times is more reliable than one you saw once. A claim from a newer source should quietly weaken an older, contradicting one. A flat store models none of this, so it slowly fills with equally-weighted claims of wildly unequal quality, and the model has no way to tell which is which.

Two facts from this essay sit on one shelf. Each column is a fact's retention, e to the power of minus days since its last confirmation over its strength. The strengths match Fig. 1 below: 120 days for the architecture decision and 9 for the transient bug, and each confirmation adds 5 to the bug. The 0.2 keep line is illustrative.

Confidence scoring

Every fact should carry a confidence: how many sources support it, how recently it was confirmed, whether anything contradicts it. When the LLM writes "Project X uses Redis for caching," that claim should know it came from two sources, was last confirmed three weeks ago, and sits at 0.85. Confidence strengthens with reinforcement and decays with time. That single number turns a flat collection of equal claims into a model that can say "fairly sure about X, less sure about Y," which is the difference between a knowledge base and a rumor mill.

Supersession, not annotation

When new information contradicts an old claim, the old one should not sit there with a note stapled to it. The new claim should explicitly supersede it: linked, timestamped, the old version preserved but marked stale. This is version control for knowledge rather than for files, and it is what lets the wiki hold its history without letting the history pollute the present.

Forgetting is a feature

Not everything should last forever. A wiki that never forgets becomes noise. The fix is a retention curve borrowed straight from Hermann Ebbinghaus, who measured in the 1880s that memory decays exponentially with time, and that each review resets the curve. Facts that mattered once but have not been accessed or reinforced in months should fade, not deleted, deprioritized. And the decay rate should depend on the kind of fact: an architecture decision decays slowly, a transient bug fast. Drag the timeline and reinforce a fact to see the curve reset.

Retention decays exponentially since a fact was last confirmed. An architecture decision holds for months; a transient bug fades in weeks. Slide the day forward, then reinforce either fact (a new source confirms it) and watch its curve reset and steepen.

Consolidation tiers

Raw observations are not established facts, and a wiki that treats them the same drowns the signal. The fix is a pipeline that promotes information upward as evidence accumulates, each tier more compressed, more confident, and longer-lived than the one below it.

A claim earns its way up as evidence accumulates. Confirm it again and again, and watch it promote from a raw observation to an established pattern. Nothing moves up until the tier below it agrees.

Beyond flat pages: a typed graph

The simple wiki is pages joined by wikilinks, and that leaves structure on the table. On ingest, the LLM should not only write prose; it should extract typed entities. React is a library. The auth migration is a project. Sarah is a person who owns that migration and has opinions about React. And the connections between them should carry meaning: "uses," "depends on," "contradicts," "caused," "fixed," "supersedes" are not interchangeable. A link that says "A relates to B" is far weaker than "A caused B, confirmed by 3 sources, confidence 0.9." With a typed graph, a query like "what breaks if we upgrade Redis?" stops being a keyword search and becomes a traversal: start at the Redis node, walk the "depends on" and "uses" edges outward, and surface everything downstream, including the connections keyword search would never find. The graph does not replace the pages. Pages are for reading; the graph is for navigation.

Search that scales

The original leans on index.md, a single file cataloging every page. That works to maybe one or two hundred pages, and then the index itself grows too long for the model to read in one pass. Past that point you want real search, and the version that wins fuses three streams: BM25 for exact keyword matching with stemming, vector search for semantic similarity, and graph traversal for entity-aware relationships. Combine their rankings with reciprocal rank fusion. Each stream catches what the others miss: BM25 finds the exact term, vectors find the paraphrase, the graph finds the structural neighbor. Keep index.md as a human-readable catalog, stop asking the model to use it as its only way to find things.

From manual to event-driven

The biggest practical gap in the simple version is that everything is manual. You drop a source and ask the model to process it. You remember to lint. You decide when to file an answer back. At scale, you want hooks, events that fire on their own:

- On new source: auto-ingest, extract entities, update the graph and index.
- On session start: load the context relevant to recent activity.
- On session end: compress the session into observations, file the insights.
- On query: check whether the answer is worth filing back, above a quality threshold.
- On memory write: check for contradictions, trigger supersession.
- On schedule: periodic lint, consolidation, retention decay.

The human stays in the loop for curation and direction. The bookkeeping, the part that makes people abandon wikis, goes fully automatic. This is the same principle I keep returning to in harness engineering: reliability is in the loop and the checks inside it, not in a single clever prompt. A wiki that lints and consolidates itself on a schedule is a wiki with a loop.

Quality, or the wiki fills with plausible noise

Not all LLM-written content is good, and without controls the wiki accumulates confident-sounding junk. Three habits keep it honest. Score everything: every page the model writes gets a quality score, from a self-evaluation or a second pass, and content below the bar gets flagged or rewritten. Self-healing lint: the lint operation should not merely suggest fixes, it should apply the safe ones, linking orphans, marking stale claims, repairing broken cross-references, so the wiki tends toward health on its own. Contradiction resolution: flagging a contradiction is step one; step two is proposing which claim is more likely right, based on source recency, source authority, and how many observations support each. The human can override, but the default should usually be correct.

The schema is still the real product

All of this is modular, and you do not need it on day one. Start with the minimal viable wiki from the original: raw sources, pages, an index, and a schema describing ingest, query, and lint. Add lifecycle when the store starts feeling like a junk drawer: confidence, supersession, basic decay. Add structure when flat pages stop surfacing the connections you need: entities, typed relationships, the graph. Add automation when the maintenance starts feeling like a chore: the hooks. Add scale, hybrid search and consolidation tiers, when you cross a few hundred pages. At every step, the thing that encodes your judgment is the schema document, the CLAUDE.md or AGENTS.md that says what entities exist, how to ingest each source, what quality bar to hold, how to resolve contradictions, and what the consolidation schedule looks like. The wiki is the output. The schema is the program, and it is the part worth writing carefully.

The idea has now been built into running tools. The next piece looks at two of them, a standalone knowledge-base engine and an implementation as a composable backend worker, in OpenWiki: The Pattern as Running Code.

Keep reading
