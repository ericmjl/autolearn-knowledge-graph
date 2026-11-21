---
type: "source-note"
title: "Notes on: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
raw: "retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks"
url: "https://arxiv.org/abs/2005.11401"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---
- Archived full text: [[retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks|Full archived text, with credits]]
- Link: <https://arxiv.org/abs/2005.11401>

## What it says

The source introduces retrieval-augmented generation (RAG), which combines a pre-trained parametric seq2seq model with a non-parametric memory: a dense vector index of Wikipedia accessed through a pre-trained neural retriever. It explores a general-purpose fine-tuning recipe and compares two formulations, one conditioning on the same retrieved passages across the whole sequence and another using different passages per token. RAG sets state-of-the-art on three open-domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation, RAG produces more specific, diverse, and factual language than a state-of-the-art parametric-only seq2seq baseline.

## Claims drawn from this source

- **Pre-trained LMs store factual knowledge but access it poorly.** Large pre-trained language models store factual knowledge in their parameters, yet their ability to access and precisely manipulate that knowledge remains limited. On knowledge-intensive tasks, they lag behind task-specific architectures.
- **Provenance and updating world knowledge remain open problems.** The source notes that providing provenance for model decisions and updating their world knowledge are still open research problems.
- **RAG pairs parametric seq2seq with a Wikipedia dense vector index.** RAG models use a pre-trained seq2seq model as parametric memory and a dense vector index of Wikipedia as non-parametric memory. The index is accessed with a pre-trained neural retriever.
- **Two formulations differ in passage reuse.** One formulation conditions on the same retrieved passages across the whole generated sequence. The other can use different passages per token.
- **RAG sets state of the art on three open-domain QA tasks.** After fine-tuning and evaluation across knowledge-intensive NLP tasks, RAG outperforms parametric seq2seq models and task-specific retrieve-and-extract architectures.
- **RAG generation is more specific, diverse, and factual.** For language generation tasks, RAG models generate more specific, diverse, and factual language than a state-of-the-art parametric-only seq2seq baseline.
- **Differentiable non-parametric access was mainly extractive.** Pre-trained models with differentiable access to explicit non-parametric memory had so far been investigated only for extractive downstream tasks. RAG explores this direction for generation.
