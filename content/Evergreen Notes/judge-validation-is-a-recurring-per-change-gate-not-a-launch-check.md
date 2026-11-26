---
type: "evergreen"
title: "Judge validation is a recurring per-change gate, not a launch check"
created_at: "2026-11-26T01:01:57Z"
updated_at: "2026-11-26T03:02:46Z"
inputs: ["notes-on-fix-llm-judge-consistency-for-engineers-mvvp-mlflow-mlflow", "claim-level-judges-need-repeated-re-validation-not-one-time-calibration", "notes-on-continuous-llm-evaluation-a-practical-guide-for-production-teams-mlflow"]
provenance_urls: ["https://mlflow.org/articles/judge-consistency-llm/", "https://arxiv.org/html/2606.19544v1", "https://langfuse.com/resources/engineering/rag-faithfulness-evaluation", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model", "https://mlflow.org/articles/continuous-llm-evaluation/"]
refutation_status: "untested"
answers_questions: ["How often should claim-level faithfulness judges be re-validated, and what specific triggers should start a re-validation?", "How do calibration loops for eval judges degrade over time as production agents drift, and what maintenance cadence do production teams use?"]
---
Agent synthesis

Judge validation is a recurring per-change gate, not a launch check. A judge that clears kappa 0.61 at launch decays silently the moment the model, prompt, or rubric changes, so the MVVP protocol re-runs the full check on every change, with the calibration set frozen in version control. The continuous-evaluation source adds the cadence underneath the per-change trigger: evaluation runs as three loops, a pre-merge CI loop over a versioned golden dataset, a post-deploy loop that samples live traffic (Airbnb reviews 5% of de-identified daily traffic), and a learning loop that feeds production failures back into the dataset. The mechanism is that judges drift with the same forces as the systems they score: a prompt edit, a model version bump, a new tool or a changed policy all shift behavior without any code change failing, so a judge calibrated at launch is quietly wrong within months. The MLflow source names the operational cadence: review the human-labeled calibration set quarterly, re-check judge agreement afterward, re-run calibration whenever the judge prompt or model changes, refresh the golden set from production failures, and hold out a slice that never gets tuned against, because Goodhart tuning raises scores while real quality stalls. The claim-level note adds the calibration evidence: raw agreement overstates chance-corrected agreement by 33 to 41 points, consistency hides inside a clean-looking score, and reproducibility can coexist with systematic skew. The synthesis neither source states alone: re-validation is not a quarterly audit, it is a per-change CI gate plus a scheduled cadence plus a golden-set discipline, and the artifact the gate produces is a report, not a single number. Gate every release on both the faithfulness score and the validation evidence (see: claim-level judges need repeated re-validation, not one-time calibration). Keep the calibration set frozen, the reports versioned, and treat any model or prompt change as a fresh validation event before the judge touches a decision.

## Where it comes from

- [[notes-on-fix-llm-judge-consistency-for-engineers-mvvp-mlflow-mlflow|Fix LLM Judge Consistency for Engineers: MVVP + MLflow | MLflow]]
- [[notes-on-continuous-llm-evaluation-a-practical-guide-for-production-teams-mlflow|Continuous LLM Evaluation: A Practical Guide for Production Teams | MLflow]]

## What this builds on

- [[claim-level-judges-need-repeated-re-validation-not-one-time-calibration|Claim-level judges need repeated re-validation, not one-time calibration]]
