---
type: "source-note"
title: "Notes on: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al., Google, 2022)"
raw: "chain-of-thought-prompting-elicits-reasoning-in-large-language-models-wei-et-al"
url: "https://arxiv.org/abs/2201.11903"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---

# Notes on: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al., Google, 2022)

- Archived full text: [[chain-of-thought-prompting-elicits-reasoning-in-large-language-models-wei-et-al|Full archived text, with credits]]
- Link: <https://arxiv.org/abs/2201.11903>

## What it says

The source argues that generating a chain of thought—a series of intermediate reasoning steps—significantly improves large language models' ability to perform complex reasoning. It introduces chain-of-thought prompting, where a few chain-of-thought demonstrations are provided as exemplars in the prompt, and shows that this reasoning ability emerges naturally in sufficiently large models. Experiments on three large language models report improved performance across arithmetic, commonsense, and symbolic reasoning tasks, with striking gains on benchmarks such as GSM8K. In particular, a 540B-parameter model prompted with eight chain-of-thought exemplars reaches state-of-the-art accuracy on GSM8K, surpassing even finetuned GPT-3 with a verifier.

## Claims drawn from this source

- **Chain-of-thought improves complex reasoning.** Generating a chain of thought—intermediate reasoning steps—significantly improves the ability of large language models to perform complex reasoning.
- **Few CoT exemplars elicit reasoning.** Chain-of-thought prompting uses a few chain-of-thought demonstrations as exemplars in prompting.
- **Reasoning emerges in sufficiently large models.** The source reports that such reasoning abilities emerge naturally in sufficiently large language models via chain-of-thought prompting.
- **Gains span multiple reasoning task types.** Experiments on three large language models show improved performance on arithmetic, commonsense, and symbolic reasoning tasks.
- **Eight exemplars yield GSM8K state of the art.** Prompting a 540B-parameter language model with just eight chain-of-thought exemplars achieves state-of-the-art accuracy on the GSM8K benchmark of math word problems.
- **CoT prompting can beat finetuned GPT-3.** The reported GSM8K result surpasses even finetuned GPT-3 with a verifier.
