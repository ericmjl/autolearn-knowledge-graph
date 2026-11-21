---
type: "source-note"
title: "Notes on: Detect hallucinations for RAG-based systems | Amazon Web Services"
raw: "detect-hallucinations-for-rag-based-systems-amazon-web-services"
url: "https://aws.amazon.com/blogs/machine-learning/detect-hallucinations-for-rag-based-systems/"
created_at: "2026-11-21T15:01:39Z"
updated_at: "2026-11-21T15:01:39Z"
---
- Archived full text: [[detect-hallucinations-for-rag-based-systems-amazon-web-services|Full archived text, with credits]]
- Link: <https://aws.amazon.com/blogs/machine-learning/detect-hallucinations-for-rag-based-systems/>

## What it says

AWS describes four practical techniques for detecting hallucinations in RAG systems (LLM prompt-based detection, semantic similarity, BERT stochastic checking, and token similarity), compares them on accuracy, precision, recall, and cost, and recommends a combination: a token similarity filter for the most evident hallucinations plus an LLM-based detector for the harder ones.

## Claims drawn from this source

- **RAG reduces but does not remove hallucinations, so detection must run on the context-question-answer triple.** Most hallucination detection techniques focus on the prompt and the response alone, but RAG-based applications have additional context available, and new techniques exploit it. The pipeline stores context, question, and the LLM answer for each query.
- **An LLM prompt-based detector scores each sentence 0 to 1 for context-grounding and beats other methods on precision within one LLM call.** The detector provides the context and statement to a separate LLM and asks it to output a hallucination score between 0 (directly based on context) and 1 (no basis in context). The LLM, memory, and parameters are kept independent of those used for Q&A, and the threshold is tuned per dataset. It scored 0.75 accuracy and 0.94 precision with 1 LLM call.
- **A BERT stochastic checker detects hallucinations by comparing the original answer against N stochastic resamples.** The approach generates N random samples from the LLM, embeds sentences, and computes cosine similarity between the original paragraph and its stochastic variants. Factual sentences remain consistent across generations (high BERT scores) while hallucinated sentences vary (low scores). It scored 0.76 accuracy and 0.90 recall at N+1 LLM calls.
- **Semantic similarity and token similarity detectors are fast and cheap but only catch the most obvious hallucinations.** Semantic similarity uses cosine similarity between embeddings of context and answer (1 minus the similarity as the hallucination score). Token similarity counts shared tokens and BLEU between answer and context. Both showed accuracy around 0.47-0.48, precision near 0.90-0.96, and recall near 0.02-0.03.
- **The LLM prompt-based detector is the most cost-effective because its cost is constant in context and response size.** Unlike the semantic similarity detector, whose cost is proportional to the number of sentences in the context and response, the LLM prompt-based detector uses a single LLM call regardless of length (cost varies with input tokens).
- **The recommended pipeline layers a cheap filter with a stronger detector.** The authors recommend using a token similarity detector to filter out the most evident hallucinations and an LLM-based detector to identify more difficult ones. BERT stochastic checking is preferred when recall is the priority; LLM prompt-based and semantic methods when precision is the priority.
