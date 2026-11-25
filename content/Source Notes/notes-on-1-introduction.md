---
type: "source-note"
title: "Notes on: 1 Introduction"
raw: "1-introduction"
url: "https://arxiv.org/html/2607.08124v3"
created_at: "2026-11-25T07:01:47Z"
updated_at: "2026-11-25T07:01:47Z"
---
- Archived full text: [[1-introduction|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2607.08124v3>

## What it says

TTHE recasts test-time adaptation for LLM agents as evolution over executable control programs. On each unlabeled test batch, it evolves a population of candidate harnesses through trace-guided proposers (conservative repair, exploratory, adversarial) and selects one with a judge using execution traces and execution-derived proxy signals, with the same frozen LLM serving solver, proposers, and judge. Execution evidence is treated as incomplete rather than as a correctness oracle, so signals (execution health, round-trip consistency, public-test pass rate) are presented alongside candidate code and traces instead of aggregated into a scalar. Results show persistent, inspectable program adaptation: 8-36 point gains on five binary benchmarks and claw-eval, cross-model transfer of batch-specific harnesses, and a 14-point selection regret between the judge and an oracle over the final candidate pool.

## Claims drawn from this source

- **TTHE treats the executable harness as the state of test-time adaptation.** On each unlabeled test batch, TTHE executes a population of candidate harnesses and iteratively refines them through agentic proposers that reason over execution traces, with a judge selecting a candidate via traces and execution-derived proxy signals. The selected harness determines the current batch's outputs and initializes adaptation on the next.
- **Solver, proposers, and judge share one frozen LLM in different roles.** The solver, proposers, and judge operate through different harnesses around the same frozen LLM, without weight updates, access to final-answer labels, or a separately trained adaptation model. Final correctness feedback is used only for post-selection evaluation.
- **Execution evidence is not a correctness oracle.** Successful execution does not establish semantic correctness, and different candidates may agree on an incorrect result, so execution health, round-trip consistency, and public-test pass rate are complementary but incomplete evidence. TTHE presents signals together with candidate code and underlying traces rather than aggregating them into a single scalar objective.
- **TTHE gains 8-36 points over fixed baselines and beats repeated sampling.** Across six execution-grounded benchmarks (text-to-SQL, competitive programming, software engineering, data-science coding, terminal-based tasks, agentic tool use) TTHE improves fixed ReAct-style baselines; on BIRD it reaches 48.7% mean execution accuracy versus 12.7% for the fixed baseline and 16.0% for a 10-run consistency-voting control. Terminal-Bench 2.1 rises from 55.1% to 67.8% and claw-eval from 48.9% to 69.4%.
- **Selection among already generated candidates is a major source of lost performance.** The judge commits to a harness reaching 50.0% on BIRD (25/50), while an oracle over the final candidates available to the judge reaches 64.0% (32/50), a 14-point selection regret, and an oracle over all evaluated candidates reaches 70.0% (35/50). Audited errors include selecting a 3/10 candidate over a 4/10.
- **Evolved harnesses produce concrete inspectable policies.** On BIRD an evolved harness probes database values before SQL generation and grounds filter values in stored casing; on SWE-bench it adopts reproduce-first workflow with root-cause localization, post-edit verification, and a recovery branch for empty patches; on LiveCodeBench it uses a low-cost path escalating to verification after public-test failure; on claw-eval it specifies single-line tool payloads, exact-identifier service chaining, and a pre-delivery completeness check citing retrieved identifiers.
- **Batch-specific evolved harnesses transfer across models.** Executing the DeepSeek-selected BIRD harness on the corresponding batch improves MiMo V2.5 from 32.0% to 56.0% and GPT-5.5 from 36.0% to 68.0%, with no further evolution.
- **Corrective gains and unintended regressions are characterized conditionally.** Under a coupled execution model, a trace-triggered edit improves when m*pi*r > m*(1-pi)*u + epsilon, where m is trigger mass, pi trigger precision, r repair success, u regression after false triggers, and epsilon the off-trigger change term. Trigger precision alone does not establish repair success, and failure-flag clearance cannot certify a strictly positive correctness gain.
