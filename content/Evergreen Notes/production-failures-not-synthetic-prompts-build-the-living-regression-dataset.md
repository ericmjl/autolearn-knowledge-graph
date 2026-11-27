---
type: "evergreen"
title: "Production failures, not synthetic prompts, build the living regression dataset"
created_at: "2026-11-27T02:01:43Z"
updated_at: "2026-11-27T02:01:43Z"
inputs: ["notes-on-ai-agent-regression-testing-from-production-failures", "grounding-improves-when-hallucination-is-scored-per-failure-mode"]
provenance_urls: ["https://www.arthur.ai/column/regression-test-datasets-ai-agents-production-failures", "https://www.splunk.com/en_us/blog/artificial-intelligence/rag-failure-modes.html", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["How does a team refresh a living test dataset of grounding failures as production failures appear?"]
---
Agent synthesis

Production failures, not synthetic prompts, build the living regression dataset. The source argues that a failure becomes a trace, the trace becomes a test case, the test case joins a curated golden dataset, and the golden dataset becomes a CI/CD release gate. The grounding note's living test dataset of 100 to 200 real queries from logs fits the same loop: production failures swapped into regression tests as they appear, with the grounding taxonomy (Context Adherence, Chunk Relevance, Completeness, eight failure modes) turning a pile of incidents into a dataset balanced across real weaknesses.

The mechanism: agents are non-deterministic and multi-step, so an input-output pair is not a trace. A complete trace captures prompts, model parameters, tokens, tool calls with inputs, outputs and latency, exactly which retrieval results came back and which did not, plus intermediate reasoning state, which is what makes a failure replayable as a test case. The grounding note scores hallucination per failure mode; the new source note adds the mechanics: classify each incident with one primary failure mode, sanitize PII and secrets, keep one or two representatives per cluster, version the dataset like source code, and gate releases on it.

Together the two say something neither says alone. The grounding note says a living dataset ties it together and lists the tests; it does not say how the dataset grows, versions, and gates releases. The source note gives the growth loop and never mentions grounding or the failure-mode taxonomy. The synthesis is that the two systems reinforce each other: scores per failure mode name what to watch, and the flywheel turns every failure into a gated case. (see: grounding improves when hallucination is scored per failure mode)

Start with 20 to 50 high-signal cases from your highest-impact incidents, classify them against the grounding failure-mode taxonomy, and re-run the suite on every prompt change, model swap, or retrieval tweak.

## Where it comes from

- [[notes-on-ai-agent-regression-testing-from-production-failures|AI Agent Regression Testing From Production Failures]]

## What this builds on

- [[grounding-improves-when-hallucination-is-scored-per-failure-mode|Grounding improves when hallucination is scored per failure mode]]
