---
type: "evergreen"
title: "A failure-mode taxonomy is a living threat-modeling tool, not a static checklist"
created_at: "2026-11-28T06:01:51Z"
updated_at: "2026-11-28T06:01:51Z"
inputs: ["notes-on-updating-the-taxonomy-of-failure-modes-in-agentic-ai-systems-what-a-year-of-red-teaming", "grounding-improves-when-hallucination-is-scored-per-failure-mode"]
provenance_urls: ["https://www.microsoft.com/en-us/security/blog/2026/06/04/updating-taxonomy-failure-modes-agentic-ai-systems-year-red-teaming-taught-us/", "https://www.splunk.com/en_us/blog/artificial-intelligence/rag-failure-modes.html", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["How should a failure-mode eval taxonomy be refreshed as models and workloads drift?"]
---
Agent synthesis

A failure-mode taxonomy survives drift only when it is refreshed against live operational evidence, not frozen at design time. Microsoft's v1.0 taxonomy for agentic AI was forward-looking: built from practitioner interviews and early experience in April 2025, with agent compromise, injection, impersonation, and flow manipulation alongside amplified memory poisoning and cross-domain injection. Twelve months of red team engagements against deployed systems confirmed, falsified, and surfaced patterns v1.0 never anticipated, so v2.0 added seven modes and the mitigations that go with them.

The mechanism is directional, not static. Two structural drivers push the taxonomy forward: the capability surface expands, with open-source frameworks like OpenClaw pulling 336,000 GitHub stars and thousands of agents in 48 hours, and MCP ecosystems plus computer-use agents adding attack surfaces with no pre-agent precedent. Operational evidence compounds. Microsoft's v2.0 additions carry concrete operational stakes: HitL bypass at very high frequency including zero-click end-to-end chains, cross-domain injection plus memory poisoning as the most reliable initial access vector, session context contamination as undetectable step by step, and capability disclosure as a key enabler of follow-on attacks.

The grounding-per-failure-mode discipline and the red-team taxonomy are two views of the same surface. The eval note treats failure modes as an instrumented taxonomy, with per-mode evaluators and a regression set that swaps production failures in as they appear. The red-team note treats failure modes as an adversarial taxonomy, with security and safety pillars and novel categories from live engagements. Both refuse to freeze the list: one keeps a living regression set, the other keeps the taxonomy updated as the evidence base and the agent surface develop. A frozen taxonomy, like a frozen baseline, reports clean on yesterday's failures. A living taxonomy names what can occur in your system, under what conditions, and whether a control would detect or prevent it.

Take every category and ask whether it can occur in your system, under what conditions, and whether a control would detect or prevent it; refresh the taxonomy and your coverage matrix whenever a new capability class, an incident, or a new deployment pattern appears. Never treat the taxonomy as a compliance checklist (see: grounding fails unless hallucination is scored per failure mode).

## Where it comes from

- [[notes-on-updating-the-taxonomy-of-failure-modes-in-agentic-ai-systems-what-a-year-of-red-teaming|Updating the taxonomy of failure modes in agentic AI systems: What a year of red teaming taught us | Microsoft Security Blog]]

## What this builds on

- [[grounding-improves-when-hallucination-is-scored-per-failure-mode|Grounding improves when hallucination is scored per failure mode]]
