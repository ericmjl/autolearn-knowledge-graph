---
type: "source-note"
title: "Notes on: Your AI Product Needs Evals (Hamel Husain)"
raw: "your-ai-product-needs-evals-hamel-husain"
url: "https://hamel.dev/blog/posts/evals/"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---
- Archived full text: [[your-ai-product-needs-evals-hamel-husain|Full archived text, with credits]]
- Link: <https://hamel.dev/blog/posts/evals/>

## What it says

Hamel Husain argues that unsuccessful AI products almost always share a root cause: a failure to build robust evaluation systems, and that product evals tailored to users' tasks are needed beyond vibe checks and general model benchmarks. He describes a three-level evaluation stack—unit tests, human/model eval, and A/B testing—with increasing cost and cadence, and shows how a strong eval system creates a virtuous cycle that also powers debugging, data synthesis/curation, and fine-tuning. The case study of Rechat's Lucy assistant illustrates how plateauing performance was broken by systematic evaluation rather than more prompt engineering. Key principles: remove friction from looking at data, keep things simple, and reuse eval infrastructure for other activities.

## Claims drawn from this source

- **Weak evals are the root cause of unsuccessful AI products.** Unsuccessful products almost always share a common root cause: failure to create robust evaluation systems. Vibe checks are useful but not enough.
- **Use product-specific evals, not generic benchmarks.** Evals must be tailored to users' tasks and measure something different from general model benchmarks. Generic evaluation frameworks should not be relied on.
- **Three evaluation levels with rising cost.** Level 1 unit tests, Level 2 model & human eval, Level 3 A/B testing; cost rises from Level 1 to Level 3, dictating cadence (every change, set cadence, significant changes).
- **Unit tests should be fast, scoped, and frequent.** Assertions scoped to features/scenarios should run on every code change, be reusable for data cleaning and retries, and be updated from observed failures; 100% pass rate is not required.
- **LLMs can generate tests, data, and critiques.** LLMs can synthesize test cases, brainstorm assertions, generate synthetic data, and critique/label outputs; synthetic inputs can replace waiting for production data.
- **Model-based eval must be aligned with humans.** Use the most powerful affordable model to critique outputs, track agreement with human labelers (precision/recall rather than raw agreement), and periodically re-check alignment.
- **Eval infrastructure doubles as debugging and fine-tuning tooling.** Traces, assertions, and search tools used for evaluation also enable fast debugging, and eval-driven data curation/synthesis feeds fine-tuning, which is best for syntax, style, and rules.
- **Remove friction from inspecting traces and data.** Traces should be rendered in domain-specific ways (e.g., custom lightweight tools), and humans should examine as much data as possible, starting with all test and user traces.
