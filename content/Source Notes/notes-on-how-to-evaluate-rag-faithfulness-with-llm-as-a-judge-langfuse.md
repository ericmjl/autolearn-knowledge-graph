---
type: "source-note"
title: "Notes on: How to evaluate RAG faithfulness with LLM-as-a-judge - Langfuse"
raw: "how-to-evaluate-rag-faithfulness-with-llm-as-a-judge-langfuse"
url: "https://langfuse.com/resources/engineering/rag-faithfulness-evaluation"
created_at: "2026-11-22T18:01:08Z"
updated_at: "2026-11-22T18:01:08Z"
---
- Archived full text: [[how-to-evaluate-rag-faithfulness-with-llm-as-a-judge-langfuse|Full archived text, with credits]]
- Link: <https://langfuse.com/resources/engineering/rag-faithfulness-evaluation>

## What it says

The page defines RAG faithfulness as a reference-free, claim-based metric: an LLM judge decomposes an answer into atomic factual claims, verifies each claim against the exact context retrieved for that answer, and scores the share of supported claims. It covers judge prompt design (claim extraction over holistic ratings, binary decisions over graded scales, explicit forbidding of outside knowledge, paraphrase tolerance, structured output, pinned temperature), offline experiment runs via the Langfuse Python SDK (v4 experiment runner), managed LLM-as-a-judge evaluators sampling 5-10% of production traffic, and the distinction between offline CI gates and online monitoring/triage. Ragas provides a maintained implementation that can feed the same traces.

## Claims drawn from this source

- **Faithfulness is reference-free.** Faithfulness compares the answer to the retrieved context, not a ground-truth answer, so it can run on any question, including ones nobody has written an expected answer for.
- **Claim-based decomposition beats holistic judgment.** A claim-extraction judge makes many small binary decisions (supported or unsupported) instead of a global 1-to-5 rating, making the aggregate score interpretable and localizing failures to specific sentences.
- **Judges must be forbidden outside knowledge and told to allow paraphrase.** Judges default to marking true statements as supported; the prompt must state that a claim counts as supported only if the context says or directly implies it, even if the claim is true, while still allowing paraphrase.
- **Unsupported-claim lists diagnose where the failure lives.** The list of claims the judge marks unsupported tells you which sentence to fix and whether the failure is in generation (context contained the fact, model ignored it) or retrieval (context never contained it).
- **Faithfulness needs the same context at evaluation time.** The three required inputs are the question, the generated answer, and the exact context retrieved for that answer; if context was thrown away after generation, nothing can be verified.
- **Offline experiments become CI gates; online evaluators monitor production.** The run-level average can gate pull requests when faithfulness regresses; managed evaluators sample 5-10% of production traffic and alert when the average drops, routing low-scoring traces to review.
- **Judging is calibration-sensitive.** The judge should be a stronger model than the generator, pinned at temperature 0, and calibrated once by having a person label 20-50 answers and comparing against the judge's verdicts; low agreement usually means rubric ambiguity rather than a model problem.
