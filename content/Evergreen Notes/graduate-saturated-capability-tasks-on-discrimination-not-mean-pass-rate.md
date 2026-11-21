---
type: "evergreen"
title: "Graduate saturated capability tasks on discrimination, not mean pass rate"
created_at: "2026-11-21T23:06:23Z"
updated_at: "2026-11-21T23:06:23Z"
inputs: ["notes-on-your-eval-suite-has-a-variance-problem-before-it-has-a-score-problem", "capability-evals-climb-regression-suites-hold-the-line"]
provenance_urls: ["https://vectoryai.com/blog/eval-variance-pass-at-k-and-suite-saturation/", "https://www.anthropic.com/research/demystifying-evals-for-ai-agents", "https://hamel.dev/blog/posts/evals/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["When capability eval tasks saturate, is there a principled rule for graduating them into regression suites, and what happens when they don't?"]
---
Agent synthesis

Saturated capability evals must graduate into the regression suite on discrimination, not on mean pass rate. The mechanism is that a suite exists to answer a release question, and the question fails the moment the suite stops separating the candidate from the baseline. The new source note shows the operational form of this rule: watch the gap between candidate and baseline, not the average. A capability suite reporting 0.98 mean pass rate with 0.01 separation has stopped answering the release question, whatever its headline says. Graduate those tasks into the regression suite where a near-perfect rate is the point, and author harder capability tasks drawn from real failures, with 20-50 simple tasks as a strong start. Retire a task only when the product behavior it covers no longer exists.

The source note adds three operational layers to the two-role stack in the existing layered-evals evergreen. First, the metric must be pre-committed: pass@k when retry is free and invisible to the user, pass^k when a single failure is user-visible or writes state, and both published when the stakes are high; at a 75 percent per-trial rate, pass^3 is roughly 42 percent, which no single average can show. Second, a floor score is a broken task until proven otherwise: a 0% pass rate across many trials, or a CORE-Bench-style precision bug where an answer of 96.12 is marked wrong against 96.124991, calls for three transcripts read end to end before any model ticket opens. Third, contamination looks identical to improvement: shared workspace, git history left behind by earlier trials, and harness version drift (mini-SWE-agent 1.x parsing actions from output strings while 2.x uses tool calling, with temperature pinned at 0.0 in 1.x) all manufacture gains, so reset and pin every run and treat any unexplained jump as a contamination hypothesis.

The layers converge on one rule the two inputs do not state alone: saturation is a discrimination failure, not a headline failure. The existing evergreen teaches where capability tasks sit (low-pass, cheap, frequent) and when to graduate; the new source note turns the graduation trigger from "pass consistently" into "stops separating candidate from baseline," and ties it to pre-committed metrics, pre-registered trial counts, and contamination checks. A task at 99 percent with healthy separation is not saturated and should stay in the capability layer; a task at 95 percent with zero separation is saturated and belongs in regression. Measure discrimination on every plateau and graduate tasks when it collapses, never on the mean alone.

## Where it comes from

- [[notes-on-your-eval-suite-has-a-variance-problem-before-it-has-a-score-problem|Your eval suite has a variance problem before it has a score problem]]

## What this builds on

- [[capability-evals-climb-regression-suites-hold-the-line|Capability evals climb; regression suites hold the line]]
