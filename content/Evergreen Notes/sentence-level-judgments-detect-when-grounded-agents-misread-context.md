---
type: "evergreen"
title: "Sentence-level judgments detect when grounded agents misread context"
created_at: "2026-11-21T15:02:34Z"
updated_at: "2026-11-21T15:02:34Z"
inputs: ["notes-on-detect-hallucinations-for-rag-based-systems-amazon-web-services", "grounding-reduces-hallucination-but-cannot-eliminate-it"]
provenance_urls: ["https://aws.amazon.com/blogs/machine-learning/detect-hallucinations-for-rag-based-systems/", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["How can you detect or measure when a grounded/RAG agent is misreading the retrieved context, rather than just trusting that retrieval happened?"]
---
Agent synthesis

Grounding alone cannot tell you whether an agent actually read the retrieved context, but sentence-level grounding judgments can. The mechanism is a measurement layer: the RAG pipeline stores the context, question, and answer for each query, then an independent judge scores each sentence in the answer from 0 (directly grounded in context) to 1 (no basis in context), with the judge kept separate from the Q&A model so it cannot inherit the generation history.

The new source note supplies the four detection approaches and their trade-offs. The LLM prompt-based detector scored 0.75 accuracy and 0.94 precision at one LLM call; the BERT stochastic checker scored 0.76 accuracy and 0.90 recall at N+1 calls by regenerating the answer and flagging sentences that vary across generations; semantic similarity and token similarity detectors are cheap and precise but weak in recall (0.02 to 0.03). The recommendation is the combination: a token-similarity filter to drop the most evident hallucinations, then the LLM prompt-based detector to catch the harder ones, since the LLM detector's cost stays constant as context grows while semantic similarity costs grow with the number of sentences.

The sampled grounding note supplies the limit: RAG reduces hallucinations and retraining cost but cannot eliminate them, because models can misinterpret retrieved context, merge outdated and updated information, and fail to recognize missing information. The synthesis is that grounding and detection are not alternatives. Grounding lowers hallucination; the sentence-level judge measures whether the grounded answer survived the generation intact. A system that grounds and then never checks its own answers repeats the same mistake in the loop; a system that grounds, judges each sentence, and thresholds the score can detect misreads before they reach the user. The BERT stochastic checker fits the same loop as a recall-heavy oracle, catching the variation that the single-pass judge misses when the original generation happens to look plausible.

Start with a token-similarity filter in front of a separate LLM prompt-based judge, keep the judge's model, memory, and parameters independent of the Q&A call, and tune the threshold per domain. Use the BERT stochastic checker when recall matters more than latency, since it pays N+1 calls for 0.90 recall.

## Where it comes from

- [[notes-on-detect-hallucinations-for-rag-based-systems-amazon-web-services|Detect hallucinations for RAG-based systems | Amazon Web Services]]

## What this builds on

- [[grounding-reduces-hallucination-but-cannot-eliminate-it|Grounding reduces hallucination but cannot eliminate it]]
