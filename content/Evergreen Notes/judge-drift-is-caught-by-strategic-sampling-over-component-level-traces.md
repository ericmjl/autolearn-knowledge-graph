---
type: "evergreen"
title: "Judge drift is caught by strategic sampling over component-level traces"
created_at: "2026-11-27T03:02:03Z"
updated_at: "2026-11-27T03:02:03Z"
inputs: ["notes-on-evaluating-llms-in-production-from-drift-detection-to-continuous-monitoring", "judge-validation-is-a-recurring-per-change-gate-not-a-launch-check"]
provenance_urls: ["https://wandb.ai/site/articles/evaluating-llms-in-production/", "https://mlflow.org/articles/judge-consistency-llm/", "https://arxiv.org/html/2606.19544v1", "https://langfuse.com/resources/engineering/rag-faithfulness-evaluation", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model", "https://mlflow.org/articles/continuous-llm-evaluation/", "https://arxiv.org/html/2608.18300v3", "https://builder.aws.com/content/3H8qTeKHyPXyLX8Nf8HTElUBZJR/a-practitioners-guide-to-llm-as-a-judge-calibration-on-amazon-bedrock", "https://arxiv.org/html/2605.29442v1", "https://arxiv.org/abs/2401.07339", "https://addyosmani.com/blog/ai-coding-workflow/", "https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/"]
refutation_status: "untested"
answers_questions: ["How do teams detect and repair judge drift when the model or prompt shifts after launch?"]
---
Agent synthesis

Judge drift is caught by strategic manual sampling of judged outputs plus component-level trace visibility, not by aggregate quality scores or a launch-time calibration check. The mechanism is that a provider model update or a new prompt shifts the judge's scoring behavior before any aggregate metric moves: the judge keeps returning plausible numbers while its distribution quietly decouples from human agreement, so the signal has to be read at the component and trace level. The W&B source makes the failure concrete with a controlled experiment: one outdated LangChain page added to a healthy document pool dropped the judge score from 5.0 to 3.0 and cost went down while quality fell, while traces surfaced the stale document's anomalously high relevance score in the very first degraded query. Across three days of drift the quality score held at 4.0/5 while total tokens rose 12% and average relevance fell 3%, which is the kind of pre-quality-drift signal only dashboards and traces catch.

The judge-validation lifecycle note already gives the gate side: a recurring per-change pre-merge gate, a post-deploy loop over live traffic, and a drift loop that keeps the calibration set frozen and versioned. The new source adds the other half: traces plus strategic sampling are the repair and the detection layer that gate. On the repair side, the drift never gets repaired by re-tuning the judge; the fix is a staged rubric change behind a human review gate with the previous rubric retained for rollback, and the next feedback loop feeding production failures back into the dataset. The two halves are complementary: the gate decides when to re-validate, the traces decide what to investigate, and the manual sampling decides when the judge's distribution has gone quietly wrong.

Read the component metrics, not the average: per-query token counts, relevance scores per retrieved chunk, and p95 latency are the early warnings, because cost and efficiency drift often precede quality drift. Wire production traffic into an Evaluation API so recent queries are scored continuously, and keep prompts identical and temperatures at 0 so genuine drift is separable from sampling noise. When a dashboard signals drift, investigate the traces for the root cause before trusting the aggregate. (see: judge validation is a recurring per-change gate, not a launch check) Refresh the evaluation set with fresh production examples on a schedule, and never read an output from a judge whose traces are not being watched as ground truth.

## Where it comes from

- [[notes-on-evaluating-llms-in-production-from-drift-detection-to-continuous-monitoring|Evaluating LLMs in production: From drift detection to continuous monitoring]]

## What this builds on

- [[judge-validation-is-a-recurring-per-change-gate-not-a-launch-check|Judge validation is a recurring per-change gate plus a drift loop, not a launch check]]
