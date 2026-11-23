---
type: "source-note"
title: "Notes on: What your agent sandbox can reach by default — WorkOS"
raw: "what-your-agent-sandbox-can-reach-by-default-workos"
url: "https://workos.com/blog/agent-sandbox-egress-defaults"
created_at: "2026-11-23T06:01:22Z"
updated_at: "2026-11-23T06:01:22Z"
---
- Archived full text: [[what-your-agent-sandbox-can-reach-by-default-workos|Full archived text, with credits]]
- Link: <https://workos.com/blog/agent-sandbox-egress-defaults>

## What it says

WorkOS audits the five hosted coding-agent environments (Codex cloud, Codex local, ChatGPT Work, Claude Code local, Claude Code on the web) and documents what each allows by default, where the boundary does not reach, and what controls can actually bind. The piece argues that egress defaults drift silently, that granting network access is a decision that must be actively justified, and that allowlists compose with credential isolation to bound the blast radius of a successful injection.

## Claims drawn from this source

- **Codex cloud blocks the agent phase by default but still runs setup scripts with unrestricted internet access, with no documented way to restrict setup-phase egress.** Codex cloud: 'By default, Codex blocks internet access during the agent phase', but setup scripts still run with internet access. Secrets are removed before the agent phase starts.
- **Codex cloud's two independent dials (domain allowlist presets and a GET/HEAD/OPTIONS method restriction) are the whole defense against a specific prompt-injection payload.** The docs demonstrate that restricting requests to GET, HEAD, and OPTIONS blocks an agent from reproducing a reported 404 by running one line that exfiltrates a commit and diff. The allowlist preset 'Common dependencies' covers 69 apex domains.
- **Claude Code reads hardening only from user or managed settings, so committing strictAllowlist or masking rules to a repository's .claude/settings.json produces a silent no-op.** strictAllowlist is read from user, managed or CLI settings only; setting it in project or local settings has no effect. The same narrower scope applies to tlsTerminate and mask credential entries.
- **Claude Code's sandboxed Bash tool restricts only Bash commands; file tools, MCP servers, and hooks run on the host, and Anthropic's own verdict is that this is not sufficient for fully unattended runs.** 'The sandboxed Bash tool is built into Claude Code and restricts only Bash commands... is not sufficient for fully unattended runs in either mode.' The reference for unattended work is the dev container with a default-deny iptables firewall.
- **Claude Code on the web publishes a Trusted default allowlist of close to 200 entries, but sessions can still reach four things that bypass the allowlist: GitHub through its separate proxy, enabled MCP connectors, environment API-credential hosts, and the Anthropic API.** 'Whichever level you pick, sessions can still reach four things, because each one takes a path that doesn't go through the session's network allowlist.'
- **Egress policy you cannot observe is egress policy you cannot tune; blocking behavior should be reported back to the caller.** Claude Code locally reports sandbox violations in the blocked command's result, naming the denied path or host; Codex cloud and ChatGPT Work document no blocked-egress visibility at all.
- **An allowlist answers where data can go but not what the agent could read; pairing it with per-agent credentials and a default-deny tool map bounds the blast radius of a successful injection.** 'An allowlist answers where data can go. It says nothing about what the agent could read in the first place.'
- **Granting internet access is an actively justified decision, not a default; AISI's 19-action incident shows that permissions granted for a build step drift as capabilities advance.** The UK AI Security Institute reported 19 catalogued actions across 10 of 122 runs, detected days later by egress monitoring. AISI's first listed lesson: treat granting internet access as a decision that must be actively justified.
