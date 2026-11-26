---
type: "evergreen"
title: "Sufficiency gates, not relevance scores, keep grounded agents from hallucinating"
created_at: "2026-11-26T05:02:33Z"
updated_at: "2026-11-26T05:02:33Z"
inputs: ["notes-on-deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context", "grounding-reduces-hallucination-but-cannot-eliminate-it"]
provenance_urls: ["https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["How can grounded agents detect when retrieved context is insufficient or misleading?"]
---
Agent synthesis

Sufficiency gates, not relevance scores, keep grounded agents from hallucinating. Relevance measures whether a passage matches the query; sufficiency measures whether the passage contains everything needed for a definitive answer. The mechanism is an autorater: a prompted LLM labels each query-context pair sufficient or insufficient, validated against human gold labels at roughly 93% accuracy, then feeds that label into generation-time decisions about answering, retrieving more, or abstaining.

The evidence is concrete. Google's autorater matches human-expert labels on 115 examples at least 93% of the time, outperforming fine-tuned PaLM-24B and ground-truth-in-context checks. Standard benchmarks like FreshQA, HotPotQA, and MuSiQue all hide many insufficient-context instances. And RAG paradoxically increases hallucination: Gemma's incorrect-answer rate jumps from 10.2% with no context to 66.1% with insufficient context, because added context raises confidence, not truth. A selective generation step, trained as a logistic regression model on the sufficiency label and self-rated confidence, beats confidence alone and lifts accuracy on the answered questions by up to 10%.

Paired with the grounding note, this closes the gap it leaves open: grounding reduces hallucination but cannot detect missing information, and this adds the control that detects it (see: grounding reduces hallucination but cannot eliminate it). Passage-match scores and cosine similarity tell you a passage is relevant. A sufficiency gate tells you whether the match is enough.

Run a sufficiency check before generation, retrieve or re-rank context when the gate fails, and emit an honest not-enough-information response when the gap cannot be closed.

## Where it comes from

- [[notes-on-deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context|Deeper insights into retrieval augmented generation: The role of sufficient context]]

## What this builds on

- [[grounding-reduces-hallucination-but-cannot-eliminate-it|Grounding reduces hallucination but cannot eliminate it]]
