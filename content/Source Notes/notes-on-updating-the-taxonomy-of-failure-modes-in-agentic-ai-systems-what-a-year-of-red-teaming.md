---
type: "source-note"
title: "Notes on: Updating the taxonomy of failure modes in agentic AI systems: What a year of red teaming taught us | Microsoft Security Blog"
raw: "updating-the-taxonomy-of-failure-modes-in-agentic-ai-systems-what-a-year-of-red-teaming"
url: "https://www.microsoft.com/en-us/security/blog/2026/06/04/updating-taxonomy-failure-modes-agentic-ai-systems-year-red-teaming-taught-us/"
created_at: "2026-11-28T06:01:20Z"
updated_at: "2026-11-28T06:01:20Z"
---
- Archived full text: [[updating-the-taxonomy-of-failure-modes-in-agentic-ai-systems-what-a-year-of-red-teaming|Full archived text, with credits]]
- Link: <https://www.microsoft.com/en-us/security/blog/2026/06/04/updating-taxonomy-failure-modes-agentic-ai-systems-year-red-teaming-taught-us/>

## What it says

Microsoft AI Red Team updated its agentic AI failure taxonomy from v1.0 (April 2025, forward-looking) to v2.0 after 12 months of red team engagements against deployed agentic systems. The update adds seven new failure-mode categories (agentic supply chain compromise, goal hijacking, inter-agent trust escalation, CUA visual attack, session context contamination, MCP/plugin abuse, capability/architecture disclosure), refines the operational findings (HitL bypass as the most exploited mode, XPIA plus memory poisoning as the reliable initial-access vector, session contamination and incremental escalation as hard to detect, capability disclosure as an enabler), and expands mitigations to supply-chain SBOM, cryptographic inter-agent identity, consent architecture hardening, and adversarial session hardening. The taxonomy is explicitly a living document that should be refreshed as the evidence base and the agent capabilities themselves evolve.

## Claims drawn from this source

- **Taxonomies need operational grounding, not forward-looking extrapolation.** The v1.0 taxonomy was built from practitioner interviews and early experience; v2.0 is grounded in 12 months of engagements that confirmed some predictions, falsified others, and surfaced unanticipated modes.
- **Seven new failure modes surfaced in v2.0.** Agentic supply chain compromise, goal hijacking, inter-agent trust escalation, CUA visual attack, session context contamination, MCP/plugin abuse, and capability/architecture disclosure.
- **HitL bypass is the most consistently exploited mode.** Red teamers achieved bypass through consent fatigue, probabilistic invocation manipulation, and incremental escalation chains, with several zero-click end-to-end chains from an external input.
- **XPIA and memory poisoning combine at high frequency.** Cross-domain prompt injection delivered via external content is the most reliable initial access vector, and one successful injection seeds persistent memory propagated across sessions.
- **Session context contamination is hard to detect.** Neither the contaminating input nor any individual escalation step is anomalous in isolation; detection requires behavioral analysis across the full session.
- **Capability disclosure is a key enabler of follow-on attacks.** Extracting tool names, schemas, and guardrail inconsistencies often needs only a direct request and consistently opens attack paths that would otherwise require external reconnaissance.
- **The taxonomy is a living threat-modeling tool.** As agentic systems gain new capabilities (persistent memory at scale, autonomous spawning, physical environment interaction), the failure mode surface expands; each category should be checked against the deployed system under what conditions it could occur and whether a control detects or prevents it.
