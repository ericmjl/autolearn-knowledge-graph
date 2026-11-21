---
type: "source-note"
title: "Notes on: How We Used Agentic AI to Automate Fixes for Flaky Tests"
raw: "how-we-used-agentic-ai-to-automate-fixes-for-flaky-tests"
url: "https://konghq.com/blog/engineering/how-we-used-agentic-ai-to-fix-kong-gateways-flakiest-tests"
created_at: "2026-11-21T16:02:28Z"
updated_at: "2026-11-21T16:02:28Z"
---
- Archived full text: [[how-we-used-agentic-ai-to-automate-fixes-for-flaky-tests|Full archived text, with credits]]
- Link: <https://konghq.com/blog/engineering/how-we-used-agentic-ai-to-fix-kong-gateways-flakiest-tests>

## What it says

Kong's engineering team used Claude Code to fix flaky tests in Kong Gateway, a suite of more than 17,000 test cases x 2 architectures (x86 and ARM) that takes ~23.5 hours on one machine. The core insight is that flaky tests are expensive for humans to fix for two reasons: the root cause is rarely obvious, and intermittent failures demand extensive validation babysitting. Agents fit the job because they can scan far more code and logs than a human and can babysit hours of verification without intervention. The team built an identify-fix-verify loop: an Opus orchestrator (fix-flakes) downloads CI logs for a seed test, an Opus flake-fixer subagent investigates and pushes a fix, and a smaller Haiku flake-verifier subagent polls reruns and filters noise from other flaky tests in the suite. Runs repeat until the full rerun streak passes or a max attempt count is reached, then a human reviews the PR. Over a week and a half the harness fixed 12 of 15 flakiest tests in 4-5 hours each (100-200k tokens), surfaced two genuine bugs (a conf_loader sorting bug and a concurrent auth race condition), and never touched the test files. The lessons: build the feedback loop and data sources, keep context small between spawns, use expensive models for analysis and cheaper ones for verification, and do not over-engineer the harness.

## Claims drawn from this source

- **Flaky tests are hard for humans to fix.** Finding a flaky test's root cause takes deep understanding of the feature and its implementation, and even the original author usually cannot spot the real cause; proper fixes also require extensive validation because a single run proves nothing. It often takes an experienced engineer a full day to fix two flaky tests.
- **Agents fit the flake-fixing job.** Agents can scan far more of the codebase and logs than a human can, and quickly, and they can babysit the validation of a fix for hours without intervention, which humans are terrible at.
- **The identify-fix-verify loop shapes the workflow.** The fix-flakes orchestrator (Opus) reads a Datadog CSV seed to download recent CI logs, spawns an Opus flake-fixer subagent that investigates and pushes a fix, then launches a Haiku flake-verifier subagent that polls reruns and filters noise from other flaky tests so the orchestrator can repeat until the test passes the rerun streak or a max attempt count is hit, after which a human reviews the PR.
- **Failure logs keep agents grounded.** Logs usually contain vital clues about what is going wrong, for example a test failure after exactly 20 seconds suggests looking at timeout conditions; without gathering logs, even the most advanced model will hallucinate, convincing itself it fixed an issue while the test stays flaky.
- **Context preservation is deliberate and cheap.** Each flake-fixer produces exactly one analysis and one fix and hands a summary back to the orchestrator; carrying full context between spawns would fill the window fast without helping the next investigation. Subagents also let the team use smaller, cheaper models like Haiku for verification instead of heavy reasoning.
- **The harness fixed most flakiest tests and surfaced latent bugs.** Over a week and a half, the harness fixed 12 of the 15 flakiest tests in ~4-5 hours each using an average of 100-200k tokens, and surfaced two genuine bugs (a conf_loader sorting bug and a concurrent auth race condition) that ended up verified by humans and dashboards.
- **Agents fixed flaky tests without touching test files.** Through log and code analysis the agent concluded the tests were written correctly and the problems lay elsewhere, which humans tend to miss because they assume flakiness comes from bad tests.
- **Do not over-engineer the harness.** Let the agent write throwaway scripts and one-off tools for the task in front of it instead of a comprehensive pre-built harness; the effort pays off in the methodology for identifying and verifying flaky tests and the data that backs those decisions, not in prescribed scripts.
