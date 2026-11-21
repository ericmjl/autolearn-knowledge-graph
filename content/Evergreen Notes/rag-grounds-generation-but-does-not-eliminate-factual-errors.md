---
type: "evergreen"
title: "RAG grounds generation but does not eliminate factual errors"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-retrieval-augmented-generation-wikipedia", "notes-on-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks"]
provenance_urls: ["https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://arxiv.org/abs/2005.11401"]
refutation_status: "untested"
---

# RAG grounds generation but does not eliminate factual errors

Agent synthesis

RAG grounds LLM responses in external documents and improves factuality, but models can still misinterpret retrieved context and produce false statements from correct sources. The mechanism is retrieval before generation: the model first refers to a specified set of documents—via embeddings, vector databases, retrieval, prompt augmentation, and generation—supplementing static training data with domain-specific or updated content, and in the original formulation pairs a pre-trained seq2seq model with a dense vector index of Wikipedia accessed through a pre-trained neural retriever.

The Wikipedia source states that RAG reduces hallucinations and the need for frequent retraining and enables cited sources for user verification, yet does not eliminate factual errors: models can misinterpret retrieved context, merge outdated and updated information, and fail to recognize when they lack sufficient information, and RAG poisoning can mislead models into retrieving factually correct but misleading sources. The RAG for Knowledge-Intensive NLP Tasks source reports that RAG sets state of the art on three open-domain QA tasks and produces more specific, diverse, and factual language than a state-of-the-art parametric-only seq2seq baseline, while noting that provenance for model decisions and updating world knowledge remain open problems.

Together, the sources show that grounding shifts knowledge into an inspectable, updatable external store and measurably improves factuality and specificity, but interpretation, conflict handling, and uncertainty recognition remain failure modes that no single source alone fully captures.

## Where it comes from

- [[notes-on-retrieval-augmented-generation-wikipedia|Retrieval-augmented generation (Wikipedia)]]
- [[notes-on-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks|Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks]]

## What this builds on

- None yet.
