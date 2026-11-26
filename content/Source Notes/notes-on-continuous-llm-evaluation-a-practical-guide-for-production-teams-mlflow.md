---
type: "source-note"
title: "Notes on: Continuous LLM Evaluation: A Practical Guide for Production Teams | MLflow"
raw: "continuous-llm-evaluation-a-practical-guide-for-production-teams-mlflow"
url: "https://mlflow.org/articles/continuous-llm-evaluation/"
created_at: "2026-11-26T03:01:23Z"
updated_at: "2026-11-26T03:01:23Z"
---
- Archived full text: [[continuous-llm-evaluation-a-practical-guide-for-production-teams-mlflow|Full archived text, with credits]]
- Link: <https://mlflow.org/articles/continuous-llm-evaluation/>

## What it says

MLflow's guide treats LLM evaluation as a continuous function of development and operations, not a release gate. It builds the program in three loops: a pre-merge CI loop over a versioned golden dataset, a post-deploy loop that samples live traffic and flags low-scoring traces, and a learning loop that turns failures into new test cases. Calibration of LLM judges against human labels is the load-bearing step, and the guide names the operational risks: Goodhart effects from tuning only on the golden set, stale labels on the human-labeled calibration set (reviewed quarterly), judge model changes that require re-running calibration before trusting trend lines, and quiet growth in judge cost.

## Claims drawn from this source

- **Continuous evaluation runs three loops: pre-merge CI, post-deploy sampled monitoring, and a learning loop.** In day-to-day terms, continuous evaluation has three loops: pre-merge runs every prompt/model/tool change against an offline dataset in CI; post-deploy scores a sample of live traffic automatically and flags low-scoring traces; learning loop turns production failures into new test cases so the suite grows with real failure modes.
- **Golden datasets should be small, include failures, and be stratified.** Airbnb's engineering team recommends a golden dataset of 50 to 100 examples that includes bad examples; prefer real traces over synthetic ones; stratify by intent, difficulty and observed failure mode; treat the dataset like code so scores are comparable across commits.
- **LLM judges need calibration against human labels before being trusted.** An uncalibrated judge is a second black box stacked on the first. Airbnb runs virtual judges against a golden dataset, measures agreement with human labels, and refines judge prompts until agreement reaches a target in the high 80s to 90s percent; humans disagree with each other too, so perfect agreement is not realistic.
- **CI gates should fail on calibrated, user-harm scorers compared per-scorer against a baseline.** Compare to the main branch baseline per scorer, not on average, since an average can hide a collapse in one intent; print which scorer dropped, on which cases, with links to the traces; keep the gate fast by caching LLM and tool responses and running a small smoke subset on every commit with the full suite on merge or nightly.
- **Production evaluation samples live traffic and routes flagged traces to a human review queue.** Airbnb describes sampling 5% of live, de-identified traffic daily, running programmatic checks and virtual judges on it, and surfacing flagged outputs for human review; a queue of low-scoring traces reviewed weekly is the cheapest source of new test cases.
- **Goodhart effects push teams to tune prompts against the golden set while real quality stalls.** If you tune a prompt only against the golden set, scores rise while real quality stalls; refresh the set with new production cases regularly and hold out a slice you never tune against.
- **Calibration sets go stale and judges drift, so recalibration is a scheduled maintenance task.** Policies change; review the human-labeled calibration set on a schedule, quarterly is a common cadence in layered evaluation guidance, and re-check judge agreement afterward; if the model behind your judge is updated, re-run calibration before trusting trend lines.
- **After rollout, the work is maintenance: add cases, retire obsolete ones, recalibrate on a schedule, tighten thresholds.** The 30-day rollout ends with 'the work is maintenance: add cases, retire obsolete ones, recalibrate on a schedule and tighten thresholds as quality improves.'
