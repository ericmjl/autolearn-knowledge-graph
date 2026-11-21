---
type: "source-note"
title: "Notes on: Rethinking the Evaluation of Harness Evolution for Agents"
raw: "rethinking-the-evaluation-of-harness-evolution-for-agents"
url: "https://arxiv.org/html/2607.12227v4"
created_at: "2026-11-21T21:03:30Z"
updated_at: "2026-11-21T21:03:30Z"
---
- Archived full text: [[rethinking-the-evaluation-of-harness-evolution-for-agents|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2607.12227v4>

## What it says

The paper re-examines how harness evolution is evaluated and argues that existing benchmarks conflate genuine harness improvements with adaptation to the tasks used for search. Under matched feedback and inference budgets on Terminal-Bench 2.1, automatic harness evolution fails to beat simple test-time scaling baselines, both with and without unit test cases, and its gains collapse on held-out tasks. It wins only in long-horizon game settings that are hard enough to leave headroom, out-of-distribution, and provide granular feedback by design, where task-specific harness evolution beats fixed-harness sequential refinement by roughly 80% on ARC-AGI-3 and 11% on EdgeBench. The takeaway: compare against test-time scaling, keep optimization feedback separate from final measurement, and expect harness evolution to pay off where the environment supplies dense, verifiable feedback.

## Claims drawn from this source

- **Harness evolution underperforms test-time scaling under matched budgets.** On Terminal-Bench 2.1, Harness Evolution averaged 67.4 pass@1 vs Parallel Sampling 72.3 without unit test cases, and 69.7 pass@1 vs 82.0 with unit test cases; even pass@5 favors Sequential Refinement (87.1) over Harness Evolution (79.0).
- **Harness evolution overfits the search tasks.** On disjoint search/eval splits, the evolved harness gained only 1.2 points on Claude Opus 4.6, left GPT-5.4 unchanged, and cost 1.4 points on GPT-5.4 mini, an exactly flat average: revisions encode task-specific shortcuts, not generalizable design.
- **Reported gains overstate harness improvement because the same tasks drive both search and final evaluation.** Prior work searches for harness configurations using unit test cases drawn from the same benchmarks it reports final performance on, violating the standard separation between training and test data; the discrepancy between gains on the search set and flat held-out results shows reporting the same-task number conflates adaptation with reusable design.
- **Without verifiable feedback, self-generated signal is noisy and can actively hurt.** Without unit test cases, Harness Evolution dropped GPT-5.4 from 75.3 to 69.7 and critically underperformed direct sampling on average, with the authors noting that even strong agents struggle to extract reliable learning signals from their own trajectories and harness revision likely requires a reliable external correctness signal.
- **Long-horizon games are where harness evolution pays off.** ARC-AGI-3 (RHAE): full-harness Harness Scaling beat sequential refinement from 43.3 to 77.5 with Claude Opus 4.8 (+79.0%) and from 21.1 to 38.2 with GPT-5.6 Terra (+81.0%); EdgeBench: +13.3% with Claude Opus 4.8 (48.3 to 54.7) and +8.5% with GPT-5.4 (45.9 to 49.8), under the same budget.
- **Long-horizon games combine hard headroom, out-of-distribution dynamics, and granular feedback.** ARC-AGI-3 and EdgeBench are challenging, out-of-distribution, and designed to give continuous, fine-grained feedback (pass rates, failing tests, scores) that guards against regression, so the best score achieved across the trajectory is compared.
- **Terminal-Bench is insensitive to harness design.** Agents already score high, the remaining failures may stem from the model rather than the harness, and a minimal shell tool plus basic prompt suffices for most solvable tasks, so modifying prompts, tools, or middleware yields only marginal gains.
- **Memory remains the dominant harness-modification interface in long-horizon games.** The meta agent diagnoses failures, breaks redundant loops, and flags overlooked details; it is most effective on tasks requiring deep exploration along a single path and sometimes neglects breadth, failing to prompt exploration of alternative directions; Claude writes concise verdicts while GPT writes plans.
