---
type: "evergreen"
title: "High-level trace patterns, not raw transcripts, make multi-agent coordination auditable"
created_at: "2026-11-21T14:02:33Z"
updated_at: "2026-11-21T14:02:33Z"
inputs: ["notes-on-how-we-built-our-multi-agent-research-system", "unstructured-dialogue-trades-coordination-for-observability"]
provenance_urls: ["https://www.anthropic.com/research/multi-agent-research-system", "https://en.wikipedia.org/wiki/Multi-agent_system", "https://blog.langchain.dev/langgraph-multi-agent-workflows/"]
refutation_status: "untested"
answers_questions: ["How can multi-agent systems keep natural-language coordination flexible while still producing an auditable record (e.g. trace layers, structured logging, supervisor patterns)?"]
---
Agent synthesis

High-level trace patterns, not raw transcripts, make multi-agent coordination auditable. Flexible natural-language coordination stays useful when the record of it is structural, not conversational: agents stay free to negotiate and pivot, while production tracing, decision-pattern monitoring, and filesystem-backed artifacts turn the run into a replayable ledger.

Anthropic's Research system shows both halves. Agents there make dynamic decisions and are non-deterministic run to run, so the team added full production tracing to diagnose why agents failed (bad search queries, poor sources, tool failures), then monitored agent decision patterns and interaction structures without monitoring individual conversation contents, keeping user privacy intact. Subagents do not chat their outputs through the lead coordinator either. They write structured artifacts (code, reports, data) to external systems and hand the coordinator a lightweight reference, which prevents information loss across stages and cuts token overhead from copying large outputs through conversation history.

Each subagent works in its own context window, condenses key tokens, and returns condensed findings to the lead, so the coordination stays flexible without the shared record becoming opaque. Raw transcript monitoring is the wrong layer: the conversations that would explain behavior are the ones you cannot safely log, while the opaque abstraction destroys auditability. Build the audit trail at the level of structure (traces, decisions, filesystem artifacts) and keep the dialogue free. (see: unstructured dialogue trades coordination for observability)

## Where it comes from

- [[notes-on-how-we-built-our-multi-agent-research-system|How we built our multi-agent research system]]

## What this builds on

- [[unstructured-dialogue-trades-coordination-for-observability|Unstructured dialogue trades coordination for observability]]
