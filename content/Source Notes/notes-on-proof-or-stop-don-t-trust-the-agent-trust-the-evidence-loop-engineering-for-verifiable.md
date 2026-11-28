---
type: "source-note"
title: "Notes on: Proof-or-Stop: Don’t Trust the Agent, Trust the Evidence Loop Engineering for Verifiable Evidence-Gated Lifecycle Control"
raw: "proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable"
url: "https://arxiv.org/html/2607.14890v1"
created_at: "2026-11-28T02:02:23Z"
updated_at: "2026-11-28T02:02:23Z"
---
- Archived full text: [[proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable|Full archived text, with credits]]
- Link: <https://arxiv.org/html/2607.14890v1>

## What it says

Proof-or-Stop Lifecycle Control treats autonomous coding agents as claimants, not actors: every lifecycle transition (reviewed, tested, done, merge-ready) advances only when fresh, tracked-source-state-bound, mechanically verifiable evidence passes the gate predicate. Evidence is a structured record carrying a binding of materialHash/headHash/storyFilesHash/policyHash/commandSetHash plus a receipt identity (command, arguments, cwd, exit code, output digest). The paper's operated implementation and powered ablation show that converting agent output into claim-admissibility decisions reduces visible-pass/hidden-fail amplification relative to compute-budgeted naive retry loops, while adding cost on clean tasks. It also reports audit evidence that independent-vendor review catches defects the author's own green tests miss.

## Claims drawn from this source

- **Agent output is a claim, not lifecycle state.** The paper instantiates agent-as-claim lifecycle semantics: agent outputs may propose lifecycle claims, but do not themselves constitute lifecycle state; transitions advance only when gate-consumable evidence satisfies the predicate.
- **Evidence carries code-state bindings and a receipt identity.** A piece of evidence E carries beta(E) = materialHash/headHash/storyFilesHash/policyHash/commandSetHash and, for executed actions, rho(E) = command, arguments, working directory, exit code, and output digest; signed local receipts also carry producer identity (actor, lane, host or session, signing-key identity).
- **Admissibility requires seven checks.** A gate admits evidence iff Fresh, Complete, IntegrityVerified, ProducerAuthorized, ExecutionAttested, Supports, and OutcomeAccepted all hold; evidence produced against an earlier source state is rejected the instant the tree changes.
- **Done requires a freshness-bound full-test receipt.** Before a story may enter done, the system requires a freshness-bound, authenticated integrity receipt that a configured set of commands (build plus the full test suite) ran to success at the current code state, recording each command, exit code, output digest, materialHash/headHash/storyFilesHash, and policyHash/commandSetHash.
- **Receipt bundles are tamper-evidence against lying agents.** The B-4c65 offline receipt-bundle contract exercised the admissibility rule against a lying agent: the authentic bundle was accepted and 18 tamper classes were rejected with zero false accepts and zero false rejects in the tested suite.
- **The gated loop amplifies fewer visible-pass/hidden-fail cells than budget-capped naive retry.** In the pre-registered 9,240-cell ablation, the A4 evidence-gated loop amplified 2/1800 injected cells versus 31/1800 for the compute-budgeted A2' naive control (+1.6pp not-amplified, 95% CI [0.8,2.5]), while spending roughly 1.2x the tokens.
- **Enforcement, not the review signal itself, is what helps.** The near-compute A3-vs-A4 contrast isolates enforcement: A3 used the same one-review signal as advisory and amplified 14/1800 injected cells, while A4 converted that signal into an enforced lifecycle gate and amplified 2/1800.
- **The loop is pure overhead on clean tasks but valuable under green-but-wrong faults.** On clean well-specified tasks all four arms completed 9/9, so the only separation was cost and latency (A4/A1 = 2.07x cost, 2.51x wall); under injected green-but-wrong faults the bare loop amplified 15/15 wrong artifacts while the gated loop shipped 0/15.
- **Independent review catches what author green tests miss.** In the curated 12-story deep set of 28 findings, 26 of 28 (93%) were filed while the author's own smoke or tests were passing; a refreshed 68-row cross-vendor exhibit contained 68 high/critical independent-vendor review findings across 26 stories, all resolved.
