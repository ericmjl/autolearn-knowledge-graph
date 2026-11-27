---
type: "source-note"
title: "Notes on: Agent Observability Patterns for Production AI Agents | MLflow"
raw: "agent-observability-patterns-for-production-ai-agents-mlflow"
url: "https://mlflow.org/articles/agent-observability-patterns/"
created_at: "2026-11-27T13:01:11Z"
updated_at: "2026-11-27T13:01:11Z"
---
- Archived full text: [[agent-observability-patterns-for-production-ai-agents-mlflow|Full archived text, with credits]]
- Link: <https://mlflow.org/articles/agent-observability-patterns/>

## What it says

MLflow's agent observability article argues that the unit of behavior for an agent is a decision between one call and the next, so agent observability must reconstruct the path, not just the health of the system. It lays out seven patterns: model the run as a span tree (workflow, agent, model, retrieval, tool, validation, policy, human-approval spans), propagate OpenTelemetry GenAI conventions so traces cross service boundaries, collect four telemetry streams (traces, metrics, logs, evaluations) rather than one, capture the full artifact set (retrieval queries and documents, tool outputs, memory operations, inter-agent messages, final responses), attach evaluation scores to traces with sampled LLM-as-a-judge scorers and weekly review of the lowest-scoring and most expensive traces, alert on behavior drift (cost per run, retry rate, tool-selection drift, eval-score drop) using p95 thresholds from a baseline week, and decide sampling, redaction and retention before launch. It also gives a four-week rollout: trace one agent, add p50/p95 cost and latency metrics, add sampled evaluation, then add behavioral alerts and redaction policy.

## Claims drawn from this source

- **Trace every agent run as a hierarchical span tree.** The trace is the primary artifact, a hierarchical span tree of one task: parent agent invocation nesting model calls, tool executions, memory reads/writes, plus a span for policy decisions and human-approval waits, which explain why a run took four minutes instead of four seconds.
- **Follow shared OpenTelemetry conventions so traces cross service boundaries.** Named operations for agent creation and invocation, workflow invocation, tool execution, retrieval, planning and memory operations let a trace starting in Python continue in a Go service as one run; propagate trace context through every hop and name spans by operation.
- **Collect four streams, not one.** Traces, metrics, logs and evaluations are complementary; with traces and metrics but no evaluation you can tell an agent was fast and cheap and have no idea whether it was right.
- **Capture the full artifact set, not just the LLM call.** Agent traces should record instructions, retrieval queries, retrieved documents, tool calls, tool outputs, memory operations, observations, intermediate claims, inter-agent messages, actions and final responses; most hallucinations in retrieval agents are retrieval failures.
- **Attach evaluation scores to traces.** Log every production run with prompt and model versions as attributes, sample traces for LLM-as-a-judge scoring against narrow written criteria, store scores on the trace, and review the lowest-scoring and most expensive traces weekly, turning real failures into regression test cases.
- **Alert on behavior drift, not only on errors.** Alerts should fire on cost per run, retry rate, tool-selection drift, eval-score drop and policy violations; set thresholds from a baseline week of normal traffic and use p95 latency and p95 cost per task so a few long runs do not hide behind an average.
- **Plan sampling, redaction and retention before launch.** Keep full traces for errors, policy violations, low eval scores and expensive runs, sample the healthy majority, redact personal data and credentials at capture time, treat trace storage like production data, and match retention to internal or regulatory requirements.
- **Roll out tracing, metrics, evaluation and alerts in four weeks.** Week one: trace one agent end to end; week two: add cost and latency at p50 and p95 with a baseline; week three: turn on sampled evaluation with two or three judges; week four: add behavioral alerts and a redaction and retention policy, and review the first low-scoring traces.
