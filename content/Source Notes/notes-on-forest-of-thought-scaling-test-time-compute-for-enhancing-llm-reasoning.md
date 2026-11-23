---
type: "source-note"
title: "Notes on: Forest-of-Thought: Scaling Test-Time Compute for Enhancing LLM Reasoning"
raw: "forest-of-thought-scaling-test-time-compute-for-enhancing-llm-reasoning"
url: "https://arxiv.org/html/2412.09078v5"
created_at: "2026-11-22T03:01:53Z"
updated_at: "2026-11-22T03:01:53Z"
---
- Archived full text: [[forest-of-thought-scaling-test-time-compute-for-enhancing-llm-reasoning|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2412.09078v5>

## What it says

Forest-of-Thought (FoT), from Huawei Noah's Ark Lab, scales test-time compute by combining multiple reasoning trees (ToT or MCTSr based) behind sparse activation, dynamic self-correction, and consensus-guided decision-making, instead of the single-pass reasoning of CoT or ToT. It reports that FoT with 8 activated subtrees reaches 96.84% on Game of 24 (base Llama-3-8B, temperature 0.95), far beyond CoT (4.38%) and ToT b=5 (74.00%), and that accuracy gains grow with the number of activated subtrees following a diminishing-returns scaling law. Sparse activation cuts LLM invocations from 32.32 to 26.99 while keeping the highest accuracy, and the gain comes from diversity of reasoning paths more than depth of individual trees.

## Claims drawn from this source

- **FoT combines multiple reasoning trees to leverage collective decision-making.** FoT integrates multiple reasoning trees (e.g., ToT or MCTSr) into a forest that approaches the input from different perspectives, producing results via sparse activation rather than full calculation on every tree.
- **Sparse activation cuts invocations while keeping accuracy.** In Game of 24 ablations, sparse activation reduced the number of LLM invocations from 32.32 to 26.99 while maintaining the highest accuracy, yielding both efficiency and accuracy.
- **Dynamic self-correction triggers on low model confidence.** FoT monitors predicted logits scores and automatically triggers a correction mechanism when the score falls below a predefined threshold; a threshold of 0.5 performed best on GSM8K.
- **Consensus-guided expert decision beats majority vote at scale.** CGED outperforms Majority Vote and Math Expert by a margin of about 2% when five subtrees are activated; the three strategies perform comparably at only two subtrees.
- **FoT reaches 96.84% on Game of 24 with 8 activated subtrees.** With 8 activated subtrees, FoT achieves 96.84% on Game of 24, versus CoT 4.38%, ToT (b=5) 74.00% and Buffer of Thought 82.40%, while only modestly increasing computational cost.
- **GSM8K: 4-rollout MCTSr with 2 trees beats 8-rollout with 2 trees.** As the number of trees in the forest increases, the multi-method forest approach becomes more pronounced, and 4-rollouts MCTSr with 2 trees achieved 3.2% higher accuracy than the 8-rollouts MCTSr, suggesting diversity beats depth.
- **FoT outperforms MCTSr at every MATH difficulty level.** Across MATH Levels 1-4, FoT (n=4) shows an impressive and consistent improvement of approximately 10% as difficulty increases from Level 1 to Level 4.
- **Accuracy scales with activated subtrees along a diminishing-returns curve.** Across Mistral-7B, Llama3-8B and GLM-4-9B, accuracy improves significantly as the number of activated subtrees increases, and each subtree incrementally contributes, though gains diminish as compute grows.
