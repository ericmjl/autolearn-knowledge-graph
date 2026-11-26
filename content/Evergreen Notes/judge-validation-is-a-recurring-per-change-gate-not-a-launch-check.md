---
type: "evergreen"
title: "Judge validation is a recurring per-change gate, not a launch check"
created_at: "2026-11-26T01:01:57Z"
updated_at: "2026-11-26T01:01:57Z"
inputs: ["notes-on-fix-llm-judge-consistency-for-engineers-mvvp-mlflow-mlflow", "claim-level-judges-need-repeated-re-validation-not-one-time-calibration"]
provenance_urls: ["https://mlflow.org/articles/judge-consistency-llm/", "https://arxiv.org/html/2606.19544v1", "https://langfuse.com/resources/engineering/rag-faithfulness-evaluation", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["How often should claim-level faithfulness judges be re-validated, and what specific triggers should start a re-validation?"]
---
Agent synthesis

Judge validation is a recurring per-configuration gate, not a launch check. A judge that clears kappa 0.61 at launch decays silently the moment the model, prompt, or rubric changes, so the MVVP (MLflow's minimum viable validation protocol) runs the full check again on every change, with the calibration set frozen in version control and the run logged as an LLJ card. The new MVVP source supplies the trigger rules and the report format: re-run the three-replicate AB/BA protocol after any model upgrade or rubric tweak, report kappa, position bias, and flip rate with confidence intervals, never ship a judge whose test-retest-above-0.95-with-position-bias-above-0.10 pattern survived, and keep a fully fixed re-calibration cadence rather than waiting for a visible failure. The sampled claim-level note supplies the mechanism: raw agreement overstates chance-corrected agreement by 33 to 41 points, the consistency-bias paradox hides inside a clean-looking score, and reproducibility can coexist with systematic skew. Together, the two notes show that re-validation is not a quarterly audit, it is a per-change CI gate plus a scheduled cadence, and the artifact the gate produces is a report, not a single number. Gate every release on both the faithfulness score and the validation evidence (see: claim-level judges need repeated re-validation, not one-time calibration). Keep the calibration set frozen, the report versioned, and treat any model or prompt change as a fresh validation event before the judge touches a decision.

## Where it comes from

- [[notes-on-fix-llm-judge-consistency-for-engineers-mvvp-mlflow-mlflow|Fix LLM Judge Consistency for Engineers: MVVP + MLflow | MLflow]]

## What this builds on

- [[claim-level-judges-need-repeated-re-validation-not-one-time-calibration|Claim-level judges need repeated re-validation, not one-time calibration]]
