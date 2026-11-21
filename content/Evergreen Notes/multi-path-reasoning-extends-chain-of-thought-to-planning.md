---
type: "evergreen"
title: "Multi-path reasoning extends chain-of-thought to planning"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-chain-of-thought-prompting-elicits-reasoning-in-large-language-models-wei-et-al", "notes-on-tree-of-thoughts-deliberate-problem-solving-with-large-language-models"]
provenance_urls: ["https://arxiv.org/abs/2201.11903", "https://arxiv.org/abs/2305.10601"]
refutation_status: "untested"
---
Agent synthesis

Chain-of-thought reasoning improves complex tasks, but deliberate multi-path exploration with lookahead and backtracking extends it to planning problems. Chain-of-thought prompting elicits intermediate reasoning steps that help large models on complex reasoning, while Tree of Thoughts generalizes that approach by treating coherent units of text as intermediate problem-solving steps and exploring multiple reasoning paths.

In "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al., Google, 2022)", generating a chain of thought significantly improves large language models on arithmetic, commonsense, and symbolic reasoning, with reasoning emerging naturally in sufficiently large models and strong GSM8K results. In "Tree of Thoughts: Deliberate Problem Solving with Large Language Models", standard token-level left-to-right decoding falls short when tasks require exploration, strategic lookahead, or pivotal early decisions; ToT lets models self-evaluate choices, look ahead, and backtrack, with significant gains on Game of 24, Creative Writing, and Mini Crosswords.

The reported Game of 24 comparison is especially direct: GPT-4 with chain-of-thought prompting solved only 4% of tasks, while ToT achieved 74% success. Together, the sources show that chain-of-thought supplies the reasoning scaffold, but deliberate multi-path search supplies the missing planning capability; neither source alone makes the full extension to planning as explicit.

## Where it comes from

- [[notes-on-chain-of-thought-prompting-elicits-reasoning-in-large-language-models-wei-et-al|Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al., Google, 2022)]]
- [[notes-on-tree-of-thoughts-deliberate-problem-solving-with-large-language-models|Tree of Thoughts: Deliberate Problem Solving with Large Language Models]]

## What this builds on

- None yet.
