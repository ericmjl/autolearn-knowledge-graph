---
type: "source-note"
title: "Notes on: AI Agent Evaluations: Task Suites and Pass Criteria"
raw: "ai-agent-evaluations-task-suites-and-pass-criteria"
url: "https://levystreet.com/engineering/ai-agent-evaluations/"
created_at: "2026-11-25T16:01:37Z"
updated_at: "2026-11-25T16:01:37Z"
---
- Archived full text: [[ai-agent-evaluations-task-suites-and-pass-criteria|Full archived text, with credits]]
- Link: <https://levystreet.com/engineering/ai-agent-evaluations/>

## What it says

Levy Street lays out how to build a task-specific evaluation suite for an agent: sample real cases stratified by type, fix environment seed states, write pass/fail criteria a program can check (required outcomes, forbidden actions, step limits), split the suite into a development set you tune against and a sealed holdout run only before releases and model upgrades, version tasks/fixtures/graders/judges together, and report pass^k consistency and cost per successful task rather than one-run success. Suites must anchor on real work, not imagined cases, and refresh continuously from production traffic so the suite keeps measuring the real task instead of memorizing fixed tasks.

## Claims drawn from this source

- **A task suite is a versioned set of realistic cases, each with an environment and criteria a program can check.** Sample real cases from tickets, inboxes or logs, stratified by type and difficulty, and deliberately include the awkward ones: missing data, conflicting instructions, requests that should be refused.
- **Every task has a seed state, required outcomes, forbidden actions, and a step limit.** A task definition is input, seed state, must outcomes, must-not actions and a max step count; the grader reads final system state and the trace, never the agent's own claim.
- **Suites are split into a development set tuned against and a sealed holdout used only before releases and model upgrades.** Keep the holdout sealed and out of every prompt; lazy reuse of the same tasks leads to overfitting, where months of tuning against 50 tasks make the suite measure memory rather than skill.
- **Tasks, fixtures, graders, judge prompts and judge model versions share one suite version.** A score always means the same thing when the tasks, fixtures, graders, judge prompts and judge model versions are versioned together.
- **Repeat trials and report pass^k, not one-run success.** Run each task several times at production settings and report intervals rather than single numbers; 40 passes out of 50 tasks gives a 95% Wilson interval of roughly 67% to 89%.
- **Cadence: smoke suite on every change, full suite with repeats before release, sealed holdout before model or provider upgrades, and a graded weekly sample of real production runs.** The trigger table maps a change to a smoke suite (no new failures on previously passing tasks), a planned release to three to five trials (success and pass^k at or above last release, zero harmful actions), a model or provider upgrade to the full suite plus holdout, and weekly production runs to a graded sample.
- **Graders must check final system state and the trace, not the agent's final message.** Grading the claim, not the state, passes agents that say done without doing it; few-shot leakage from examples copied from the test set inflates scores.
- **Cost per successful task and uncertainty intervals belong in the metric set.** Mean steps, tokens and USD per successful trial separate a good agent from an expensive one; 60 tasks x 5 trials at US$0.40 each is 300 runs and US$120 per full suite.
