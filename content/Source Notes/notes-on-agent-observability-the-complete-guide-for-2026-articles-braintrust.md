---
type: "source-note"
title: "Notes on: Agent observability: The complete guide for 2026 - Articles - Braintrust"
raw: "agent-observability-the-complete-guide-for-2026-articles-braintrust"
url: "https://www.braintrust.dev/articles/agent-observability-complete-guide-2026"
created_at: "2026-11-28T10:01:03Z"
updated_at: "2026-11-28T10:01:03Z"
---
- Archived full text: [[agent-observability-the-complete-guide-for-2026-articles-braintrust|Full archived text, with credits]]
- Link: <https://www.braintrust.dev/articles/agent-observability-complete-guide-2026>

## What it says

Braintrust argues that agent observability is the layer that captures every step an AI agent takes - tool calls, reasoning, state transitions, and memory operations - and that tracing alone does not make an agent correct; only a loop that scores live production traces and feeds failures back into the eval suite turns debugging into a continuous quality loop.

## Claims drawn from this source

- **Traditional APM cannot see agent quality.** APM can confirm a request returned a 200, but it cannot show that the agent looped twice, called the wrong tool, or hallucinated a billing policy.
- **Agent traces need four typed span types.** Tool-call spans, reasoning spans, state-transition spans, and memory-operation spans map directly to four failure modes, so the surface where a failure shows up is the surface where you fix it.
- **Online evaluation scores live traces.** Inline scorers, LLM-as-a-judge checks, and rule-based assertions run on live traces so quality regressions surface as they happen, not after a customer complaint.
- **Production failures become eval cases.** The feedback loop converts production traces that fail an online scorer into eval cases, so the eval suite grows from real user behavior rather than a fixed golden set.
- **The same scorers run offline and in CI.** Offline evaluation runs the agent against a curated dataset before deployment, and the same evaluation definitions run locally, in CI, and in production so quality checks stay consistent.
- **CI gates enforce quality before release.** A GitHub Action runs evals on every pull request and blocks merges that drop quality below a configured threshold.
- **Multi-agent handoffs need parent-child span propagation.** Each handoff payload is recorded as a span on the parent agent's trace so Agent B's run nests under it and a single trace shows the planning agent, handoff, and sub-agent tool calls.
- **Rollout order matters.** Day 1 is trace capture, week 1 adds production context and early failure conversion, month 1 adds online scoring on a sample, and quarter 1 gates releases in CI.
