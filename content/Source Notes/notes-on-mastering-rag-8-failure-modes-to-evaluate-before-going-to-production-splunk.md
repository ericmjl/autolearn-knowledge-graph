---
type: "source-note"
title: "Notes on: Mastering RAG: 8 Failure Modes to Evaluate Before Going to Production | Splunk"
raw: "mastering-rag-8-failure-modes-to-evaluate-before-going-to-production-splunk"
url: "https://www.splunk.com/en_us/blog/artificial-intelligence/rag-failure-modes.html"
created_at: "2026-11-25T15:01:40Z"
updated_at: "2026-11-25T15:01:40Z"
---
- Archived full text: [[mastering-rag-8-failure-modes-to-evaluate-before-going-to-production-splunk|Full archived text, with credits]]
- Link: <https://www.splunk.com/en_us/blog/artificial-intelligence/rag-failure-modes.html>

## What it says

Splunk argues that RAG systems fail quietly in production because they were never tested against the failure points neither retrieval nor generation has on its own. It enumerates eight failure modes to evaluate before deployment: retrieval quality, hallucinations, privacy breaches, malicious use, security breaches, out-of-domain questions, completeness, and brand damage. Each mode maps to a specific evaluator, and the article describes how to build a living test dataset (real queries plus synthetic edge cases with ground truth annotations), map cases to all eight modes, and keep the dataset growing quarterly from production failures.

## Claims drawn from this source

- **RAG requires systematic testing across eight distinct failure modes.** Retrieval quality, hallucinations, privacy breaches, malicious use, security breaches, out-of-domain questions, completeness, and brand damage are each invisible during standard development and need dedicated evaluation.
- **Retrieval quality is measured by five aspects.** Relevance (query intent vs retrieved content, scored by Context Relevance), diversity (covering different perspectives), top-k document omission (the definitive answer exists but ranks below K), format mismatch, and specificity issues (too vague or buried behind detail), scored by Instruction Adherence.
- **Hallucination has six patterns to watch for.** Noise robustness (extracting the relevant fact from a mixture, scored by Chunk Relevance), negative rejection (declining when context is uninformative), information integration (combining across documents), counterfactual robustness (identifying known errors in sources), unclear queries, and incorrect citations, all gated by Context Adherence, the 0-to-1 metric for closed-domain hallucination.
- **Context Adherence and Completeness act as precision and recall for grounding.** Context Adherence measures closed-domain hallucination (0 to 1); Completeness measures whether responses incorporate all relevant context available. Chunk Relevance tells you which retrieved chunks actually contained useful information, separating retrieval problems from generation problems.
- **Privacy needs an audit, not just a metric.** PII retrieval and context leakage are caught by a PII evaluator, but data retention violations are the quietest and hardest to catch: deletion requests honored in the source system do not cascade to derived chunks, embeddings, and indexes, so a sample of 100 documents with creation dates and deletion flags must be audited.
- **Security breaches are a separate category from misuse.** Emotional manipulation, prefix injection, refusal suppression, and mismatched generalization are attack patterns, covered by a Prompt Injection evaluator against malicious inputs attempting to override system instructions.
- **The test dataset must be living and balanced.** Extract 100 to 200 real queries from logs, add synthetic cases targeting each failure mode, record ground truth (expected document IDs, required facts, acceptable formats, unacceptable hallucinations), and map test cases to all eight modes so no mode is under-tested.
- **Production failures become regression tests.** Version the dataset alongside model versions, add production failures immediately as tests, expect 10 to 20 percent quarterly growth, and audit quarterly for outdated annotations and missing query patterns.
