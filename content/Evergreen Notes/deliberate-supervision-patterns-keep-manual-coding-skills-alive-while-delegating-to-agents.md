---
type: "evergreen"
title: "Deliberate supervision patterns keep manual coding skills alive while delegating to agents"
created_at: "2026-11-23T04:01:53Z"
updated_at: "2026-11-23T04:01:53Z"
inputs: ["notes-on-the-80-problem-in-agentic-coding", "agentic-coding-expands-what-s-buildable-but-atrophies-skills"]
provenance_urls: ["https://addyo.substack.com/p/the-80-problem-in-agentic-coding", "https://larsfaye.com/articles/agentic-coding-is-a-trap", "https://x.com/karpathy/status/2015883857489522876"]
refutation_status: "untested"
answers_questions: ["What supervision patterns preserve manual coding skills while delegating to agents?"]
---
Agent synthesis

Deliberate supervision patterns keep manual coding skill alive while delegating to agents. The sampled evergreen on agentic coding argues that overuse erodes manual skills and supervision quality, treating the loss as structural; the new source adds what actually blunts it: the same practices that restore the skill also protect comprehension, starting with writing tests or test cases before the agent implements, pairing with a senior to learn the decision-making, asking the AI to justify its approach, and alternating some manual implementation. The mechanism is that each pattern re-engages the same cognitive loop the task removes. TDD makes you write the success criteria before the agent generates; pairing reconstructs the taste of the choice; explanations force the agent to surface its premises; manual alternation preserves muscle memory. The productivity evidence reinforces the split: high-adoption teams merged 98% more PRs while review times ballooned 91% and PR size grew 154%, so the bottleneck moved to review and comprehension, and only 48% of developers consistently check AI-assisted code.
The evidence from the existing evergreen and the source agree on where the failure concentrates. One input cites an Anthropic study with a 47% drop-off in debugging skills among heavy users, the source notes juniors reporting less confidence in problem-solving, and both flag that generation and discrimination are different capabilities. Both flag that agents are not self-sufficient and need close supervision. The synthesis adds the practical rule: review AI code like a mentor's output, to learn, not just to ship, and treat every explanation gap as a signal to dig deeper. A supervision system that never asks the agent to justify its approach is rubber-stamping in disguise.
The 80/20 threshold still favors greenfield work, personal projects, and MVPs, where comprehension debt stays manageable; mature codebases with complex invariants invert the calculus. Architecture follows: declarative specs and success criteria up front, fresh-context review, automated verification as guardrails, and bounded autonomy. The signal of an effective system is that the human keeps the macro and the agent handles the micro: 70% of effort on problem definition, 30% on execution.
Adopt the counter-patterns from the 80% source rather than relying on raw agent output, and block on comprehension, not on speed, when you review. (see: agentic coding expands what's buildable but atrophies skills)

## Where it comes from

- [[notes-on-the-80-problem-in-agentic-coding|The 80% Problem in Agentic Coding]]

## What this builds on

- [[agentic-coding-expands-what-s-buildable-but-atrophies-skills|Agentic coding expands what's buildable but atrophies skills]]
