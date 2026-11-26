---
type: "evergreen"
title: "Adaptive width beats fixed depth once the test-time budget grows"
created_at: "2026-11-26T02:01:51Z"
updated_at: "2026-11-26T02:01:51Z"
inputs: ["notes-on-wider-or-deeper-scaling-llm-inference-time-compute-with-adaptive-branching-tree-search", "diversity-of-reasoning-paths-beats-deeper-search-in-one-tree"]
provenance_urls: ["https://arxiv.org/html/2503.04412v1", "https://arxiv.org/html/2412.09078v5", "https://arxiv.org/abs/2201.11903", "https://arxiv.org/abs/2305.10601"]
refutation_status: "untested"
answers_questions: ["When do parallel reasoning trees stop adding value over a single deeper tree in test-time compute scaling?"]
---
Agent synthesis

Adaptive width beats fixed depth once the test-time budget grows, because the width/depth split is a per-node decision, not a ring-fenced hyperparameter. AB-MCTS reads an external score at every node, models the score distribution with a Bayesian posterior, and uses Thompson Sampling to decide whether to go wider (generate a new candidate) or go deeper (refine an existing one). It beats both repeated sampling (only wide) and standard MCTS (fixed branching) on Code Contest with GPT-4o and DeepSeek-V3 and on MLE-Bench, with the gap opening past 2^6 generation budget. The AB-MCTS-A variant (aggregating refinements under a CONT node, Beta prior for bounded scores) wins at larger budgets, while AB-MCTS-M (a mixed-effects model per generated-and-refined group) converges faster on limited budgets.

This refines the FoT finding that diversity of reasoning trees beats deeper search in one tree. FoT buys diversity by growing the forest with sparsely activated subtrees and consensus-guided expert decision; AB-MCTS buys it node by node by making the branching factor an adaptive posterior, never a constant. Both reject the same fixed branching factor: FoT by activating only the trees that produce valid outputs, AB-MCTS by letting each node choose GEN versus refine. The budget question is not how many nodes in a tree but how to spend the next one.

The practical rule is stage-dependent. At small budgets, refinement-heavy adaptive search (AB-MCTS-M, or a few trees with aggressive pruning) captures most of the gain. Past the hundreds of generations, switch to wider adaptive search with real feedback. Either way, hand-fixing the branching factor treats an adaptive decision as a constant (see: diversity of reasoning paths beats deeper search in one tree). For small budgets, start with FEW trees and refine; for large budgets, expand the forest and let the posterior decide (see: diversity of reasoning paths beats deeper search in one tree).

## Where it comes from

- [[notes-on-wider-or-deeper-scaling-llm-inference-time-compute-with-adaptive-branching-tree-search|Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive Branching Tree Search]]

## What this builds on

- [[diversity-of-reasoning-paths-beats-deeper-search-in-one-tree|Diversity of reasoning paths beats deeper search in one tree]]
