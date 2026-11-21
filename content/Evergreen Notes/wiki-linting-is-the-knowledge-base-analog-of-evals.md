---
type: "evergreen"
title: "Wiki linting is the knowledge-base analog of evals"
created_at: "2026-11-21T03:02:25Z"
updated_at: "2026-11-21T03:02:25Z"
inputs: ["notes-on-llm-wiki-pattern-andrej-karpathy", "notes-on-your-ai-product-needs-evals-hamel-husain"]
provenance_urls: ["https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f", "https://hamel.dev/blog/posts/evals/"]
refutation_status: "untested"
---
Agent synthesis

Periodic wiki linting plays for a knowledge base the same role that evals play for a product: a recurring, systematic check that keeps the artifact healthy rather than trusting it to stay correct by default. In the LLM Wiki pattern, lint is a defined workflow that looks for contradictions, stale claims, orphan pages, missing concept pages, missing cross-references, and data gaps, and can suggest new questions and sources. In the AI product case, robust evaluation systems are the root cause of successful products, and weak evals are the root cause of unsuccessful ones.

The mechanism is parallel. Evals are product-specific checks run on a cadence, from fast unit tests on every change to human/model eval and A/B testing at higher cost, and they feed debugging, data curation, and fine-tuning. Wiki linting is a periodic health check over the compiled knowledge base, catching the same class of failure — drift between the artifact and reality — and it is cheap enough for an LLM to run because maintenance cost is near zero: the LLM does not get bored, does not forget cross-references, and can touch many pages in one pass. Just as eval infrastructure doubles as debugging and data tooling, the wiki's lint pass is also a source of new questions, sources, and filed-back answers.

The evidence comes from two sources: the LLM Wiki pattern (Andrej Karpathy) defines lint as a workflow and notes the wiki is a persistent, compounding artifact with contradictions already flagged, while Your AI Product Needs Evals (Hamel Husain) argues that unsuccessful products almost always fail at evaluation systems and that product-specific evals, not vibe checks or generic benchmarks, are what keep a product healthy. Neither source alone makes the analogy. Together they show that both a product and a knowledge base need a recurring, task-specific check that detects drift and feeds improvement, and that the LLM is well suited to run that check for the wiki the way eval infrastructure runs for the product.

## Where it comes from

- [[notes-on-llm-wiki-pattern-andrej-karpathy|LLM Wiki pattern (Andrej Karpathy)]]
- [[notes-on-your-ai-product-needs-evals-hamel-husain|Your AI Product Needs Evals (Hamel Husain)]]

## What this builds on

- None yet.
