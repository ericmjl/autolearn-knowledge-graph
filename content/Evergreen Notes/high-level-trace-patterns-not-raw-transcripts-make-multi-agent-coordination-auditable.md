---
type: "evergreen"
title: "High-level trace patterns, not raw transcripts, make multi-agent coordination auditable"
created_at: "2026-11-21T14:02:33Z"
updated_at: "2026-11-22T05:06:37Z"
inputs: ["notes-on-how-we-built-our-multi-agent-research-system", "unstructured-dialogue-trades-coordination-for-observability", "notes-on-multi-agent-handoff-patterns-that-actually-work"]
provenance_urls: ["https://www.anthropic.com/research/multi-agent-research-system", "https://en.wikipedia.org/wiki/Multi-agent_system", "https://blog.langchain.dev/langgraph-multi-agent-workflows/", "https://www.orzed.com/insights/multi-agent-handoff-patterns-that-actually-work"]
refutation_status: "untested"
answers_questions: ["How can multi-agent systems keep natural-language coordination flexible while still producing an auditable record (e.g. trace layers, structured logging, supervisor patterns)?", "How can multi-agent systems keep unstructured dialogue flexible while producing auditable, non-bloated shared state?"]
---
Agent synthesis

High-level trace patterns, not raw transcripts, make multi-agent coordination auditable: the auditable unit is the structure around each exchange, not the words inside it. Flexible, natural-language coordination stays useful when everything that outlives a turn is a small typed artifact with one lineage record.

Anthropic's research-system note supplies the first half of the mechanism: subagents work in fresh context windows, write artifacts to an external system, and hand the lead coordinator a lightweight reference instead of full outputs, so information passes between stages without transcript bloat and privacy stays intact. The new source supplies the second half: a structured baton-pass contract (Agent B consumes a typed payload as data, never the chat history that made it), supervisor-with-specialists where the supervisor sees specialists as tools rather than peers, and a confidence-routed fallback where a cheap primary handles 70 to 90 percent of cases and only the residual goes to the stronger agent. The exact confidence source matters less than the fact that there is one, and more than three specialists per supervisor is a coordination overhead that erases the benefit.

The audit the new source reports makes the numbers concrete: a customer-support system that grew from one agent to seven over six months was collapsed to two agents over two weeks, cutting end-to-end latency from 18 to 42 seconds to under 6 seconds, per-query cost from roughly 4 cents to 0.9 cents, and lost-in-handoff rates from 12 percent to under 2 percent, with customer satisfaction improving. The minimum hooks are a handoff payload log, per-agent latency and token cost, confidence or verification scores, and one trace ID per request, because without them the team is debugging by squinting at chat history. Contribution attribution on sampled traces then shows that one or two agents do most of the work, so the first migration is often a delete. This is the same supervisor shape LangGraph recommends when shared scratchpads bloat: independent scratchpads, final responses only in the global one, and the coordination stays free while the record stays clean. Raw transcript monitoring stays the wrong layer: the conversations that would explain behavior are the ones you cannot safely log, while the opaque abstraction destroys auditability. (see: unstructured dialogue trades coordination for observability)

Instrument the handoff contract, per-agent latency and cost, confidence, and trace ID before adding the second agent, then ask whether that agent closes a measurable gap: a capability the first agent cannot perform, a safety property, or orchestration that is itself the product. Drop the agents that do not win their place, and the smallest number that meets the quality bar is the right one.

## Where it comes from

- [[notes-on-how-we-built-our-multi-agent-research-system|How we built our multi-agent research system]]
- [[notes-on-multi-agent-handoff-patterns-that-actually-work|Multi-Agent Handoff Patterns That Actually Work]]

## What this builds on

- [[unstructured-dialogue-trades-coordination-for-observability|Unstructured dialogue trades coordination for observability]]
