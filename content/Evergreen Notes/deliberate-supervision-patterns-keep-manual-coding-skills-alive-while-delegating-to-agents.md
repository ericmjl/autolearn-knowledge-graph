---
type: "evergreen"
title: "Deliberate supervision patterns keep manual coding skills alive while delegating to agents"
created_at: "2026-11-23T04:01:53Z"
updated_at: "2026-11-23T20:03:06Z"
inputs: ["notes-on-the-80-problem-in-agentic-coding", "agentic-coding-expands-what-s-buildable-but-atrophies-skills", "notes-on-skill-atrophy-when-ai-reliance-erodes-developer-capability-agentpatterns-ai"]
provenance_urls: ["https://addyo.substack.com/p/the-80-problem-in-agentic-coding", "https://larsfaye.com/articles/agentic-coding-is-a-trap", "https://x.com/karpathy/status/2015883857489522876", "https://agentpatterns.ai/human/skill-atrophy/"]
refutation_status: "untested"
answers_questions: ["What supervision patterns preserve manual coding skills while delegating to agents?", "What interventions actually preserve human debugging and coding skills when implementation work is delegated to coding agents?"]
---
Agent synthesis

Deliberate supervision patterns keep manual coding skill alive while delegating to agents. The sampled evergreen on agentic coding argues that overuse erodes manual skill and supervision quality, treating the loss as structural; the new source adds the mechanism and the mitigations. Delegation is cognitive offloading: handing a task to an agent bypasses the effortful practice that builds durable skill, the same pattern documented for calculators and GPS navigation, and AI output is non-deterministic, so code can compile, pass tests, and still break requirements in ways a reviewer without independent reasoning cannot see. The perception gap compounds it: developers cannot self-diagnose the loss. The new source supplies four interventions: dual-mode competency (code without AI periodically, like pilots flying manual approaches), explain-then-code (ask the agent to explain the approach before requesting implementation), deliberate practice blocks in delegated domains, and review-as-skill-exercise (predict what the output does and verify edge cases before accepting it). It also supplies the evidence: full delegation produced roughly a 17 percentage-point comprehension deficit with junior developers, and the interaction pattern mattered more than the use itself, with developers who asked why the approach worked before writing the code themselves outperforming code-dispensers who accepted output and moved on. Read against the existing supervision evidence, the two converge: writing tests or criteria first, pairing, requesting explanations, and alternating manual implementation all re-engage the cognitive loop the task removes, and the perception gap means supervision cannot rest on self-trust. The synthesis adds the rule: interventions are not extras layered onto delegation, they are the supervision strategy itself, sustained over time rather than one-time fixes. (see: agentic coding expands what's buildable but atrophies skills) Adopt dual-mode practice, explain-then-code, deliberate practice blocks, and review-as-exercise for the domains you have been delegating, and block on comprehension, not on speed, when you review.

## Where it comes from

- [[notes-on-the-80-problem-in-agentic-coding|The 80% Problem in Agentic Coding]]
- [[notes-on-skill-atrophy-when-ai-reliance-erodes-developer-capability-agentpatterns-ai|Skill Atrophy: When AI Reliance Erodes Developer Capability — AgentPatterns.ai]]

## What this builds on

- [[agentic-coding-expands-what-s-buildable-but-atrophies-skills|Agentic coding expands what's buildable but atrophies skills]]
