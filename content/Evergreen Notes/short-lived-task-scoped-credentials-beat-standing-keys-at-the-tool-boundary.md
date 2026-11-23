---
type: "evergreen"
title: "Short-lived task-scoped credentials beat standing keys at the tool boundary"
created_at: "2026-11-23T17:03:09Z"
updated_at: "2026-11-23T17:03:09Z"
inputs: ["notes-on-the-agent-access-model", "egress-allowlists-must-be-read-justified-and-paired-with-per-agent-credentials"]
provenance_urls: ["https://blog.cloudflare.com/the-agent-access-model", "https://workos.com/blog/agent-sandbox-egress-defaults", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["How do agent frameworks enforce per-agent credentials and default-deny tool maps at the tool boundary today?"]
---
Agent synthesis

Short-lived, task-scoped credentials enforced at the tool boundary beat standing keys. The Cloudflare source builds the mechanism: an Agent Identity Broker mints a credential at dispatch that expires with the task, bound to a proof key held by the harness, so a stolen token alone cannot be replayed and the model never receives it. Enforcement lives in the harness that brokers tool calls and in the network that mediates packets, not in the prompt. The egress allowlist note supplies the complementary half: an allowlist says where data can go; the task-scoped credential says who holds it and for how long.

The egress note's wiring pairs allowlists with per-agent credentials and a default-deny tool map because a successful injection otherwise reaches an arbitrary outbound path. The new source shows the mechanism underneath that pairing. The Task-Scoped Access Engine intersects the approved task template with the initiating principal's authority at dispatch, then the adapter freezes the request representation and executes exactly that, so the credential cannot widen past the task ceiling. MCP standardizes transports and an OAuth resource-server boundary, but leaves per-tool and argument policy entirely to the harness or tool server, which is where the deny-by-default default lives. The new evidence is that harness and network enforcement fail independently: a harness bug should still meet network policy, and a network misconfiguration should not grant tool access.

The stateful piece is the Trust Ratchet, which can only narrow during a task: a declared protected event strips capabilities across the task execution graph, and removed authority returns only in a newly authorized task. That converts the egress note's "one repository read, one allowed source host, one credential that dies at revocation" into an enforced ceiling rather than an aspiration. The complementary control is an Agent Activity Log fed by external control points, not model self-report, because the model's account of its own behavior can be shaped by the same inputs that shape its actions; the log records whether each covered action read, created, updated, or deleted data and ties each event to the task and its principal.

Start with one bounded agent that touches a system of record, replace standing keys with a short-lived task-scoped credential, route declared tool paths through harness enforcement, and turn on the activity log. The pairing to keep in mind: an allowlist bounds where data flows, and the task-scoped credential bounds who can ask and for how long (see: egress allowlists must be read, justified, and paired with per-agent credentials).

## Where it comes from

- [[notes-on-the-agent-access-model|The Agent Access Model]]

## What this builds on

- [[egress-allowlists-must-be-read-justified-and-paired-with-per-agent-credentials|Egress allowlists must be read, justified, and paired with per-agent credentials]]
