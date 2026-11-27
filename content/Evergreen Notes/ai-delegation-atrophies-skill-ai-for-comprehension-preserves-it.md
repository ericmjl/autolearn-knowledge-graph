---
type: "evergreen"
title: "AI delegation atrophies skill; AI-for-comprehension preserves it"
created_at: "2026-11-27T14:02:39Z"
updated_at: "2026-11-27T14:02:39Z"
inputs: ["notes-on-how-ai-assistance-impacts-the-formation-of-coding-skills", "agentic-coding-expands-what-s-buildable-but-atrophies-skills"]
provenance_urls: ["https://www.anthropic.com/research/AI-assistance-coding-skills", "https://larsfaye.com/articles/agentic-coding-is-a-trap", "https://x.com/karpathy/status/2015883857489522876"]
refutation_status: "untested"
answers_questions: ["What does the evidence say about skill atrophy and supervision quality when overuse of agentic coding replaces direct code work?"]
---
Agent synthesis

AI assistance accelerates familiar work but stunts skill formation unless engineers use the tool for comprehension rather than delegation. In the Anthropic RCT, 52 junior Python developers learning a new Trio library scored 17% lower on a quiz just minutes after the task when AI was available (50% vs 67%, Cohen's d=0.738), with no significant time gain, because composing up to 15 AI queries (up to 11 minutes, 30% of the time budget) ate the productivity edge. The mechanism is cognitive offloading: delegating code generation to the assistant removes the error-encounter loop that builds debugging skill, and the largest score gap was on debugging questions, exactly the skill needed to supervise AI-written code.

The interaction typology separates two uses of the same tool. Low-scoring modes (AI delegation n=4, progressive AI reliance n=4, iterative AI debugging n=4) averaged under 40% and meant minimal independent thinking; high-scoring modes (generation-then-comprehension n=2, hybrid code-explanation n=3, conceptual inquiry n=7) averaged 65% or higher. Generation-then-comprehension looked nearly identical to delegation on the surface, yet asking follow-up questions to check understanding flipped the learning outcome. Conceptual inquiry was the second-fastest pattern overall, second only to pure delegation.

This sharpens the skill-atrophy lesson from the agentic-coding note: Karpathy's 80%-to-agent-coding shift and the 47% drop-off in debugging skills are symptoms, not the mechanism. The Anthropic study shows the binding variable is how the developer uses AI, not whether they use it at all. The 80%-productivity and skill-atrophy findings are consistent once you separate familiar tasks from new ones: AI speeds up the former (observational) and hinders the latter (RCT), so the same tool is a shortcut when the skill is new. Supervision quality survives only when engineers stay in error-encounter loops and demand explanation, not when they treat the assistant as a code writer.

Deploy AI with an intentional-learning stance: let it handle repetitive calls, reserve new-skill work for error-encounter with verification questions, and audit reviewers for conceptual inquiry rather than delegation, so the people who supervise agents actually retain the skills to catch their errors.

## Where it comes from

- [[notes-on-how-ai-assistance-impacts-the-formation-of-coding-skills|How AI assistance impacts the formation of coding skills]]

## What this builds on

- [[agentic-coding-expands-what-s-buildable-but-atrophies-skills|Agentic coding expands what's buildable but atrophies skills]]
