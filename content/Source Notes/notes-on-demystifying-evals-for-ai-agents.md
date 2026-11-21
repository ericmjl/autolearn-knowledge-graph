---
type: "source-note"
title: "Notes on: Demystifying evals for AI agents"
raw: "demystifying-evals-for-ai-agents"
url: "https://www.anthropic.com/research/demystifying-evals-for-ai-agents"
created_at: "2026-11-21T13:02:07Z"
updated_at: "2026-11-21T13:02:07Z"
---
- Archived full text: [[demystifying-evals-for-ai-agents|Full archived text, with credits]]
- Link: <https://www.anthropic.com/research/demystifying-evals-for-ai-agents>

## What it says

Anthropic details how to design, build, and maintain evaluations for AI agents, from what an eval is (tasks, trials, graders, transcripts, outcomes, harnesses, suites) to how capability and regression evals split a quality bar. It argues that agent evals fail when teams skip transcripts, saturate tasks, or ignore harness noise; the same eval discipline that defines success early also accelerates model upgrades, baselines, and cross-team communication.

## Claims drawn from this source

- **Agent evals evaluate the harness and the model together, not the model in isolation.** An agent harness processes inputs, orchestrates tool calls, and returns results; when we evaluate an agent, we evaluate the harness and the model working together, e.g. Claude Code as a flexible agent harness.
- **Capability evals start at a low pass rate, regression evals demand nearly 100%, and high-pass capability evals graduate into regression suites.** Capability evals ask what the agent can do well and target tasks it struggles with; regression evals ask whether it still handles tasks it used to; after an agent is launched and optimized, capability evals with high pass rates can graduate into a regression suite run continuously to catch drift.
- **Start with 20-50 simple tasks drawn from real failures, not hundreds of tasks up front.** Teams delay building evals because they think they need hundreds of tasks, but 20-50 simple tasks from real failures are a great start, because early changes have a large effect size that small samples suffice to detect.
- **Unambiguous tasks and reference solutions are required to make metrics honest.** A good task is one where two domain experts independently reach the same pass/fail verdict; a 0% pass rate across trials is most often a signal of a broken task, not an incapable agent, and a reference solution proves the task is solvable and the graders correctly configured.
- **Graders should reward outcomes, not paths, and combine deterministic, model-based, and human graders.** Checking agents followed a specific sequence of tool calls is too rigid and results in brittle tests; it is often better to grade what the agent produced, not the path it took, using deterministic graders where possible, LLM graders where necessary, and human graders judiciously.
- **Eval saturation makes scores deceptive and hides real progress.** An eval at 100% tracks regressions but provides no signal for improvement; SWE-Bench Verified went from 30% to >80%, and Qodo, initially unimpressed by Opus 4.5's one-shot coding evals, built a new agentic eval framework to better capture gains on longer, more complex tasks.
- **Evals should be paired with production monitoring, A/B testing, transcript review, and systematic human studies rather than used in isolation.** No single evaluation layer catches every issue, like the Swiss Cheese Model; automated evals run at scale pre-launch and in CI/CD, production monitoring catches distribution drift post-launch, and manual transcript review builds intuition for failure modes.
