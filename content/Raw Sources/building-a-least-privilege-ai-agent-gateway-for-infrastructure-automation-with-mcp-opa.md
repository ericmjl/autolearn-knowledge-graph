---
title: "Building a Least-Privilege AI Agent Gateway for Infrastructure Automation with MCP, OPA, and Ephemeral Runners"
type: "raw-source"
url: "https://www.infoq.com/articles/building-ai-agent-gateway-mcp/"
author: "Nabin Debnath"
publication: "InfoQ"
published: "2026-02-23"
archived: "2026-11-25T06:01:09Z"
---

> [!quote] Original source
> **Author(s):** Nabin Debnath  
> **Title:** Building a Least-Privilege AI Agent Gateway for Infrastructure Automation with MCP, OPA, and Ephemeral Runners  
> **Published in:** InfoQ  
> **Date:** 2026-02-23  
> **Original:** <https://www.infoq.com/articles/building-ai-agent-gateway-mcp/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-building-a-least-privilege-ai-agent-gateway-for-infrastructure-automation-with-mcp-opa|Source note]]
Themes: [[Agent design patterns]], [[Loop engineering]]
Why it was archived: What does a staged MCP workflow with per-stage least privilege look like in deployed practice?

## Archived text

Key Takeaways

- Use a dedicated AI agent gateway to place governance boundaries outside execution systems, preventing agents from directly interacting with sensitive infrastructure.
- Use policy as code with OPA to authorize every agent-initiated action based on identity, intent, and context instead of embedding authorization logic in application code.
- Use OpenTelemetry-based observability to verify, debug, and audit agent behavior through traces, metrics, and logs rather than relying on inferred correctness.
- Use the MCP, OPA, and ephemeral runner combination as a reusable pattern for securing AI-driven continuous integration and continuous delivery (CI/CD), infrastructure automation, and internal tooling workflows.
- Use short-lived, isolated execution runners to contain the blast radius of agent-driven operations and ensure predictable cleanup after every action.

The Problem: Agents Without Guardrails

Many engineering teams are experimenting with automation beyond traditional scripts and pipelines. Instead of humans clicking through dashboards or manually approving changes, a practice often referred to as "ClickOps", some organizations are beginning to delegate operational tasks to autonomous or semi-autonomous agents. These agents may generate infrastructure changes, trigger deployments, or respond to operational signals with little or no human intervention. Unlike traditional CI/CD bots, which execute predefined pipelines with static permissions and deterministic inputs, agent-driven systems introduce dynamic decision-making and cross-system actions at runtime.

This shift introduces a new class of risk. Unlike traditional automation, which is usually scoped to a single tool or workflow, AI-driven agents often operate across multiple systems: CI/CD platforms, cloud APIs, infrastructure as code tools, and internal services. When these agents are granted broad or persistent permissions, they effectively inherit the same level of access as a highly privileged human operator, but without the same contextual judgment or accountability.

For example, in a multi-region deployment, a standby region may not be actively serving traffic but is critical for failover. An agent responding to a cost optimization or remediation signal may misinterpret the lack of traffic as unused capacity and modify or terminate resources in the standby region, causing severe impact when traffic later fails over from the primary region, with no clear approval trail or human decision point to hold responsible.

The consequences of failure in this space are concrete. An agent misinterpreting an instruction can initiate destructive infrastructure changes, such as tearing down environments or modifying production resources. A compromised agent identity can be abused to exfiltrate secrets, create unauthorized workloads, or consume resources at scale. In practice, teams often discover these issues late, because traditional logs record what happened, but not why an agent decided to act in the first place.

For organizations, this liability creates operational and governance challenges. Incidents become harder to investigate, change approvals are bypassed unintentionally, and security teams are left with incomplete audit trails. Over time, this problem erodes trust in automation itself, forcing teams to either roll back agent usage or accept increasing levels of unmanaged risk.

One approach is to limit or block agent-driven actions entirely, but this action undermines the value agents are meant to provide. A more sustainable approach is to introduce an explicit control layer between agents and the systems they operate on. In this article, we focus on an AI Agent Gateway, a dedicated boundary that validates intent, enforces policy as code, and isolates execution before any infrastructure or service API is invoked.

Rather than treating agents as privileged actors, this model treats them as untrusted requesters whose actions must be authorized, constrained, observed, and contained.

Design Principles

Before diving into the individual principles, it helps to establish what the AI Agent Gateway is at a structural level, drawing from established production security and platform patterns rather than AI-specific theory.

