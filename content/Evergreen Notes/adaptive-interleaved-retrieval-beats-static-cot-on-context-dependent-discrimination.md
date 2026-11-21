---
type: "evergreen"
title: "Adaptive interleaved retrieval beats static CoT on context-dependent discrimination"
created_at: "2026-11-21T12:56:26Z"
updated_at: "2026-11-21T12:56:26Z"
inputs: ["notes-on-benchmarking-llms-and-llm-based-agents-in-practical-vulnerability-detection-for-code", "interleaved-reasoning-and-acting-ground-steps-in-external-sources"]
provenance_urls: ["https://arxiv.org/html/2503.03586", "https://arxiv.org/abs/2210.03629", "https://arxiv.org/abs/2005.11401"]
refutation_status: "untested"
answers_questions: ["Does interleaving reasoning and retrieval actions still beat plain chain-of-thought on current models, or has long-context CoT caught up?"]
---

# Adaptive interleaved retrieval beats static CoT on context-dependent discrimination

Agent synthesis

Adaptive interleaving of reasoning and retrieval beats static chain-of-thought when a task demands iterative, context-dependent discrimination. In the JitVul pairwise vulnerability benchmark, ReAct agents that reason, pull callers/callees, and observe beat plain LLMs and dependency-augmented LLMs on pairwise accuracy (the ability to tell a vulnerable function apart from its patched benign version), with average gains of 9.46% over Dep-Aug with GPT-4o-mini and 8.42% with GPT-4o, and the largest single gain up to 16.61%. Plain LLMs post higher F1 scores, but that metric is inflated by over-predicting the vulnerable label (more than 90% in some settings) while precision stays near 50%, so F1 hides exactly the discrimination the benchmark measures. CoT and few-shot examples lift plain LLMs' pairwise accuracy by 1.26% to 17.76%, and Dep-Aug's fixed Top-5 similarity-ranked context can inject noise, which is why its pAcc sometimes drops below Plain LLM.

The mechanism is the same one that made interleaving compelling in ReAct: on-demand retrieval shaped by the model's own reasoning, instead of a one-shot context dump. ReAct agents invoke tools one to three times per case in JitVul; the paper's two-version case studies show the agent finding a caller (daemon_serviceloop) that makes the vulnerable function's risk visible. Static CoT just front-loads instructions; it cannot decide which callers to fetch or when to stop. Long-context windows don't fix this, because the failure is not the window size but the lack of a stopping signal tied to evidence, and weak foundation models cannot even complete the loop (Llama-3.1-8B collapses to the benign label). Pairwise accuracy exposes the gap that single-label F1 hides.

The old ReAct evidence said interleaving grounds steps in external sources and reduces hallucination over chain-of-thought on HotpotQA, Fever, ALFWorld, and WebShop; JitVul adds that the same effect survives current, strong models on a context-dependent task, and that static prompting shines only on flatter, isolated-function tasks where the context is already in the prompt. Both notes point the same way: interleaving wins when the task needs adaptive, iterative context; static CoT remains competitive otherwise. (See: interleaved reasoning and acting ground steps in external sources.) Do not let a higher F1 from a flatter prompting strategy fool you into dropping the agent loop for tasks where discrimination is the point.

## Where it comes from

- [[notes-on-benchmarking-llms-and-llm-based-agents-in-practical-vulnerability-detection-for-code|Benchmarking LLMs and LLM-based Agents in Practical Vulnerability Detection for Code Repositories]]

## What this builds on

- [[interleaved-reasoning-and-acting-ground-steps-in-external-sources|Interleaved reasoning and acting ground steps in external sources]]
