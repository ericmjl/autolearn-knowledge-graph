---
type: "evergreen"
title: "A least-privilege agent gateway enforces policy outside the execution path"
created_at: "2026-11-25T06:02:20Z"
updated_at: "2026-11-25T06:02:20Z"
inputs: ["notes-on-building-a-least-privilege-ai-agent-gateway-for-infrastructure-automation-with-mcp-opa", "stage-mcp-agent-work-so-no-stage-holds-all-three-trifecta-factors"]
provenance_urls: ["https://www.infoq.com/articles/building-ai-agent-gateway-mcp/", "https://martinfowler.com/articles/agentic-ai-security.html", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["What does a staged MCP workflow with per-stage least privilege look like in deployed practice?"]
---
Agent synthesis

A least-privilege agent gateway moves governance outside the execution path so agents never hold credentials or call infrastructure APIs directly. The mechanism is a one-way flow: the agent discovers capabilities over MCP, submits a structured request, and the gateway validates schema, authorizes via OPA policy as code, queues a short-lived ephemeral runner, and emits traces at each step. OPA rules return 403 on denial, and runners execute in unique namespaces that are deleted even on failure, so blast radius stays bounded and no resources are orphaned. The synthesis combines three ideas none of the inputs states alone: staging, where work is split so no stage holds all three trifecta factors; policy as code, where declarative RBAC, integrity, safety, and change-window checks hold regardless of agent behavior; and observable SLOs, including latency, denial-rate, teardown, and audit-availability targets that pause automation when governance degrades. The enterprise additions, such as stronger isolation boundaries, signed plan catalogs, explicit human approval via a Pending status, and regional runners, extend the same control plane without giving agents more power. What this means in practice is that staged least-privilege design and deployed gateways are two views of one pattern: keep agents untrusted requesters, enforce policy at the boundary, and make every execution auditable (see: stage MCP agent work so no stage holds all three trifecta factors).

## Where it comes from

- [[notes-on-building-a-least-privilege-ai-agent-gateway-for-infrastructure-automation-with-mcp-opa|Building a Least-Privilege AI Agent Gateway for Infrastructure Automation with MCP, OPA, and Ephemeral Runners]]

## What this builds on

- [[stage-mcp-agent-work-so-no-stage-holds-all-three-trifecta-factors|Stage MCP agent work so no stage holds all three trifecta factors]]
