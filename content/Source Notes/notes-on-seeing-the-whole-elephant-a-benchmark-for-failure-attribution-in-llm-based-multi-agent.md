---
type: "source-note"
title: "Notes on: Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM-based Multi-Agent Systems"
raw: "seeing-the-whole-elephant-a-benchmark-for-failure-attribution-in-llm-based-multi-agent"
url: "https://arxiv.org/html/2604.22708v1"
created_at: "2026-11-26T07:01:17Z"
updated_at: "2026-11-26T07:01:17Z"
---
- Archived full text: [[seeing-the-whole-elephant-a-benchmark-for-failure-attribution-in-llm-based-multi-agent|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2604.22708v1>

## What it says

TraceElephant is a failure attribution benchmark for LLM-based multi-agent systems built under full execution observability, rather than the output-only traces used by existing benchmarks such as Who&When. It collects 220 annotated failure traces from three representative systems (Captain-Agent, Magentic-One, SWE-Agent), records step-level inputs, outputs, tool invocations, agent configurations, and architecture, and ships each trace with a reproducible environment for replay and counterfactual probing. Full traces improve attribution accuracy by 22% at the agent level and 76% at the step level over output-only traces, and with the running environment, step-level accuracy improves a further 10%. Step-level attribution is far more sensitive to missing information than agent-level attribution.

## Claims drawn from this source

- **Full traces beat output-only traces.** Complete trace information yields 65.9% agent-level and 30.3% step-level accuracy, an improvement of 22% at agent level and 76% at step level over output-only traces.
- **Replayable environments add more.** With the running environment, step-level accuracy improves by another 10%, through counterfactual probing of candidate failure steps.
- **Step-level attribution is more fragile.** Step-level attribution suffers a 76% accuracy drop from output-only inputs vs. 22% for agent-level, showing that localizing the precise failure step depends on the exact decision context of each call.
- **Missing inputs obscure failures.** Analysis of Who&When's 184 failure cases showed developers cannot reliably perform attribution from output-only logs in at least 21% of instances; with full inputs the ambiguity mostly resolves.
- **Attribution must be role- and recoverability-aware.** The decisive failure step is the earliest point failure becomes inevitable, and recoverable upstream mistakes are attributed to the verifier or orchestrator whose responsibility was missed, not to the upstream agent.
- **Early-phase failures are hard to attribute.** For Magentic-One, step-level accuracy is 8% early, 19% mid, and 52% late, because early errors such as incorrect decomposition only surface after subsequent execution fails.
- **Attribution is architecture-aware.** Performance varies across MAS architectures, agent types, and step positions, so architecture-aware attribution approaches are needed.
- **Reproduction of prior techniques failed.** The authors attempted to reproduce ECHO, AgenTracer, GraphTracer and FAMAS reported numbers but could not match them, so they are not included in the evaluation.
