---
type: "source-note"
title: "Notes on: CORTEX: Token-Level Hallucination Detection in RAG via Comparative Internal Representations"
raw: "cortex-token-level-hallucination-detection-in-rag-via-comparative-internal-representations"
url: "https://arxiv.org/html/2606.31033v1"
created_at: "2026-11-21T19:02:19Z"
updated_at: "2026-11-21T19:02:19Z"
---
- Archived full text: [[cortex-token-level-hallucination-detection-in-rag-via-comparative-internal-representations|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2606.31033v1>

## What it says

CORTEX is a post-hoc, token-level hallucination detection method for retrieval-augmented generation (RAG). It treats hallucination as a localized phenomenon in long-form outputs by comparing internal representations of a separate open-weight LLM under two paired inputs of the same answer (with and without the retrieved references), encoding the reference-induced delta as token-level features, adding an attention-based contextual residual that subtracts reference influence propagated through preceding answer tokens, and applying label-persistence smoothing so predictions align with span-based human annotations. It reports the best token-level detection on two RAG benchmarks and three open-weight LLMs, with competitive answer-level results via simple max-token-score aggregation, and notes that answer-level detection may need global signals beyond token-level ones.

## Claims drawn from this source

- **CORTEX is the first token-level hallucination detector built for RAG.** The paper states CORTEX is the first token-level hallucination detection method specifically designed for RAG, and that it is a practical post-hoc framework that can detect hallucinations in outputs from arbitrary LLMs, including API-based closed-weight models.
- **Faithful tokens change more under references than hallucinated tokens.** CORTEX constructs reference-conditioned and no-reference inputs of the same answer and computes delta features delta-h_i = h_ref_i - h_no-ref_i; faithful tokens exhibit coherent representational changes when references are provided, while hallucinated tokens show weaker or less coherent changes.
- **Direct-delta alone false-positives indirectly grounded tokens.** Reference influence also reaches a token through preceding answer tokens (r -> t_<i -> t_i), so CORTEX adds a contextual residual c_i = delta-h_i - sum of attention-weighted delta-h_j over preceding tokens, which reduces false positives for tokens indirectly grounded through context.
- **Raw token scores are locally noisy; smoothing aligns them with span annotations.** Human hallucination annotations appear as contiguous spans, so CORTEX applies label-persistence smoothing (p_stay = 0.993 at token level, 0.930 at answer level) that models neighboring labels persisting and marginalizes over span-consistent labels via forward-backward, rather than moving-average smoothing.
- **CORTEX wins token-level detection across both benchmarks and all three LLMs.** On RAGTruth and HalluRAG with Llama-3.1-8B, Qwen3-8B and Mistral-7B, CORTEX achieves the best token-level AP and AUROC in every setting (e.g. Qwen token-level AP 0.5940 and AUROC 0.9372 on RAGTruth), with all components contributing gains in ablations (0.4732 -> 0.5335 -> 0.5940).
- **Answer-level detection needs more than token-level signals.** Aggregating token-level scores by max token score gives competitive answer-level performance, but some answer-level baselines still lead, so the authors conclude token-level and answer-level detection are complementary problems rather than interchangeable ones.
- **The generator can stay closed-weight; an open-weight post-hoc model does the detecting.** The closed-weight generator (e.g. an API model) produces the answer; a separate open-weight LLM exposes hidden states and attention weights and performs the analysis, so no modification of the generation pipeline is needed.
