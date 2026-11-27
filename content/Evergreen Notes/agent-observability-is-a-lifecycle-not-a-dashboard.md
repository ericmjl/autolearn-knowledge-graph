---
type: "evergreen"
title: "Agent observability is a lifecycle, not a dashboard"
created_at: "2026-11-27T13:01:36Z"
updated_at: "2026-11-27T13:01:36Z"
inputs: ["notes-on-agent-observability-patterns-for-production-ai-agents-mlflow", "judge-drift-is-caught-by-strategic-sampling-over-component-level-traces"]
provenance_urls: ["https://mlflow.org/articles/agent-observability-patterns/", "https://wandb.ai/site/articles/evaluating-llms-in-production/", "https://mlflow.org/articles/judge-consistency-llm/", "https://arxiv.org/html/2606.19544v1", "https://langfuse.com/resources/engineering/rag-faithfulness-evaluation", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model", "https://mlflow.org/articles/continuous-llm-evaluation/", "https://arxiv.org/html/2608.18300v3", "https://builder.aws.com/content/3H8qTeKHyPXyLX8Nf8HTElUBZJR/a-practitioners-guide-to-llm-as-a-judge-calibration-on-amazon-bedrock", "https://arxiv.org/html/2605.29442v1", "https://arxiv.org/abs/2401.07339", "https://addyosmani.com/blog/ai-coding-workflow/", "https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/"]
refutation_status: "untested"
answers_questions: ["Which tools and patterns do teams use to get component-level trace visibility (per-query tokens, relevance, p95 latency) in an agent eval pipeline?"]
---
Agent synthesis

Agent observability is a lifecycle, not a dashboard. Teams that watch only latency, error rate and throughput learn that the service is healthy while the agent quietly answers wrong: a support agent can return a polite, plausible refund answer in 1.8 seconds while the trace shows it skipped the policy lookup, guessed from memory and retried the order API three times.

The MLflow source supplies the mechanics. Trace the whole run as a hierarchical span tree (workflow, agent, model, retrieval, tool, validation, policy and human-approval spans), propagate OpenTelemetry GenAI conventions across every hop, collect four streams instead of one (traces, metrics, logs and evaluations), keep the full artifact set (retrieval queries and documents, tool outputs, memory operations, inter-agent messages), attach sampled LLM-as-a-judge scores to traces so a low score links straight to the run that earned it, alert on behavior drift (cost per run, retry rate, tool-selection drift, eval-score drop at p95, not from a baseline week), and decide sampling, redaction and retention before launch.

The judge-drift note supplies the complementary gate side: a recurring pre-merge gate and a drift loop that keeps the calibration set frozen, while traces and strategic sampling are the detection layer that gate. Together they split observability into three working layers. The gate decides when to re-validate. The traces decide what to investigate. The sampling decides when the judge's distribution has gone quietly wrong. A trace tells you what happened; an evaluation tells you whether it was good; the two joined on the same run turn debugging into a quality system.

Read the component metrics, not the average, and open the trace for any low-scoring or expensive run before trusting the aggregate. Refresh the evaluation set with fresh production examples on a schedule, and feed real failures back into regression test cases. Dashboards saying the service is up can sit next to an agent that never looked up the policy; only a span tree with a score on it catches that.

## Where it comes from

- [[notes-on-agent-observability-patterns-for-production-ai-agents-mlflow|Agent Observability Patterns for Production AI Agents | MLflow]]

## What this builds on

- [[judge-drift-is-caught-by-strategic-sampling-over-component-level-traces|Judge drift is caught by strategic sampling over component-level traces]]
