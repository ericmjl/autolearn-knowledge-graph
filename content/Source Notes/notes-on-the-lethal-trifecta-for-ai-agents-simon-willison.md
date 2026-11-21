---
type: "source-note"
title: "Notes on: The lethal trifecta for AI agents (Simon Willison)"
raw: "the-lethal-trifecta-for-ai-agents-simon-willison"
url: "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---

# Notes on: The lethal trifecta for AI agents (Simon Willison)

- Archived full text: [[the-lethal-trifecta-for-ai-agents-simon-willison|Full archived text, with credits]]
- Link: <https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/>

## What it says

The source argues that LLM agents combining three capabilities—access to private data, exposure to untrusted content, and external communication—are vulnerable to prompt injection attacks that can exfiltrate private data. Because LLMs follow instructions in content regardless of source, malicious text in web pages, emails, or images can hijack the agent. Vendors fix production systems but cannot protect users who mix and match tools (e.g., via MCP), and guardrails are unreliable, so the only safe approach is to avoid the trifecta combination entirely.

## Claims drawn from this source

- **Trifecta combination enables data theft.** An agent with private data access, untrusted content exposure, and external communication can be tricked into sending private data to an attacker.
- **LLMs follow instructions from any source.** LLMs cannot reliably distinguish instruction importance by origin; all content is glued into tokens and fed to the model.
- **Prompt-based defenses are unreliable.** Because systems are non-deterministic and malicious instructions can be phrased infinitely many ways, telling the model not to obey cannot guarantee protection.
- **Exploits seen across many production systems.** Researchers report the exploit against Microsoft 365 Copilot, GitHub's MCP server, GitLab's Duo Chatbot, and many other products; vendors usually fix by locking down exfiltration.
- **Vendor fixes do not protect tool mixers.** Once users combine tools themselves, vendors cannot protect them; mixing those three ingredients leaves them ripe for exploitation.
- **MCP encourages risky tool mixing.** MCP lets users mix tools from different sources, and a single tool can combine all three patterns, as in the GitHub MCP exploit.
- **Guardrails are not trustworthy.** Vendor guardrails claim high detection rates (e.g., 95%), but no 100% reliable prevention is known; 95% is a failing grade in web security.
- **Prompt injection differs from jailbreaking.** Prompt injection is mixing trusted and untrusted content in one context, distinct from jailbreaking, which is injecting prompts to make the LLM do something embarrassing.
