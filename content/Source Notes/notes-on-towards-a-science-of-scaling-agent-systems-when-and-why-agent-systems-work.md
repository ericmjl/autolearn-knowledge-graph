---
type: "source-note"
title: "Notes on: Towards a science of scaling agent systems: When and why agent systems work"
raw: "towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work"
url: "https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/"
created_at: "2026-11-28T08:01:24Z"
updated_at: "2026-11-28T08:01:24Z"
---
- Archived full text: [[towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work|Full archived text, with credits]]
- Link: <https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/>

## What it says

Google Research ran a controlled evaluation of 180 agent configurations across five canonical architectures (one single-agent system and four multi-agent variants: independent, centralized, decentralized, hybrid) on four benchmarks (Finance-Agent, BrowseComp-Plus, PlanCraft, Workbench), across OpenAI GPT, Google Gemini, and Anthropic Claude. The paper challenges the heuristic that more agents is better: multi-agent coordination pays off on parallelizable tasks but degrades performance on sequential ones, and a predictive model of measurable task properties identifies the right architecture for 87% of unseen tasks.

## Claims drawn from this source

- **Multi-agent coordination helps parallelizable tasks but hurts sequential ones.** Through a large-scale controlled evaluation of 180 agent configurations, the authors found that multi-agent coordination dramatically improves performance on parallelizable tasks but degrades it on sequential ones, with the 'more agents' approach hitting a ceiling or even degrading performance.
- **Centralized coordination improved performance by 80.9% over a single agent on parallelizable financial reasoning.** On parallelizable tasks like financial reasoning (e.g., distinct agents simultaneously analyzing revenue trends, cost structures, and market comparisons), centralized coordination improved performance by 80.9% over a single agent.
- **Every multi-agent variant degraded performance by 39-70% on sequential planning tasks.** On tasks requiring strict sequential reasoning (like planning in PlanCraft), every multi-agent variant tested degraded performance by 39-70%; the overhead of communication fragmented the reasoning process, leaving insufficient 'cognitive budget' for the actual task.
- **A tool-coordination trade-off grows with tool count.** As tasks require more tools (e.g., a coding agent with access to 16+ tools), the 'tax' of coordinating multiple agents increases disproportionately.
- **Independent multi-agent systems amplify errors 17.2x; centralized containment cuts it to 4.4x.** Without a mechanism to check each other's work, errors by one agent cascade unchecked; independent multi-agent systems amplified errors by 17.2x, while centralized systems with an orchestrator contained this amplification to just 4.4x, where the orchestrator acts as a 'validation bottleneck'.
- **A predictive model of measurable task properties picks the right architecture for 87% of unseen tasks.** The authors developed a predictive model (R^2 = 0.513) that uses measurable task properties like tool count and decomposability to predict which architecture will perform best. This model correctly identifies the optimal coordination strategy for 87% of unseen task configurations.
