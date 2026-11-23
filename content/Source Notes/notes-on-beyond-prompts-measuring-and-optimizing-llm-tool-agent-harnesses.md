---
type: "source-note"
title: "Notes on: Beyond Prompts: Measuring and Optimizing LLM Tool-Agent Harnesses"
raw: "beyond-prompts-measuring-and-optimizing-llm-tool-agent-harnesses"
url: "https://arxiv.org/html/2609.05736v2"
created_at: "2026-11-23T13:03:25Z"
updated_at: "2026-11-23T13:03:25Z"
---
- Archived full text: [[beyond-prompts-measuring-and-optimizing-llm-tool-agent-harnesses|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2609.05736v2>

## What it says

The paper studies improving LLM tool agents without retraining by editing the runtime harness around a fixed model: prompts and tool-boundary middleware. It proposes an optimizer-agnostic evaluation protocol (repair/gate/scorecard splits, reported with mean held-out lift, worst-condition lift, repeatability, logged cost, and a budgeted reliable-lift estimator RelLift95) and a concrete optimizer, PRISM, that clusters failures and routes repairs to prompt, middleware, or joint edit surfaces under a three-pattern middleware vocabulary. On BFCL multi-round, tau^2-Retail, and tau^2-Telecom, PRISM achieves the strongest selected-harness profile with mean held-out lifts of 14.2, 14.9, and 10.1 percentage points.

## Claims drawn from this source

- **The harness around a fixed model is the lever, not the model weights.** LLM tool agents can be improved without retraining by modifying the runtime harness: prompts, tool interfaces, middleware, state handling, and recovery logic, scoped here to prompts plus tool-boundary middleware.
- **Peak discovery and selected-harness reliability are different quantities.** MaxLift measures whether search ever finds a strong harness; WorstLift, RR0, and RelLift95 measure whether the optimizer reliably returns and selects one. BH found the best individual harnesses on both tau^2 domains yet returned a selected tail of WorstLift -13.5 pp with negative RelLift95.
- **Middleware edits need a constrained vocabulary.** Middleware mutations are constrained to three tool-boundary edit patterns: silent correction, error blocking, and prerequisite blocking. BH, whose middleware edits are unconstrained, falls below its own prompt-only variant on both tau^2 tasks.
- **Routing and the edit-pattern constraint are the first-order components.** The component ablation finds that routing and the pattern constraint are the only components whose removal is first-order on all three tasks; removing either collapses both mean lift and the reliability tail. Clustering alone is not first-order.
- **Repair/gate/scorecard splits keep scorecard data out of the loop.** Each run partitions benchmark data into repair (search), gate (accept candidates and final pre-scorecard selection), and scorecard (held out from the entire search, touched exactly once) roles; lift is a paired comparison against the baseline on shared scorecard cases.
- **RelLift95(B) is a budgeted lower-tail deployment diagnostic.** Under budget B, the number of affordable independent optimizer runs is floor(B/mean C); selection picks the run with the best pre-scorecard statistic, and RelLift95 is the 5th percentile of selected held-out lift over repeated uses of the same protocol, estimated by bootstrap over observed runs.
- **Runs that fall apart on the repair split are excluded before aggregation.** Runs whose final repair-split reliability falls below 0.5 are excluded as infrastructure failures; per-arm denominators can fall below the design maximum of 16, and the controlled search budget excludes final scorecard evaluation.
