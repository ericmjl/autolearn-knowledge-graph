---
type: "source-note"
title: "Notes on: LLM Judge Calibration: Measure, Correct and Report | MLflow"
raw: "llm-judge-calibration-measure-correct-and-report-mlflow"
url: "https://mlflow.org/articles/llm-judge-calibration/"
created_at: "2026-11-22T23:01:55Z"
updated_at: "2026-11-22T23:01:55Z"
---
- Archived full text: [[llm-judge-calibration-measure-correct-and-report-mlflow|Full archived text, with credits]]
- Link: <https://mlflow.org/articles/llm-judge-calibration/>

## What it says

MLflow's guide on calibrating LLM-as-a-judge: a judge is a classifier whose verdicts need to be checked against human labels, with two jobs (alignment and statistical correction), a deliberately built human-labeled calibration set, chance-corrected agreement, bias testing, calibrated reporting with error bars, and re-measurement whenever the judge, prompt, or task changes. Rare failures are the sharp edge: if failures are rare, the set must oversample them or the false-negative rate cannot be estimated at all.

## Claims drawn from this source

- **An LLM judge is a classifier with a true positive rate and a false positive rate.** The judge reads an output and returns a label: pass or fail, a 1 to 5 score, or a preference between two answers. If it passes 90% of outputs, that does not mean 90% are good, it just means the judge said so.
- **Two related jobs: alignment and statistical correction.** Alignment changes the judge (rubric, examples, model, optimizer) so verdicts match trusted humans. Statistical correction leaves the judge as is, estimates its error rates from labeled data, and adjusts the reported metric and its uncertainty. Alignment raises the ceiling; correction keeps reported numbers honest.
- **If failures are rare, the calibration set must oversample them.** Class balance: if failures are rare, you need enough of them in the set to estimate the false-negative rate at all. Oversample failures on purpose.
- **Use chance-corrected agreement, not raw accuracy.** Raw percent agreement flatters you when one label dominates (a judge that always says good scores 95% agreement on a 95% good set). Cohen's kappa for two raters and Fleiss' kappa for three or more, with iteration on the rubric when kappa falls below about 0.61.
- **Agreement can hide structured bias; test for it directly.** Test position bias by running every pair in AB and BA order and counting flips, verbosity bias by comparing scores on paired short and long answers, fluency bias with correct-but-rough and wrong-but-polished cases, and leniency by checking the false-positive rate against humans. A 2026 Berkeley study describes a consistency-bias paradox: test-retest reliability above 0.95 can coexist with position bias above 0.10.
- **Keep a holdout separate from tuning data.** Split the set into development and a fresh holdout you never touch until you measure. Tuning on test labels gives an optimistic number that fails in production. Chrome's guidance recommends expert-labeled data, a fresh holdout, and measuring human-human agreement first.
- **Report calibrated results with error bars and calibration conditions.** Report the number of evaluation questions and the standard error next to each mean, with a normal-approximation 95% interval (plus or minus 1.96 times its standard error), carrying the judge's own uncertainty too. Name the judge model, prompt version, calibration set size and agreement figures next to the score.
- **Re-run calibration when the judge model, prompt, or task changes.** Calibration decays: a provider update or a swap to a cheaper model changes error rates, even small wording edits can move agreement, and new user intents or tools push outputs outside what the set covered.
