---
type: "source-note"
title: "Notes on: Retrieval-Augmented Generation (RAG) Security Cheat Sheet¶"
raw: "retrieval-augmented-generation-rag-security-cheat-sheet"
url: "https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html"
created_at: "2026-11-25T17:01:44Z"
updated_at: "2026-11-25T17:01:44Z"
---
- Archived full text: [[retrieval-augmented-generation-rag-security-cheat-sheet|Full archived text, with credits]]
- Link: <https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html>

## What it says

The OWASP RAG Security Cheat Sheet argues that RAG does not reduce risk so much as redistribute it: it creates new attack surfaces at every stage of the pipeline, from ingestion through embedding, storage, retrieval, generation, output validation, and downstream agent integration. It gives practical controls for document provenance and integrity, context window protection, access control metadata on every vector chunk, tenant isolation, embedding distribution monitoring, output validation, caching, supply chain vetting, observability, and fail-closed behavior. Not all controls need to be implemented at once: provenance, context window protection, per-chunk access control, tenant isolation, query normalization, output validation, observability, and fail-closed behavior come first, with signed attribution and tool safety next.

## Claims drawn from this source

- **RAG redistributes risk rather than reducing it.** The cheat sheet states that RAG introduces a unique attack surface distinct from both traditional web application vulnerabilities and standalone LLM risks, and that it redistributes risk across the data pipeline at every stage.
- **Document poisoning is the most common and immediately exploitable RAG attack vector.** Malicious content is injected into the retrieval corpus (uploads with hidden instructions, compromised data sources, insiders modifying documents invisibly, invisible Unicode characters), and is later included in the model's context window when retrieved.
- **Integrity verification must be anchored in a separately controlled, signed manifest.** Record a SHA-256 digest of each approved document in a manifest protected by a digital signature or MAC with keys outside the document store's write permissions, and verify manifest authenticity and document digest before retrieval; a matching digest establishes consistency with the approved baseline, not that content is safe.
- **Retrieved content must be treated as untrusted data, not instructions.** The cheat sheet recommends delimiters and explicit instructions to treat retrieved content as data only, limits of 3-5 chunks and 2,000-4,000 tokens, scanning retrieved chunks for prompt injection patterns, and system prompt reinforcement positioned after retrieved content.
- **Access control metadata must travel with every vector chunk and be enforced at retrieval time.** Store classification, owner, permitted roles, and permitted tenants alongside every chunk; enforce checks at retrieval rather than ingestion; and isolate tenants with separate namespaces or collections and pre-retrieval filtering.
- **Output validation is the last line of defense because model output is untrusted.** Validate all model outputs before returning, apply policy filters for PII and secrets, enforce allowed action schemas for tool calls, and never let retrieved content directly influence tool execution without an intermediate validation step.
- **Fail-closed behavior is required at every stage.** When retrieval fails, return an error instead of answering from model memory; when an access control check fails, return nothing; when hash verification fails, exclude the document and alert; and when cache lookup fails, generate a fresh response rather than serving stale content.
