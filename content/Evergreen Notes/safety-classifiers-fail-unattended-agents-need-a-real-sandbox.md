---
type: "evergreen"
title: "Safety classifiers fail; unattended agents need a real sandbox"
created_at: "2026-11-21T04:02:52Z"
updated_at: "2026-11-21T04:02:52Z"
inputs: ["notes-on-breaking-claude-code-opus-5-auto-mode", "prompt-injection-defeats-prompt-defenses-separate-data-content-and-communication"]
provenance_urls: ["https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
---

# Safety classifiers fail; unattended agents need a real sandbox

Agent synthesis

Safety classifiers for coding agents are not containment, so unattended agents belong in a sandbox. The mechanism is that a classifier reads the environment the same way the agent does, so the same nondeterminism that lets the agent fail lets the classifier fail: Johann Rehberger's attack against Claude Code's auto mode works about 80% of the time, tricking the agent into downloading and uncompressing a zip archive, then executing code that imports base64 without noticing that this imports and executes a local struct.py file extracted from the archive. Worse, the classifier itself can become part of the failure: in a few runs auto mode let the malware process start, then blocked the agent's cleanup command, so the detection that should have stopped the attack disabled it. That is the action-layer version of why prompt defenses fail: content that looks dangerous is a signal the classifier reads, but a gate on behavior is not a boundary around the agent. Prompt injection defeats prompt defenses because LLMs cannot reliably tell instructions apart by origin (see: prompt injection defeats prompt defenses; separate data, content, and communication); auto mode shows the same lesson on the other side, where the classifier judges commands instead of text, and still gets it wrong. The lethal-trifecta source argues for architectural separation of private data, untrusted content, and external communication; the auto-mode source adds that the control surface at the point of action is fragile too. The durable fix is containment: run unattended coding agents in a container, VM, or OS sandbox, restrict network egress, monitor the agents, and expose no home directories, SSH keys, or cloud credentials to the runtime. Sandbox the agent, not the prompt.

## Where it comes from

- [[notes-on-breaking-claude-code-opus-5-auto-mode|Breaking Claude Code Opus 5 Auto Mode]]

## What this builds on

- [[prompt-injection-defeats-prompt-defenses-separate-data-content-and-communication|Prompt injection defeats prompt defenses; separate data, content, and communication]]
