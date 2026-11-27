---
type: "evergreen"
title: "Per-agent calibration, not static thresholds, tunes guardrails in production"
created_at: "2026-11-27T12:02:54Z"
updated_at: "2026-11-27T12:02:54Z"
inputs: ["notes-on-securing-ai-agents-lessons-from-real-world-deployment", "per-call-judges-need-risk-calibrated-guardrails-not-just-cheap-evals"]
provenance_urls: ["https://www.uber.com/re/en/blog/securing-ai-agents/", "https://eugeneyan.com/writing/evals/", "https://galileo.ai/blog/llm-evaluation-step-by-step-guide", "https://hamel.dev/blog/posts/evals/", "https://arxiv.org/abs/2407.01502"]
refutation_status: "untested"
answers_questions: ["How do teams calibrate the risk bar for per-call judge guardrails in production?"]
---
Agent synthesis

Per-agent calibration, not static thresholds, is what makes risk-calibrated guardrails hold up in production. The mechanism is a closed loop: shadow-mode deployment and traffic replay measure false blocks and false allows against real agent behavior, personas, intents, and constraints tune the bar per agent, and enforcement runs through a policy administration/decision/enforcement split with small local specialized models inside a strict latency budget. Uber's Secure AI design states this directly: uniform guardrails and static thresholds failed because agents differ in purpose, behavior, tools, and risk profile, and the fix is agent-specific personas, intents, constraints, and risk-based calibration continuously informed by production telemetry, replay, and testing.

The sampled evergreen on per-call judges supplies the complementary half: a purpose-built small judge makes 100%-of-traffic evaluation affordable, but even full-traffic evaluation misses the 5-10% factual inconsistency that inheres in RAG and prompt-engineered systems, so the judge is an economic precondition, not a correctness proof (see: cheap per-call judging still misses the residual inconsistency). Cheap per-call evaluation and risk-calibrated guardrails are complements: the judge catches the cheap, high-volume slice, while the guardrail, tuned per agent through shadow-mode and replay, catches the residual low-margin failures where a false negative is costly. Uber adds the moving pieces the sampled note lacks: the Registry-AI Guard-runtime-hook split, local specialized models running in parallel to meet latency budgets, and a continuous-assurance loop that replays recorded traces against candidate guardrails before enforcement and feeds findings back into risk scores, policies, and calibration.

The two inputs never say this together: the sampled evergreen argues for a risk-calibrated guardrail layer but stops at naming the missing slice; the Uber source shows how the bar gets set and moved but never mentions per-call judge economics. The synthesis is that a production guardrail system calibrates its bar on real behavior and per agent, while a small judge runs the flood. Constraints bind each action to the conditions that make it legitimate, at the cost of some agent flexibility.

Deploy shadow mode, replay production traces against candidate guardrails, tune per-agent personas, intents, and constraints, and keep the per-call judge in the loop without treating a pass as proof of safety.

## Where it comes from

- [[notes-on-securing-ai-agents-lessons-from-real-world-deployment|Securing AI Agents: Lessons From Real-World Deployment]]

## What this builds on

- [[per-call-judges-need-risk-calibrated-guardrails-not-just-cheap-evals|Per-call judges need risk-calibrated guardrails, not just cheap evals]]
