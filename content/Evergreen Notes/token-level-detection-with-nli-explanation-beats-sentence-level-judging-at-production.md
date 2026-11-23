---
type: "evergreen"
title: "Token-level detection with NLI explanation beats sentence-level judging at production volume"
created_at: "2026-11-23T16:01:54Z"
updated_at: "2026-11-23T16:01:54Z"
inputs: ["notes-on-token-level-truth-real-time-hallucination-detection-for-production-llms", "sentence-level-judgments-detect-when-grounded-agents-misread-context"]
provenance_urls: ["https://vllm.ai/blog/2025-12-14-halugate", "https://aws.amazon.com/blogs/machine-learning/detect-hallucinations-for-rag-based-systems/", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["Which sentence-level detectors scale best to long contexts, and what does the cost-vs-recall tradeoff look like at production volume?"]
---
Agent synthesis

Token-level detection with an NLI explanation layer beats sentence-level LLM judging at production volume, because a conditional pipeline spends verification cost only where it matters. The mechanism has three stages: a Sentinel ModernBERT classifier (96.4% accuracy, ~12ms) throws out the ~35% of queries that are not fact-seeking, a token-level detector classifies answer tokens at ~125ms for 4K-token context and ~365ms for 16K, and an NLI explainer runs only on the detected spans, mapping each to ENTAILMENT/NEUTRAL/CONTRADICTION with severity 0/2/4. The new source says token-level detection alone is recall-biased (59% F1 on the hallucinated class, one-third of flags false positives), so the NLI layer supplies precision and explainability; the sampled sentence-level note makes the complementary trade, a cheap token-similarity filter dropping the most obvious hallucinations and then a separate LLM judge (0.75 accuracy, 0.94 precision at one call) catching the harder ones, with the BERT stochastic checker as a recall-heavy oracle at N+1 calls. Together, the notes describe the same loop at different sensitivities: one pre-filters prompts, detects tokens, then explains spans; the other filters tokens, then judges sentences, and both refuse to trust a single pass (see: sentence-level judgments detect when grounded agents misread context). The combination is the rule: cheap detection in front, a separate judge or NLI stage behind it, and outputs that travel as headers so downstream policy can block, disclaim, or queue review. Do not ship one-pass detection as the only check, and decide how intrinsic hallucinations with no tool context get handled before launch, since neither pipeline can verify them.

## Where it comes from

- [[notes-on-token-level-truth-real-time-hallucination-detection-for-production-llms|Token-Level Truth: Real-Time Hallucination Detection for Production LLMs]]

## What this builds on

- [[sentence-level-judgments-detect-when-grounded-agents-misread-context|Sentence-level judgments detect when grounded agents misread context]]
