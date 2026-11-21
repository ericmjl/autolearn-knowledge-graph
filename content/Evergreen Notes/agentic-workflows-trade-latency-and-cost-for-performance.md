---
type: "evergreen"
title: "Agentic workflows trade latency and cost for performance"
created_at: "2026-11-21T03:02:25Z"
updated_at: "2026-11-21T03:02:25Z"
inputs: ["notes-on-agentic-coding-is-a-trap-lars-faye", "notes-on-building-effective-agents-anthropic"]
provenance_urls: ["https://larsfaye.com/articles/agentic-coding-is-a-trap", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
---
Agent synthesis

Agentic workflows trade latency and token cost for better task performance, and the cost side of that trade is real rather than incidental. The mechanism is that agents and workflows add orchestration, tool use, review, and surrounding systems around the model, so the gain in output quality is paid for in time and tokens.

In "Building effective agents (Anthropic)", the core guidance is to start simple and add complexity only when it demonstrably improves outcomes, because agentic systems trade latency and cost for better task performance; it also notes compounding errors and higher costs for autonomous agents. In "Agentic Coding is a Trap (Lars Faye)", the cost is made concrete: token costs fluctuate and rise while employee costs stay fixed, and teams have stalled during Claude outages, alongside extra complexity from managing non-determinism and more review, revisions, and tokens burned.

Together, the two sources show more than either alone: Anthropic supplies the general performance-for-latency-and-cost trade, while Faye shows that the cost side is not a stable, one-time expense but a fluctuating, rising burden against fixed human costs. The combined point is that agentic workflows are a deliberate exchange of speed and output quality for operational overhead, not a free upgrade.

## Where it comes from

- [[notes-on-agentic-coding-is-a-trap-lars-faye|Agentic Coding is a Trap (Lars Faye)]]
- [[notes-on-building-effective-agents-anthropic|Building effective agents (Anthropic)]]

## What this builds on

- None yet.
