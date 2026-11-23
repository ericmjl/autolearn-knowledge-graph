---
type: "source-note"
title: "Notes on: StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments"
raw: "starharness-evolving-harnesses-with-stratified-search-for-enterprise-environments"
url: "https://arxiv.org/html/2608.24804v1"
created_at: "2026-11-22T22:01:30Z"
updated_at: "2026-11-22T22:01:30Z"
---
- Archived full text: [[starharness-evolving-harnesses-with-stratified-search-for-enterprise-environments|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2608.24804v1>

## What it says

StarHarness evolves a frozen model's harness (prompts, tools, skills, MCP providers, subagents, loop config) against a compact, failure-mode-stratified task pool, separating proposer-visible search tasks from proposer-hidden selection tasks and reserving a holdout set for generalization. Across three stateful enterprise benchmarks (ITBench SRE, EnterpriseOps-Gym ITSM, AutomationBench Finance), the evolved harness gains 20-35 percentage points over the default harness after 4-12 accepted changes, persists on tasks excluded from evolution, and transfers without re-evolution across GPT and Qwen model families. The gains come from interface repairs, explicit environment conventions, and operational knowledge that compresses search, which shortens workflows and reduces false positives.

## Claims drawn from this source

- **Task partition is built before evolution.** From the full benchmark of N tasks, they retain N' reproducible tasks, then sample an evolution pool of K tasks (typically K~N/2) stratified by baseline failure mode, baseline score, and verifier pass rate, computed from a baseline run on all N' tasks.
- **Search and selection tasks are distribution-matched but proposer-hidden.** The evolution pool is split into proposer-visible search tasks and proposer-hidden selection tasks while matching baseline score, failure-mode, and verifier-pass distributions. The proposer never sees selection-task contents, traces, verifier feedback, or outcomes; the remaining N'-K tasks form a holdout that never affects proposal or acceptance.
- **Held-out tasks never enter proposal or acceptance.** Held-out outcomes are kept out of the loop entirely, so the protocol approximates optimizing the true target over the permitted harness space rather than the search set.
- **Evolution gains concentrate on full-benchmark performance.** Across ITBench, EnterpriseOps-Gym, and AutomationBench, harness evolution improves full-benchmark performance by 20-35 percentage points over the default harness, after 4-12 accepted changes per environment.
- **Fewer accepted changes suffice and cost drops.** ITBench accepted 4 patches, EnterpriseOps-Gym 12, AutomationBench 5; StarHarness reduces estimated GPT-5.4 inference cost by 17% on ITBench, 53% on EnterpriseOps-Gym, and 29% on AutomationBench at published rates.
- **Gains transfer without re-evolution across model families.** The same GPT-5.4-evolved harness, evaluated without re-evolution, improves transferred GPT and Qwen models on all three benchmarks.
- **Accepted edits cluster into three repairs.** Interface repair (MCP argument handling, compound schema preservation, pruning misleading fields, linkage self-reference cues), environment conventions (execution contracts, date anchoring to sandbox clock, triage before mutation), and operational knowledge that compresses search (forensics overview, deterministic date and finance calculators).
- **Frozen baselines still mis-score the lab.** The authors critique Meta-Harness, which uses held-out sets for text classification and math but reports TerminalBench-2 on the same 89 tasks it searched, distinguishing search performance from generalization instead.
