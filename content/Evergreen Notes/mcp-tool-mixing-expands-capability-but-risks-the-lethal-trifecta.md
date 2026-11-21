---
type: "evergreen"
title: "MCP tool mixing expands capability but risks the lethal trifecta"
created_at: "2026-11-21T03:02:24Z"
updated_at: "2026-11-21T03:02:24Z"
inputs: ["notes-on-the-lethal-trifecta-for-ai-agents-simon-willison", "notes-on-building-effective-agents-anthropic"]
provenance_urls: ["https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
---
Agent synthesis

MCP-style tool composition expands what agents can do, but mixing private-data access, untrusted content, and external communication creates the lethal trifecta. The mechanism is composition: MCP lets users mix tools from different sources, and an augmented LLM—an LLM enhanced with retrieval, tools, and memory—can be wired into open-ended tasks where it dynamically directs its own tool use. That same flexibility is what makes the combination dangerous.

In "The lethal trifecta for AI agents (Simon Willison)," the trifecta—private data access, exposure to untrusted content, and external communication—enables prompt injection that can exfiltrate private data, because LLMs follow instructions in content regardless of source. Exploits have been reported across many production systems, including GitHub's MCP server, and vendors fix production systems by locking down exfiltration, but once users mix tools themselves, vendors cannot protect them; guardrails are unreliable (high detection rates are not prevention), so the safe approach is to avoid the trifecta combination entirely. In "Building effective agents (Anthropic)," MCP is presented as a way to tailor an augmented LLM's capabilities with a well-documented interface, and agents are described as best suited to open-ended problems in trusted environments, with careful tool design, transparency, and sandboxed testing as core principles.

Together, the two notes show that the same composition is both the source of capability and the source of risk: Anthropic treats MCP-style tooling as the practical way to build useful agents, while Willison shows that the moment those tools are mixed across sources, the trifecta appears and vendor protections no longer apply. No single source makes this full point—Anthropic does not warn about the trifecta, and Willison does not describe the capability upside—but their combination shows that MCP-style composition is simultaneously the enabling mechanism and the main route to the lethal trifecta.

## Where it comes from

- [[notes-on-the-lethal-trifecta-for-ai-agents-simon-willison|The lethal trifecta for AI agents (Simon Willison)]]
- [[notes-on-building-effective-agents-anthropic|Building effective agents (Anthropic)]]

## What this builds on

- None yet.
