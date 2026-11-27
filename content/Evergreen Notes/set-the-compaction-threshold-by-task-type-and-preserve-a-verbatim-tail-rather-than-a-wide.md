---
type: "evergreen"
title: "Set the compaction threshold by task type, and preserve a verbatim tail rather than a wide window"
created_at: "2026-11-27T11:02:09Z"
updated_at: "2026-11-27T11:02:09Z"
inputs: ["notes-on-optimal-context-window-for-coding-agents-langwatch", "clearing-compaction-and-memory-divide-context-management-by-failure-mode"]
provenance_urls: ["https://langwatch.ai/research/finding-the-optimal-context-window", "https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools", "https://www.anthropic.com/research/effective-context-engineering-for-ai-agents", "https://addyosmani.com/blog/ai-coding-workflow/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["How do you choose compaction trigger and keep thresholds for a specific workload, and what does lossy compaction cost in probe-verifiable detail fidelity?"]
---
Agent synthesis

Set the compaction threshold by task type and preserve a verbatim tail rather than a wide window. The reconciled picture, where the cookbook's three context primitives meet the LangWatch case study, is that the threshold is a per-task knob, not a global constant. The cookbook separates clearing, compaction, and memory by failure mode; the LangWatch study measured what compaction actually costs and what it actually saves. Cumulative cost scales as C^2.5, so each doubling of window costs roughly 6x, while the active context stays invariant at 6,000-8,500 tokens across a 16.6-fold range of windows. Threshold tuning alone is the visible knob, but it is the wrong one to push: the median compaction preserves only 0.8% of the window it replaces, and the harm concentrates at that discontinuity.

The behavioral evidence sharpens the decision. Operator corrections rise to 41.9% in the five steps after a compaction against a 17.7% baseline, and stay elevated past 100 steps, while tool-error rate stays flat at 2.6-3.2%, a decision-quality effect, not an execution effect. The judge audit that scores the steps taken cannot see this, so every compaction verdict is biased optimistic. 14% of steps genuinely require verbatim old context, the exact-string edits, and 85% would survive a counterfactual summary. Those two findings point the same way: set the threshold by task type (PR driving 200k-250k, QA 250k-350k, building and code understanding 300k-450k) and preserve a verbatim tail of 30k-60k rather than a 4,382-token digest, which costs 25% less per unit of productive work than a 600k window with a bare digest.

The largest cost driver is where the agent starts, not where it compacts. A fresh subagent begins near 30k tokens; a forked subagent begins wherever the parent was (523,544 and 304,404 in the incident) and pays the power-law toll from a running start. The cookbook's memory primitive and the LangWatch study's per-workload trigger tuning are the two instruments that fit this: per-primitive knobs set to the workload, fresh context for the agents that only need a short reach, and saved notes that survive the session when the work outlives the window. Start with the matching primitive for the workload, keep the tail verbatim, and do not litigate a wide window on cost grounds: on the token axis it loses by one to two orders of magnitude (see: context signals outrank context size).

## Where it comes from

- [[notes-on-optimal-context-window-for-coding-agents-langwatch|Optimal Context Window for Coding Agents | LangWatch]]

## What this builds on

- [[clearing-compaction-and-memory-divide-context-management-by-failure-mode|Clearing, compaction, and memory divide context management by failure mode]]
