---
type: "source-note"
title: "Notes on: Retrieval-augmented generation (Wikipedia)"
raw: "retrieval-augmented-generation-wikipedia"
url: "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---
- Archived full text: [[retrieval-augmented-generation-wikipedia|Full archived text, with credits]]
- Link: <https://en.wikipedia.org/wiki/Retrieval-augmented_generation>

## What it says

Retrieval-augmented generation (RAG) is a technique that lets LLMs retrieve and incorporate information from external data sources before generating responses, supplementing static training data with domain-specific or updated content. It reduces hallucinations and the need for frequent retraining, and enables cited sources for user verification, but it does not eliminate factual errors: models can misinterpret retrieved context, merge outdated and updated information, and fail to recognize when they lack sufficient information. The source covers the RAG pipeline (embeddings, vector databases, retrieval, prompt augmentation, generation), improvements (encoder, retriever-centric, language-model, chunking, hybrid search), and challenges including RAG poisoning.

## Claims drawn from this source

- **RAG grounds LLM responses in external documents.** LLMs first refer to a specified set of documents, then respond to queries, supplementing pre-existing training data with domain-specific or updated information.
- **RAG reduces hallucinations but does not eliminate them.** It helps LLMs stick to facts, yet the model can still hallucinate around source material or misinterpret context, producing false statements from correct sources.
- **RAG lowers retraining cost.** Rather than retraining the model when new information becomes available, only the external knowledge base needs augmentation, saving computational and financial costs.
- **Prompt stuffing prioritizes retrieved context.** Additional relevant context is added early in the prompt so the LLM prioritizes supplied data over pre-existing training knowledge.
- **Chunking trades focus against context.** Smaller chunks isolate relevant information but omit context; larger chunks retain context but may include irrelevant material and consume input budget.
- **Hybrid search mitigates vector-search misses.** Combining traditional full-text search results with vector-retrieved chunks, then feeding combined text into the model, helps recover key facts semantic search may miss.
- **RAG poisoning can mislead models.** Models may retrieve factually correct but misleading sources, struggle with conflicting information, or merge outdated and updated details; a 2026 study found models easily misled by wrong answers matching their own mistakes.
- **Models may not recognize uncertainty.** Without specific training, LLMs may generate answers even when they lack sufficient information to provide a reliable response.
