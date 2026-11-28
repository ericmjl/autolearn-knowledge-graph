---
type: "evergreen"
title: "Rollout-model diversity beats deeper search in one tree"
created_at: "2026-11-28T03:04:13Z"
updated_at: "2026-11-28T03:04:13Z"
inputs: ["notes-on-scaling-test-time-compute-for-llm-agents", "diversity-of-reasoning-paths-beats-deeper-search-in-one-tree"]
provenance_urls: ["https://arxiv.org/html/2506.12928v1", "https://arxiv.org/html/2412.09078v5", "https://arxiv.org/abs/2201.11903", "https://arxiv.org/abs/2305.10601"]
refutation_status: "untested"
answers_questions: ["Does the diversity-beats-depth reasoning result hold across model families, or is it an artifact of QwQ-class models?"]
---
Agent synthesis

Diversity beats depth at the agent level too, but the unit of diversity moves: what pays is distinct model families in the rollout pool, not more branches in one tree. In the sampled FoT evergreen, diversity means separate subtrees within a single tree: 8 activated subtrees lift Game of 24 to 96.84% at QwQ, and 4 rollouts with 2 trees beat 8 rollouts with 2 trees by 3.2%. The ATTS source note shows that same budget axis inside language agents resolves differently. Deeper-search machinery barely moves the score: Beam-Search reaches 56.97 and DVTS 55.76 against a 55.76 baseline, because their exploration still leans on verifier signal accuracy, while Best-of-N reaches 63.03 and BoN-wise reaches 38.46 on the hardest GAIA level. The diversity that pays in ATTS is across models: pass@4 with GPT-4.1 mixed with Claude-3-5, Gemini-2.5-Pro and Claude-3-7 reaches 74.55, above GPT-4.1 alone (69.14) and above open-source SOTA frameworks. The Verifier and merging evidence points the same direction: list-wise selection beats scoring and voting, since it can pick the correct answer out of diverse candidates rather than average a majority. So the QwQ-era result is not an artifact of long-thinking models: the principle survives, but the unit of diversity changes with the setting. For reasoning inside one model, buy more subtrees; for agents, buy more rollout models with complementary profiles, and let the verifier pick rather than rank by score.

The sampled evergreen's mechanism gives the second half. FoT activates only trees producing valid outputs and stops search when a clear target appears, which is exactly what ATTS's selective reflection does: the <2 trigger scores 56.36, above step-based reflection (55.15) and frequent reflection (53.33), because reflection pays only on the steps where the agent is failing. Both notes therefore say the budget should go to independent perspectives plus a gate on when to spend, not deeper capture of one path. The new evidence adds the sharper boundary: this does not mean deeper parallel trees are useless. DVTS fails on GAIA not because diversity is worthless but because the verifier it leans on is not reliable enough to steer it, which is also why Beam-Search stalls. That connects the diversity-of-paths result to the verifier-quality problem: the cheap way to buy depth, at the cost of another brittle signal.

The synthesis across the two notes is a concrete budget order. First buy independent rollout perspectives, then a gate that decides when to spend reflection, then a selection rule that reads the whole candidate set. When the budget is fixed, that ordering beats a single deeper tree, in both settings, and it holds across model families as long as the rollout pool carries complementary capability profiles. The caveat the ATTS source adds is honest: on pure reasoning tasks with a strong single model, BoN and FoT-style subtrees already deliver most of the gain, and the mixed-model payoff shows up at high sample width (pass@4, 74.55), not at pass@1, where GPT-4.1 alone still leads at 55.76.

Do not spend agent budget on deeper search inside one tree. Spend it on heterogeneous rollout models, gate reflection to the steps that fail, and select the final answer list-wise across the candidate set.

## Where it comes from

- [[notes-on-scaling-test-time-compute-for-llm-agents|Scaling Test-time Compute for LLM Agents]]

## What this builds on

- [[diversity-of-reasoning-paths-beats-deeper-search-in-one-tree|Diversity of reasoning paths beats deeper search in one tree]]
