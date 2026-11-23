---
type: "source-note"
title: "Notes on: Agent Sandbox Egress Control & Outbound Allow-Listing | Blaxel"
raw: "agent-sandbox-egress-control-outbound-allow-listing-blaxel"
url: "https://blaxel.ai/blog/sandbox-egress-control-outbound-allow-listing"
created_at: "2026-11-22T21:01:20Z"
updated_at: "2026-11-22T21:01:20Z"
---
- Archived full text: [[agent-sandbox-egress-control-outbound-allow-listing-blaxel|Full archived text, with credits]]
- Link: <https://blaxel.ai/blog/sandbox-egress-control-outbound-allow-listing>

## What it says

The article argues that for sandboxes running untrusted or AI-generated agent code, egress control is the blocking control for enterprise security reviews. It lays out the attack path (indirect prompt injection redirects outbound calls and data leaves the perimeter) and then describes three complementary egress patterns: domain-level allow-lists at the network layer, static egress IPs for downstream firewalls, and managed-proxy routes that inject credentials server-side. It shows that the right combination depends on the agent's outbound communication pattern (stable destination sets versus user-specified URLs), audited before any rules are written, and aligned with compliance frameworks like SOC 2, HIPAA, and ISO 27001. It closes with operational tradeoffs: proxy routing adds latency across sequential tool calls, and undefined egress usually stalls deals only at the procurement stage.

## Claims drawn from this source

- **Indirect prompt injection is a short path to exfiltration.** Adversarial content reaches the model, the model interprets it as an instruction, and the generated code makes an outbound call that sends data outside the perimeter; experiments on computer-use agents measured end-to-end exfiltration success rates up to 85%, consistent across multiple programming languages.
- **Default-deny domain filtering is the baseline.** The sandbox can only resolve and route to pre-approved domains; most implementations inspect the SNI field in the TLS handshake, but TLS 1.3 Encrypted Client Hello hides the hostname and creates a blind spot, so domain filtering fits stable destination sets.
- **Static egress IPs establish source identity.** A NAT gateway replaces each sandbox's private IP with a fixed public one; downstream firewalls and third-party APIs can allow-list that IP. Domain filtering controls destinations while static IPs control the source, so they pair together.
- **Credentialed calls belong behind a managed proxy.** A proxy injects API keys and tokens server-side after the request leaves the sandbox, so the executing code never holds the secret; environment variables are a poor fit because OWASP notes they are generally accessible to all processes and may end up in logs, and NIST SP 800-190 recommends secrets outside images at runtime.
- **Audit outbound traffic before writing any rules.** Catalog every external domain and port the agent contacts across realistic workloads, separate agent-initiated API calls from system-level calls like DNS resolutions and package installs, and group connections by destination before defining the allow-list.
- **Egress controls map to compliance frameworks.** SOC 2 asks for network controls and monitoring; HIPAA raises the bar for protected health data; CSA questionnaires document network restrictions; NIST SP 800-53 names SC-7(10) for preventing exfiltration and SI-4(4) for monitoring inbound and outbound traffic.
- **Proxy routing adds latency that compounds across tool chains.** Istio benchmarks measured 3 milliseconds at the median and 20 milliseconds at P90 under higher concurrency; sequential tool calls make the cumulative cost material, so domain filtering is the lower-overhead option for non-credentialed endpoints.
- **Undefined egress stalls deals at procurement.** Enterprise reviews ask what outbound connections the sandbox can make; undefined egress usually surfaces only when the infrastructure reaches the security review stage, and fixing it then is a stalled deal and a scramble to retrofit controls under deadline.
