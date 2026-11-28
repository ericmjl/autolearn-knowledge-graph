---
type: "source-note"
title: "Notes on: Scaling Test-time Compute for LLM Agents"
raw: "scaling-test-time-compute-for-llm-agents"
url: "https://arxiv.org/html/2506.12928v1"
created_at: "2026-11-28T03:03:05Z"
updated_at: "2026-11-28T03:03:05Z"
---
- Archived full text: [[scaling-test-time-compute-for-llm-agents|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2506.12928v1>

## What it says

ATTS (Agentic Test-Time Scaling) is the first systematic study of test-time scaling inside language agents. Running GPT-4.1 on SmoLAgents over the 165-sample GAIA validation set, it compares parallel sampling algorithms, sequential revision strategies, verifiers and merging methods, and strategies for diversifying rollouts. Its results: parallel sampling helps (Best-of-N wins, +8 points over baseline), reflection helps only when triggered selectively, list-wise verification and merging beat voting or scoring, and mixing rollout models beats a single model.

## Claims drawn from this source

- **Parallel sampling significantly improves agent performance over a single linear rollout.** On GAIA with GPT-4.1, the baseline scores 55.76; BoN reaches 63.03 (+8), BoN-wise 58.79 (+3), and Beam-Search 56.97.
- **Best-of-N is the best parallel sampling algorithm but BoN-wise is best on hard problems.** BoN achieves the overall best score (63.03) and leads on level 1 and level 2, while BoN-wise reaches 38.46 on level 3, above baseline (26.92) and BoN (30.77).
- **Beam search and DVTS do not beat the baseline because their exploration depends on verifier signal accuracy.** Beam-Search matches the baseline (56.97 vs 55.76) and DVTS scores 55.76 exactly, because both algorithms increase exploration space while depending on verify-model signal accuracy.
- **Reflection helps only at the right moment; reflecting every step can hurt.** Baseline 55.76 vs step-based reflection 55.15. Selective reflection below a <2 threshold scores 56.36 and is best across levels, while frequent reflection (threshold <8, 53.33) and moderate (<5, 52.12) score lowest.
- **List-wise verification and merging outperform scoring and voting for agents.** For result merging, list-wise beats scoring and voting on BoN (63.03 vs 59.39 vs 56.80), Beam-Search (56.97 vs 53.94 vs 54.55), and Tree-Search (55.76). List-wise verification adds 3 points over scoring on BoN-wise (58.79 vs 56.36).
- **Mixing heterogeneous rollout models beats a single strong model at high sample width.** Pass@1 is highest for GPT-4.1 alone (55.76). At pass@4, GPT-4.1 mixed with Claude-3-5, Gemini-2.5-Pro and Claude-3-7 reaches 74.55, above GPT-4.1 alone (69.14) and above open-source SOTA frameworks (55.15-55.76).
- **Different models have distinct capability profiles that complement each other.** The paper notes LLMs vary in capability profiles (some excel at coding, others at tool use), so combining models maximizes rollout diversity in the multi-agent collaborative sampling strategy.
