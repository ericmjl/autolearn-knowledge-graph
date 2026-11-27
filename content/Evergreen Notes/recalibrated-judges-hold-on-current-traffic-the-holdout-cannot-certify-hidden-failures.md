---
type: "evergreen"
title: "Recalibrated judges hold on current traffic; the holdout cannot certify hidden failures"
created_at: "2026-11-27T00:04:45Z"
updated_at: "2026-11-27T00:04:45Z"
inputs: ["notes-on-autorefine-auto-calibrating-code-judges-from-workflow-outcomesthanks-these-authors", "threshold-tuning-survives-rare-failures-only-with-deliberate-oversampling"]
provenance_urls: ["https://arxiv.org/html/2611.09291v1", "https://mlflow.org/articles/llm-judge-calibration/", "https://hamel.dev/blog/posts/decision-model-evals/", "https://hamel.dev/blog/posts/evals/", "https://arxiv.org/abs/2407.01502"]
refutation_status: "untested"
answers_questions: ["Once a rare-failure calibration set is rebalanced, how do you recalibrate the judge and report the tuned threshold's uncertainty, and does the natural-distribution holdout fully de-risk the decision?"]
---
Agent synthesis

A recalibrated judge survives the rare-failure problem that threshold tuning cannot: rebalancing the training set for failures, rewriting the judge's prompt against chance-corrected agreement, and selecting the final prompt on an untouched validation split moves a rubric judge from π 0.36 to 0.60, while even the best threshold picked on the test set itself reaches only 0.42. The mechanism is that a threshold cuts a frozen score while calibration rewrites the criteria that produce the score; the sampled threshold-tuning note fixes the sampling half of the problem (run the calibration set so failures are visible), and the AutoRefine note supplies the second half (balanced prompt edits scored by Scott's π, paired bootstrap intervals, and a separate uncurated validation split). Reported as paired intervals rather than point estimates, the gain runs +0.27 to +0.30 in π, with McNemar p at or below 0.013 in every replay.

The natural-distribution holdout does not de-risk the decision by itself. The independent test slice of 17 diffs, never used for training or selection, showed π rising from 0.16 to 0.51 with a paired +0.35 gain and a CI of [0.00, 0.74] that brushes zero; on 16 older diffs from the earlier pipeline the prior judge stayed ahead, which is exactly the drift recalibration exists to track. The sampled note's rule that a tuned threshold must be reported with its interval stays correct, but the interval is only as honest as the distribution underneath it, and a holdout that mixes current and legacy slices hides the loss.

The deeper limit is that failures the judge's view cannot see are invisible even to the holdout. The informed teacher abstained on 12 of 13 hidden-test failures and on none of the 72 passes, engineers blind to outcome and teacher missed nearly every failure, and the reference-free judge still reached only π 0.35 catching 5 of 13. A held-out score answers reliability questions, not whether the judge's inputs carry the evidence; abstention share is the canary, because abstention at scale means the judge needs better inputs rather than a better prompt. Rebalance the training set, recalibrate with balanced edits, select on an uncurated validation split, report the paired interval next to any score, and treat the abstention rate as the falsifier of the holdout's claim (see: threshold tuning survives rare failures only with deliberate oversampling).

## Where it comes from

- [[notes-on-autorefine-auto-calibrating-code-judges-from-workflow-outcomesthanks-these-authors|AutoRefine: Auto-Calibrating Code Judges from Workflow OutcomesThanks: *These authors contributed equally to this work]]

## What this builds on

- [[threshold-tuning-survives-rare-failures-only-with-deliberate-oversampling|Threshold tuning survives rare failures only with deliberate oversampling]]
