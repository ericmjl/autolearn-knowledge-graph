---
type: "evergreen"
title: "Purpose-built small evaluators make product-specific evals run on every transaction"
created_at: "2026-11-23T00:02:00Z"
updated_at: "2026-11-23T00:02:00Z"
inputs: ["notes-on-agent-observability-splunk", "product-specific-evals-beat-generic-benchmarks"]
provenance_urls: ["https://galileo.ai/blog/llm-evaluation-step-by-step-guide", "https://hamel.dev/blog/posts/evals/", "https://arxiv.org/abs/2407.01502"]
refutation_status: "untested"
answers_questions: ["How do teams decide which tasks warrant product-specific evals vs generic benchmarks, and what is the cost of building each?"]
---
Agent synthesis

Purpose-built small evaluators make product-specific evals run on every transaction, not just a sampled slice. The Splunk source argues that Eval-G1 models score and protect 100% of production traffic at a fraction of the cost of a frontier judge, so the cost of product-specific evaluation stops being the factor that forces teams to sample. The mechanism: once a judge is cheap enough to run per interaction, evaluation stops being a periodic audit and becomes a per-call control, which is the economic precondition for the holdout-and-cost-accuracy discipline the evals note argues for.

The evidence is concrete. Splunk traces every step of a workflow from request to response, reads latency and errors next to hallucinations, bias, prompt injection, and PII leakage, and turns evaluations into runtime guardrails that block or steer risky actions instead of flagging after the fact. Eval-G1 is the cost lever that makes product-specific evals scale to full traffic. The sampled evals evergreen holds that product-specific evals with holdouts beat generic benchmarks; the Splunk source supplies what the earlier note left out: a working configuration for running that evaluation on 100% of traffic.

The synthesis is that the product-specific vs generic decision is not only which tasks merit evaluation, but what stack can afford to evaluate them. Generic benchmarks amortize cost across every model and task; product-specific evals tied to a harness and CI suite become viable when the judge is cheap enough to run on each call.

Measure judge cost per interaction before choosing an eval stack; a judge you cannot run on 100% of traffic forces you back to samples and strata, which is the gap that lets benchmark-beating agents drift past the evals.

## Where it comes from

- [[notes-on-agent-observability-splunk|Agent Observability | Splunk]]

## What this builds on

- [[product-specific-evals-beat-generic-benchmarks|Product-Specific Evals Beat Generic Benchmarks]]