At its core, the gateway acts as a control boundary between autonomous agents and infrastructure systems. Agents never interact with infrastructure APIs directly. Instead, every request passes through a centralized gateway that validates intent, enforces authorization rules, and delegates execution to isolated, short-lived environments. This separation allows organizations to introduce AI-driven automation without giving agents persistent or unrestricted access to critical systems.

Figure 1 provides a macro-level view of this architecture and shows how requests flow from an AI agent through policy evaluation, controlled execution, and observability. Unlike a simple API wrapper or proxy, the gateway does not forward agent requests directly. It externalizes intent validation, policy decision-making, and execution into separate components, preventing agents from holding credentials or invoking infrastructure APIs themselves.

Figure 1: Macro Architecture of the AI Agent Gateway (Debnath, 2026)

With this structure in place, the gateway architecture adheres to the following design principles:

- Policy as Code externalizes authorization logic into declarative policies (OPA), avoiding hardcoded access rules inside application code.
- Least Privilege prevents direct agent communication with infrastructure APIs. The gateway mediates every request and limits execution to the minimum required permissions.
- Ephemeral Execution forces actions to run in short-lived, isolated environments that are destroyed immediately after execution.
- Observability by Default tracks every request and execution, producing traces, metrics, and audit logs, and enabling inspection and post-incident analysis.
- Versioning and Auditability tracks requests using plan hashes, idempotency keys, and immutable job metadata, ensuring repeatability and traceability.
- Local First, Cloud-Ready runs the same architecture locally for experimentation and testing, while remaining portable to production environments.

Reference Architecture

The gateway architecture follows a defense in depth model, a well-established security principle in infrastructure and cloud systems. Rather than relying on a single control to prevent misuse, defense in depth applies multiple, independent safeguards so that failure in one layer does not result in full system compromise. This approach is commonly used in Zero Trust networking, cloud IAM design, and production-grade CI/CD pipelines. In agent-driven systems, relying on a single control, such as prompt constraints or static tool allow lists, is insufficient because agents make decisions at runtime and may act across multiple tools and systems in ways that cannot be fully anticipated or constrained by a single safeguard.

In the context of AI-driven automation, defense in depth means that no single component, neither the agent, nor the gateway, nor the execution environment, has enough authority on its own to cause damage. Each layer performs a narrow, well-defined role, and every transition between layers is validated.

This principle is reflected in how the architecture deliberately separates who requests an action from where that action is executed. AI agents are treated as untrusted requesters. They can discover capabilities and submit structured requests, but they never interact with infrastructure APIs directly. All execution happens behind a strict gateway that enforces validation, authorization, and isolation.

The flow through the system is intentionally one-way, enforcing the invariant that no execution occurs without prior authorization and isolated execution:

- Discovery

The agent uses the Model Context Protocol (MCP) to discover which tools are available and what inputs they require.

- Request

The agent invokes a tool (for example, apply_infra) using a JSON-RPC call.

- Validation

The gateway validates the request schema, computes a plan hash, enriches the request with identity and context, and sends it to OPA for authorization.

- Decision

If OPA denies the request, the gateway returns a 403 response and execution stops. If approved, the request is converted into a job and placed onto the execution queue.

- Execution

A short-lived runner pulls the job, creates an isolated namespace, applies the infrastructure plan, and deletes the environment after completion.

- Observability

Metrics and traces are emitted at each stage, allowing dashboards to track policy decisions, execution latency, and failure modes in real time.

This separation ensures that even if an agent behaves unexpectedly due to prompt errors, misconfiguration, or compromise, the blast radius is constrained. Authorization decisions are made before execution, execution occurs in isolated environments, and every step is observable and auditable.

In Figure 2, we can see the complete request-to-execution workflow enforced by the AI Agent Gateway. The diagram shows how an agent request is validated, authorized, queued, executed in an isolated environment, and fully observed, with clear stop points when policy denies an action.

Figure 2: End-to-end request and execution workflow for the AI Agent Gateway (Debnath, 2026)

About This Reference Implementation

This article presents a reference implementation designed to illustrate governance boundaries for AI-driven automation, rather than a production-hardened security platform.

The accompanying repository intentionally prioritizes architectural clarity over completeness. It demonstrates how intent, authorization, and execution can be separated and enforced through a gateway pattern, while keeping the implementation minimal and locally runnable.

