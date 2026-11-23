---
type: "evergreen"
title: "Threshold tuning survives rare failures only with deliberate oversampling"
created_at: "2026-11-22T23:02:54Z"
updated_at: "2026-11-22T23:02:54Z"
inputs: ["notes-on-llm-judge-calibration-measure-correct-and-report-mlflow", "tune-decision-model-thresholds-and-calibration-before-trusting-eval-scores"]
provenance_urls: ["https://mlflow.org/articles/llm-judge-calibration/", "https://hamel.dev/blog/posts/decision-model-evals/", "https://hamel.dev/blog/posts/evals/", "https://arxiv.org/abs/2407.01502"]
refutation_status: "untested"
answers_questions: ["Does decision-model threshold tuning still hold when failures are rare and classes are extremely imbalanced?"]
---
Agent synthesis

Threshold tuning survives rare failures only when the calibration set oversamples them; without enough failures in the set, the false-negative rate is invisible and the tuned threshold is tuned on fiction. The mechanism is sampling economics: at a 0.5% failure rate, a 1,000-example set holds about five failures, so precision, recall, and the tuned threshold all rest on a handful of points and move with the resampling. The MLflow calibration guide makes the requirement concrete: if failures are rare, you need enough of them in the set to estimate the false-negative rate at all, and you must oversample failures on purpose; chance-corrected kappa, not raw accuracy, is needed because raw agreement flatters a judge that always says good on a 95%-good set.

The prior eval discipline note made the loop concrete: minimum precision and recall tied to the business, stratified cross-validation over saved scores, calibration checks, and Platt scaling when calibration is poor. It assumed labels drawn from the natural production distribution and graded the judge on that same distribution. The new source shows the two moving parts must be fixed in order: resample the set for rare failures, tune on the rebalanced data, then validate on an untouched holdout that reflects the natural distribution, with the tuned threshold reported alongside its interval. Read the confusion matrix, not the summary; whether the judge errs toward false passes or false failures decides what to do next.

A rare-failure decision model tuned on natural traffic hides exactly the failures it exists to catch; tuned on a rebalanced set and validated on a holdout, the same judge earns its keep. Report the calibration conditions next to the score: the judge model, prompt version, set size, and agreement figures. When a failure mode is rare, budget the first effort for the calibration set, not the threshold (see: decision models stay useful only after thresholds and calibration are tuned against labeled data).

## Where it comes from

- [[notes-on-llm-judge-calibration-measure-correct-and-report-mlflow|LLM Judge Calibration: Measure, Correct and Report | MLflow]]

## What this builds on

- [[tune-decision-model-thresholds-and-calibration-before-trusting-eval-scores|Tune decision-model thresholds and calibration before trusting eval scores]]
