---
type: "source-note"
title: "Notes on: How Do AI Agents Spend Your Money? Analyzing and Predicting Token Consumption in Agentic Coding Tasks"
raw: "how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic"
url: "https://arxiv.org/html/2604.22750v3"
created_at: "2026-11-26T12:01:29Z"
updated_at: "2026-11-26T12:01:29Z"
---
- Archived full text: [[how-do-ai-agents-spend-your-money-analyzing-and-predicting-token-consumption-in-agentic|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2604.22750v3>

## What it says

A first systematic study of token consumption in agentic coding tasks. Researchers ran eight frontier LLMs (Claude Sonnet 3.7/4/4.5, GPT-5, GPT-5.2, Qwen3-Coder-480B, Kimi-K2, Gemini-3-Pro) via OpenHands on SWE-bench Verified, measuring where tokens go, which models are efficient, and whether agents can predict their own cost before executing. Agentic tasks consume orders of magnitude more tokens than reasoning or chat, input tokens dominate cost, usage is highly variable, more tokens do not buy more accuracy, and frontier models underestimate their own token needs.

## Claims drawn from this source

- **Agentic coding tasks are uniquely expensive and input-token driven.** Agentic coding consumes about 3500x more tokens than a single-round code reasoning task and 1200x more than multi-round code chat, driven by exponential growth of input tokens as context accumulates and repeats across rounds.
- **Token usage is highly variable even on the same task.** Runs on the same task differ by up to 30x in total tokens; the most expensive run doubles the least expensive run's token and monetary cost; high-token-cost problems show larger cross-run variance.
- **More tokens do not buy more accuracy.** Accuracy rises modestly from the cheapest to intermediate-cost runs, then saturates; higher-cost runs show sharply increased repeated file-view and modify actions, suggesting unproductive exploration.
- **Models differ in token efficiency beyond task difficulty.** Kimi-K2 and Claude Sonnet-4.5 consume over 1.5 million more tokens on average than GPT-5 on the same tasks, even on the easy subset all models solve; token-efficient models perform fewer file views and repeated actions.
- **Human-rated difficulty weakly predicts actual token cost.** Kendall tau_b between expert difficulty labels and total token usage is only 0.32; 6.7% of under-15-minute tasks cost more than the average one-hour-plus task.
- **Cache reads dominate agentic cost across phases and rounds.** Cache-read input tokens are the largest category by a wide margin in every phase (Setup, Explore, Fix, Validate, Closeout); individual round costs spike when the agent adds new content to the context, not from reuse.
- **Models fail to predict their own token usage.** Self-prediction correlations reach only weak-to-moderate levels (max 0.39 for Sonnet 4.5 output tokens); output tokens are easier to predict than input tokens; all tested models systematically underestimate real usage, even without an in-context example.
- **Self-prediction is cheap but noisy.** For most models prediction costs less than half the task cost; Sonnet 4.5 reaches its best correlation at 0.32x task cost and GPT-5.2 drops below 6% overhead, while Sonnet 3.7 and 4 spend more than 2x.
