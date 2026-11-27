---
title: "Paper page - TRACE: A Unified Rollout Budget Allocation Framework for Efficient Agentic Reinforcement Learning"
type: "raw-source"
url: "https://huggingface.co/papers/2606.11119"
author: "Heming Zou"
publication: "Huggingface"
published: "2026-06-11"
archived: "2026-11-27T06:01:21Z"
---

> [!quote] Original source
> **Author(s):** Heming Zou  
> **Title:** Paper page - TRACE: A Unified Rollout Budget Allocation Framework for Efficient Agentic Reinforcement Learning  
> **Published in:** Huggingface  
> **Date:** 2026-06-11  
> **Original:** <https://huggingface.co/papers/2606.11119>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-paper-page-trace-a-unified-rollout-budget-allocation-framework-for-efficient-agentic|Source note]]
Themes: [[Agent economics]], [[Evals and agent quality]]
Why it was archived: Does the adaptive width/depth split for test-time search still hold when the search is a multi-turn agentic loop rather than one generation?

## Archived text

TRACE: A Unified Rollout Budget Allocation Framework for Efficient Agentic Reinforcement Learning

Abstract

TRACE is a rollout allocation framework that improves reward contrast in multi-turn agentic reinforcement learning by dynamically distributing resources across tree-structured rollouts based on prefix-level informativeness.

Reinforcement learning with verifiable rewards (RLVR) is a promising approach for enhancing reasoning and agentic behavior in large language models. However, rollout-intensive policy optimization is often limited by insufficient reward contrast, arising when overly simple or complex prompts generate low-variance feedback and when outcome-only rewards assign the same terminal assessment to every decision in a multi-turn rollout. Past efforts have focused on allocating available rollout resources to promising prompts, yet they only leverage sample informativeness at the prompt level and neglect variation in prefix-level informativeness across turns within the same rollout. This work targets multi-turn agentic RL by modeling each ReAct-style thought-action-observation turn as a semantically distinct node, allowing budget allocation to extend from prompt roots to turn-level prefixes with further continuations, which naturally forms tree-structured rollouts. We introduce Tree Rollout Allocation for Contrastive Exploration (TRACE), a unified rollout allocation framework that enhances reward contrast within a fixed sampling budget. Technically, TRACE allocates rollout budget to both prompt roots and intermediate prefixes that are most likely to yield mixed terminal rewards. A shared generalizable predictor estimates conditional success probability at these anchors from prefix histories to guide this allocation. The resulting adaptive tree structure enriches outcome-only feedback and amplifies the policy-update signal. Empirically, TRACE achieves competitive performance and efficiency gains on typical agentic benchmarks, e.g., improving Qwen3-14B Multi-Hop QA average accuracy by 2.8 points over competitive baselines at equal sampling cost.

Community

TL;DR: We make agentic RLVR more sample-efficient by allocating a fixed rollout budget not just across prompts, but across turns within a rollout.

RLVR training is bottlenecked by reward contrast: overly easy/hard prompts give low-variance feedback, and a single outcome-only reward leaves almost no local signal for credit assignment across a long multi-turn rollout. Prior work only allocates budget at the prompt level — once a prompt is picked, each rollout is still an atomic trajectory.

We observe that ReAct-style agentic interaction naturally packages each thought–action–observation step as a node, turning flat rollouts into tree-structured rollouts. This lets us unify prompt filtering, rollout-count allocation, and turn-level branching under one principle — mixed-reward contrast construction: spend budget on anchors (roots and intermediate prefixes) whose descendants are most likely to contain both successes and failures. A single shared predictor estimates conditional success probability from prefix histories to guide a two-stage scheme (global root allocation → local prefix expansion).

Across Mathematical Reasoning, Multi-Hop QA, and Function Calling, TRACE improves accuracy at equal sampling cost — e.g., +2.8 points on Qwen3-14B Multi-Hop QA over competitive baselines.

This is an automated message from the Librarian Bot. I found the following papers similar to this paper.

The following papers were recommended by the Semantic Scholar API

Please give a thumbs up to this comment if you found it helpful!

If you want recommendations for any Paper on Hugging Face checkout this Space

 You can directly ask Librarian Bot for paper recommendations by tagging it in a comment: @librarian-bot recommend

Get this paper in your agent:

hf papers read 2606.11119 Don't have the latest CLI?

curl -LsSf https://hf.co/cli/install.sh | bash Models citing this paper 0

No model linking this paper

Datasets citing this paper 0

No dataset linking this paper

Spaces citing this paper 0

No Space linking this paper

Collections including this paper 0

No Collection including this paper