As a result, some controls discussed in the article are shown as architectural patterns rather than fully enforced guarantees. For example, Kubernetes namespaces provide logical isolation for ephemeral execution, but do not yet enforce least-privilege access through scoped service accounts, network policies, or workload identities. Similarly, plan integrity is validated at the policy layer using hashes, but those hashes are not cryptographically bound to signed artifacts executed by the runner. Observability is described in terms of OpenTelemetry-based traces and metrics, but the reference code illustrates where instrumentation belongs rather than wiring a complete telemetry pipeline.

Project Blueprint

The AI Agent Gateway is designed as a composition of narrowly scoped components rather than a single, monolithic service. Each component addresses a distinct responsibility: request mediation, authorization, or execution so that agent behavior can be governed, audited, and evolved independently of infrastructure execution details. This separation is intentional and reflects the core design goal of minimizing blast radius while keeping the system understandable and testable.

This section outlines how the AI Agent Gateway is constructed from a small set of focused components, each responsible for a single concern. The goal is to make the system understandable, auditable, and evolvable by design, rather than embedding policy, execution, and orchestration logic into a single service.

At a high level, the architecture is split into three parts, each communicating through well-defined contracts to support replaceability and testability:

- The Gateway (API layer) accepts agent requests, validates intent, enforces authorization decisions, and coordinates execution.
- The Policy Layer encapsulates all authorization and safety rules using policy as code.
- The Execution Layer performs approved actions inside isolated, short-lived environments.

This separation allows each layer to evolve independently. Policies can change without redeploying the gateway, execution environments can be hardened without touching authorization logic, and agents can be replaced or upgraded without impacting infrastructure controls.

The following subsections walk through each component in detail, starting from request handling, moving through policy enforcement, and ending with isolated execution.

Component Overview

The project layout reflects this separation explicitly. Rather than grouping files by language or deployment unit, the repository is organized by responsibility. This structure is optimized for architectural clarity rather than language or framework-specific conventions:

agent-gateway/

├── mcp/              # Component 1: TypeScript Gateway Service

│   └── server.ts     #   - Handles JSON-RPC & OPA Checks

├── policies/         # Component 2: OPA Policy Engine

│   └── agent_authz.rego # - Defines "Who can do What"

├── runner/           # Component 3: Ephemeral Runner

│   └── runner.py     #   - Python script to execute Terraform in Kind

├── infra/            # Sample Infrastructure (OpenTofu Plans)

└── docker-compose.yml # Orchestration

Terraform/OpenTofu is used here as a concrete execution example, but the same execution pattern applies to other backends such as cloud CLIs, deployment tools, or internal automation scripts.

Prerequisites for this build include Docker, Kind (Kubernetes v1.26+), Node.js v20+, Python 3.11+, and the OPA CLI.

Reference Implementation

The complete, runnable reference implementation for this article is available as an open-source project on GitHub and is intended as a reference and demonstration of the architectural patterns described, not as a production-hardened baseline.The repository contains the MCP gateway, OPA policies, ephemeral runner, and a Docker-based local setup that allows readers to reproduce the examples and experiments described in this article.

The Gateway (MCP Layer)

We start by building the coordination layer of the system, rather than a decision-making component. We chose the Model Context Protocol (MCP) specifically because it decouples the agent from the tool definition. This decision allows us to swap the LLM or the agent framework without rewriting our governance layer which is a crucial requirement for avoiding vendor lock-in.

We implemented the Gateway logic in mcp/server.ts file to handle two critical tasks: discovery and enforcement.

First, we define the apply_infra tool structure so the agent understands the required inputs (plan, path, hash, and environment), constraining agent behavior to explicitly declared capabilities and preventing it from inventing or invoking undeclared actions:

// mcp/server.ts - Tool Definition

if (method === "tools/list") {

  return res.json(rpcResult(id, {

    tools: [

      { 

        name: "apply_infra", 

        description: "Apply an OpenTofu/Terraform plan in sandbox", 

        inputSchema: ApplyInfraParams.shape 

      }

    ]

  }));

}

Next, when the tool is called, we rely on Zod for strict schema validation. We then pass the context to OPA. Note that we do not execute the infrastructure change here; we only queue it.

// mcp/server.ts - Tool Execution

if (method === "tools/call") {

  const { name, arguments: args } = params;
  
  // 1. Validate Schema

  const parsed = ApplyInfraParams.safeParse(args);

  if (!parsed.success) return res.json(rpcError(id, -32602, "Invalid params"));

  // 2. Authorize via OPA

  const decision = await authorize({

    action: name,

    actor, // Extracted from JWT/mTLS

    plan: { path: args.planPath, hash: args.planHash, env: args.env },

    time: new Date().toISOString()

  });

  if (!decision) return res.json(rpcError(id, 403, "Policy denied"));

  // 3. Enqueue Job (Asynchronous)

  const job = await enqueueApply({ ...args, actor: actor.id }, args.idempotencyKey);

  return res.json(rpcResult(id, { accepted: true, jobId: job.id }));

}

