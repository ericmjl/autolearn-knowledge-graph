---
type: "evergreen"
title: "Egress control is the boundary that makes unattended sandboxes real"
created_at: "2026-11-22T21:01:50Z"
updated_at: "2026-11-22T21:01:50Z"
inputs: ["notes-on-agent-sandbox-egress-control-outbound-allow-listing-blaxel", "safety-classifiers-fail-unattended-agents-need-a-real-sandbox"]
provenance_urls: ["https://blaxel.ai/blog/sandbox-egress-control-outbound-allow-listing", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["What does a real sandbox for unattended coding agents look like beyond containers, and what network/credential controls are needed?"]
---
Agent synthesis

Unattended agent sandboxes fail without egress controls. A container hides the filesystem, but if the sandbox can make any outbound call, the agent becomes an exfiltration path: adversarial content in the model's context becomes instructions, and the generated code sends data to endpoints nobody approved. The Blaxel source measures computer-use agent exfiltration success up to 85% and lays out the patterns that close the path: default-deny domain filtering at the network layer, static egress IPs for source identity where downstream firewalls require them, managed-proxy routes that inject credentials server-side so secrets never touch the execution environment, and an audit of outbound traffic before any rules are written. The mechanism is that no classifier or prompt defense can see this path: the safety-sandbox note shows that classifiers read the same environment the agent does, so they fail on the same inputs, while egress control binds the network to a fixed destination list regardless of what the agent or the attacker intends. Compliance alike forces the same answer: SOC 2, HIPAA, and CSA questionnaires ask what outbound connections the sandbox can make, and undefined egress stalls deals at the procurement stage. The combination to build is audit first, default-deny allow-list, proxy-injected credentials, static IPs for fixed-IP partners, and network controls in the architecture diagram before the review starts.

## Where it comes from

- [[notes-on-agent-sandbox-egress-control-outbound-allow-listing-blaxel|Agent Sandbox Egress Control & Outbound Allow-Listing | Blaxel]]

## What this builds on

- [[safety-classifiers-fail-unattended-agents-need-a-real-sandbox|Safety classifiers fail; unattended agents need a real sandbox]]
