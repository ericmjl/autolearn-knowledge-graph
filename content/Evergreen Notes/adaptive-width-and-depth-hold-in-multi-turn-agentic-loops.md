---
type: "evergreen"
title: "Adaptive width and depth hold in multi-turn agentic loops"
created_at: "2026-11-27T06:02:51Z"
updated_at: "2026-11-27T06:02:51Z"
inputs: ["notes-on-paper-page-trace-a-unified-rollout-budget-allocation-framework-for-efficient-agentic", "adaptive-width-beats-fixed-depth-once-the-test-time-budget-grows"]
provenance_urls: ["https://huggingface.co/papers/2606.11119", "https://arxiv.org/html/2503.04412v1", "https://arxiv.org/html/2412.09078v5", "https://arxiv.org/abs/2201.11903", "https://arxiv.org/abs/2305.10601"]
refutation_status: "untested"
answers_questions: ["Does the adaptive width/depth split for test-time search still hold when the search is a multi-turn agentic loop rather than one generation?"]
---
Agent synthesis

The adaptive width/depth split survives the move from one generation to a multi-turn agentic loop, but the unit of the decision shifts: instead of choosing whether to generate a new candidate or refine an existing one at a single node, the allocator chooses where to spend budget across turns of a ReAct rollout. Adaptive width beats fixed depth once the test-time budget grows: AB-MCTS reads an external score at every node and uses Thompson sampling to decide GEN versus refine, and it beats both repeated sampling and standard MCTS past 2^6 generation budget. TRACE extends the same principle to the multi-turn setting, modeling each thought-action-observation step as a semantically distinct node and allocating budget to prompt roots and turn-level prefixes under a shared mixed-reward contrast principle: anchors whose descendants are most likely to contain both successes and failures get continuations.

The mechanism is contrast, not depth. Both frameworks reject the fixed branching factor as a constant; AB-MCTS makes it an adaptive per-node posterior, TRACE makes it a per-anchor decision over roots and visited prefixes. TRACE adds a prefix-level refinement that AB-MCTS does not have: a shared generalizable predictor estimates conditional success probability from prefix histories, prefix-level scoring is at least as informative as prompt-only scoring (prediction error cannot worsen as more turns are observed), and the value of expanding a visited prefix equals the probability that at least one new continuation flips the observed reward. In the AB-MCTS framing, width and depth are two ends of one per-node decision; in TRACE, the same decision happens at depth-zero roots and at every intermediate prefix, turning flat rollouts into tree-structured rollouts whose shared-prefix branches turn opposite terminal outcomes into local pairwise preferences.

The evidence is symmetric in shape but different in scale. AB-MCTS wins on Code Contest and MLE-Bench past 2^6 generation budgets, with the AB-MCTS-M variant converging faster at small budgets and AB-MCTS-A winning at large ones. TRACE reports +2.8 points on Qwen3-14B Multi-Hop QA over competitive baselines at equal sampling cost across mathematical reasoning, multi-hop QA, and function calling, with prefix-conditioned prediction more reliable at deeper prefix depths. The shared lesson: the question is not whether to search wider or deeper but where the next unit of budget buys the most contrast. A fixed depth treats adaptive allocation as a constant.

Treat the turn as the smallest budget-bearing unit in agentic loops. At small budgets, refinement-heavy allocation (a few continuations, heavy pruning, M-style variants) captures most of the gain; past the hundreds-of-generations range, widen with feedback and let a predictor decide (see: adaptive width beats fixed depth once the test-time budget grows). Separate root-level and prefix-level allocation, score prefixes with the same shared predictor that scores roots, and spend budget where descendants are most likely to disagree in terminal outcome.

## Where it comes from

- [[notes-on-paper-page-trace-a-unified-rollout-budget-allocation-framework-for-efficient-agentic|Paper page - TRACE: A Unified Rollout Budget Allocation Framework for Efficient Agentic Reinforcement Learning]]

## What this builds on

- [[adaptive-width-beats-fixed-depth-once-the-test-time-budget-grows|Adaptive width beats fixed depth once the test-time budget grows]]
