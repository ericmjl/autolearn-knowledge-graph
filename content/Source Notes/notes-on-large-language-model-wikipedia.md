---
type: "source-note"
title: "Notes on: Large language model (Wikipedia)"
raw: "large-language-model-wikipedia"
url: "https://en.wikipedia.org/wiki/Large_language_model"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---

# Notes on: Large language model (Wikipedia)

- Archived full text: [[large-language-model-wikipedia|Full archived text, with credits]]
- Link: <https://en.wikipedia.org/wiki/Large_language_model>

## What it says

The source gives a broad overview of large language models: their transformer-based architecture, training (pretraining, fine-tuning via RLHF/constitutional AI, instruction tuning), and inference (hosted vs. local). It covers how LLMs are extended beyond basic text generation through prompt engineering, few-shot prompting, retrieval-augmented generation, tool use, and agentic patterns such as prompt chaining, Reflexion, DEPS, and Monte Carlo tree search. It also describes reasoning models that generate step-by-step analysis, and notes that biased or inaccurate training data can reduce output reliability, with benchmarks used to measure reasoning, factual accuracy, alignment, and safety.

## Claims drawn from this source

- **LLMs are not autonomous agents by themselves.** An LLM lacks the ability to interact with dynamic environments, recall past behaviors, and plan future actions; it becomes an agent only when given a role/profile, environment, memory, instructions, and tool use.
- **Prompt chaining decomposes complex problems into steps.** A user manually breaks a complex problem into steps, feeding each step's output into the next; non-experts can write successful stepwise prompts after trial and error.
- **Chain-of-thought prompting improves correctness.** Giving examples of verbal step-by-step reasoning (or adding 'Let's think step by step') makes the LLM generate intermediate steps before answering, improving accuracy on complex questions.
- **Reasoning models trade compute for accuracy.** Models like OpenAI o1 and DeepSeek-R1 generate step-by-step analysis and outperform GPT-4o on math/logic tasks, but require more computational resources per query.
- **Tool use requires an external orchestration program.** A program separate from the LLM watches the output stream for tool-calling syntax, invokes the tool, and feeds the result back into the LLM's input stream.
- **Reflexion stores lessons learned as long-term memory.** After each episode, the LLM is prompted to extract 'lessons learned' from the episode record, which are stored and reused in subsequent episodes to improve performance.
- **Biased training data degrades output reliability.** Biased or inaccurate training data makes an LLM's output less reliable; benchmark evaluations attempt to measure reasoning, factual accuracy, alignment, and safety.
- **Few-shot prompting adapts LLMs without fine-tuning.** Providing a few rounds of Q&A or task examples in the input lets an LLM understand the desired format and adapt to any task without fine-tuning.
