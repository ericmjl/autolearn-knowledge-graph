---
type: "evergreen"
title: "A fixed verifier goes stale as the harness evolves"
created_at: "2026-11-28T05:02:44Z"
updated_at: "2026-11-28T05:02:44Z"
inputs: ["notes-on-verifier-harness-co-evolution-for-training-free-self-improvement-on-open-ended-tasks", "stratified-search-plus-proposer-hidden-selection-tasks-keep-harness-evolution-honest"]
provenance_urls: ["https://arxiv.org/html/2610.17609v1", "https://arxiv.org/html/2608.24804v1", "https://arxiv.org/html/2607.12227v4", "https://lilianweng.github.io/posts/2026-07-04-harness/", "https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["When harness evolution hides selection tasks from the proposer, how does the verifier itself avoid drift as the harness changes?"]
---
Agent synthesis

A fixed verifier silently goes stale as the actor, the harness state, and the task demands evolve, and a stale verifier is worse than no verifier, because it decides which response is served and which experience the agent keeps. UCoE makes the failure concrete: as draft and revision pairs drift away from the contrasts on which the verifier was selected, its criteria and aggregation can stop predicting the errors the actor now produces, and a single stale judgment can harm the current task and persist across the stream; across six open-ended benchmarks UCoE already beats matched direct generation by 9.00 points with Qwen3-8B and 7.19 points with Qwen3.8-27B (59.00% and 57.19% preference), all on a verifier that re-evolves at checkpoints rather than stays fixed. The fix is co-evolution, not selection alone: at checkpoints, the verifier model synthesizes candidate programs from the diagnostics of completed tasks, tests them on the same contrasts grouped by declared property family, and replaces the active one only when the candidate wins on worst-family driving capacity, wins more held-out contrasts than it loses, and holds a regression tolerance on every existing family.

The stratified-search note is the other half of the same discipline from a different side: keep the selection tasks hidden from the proposer so the proposer cannot overfit the benchmark, and keep the verifier honest the same way by never letting it see the tasks it is judged on, since a proposer-hidden holdout guards task selection but says nothing about the verifier's own drift. The sampled harness-evolution note names the two-gate split (proposer-visible search, proposer-hidden selection) but never says what happens when the verifier itself is stale; UCoE names the verifier gate but never says how the search is kept from drifting toward the holdout. Together they show that a harness-evolution system must gate two surfaces before the loop starts, the holdout tasks and the verifier, or both become moving targets inside the loop.

Deploy the two gates as one discipline: run the baseline, stratify the search and selection slices on baseline score, failure mode, and verifier pass rate, keep the holdout and the selection tasks unreachable to the proposer, and adopt a new verifier only through a contrast-based gate with a fixed regression tolerance; treat driving capacity, discrimination on the weakest contrast family, as the anti-overfitting measure for the verifier the same way the hidden selection mean is for the search.

## Where it comes from

- [[notes-on-verifier-harness-co-evolution-for-training-free-self-improvement-on-open-ended-tasks|Verifier–Harness Co-Evolution for Training-Free Self-Improvement on Open-Ended Tasks]]

## What this builds on

- [[stratified-search-plus-proposer-hidden-selection-tasks-keep-harness-evolution-honest|Stratified search plus proposer-hidden selection tasks keep harness evolution honest]]
