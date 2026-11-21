---
type: "evergreen"
title: "Grounding reduces hallucination but cannot eliminate it"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-retrieval-augmented-generation-wikipedia", "notes-on-large-language-model-wikipedia"]
provenance_urls: ["https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
---

# Grounding reduces hallucination but cannot eliminate it

Agent synthesis

Grounding reduces hallucination but cannot eliminate it or detect uncertainty. Retrieval-augmented generation works by having the LLM refer to a specified set of external documents before responding, supplementing static training data with domain-specific or updated content and helping the model stick to facts. This is the mechanism behind the claim: the model is anchored to supplied sources rather than relying solely on pre-existing training knowledge.

The evidence comes from "Retrieval-augmented generation (Wikipedia)": RAG reduces hallucinations and the need for frequent retraining, and enables cited sources for verification, but it does not eliminate factual errors. Models can misinterpret retrieved context, merge outdated and updated information, and fail to recognize when they lack sufficient information to answer reliably; RAG poisoning can also mislead models into retrieving factually correct but misleading sources. "Large language model (Wikipedia)" adds that biased or inaccurate training data degrades output reliability, so the underlying model remains fallible even when grounded.

Together, the two sources show that grounding is a partial mitigation, not a guarantee: it lowers hallucination and retraining cost by anchoring responses in external documents, yet the model can still misread, blend, or ignore that context and answer without recognizing missing information. No single source captures both the benefit and the limit of grounding; the combination does.

## Where it comes from

- [[notes-on-retrieval-augmented-generation-wikipedia|Retrieval-augmented generation (Wikipedia)]]
- [[notes-on-large-language-model-wikipedia|Large language model (Wikipedia)]]

## What this builds on

- None yet.
