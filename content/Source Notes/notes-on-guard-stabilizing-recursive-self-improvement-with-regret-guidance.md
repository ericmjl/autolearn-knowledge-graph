---
type: "source-note"
title: "Notes on: GUARD: Stabilizing Recursive Self-Improvement with Regret Guidance"
raw: "guard-stabilizing-recursive-self-improvement-with-regret-guidance"
url: "https://arxiv.org/html/2611.23476v1"
created_at: "2026-11-26T04:02:50Z"
updated_at: "2026-11-26T04:02:50Z"
---
- Archived full text: [[guard-stabilizing-recursive-self-improvement-with-regret-guidance|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2611.23476v1>

## What it says

GUARD is a reference-free continual harness-evolution framework for autonomous agents: a frozen model stays fixed while its inspectable harness (prompts, skills, tool rules, memory) evolves each round. It decomposes each task into a fixed pre-execution checklist of atomic binary predicates, grades completed trajectories against it with a two-layer self-reviewer (sandbox execution checks plus semantic trace judgments), ranks criteria by paired directional regret (newly broken behaviors ahead of unsolved gaps, mastered criteria pinned), samples a parallel group of candidate harnesses scored on the same tasks with group-standardized fitness, and promotes a winner only through a Soft-HURT gate that requires gains to outweigh induced regressions, logging rejected edits. At test time one frozen harness runs a single pass. Across PAST-Bench, EvoHarnessBench, and Drift Gauntlet it improves without catastrophic forgetting or memory pollution while cutting tokens per task.

## Claims drawn from this source

- **Self-editing harness loops fail by conflating regressions with gaps.** Free-form reflection and scalar task scores mix two distinct signals: behaviors the latest edit newly broke and capability gaps the agent still has not solved. Mixing them across rounds causes local overfitting (over-triggering), catastrophic forgetting, and memory pollution, leaving the agent worse than its starting point.
- **Tasks are decomposed into pre-execution atomic binary checklists.** The self-reviewer reads only the task prompt, visible tool declarations, and schema once at Turn 0 to derive a fixed checklist of execution-verifiable predicates (clean sandbox execution, valid entity IDs/columns, idempotent mutations) and semantic predicates (honoring every prompt constraint, recipient, format, and safety rule).
- **Two-layer grading separates execution from semantics.** Layer 1 checks execution predicates deterministically on an ephemeral sandbox copy; Layer 2 grades semantic predicates individually from the prompt, output, and tool/state trace. Dense per-criterion grading removes the 1/epsilon passive-discovery penalty on rare task invariants.
- **Paired directional regret ranks regressions above gaps.** Priority_t(c) = Delta_hurt,t(c) + Delta_gap,t(c), where Delta_hurt is the incumbent-vs-previous-promotion obedience drop and Delta_gap is the incumbent's shortfall against an oracle. A fresh regression (1 to 0) outranks every non-regressed criterion, and only mastered criteria (obeyed and unhurt) are pinned; frequency ranking 1-obey fails regression dominance, signed difference fails pinning.
- **Parallel candidate pooling gives credit isolation without a critic.** Propose samples a parallel group (M >= 2) of candidate harnesses from a single domain-agnostic seed prompt, scores them on the same task batch by within-group standardized fitness R = Perf - beta*|Q-| + gamma*|Q+| with beta > gamma, and contrasts the best and worst candidates to rewrite proposal prompts. Parallel two-candidate pooling beats sequential search and cuts rejected gate rounds by 64%.
- **Soft-HURT gates promotion on gains outweighing induced regressions.** A candidate promotes only if |Q-| <= h_max, |Q+| >= [|Q-| > 0], and net gain exceeds induced hurt beyond delta_noise. Isolated regressions trigger at most one in-round [iff] scope-guard repair; rejected edits are logged to a deduplicated ledger window so refused changes are not repeated verbatim.
- **Gating yields non-regression and 19/19 verified promotions.** Under the gate, self-review scores are non-decreasing on each round's gated buffer; every one of the 19/19 execution-gated Soft-HURT promotions across Drift Gauntlet, EvoHarnessBench, and professional suites satisfied Delta_test >= 0 on held-out tasks, with 15/19 strictly positive.
- **GUARD improves without forgetting and at lower token cost.** On Drift Gauntlet it is the only arm whose stream-mean never drops (0/12 block transitions, zero post-block forgetting on all four streams), outranks GEPA on final mean (73.22% vs 72.40%), cuts tokens per task by 54.5% versus the base agent, and is the only method with no negative backward or forward transfer on EvoHarnessBench.
