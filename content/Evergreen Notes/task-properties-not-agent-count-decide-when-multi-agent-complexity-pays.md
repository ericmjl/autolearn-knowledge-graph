---
type: "evergreen"
title: "Task properties, not agent count, decide when multi-agent complexity pays"
created_at: "2026-11-28T08:01:54Z"
updated_at: "2026-11-28T08:01:54Z"
inputs: ["notes-on-towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work", "simple-composable-patterns-beat-complex-frameworks"]
provenance_urls: ["https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/", "https://blog.anthropic.com/building-effective-agents", "https://arxiv.org/abs/2407.01502"]
refutation_status: "untested"
answers_questions: ["What evidence should trigger adding complexity over a simple composable pattern in agentic systems — when does framework machinery measurably pay?"]
---
Agent synthesis

Task properties, not agent count, decide when multi-agent complexity pays. The scaling paper's controlled evaluation of 180 agent configurations gives the evidence the simpler design rule was missing: multi-agent coordination pays when the task decomposes into parallelizable sub-tasks with modest tool density, and it backfires when the task is sequential and tool-heavy. Centralized coordination beat a single agent by 80.9% on parallelizable financial reasoning, where distinct agents can analyze revenue trends, cost structures, and market comparisons at once. Every multi-agent variant degraded performance by 39-70% on sequential planning in PlanCraft, because communication overhead fragmented the reasoning and left insufficient cognitive budget for the actual task.

The mechanism is coordination cost, not agent count. Each added agent taxes the model: tool-coordination grows disproportionately once tasks need 16+ tools, and without a validation step, errors cascade. Independent multi-agent systems amplified errors 17.2x, because agents working in parallel without talking never check each other; centralized systems with an orchestrator contained that amplification to 4.4x, where the orchestrator acts as a validation bottleneck. A predictive model using tool count and decomposability reaches R^2 = 0.513 and picks the right architecture for 87% of unseen tasks.

Read against the simple-composable-patterns note, the design rule sharpens into a diagnosis. That note says start with the simplest pattern and add complexity only when it demonstrably improves outcomes; the Google Research results say what "demonstrably" means: measure the task's sequential dependencies and tool density, and only pay for coordination when decomposition actually exists. Simple patterns stay the default; framework machinery earns its keep only when the task is parallelizable and the tool count is modest. Diagnose decomposition and tool density before adding any coordination machinery, and use an orchestrator rather than independent parallel agents to contain error amplification.

## Where it comes from

- [[notes-on-towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work|Towards a science of scaling agent systems: When and why agent systems work]]

## What this builds on

- [[simple-composable-patterns-beat-complex-frameworks|Simple composable patterns beat complex frameworks]]
