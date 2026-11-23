---
type: "source-note"
title: "Notes on: The Agent Access Model"
raw: "the-agent-access-model"
url: "https://blog.cloudflare.com/the-agent-access-model"
created_at: "2026-11-23T17:01:56Z"
updated_at: "2026-11-23T17:01:56Z"
---
- Archived full text: [[the-agent-access-model|Full archived text, with credits]]
- Link: <https://blog.cloudflare.com/the-agent-access-model>

## What it says

Cloudflare proposes the Agent Access Model (AAM), an access architecture for task-scoped agent runs. Against BeyondCorp's human-shaped controls, it argues that agent runtimes fail quietly by granting too much, and that least privilege must become a real-time system with an audit trail. Its five principles are short-lived, bound, task-scoped credentials; enforcement in the harness and network rather than the prompt; exceptional human oversight; grants reviewed from evidence; and a Trust Ratchet that can only narrow capability state across the task execution graph. The architecture pairs an Agent Identity Broker, a Task-Scoped Access Engine, a Mediation Layer, and the Trust Ratchet with a Grant Review Loop and an Agent Activity Log, and separates the single-principal case, which is buildable today, from multiplayer access control, which remains an open problem.

## Claims drawn from this source

- **Least privilege for agents is a real-time system, not a quarterly review.** An agent must have enough authority to complete its task and no more; for large populations of short-lived agents, least privilege is a system that runs in real time and leaves an audit trail, not a policy reviewed every quarter.
- **Credential lifetime should match task lifetime.** Agents are ephemeral but credentials are durable; service accounts with long-lived keys and broad scopes applied to short-lived agents outlive the work they were issued for and remain in memory, logs, or environment variables where they can be replayed.
- **The prompt is not a perimeter.** Prompt instructions do not enforce access; a model can be manipulated by content injected into the data it reads. Enforcement belongs in the harness that mediates tool calls and at the network layer that mediates packets.
- **The Trust Ratchet makes trust stateful and one-directional.** Capability state can only narrow during a task; when a declared protected event occurs, the Trust Ratchet removes capabilities across the task execution graph, and authority removed returns only in a newly authorized task.
- **Credentials are minted short-lived, task-scoped, and sender-constrained.** The Agent Identity Broker issues a credential at dispatch encoding who the agent is, who it acts for, and the task; DPoP binds the token to a proof key held by the harness so a leaked token alone cannot be replayed.
- **MCP does not define per-tool or argument policy.** MCP standardizes requests over defined transports and supplies an OAuth resource-server boundary, but its authorization layer does not define per-tool or argument policy; the harness or tool server must enforce that.
- **Enforcement evidence must come from external control points, not model self-report.** The Agent Activity Log is an append-only record of activity captured by the Identity Broker, Access Engine, harness, Trust Ratchet state store, and network enforcement point; an attacker can influence model self-report through the same inputs that influence actions.
- **Multiplayer access control is an open problem.** Shared-workspace agents act for multiple principals with different permissions; caching an answer computed under Alice's authority and reusing it for Bob is an authorization bug, and no widely deployed end-to-end system closes the whole chain.
