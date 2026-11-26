---
type: "source-note"
title: "Notes on: Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive Branching Tree Search"
raw: "wider-or-deeper-scaling-llm-inference-time-compute-with-adaptive-branching-tree-search"
url: "https://arxiv.org/html/2503.04412v1"
created_at: "2026-11-26T02:01:26Z"
updated_at: "2026-11-26T02:01:26Z"
---
- Archived full text: [[wider-or-deeper-scaling-llm-inference-time-compute-with-adaptive-branching-tree-search|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2503.04412v1>

## What it says

AB-MCTS, presented by Kou Misaki et al., points out that fixed-width tree search and repeated sampling both fail to scale because they ignore external feedback. It proposes a Bayesian adaptive-branching MCTS that, at every node, chooses between going wider (sampling a new candidate) and going deeper (refining an existing one) based on a score evaluator, and it shows the method beats both repeated sampling and standard MCTS on competitive coding and MLE-bench tasks.

## Claims drawn from this source

- **Fixed branching factors hinder inference-time scaling.** Standard MCTS uses a fixed branching factor as a hyperparameter, and studies show the gain diminishes when the inference-time computational budget is increased.
- **Pure exploration and pure exploitation are the two extremes.** Repeated sampling is 'only go wide' (exploration), sequential refinement is 'only go deep' (exploitation), and AB-MCTS generalizes both into a single tree-search framework.
- **Generic branching decisions are made with Thompson Sampling.** Each node offers actions a_0 (a GEN node representing a new child) and a_1..a_n (existing children); posterior distributions over the score r are drawn and Thompson Sampling picks the action.
- **Two AB-MCTS variants trade off convergence speed against final performance.** AB-MCTS-M uses a mixed-effects model with a random intercept per generated-then-refined group; AB-MCTS-A aggregates refinements under a CONT node with Beta/Gaussian conjugate priors. AB-MCTS-A is stronger at larger budgets while AB-MCTS-M converges faster early.
- **AB-MCTS beats repeated sampling and standard MCTS.** On Code Contest with GPT-4o, all AB-MCTS variants exceed repeated sampling and standard MCTS across most budgets; with DeepSeek-V3, the advantage emerges clearly once the budget exceeds 2^6.
- **Adaptive width outperforms on MLE-Bench.** On three MLE-Bench competitions, AB-MCTS-A (Gaussian) beats repeated sampling at larger budgets; AB-MCTS-M converges faster for limited budgets and scores competitively.
- **Success depends on a usable score evaluator.** The method relies on an accessible evaluator (public tests, public validation set, or a reward model) and the probability of reaching deep refinement decays roughly geometrically in the AB-MCTS-A design.
