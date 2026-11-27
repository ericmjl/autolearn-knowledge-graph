---
type: "source-note"
title: "Notes on: Securing AI Agents: Lessons From Real-World Deployment"
raw: "securing-ai-agents-lessons-from-real-world-deployment"
url: "https://www.uber.com/re/en/blog/securing-ai-agents/"
created_at: "2026-11-27T12:01:36Z"
updated_at: "2026-11-27T12:01:36Z"
---
- Archived full text: [[securing-ai-agents-lessons-from-real-world-deployment|Full archived text, with credits]]
- Link: <https://www.uber.com/re/en/blog/securing-ai-agents/>

## What it says

Uber describes a defense-in-depth framework for securing AI agents across the lifecycle: provisioning-time validation, runtime enforcement, and continuous assurance. Traditional authorization answers who may act; the framework answers whether a proposed action is consistent with what the user requested, the agent's defined persona and intents, its role, and the full session context. Uniform guardrails and static thresholds failed because agents differ in purpose, behavior, tools, and risk profile, so enforcement is calibrated per agent, continuously, from shadow-mode deployments, traffic replay, and production telemetry.

## Claims drawn from this source

- **Agentic AI shifts the attack surface into the semantic layer.** Traditional authorization can determine who is allowed to act, but agents dynamically reason over content from users, webpages, documents, tools, and other agents and can translate reasoning into real-world actions, creating risks such as prompt injection, tool and memory poisoning, goal hijacking, behavioral drift, and hallucination-driven actions.
- **Uniform guardrails and static thresholds fail per-agent risk profiles.** Uniform guardrails and static thresholds couldn't account for the different purposes, behaviors, tools, and risk profiles of individual agents. The fix is agent-specific personas, intents, constraints, and risk-based calibration, continuously informed by production telemetry, replay, and testing.
- **Shadow mode plus replay calibrates the bar before enforcement.** Persona and intent enforcement balances overly restrictive policies that disrupt legitimate activity against overly broad ones that weaken protection, achieved through shadow-mode deployment, traffic replay, and per-agent calibration so teams can measure false blocks and false allows against real behavior and validate changes before enforcement.
- **Latency budgets push guardrails to small local specialized models.** Guardrail decisions occur in the agent's execution path, so runtime controls must operate within a strict latency budget. Uber uses small specialized models hosted locally, fine-tuned for specific guardrail functions, executed in parallel with in-memory vector search, rather than large general-purpose LLMs, reducing latency and inference cost.
- **Policy administration/decision/enforcement separation extends into semantic behavior.** The AI Registry acts as the policy administration point, AI Guard as the policy decision point, and Agent Guard runtime hooks with LangFx or the AI Guard SDK as policy enforcement points, invoking AI Guard at critical checkpoints and applying verdicts before an interaction or action proceeds.
- **Continuous assurance replays production traces against candidate guardrails.** Recorded interactions can be replayed against candidate guardrails and updated policies as new attacks emerge, allowing teams to evaluate security changes against real production behavior before enforcement; automated threat modeling feeds scenario-based penetration testing and continuous red teaming back into agent risk scores, policies, model calibration, and guardrails.
- **Explicit intents and constraints are the least glamorous but most effective control.** The most effective mitigation Uber found was restricting agents to explicit intents and constraints that tightly govern what may happen and under what conditions; it substantially reduced the ability to act on manipulated instructions, at the cost of some flexibility that autonomous designs gain.
