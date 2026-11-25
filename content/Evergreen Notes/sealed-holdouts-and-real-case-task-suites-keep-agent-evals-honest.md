---
type: "evergreen"
title: "Sealed holdouts and real-case task suites keep agent evals honest"
created_at: "2026-11-25T16:02:02Z"
updated_at: "2026-11-25T16:02:02Z"
inputs: ["notes-on-ai-agent-evaluations-task-suites-and-pass-criteria", "product-specific-evals-beat-generic-benchmarks"]
provenance_urls: ["https://levystreet.com/engineering/ai-agent-evaluations/", "https://hamel.dev/blog/posts/evals/", "https://arxiv.org/abs/2407.01502"]
refutation_status: "untested"
answers_questions: ["How do product teams structure holdout sets and task-specific eval suites to avoid agent overfitting, and what cadence keeps them honest?"]
---
Agent synthesis

Product teams avoid agent overfitting by splitting a versioned task suite into a development set they tune against and a sealed holdout run only before releases and model upgrades. The mechanism works because the suite measures the real task rather than the 50 cases the team tuned against: it samples 50 to 150 real cases stratified by type, fixes seed states so the environment is deterministic, and grades final system state and the step trace rather than the agent's own claim of success.

The cadence is the load-bearing part. A smoke suite runs on every prompt, tool or model change; the full suite with repeats gates every release; the holdout runs before model or provider upgrades; and a graded sample of real production runs feeds new failures back into the suite weekly. Version everything together so a score always means the same thing, and report pass^k consistency and cost per successful task, not one-run success. A two-point move between releases is noise at 50 tasks, so the gate should require sustained improvement, not single-run wins (see: product-specific evals beat generic benchmarks).

Cost stays flat: 60 tasks at 5 trials each runs about US$120 per full suite at US$0.40 per run, which is cheap enough to run often. Keep the suite in your own repository and runner, and treat hosted evaluation services as decoration rather than the instrument.

## Where it comes from

- [[notes-on-ai-agent-evaluations-task-suites-and-pass-criteria|AI Agent Evaluations: Task Suites and Pass Criteria]]

## What this builds on

- [[product-specific-evals-beat-generic-benchmarks|Product-Specific Evals Beat Generic Benchmarks]]
