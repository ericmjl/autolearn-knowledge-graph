---
type: "source-note"
title: "Notes on: Stop Flaky AI Agent Evals From Gating Releases"
raw: "stop-flaky-ai-agent-evals-from-gating-releases"
url: "https://makeyouragent.ai/blog/stop-flaky-ai-agent-evals-release-gates"
created_at: "2026-11-25T01:01:06Z"
updated_at: "2026-11-25T01:01:06Z"
---
- Archived full text: [[stop-flaky-ai-agent-evals-from-gating-releases|Full archived text, with credits]]
- Link: <https://makeyouragent.ai/blog/stop-flaky-ai-agent-evals-release-gates>

## What it says

The article argues that a single stochastic eval run cannot support a release verdict and prescribes a paired, repeated, slice-aware gate: separate statistical trials from retries, pin the eval in an immutable manifest, pair baseline and candidate trials on the same cases and fixtures, measure risk slices before the aggregate, spend extra trials only where uncertainty remains, and return pass/fail/inconclusive from a tamper-evident evidence receipt rather than an average score.

## Claims drawn from this source

- **A single eval run cannot support a release verdict.** The model, grader, retrieved data, and rate limits all vary, so an aggregate score is one draw from several distributions, not a stable measurement.
- **Release gates must separate trials from retries.** A statistical trial is a deliberate independent observation; a retry is an operational attempt to complete one. Logical trial IDs keep retries separate from repetitions so a timeout-then-success does not inflate reliability or sample size.
- **Baseline and candidate must be paired on the same cases and fixtures.** Pairing reduces noise from case-difficulty differences and prevents a different random task sample from measuring the sample instead of the release.
- **Measure risk slices before the aggregate.** An aggregate can stay flat while a critical workflow degrades; minimum sample policies mark thin slices inconclusive instead of letting easy cases overrule ten payments cases.
- **Repeat budget should be allocated where uncertainty remains.** A bounded sequential policy recomputes paired effects at each checkpoint, stops slices that clearly pass or fail, and sends next trials to unresolved slices, with a deterministic and versioned allocation rule.
- **The decision comes from a signed evidence receipt, not a dashboard.** The receipt carries the manifest digest, trial counts with reason codes, per-slice effects and uncertainty, decision margin, budget consumed, grader release, and final pass/fail/inconclusive outcome. A deterministic safety invariant blocks immediately regardless of the confidence interval.
- **Inconclusive must not be converted into a pass.** Do-not-convert-inconclusive-into-pass simply restores the one-shot failure under a more elaborate name.
- **The gate itself must be tested and tracked.** Controlled-defect tests (self-comparison, injected regressions, forced retries, fixture drift, budget exhaustion) verify the gate, and time-series tracking of false blocks, regressions missed, inconclusive rate, and repeat cost tells you whether the suite has the power it needs.
