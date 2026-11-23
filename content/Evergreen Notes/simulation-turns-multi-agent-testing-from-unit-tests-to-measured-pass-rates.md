---
type: "evergreen"
title: "Simulation turns multi-agent testing from unit tests to measured pass-rates"
created_at: "2026-11-22T15:01:18Z"
updated_at: "2026-11-22T15:01:18Z"
inputs: ["notes-on-multi-agent-simulation-how-to-test-complex-agentic-workflows-in-a-sandbox-before-they", "redundant-multi-agent-systems-need-sandboxed-testing-and-guardrails"]
provenance_urls: ["https://agentswarms.fyi/blog/multi-agent-simulation-testing-agentic-workflows-sandbox", "https://en.wikipedia.org/wiki/Multi-agent_system", "https://blog.anthropic.com/building-effective-agents"]
refutation_status: "untested"
answers_questions: ["How do you design a sandboxed evaluation harness for redundant multi-agent systems when emergent drift is what you're testing for?"]
---
Agent synthesis

Unit tests prove a swarm's parts work; simulation is the only honest check of what emerges from the wiring. The mechanism is that a swarm's interesting failures live in handoffs, shared state, non-deterministic planning, and behavior no one designed, so a single happy-path run stays invisible until many seeded runs expose it.

The simulation source defines four parts (scenario, sandbox, end-to-end agents, measurement layer) and five sandbox properties: isolation, determinism, hard resource caps, full tracing, and repeatability at scale. A failing run replays exactly from its seed; an assertion on the whole trace catches deadlocks, double-refunds, and budget blowouts that a golden-answer check waves through. The redundant multi-agent systems note makes the complementary case from the failure side: emergent drift, protocol drift, and observability gaps demand sandboxed testing and guardrails before deployment. The combination is that sandboxed simulation is the concrete harness for those guardrails, and pass-rate over many seeds is the honest success metric.

The signal, per τ-bench's lesson, is consistency across many runs rather than a single pass. Start with the simplest harness that fixes the seed, mocks the tools, caps turns and spend, traces every step, and asserts on the trace. Add seeds, harder inputs, and adversarial cases only as failures accumulate (see: sandboxed testing and guardrails for redundant multi-agent systems).

## Where it comes from

- [[notes-on-multi-agent-simulation-how-to-test-complex-agentic-workflows-in-a-sandbox-before-they|Multi-Agent Simulation: How to Test Complex Agentic Workflows in a Sandbox Before They Touch Production]]

## What this builds on

- [[redundant-multi-agent-systems-need-sandboxed-testing-and-guardrails|Redundant Multi-Agent Systems Need Sandboxed Testing and Guardrails]]
