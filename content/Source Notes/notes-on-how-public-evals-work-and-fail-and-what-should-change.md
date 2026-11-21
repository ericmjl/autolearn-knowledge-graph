---
type: "source-note"
title: "Notes on: How Public Evals Work and Fail, and What Should Change"
raw: "how-public-evals-work-and-fail-and-what-should-change"
url: "https://eugeneyan.com/writing/public-evals"
created_at: "2026-11-21T05:01:55Z"
updated_at: "2026-11-21T05:01:55Z"
---
- Archived full text: [[how-public-evals-work-and-fail-and-what-should-change|Full archived text, with credits]]
- Link: <https://eugeneyan.com/writing/public-evals>

## What it says

Eugene Yan reviews twelve public evals (coding, knowledge work, browsing/computer use), showing how they are built (instruction, environment, grader, optional reference), the four design principles they share (deterministic checks, outcome-not-steps grading, all-pass scoring, difficulty mining), the two failure modes (skipped verification and dropped requirements), two grader gaps (false negatives and false positives), and where evaluation thinking goes wrong (average pass rate, dollar cost, verifiable-but-not-judgment-heavy tasks, single-shot instructions). He recommends looking past headline numbers and running your own evals.

## Claims drawn from this source

- **Grader failures are common in public evals.** In eight of twelve public evals studied, there is evidence the grader failed work that should have passed.
- **False negatives dominate grader gaps.** Reviewers found 41 of 65 Terminal Bench 4.0 tasks graded on unstated requirements, and 23 of 113 DeepSWE tasks marked correct solutions as failures. On BrowseComp, human trainers who solved a question disagreed with the reference answer on 50 of 367 questions (14%), and Harvey LAB removed 17 unsolvable criteria from the held-out set.
- **False positives pass wrong work.** Assertions usually check that an expected point is present, not that the rest of the work is correct. Artificial Analysis found material hallucinations in more than 60% of Harvey LAB results that passed every criterion, and 55% of AutomationBench assertions only check string containment, so a keyword match can pass regardless of correctness.
- **Average pass rate hides reliability differences.** Two agents both scoring 70% on average can differ hugely: one solves 70% of tasks every time while the other solves every task 70% of the time, and over five trials the second falls to 17% pass^k while the first still holds 70%.
- **Cost per task is a misleading metric.** Evals average cost across every task attempted, and models can fail cheaply by skipping verification or giving up early. On Agents' Last Exam, 17% of failures were premature abandonment, and on FrontierSWE one model submitted and stopped within eight hours of a 20-hour budget in 169 of 170 trials.
- **Token cost savings can be time-foolish.** GPT-4o cost about a tenth of GPT-5 per task in GDPval, but once expert review and redo time were factored in, GPT-4o was slower than an expert alone while GPT-5 was faster. On AutomationBench, models declared success on 72% to 91% of the failures analyzed.
- **Single-shot instructions miss multi-turn work.** Users rarely write all requirements upfront; they discuss, review a draft, add constraints, and course-correct. Single-shot benchmarks do not test whether models ask clarifying questions on ambiguous requests or handle evolving requirements.
