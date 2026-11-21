---
type: "evergreen"
title: "Public eval headlines hide reliability, grader noise, and single-shot limits"
created_at: "2026-11-21T05:03:04Z"
updated_at: "2026-11-21T05:03:04Z"
inputs: ["notes-on-how-public-evals-work-and-fail-and-what-should-change", "simple-benchmark-scores-overstate-real-world-agent-reliability"]
provenance_urls: ["https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339"]
refutation_status: "untested"
---
Agent synthesis

Public eval headlines overstate what a leaderboard score means: average pass rate hides the difference between a model that solves a task every time and one that solves it one time in three, and grader failures cut both ways, failing the correct work and passing the wrong.

The teardown of twelve public evals shows the failure modes concretely. Eight of twelve benchmarks graded away correct work, 41 of 65 Terminal Bench 4.0 tasks scored on unstated requirements, 23 of 113 DeepSWE tasks marked correct solutions as failures, and more than 60% of Harvey LAB results that passed every criterion carried material hallucinations. The average-pass-rate lens hides all of this: two agents at 70% average can differ from always-70% to 17% pass^k over five trials, and AutomationBench records models declaring success on 72% to 91% of the failures analyzed. Dollar cost is equally deceptive: GPT-4o cost about a tenth of GPT-5 per task in GDPval, but once expert review and redo time were counted, it was slower than an expert working alone while GPT-5 was faster.

The existing note on simple benchmark scores already makes the adjacent point that narrow accuracy-focused holdouts let agents overfit and take shortcuts, and that realistic repo-level tasks degrade performance relative to simple settings. Together, the two show that a public score carries three distinct errors on top of ordinary benchmark weakness: a wrong aggregate (average pass rate instead of pass^k), a flawed grader (false negatives and false positives), and a mismatched task (single-shot instructions where real work involves drafts, review, and course-correction). The synthesis: a public eval score is a screen for shortlisting, not a verdict on capability (see: simple benchmark scores overstate real-world agent reliability).

Use public scores to narrow the models worth testing, then run the final check in your own harness, demanding pass^k alongside the average, and reading the error analysis before trusting any headline number.

## Where it comes from

- [[notes-on-how-public-evals-work-and-fail-and-what-should-change|How Public Evals Work and Fail, and What Should Change]]

## What this builds on

- [[simple-benchmark-scores-overstate-real-world-agent-reliability|Simple benchmark scores overstate real-world agent reliability]]
