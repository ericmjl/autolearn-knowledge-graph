---
type: "evergreen"
title: "A public headline earns trust only inside your own gated harness"
created_at: "2026-11-25T18:07:18Z"
updated_at: "2026-11-25T18:07:18Z"
inputs: ["notes-on-agent-evaluation-readiness-checklist", "public-eval-headlines-hide-reliability-grader-noise-and-single-shot-limits"]
provenance_urls: ["https://www.langchain.com/blog/agent-evaluation-readiness-checklist", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339"]
refutation_status: "untested"
answers_questions: ["What gates should a small internal eval harness run before trusting a public benchmark headline, beyond pass^k and raw error analysis?"]
---
Agent synthesis

A public benchmark headline is a shortlist, not a verdict, and an internal gate is the only thing that turns it into signal. The gate works because a headline folds together errors an internal harness can separate: a wrong aggregate (average pass rate hides the difference between an agent that passes every time and one that passes once in three), a flawed grader (false negatives on correct work and false positives on wrong work), and a mismatched task (single-shot instructions where real work involves drafts, review, and course-correction).

The new source note supplies the gate machinery. It starts with a manual pass over 20-50 real traces, which teaches more about failure patterns than any automated system. It separates capability evals ("what can it do?", a low pass rate to climb) from regression evals ("does it still work?", a near-perfect rate to protect). It tells teams to spend 60-80% of eval effort on error analysis, gathering traces, open-coding them with a domain expert, and grouping issues into a failure taxonomy (prompt problems, tool design problems, model limitations, tool failures, data gaps) until no new category surfaces. It refuses to blame the agent before checking the pipeline: the Witan Labs team saw a single extraction bug move their benchmark from 50% to 73%. Full-turn evals must grade the response, the trajectory, and the state changes, because a calendar event can say "scheduled" while never existing.

Grader design is the second gate. The checklist defaults to code-based graders for objective checks, reserves LLM-as-judge for genuinely subjective assessments, prefers binary pass/fail over numeric scales, calibrates judges on 20+ labeled examples, and grades the outcome, not the exact path, with partial credit for incremental progress. Trials must run in clean isolated environments with no shared state, and reported improvements need confidence intervals from multiple repetitions, not a single run. Distinguish task failures from evaluation failures: a timeout marked as "incorrect reasoning" pollutes the signal. The checklist also tracks operational metrics alongside quality: turns, token usage, latency, and cost per task, so a 95%-accurate agent that is 10x slower does not read as an improvement.

The synthesis none of the two inputs states alone: the public headline note teaches the discipline of "a screen, not a verdict", and the checklist turns that discipline into an executable gate. The two inputs agree on what a headline hides; only together do they say what to build to hide it. Public scores narrow the shortlist. An internal gate answers the four questions a headline cannot: whether the failures are infrastructure or reasoning, whether the grader is fair, whether the trial was isolated, and whether the task separation holds under repeat runs. Build the gate first, then let the public number choose the models worth running through it, with pass^k and per-task cost published alongside the average (see: public eval headlines hide reliability, grader noise, and single-shot limits).

## Where it comes from

- [[notes-on-agent-evaluation-readiness-checklist|Agent Evaluation Readiness Checklist]]

## What this builds on

- [[public-eval-headlines-hide-reliability-grader-noise-and-single-shot-limits|Public eval headlines hide reliability, grader noise, and single-shot limits]]
