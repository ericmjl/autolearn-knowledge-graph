---
type: "source-note"
title: "Notes on: ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., ICLR 2023)"
raw: "react-synergizing-reasoning-and-acting-in-language-models-yao-et-al-iclr-2023"
url: "https://arxiv.org/abs/2210.03629"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---

# Notes on: ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., ICLR 2023)

- Archived full text: [[react-synergizing-reasoning-and-acting-in-language-models-yao-et-al-iclr-2023|Full archived text, with credits]]
- Link: <https://arxiv.org/abs/2210.03629>

## What it says

ReAct interleaves reasoning traces and task-specific actions so an LLM can both plan and act, rather than treating reasoning and acting as separate modules. Reasoning traces help induce, track, update, and recover from action plans, while actions let the model query external knowledge bases or environments for additional information. Across question answering, fact verification, and interactive decision-making benchmarks, ReAct improves over strong baselines and produces more interpretable, human-like trajectories. It also reduces hallucination and error propagation seen in chain-of-thought reasoning by grounding steps in external sources.

## Claims drawn from this source

- **Reasoning and acting should be interleaved.** The paper argues that LLMs should generate reasoning traces and task-specific actions in an interleaved manner to get synergy between the two.
- **Reasoning traces support action-plan management.** Reasoning traces help the model induce, track, and update action plans and handle exceptions.
- **Actions ground the model in external sources.** Actions allow the model to interface with external sources such as knowledge bases or environments to gather additional information.
- **ReAct reduces hallucination and error propagation.** On HotpotQA and Fever, interacting with a simple Wikipedia API helps overcome hallucination and error propagation prevalent in chain-of-thought reasoning.
- **ReAct improves interpretability and trustworthiness.** It generates human-like task-solving trajectories that are more interpretable than baselines without reasoning traces, improving human interpretability and trustworthiness.
- **ReAct beats imitation and RL with few examples.** On ALFWorld and WebShop, ReAct outperforms imitation and reinforcement learning methods by absolute success rates of 34% and 10% respectively, using only one or two in-context examples.
