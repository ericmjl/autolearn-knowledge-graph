---
type: "source-note"
title: "Notes on: AI Agent Regression Testing From Production Failures"
raw: "ai-agent-regression-testing-from-production-failures"
url: "https://www.arthur.ai/column/regression-test-datasets-ai-agents-production-failures"
created_at: "2026-11-27T02:01:14Z"
updated_at: "2026-11-27T02:01:14Z"
---
- Archived full text: [[ai-agent-regression-testing-from-production-failures|Full archived text, with credits]]
- Link: <https://www.arthur.ai/column/regression-test-datasets-ai-agents-production-failures>

## What it says

Arthur AI argues that the highest-value regression test dataset for an AI agent comes from production failures, not handcrafted synthetic prompts. The pattern is a flywheel: a production failure becomes a trace, the trace becomes a test case, the test case joins a golden dataset, and the dataset becomes a release gate in CI/CD. Agents make this harder than traditional software because they are non-deterministic, operate over multi-step trajectories, and face a production input space far larger than any synthetic suite.

## Claims drawn from this source

- **Production failures are the best source of regression tests.** Production failures reflect what users actually did, while synthetic prompts reflect what an engineer imagined; real incidents are authentic edge cases with a concrete definition of what broken looks like.
- **Capture the full execution trace, not just the final error.** A complete trace includes the user request and history, system prompts and version, tool calls with inputs, outputs, and latency, RAG retrieval results, intermediate reasoning state, final response, and metadata (session, user, model, timestamp). OpenInference captures richer LLM detail than OTEL GenAI conventions, with explicit LLM, TOOL, AGENT, CHAIN, and RETRIEVER span types.
- **Classify each failure with one primary failure mode.** A practical agent failure taxonomy tags each incident so teams can cluster similar issues, prioritize fixes, and keep the dataset balanced; most incidents are system-level failures (tool use, retrieval, orchestration) rather than pure model mistakes.
- **Sanitize traces before they become permanent test cases.** Strip or swap PII, remove credentials and secrets, abstract live database IDs and server URLs into deterministic placeholders, and capture external state so it can be mocked; where data is too sensitive, rewrite the case into a synthetic equivalent that preserves the failure pattern.
- **Assert on behavior, not exact string match.** Check that the correct tool was called with valid arguments in the right order, that required facts are present and grounded, that forbidden actions are absent, and that the output conforms to the expected schema; supervised evals compare output against a ground truth, complementing unsupervised evals.
- **Keep evals binary and specific.** Score pass/fail, not a 1-to-10 range; each eval targets one concrete failure mode in a single sentence; anchor judges with examples; use deterministic checks for schema and tool-call verification and reserve LLM-as-a-judge for grounding and tone.
- **Start narrow, cluster, and version the dataset.** Begin with 20 to 50 high-signal cases from the highest-impact incidents, cluster incoming failures (vector embeddings work well) and keep one or two representatives per cluster, and version the dataset like source code alongside prompt and model versions.
- **Run experiments at the right level of isolation and gate on CI/CD.** Prompt experiments (fastest), RAG experiments, and full agent experiments keep the dataset and evals fixed while changing one variable; run the suite on every PR, and require that previously-fixed cases pass before promoting.
