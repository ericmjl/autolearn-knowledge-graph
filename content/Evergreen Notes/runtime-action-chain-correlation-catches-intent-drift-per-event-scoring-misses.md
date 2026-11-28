---
type: "evergreen"
title: "Runtime action-chain correlation catches intent drift per-event scoring misses"
created_at: "2026-11-28T07:01:58Z"
updated_at: "2026-11-28T07:01:58Z"
inputs: ["notes-on-detecting-intent-drift-in-ai-agents-with-runtime-behavioral-data-armo", "focused-multi-agent-graphs-still-drift-so-stability-needs-instrumentation"]
provenance_urls: ["https://www.armosec.io/blog/detecting-intent-drift-in-ai-agents-with-runtime-behavioral-data/", "https://arxiv.org/abs/2601.04170", "https://blog.langchain.dev/langgraph-multi-agent-workflows/", "https://en.wikipedia.org/wiki/Multi-agent_system", "https://arxiv.org/html/2505.24201v1"]
refutation_status: "untested"
answers_questions: ["How do multi-agent systems detect and attribute drift mid-run without halting execution?"]
---
Agent synthesis

Runtime action-chain correlation detects intent drift that per-event anomaly scoring misses. Baselines ask "is this event different?" and miss the shift that matters, because intent drift lives in the combination and direction of actions: tool invocation, data access, external egress, credential use. The ARMO source calls drift different from anomaly: an individual event, like a database read, can score low against a baseline while the chain that follows (customer_pii query then HTTPS POST to an unknown domain) reveals the goal change. ARMO's answer is a runtime-first architecture: eBPF kernel observation from the first syscall, Deployment-level behavioral profiles that survive pod churn, application-layer context for prompt content and tool parameters, and attack-story correlation across kernel, container, Kubernetes, and application layers, which cuts investigation time by over 90%.

The sampled evergreen on multi-agent graphs states that drift emerges from interaction, not any single agent, and that coordination stays auditable when agent and tool status is labeled as typed, timestamped graph edges. ARMO's runtime correlation is the production-grade version of that argument: the graph of actions is where drift shows up, and the same principle holds for ephemeral infrastructure where pod-level baselines reset constantly. Authored-baselines age within hours; runtime ground truth does not depend on convergence, so detection stays live even during rolling deployment windows. It gives the sampled evergreen's ASI-style monitoring a concrete mechanism, and it gives graph-based oversight a way to distinguish a bad event from a bad chain.

Deployment-level identity is the load-bearing choice: reattach detection to the Deployment or ServiceAccount, not the pod, and profile what actually executed (AI-BOM) so CI/CD churn correlates to specific changes instead of triggering learning mode. Kernel-level signals alone catch symptoms; prompt content and tool invocation parameters are what turn an alert into a root-cause story. (see: focused multi-agent graphs still drift, so stability needs instrumentation)

Build detection on action chains across the full stack, anchor profiles to Deployment identity, and treat per-event anomaly scores as the floor, not the ceiling.

## Where it comes from

- [[notes-on-detecting-intent-drift-in-ai-agents-with-runtime-behavioral-data-armo|Detecting Intent Drift in AI Agents With Runtime Behavioral Data - ARMO]]

## What this builds on

- [[focused-multi-agent-graphs-still-drift-so-stability-needs-instrumentation|Focused multi-agent graphs still drift, so stability needs instrumentation]]
