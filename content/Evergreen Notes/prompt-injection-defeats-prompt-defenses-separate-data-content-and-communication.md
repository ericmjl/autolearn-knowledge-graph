---
type: "evergreen"
title: "Prompt injection defeats prompt defenses; separate data, content, and communication"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-the-lethal-trifecta-for-ai-agents-simon-willison", "notes-on-software-agent-wikipedia"]
provenance_urls: ["https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
---

# Prompt injection defeats prompt defenses; separate data, content, and communication

Agent synthesis

Prompt injection defeats prompt-based defenses, so durable protection comes from architectural separation of private data, untrusted content, and external communication, plus security verification of agent actions. The mechanism is that LLMs cannot reliably distinguish instructions by origin: all content is glued into tokens and fed to the model, so malicious text in web pages, emails, or images can hijack an agent. Because systems are non-deterministic and malicious instructions can be phrased in infinitely many ways, telling the model not to obey cannot guarantee protection.

The source "The lethal trifecta for AI agents (Simon Willison)" argues that an agent combining private-data access, untrusted-content exposure, and external communication can be tricked into sending private data to an attacker, and reports exploits across Microsoft 365 Copilot, GitHub's MCP server, GitLab's Duo Chatbot, and many other products. It also notes that vendor fixes usually lock down exfiltration, but users who mix tools themselves—especially through MCP—remain exposed, and guardrails are not trustworthy. The source "Software agent (Wikipedia)" adds that an agent acts on behalf of a user with decision authority, and that after deciding to act, an agent's action is verified by a security function before being given the user's authority and delivered.

Together, the sources show more than either alone: Willison supplies the failure mode and the architectural boundary, while Wikipedia supplies the control point for agent behavior. The durable pattern is not a stronger prompt but separation of the three ingredients plus verification of actions, because prompt-based instructions cannot reliably separate trusted from untrusted content.

## Where it comes from

- [[notes-on-the-lethal-trifecta-for-ai-agents-simon-willison|The lethal trifecta for AI agents (Simon Willison)]]
- [[notes-on-software-agent-wikipedia|Software agent (Wikipedia)]]

## What this builds on

- None yet.
