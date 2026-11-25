---
type: "evergreen"
title: "Repeated paired trials beat single-run release gates"
created_at: "2026-11-25T01:01:30Z"
updated_at: "2026-11-25T01:01:30Z"
inputs: ["notes-on-stop-flaky-ai-agent-evals-from-gating-releases", "eval-graders-should-turn-scores-into-a-baseline-decision-not-a-headline"]
provenance_urls: ["https://makeyouragent.ai/blog/stop-flaky-ai-agent-evals-release-gates", "https://www.endorlabs.com/learn/why-evals-are-the-missing-layer-in-integration-testing", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339"]
refutation_status: "untested"
answers_questions: ["How do non-deterministic graders behave under repeat sampling: what flip rates are tolerable and when should a regression be auto-blocked?"]
---
Agent synthesis

Repeated paired trials beat single-run release gates, because one stochastic attempt cannot support a release verdict. The flaky-gate article argues that the model, the grader, the fixture, and the provider all vary, so an aggregate score is one draw from several distributions. It separates statistical trials from operational retries, pins every behavior-affecting input into an immutable manifest, pair-compares baseline and candidate on the same cases and fixtures, computes per-slice effects before the aggregate, spends extra repetitions only on unresolved slices, and returns pass, fail, or inconclusive from a tamper-evident evidence receipt.

The existing grader-design note attacks the same problem one layer in: that a grader should turn scores into a baseline decision, not a headline. It already demands repeat sampling, person-gated losses, and stability gating. The flaky-gate article generalizes that: the gate is the measurement instrument, and its decision rule must never convert an inconclusive result into a pass. Inconclusive is the honest verdict when a critical slice crosses a boundary with too little evidence, never the safety blanket for a flaky suite. Together they show that grader design and gate design are the same discipline: both hide the mismatch between the metric and the decision until repeat sampling, pairing, slice-level accounting, and honest refusal to conclude are in place. (see: eval graders turn scores into baseline decisions, not headlines)

The operational sequence is concrete: run the release against itself first with three paired trials per case, then set a practical regression margin and a bounded inconclusive policy, then inject a known regression into one high-risk slice and confirm the gate fails even with a flat global average. Track false blocks, regressions missed, and inconclusive rate over time; a rising inconclusive rate means the suite lacks power, the system became more variable, or the margin is tighter than the budget can support. Never rerun CI until green; a gate needs one evidence policy, not a contest between random outcomes.

## Where it comes from

- [[notes-on-stop-flaky-ai-agent-evals-from-gating-releases|Stop Flaky AI Agent Evals From Gating Releases]]

## What this builds on

- [[eval-graders-should-turn-scores-into-a-baseline-decision-not-a-headline|Eval graders should turn scores into a baseline decision, not a headline]]
