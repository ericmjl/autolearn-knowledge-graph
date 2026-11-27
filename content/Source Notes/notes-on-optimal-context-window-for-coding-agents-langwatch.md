---
type: "source-note"
title: "Notes on: Optimal Context Window for Coding Agents | LangWatch"
raw: "optimal-context-window-for-coding-agents-langwatch"
url: "https://langwatch.ai/research/finding-the-optimal-context-window"
created_at: "2026-11-27T11:01:34Z"
updated_at: "2026-11-27T11:01:34Z"
---
- Archived full text: [[optimal-context-window-for-coding-agents-langwatch|Full archived text, with credits]]
- Link: <https://langwatch.ai/research/finding-the-optimal-context-window>

## What it says

A case study of one engineer's agentic coding fleet over 162 days (287,748 deduplicated API calls, 2,451 agents, 873 compactions, 201 judged steps) measures both sides of the context-window trade. Cumulative cost scales as C^2.5 (exponent 2.55, R^2 = 0.994), each doubling of window costs roughly 6x. LLM-judge audits find the active context invariant at 6,000-8,500 tokens across a 16.6-fold range of window sizes, yet compaction carries a real behavioural cost: operator corrections rise to 41.9% in the five steps after a compaction against a 17.7% within-session baseline, and stay elevated past 100 steps. Reconciling cost and disruption yields an operating range of 250,000-450,000 tokens differentiated by task type, and the study argues the dominant lever is enlarging the verbatim tail preserved across compaction (median 0.8% survives) rather than widening the window.

## Claims drawn from this source

- **Cumulative cost of reaching a window size C grows as C^2.5.** Fitted exponent 2.55 with R^2 = 0.994 across 2,451 agents; reaching 100k costs a median 1.4M tokens, 200k costs 9M, and 800k costs 338M, so doubling the window costs roughly 6x. Prompt caching multiplies the constant, not the exponent.
- **The active context is invariant to window size.** Judges marked the items each step actually drew on; the active context sits at 7,949-8,452 tokens across a 16.6x range of median window sizes (38,886 to 644,962), falling from 47.5% to 2.5% of the window as a share. The judged minimum sufficient context is near 1,500 tokens in every band except the largest.
- **Cost-optimal compaction threshold converges at 220,000-240,000 tokens.** The amortised cycle model puts the optimum at 220,000 tokens (region 170k-316k within 10%; below ~110k fails outright). The mechanical reference-distance frontier independently puts coverage-per-cost peak at 240,000 tokens: 100k captures 72.4% of repeat references, 200k 77.6%, and 500k 82.6%, an asymptotic ceiling.
- **Compaction carries a measurable behavioural cost.** Over 128,853 observations, operator corrections reach 41.9% in the five steps after compaction against a 17.7% baseline (2.37x), persist beyond 100 steps, and do not track tool-error rate (flat at 2.6-3.2%). The audit that scores steps is blind to exactly this failure mode, so every compaction verdict is biased optimistic.
- **Recommended operating range is 250,000-450,000 tokens, differentiated by task type.** PR driving 200k-250k (2% verbatim dependence, zero materially degraded), research 250k-300k, QA and dogfooding 250k-350k, building 300k-450k, code understanding 300k-450k (slowest decay). 14% of steps require verbatim old context, concentrated in exact-string reproduction.
- **Preserving a verbatim tail dominates widening the window.** The median compaction event reduces a 574,875-token window to a 4,382-token summary, preserving 0.8% of the raw material. Preserving 30k-60k verbatim tokens costs 25% less per unit of productive work than 600k with a bare digest. The largest determinant of cost is where the agent starts: fresh subagents begin near 30k, while the two incident subagents started at 523,544 and 304,404 tokens.
