---
type: "evergreen"
title: "Runtime policy enforcement moves prompt-injection defenses out of the prompt"
created_at: "2026-11-26T11:01:56Z"
updated_at: "2026-11-26T11:01:56Z"
inputs: ["notes-on-building-harvey-s-mcp-policy-engine", "prompt-injection-defeats-prompt-defenses-separate-data-content-and-communication"]
provenance_urls: ["https://www.harvey.ai/blog/building-harveys-mcp-policy-engine", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["How do permission and verification controls hold up under adversarial MCP composition, and what do they cost?"]
---
Agent synthesis

Runtime policy enforcement moves prompt-injection defenses out of the prompt and into the orchestration layer, where they can be pinned, tested, and enforced. The Harvey MCP Policy Engine shows the mechanism: tools are pinned against an approved baseline, arguments are assessed by capacity and authority rather than by read/write labels, and every proposed call is checked against structured annotations and call history in a Rego policy before it runs, with fail-closed denial when checks cannot complete. Filtering happens in one place, and prompt content and customer data never enter the decision path, which is what makes the policy layer testable and keeps enforcement from depending on a model that can be bypassed.

The prompt-injection evergreen supplies the principle: all content is glued into tokens, so no prompt instruction reliably separates trusted from untrusted content. The Harvey evidence turns that principle into a runtime control. The pinner addresses rug-pull (changes after approval), the sanitizer strips hidden characters and lookalike combinations, and the trajectory evaluator applies the trifecta as a sequential-risk rule rather than as a static configuration. Together the two show something neither says alone: separating data, content, and communication is only a design intent unless the orchestration layer checks each call at the moment it is proposed.

The cost side matters. Pinning on first use would guard against rug-pull but reject legitimate catalog churn, so Harvey pins and alerts, leaving human prioritization to decide what to trust. The self-verification evergreen makes the same point in a different domain: fresh context, cheap verifiers, and streak-based checks all trade throughput for confidence, and both land verification at a boundary that needs its own approval loop. Start with the most consequential capability and pin it, then add trajectory-aware policies for the calls that cross the trifecta boundary, and treat the pinner's alerts as a prioritization queue rather than a gate to ignore.

## Where it comes from

- [[notes-on-building-harvey-s-mcp-policy-engine|Building Harvey’s MCP Policy Engine]]

## What this builds on

- [[prompt-injection-defeats-prompt-defenses-separate-data-content-and-communication|Prompt injection defeats prompt defenses; separate data, content, and communication]]
