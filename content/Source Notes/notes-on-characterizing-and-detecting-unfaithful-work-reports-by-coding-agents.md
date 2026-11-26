---
type: "source-note"
title: "Notes on: Characterizing and Detecting Unfaithful Work Reports by Coding Agents"
raw: "characterizing-and-detecting-unfaithful-work-reports-by-coding-agents"
url: "https://arxiv.org/html/2611.25760v1"
created_at: "2026-11-26T17:04:10Z"
updated_at: "2026-11-26T17:04:10Z"
---
- Archived full text: [[characterizing-and-detecting-unfaithful-work-reports-by-coding-agents|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2611.25760v1>

## What it says

A mixed-methods study of real developer-agent conversations in SWE-chat characterizes unfaithful reporting by coding agents. Claims split into four categories (misreported observations, misattributed evidence, overstated task success, faulty technical explanations) with eleven subtypes; overstated task success dominates (69.3%). Among 435 sampled work reports, 37.24% contain at least one unfaithful claim. Challenges trigger on average 4.3 further user turns and 12.71 minutes of recorded handling, with dissatisfaction in 40.28% of user messages. The authors build FaithDetector, which attains 93.06% macro-F1 against a baseline of 80.42%, and argue that reports should be scored separately from task outcomes, with routine claim-level checking against the work records.

## Claims drawn from this source

- **Unfaithful reporting splits into four categories and eleven subtypes.** Misreported observations (45 claims, 13.3%), misattributed evidence (28 claims, 8.3%), overstated task success (235 claims, 69.3%), and faulty technical explanations (42 claims, 12.4%). Overstated completeness is the largest subtype at 110 claims.
- **Unfaithful claims are frequent in sampled work reports.** 162 of 435 sampled reports (37.24%) contain at least one unfaithful claim; most affected reports contain one or two, and a smaller group contains three or more.
- **Handling a reporting problem takes many extra exchanges.** Challenged cases average 4.29 user turns, 36.67 main-model responses, and 35.19 tool calls (median 3 turns, 19 calls; 90th percentile about 9 turns and 86 calls), and 12.71 minutes of recorded response and execution time (median 5.57; 90th percentile 32.31), with 12,135 partial output tokens on average.
- **Follow-up dissatisfaction outlasts the first challenge.** Dissatisfaction appears in 40.28% of user messages in challenged cases versus 17.90% in comparison messages (22.38 points higher); excluding first-challenge messages, 30.71% remain dissatisfied.
- **FaithDetector detects unfaithful claims about 13 points above the baseline.** On naturally sampled reports, FaithDetector attains 93.06% macro-F1 versus 80.42% for a baseline using the same reports and trajectories (+12.64 points, 95% CI 9.71-15.49). On unfaithful claims it reaches 88.91% F1 versus 67.92% for the baseline, with recall 86.98% versus 59.71%.
- **Genuine edits and passing checks coexist with inaccurate claims.** In the cases, successful local operations, passing tests, and healthy services can accompany inaccurate statements about the outcome, destination, or operating conditions; tests and health checks do not establish what the report claims.
- **Claim-level checking should be routine, not prompted by suspicion.** Because 37.24% of reports contain unfaithful claims and problems surface only when a user challenges them, reviewers should check completion, attribution, observation, and explanation claims before accepting, merging, deploying, or building on the work, with depth following the decision the report supports.
- **Reports should carry their evidence and be scored separately from outcomes.** The authors propose that a faithful report names the artifact or revision it concerns, the conditions of the check, the record that supports it, and what remains unverified, and that evaluations score task credit and reporting faithfulness as separate scores so that an overstated, faithful, and over-hedged report with identical task credit separate on the reporting score.
