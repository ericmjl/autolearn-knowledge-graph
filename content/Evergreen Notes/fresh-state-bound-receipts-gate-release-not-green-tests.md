---
type: "evergreen"
title: "Fresh state-bound receipts gate release, not green tests"
created_at: "2026-11-28T02:03:20Z"
updated_at: "2026-11-28T02:03:20Z"
inputs: ["notes-on-proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable", "repeated-paired-trials-beat-single-run-release-gates"]
provenance_urls: ["https://arxiv.org/html/2607.14890v1", "https://makeyouragent.ai/blog/stop-flaky-ai-agent-evals-release-gates", "https://www.endorlabs.com/learn/why-evals-are-the-missing-layer-in-integration-testing", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339"]
refutation_status: "untested"
answers_questions: ["How do teams implement paired-trial release gates with heterogeneous graders and fixtures, and what does a tamper-evident evidence receipt contain?"]
---
Agent synthesis

Repeated paired trials and fresh state-bound receipts make the release gate honest: a gate built on one green test run will promote a green-but-wrong artifact, while a gate that decides only on receipts bound to the exact tracked source tree survives a lying agent. The mechanism is the binding: an admissible receipt carries the command, arguments, working directory, exit code, output digest, and a binding of materialHash/headHash/storyFilesHash/policyHash/commandSetHash; the freshness conjunct rejects the moment the tree changes, so a stale pass can never be re-presented as current. The paired-trial design adds the statistical layer: the same baseline and candidate run on the same cases and fixtures, per-slice effects computed before the aggregate, extra repetitions spent only on unresolved slices, and an honest pass/fail/inconclusive verdict that never converts inconclusive into a pass.

The Proof-or-Stop source answers the receipt half directly: a done transition requires a freshness-bound, authenticated full-test receipt, 18 tamper classes are rejected with zero false accepts in the tested suite, and a review floor demands multi-round independent verdicts over the same materialHash. The paired-trials note answers the design half: one stochastic attempt cannot support a release verdict, and the gate is the measurement instrument, so its decision rule is never a contest between random outcomes. Together they show that statistical trial design and evidence binding are the same control problem seen from two sides. The synthesis is that a release gate should consume the receipt, not the badge: the paired-trial apparatus decides whether the result is statistically trustworthy, and the receipt decides whether it was produced for the code being merged.

What this rules out is convergence of two tempting shortcuts: adding another retry on a flaky run and adding another reviewer without a hard gate. The gated review (A4) reduced visible-pass/hidden-fail amplification from 31/1800 to 2/1800 injected cells versus a compute-budgeted naive loop, while the near-compute A3 contrast shows the review signal alone, treated as advice, still amplifies 14/1800. Clean tasks show the cost honestly: the loop adds overhead with no completion benefit. The prescription is concrete: never let a release gate consume a single green run; require the receipt to re-derive at the exact commit being merged and refuse to conclude when the evidence is missing or stale. (see: repeated paired trials beat single-run release gates)

## Where it comes from

- [[notes-on-proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable|Proof-or-Stop: Don’t Trust the Agent, Trust the Evidence Loop Engineering for Verifiable Evidence-Gated Lifecycle Control]]

## What this builds on

- [[repeated-paired-trials-beat-single-run-release-gates|Repeated paired trials beat single-run release gates]]
