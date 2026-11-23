---
type: "source-note"
title: "Notes on: How Cresta Grades Its AI Agent Evaluators"
raw: "how-cresta-grades-its-ai-agent-evaluators"
url: "https://cresta.com/blog/how-cresta-grades-its-agents-evaluators-in-an-llm-world"
created_at: "2026-11-23T21:02:59Z"
updated_at: "2026-11-23T21:02:59Z"
---
- Archived full text: [[how-cresta-grades-its-ai-agent-evaluators|Full archived text, with credits]]
- Link: <https://cresta.com/blog/how-cresta-grades-its-agents-evaluators-in-an-llm-world>

## What it says

Cresta describes how its forward-deployed team evaluates customer-experience agents at scale. Trial runs against synthetic and replay-recreated conversations fill the gaps happy-path tests miss; the test case pairs a conversation transcript with a set of evaluators. Global evaluators come from a Requirements Adherence List written as binary, observable, transcript-verifiable checks, and local evaluators target structured data (tool, article, variable, action) with deterministic checks while LLM judges handle semantic judgments of transcript content. Judge calibration runs human-in-the-loop review, with disagreements driving requirement tightening before evaluators are promoted; claim-based variants (completeness, accuracy, accuracy and completeness) split under-claiming from over-claiming, and layering deterministic plus LLM evaluators works like Swiss cheese.

## Claims drawn from this source

- **Trajectory evaluation judges the path, final outcome evaluation judges the result.** Cresta splits its grading into trajectory evaluation (reasoning steps, tool calls, procedures followed, decisions along the way) and final outcome evaluation (only what the end result produced, regardless of path).
- **Global evaluators come from a Requirements Adherence List.** Business objectives, brand standards, and compliance obligations are converted into LLM evaluators that run against every test case in the set; requirements are written to be binary, observable, and verifiable from the transcript alone, since a vague requirement produces inconsistent verdicts while a precise one does not.
- **Requirements must pass the intern test.** Every requirement is held to whether someone with no context, reading only the transcript, could reach the same verdict as the team would.
- **Human-in-the-loop calibration gates evaluator promotion.** After new evaluators are configured, reviewers run them against a set of transcripts and either agree or disagree with the LLM's judgment case by case; disagreements expose requirements that need tightening, and the loop continues until verdicts stabilize and match the team's own judgment before evaluators are promoted to the full test suite.
- **Structured-data signals use deterministic checks, not LLM judges.** Cresta's deterministic evaluators cover Tool Match (specific tool invoked with expected parameters), Article Match (correct knowledge base article retrieved), Variable Match (structured fields captured correctly), and Action Match (platform-level actions like transfers, hang-ups, escalations actually fired).
- **LLM judges infer behavior the agents never executed.** A loan servicing agent passed an LLM requirement evaluator at a 94% rate across test cases; adding a Tool Match evaluator that checked the authentication tool was actually called dropped the combined pass rate to 71%, because the LLM judge had been inferring authentication from conversational context.
- **Claim-based evaluators split under-claiming from over-claiming.** Completeness fails the agent for missing any required claim (extra information passes); Accuracy fails it for including any out-of-scope claim (missing some is acceptable); Accuracy and Completeness requires all and only the approved claims, decomposing what one semantic-equivalence score would hide.
- **Effective test cases layer evaluators like Swiss cheese.** A FAQ answer test pairs an Article Match evaluator with a Completeness LLM evaluator to check retrieval and generation accuracy; an intent routing test layers Tool Match, Variable Match, and Action Match across three failure modes, while global requirements run against the whole set without per-case reconfiguration.
