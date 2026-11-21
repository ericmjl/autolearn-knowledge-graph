---
type: "source-note"
title: "Notes on: Your eval suite has a variance problem before it has a score problem"
raw: "your-eval-suite-has-a-variance-problem-before-it-has-a-score-problem"
url: "https://vectoryai.com/blog/eval-variance-pass-at-k-and-suite-saturation/"
created_at: "2026-11-21T23:04:17Z"
updated_at: "2026-11-21T23:04:17Z"
---
- Archived full text: [[your-eval-suite-has-a-variance-problem-before-it-has-a-score-problem|Full archived text, with credits]]
- Link: <https://vectoryai.com/blog/eval-variance-pass-at-k-and-suite-saturation/>

## What it says

The Vectory field note argues that eval suites fail on variance and discrimination before they fail on score: a single run is a sample, not a score, so trial counts and a named metric must be stated before results are read. It distinguishes pass@k (at least one success in k attempts) from pass^k (all k trials succeed), and says a 0% rate is usually a broken task, an ambiguous task shows up as scatter, and contamination between trials masquerades as improvement. Its central claim for suite lifecycles: saturation is a suite failure, not a milestone, so a capability suite that no longer separates candidate from baseline must graduate its tasks into the regression suite and author harder capability tasks, retiring a task only when the product behavior it covers no longer exists.

## Claims drawn from this source

- **One run is a sample, not a score.** The note argues that if you cannot tell whether a drop from 0.88 to 0.79 is a regression or noise, you lack trials and a named metric; a run manifest should record task_id, suite_version, trials, metric, model_id, temperature, seed, and harness_version before results are read.
- **pass@k and pass^k measure different product promises.** pass@k rises with k (at least one of k attempts succeeds) while pass^k falls with k; with a 75% per-trial rate, pass^3 is roughly 42%. Gate on pass@k when retry is free and invisible, gate on pass^k when a single failure is user-visible or writes state.
- **A 0% pass rate is usually a broken task, not a capability gap.** A 0% pass rate across many trials, such as 0% pass@100, is most often a signal of a broken task; a CORE-Bench case marked a 96.12 answer wrong because the expected value was 96.124991, so grader precision must be read against transcripts.
- **Ambiguous tasks show up as variance, not as errors.** Underspecified tasks fail sometimes and read as flakiness; the two-expert test (would two domain experts agree on pass/fail) is the quality bar, and a Terminal-Bench audit found undeserved failures from unspecified script filepaths.
- **Contamination between trials looks exactly like improvement.** A Claude run gained an advantage reading git history left by earlier trials, and SWE-bench Verified results from mini-SWE-agent 1.x and 2.x are not comparable because 1.x parsed actions from output strings while 2.x uses tool calling; reset workspace and pin harness and sampling versions, treating any unexplained score jump as a contamination hypothesis.
- **Saturation is a suite failure, not a milestone.** Anthropic's guidance is that capability evals start at a low pass rate while regression evals sit near 100%, and a saturated capability eval can graduate into the regression suite; discrimination, not the mean, is the number to watch, so a capability suite at 0.98 with 0.01 separation must graduate its tasks.
- **The graduation rule and suite retirement criteria.** Saturated tasks graduate into regression where near-perfect rates are the point; new capability tasks come from real failures (20-50 simple tasks as a strong start), and a task is retired only when the product behavior it covers no longer exists.
- **The reporting contract next to the score.** Every reported score carries trial count and metric name, an interval or spread, cost and token usage beside quality, and suite/harness/model/grader versions plus known gaps.
