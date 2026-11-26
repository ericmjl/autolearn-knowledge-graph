---
type: "evergreen"
title: "Full execution traces make multi-agent failure attribution work"
created_at: "2026-11-26T07:01:53Z"
updated_at: "2026-11-26T07:01:53Z"
inputs: ["notes-on-seeing-the-whole-elephant-a-benchmark-for-failure-attribution-in-llm-based-multi-agent", "focused-agents-outperform-tool-heavy-monoliths"]
provenance_urls: ["https://arxiv.org/html/2604.22708v1", "https://blog.langchain.dev/langgraph-multi-agent-workflows/", "https://en.wikipedia.org/wiki/Multi-agent_system"]
refutation_status: "untested"
answers_questions: ["When tool-heavy monoliths fail, what does decomposition change about evaluation: which agent gets blamed when the graph fails?"]
---
Agent synthesis

Full execution traces, not output-only logs, are what make multi-agent failure attribution work. A graph of focused agents gains specialization, independent evaluation, and independent improvement over a monolith, but that decomposition only pays off if the graph can say which agent and which step failed when it does. TracElephant measures this directly: complete traces yield 65.9% agent-level and 30.3% step-level attribution accuracy, up 22% and 76% respectively from output-only traces, and a replayable environment adds another 10% at step level through counterfactual probing of candidate failure steps.

The mechanism is observability, not attribution cleverness. The decisive step is the earliest point failure becomes inevitable, and a recoverable upstream mistake is attributed to the verifier or orchestrator whose responsibility was missed, not to the agent that made the mistake. Output-only logs cannot see this: analysis of the Who&When benchmark's 184 failure cases shows developers fail attribution on at least 21% of instances from outputs alone, and step-level attribution drops 76% versus 22% for agent-level when metadata and inputs are missing. The attribution unit is the functional component, not the agent id, so a single-agent scaffold with planning, orchestration, and tool-use modules behaves like a small multi-agent system for this task.

The evidence cuts both ways. Focused agents, evaluated and improved independently, are exactly what a diagnostic loop needs, but the diagnostic loop silently degrades to guessing if the graph only records outputs; early-phase failures in Magentic-One are attributed at 8% in the first third of steps, because early errors such as a bad decomposition only surface after downstream execution fails, while late-phase failures attribute at 52%. Step position, agent type, and architecture all shift accuracy, so architecture-aware attribution is the direction rather than a universal black box. One caveat the benchmark raises: the authors could not reproduce ECHO, AgenTracer, GraphTracer, or FAMAS numbers, so published claims about those tools should not be trusted without independent numbers.

If you build a decomposed graph, instrument it with full step-level traces, capture the exact inputs each component saw, and keep a replayable environment; otherwise the isolated-evaluation benefit of focused agents is an optimization whose failures you cannot localize. Start with output-only evaluation, add full tracing, and treat attribution accuracy, not task success, as the gate on each agent's improvement cycle (see: focused agents outperform tool-heavy monoliths).

## Where it comes from

- [[notes-on-seeing-the-whole-elephant-a-benchmark-for-failure-attribution-in-llm-based-multi-agent|Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM-based Multi-Agent Systems]]

## What this builds on

- [[focused-agents-outperform-tool-heavy-monoliths|Focused agents outperform tool-heavy monoliths]]
