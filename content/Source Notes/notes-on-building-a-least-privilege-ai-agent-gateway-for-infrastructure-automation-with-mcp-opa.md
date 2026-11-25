---
type: "source-note"
title: "Notes on: Building a Least-Privilege AI Agent Gateway for Infrastructure Automation with MCP, OPA, and Ephemeral Runners"
raw: "building-a-least-privilege-ai-agent-gateway-for-infrastructure-automation-with-mcp-opa"
url: "https://www.infoq.com/articles/building-ai-agent-gateway-mcp/"
created_at: "2026-11-25T06:01:47Z"
updated_at: "2026-11-25T06:01:47Z"
---
- Archived full text: [[building-a-least-privilege-ai-agent-gateway-for-infrastructure-automation-with-mcp-opa|Full archived text, with credits]]
- Link: <https://www.infoq.com/articles/building-ai-agent-gateway-mcp/>

## What it says

The article builds a reference AI Agent Gateway between autonomous agents and infrastructure: agents discover capabilities over MCP and submit JSON-RPC requests, the gateway validates schema (Zod), authorizes via Open Policy Agent, enqueues isolated short-lived execution, and emits OpenTelemetry traces. Agents are treated as untrusted requesters that never hold credentials or call infrastructure APIs directly. The reference implementation is local-first and minimal, but the article maps its enterprise evolution: stronger isolation, signed plan catalogs, explicit human approval, and regional runners, plus operational SLOs that pause automation when governance degrades.

## Claims drawn from this source

- **Agents are untrusted requesters behind a gateway, never direct holders of credentials.** At its core, the gateway acts as a control boundary; AI agents never interact with infrastructure APIs directly. Every request passes through a centralized gateway that validates intent, enforces authorization rules, and delegates execution to isolated, short-lived environments.
- **Authorization is policy as code in OPA, evaluated before execution.** The gateway passes context to OPA with four non-negotiable rules: RBAC (sre-bot has full access, deploy-bot is restricted to non-prod), integrity (plan hash must match a registered artifact), safety (plans ending in -destroy.plan are explicitly blocked), and change management (deployments allowed Monday-Friday 09:00-17:00 UTC). OPA denies return 403 and stop execution.
- **Execution runs in ephemeral runners that always clean up.** A short-lived runner pulls the job, creates a unique namespace (run-uuid), executes the plan with kubectl and tofu, and deletes the namespace even if the job fails, guaranteeing no orphaned resources.
- **Observability is built in, with hard SLOs.** Metrics and traces are emitted at each stage; the architecture sets SLOs: policy decision latency under 100 ms, runner start latency under 2 s dev / 5 s staging, denied actions at or below 2%, sandbox teardown under 30 s, audit log availability under 5 minutes. When SLOs degrade, automation must pause.
- **Enterprise scale adds isolation, signatures, human approval, and regional runners.** At scale, teams move ephemeral runners into lightweight VMs (Firecracker or Kata Containers) or dedicated short-lived clusters, replace plan-hash checks with signed plan catalogs (Sigstore-style) for chain of custody, return a Pending status with an external signed approval token (Slack or Jira) for high-risk actions, and deploy runners regionally with policy determining where execution is permitted.
- **Separating intent from execution makes safety and debugging simpler.** Letting agents describe what they wanted to do while runners control how it happened simplifies both safety and debugging: policy violations, invalid requests, and execution failures surface as distinct signals instead of being tangled together.
- **Guardrails must execute as part of the system, not as documentation.** Static guidelines, access reviews, and best-practice documents were easy to bypass; controls enforced by the gateway and evaluated on every request consistently held because agents never interacted with infrastructure APIs directly.