Policy as Code

We move authorization logic out of the TypeScript code and into Open Policy Agent (OPA). This decision allows us to enforce complex business rules without redeploying the gateway.

For the policy engine, we defined policies/agent_authz.rego to enforce four non-negotiable rules:

- RBAC (sre-bot has full access; deploy-bot is restricted to non-prod).
- Integrity (The plan hash must match a registered artifact).
- Safety (Plans ending in -destroy.plan are explicitly blocked).
- Change management (Deployments are only allowed Mon-Fri, 09:00-17:00 UTC).

# policies/agent_authz.rego

package agent.authz

default allow = false

allow {

    input.action == "apply_infra"

    allow_actor[input.actor.id][input.plan.env]      # RBAC

    plan_is_registered[input.plan.hash]              # Integrity

    not is_destroy_plan(input.plan.path)             # Safety

    in_change_window(time.parse_rfc3339_ns(input.time)) # Change Window

}

# Role Definitions

allow_actor := {

    "sre-bot": {"dev":true, "staging":true, "prod":true},

    "deploy-bot": {"dev":true, "staging":true}

}

is_destroy_plan(path) {

    endswith(path, "-destroy.plan")

}

# Monday to Friday 9am-5pm

in_change_window(t) {

    ns := time.parse_rfc3339_ns(input.time)

    day := time.weekday([ns, "Local"])

    is_weekday(day)

    clock := time.clock([ns, "America/New_York"])

    hour := clock[0]

    hour >= 9

    hour &lt; 17

}

is_weekday(day) {

    weekdays := {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}

    weekdays[day]

}

The Ephemeral Runner

The runner is the "hands" of the system. We use Python to manage the lifecycle. It ensures the environment is clean before and after execution.

The runner, implemented in Python (runner/runner.py), adheres to a strict workflow:

- Generate a unique namespace (run-uuid).
- Execute the plan using kubectl and tofu.
- Always delete the namespace, even if the job fails.

# runner/runner.py

def main():

    job = json.loads(sys.stdin.read())

    namespace = f"run-{uuid.uuid4().hex[:8]}" 
    
    with tracer.start_as_current_span("apply_infra_execution") as span:

        try:

            # 1. Create Sandbox

            subprocess.run(["kubectl", "create", "ns", namespace], check=True)

            # 2. Execute Infrastructure-as-Code

            subprocess.run(["tofu", "apply", "-chdir=infra", "-auto-approve"], check=True)

            span.set_status(trace.Status(trace.StatusCode.OK))

        finally:

            # 3. Mandatory Cleanup

            subprocess.run(["kubectl", "delete", "ns", namespace, "--wait"], check=False)

This workflow guarantees that we never leave "orphaned" resources running in the cluster.

Execution and Results

With our components built, we can now assemble the system.

Bootstrap the Cluster

Initialize a local Kind cluster to act as our "cloud".

make bootstrap # Wrapper for: kind create cluster

Seed the Data

Push sample Terraform plans into the infra/ directory and calculate their SHA-256 hashes to register them in OPA.

Test the Happy Path

Simulate a valid agent request. You should see the Gateway accept the JSON-RPC call, and within seconds, a new namespace will appear and disappear in your Kind cluster .

# Expect: {"accepted": true, "jobId": "..".}

curl -X POST http://localhost:8080/rpc ...

Test the Guardrails

Try modifying the request to use an unauthorized actor or a destructive plan (infra/app-destroy.plan). The Gateway should return an immediate 403 Forbidden error, proving that OPA is intercepting the request before it reaches the runner.

We must anticipate how this system breaks. The architecture accounts for these specific risks :

Scaling to Enterprise

The architecture described so far is intentionally minimal and suitable for local experimentation and controlled environments. However, as teams move from individual workflows to organization-wide adoption, several aspects of the system need to evolve while preserving the same control plane semantics. These changes are not about adding complexity, but about meeting the operational, security, and compliance constraints that emerge at scale.

One of the first pressure points is execution isolation. Kubernetes namespaces provide a reasonable sandbox for local testing and early prototypes, but they are often insufficient in regulated or multi-tenant environments. As adoption grows, teams typically move ephemeral runners into stronger isolation boundaries, such as lightweight virtual machines (Firecracker or Kata Containers, for example) or dedicated, short-lived Kubernetes clusters. This shift allows organizations to enforce stricter tenant separation and satisfy audit requirements without changing how agents or policies are defined.

