---
type: "source-note"
title: "Notes on: Agent Evaluation Readiness Checklist"
raw: "agent-evaluation-readiness-checklist"
url: "https://www.langchain.com/blog/agent-evaluation-readiness-checklist"
created_at: "2026-11-25T18:05:57Z"
updated_at: "2026-11-25T18:05:57Z"
---
- Archived full text: [[agent-evaluation-readiness-checklist|Full archived text, with credits]]
- Link: <https://www.langchain.com/blog/agent-evaluation-readiness-checklist>

## What it says

LangChain's checklist for building, running, and shipping agent evals. It walks from the simplest end-to-end baseline through trace-level evaluation, dataset construction, grader design, and production hardening. The recurring theme: evals fail when they grade the wrong thing, so the checklist insists on manual trace review, unambiguous success criteria, capability/regression separation, error analysis, and specialized graders before any metric is trusted.

## Claims drawn from this source

- **Start with a few end-to-end evals and add complexity only with evidence.** A few end-to-end evals testing whether the agent completes its core tasks give a baseline immediately, even if the architecture is still changing. Only add complexity when you have evidence that simpler approaches are missing real failures.
- **Manually review 20-50 real traces before building any eval infrastructure.** Spending 30 minutes reading real agent traces teaches more about failure patterns than any automated system. Use LangSmith traces and annotation queues for this.
- **Success criteria must be unambiguous enough for two experts to agree on pass/fail.** If two experts cannot agree on pass/fail, the task needs refinement: unclear success (Summarize this document well) versus clear success (Extract the 3 main action items... each under 20 words with an owner if mentioned).
- **Capability evals and regression evals must be separated.** Capability evals answer 'what can it do?' and start with a low pass rate as a hill to climb; regression evals answer 'does it still work?' and should have ~100% pass rate to catch backsliding.
- **Spend 60-80% of eval effort on error analysis, not on metrics.** Gather traces, open-code them with a domain expert without pre-categorizing, group issues into a failure taxonomy (prompt problems, tool design problems, model limitations, tool failures, data gaps), and keep reviewing until no new categories surface.
- **Rule out infrastructure and data pipeline issues before blaming the agent.** The Witan Labs team found a single extraction bug moved their benchmark from 50% to 73%. Timeouts, malformed API responses, and stale caches frequently masquerade as reasoning failures, so check the pipeline first.
- **Full-turn evals must grade response, trajectory, and state changes, not just say-things.** Check that calendar events actually exist, run the written code, and query the updated rows; an agent that says 'Done!' while the state is wrong still fails.
- **Calibrated specialized graders and isolated trials replace single noisy scores.** Default to code-based graders for objective checks and LLM-as-judge for subjective ones, prefer binary pass/fail, review ~20+ labeled examples to calibrate judges, and ensure each trial runs in a clean isolated environment with no shared state. Track turns, tokens, latency and cost per task alongside quality, and distinguish task failures from evaluation failures.
