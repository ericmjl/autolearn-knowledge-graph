---
type: "evergreen"
title: "Stage MCP agent work so no stage holds all three trifecta factors"
created_at: "2026-11-25T05:02:28Z"
updated_at: "2026-11-25T05:02:28Z"
inputs: ["notes-on-agentic-ai-and-security", "mcp-tool-mixing-expands-capability-but-risks-the-lethal-trifecta"]
provenance_urls: ["https://martinfowler.com/articles/agentic-ai-security.html", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["Beyond avoiding the lethal trifecta entirely, what practical mitigations work for agents that must combine private data access, untrusted content, and external communication?"]
---
Agent synthesis

The safest way to let an MCP-style agent mix tools is not to avoid mixing them, but to split the work so no single stage holds all three trifecta factors. The existing note shows that MCP composition is simultaneously the source of capability and the route to the risk: an augmented LLM wired into open-ended tasks mixes private-data access with untrusted content and external communication, and the moment users mix tools themselves, vendor protections no longer apply. The new source turns that structural fact into an operational stack: minimize each leg of the trifecta, run the agent inside a controlled environment, break the work into stages each of which blocks at least one factor, and keep a human in the loop to review every stage.

The mechanism is staging. A kafka-debug research flow, for instance, does not need the same permissions as the fix: stage one examines the codebase and crafts a research plan, stage two runs that plan with web-search-only access and no sensitive permissions, and stage three returns to the codebase to apply the fix. Each stage then breaks one trifecta factor, so the whole pipeline inherits neither private-data access nor untrusted content nor external communication in a single hands-on context. The new source makes the data leg concrete: never store production credentials in files, keep secrets in memory via environment variables and a secrets CLI, apply temporary privilege escalation, limit tokens to read-only least privilege, and avoid browser-automation MCPs that connect to the real browser, where cookies, sessions, and history turn an inert snapshot of credentials into a live attack surface.

Containers and review do the remaining work. A container isolates the agent from host resources and lets you mount only the source code it needs behind a firewall allow-list of domains, but the new source is explicit that a container is not a panacea: a project loaded inside one that contains credentials and browses untrusted sites still leaks those credentials. And a human must check every stage's output, watching for spurious commands, doctored content, and AI slop, because no guardrail fully separates instructions from data. The synthesis is a checklist none of the two inputs states alone: reduce each leg, stage the work so every stage is safe, sandbox the runtime, and review every step.

What this means in practice is that MCP capability and lethal-trifecta risk are the same composition seen from two sides, and the resolution is operational rather than architectural (see: MCP tool mixing expands capability but risks the lethal trifecta). Design agents so that the stage that reads untrusted content never holds credentials, the stage that holds credentials never touches untrusted content, and both stages show their work to a human before either moves to the next step.

## Where it comes from

- [[notes-on-agentic-ai-and-security|Agentic AI and Security]]

## What this builds on

- [[mcp-tool-mixing-expands-capability-but-risks-the-lethal-trifecta|MCP tool mixing expands capability but risks the lethal trifecta]]
