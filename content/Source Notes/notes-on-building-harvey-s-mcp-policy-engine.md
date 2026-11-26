---
type: "source-note"
title: "Notes on: Building Harvey’s MCP Policy Engine"
raw: "building-harvey-s-mcp-policy-engine"
url: "https://www.harvey.ai/blog/building-harveys-mcp-policy-engine"
created_at: "2026-11-26T11:01:20Z"
updated_at: "2026-11-26T11:01:20Z"
---
- Archived full text: [[building-harvey-s-mcp-policy-engine|Full archived text, with credits]]
- Link: <https://www.harvey.ai/blog/building-harveys-mcp-policy-engine>

## What it says

Harvey rebuilt its Connector Library around an MCP Policy Engine that enforces runtime controls beyond initial connector review. It draws on Sondera, Progent, ETDI, and CaMeL ideas: enforce policies outside the model, limit tool privileges, and control information flow. The engine splits runtime enforcement into a Tool Pinner that compares advertised catalogs against approved baselines (flags additions, removals, changes), a sanitizer that strips hidden characters and detects lookalike-character combinations, and a trajectory-level policy evaluator that judges each proposed call against Harvey's structured tool annotations, call history, and Rego policies (Regorus), permitting, denying, or pausing for approval. Failclosed: if checks cannot complete, the call is denied.

## Claims drawn from this source

- **MCP expands the attack surface beyond the protocol guarantee.** MCP provides a common standard for discovering tools, accessing data, and acting across services, but also brings externally supplied tool definitions, content, and interaction requests into an agent's workflow while increasing supply chain risk.
- **Tool poisoning and rug-pull are the two persistent threats.** In a tool poisoning attack, malicious instructions embedded in a tool's definition redirect the agent's behavior; in a rug-pull attack, a server introduces malicious changes after it has been approved.
- **Read/write labels do not capture a tool's blast radius.** A read-only search tool could still disclose confidential information if that information is placed in a query sent to an external service; tools are assessed for capacity (how much information an argument can carry) and authority (what the argument controls).
- **Enforcement sits in the orchestration layer, outside the model.** Mitigations such as safety training, content marking, and classifiers are bypassable and do not meet the Harvey security bar in isolation; policies constrain proposed actions even when the model follows a malicious instruction.
- **Defense-in-depth rests on least privilege, complete mediation, and secure information flow.** Approval to connect a server does not authorize every subsequent action; each partner MCP tool call is checked before execution, and the engine restricts combinations of capabilities that could expose private information or let untrusted content drive consequential actions.
- **The Tool Pinner flags catalog drift but is alert-heavy.** MCP does not require versioning of individual tool definitions, so a tool can change after approval; the pinner records approved tools including model-facing descriptions and input schemas and flags additions, removals, and changes, but generates a substantial volume of alerts.
- **Policies evaluate agent trajectories, not just single calls.** A proposed tool call carries different risks depending on what happened earlier in the workflow, so the engine evaluates sequences of calls; the interpreter never inspects prompt content or customer data.
- **Agent-to-agent cycles and salami-slicing are explicit threat models.** MCP tools that create or invoke agents can form implicit multi-agent systems, where one agent's response prompts another delegation; policies aim to detect and interrupt these cycles, and cumulative changes across many small edits are a modeled attack.
