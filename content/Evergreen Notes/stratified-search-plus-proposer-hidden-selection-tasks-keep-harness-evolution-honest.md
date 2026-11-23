---
type: "evergreen"
title: "Stratified search plus proposer-hidden selection tasks keep harness evolution honest"
created_at: "2026-11-22T22:02:33Z"
updated_at: "2026-11-22T22:02:33Z"
inputs: ["notes-on-starharness-evolving-harnesses-with-stratified-search-for-enterprise-environments", "harness-evolution-pays-off-only-with-a-dense-held-out-oracle"]
provenance_urls: ["https://arxiv.org/html/2608.24804v1", "https://arxiv.org/html/2607.12227v4", "https://lilianweng.github.io/posts/2026-07-04-harness/", "https://addyo.substack.com/p/agentic-verification", "https://hamel.dev/blog/posts/evals/", "https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
answers_questions: ["How do harness-evolution systems choose the held-in selection set and the held-out verifier, and does the split hold when the eval tasks overlap in distribution?"]
---
Agent synthesis

Harness evolution stays trustworthy only when the tasks that steer the search stay hidden from the proposer and the holdout is never consulted. The mechanism is a two-gate split: the evolution pool is built from baseline failure-mode, baseline score, and verifier pass rate, split into proposer-visible search tasks and proposer-hidden selection tasks with matched distributions, and the remaining tasks form a holdout that no proposal, acceptance, or evaluation may read. The existing oracle note prescribes a held-in selection set and a verifier owned outside the loop; StarHarness gives that concrete shape. The baseline run on all N' reproducible tasks supplies the three descriptors, the pool samples roughly half of them, the proposer receives search-task traces and outcomes but none of the selection-task contents, traces, verifier feedback, or per-task outcomes, and acceptance requires an improvement in the hidden selection mean. That is why the 4-12 accepted changes per run lift full-benchmark scores by 20-35 percentage points (40.0% to 75.0% on ITBench), persist on tasks excluded from evolution, and transfer without re-evolution across GPT and Qwen model families. The contrast with the flat practice is the identity-collision trap the existing note names: Meta-Harness searches and reports TerminalBench-2 on the same 89 tasks, and the harness-evolution note shows a flat 63.2 versus 63.2 held-out score, where gains reflect adaptation to instances rather than reusable design. When the eval tasks overlap in distribution, the stratification by failure mode still forces both slices to be representative, so a flat split would misstate generalization. Budget the split before the first patch: run the baseline, match the search and selection slices on baseline score, failure mode, and verifier pass rate, and never put holdout outcomes anywhere in the loop.

## Where it comes from

- [[notes-on-starharness-evolving-harnesses-with-stratified-search-for-enterprise-environments|StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments]]

## What this builds on

- [[harness-evolution-pays-off-only-with-a-dense-held-out-oracle|Harness evolution pays off only with a dense, held-out oracle]]
