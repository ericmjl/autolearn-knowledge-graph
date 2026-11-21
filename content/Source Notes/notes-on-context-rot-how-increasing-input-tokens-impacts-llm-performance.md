---
type: "source-note"
title: "Notes on: Context Rot: How Increasing Input Tokens Impacts LLM Performance"
raw: "context-rot-how-increasing-input-tokens-impacts-llm-performance"
url: "https://www.trychroma.com/research/context-rot"
created_at: "2026-11-21T20:01:56Z"
updated_at: "2026-11-21T20:01:56Z"
---
- Archived full text: [[context-rot-how-increasing-input-tokens-impacts-llm-performance|Full archived text, with credits]]
- Link: <https://www.trychroma.com/research/context-rot>

## What it says

Chroma's technical report evaluates 18 frontier and open-weights LLMs across needle-in-a-haystack extensions, a conversational memory benchmark (LongMemEval), and a synthetic repeated-words replication task, holding task complexity constant while varying only input length. Their results show performance degrades non-uniformly as input length grows: lower needle-question similarity accelerates degradation, distractors compound it non-uniformly, haystack structure consistently hurts, and full prompts leave far behind focused ones. The report argues that context engineering, not context size, is what governs reliability.

## Claims drawn from this source

- **Performance degrades as input length grows, even for simple tasks.** Across all 18 models tested, performance consistently degrades with increasing input length across controlled NIAH, LongMemEval, and repeated-words experiments that hold task complexity constant.
- **Lower needle-question similarity increases the degradation rate.** With needle-question similarity quantified by five embedding models (average text-embedding-3-small, text-embedding-3-large, jina-embeddings-v3, voyage-3-large, all-MiniLM-L6-v2), models degrade faster as similarity drops; PG essay needles span 0.445-0.775 and arXiv needles 0.521-0.829.
- **Distractors compound degradation non-uniformly.** A single distractor already reduces performance relative to the needle-only baseline, and four distractors compound it; distractor 3 causes greater decline than the others, and Claude models abstain under ambiguity while GPT models hallucinate confidently.
- **Haystack structure consistently hurts performance.** Shuffling sentences and removing local coherence consistently improves performance across all 18 models and needle-haystack configurations, despite the intuition that structured order helps.
- **Focused prompts beat full prompts by a wide margin.** On LongMemEval, full 113k-token prompts force retrieval plus reasoning in one call and underperform focused ~300-token prompts across Claude, GPT, Gemini, and Qwen families even with thinking modes enabled.
- **Position of the needle does not matter much for retrieval.** Testing across 11 needle positions shows no notable variation in performance for the NIAH task.
- **Refusals and non-attempts appear at long lengths.** In the repeated-words task across up to 10,000 words, GPT-4.1 refuses about 2.55% of tasks (typically starting around 2,500 words) and Sonnet 3.5 outperforms newer Claude models up to its 8,192-token output limit.
