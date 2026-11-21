---
type: "evergreen"
title: "Optimize agent cost and accuracy jointly, not accuracy alone"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-ai-agents-that-matter-kapoor-stroebl-siegel-nadgir-narayanan", "notes-on-building-effective-agents-anthropic"]
provenance_urls: ["https://arxiv.org/abs/2407.01502", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
---
Agent synthesis

Accuracy-only benchmarking makes state-of-the-art agents needlessly complex and costly, so cost and accuracy should be optimized jointly rather than traded blindly. The mechanism is that a narrow accuracy focus rewards complexity and misattributes gains, pushing agents toward heavier architectures than the task requires; joint optimization instead finds configurations that hold accuracy while cutting cost.

In "AI Agents That Matter (Kapoor, Stroebl, Siegel, Nadgir, Narayanan)," the authors argue that current benchmarks narrowly focus on accuracy without attention to other metrics, making state-of-the-art agents needlessly complex and costly, and that this focus leads the community to mistaken conclusions about the sources of accuracy gains. They design and implement one such joint cost-accuracy optimization, showing potential to greatly reduce cost while maintaining accuracy. In "Building effective agents (Anthropic)," the same logic appears from the design side: the most successful implementations used simple, composable patterns rather than complex frameworks, developers should start with the simplest viable solution and add complexity only when it demonstrably improves outcomes, and agentic systems trade latency and cost for performance.

Together, the two sources show that the cost problem is not just an evaluation artifact but a design failure: benchmarks that reward accuracy alone push agents toward complexity, while simple, composable patterns with complexity added only when it pays off deliver comparable performance at lower cost. No single source alone makes the full argument—one diagnoses and proposes the joint optimization, the other supplies the practical simplicity discipline—but their combination shows that cost and accuracy are coupled, and that optimizing accuracy in isolation systematically inflates both complexity and spend.

## Where it comes from

- [[notes-on-ai-agents-that-matter-kapoor-stroebl-siegel-nadgir-narayanan|AI Agents That Matter (Kapoor, Stroebl, Siegel, Nadgir, Narayanan)]]
- [[notes-on-building-effective-agents-anthropic|Building effective agents (Anthropic)]]

## What this builds on

- None yet.
