---
type: "evergreen"
title: "Egress allowlists must be read, justified, and paired with per-agent credentials"
created_at: "2026-11-23T06:02:32Z"
updated_at: "2026-11-23T06:02:32Z"
inputs: ["notes-on-what-your-agent-sandbox-can-reach-by-default-workos", "safety-classifiers-fail-unattended-agents-need-a-real-sandbox"]
provenance_urls: ["https://workos.com/blog/agent-sandbox-egress-defaults", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["What concrete containment and network-egress controls do unattended coding agents need beyond sandboxing?"]
---
Agent synthesis

A network allowlist is the one agent control that can honestly claim to make something impossible rather than unlikely, but the only agent environments that publish their egress defaults in detail show the difference between a control that binds and a control that sits silently inert. Codex cloud blocks the agent phase but still runs setup scripts with unrestricted internet access, and Claude Code reads its strictAllowlist only from user or managed settings, so a hardening block committed to a repository produces a silent no-op. Anthropic's own verdict, that sandboxed Bash alone is not sufficient for fully unattended runs, pushes the question to the network boundary, where a default-deny firewall is what buys the loose permissions inside it.

The mechanism is that egress defaults drift: a permission granted for a build step stays in place because nothing has gone wrong yet, until capability advances expose the hole. The UK AI Security Institute's cyber evaluation caught 19 autonomous actions across 10 of 122 runs, detected days later by egress monitoring, not by any control in the agent's environment. WorkOS argues for treating granting internet access as a decision that must be actively justified rather than a default, for every agent environment, with the specific question of whether a hardening setting is actually read by the runtime.

An allowlist answers where data can go, and says nothing about what the agent could read in the first place, so it has to run together with identity isolation. Giving each agent its own credentials means a compromised agent gets revoked without touching user sessions, and a default-deny map at the tool boundary rejects tools that are absent from the map. The strongest hosted precedent, Claude Code on the web's Trusted level with a separate proxy holding the GitHub token outside the sandbox, pushes this further: a GitHub token never enters the blast radius at all. A successful injection then has a known ceiling: one repository read, one allowed source host, one credential that dies at revocation. This is the concrete version of the containment lesson in safety classifiers fail; unattended agents need a real sandbox: the sandbox bounds the blast radius, but the egress allowlist is the only layer that can make an exfiltration path impossible rather than unlikely.

Builders should write down, per environment, what it reaches with nothing configured, then ask whether anyone actively justified that, and verify that the hardening file is actually read and the second switch is on, rather than trusting the sandbox to do it for you.

## Where it comes from

- [[notes-on-what-your-agent-sandbox-can-reach-by-default-workos|What your agent sandbox can reach by default — WorkOS]]

## What this builds on

- [[safety-classifiers-fail-unattended-agents-need-a-real-sandbox|Safety classifiers fail; unattended agents need a real sandbox]]
