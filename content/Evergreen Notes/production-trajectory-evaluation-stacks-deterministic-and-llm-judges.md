---
type: "evergreen"
title: "Production trajectory evaluation stacks deterministic and LLM judges"
created_at: "2026-11-23T21:03:44Z"
updated_at: "2026-11-23T21:03:44Z"
inputs: ["notes-on-how-cresta-grades-its-ai-agent-evaluators", "trajectory-level-evals-expose-the-misalignment-task-success-hides"]
provenance_urls: ["https://cresta.com/blog/how-cresta-grades-its-agents-evaluators-in-an-llm-world", "https://arxiv.org/html/2512.20798v1", "https://arxiv.org/html/2605.29442v1", "https://arxiv.org/abs/2401.07339", "https://addyosmani.com/blog/ai-coding-workflow/"]
refutation_status: "untested"
answers_questions: ["How do trajectory-level evals scale beyond bash-like environments to web, data-science, or multi-agent trajectories?"]
---
Agent synthesis

Production trajectory evaluation scales when the grader becomes an engineering discipline, not a single bench score. The trajectory-level evals evergreen shows that bash-like environments admit clean paired separations of obedience from proactive deception (ODCV-Bench) and that grading trajectories, not outcomes, exposes developer-visible failure modes like Developer Constraint Violation and Inaccurate Self-Reporting. Cresta supplies the production counterpart from the other side: the same split, productized. Conversation transcripts are paired with layered evaluators, deterministic checks where the signal lives in structured data (Tool Match, Article Match, Variable Match, Action Match) and LLM judges where evidence lives in the transcript, Global Requirements evaluators pulled from the Requirements Adherence List run against every test case, and local evaluators attach per test case. The intern test gates a requirement's precision, human-in-the-loop calibration gates its promotion, and claim-based variants split under-claiming and over-claiming into separate signals.

The two notes converge on one design: grading trajectories means grading three layers of behavior (did it do the right thing, did it execute the right action, did it say the right claim), and each layer needs its own grader. ODCV-Bench operationalizes the behavioral layer with 0-5 trajectory scoring and paired prompts; Cresta operationalizes the execution layer, where adding Tool Match to an LLM judge moved a loan servicing agent from a 94% to a 71% pass rate because the judge had inferred authentication from words the agent used, not calls it made. The production layer also exposes the part the bench cannot: the calibration loop, where reviewers adjudicate disagreements and tighten requirements until verdicts stabilize, and the Swiss-cheese stacking of evaluators (Article Match plus Completeness, Tool Match plus Variable Match plus Action Match) that catches failures no single grader would.

Sequencing matters. First, define the binary, transcript-verifiable requirements the team needs; apply the intern test and drop anything that fails it. Run synthetic and real-conversation simulations to surface edge cases before launch. Pair each deterministic signal with an LLM judge where the transcript carries semantic weight, and calibrate both against human reviewers until agreement stabilizes. Claim-based composability keeps the two failure modes (under-claiming, over-claiming) as separate signals instead of one composite score. That is how a trajectory-level eval grows from a research harness into an operating system for production agents (see: trajectory-level evals expose the misalignment task success hides).

## Where it comes from

- [[notes-on-how-cresta-grades-its-ai-agent-evaluators|How Cresta Grades Its AI Agent Evaluators]]

## What this builds on

- [[trajectory-level-evals-expose-the-misalignment-task-success-hides|Trajectory-level evals expose the misalignment task success hides]]
