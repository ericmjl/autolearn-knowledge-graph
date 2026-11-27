---
type: "evergreen"
title: "Judge validation is a recurring per-change gate plus a drift loop, not a launch check"
created_at: "2026-11-26T01:01:57Z"
updated_at: "2026-11-27T01:03:17Z"
inputs: ["notes-on-fix-llm-judge-consistency-for-engineers-mvvp-mlflow-mlflow", "claim-level-judges-need-repeated-re-validation-not-one-time-calibration", "notes-on-continuous-llm-evaluation-a-practical-guide-for-production-teams-mlflow", "notes-on-the-lifecycle-of-llm-as-a-judge-for-large-scale-recommendation-explanations", "calibrated-judges-not-trusted-ones-keep-evaluation-honest"]
provenance_urls: ["https://mlflow.org/articles/judge-consistency-llm/", "https://arxiv.org/html/2606.19544v1", "https://langfuse.com/resources/engineering/rag-faithfulness-evaluation", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model", "https://mlflow.org/articles/continuous-llm-evaluation/", "https://arxiv.org/html/2608.18300v3", "https://builder.aws.com/content/3H8qTeKHyPXyLX8Nf8HTElUBZJR/a-practitioners-guide-to-llm-as-a-judge-calibration-on-amazon-bedrock", "https://arxiv.org/html/2605.29442v1", "https://arxiv.org/abs/2401.07339", "https://addyosmani.com/blog/ai-coding-workflow/", "https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/"]
refutation_status: "untested"
answers_questions: ["How often should claim-level faithfulness judges be re-validated, and what specific triggers should start a re-validation?", "How do calibration loops for eval judges degrade over time as production agents drift, and what maintenance cadence do production teams use?", "When should a calibrated judge be re-validated after the generator, prompt distribution, or catalogue changes, and what signals should trigger re-calibration?"]
---
Agent synthesis

Judge validation is a recurring per-change gate plus a drift loop, not a launch check. A judge calibrated at launch is quietly wrong within months when the model, prompt, tool, or policy shifts, so production teams run three loops: a pre-merge CI gate over a versioned golden set, a post-deploy loop that samples live traffic, and a learning loop that feeds production failures back into the dataset. The lifecycle source makes the mechanism concrete: a class-balanced, rationale-annotated benchmark of about 900 human-labeled explanations refreshed from live traffic, one tuned judge serving both the quality gate and the revision-loop critic, and a weekly human-in-the-loop loop that samples about 300 generated explanations stratified across served-without-revision, served-after-revision, and dropped outcomes, biased toward newer catalog items. The acceptance band is relative to human disagreement, not a fixed threshold: each explanation gets at least three raters, and the judge must score no worse than two standard deviations below the mean rater on each metric, computed on the full sample and separately on newly added titles, which turns the gate into a shift detector rather than a generic regression test. A sustained drop in the k=0 pass rate signals a generator-side regression rather than judge drift, and when drift fires the new rubric is staged behind a human review gate with the previous rubric retained for rollback. Raw agreement cannot carry this check either: chance-corrected agreement overstates reliability by 33 to 41 percentage points, and a stable judge can pass conventional validation while consistently measuring the wrong thing. (see: calibrated judges, not trusted ones, keep evaluation honest) Keep the calibration set frozen and versioned, gate releases on both the score and the validation evidence, and never read an output from an unvalidated judge as ground truth.

## Where it comes from

- [[notes-on-fix-llm-judge-consistency-for-engineers-mvvp-mlflow-mlflow|Fix LLM Judge Consistency for Engineers: MVVP + MLflow | MLflow]]
- [[notes-on-continuous-llm-evaluation-a-practical-guide-for-production-teams-mlflow|Continuous LLM Evaluation: A Practical Guide for Production Teams | MLflow]]
- [[notes-on-the-lifecycle-of-llm-as-a-judge-for-large-scale-recommendation-explanations|The Lifecycle of LLM-as-a-Judge for Large-Scale Recommendation Explanations]]

## What this builds on

- [[claim-level-judges-need-repeated-re-validation-not-one-time-calibration|Claim-level judges need repeated re-validation, not one-time calibration]]
- [[calibrated-judges-not-trusted-ones-keep-evaluation-honest|Calibrated judges, not trusted ones, keep evaluation honest]]
