---
type: "evergreen"
title: "Focused multi-agent graphs still drift, so stability needs instrumentation"
created_at: "2026-11-22T14:01:23Z"
updated_at: "2026-11-23T14:04:28Z"
inputs: ["notes-on-agent-drift-quantifying-behavioral-degradation-in-multi-agent-llm-systems-over-extended", "focused-agents-outperform-tool-heavy-monoliths", "notes-on-sentinelagent-graph-based-anomaly-detection-in-llm-based-multi-agent-systems"]
provenance_urls: ["https://arxiv.org/abs/2601.04170", "https://blog.langchain.dev/langgraph-multi-agent-workflows/", "https://en.wikipedia.org/wiki/Multi-agent_system", "https://arxiv.org/html/2505.24201v1"]
refutation_status: "untested"
answers_questions: ["What mechanisms keep multi-agent graphs from drifting into emergent dialects and protocol divergence as agents get stronger?", "How does protocol drift in multi-agent systems get detected or contained in production long-horizon runs?"]
---
Agent synthesis

Focused multi-agent graphs still drift over extended interactions: every added boundary is another channel where inter-agent coherence decays, and the drift comes from the interaction itself, not from any single agent's prompt. The Agent Drift source defines drift as progressive degradation of behavior, decision quality, and inter-agent coherence, with semantic, coordination, and behavioral manifestations, and proposes the Agent Stability Index, a composite metric across twelve dimensions. SentinelAgent adds the enforcement side: execution is modeled as a dynamic interaction graph, with agents and tools as nodes and typed, timestamped edges for messages and invocations, and the system labels nodes and edges with behavioral status at runtime. Drift that never appears in any single agent shows up as an anomalous subgraph, so coordination stays auditable (see: unstructured dialogue trades coordination for observability).

The two instruments answer the same failure at different resolutions. ASI is a periodic metric for whether the graph is on-task; graph-based oversight answers what happened and which hop caused it. The topology matters for both. Round-robin pipelines drift gradually across iterations and need intermediate checks on state transformations. A central orchestrator can misclassify and propagate the error through every worker even when each behaves per spec. A shared ledger lets an early-stage injection poison later rounds, so detection must reason temporally across the ledger, not over one screenful of messages.

The combination shows something neither source states alone: stability is not a property added at the handoff, it is a property of an always-on oversight layer that feeds back into routing, memory, and re-anchoring. SentinelAgent's Event Monitor streams traces into the graph, the Behavior Analyzer judges node and edge status at runtime, and the Risk Responder emits tiered alerts with root-cause attribution and remediation recommendations; periodic human audits refine the behavior model and attack-path library. Build ASI-style monitoring and graph-based oversight into any multi-agent graph before it runs longer than a few dozen turns, treat drift as a routing and containment signal, and refine the detection model with human experts at cold start and audit it periodically.

## Where it comes from

- [[notes-on-agent-drift-quantifying-behavioral-degradation-in-multi-agent-llm-systems-over-extended|Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems Over Extended Interactions]]
- [[notes-on-sentinelagent-graph-based-anomaly-detection-in-llm-based-multi-agent-systems|SentinelAgent: Graph-based Anomaly Detection in LLM-based Multi-Agent Systems]]

## What this builds on

- [[focused-agents-outperform-tool-heavy-monoliths|Focused agents outperform tool-heavy monoliths]]
