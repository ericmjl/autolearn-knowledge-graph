---
type: "source-note"
title: "Notes on: Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
raw: "tree-of-thoughts-deliberate-problem-solving-with-large-language-models"
url: "https://arxiv.org/abs/2305.10601"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---

# Notes on: Tree of Thoughts: Deliberate Problem Solving with Large Language Models

- Archived full text: [[tree-of-thoughts-deliberate-problem-solving-with-large-language-models|Full archived text, with credits]]
- Link: <https://arxiv.org/abs/2305.10601>

## What it says

The source introduces Tree of Thoughts (ToT), a framework for language-model inference that generalizes Chain of Thought prompting by exploring coherent units of text ("thoughts") as intermediate problem-solving steps. It argues that standard left-to-right, token-level decoding falls short on tasks requiring exploration, strategic lookahead, or pivotal early decisions. ToT lets models consider multiple reasoning paths, self-evaluate choices, and look ahead or backtrack to make global decisions. Experiments on Game of 24, Creative Writing, and Mini Crosswords report significant gains, including 74% success with ToT versus 4% for GPT-4 with chain-of-thought prompting on Game of 24.

## Claims drawn from this source

- **Standard LMs use token-level left-to-right inference.** The abstract says language models are increasingly deployed for general problem solving but remain confined to token-level, left-to-right decision-making during inference.
- **Token-level decoding limits exploration and lookahead.** This limitation makes LMs fall short in tasks requiring exploration, strategic lookahead, or where initial decisions play a pivotal role.
- **ToT generalizes Chain of Thought prompting.** Tree of Thoughts is presented as a new inference framework that generalizes the popular Chain of Thought approach.
- **ToT explores coherent text units as intermediate steps.** It enables exploration over coherent units of text, called thoughts, that serve as intermediate steps toward problem solving.
- **ToT supports deliberate multi-path decision making.** Models can consider multiple different reasoning paths and self-evaluate choices to decide the next course of action.
- **ToT enables lookahead and backtracking.** The framework allows looking ahead or backtracking when necessary to make global choices.
- **ToT improves non-trivial planning and search tasks.** Experiments on Game of 24, Creative Writing, and Mini Crosswords show ToT significantly enhances problem-solving abilities.
- **ToT greatly outperforms CoT on Game of 24.** GPT-4 with chain-of-thought prompting solved only 4% of Game of 24 tasks, while the method achieved 74% success.