Another scaling concern is artifact trust. In early stages, validating a plan hash inside policy is often enough to prevent accidental drift. At enterprise scale, this approach does not hold. Plans must be traceable, verifiable, and attributable. Many teams address this by introducing a signed plan catalog backed by an internal artifact registry or tooling such as Sigstore. This allows the policy layer to verify not only the integrity of a plan, but also who produced it and when, turning execution into a verifiable chain of custody rather than a best-effort safeguard.

As the impact of changes increases, fully automated execution is rarely acceptable. High-risk actions, such as production changes or destructive operations often require explicit human approval. Instead of embedding approval logic inside the agent or the runner, the gateway becomes the coordination point. When approval is required, the gateway returns a Pending status and instructs the agent to retry only after a signed approval token is issued through an external system such as Slack or Jira. This keeps human decision-making visible and auditable without weakening the automation boundary.

Finally, geography becomes a governance concern. In multi-region environments, execution must occur close to the infrastructure being managed, while control logic remains centralized. Agents should not decide where work runs. Instead, ephemeral runners are deployed regionally, and policy determines where execution is permitted. This policy decision prevents agents from crossing regulatory or data residency boundaries while preserving a single, consistent control plane.

Together, these changes preserve the core design principles of the gateway while allowing it to operate under real-world enterprise constraints. The system scales not by giving agents more power, but by tightening execution boundaries and making trust explicit.

Operational SLOs

Performance is not a secondary concern in agent governance. If authorization or execution becomes slow or unpredictable, teams will bypass the system.

The following Service Level Objectives (SLOs) are designed to protect both developer trust and operational safety:

- Policy Decision Latency (&lt; 100 ms)

Authorization must be fast enough to remain invisible to the agent. Slow policy checks lead to retries, timeouts, or direct API access outside the gateway.

- Runner Start Latency (&lt; 2s Dev / &lt; 5s Staging)

Ephemeral execution is only viable if startup cost remains low. Longer startup times usually mean something is wrong with the runner setup, either the images are too heavy, the cluster is under load, or the isolation rules are slowing things down.

- Denied Actions (≤ 2%)

A high denial rate often indicates poor tool design or overly coarse policies. This metric helps teams identify friction before agents are retrained to work around controls.

- Sandbox Teardown Time (&lt; 30s)

Cleanup latency directly affects blast radius. Long-lived sandboxes increase cost, leak credentials, and complicate incident response.

- Audit Log Availability (&lt; 5 min)

Governance is ineffective if evidence arrives after the fact. Audit data must be queryable during an incident.

These SLOs are enforced through alerts. When they degrade, automation needs to pause.

Conclusion

Building and exercising this system locally, intentionally triggering policy violations, failed executions, and cleanup edge cases made one thing clear early on: Agent safety is not something you retrofit with documentation or model tuning. It only works when guardrails execute as part of the system itself.

The most effective control was placing governance outside the execution path. Static guidelines, access reviews, and best-practice documents were easy to bypass during automation experiments. In contrast, controls enforced by the gateway and evaluated on every request consistently held, because agents never interacted with infrastructure APIs directly. Treating governance as a system boundary and not an afterthought that changed how safely automation could evolve.

Separating intent from execution also proved critical. Letting agents describe what they wanted to do, while runners controlled how it happened, simplified both safety and debugging. Policy violations, invalid requests, and execution failures surfaced as distinct signals instead of being tangled together. This separation made it possible to tighten policies without breaking workflows, and to harden execution without touching authorization logic.

Observability played an equally important role, even in a local setup. Traces and logs that captured policy decisions, execution steps, and sandbox cleanup made agent behavior inspectable rather than assumed. Instead of trusting that an agent "did the right thing", we could verify what happened, when it happened, and why a decision was allowed or denied.

Finally, ephemeral execution fundamentally changed how risky experimentation felt. Knowing that every action ran in a short-lived environment with mandatory teardown made it safe to test destructive scenarios without leaving residual state behind. This approach reduced the cost of failure and encouraged stricter policies, because mistakes were contained by design.

Taken together, these lessons point to a broader conclusion: The safety of AI-driven automation improves less through smarter models and more through explicit, enforceable boundaries. By decoupling intent (agents), authorization (policy as code), and execution (ephemeral runners), the least privilege AI agent gateway turns abstract AI risk into concrete engineering constraints. Trust in agents, in this model, is not a belief, it is something you can observe, measure, and enforce.
