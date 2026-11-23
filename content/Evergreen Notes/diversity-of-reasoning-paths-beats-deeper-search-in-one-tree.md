---
type: "evergreen"
title: "Diversity of reasoning paths beats deeper search in one tree"
created_at: "2026-11-22T03:02:36Z"
updated_at: "2026-11-22T03:02:36Z"
inputs: ["notes-on-forest-of-thought-scaling-test-time-compute-for-enhancing-llm-reasoning", "multi-path-reasoning-extends-chain-of-thought-to-planning"]
provenance_urls: ["https://arxiv.org/html/2412.09078v5", "https://arxiv.org/abs/2201.11903", "https://arxiv.org/abs/2305.10601"]
refutation_status: "untested"
answers_questions: ["Does tree-of-thought multi-path search pay for itself at scale, where does the token cost outweigh the accuracy gain?"]
---
Agent synthesis

Diversity of reasoning paths beats deeper search in one tree when test-time compute is the constraint. FoT (Huawei Noah's Ark Lab) does not claim that adding more ToT leaf nodes helps: expanding leaf nodes from 2 to 32 gave gradual gains with no significant improvement at 32, a reasoning bottleneck. Instead, FoT grows the forest: n parallel reasoning trees (ToT or MCTSr based), sparse activation that activates only trees whose nodes produce valid outputs, dynamic self-correction when the model's score drops below 0.5, and consensus-guided expert decision (CGED) to pick the final answer. The evidence is in the numbers: Game of 24 rises from 4.38% (CoT) and 74.00% (ToT b=5) to 96.84% with 8 activated subtrees; GSM8K reaches 97.33% with 4 subtrees at QwQ, above rStar-Math (95.20%) and GPT-4o (92.90%); MATH improves about 10% across Levels 1 to 4; and accuracy follows a diminishing-but-consistent scaling law as subtrees are added.

The sampled multi-path note (multi-path reasoning extends chain-of-thought to planning) establishes the mechanism: CoT gives the reasoning scaffold, ToT adds multi-path exploration with self-evaluation and backtracking, lifting Game of 24 from 4% (CoT) to 74%. FoT extends that same move along the budget axis. Brute-force node expansion saturates; FoT shows where the real savings are: LLM invocations drop from 32.32 to 26.99 via sparse activation while accuracy holds, plus an early-termination rule that stops search the moment a clear target is found. Diversity of outcomes beats depth of any individual tree: 4-rollouts MCTSr with 2 trees beats 8-rollouts with 2 trees by 3.2%. So the budget decision is not how many steps but how many distinct perspectives: expand the forest, not the tree (see: multi-path reasoning extends chain-of-thought to planning).

Budget multi-path reasoning by diversity first: buy more independent trees with cheap pruning and early stopping before spending tokens deeper inside one tree, and stop activating paths that cannot produce valid outputs.

## Where it comes from

- [[notes-on-forest-of-thought-scaling-test-time-compute-for-enhancing-llm-reasoning|Forest-of-Thought: Scaling Test-Time Compute for Enhancing LLM Reasoning]]

## What this builds on

- [[multi-path-reasoning-extends-chain-of-thought-to-planning|Multi-path reasoning extends chain-of-thought to planning]]
