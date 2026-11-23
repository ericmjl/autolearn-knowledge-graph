---
type: "evergreen"
title: "Claim-level faithfulness is the actionable check that a grounded model used its context"
created_at: "2026-11-22T18:03:39Z"
updated_at: "2026-11-22T18:03:39Z"
inputs: ["notes-on-how-to-evaluate-rag-faithfulness-with-llm-as-a-judge-langfuse", "grounding-reduces-hallucination-but-cannot-eliminate-it"]
provenance_urls: ["https://langfuse.com/resources/engineering/rag-faithfulness-evaluation", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["How can you verify that a grounded model actually used the retrieved context rather than blending it with prior knowledge?"]
---
Agent synthesis

Claim-level faithfulness is the actionable check that a grounded model used its context. Grounding, as the linked note argues, anchors a model in external documents and lowers hallucination, yet cannot guarantee it: the model can still misread, blend, or ignore the retrieved context. Faithfulness closes that gap by scoring the answer against the exact documents retrieved for it, not against a ground-truth answer or world knowledge. The mechanism is claim decomposition: the answer is split into atomic factual statements, an LLM judge labels each claim supported or unsupported by the retrieved context, and the share of supported claims is the score, with the unsupported-claim list localizing whether the failure is in generation (the context contained the fact and the model ignored it) or retrieval (the context never contained it).
The Langfuse evidence makes the judge concrete: claim extraction beats holistic 1-to-5 ratings, binary decisions beat graded scales, the judge must be forbidden outside knowledge explicitly, allow paraphrase, demand structured output, and pin the judge at temperature 0. Calibration against 20-50 human-labeled answers catches rubric ambiguity, which is the more common failure than a weak judge. Faithfulness runs offline as an experiment with a CI gate that fails a pull request when scores regress, and online as a managed evaluator sampling 5-10% of production traffic, alerting when the average drops and routing low-scoring traces to review. Crucially, the retrieved documents must survive past generation: if the context was thrown away, nothing can be verified against.
Read together with the grounding note, the two sources show that grounding is a partial mitigation whose failures are now measurable: hallucination persists, but faithfulness turns vague trust in the documents into a per-claim number with a where-to-fix payload. (see: grounding reduces hallucination but cannot eliminate it) Start with a claim-extraction judge on sampled traces before trusting any grounding claim, and block releases on faithfulness regression.

## Where it comes from

- [[notes-on-how-to-evaluate-rag-faithfulness-with-llm-as-a-judge-langfuse|How to evaluate RAG faithfulness with LLM-as-a-judge - Langfuse]]

## What this builds on

- [[grounding-reduces-hallucination-but-cannot-eliminate-it|Grounding reduces hallucination but cannot eliminate it]]
