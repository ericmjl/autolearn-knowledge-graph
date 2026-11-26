---
type: "evergreen"
title: "Purpose-built small evaluators make product-specific evals run on every transaction"
created_at: "2026-11-23T00:02:00Z"
updated_at: "2026-11-26T09:05:58Z"
inputs: ["notes-on-agent-observability-splunk", "product-specific-evals-beat-generic-benchmarks", "notes-on-agent-observability-splunk-ca1da2", "test-scopes-mirror-eval-layers"]
provenance_urls: ["https://galileo.ai/blog/llm-evaluation-step-by-step-guide", "https://hamel.dev/blog/posts/evals/", "https://arxiv.org/abs/2407.01502", "https://galileo.ai/blog/multi-agent-ai-system-failure-recovery", "https://en.wikipedia.org/wiki/Test", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["How do teams decide which tasks warrant product-specific evals vs generic benchmarks, and what is the cost of building each?", "How do you wire layered evals into CI so unit-scope checks run on every change without blowing the budget?"]
---
Agent synthesis

Purpose-built small evaluators make product-specific evals run on every transaction, not just a sampled slice. The source note documents the mechanism: Splunk evaluates behavior, observability, tokenomics, and guardrails across 100% of traffic with purpose-built Eval-G1 small models at a fraction of frontier-judge cost, turning trustable evaluations into runtime guardrails that block or steer risky actions instead of flagging after the fact. The product-specific-evals note supplies the companion claim: generic benchmarks amortized across every model and task cannot catch a product-specific weakness, so the real stack question is what a judge can afford to run per call.

The CI wiring comes from the test-scopes note: unit-scope checks on every change, structural checks at the task boundary, cohort checks on significant changes, each layer its own call. The cheap-judge economics resolve the budget objection on the production side, where always-on scoring replaces a sampled slice and the same score mechanism now gates releases instead of auditing reports. What a final-only eval hides, the layered split exposes, because each scope names what it measures and what its failure means. (see: test scopes mirror eval layers)

Measure judge cost per interaction before choosing an eval stack. A judge too expensive for 100% of traffic forces samples and strata, and that sample is the gap that lets a benchmark-beating build pass the CI gate and drift in production.

## Where it comes from

- [[notes-on-agent-observability-splunk|Agent Observability | Splunk]]
- [[notes-on-agent-observability-splunk-ca1da2|Agent Observability | Splunk]]

## What this builds on

- [[product-specific-evals-beat-generic-benchmarks|Product-Specific Evals Beat Generic Benchmarks]]
- [[test-scopes-mirror-eval-layers|Test scopes mirror eval layers]]
