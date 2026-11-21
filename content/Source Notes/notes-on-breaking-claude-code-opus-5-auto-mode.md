---
type: "source-note"
title: "Notes on: Breaking Claude Code Opus 5 Auto Mode"
raw: "breaking-claude-code-opus-5-auto-mode"
url: "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/"
created_at: "2026-11-21T04:01:43Z"
updated_at: "2026-11-21T04:01:43Z"
---

# Notes on: Breaking Claude Code Opus 5 Auto Mode

- Archived full text: [[breaking-claude-code-opus-5-auto-mode|Full archived text, with credits]]
- Link: <https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/>

## What it says

Simon Willison reports that Anthropic made Claude Code's auto mode the default for protecting coding agents against prompt injection. Johann Rehberger found an attack against it that works about 80% of the time: Claude Code is tricked into downloading and uncompressing a zip archive, then executing code that imports base64 without noticing that this imports and executes a local struct.py file extracted from the archive. In a few runs, auto mode directly prevented the agent from preventing harmful code from continuing to execute: it allowed creation of the malware process but blocked the cleanup command. Willison agrees that the only safe way to run agents when adversarial attention is possible is a sandbox (container, VM, or OS sandbox, restricted network egress, monitoring, no home directories/SSH keys/cloud credentials). A Lobste.rs commenter notes the attack is not a classic prompt injection because no malicious instructions are accidentally followed; it is closer to a confused-environment attack where the nature of the environment the agent is exposed to produces the exploit.

## Claims drawn from this source

- **Claude Code auto mode is Anthropic's default defense for prompt injection.** Anthropic put a great deal of faith in Claude Code's auto mode for protecting coding agent users against prompt injection attacks and recently made it the default, with bold claims about its effectiveness.
- **Auto mode can be broken in about 80% of runs.** Johann Rehberger found an attack against auto mode that he claims works 80% of the time, by tricking Claude Code into downloading and uncompressing a zip archive, then executing code that imports base64 without noticing that this will import and execute a local struct.py file extracted from the archive.
- **Auto mode can block the agent's own cleanup.** In a few cases auto mode directly prevented the agent from preventing harmful code from continuing to execute. Claude detects the compromise, but auto mode blocks the cleanup command.
- **Auto mode is not a substitute for sandboxing.** Willison agrees with Johann's conclusion that the only safe way to run agents in the presence of adversarial attention is with a sandbox: run unattended coding agents in a container, VM or OS sandbox, restrict network egress, monitor agents, and do not expose home directories, SSH keys, or cloud credentials to the agent runtime.
- **The attack is a confused-environment exploit, not a classic prompt injection.** A Lobste.rs commenter points out that at no point are malicious instructions from the website accidentally followed by the LLM; the attack is more a confused environment attack where the nature of the environment the agent is exposed to results in the exploit.
