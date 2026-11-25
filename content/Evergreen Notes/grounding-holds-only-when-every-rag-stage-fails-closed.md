---
type: "evergreen"
title: "Grounding holds only when every RAG stage fails closed"
created_at: "2026-11-25T17:02:32Z"
updated_at: "2026-11-25T17:02:32Z"
inputs: ["notes-on-retrieval-augmented-generation-rag-security-cheat-sheet", "grounding-reduces-hallucination-but-cannot-eliminate-it"]
provenance_urls: ["https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["What controls hold up against RAG poisoning beyond citation verification?"]
---
Agent synthesis

Grounding holds only when every RAG stage fails closed. The grounding evidence shows that retrieval anchors the model to supplied sources, but the model can still misread, blend, or ignore that context; the OWASP cheat sheet adds the half retrieval alone cannot provide: RAG redistributes risk across the data pipeline, so each stage needs its own control, not one trust boundary at the prompt. Document provenance wraps the corpus in a separate signed manifest of SHA-256 digests, verified before retrieval, so a poisoned document fails consistency checks against the approved baseline; retrieved chunks carry delimiters treated as data, a 3-5 chunk and 2,000-4,000-token cap, and system-prompt reinforcement after the data; and access control metadata travels with every vector chunk, enforced at retrieval time rather than at ingestion, with per-tenant isolation. Fail-closed behavior ties it together: a retrieval failure returns an error instead of answering from model memory, a lapsed access control check returns nothing, a hash mismatch excludes the document and alerts, and a cache lookup failure regenerates rather than serving a stale response. (see: citation verification alone cannot defend a poisoned corpus.) The per-failure-mode scoring from the grounding note answers what broke after a response is generated; the provenance, delimiter, per-chunk access control, and fail-closed controls from the security cheat sheet answer what stops the attack before the model ever sees poisoned content. Operate them together: provenance-verified retrieval with delimiter discipline up front, per-mode scoring and regression tests from production failures after generation, and every failure mode rehearsed fail-closed so the system degrades loudly, not confidently.

## Where it comes from

- [[notes-on-retrieval-augmented-generation-rag-security-cheat-sheet|Retrieval-Augmented Generation (RAG) Security Cheat Sheet¶]]

## What this builds on

- [[grounding-reduces-hallucination-but-cannot-eliminate-it|Grounding reduces hallucination but cannot eliminate it]]
