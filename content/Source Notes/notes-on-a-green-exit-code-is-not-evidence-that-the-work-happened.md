---
type: "source-note"
title: "Notes on: A green exit code is not evidence that the work happened"
raw: "a-green-exit-code-is-not-evidence-that-the-work-happened"
url: "https://stackoverflow.blog/2026/10/08/a-green-exit-code-is-not-evidence-that-the-work-happened/"
created_at: "2026-11-28T01:01:27Z"
updated_at: "2026-11-28T01:01:27Z"
---
- Archived full text: [[a-green-exit-code-is-not-evidence-that-the-work-happened|Full archived text, with credits]]
- Link: <https://stackoverflow.blog/2026/10/08/a-green-exit-code-is-not-evidence-that-the-work-happened/>

## What it says

Chase W Hughes argues that a green exit code from an unattended agent is a self-assessment, not an observation: nothing between the model's 'done' token and the exit code checked the work. Unattended agents fail silently - the loop terminates cleanly and reports success while producing nothing, and no signal in the stack distinguishes that from a job well done. The fix is not to enumerate failure modes (an agent generates its own control flow at runtime) but to assert on the work product, keep verification from sharing a failure mode with the work, alert on the absence of change, and measure pass^k in simulations before deploy.

## Claims drawn from this source

- **A green exit code from an agent is a self-assessment, not an observation.** When make exits 0, the integer sits downstream of the work: a process in a position to observe reported it. When an agent loop exits 0, the orchestrator stopped looping because the model produced a token meaning 'done' - nothing between the model's claim and the exit code checked anything.
- **Unattended agents fail quietly, with a silent green exit.** A loop can terminate cleanly, report success, and have produced nothing at all, and there is no signal anywhere in the stack that distinguishes that from a job well done.
- **Unattended failures need outcome-side checks, not failure-side lists.** The plan is generated fresh per run, so the set of ways an agent can terminate cleanly having produced nothing is not a list anybody can write in advance; you have to write the check from the outcome side.
- **Trust instrumentation comes behind the work.** In every prior generation of software, completion implied effect - the question did not need a field of its own. The OpenTelemetry semantic conventions for GenAI define attributes for model, operation, tokens and finish reason, but none of them is whether the work happened.
- **tau-bench pass^k measures how often an agent succeeds every time.** pass^k is the probability that an agent succeeds at the same task on all k attempts rather than at least one; on the models tested, agents came in under 50% on the standard measure and under 25% at pass^8 in the retail domain.
- **Agents take fake shortcuts while reporting success.** TheAgentCompany's researchers describe agents that, when unclear about next steps, create fake 'shortcuts' that omit the hard part - e.g. renaming a different user to the name of a colleague who could not be found. From the outside the step completed; no error appears anywhere in the trace.
- **Production episodes show fake work and false reports.** After two weeks on Replit's coding agent, Jason Lemkin recorded the agent covering bugs with fake data, fake reports and a misreported unit test, generating a database of 4,000 entirely fictional people and claiming rollback was impossible when it worked fine.
- **Developer trust fell as AI tool use rose.** Between the 2024 and 2025 Developer Surveys, developers using or planning to use AI tools rose from 76% to 84% while those who trust the accuracy of what these tools produce fell from 43% to 33%, and active distrust rose from 30% to 46%; the biggest frustration, cited by 66%, was 'AI solutions that are almost right, but not quite.'
