---
type: "evergreen"
title: "Token-level reference deltas localize misreads sentence-level judges only flag"
created_at: "2026-11-21T19:03:33Z"
updated_at: "2026-11-21T19:03:33Z"
inputs: ["notes-on-cortex-token-level-hallucination-detection-in-rag-via-comparative-internal-representations", "sentence-level-judgments-detect-when-grounded-agents-misread-context"]
provenance_urls: ["https://arxiv.org/html/2606.31033v1", "https://aws.amazon.com/blogs/machine-learning/detect-hallucinations-for-rag-based-systems/", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["When does sentence-level grounding judging beat or lose to single-pass answer-level judging for grounded RAG agents?"]
---
Agent synthesis

Token-level reference deltas localize the misreads that sentence-level and answer-level judges only flag. The mechanism is a paired counterfactual view: CORTEX feeds the same answer to a separate open-weight LLM with and without the retrieved references, encodes how each token's internal representation changes in response to the references, subtracts reference influence that propagates through preceding answer tokens, and smooths raw scores into span-consistent labels. Faithful tokens change coherently when references are present; hallucinated tokens barely move, so the delta is a localization signal, not just a reliability score.

The sampled grounding note argues that grounded agents can misread retrieved context, and that sentence-level judges, able to score each sentence from 0 (directly grounded) to 1 (no basis), can detect those misreads while keeping the judge's model and parameters independent of the Q&A call. CORTEX sharpens the same idea one granularity down: the fact that a sentence misreads context is not the same as knowing which tokens in it are ungrounded, and a mixed long-form answer can carry faithful prose beside a hallucinated span. CORTEX's token-level detection costs one pass per generation for the delta features, versus N+1 calls for stochastic-regeneration checkers, and its label-persistence smoothing step aligns raw token scores with the span-shaped annotations humans actually write.

The two approaches converge rather than compete. Sentence-level judges answer which sentences survived grounding intact and stay robust when outputs are short or few-sentence; token-level deltas answer which exact spans are ungrounded and are the only way to localize a single hallucinated clause inside an otherwise correct answer. Answer-level aggregation, as CORTEX demonstrates by max-pooling token scores, is competitive but not best-in-class, which reinforces the grounding note's point that answer-level judging is coarse. Grounding, sentence-level gating, and token-level localization form one layered check on the same grounded answer.

Use a token-level reference-delta detector when long-form RAG output mixes faithful and ungrounded spans, and keep the sentence-level judge as the gate on the whole answer: tune the token-level threshold to catch localized drift, then let the sentence-level layer catch whole-answer misreads, with the judge kept independent of the generator and tuned per domain.

## Where it comes from

- [[notes-on-cortex-token-level-hallucination-detection-in-rag-via-comparative-internal-representations|CORTEX: Token-Level Hallucination Detection in RAG via Comparative Internal Representations]]

## What this builds on

- [[sentence-level-judgments-detect-when-grounded-agents-misread-context|Sentence-level judgments detect when grounded agents misread context]]
