---
title: "Proof-or-Stop: Don’t Trust the Agent, Trust the Evidence Loop Engineering for Verifiable Evidence-Gated Lifecycle Control"
type: "raw-source"
url: "https://arxiv.org/html/2607.14890v1"
author: "Jek Huang † † thanks Corresponding author jek huang ai"
publication: "arXiv"
published: "2026-06-23"
archived: "2026-11-28T02:01:39Z"
---

> [!quote] Original source
> **Author(s):** Jek Huang † † thanks Corresponding author jek huang ai  
> **Title:** Proof-or-Stop: Don’t Trust the Agent, Trust the Evidence Loop Engineering for Verifiable Evidence-Gated Lifecycle Control  
> **Published in:** arXiv  
> **Date:** 2026-06-23  
> **Original:** <https://arxiv.org/html/2607.14890v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable|Source note]]
Themes: [[Loop engineering]]
Why it was archived: paired-trial release gates and what a tamper-evident evidence receipt contains

## Archived text

Proof-or-Stop:

Don’t Trust the Agent, Trust the Evidence

Loop Engineering for Verifiable Evidence-Gated Lifecycle Control

Abstract

Autonomous coding agents increasingly execute multi-step software work. However, lifecycle states such as reviewed, tested, done, and ready-to-merge remain claims unless a downstream system can decide whether those claims are supported by current evidence. In this work, we present Proof-or-Stop Lifecycle Control, a method in which lifecycle transitions are admitted only when fresh, tracked-source-state-bound, mechanically verifiable evidence satisfies the relevant gate. The method instantiates an agent-as-claim lifecycle semantics: agent outputs may propose lifecycle claims, but do not themselves constitute lifecycle state. Here, “proof” is used operationally to mean gate-admissible evidence under a stated trust model, not a proof of semantic program correctness.

The method was instantiated in the open-source Proof-or-Stop implementation and evaluated through mechanism tests, a powered control-policy ablation, and operated self-application evidence. Mechanism checks show that done and receipt claims do not advance on self-report in the tested engine contract: the unattended-loop engine passed 10/10 scenarios with zero false-done, and local-key receipt bundles rejected 18 tamper classes with zero false accepts in the tested suite. In a 9,240-cell powered ablation, the pre-registered A4-vs-A2′ contrast reduced visible-pass/hidden-fail amplification from \(31/1800\) injected cells under a compute-budgeted naive loop to \(2/1800\) under the gated loop (+1.6pp not-amplified, 95% CI \([0.8,2.5]\)). The separation was concentrated in a trap-active task; the near-compute A3-vs-A4 contrast (\(14/1800\) vs \(2/1800\)) indicates that the improvement is associated with enforcing the review signal as a lifecycle gate, rather than merely adding a reviewer. Finally, the operated self-application corpus (565 stories / 1007 review findings, 94.8% resolved) and a refreshed 68-row high/critical cross-vendor exhibit show that the system produces auditable evidence on its own development. Together, these results support Proof-or-Stop as a model-agnostic, host-neutral control layer for deciding which autonomous-agent claims a lifecycle may safely act on, rather than as a new model or coding agent. The evaluation is limited to one model family, 24 ablation tasks, and a self-hosted corpus.

Keywords: AI agents; language models; autonomous agents; software lifecycle; verifiable evidence; evidence gating; provenance; reproducibility; agentic software engineering.

1 Introduction

Autonomous coding systems increasingly combine durable execution, tool use, review agents, and handoff protocols. These systems have made agent work more executable, resumable, and measurable. However, they do not by themselves decide whether lifecycle claims such as tested, reviewed, done, and ready to merge are safe for downstream automation to act on. This distinction becomes load-bearing when an unattended agent can generate code, retry until visible checks pass, and narrate completion in the same workflow that will be asked to advance the work.

The resulting problem is claim admissibility. A self-report is not evidence; a log line saying “All tests passed” is not evidence that the tests correspond to the code about to be merged; and a reviewer response saying “LGTM” is not, by itself, an artifact that a later gate can re-check. In existing practice, a green pipeline or a successful agent handoff can therefore coexist with a stale, incomplete, or unsupported lifecycle claim. The missing control is not another model, but an admissibility rule for deciding when a claim may move lifecycle state.

Thesis.

In this work, we present Proof-or-Stop Lifecycle Control. The key idea is to treat every consequential actor output as a claim and to admit that claim only when fresh, structured, tracked-source-state-bound evidence satisfies a gate predicate. If the evidence is admissible, the lifecycle advances; if it is missing, stale, incomplete, or outside the stated trust model, the system repairs within a bounded loop, degrades honestly, escalates, or stops. In the Proof-or-Stop implementation, this evidence is protected by authenticated integrity, producer identity, and freshness checks over the exact tracked source state. We use “proof” operationally: a proof is gate-admissible evidence under that trust model, not a formal proof of semantic program correctness. The broader engineering practice is Loop Engineering: engineering the autonomous develop/review/test/done loop so that control decisions are made by evidence-checking gates.

Semantic stance.

We separate the contribution into four layers. First, the semantic shift is agent-as-claim: an agent output may propose a lifecycle claim, but it is not itself lifecycle state. Second, Proof-or-Stop Lifecycle Control is the methodology: lifecycle advancement is a claim-admissibility decision. Third, evidence gates are the mechanism: claims advance only when fresh, tracked-source-state-bound evidence satisfies the relevant predicate. Fourth, receipts, source-state hashes, review runs, done gates, and the ablation, corpus, and cross-vendor exhibits are the instantiation and evidence used to evaluate the method.

Contributions.

- C1 — Proof-or-Stop Lifecycle Control.
- We define a model-agnostic evidence-gated control method for autonomous coding lifecycles. Every consequential lifecycle claim emitted by a host agent or workflow actor must reduce to gate-consumable evidence before it can advance phase, review, test, done, or merge-relevant state; ordinary notes and documentation remain light (§3, §4).
- C2 — Code-state-bound evidence mechanics.
- We instantiate claim admissibility through authenticated integrity, producer identity, and freshness binding. Evidence carries fresh material, head, and story hashes; policy and command-set hashes; and a receipt identity (command, arguments, working directory, exit code, output digest). Stale, reconfigured, tampered, unauthorized, or build-proof-missing evidence is rejected (§3, §4).
- C3 — Host-neutral transfer as an evidence property.
- We characterize host-neutrality as local evidence over the same code identity rather than trust in a remote host or protocol. Safety mechanisms and the cross-machine resume (HN-2) are verified; the strong cross-vendor quorum remains gated (§7).
- C4 — Operated evaluation and boundary discipline.

What is established, and what is not.

Table 1 separates the evidence tiers used in the paper. The engine contract and evidence discipline are demonstrated in the operated Proof-or-Stop corpus. The comparative ablation is a powered 9,240-cell result: the primary A4-vs-A2′ contrast against the pre-registered budget-capped naive control has a CI-excluding-zero not-amplification gain (H1 \(+1.6\)pp, [0.8,2.5]) and marginal completion gain (H2). The recovery claim is supported by both the powered full-matrix estimate (§6) and a verified pilot showing a loop-fidelity gradient on visible-test-passing wrong artifacts. Clean tasks show overhead; green-but-wrong injected faults show risk-mitigation value, and the 68-row cross-vendor refresh shows that independent-vendor review caught high/critical defects in the paper’s own evidence machinery. The present evidence supports host-neutral gate semantics and local receipt validation; strong cross-vendor quorum claims remain gated on fresh independent host verdicts over the same material hash. These boundaries are part of the method: claims are reported only at the tier supported by admissible evidence. Cross-domain, multi-model, external-benchmark, and strong independent-host generalization remain future work.

Roadmap.

Section 2 states the claim-admissibility problem in autonomous software work. Section 3 formalizes evidence admission, and Section 4 instantiates it in the Proof-or-Stop lifecycle. Sections 5 and 6 evaluate the unattended loop and injected-failure recovery. Section 7 covers host-neutral transfer; Section 8 reports self-application and audit evidence; Section 9 states the honest boundary of experience reuse. Sections 10–13 cover related work, threats, future work, and the conclusion.

Proof chain at a glance.

This paper does not ask the reader to accept one large informal claim. It builds one chain: an agent output is a claim; a lifecycle transition needs admissible evidence; a gate checks that evidence against the current tracked source state; and missing or stale evidence blocks advancement. Table 1 is the single map for current evidence, tier, and boundary. In the table, engine evidence checks that the gate behaves correctly; empirical evidence tests whether acting on the gate helps against weaker controls; independent-host evidence is reserved for fresh multi-host receipts.

Terminology. A claim is an agent- or workflow-implied statement such as reviewed, tested, done, or ready-to-merge. Admissible evidence satisfies the freshness, tracked-source-state binding, authenticated-integrity, producer-authorization, and accepted-outcome checks in Eq. (2). Amplified means a wrong artifact was shipped or propagated; not-amplified means it was repaired, stopped, or otherwise not propagated.

2 Background and Problem

Three lines of systems work have made autonomous agent work more robust, and each leaves the trust problem open.

Durable / resumable execution (Temporal-style workflows, graph runtimes, agent frameworks with persistence, transactional agent runtimes) makes work survive crashes and restarts by checkpointing state. But surviving state is not verified state: resuming a workflow that recorded “tests passed” re-asserts the recorded claim; it does not re-establish that the claim matches the code now being merged.

Cross-vendor coordination (agent-to-agent protocols, tool/context protocols, and the broader family of agent-interoperability standards) routes messages and delegates tasks across heterogeneous systems. These are communication layers. They standardize how a verdict travels, not whether it is admissible against the current artifact.

Evidence-driven release gates and deterministic verification loops aggregate signals into promote/hold/rollback decisions. This is the closest prior practice. The gap we address is binding and scope: a release gate typically makes one decision at the end, on coarse signals; we bind every lifecycle evidence item to code identity (materialHash/headHash/storyFilesHash), add authenticated integrity digests and a receipt identity, and operate it lifecycle-wide on a real self-hosted system.

The common failure mode these leave intact is that a green pipeline can coexist with a real defect. If downstream automation treats that green status as sufficient evidence, it may advance, merge, and mark the work done. Our deep finding set (§8) measures how often “author’s tests pass” failed to imply “correct” in the operated corpus.

The agent setting makes this sharper than ordinary CI slippage. A conventional gate can often assume the actor is honest but fallible; an unattended coding agent can generate the code, retry until a visible check turns green, and narrate or package success. The gate must therefore verify state-bound evidence rather than trust the actor’s report. This is not only a theoretical risk: in the powered ablation, the compute-budgeted naive loop amplified \(31/1800\) visible-pass/hidden-fail injected cells while the gated loop amplified \(2/1800\) (Table 11); in the self-application deep set, 26 of 28 findings were filed while the author’s tests were green (§8).

3 The Evidence-Gating Principle

Method abstraction.

Proof-or-Stop Lifecycle Control reduces lifecycle advancement to a claim-admissibility decision. The core method is:

Proof-or-Stop controls each lifecycle transition; repeated proof-or-stop transitions form the bounded lifecycle loop. In the autonomous-coding implementation evaluated here, actors include agents, reviewers, tools, and workflow commands. Their outputs are interpreted as lifecycle claims; claims require admissible evidence; evidence is checked by gate predicates; and only passing gates may advance lifecycle state. Evidence-gated claim admissibility is the enforcement mechanism for this method. This is the operational form of agent-as-claim semantics: the actor may emit the claim, but the lifecycle transition is decided by evidence admission.

The control abstraction is domain-neutral: actor output is treated as a claim, claims require admissible evidence, and gates decide whether a lifecycle transition may advance. This paper empirically evaluates the abstraction in autonomous coding lifecycles. Cross-domain instantiations require domain-specific evidence packages and separate evaluation.

We make the thesis precise. Let \(H\) be the current tracked source state of a unit of work, identified by content digests over the version-control tree. We define three identities, computed over git ls-tree with the lifecycle’s own metadata excluded so that recording evidence does not perturb the hash it is bound to:

These identities bind the tracked source state. They are not, by themselves, a full executable-state attestation: dependency resolution, toolchain/container/OS, environment variables, external service state, and untracked generated files must be covered by policy, command, environment, or dependency digests if a deployment needs that stronger claim.

A piece of evidence \(E\) is a structured record (not prose) describing the outcome of a checkable action: a test run, a build, a scope check, a reviewer verdict. Evidence carries a binding \(\beta(E)=\langle\textsf{materialHash}_{E},\textsf{headHash}_{E},\textsf{storyFilesHash}_{E},\textsf{policyHash}_{E},\textsf{commandSetHash}_{E}\rangle\) and, for executed actions, a receipt identity \(\rho(E)=\langle\text{cmd},\text{args},\text{cwd},\text{exit},\textsf{outputDigest}\rangle\). Signed local receipts and review verdicts also carry producer identity, such as actor, lane, host or session, and signing-key identity.

Admissibility.

A gate admits evidence \(E\) for claim \(c\) at state \(H\) iff

Here \(\mathrm{Fresh}\) checks the required materialHash/headHash/storyFilesHash bindings against the live state \(H\); \(\mathrm{Complete}\) checks required policy and command-set bindings; \(\mathrm{IntegrityVerified}\) checks signatures and digest chains; \(\mathrm{ProducerAuthorized}\) checks that the actor, lane, host/session, or signing key is authorized for the claim; \(\mathrm{ExecutionAttested}\) checks command, arguments, working directory, exit code, and output digest when execution is required; \(\mathrm{Supports}\) ties the record to claim \(c\); and \(\mathrm{OutcomeAccepted}\) checks the gate-specific pass or accepted-degradation outcome. The freshness conjunct defeats the most common silent failure: evidence produced against an earlier source state is rejected the instant the source tree changes, because \(\textsf{materialHash}_{E}\neq\textsf{materialHash}(H)\) (Eq. (1)). Missing build proof, a reconfigured command set (commandSetHash mismatch), an unauthorized producer, a failed execution attestation, or a hand-edited metadata file all fail Eq. (2). Local-key receipts provide authenticated integrity, producer identity, and freshness under the stated single-host trust assumption; they do not independently prove execution truth against a compromised runner or semantic correctness of the claim.

Offline receipt-bundle contract.

B-4c65 exercises Eq. (2) as an adversarial contract test for the “lying agent” case: an agent may claim that DONE evidence is fresh, signed, and passing, but the verifier accepts only a self-contained bundle whose binding and receipt identity re-check offline. The implementation exposes a programmatic API that builds a local-key-signed bundle from DONE-story evidence and verifies it without network or server access. Its assurance label is deliberately local-key-single-host: it proves portable freshness and tamper-evidence for a local receipt, not an independent multi-host quorum. We call this local-key scope below.

Gate-strength self-red-team contract.

A verifier is only as good as its discrimination: a gate that blocks everything has a perfect “catch rate” yet ships nothing. B-7b6e instruments this directly by scoring a reviewer over a hidden-ground-truth corpus of passes-the-visible-test-but-wrong artifacts plus one genuine control. The score is the pair \((\textsf{catchRate}=\textsf{caught}/\textsf{wrongTotal},\ \textsf{falseBlock})\), because catch rate alone is gameable. Three reference reviewers make the metric non-vacuous: a test-only reviewer misses every wrong-but-test-passing artifact; a block-all reviewer reaches \(\textsf{catchRate}=1.0\) but falsely blocks the genuine control; and an oracle reviewer reaches \(\textsf{catchRate}=1.0\), \(\textsf{falseBlock}=0\), dominating both. The score is itself evidence: B-7b6e publishes it as a B-4c65 receipt bundle in local-key scope, and the gate-strength verifier re-derives the result digest so the receipt binds not just “a pass happened” but “this discrimination score, over this hidden-truth corpus, is the one attested.” Honest scope: these are reference endpoints and an oracle, not a live review lane; integrating the metric into a live artifact-reading review lane remains explicit future work.

Evidence-instrument characterization contract.

An evidence gate is only as trustworthy as the instruments that produce its evidence. Where B-4c65 and B-7b6e red-team a receipt and a reviewer, the proof-or-stop replay campaign (five DONE stories B-9e44 / B-bae9 / B-2a5b / B-f511 / B-853a) red-teams a producer: the memory/playbook runtime baseline verifier. Against a frozen pre-registered protocol (protocol.json, sha256 a3a781fed2…) it characterizes the instrument on four properties — replay-determinism, tamper-fail-closed, resume-integrity, and scale-envelope — and adjudicates them with a purely offline three-state (pass / fail / inconclusive) analyzer that reads only committed evidence and re-verifies every ledger record’s digest before adjudicating. The resume-integrity arm is the proof-or-stop discipline itself under injected interruption: boundary and mid-iteration kills leave, on resume, exactly one identity-keyed record per iteration with zero duplicates and zero gaps. The analyzer emits a report whose digest 198e33866b… \(=\textsf{sha256}(\textsf{canonicalJson}(\textit{report}-\textit{digest}))\) was re-derived byte-for-byte offline and cross-vendor (an independent Codex host recomputed it), and a hermetic 19-check selfcheck proves the three-state logic un-gameable: incomplete, stub, mislabeled, non-physical, or tampered evidence each yields fail / inconclusive / abort, never a false all-pass, and the claim text is emitted only when all four properties hold. Honest scope: this characterizes one instrument under a frozen protocol over enumerated scenarios; the report digest is a reproducibility and tamper-evidence anchor at local + cross-vendor-replication scope, not an authenticated multi-host quorum, and the study is not Tier-C (a signing adversary who recomputes digests is out of scope).

Gated advancement.

Let a unit of work pass through phases \(\phi_{1}\to\phi_{2}\to\cdots\). Each transition \(\phi_{i}\to\phi_{i+1}\) declares a set of required claims \(C_{i}\) (e.g. “scope is frozen,” “tests pass,” “review quorum met”). The transition is permitted iff every required claim is backed by admissible evidence:

Crucially, a natural-language report from an agent is not an \(E_{c}\): it provides neither verified integrity nor attested execution and carries no binding. Eq. (3) therefore has no term for self-report (Fig. 2).

Scope (why this is not too heavyweight).

The heavy machinery of Eqs. (2)–(3) applies only to claims in \(\bigcup_{i}C_{i}\) — those that move phase, pass review, certify tests, mark done, or merge. Ordinary developer notes, design rationale, and documentation are advisory: they inform attention, never a gate, and are deliberately excluded from every binding (§9). The discipline is expensive exactly where being wrong is expensive, and cheap everywhere else.

4 Lifecycle Instantiation

Proof-or-Stop instantiates Eqs. (2)–(3) as a command-line lifecycle for a unit of work it calls a story. A story moves init \(\to\) init-check \(\to\) plan \(\to\) dev \(\to\) review \(\to\) test \(\to\) done, and each arrow is an instance of Eq. (3) with concrete required claims:

- • 

plan\(\to\)dev: an adversarial plan review must persist a structured result (not a “looks good”); scope is frozen into a contract bound to declared file paths.

- • 

dev\(\to\)review: a scope-contract check verifies the diff touches only contracted paths; out-of-scope edits fail closed.

- • 

review\(\to\)test: independent reviewer lanes must persist verdicts; critical/high findings block; a per-run test receipt must be admissible.

- • 

test\(\to\)done: see the full-test receipt and review-assurance floor below.

Review-run binding race.

B-6c4d refined the REVIEW evidence rule after a concurrency failure in which a reviewer retrying review_run_start minted a newer reviewRunId on the same lane and round, causing an earlier no-issue pass to be rejected solely by id-recency even though it was still bound to the same material and scope. Id-recency is therefore not itself a freshness predicate. A PASS is admissible from any signed run in the current review round if the run’s materialHash/storyFilesHash and scope binding still match the live story state. The relaxation is kind-aware: open FINDING evidence still requires the lane’s latest run, so a newer pass cannot hide an unresolved older finding. The only whole-tree-drift downgrade through storyFilesHash also excludes EMPTY_STORY_FILES_HASH on both the recorded and live side; the hash of an empty story-owned diff carries no story-owned signal and falls back to strict materialHash freshness. Thus the gate removes a false rejection without weakening the surviving round, lane, signature, freshness, and scope checks.

The done-required full-test receipt.

Before a story may enter done, Proof-or-Stop requires a freshness-bound, authenticated integrity receipt that a configured set of commands (a build plus the full test suite) ran to success at the current code state. The receipt records each command, its exit code, an output digest, the materialHash/headHash/storyFilesHash, and a \(\textsf{policyHash}/\textsf{commandSetHash}\); it is rejected if any command set was altered or if the source tree has drifted since. This is C2 in its sharpest form: “done” is not the agent saying done, and not even a green test log — it is a receipt that re-derives, bound to the exact tree being merged.

The review-assurance floor.

For material code changes on high-risk paths, a done transition additionally requires a multi-round, multi-host review floor. Let a host verdict be admissible (Eq. (2)) and let two verdicts be independent if they differ in host, session, and signing-key identity. Let \(S\) denote the current tracked source state for this floor. The full floor is

i.e. at least \(R{=}3\) rounds each carrying \(\geq K{=}2\) independent passing verdicts over the current materialHash. When a second host is genuinely unavailable, the system does not synthesize a quorum: it records a degraded single-host fallback that remains local-only, preserving honesty by construction:

Pull requests as interface, not trust boundary.

The 3\(\times\)2 host done floor shifts the trust root for merge-readiness away from a pull-request comment thread or approval checkbox and toward a Proof-or-Stop evidence certificate. A pull request may remain a useful display, discussion, and audit surface, but the admissibility decision is the current-tracked-source-state-bound evidence bundle: fresh full-test receipts, admissible review verdicts, material-hash freshness, and the required review-assurance floor. In the full-quorum case, this supports a done or merge-readiness certificate that a repository could consume as a merge gate. In the degraded single-host case, the certificate remains local assurance only and must not be upgraded into full merge-readiness. This paper therefore supports PR-independent merge-readiness as a mechanism claim; it does not claim general PR-less auto-merge or production release.

A merge consumer must verify the certificate against the exact source commit it is about to merge and perform the merge under a protected compare-and-swap condition: if either the source commit or the target branch head changes between verification and merge, the certificate is stale and the merge is refused.

We observed Eqs. (2) and (4) act in practice while preparing this very work: a small fix re-merged the main line under it, which advanced the tree hash and invalidated previously-submitted host verdicts (their \(\textsf{materialHash}_{E}\) no longer matched \(\textsf{materialHash}(H)\)); the floor refused done until the verdicts were re-attested over the new materialHash — the freshness conjunct of Eq. (2) doing exactly its job.

5 The Unattended Loop

To evaluate the engine contract, we run Proof-or-Stop as a single evidence-gated loop (Figure 4): plan\(\to\)execute\(\to\)review\(\to\)bounded reflect\(\to\)gate\(\to\)done. At every step, agent actions are reduced to structured, code-bound evidence; the gate decides whether to advance, loop back for a bounded retry, or stop safely. The machinery is first verified as a contract (§5.1) and then compared with weaker control regimes (§5.2). This is proof-or-stop control: the loop may continue only by producing admissible evidence, not by repeating or rephrasing a lifecycle claim.

5.1 Engine contract (verified)

To evaluate the loop contract, we encode a full unattended develop loop as ten scenarios (Table 9), each asserting whether the engine should advance or block. The suite passes 10/10 with zero false-DONE and a safety success rate of \(1.0\) on the engine harness. This is a Tier-A correctness check of the machinery: it demonstrates that the gate enforces the contract, but it does not by itself show that acting on the contract improves outcomes against a baseline. That comparison is §5.2.

Large-ledger no-false-done stress suite.

The ten-scenario contract above checks the loop’s lifecycle surface. A second Tier-A stress suite checks a different failure mode: large user intent ledgers. It instantiates ten synthetic parent ledgers, each with exactly 15 required milestone rows, for a 150-row local matrix. The rows are intentionally milestone-ledger rows, not 150 real implementation stories: the purpose is to prove that the gate can distinguish coverage, freshness, deferral, assignment, and claim-boundary states before allowing a done summary.

5.2 Reflection-loop ablation (powered: 9,240 cells)

To evaluate whether stronger control improves outcomes relative to weaker loops, we pre-register a five-arm ablation [13]. All arms used the same provider model family/model label, tool surface, tasks, and randomized run window; the exact dated provider snapshot was not recorded, which is a reproducibility limitation. Thus the control logic is the intended difference: (A1) prompt-only (one pass, no loop); (A2) naive-retry (blind retry on failure, \(R{=}3\), no gate); (A2′) compute-budgeted naive — identical to A2 but bounded by a token \(+\) wall-clock spend budget equal to A4’s per-task median (measured in pilot; \(\pm\)20% band, token binds first, hard-truncated), so it is compute-budgeted to A4’s pilot median rather than structured; (A3) review-only (A2 plus exactly one review pass using A4’s reviewer, not iterated); and (A4) the Proof-or-Stop reflection loop (plan\(\to\)execute\(\to\)review\(\to\)bounded reflection\(\to\)evidence gates\(\to\)done).

What counts as wrong.

Each programming task has two scoring surfaces. The visible acceptance test is available to the agent and is the test a weak loop can learn to satisfy. A hidden ground-truth oracle, kept out of the agent prompt and used only by the harness, decides whether the accepted artifact is actually correct. For the non-null scenarios B1–B15, the harness injects failures designed to expose this gap: an artifact may pass the visible acceptance check while still failing the hidden oracle. We score such a shipped artifact as amplified. Thus the “wrong” outcome in Fig. 5 is not a subjective review label; it is a machine-read event: visible acceptance passes, the hidden correctness oracle fails, and the arm nevertheless ships or propagates the artifact. The complement, not-amplified, means the arm either repairs the artifact or refuses to advance it.

A2′ is the pre-registered budget-capped naive control: it reduces, but does not eliminate, the raw-compute confound, so the headline comparison A4 vs A2′ cannot be read as a clean equal-spend causal estimate. Cost (model calls \(+\) tokens \(+\) wall-clock) is a primary co-metric, reported beside completion so more compute is never hidden. Each arm runs over \(24\) stratified tasks \(\times\,5\) repeats; outcomes are read objectively from git history, the process-event log, and an independently-authored, known-good-validated acceptance script — never from agent narration. For each rate \(p\) with \(n\) trials we report a Wilson 95% interval [27]

and test arm differences with a two-proportion test (Fisher’s exact [5] per scenario given small per-cell \(k\) and large expected effects), reporting effect size with CI rather than \(p\) alone. The pre-registered hypotheses are H1 (A4 not-amplified rate \(>\) A2′, compute-budgeted control), H2 (A4 completion \(\geq\) A2′ and A4 regression \(&lt;\) A2′), and H3 (A4 \(>\) A3 — does the bounded loop add value beyond a single review?). Status: powered run COMPLETE (9,240 applicable unique cells). The design starts from 5 arms \(\times\) 24 stratified tasks \(\times\) 16 scenarios \(\times\,k{=}5\); per-arm applicability gives A1 13 scenarios (1,560 cells) and A2/A2′/A3/A4 all 16 scenarios (7,680 cells), for 9,240 scored cells total (Sonnet; 0 invalid records). The pre-registered primary contrast A4 vs A2′ (compute-budgeted naive control, seeded cluster bootstrap, \(B{=}2000\)) gives H1 (§6 not-amplified) \(=+1.6\)pp, 95% CI \([0.8,2.5]\) — the CI excludes zero: the evidence-gated loop amplifies less than the compute-budgeted naive loop, and does so while spending more (A4 \(\approx\!1.2\times\) A2′ tokens), a conservative direction. H2 (completion) \(=+3.3\)pp \([0.0,10.0]\) is marginal (null-cell completion is near-ceiling for every arm). Full per-arm rates are in Table 11; the clean-task pilot (mechanism, no injection) is reported below. The deterministic execution+analysis harness is built, offline-tested, and locally 3\(\times\)2 host-verdict reviewed. The harness (in the recovery-runner, merged to Proof-or-Stop main) is the full pipeline enumerate \(\to\) run (pluggable engine) \(\to\) adjudicate \(\to\) score \(\to\) analyze: a cell-matrix driver honouring the §A applicability table, the §4.2 total-order adjudicator, harness-owned hash-checked acceptance \(+\) hidden-regression \(+\) diff-hygiene scoring, and an analysis stage that computes matched common-cell rates with the Wilson interval of Eq. (6), an A4-vs-A2′ seeded cluster bootstrap as the primary readout, one Benjamini–Hochberg FDR over the exploratory per-scenario tests, the cost co-metric, and an emitted analysis.glmm.R sensitivity script (two disjoint H1/H2 lme4::glmer models [2] over the matched corpus); the harness’s lifecycle-readiness evidence (the live-engine adapter B-8d44, self-checks, and a local review quorum) is in Appendix A. A matched-cell invariant — every per-arm estimate scores both arms over the same both-arms-have-data cell set, so no headline number can be inflated by a mismatched denominator (§8) — closes the §8 denominator-bias threat in code. The full protocol (arms, stratified corpus, per-arm injection applicability, readout, validity filters) is in Appendix A.

Cost–reliability trade-off.

Table 11 shows the main operational trade-off: stronger control reduces visible-pass/hidden-fail amplification, but it costs more tokens and time. A4 amplifies \(2/1800\) injected cases versus \(31/1800\) for the pre-registered budget-capped A2′ control (equivalently, H1 not-amplified \(+1.6\)pp [0.8,2.5]) while using 204,553 mean tokens and 81.2 s per cell, compared with 170,545 tokens and 54.8 s for A2′. This supports the narrower claim that Proof-or-Stop is a reliability-oriented control mechanism, not a free speed-up or a clean equal-spend result. Table 11 reports the pre-registered not-amplified endpoint and cost co-metrics; Fig. 5 plots the same injected B1–B15 evidence on the amplified-outcomes scale, making the rare-event A4-vs-A2′ contrast explicit.

What the ablation proves.

The powered result is a mechanism claim, not a general theorem that agents become correct. First, the enforced gate helps against the pre-registered budget-capped naive control A2′: A4 reduces amplification from \(31/1800\) to \(2/1800\) injected cells, yielding H1 not-amplified \(+1.6\)pp with a 95% cluster-bootstrap CI \([0.8,2.5]\) that excludes zero. This contrast is pre-registered but not a clean causal estimate of budgeting: A2′ realized-spend matching is coarse, A4 spends more on average, and A2′ is weaker than raw A2 in this rare-event run. Second, the A3–A4 pair is the cleanest exploratory isolation of enforcement: A3 spends nearly the same tokens as A4 (A3/A4 token ratio \(0.98\)) and uses the same one-review signal, but A3 treats the review as advisory and amplifies \(14/1800\) injected cells; A4 enforces the review gate and amplifies \(2/1800\). This enforcement-isolation contrast is less concentrated than the A2′ comparison: excluding du-duration, A3 still amplifies \(9/1725\) cells while A4 amplifies \(0/1725\) cells. Third, this powered readout measures recovery/not-amplification, not terminal stop activation: safe-stop and the unsafe-action detectors are zero in these records, so stop behavior is supported by the separate engine-contract and recovery-pilot evidence. The supported conclusion is therefore narrow: for this pre-registered coding corpus, Proof-or-Stop-style enforcement reduces visible-pass/hidden-fail error amplification relative to weaker control logic, with the strongest primary-control contrast occurring where the visible-pass/hidden-fail trap is active.

What the powered ablation instantiates.

The powered ablation instantiates the control-policy contrast over a deterministic experiment harness. It does not instantiate the full story-level materialHash/receipt-gated lifecycle for each cell. The story-level Proof-or-Stop engine tests separately validate materialHash freshness, commandSetHash binding, full-test receipts, review verdict admissibility, and the done gate; the powered ablation validates whether enforcing the review-and-redo gate reduces visible-pass/hidden-fail amplification under a fixed task/scenario matrix. These are complementary evidence objects rather than the same artifact. A future gate-grade replay should package selected powered cells as story-level materialHash/commandSetHash/receipt evidence.

Supplemental paired execution-status comparison.

As a descriptive companion to the powered control-policy result, we joined a separate executed Proof-or-Stop gated run and a no-review control run by task, scenario, and repeat over the same 1,152 cells. The no-review control reached terminal completion on \(1{,}143/1{,}152\) cells, while Proof-or-Stop admitted \(1{,}042/1{,}152\) cells after completion or recovery and safe-stopped \(110/1{,}152\) cells. Among paired cells, 106 no-review completions were not admitted by Proof-or-Stop (Table 12). Because these safe-stops were not adjudicated against hidden ground truth, we do not claim that the 106 no-review artifacts were incorrect. The supported observation is narrower: terminal completion and admissible delivery are distinct lifecycle states, consistent with the agent-as-claim framing. This is a separate execution-status matrix from the multi-model-ablation program (Phase 1; protocol incomplete) and does not extend the pre-registered §5.2 powered ablation result. Full precision and native outcome details are in Appendix B.

The difference from the safe-stop \(=0\) powered-ablation readout in Table 11 is protocol-driven rather than contradictory: in the powered matrix A4 repaired the injected visible-pass/hidden-fail cases within that harness, whereas this execution-status matrix records a safe-stop whenever the gated run’s evidence path does not admit delivery.

Supplemental token-usage readout.

The same paired matrix also provides a descriptive token-usage comparison. Under input+output token semantics, without double-counting cached-input or reasoning-output subfields, the gated run used 221,068,475 input+output tokens over 1,152 matched final rows, while the no-review control used 58,173,502 input+output tokens over the same 1,152 matched formal rows. This gives a 3.80\(\times\) input+output token-usage ratio and an incremental 162,894,973 input+output tokens. Both sides are labeled as OpenAI/GPT-family gpt-5.5 runs in the underlying artifacts; if a future validation showed a model-family mismatch, the ratio should be replaced by side-by-side provider-reported counts. This is a bundled condition comparison, not an isolated estimate of review overhead, not a dollar-cost estimate, and not a cost-benefit proof. Cell06 reports cached input separately (46,874,624 of 57,199,341 input tokens, 81.95%), while Cell03 does not expose a matching cached-input breakdown, so the ratio is not necessarily cost-proportional under provider billing. This supplemental 3.80\(\times\) token-usage ratio is not directly comparable to the approximately 1.2\(\times\) token ratio in Table 11: the powered ablation uses a different pre-registered matrix and a compute-budgeted A2′ control, while this paired readout compares a bundled gated run with a no-review control in a separate execution-status matrix.

Readout completeness and deviations.

The headline A4-vs-A2′ estimate is the in-process seeded cluster bootstrap. The pre-registered GLMM script is emitted as analysis.glmm.R (two disjoint H1/H2 lme4::glmer models [2] over the matched corpus) for external fitting, but is not used as an inferential claim in this paper; the primary inferential claim is the seeded cluster bootstrap. H3 (A4 vs A3, near-compute but not strict per-run matched: A4 not-amplified \(99.9\%\) vs A3 \(99.2\%\) at A4 \(\approx\) A3 spend) is exploratory. The secondary descriptors (uncontrolled-retries, evidence-completeness, human-intervention) and the per-category breakdown are not separately tabulated: under the single pre-registered FDR no per-scenario contrast reached the FDR threshold, and the safe-stop / event-based detectors are structurally \(0\) in these records. Data hygiene: 77 restart duplicates (identical outcomes, from the multi-day run) were de-duplicated by cell key (arm\(|\)task\(|\)scenario\(|\)repeat) to reach the \(9{,}240\) unique cells, and 24 A1 (single-shot) acceptance-fail edge cells (16 injected, 8 null/no-injection) fall outside the recovered/amplified/safe-stop classification and sit in the non-primary A1 reference arm. A4’s two amplifications both fall on a single task (du-duration); every other task is \(100\%\) not-amplified for A4. Table 13 shows the concentration explicitly. The primary effect should therefore be read as a matrix-level aggregate, not per-task dominance: Proof-or-Stop buys little on easy cells that almost never amplify, and most visibly helps on the task where the visible-pass/hidden-fail trap is active. The released records carry modelId=sonnet (the exact dated provider snapshot was not recorded in the experiment records) and leave headHash/materialHash null — the powered harness does not material-hash-gate experiment cells (distinct from the story-level evidence gate that does). Thus the scoring artifacts are mechanically reproducible from released records, but model-output replay is not provider-snapshot reproducible and these records are not lifecycle-gate-grade evidence under Eq. (2). Raw records, the tidy CSV, analysis.glmm.R, a per-scenario CSV, and scenario/task/schema dictionaries are released in experiments/powered-ablation/.

Pilot (clean-task ablation, \(n{=}9\)/arm).

As a first measurement we ran all four arms on three clean, well-specified tasks (parse-range, median, text-stats), \(k{=}3\), no injection — the deliberate complement of the §6 fault case (Table 14). All four arms completed correctly \(9/9\) (hidden ground-truth pass) in a single attempt: naive-retry never retried and bounded reflection never triggered, because there was no failure to recover from (A1\(\approx\)A2, A3\(\approx\)A4). The only separation is cost and latency — the independent review gate roughly doubles both (A4/A1 \(=2.07\times\) cost, \(2.51\times\) wall). This is the honest boundary of the loop: on easy, well-specified work the loop is pure overhead with no completion benefit; its value appears precisely under the green-but-wrong faults of §6, where the bare loop amplified \(15/15\) and the gated loop shipped \(0/15\) wrong results. The loop functions as a risk-mitigation mechanism: it adds overhead on clean tasks, but becomes valuable when the visible test is green and the artifact is wrong. Caveat: \(n{=}9\)/arm, three small tasks, one model; with \(9/9\) the completion CI is wide (\([0.70,1.0]\)), so this bounds completion at “no observed failures,” not a powered equality — the cost/latency ladder is the robust signal; the powered fault-bearing study (H1–H3) is now complete (Table 11: H1 \(+1.6\)pp [0.8,2.5], CI excluding 0).

6 Recovery under Injected Failure

To evaluate behavior under injected failures, we separate the Tier-A contract result from comparative recovery measurements. The engine contract demonstrates that the loop can stop, escalate, and repair; the empirical question is the rate at which it does so under realistic faults. We pre-register fifteen deliberate failure injections (Table 17), each run under {naive-retry loop, Proof-or-Stop loop} (optionally a review-only arm) with \(k\geq 3\) repeats. Each injection has an objective readout derived from the final diff, the process-event log, or the gate decisions — e.g. “does the final diff contain the out-of-scope file?”, “did the loop stop after \(N\) no-progress iterations or spin forever?”. The deliverable is, per scenario, “Proof-or-Stop loop contains/recovers \(X\%\) vs naive \(Y\%\), \(\Delta\) with 95% CI” (Eq. (6)). We deliberately drop injections that merely re-assert the Tier-A contract checks, keeping the net-new empirical scenarios. Status: powered run COMPLETE (9,240 cells). Over the full matrix, the evidence-gated loop A4 is not-amplified \(99.9\%\) [99.6,100] vs the compute-budgeted naive loop A2′ \(98.3\%\) [97.6,98.8] (primary H1 \(=+1.6\)pp [0.8,2.5], CI excluding 0; Table 11). Amplification is rare and spread thinly across scenarios (A4 \(=2\), A2′ \(=31\) events over B1–B15), so the powered run contributes statistical power over the full matrix. It complements the discrimination-cell pilot below, which isolates the mechanism with a large effect on selected green-but-wrong cells. An exploratory single-agent probe over all fifteen injections (Table 17, last column) illustrates the targeted failure mode: the bare agent amplified on 5/15 (e.g. garbage-fix, delete-critical, destructive-migration), recovered on 6, and safe-stopped on 4 (\(n{=}1\) per scenario, no arm comparison—illustrative only, not the powered result, which is now in Table 11).

The pilot separates loop-fidelity levels before the full lifecycle harness: A2′ is a compute-budgeted bare loop, A4-C is a single independent review gate, and A4b-B is a B-fidelity proxy of the A4 loop used to isolate the block\(\to\)revise\(\to\)re-review mechanism.

For the pilot, let \(A_{j}\) denote visible-acceptance pass, \(G_{j}\) hidden ground-truth pass, and \(S_{j}\) whether the arm ships the final artifact (for A2′, the bare loop ships by construction; for gated arms, \(S_{j}\) is the final independent-review ship verdict). We score each run by

The non-definitional discrimination cells are exactly \(A_{j}\land\neg G_{j}\): the visible test is green, but the artifact is wrong under hidden ground truth, so only an independent gate can prevent amplification.

In this pilot, the loop is not free; under green-but-wrong faults, added evidence and review fidelity act as a risk-mitigation mechanism, moving outcomes from amplification to safe-stop to bounded repair.

Pilot (verified proof-of-mechanism, \(n{=}3\) per task-cell, three tasks).

A pilot confirms the measurement pipeline runs end-to-end and exercises the thesis-shaped differential at increasing difficulty (Table 15; Fig. 6). Early delete/corrupt cells verified the classifier and runner, but their differential is partly definitional: A4 safe-stops when acceptance is not met, while A2′ ships whatever it has. The non-definitional signal comes from the \(A_{j}\land\neg G_{j}\) cells in Eq. (7). Across parse-range, median, and text-stats, the injected artifacts pass visible acceptance while failing hidden ground truth. A2′ ships these wrong artifacts 15/15 (amplified); A4-C catches them and refuses to ship 15/15 (safe-stop); A4b-B consumes the same review signal through bounded reflection and repairs them 15/15 (recovered-to-green). The subtle parse-range defect is a complete plausible implementation whose falsy guard if(!n) wrongly rejects 0; the median subtle defect returns the lower middle element rather than the average for even-length arrays; the text-stats subtle defect is buried in a 63-line multi-helper artifact. Captured reviewer reasoning names these defects and their fixes.

Separate V3/V4 data/code audits verified that A4b-B recovery is not a classifier artifact: all 15 A4b-B runs have groundTruthPass=true, final reviewer ship, and reviewRounds>=1; in the runner, a review round increments only after a reviewer block, while recovered-to-green requires a final shipped artifact that passes hidden ground truth. Thus the key signal is the A4-C\(\to\)A4b-B step: the caught fault becomes a repair. Honest caveats: still three tasks, \(n{=}3\) per task-cell, one model, a B-fidelity bounded-reflection proxy rather than the full Proof-or-Stop lifecycle, artifacts still small enough to fit in the reviewer prompt, and no observed fault that exceeded the two-review-round cap. We report this as an independently verified proof-of-mechanism and directional shape; the powered run (stratified corpus, full A4 fidelity, 9,240 cells) is now complete and reported in Table 11 (primary H1 \(+1.6\)pp [0.8,2.5], CI excluding 0).

7 Host-Neutral Transfer

Host-neutrality, in our framing, is an evidence property: a unit of work is portable because it is git-native, and a cross-host verdict is admissible only if its receipt’s materialHash matches the current code (Eq. (2)). No new wire protocol is required; the assurance travels with the artifact. Host identity affects provenance and independence checks, but not the gate semantics for admissibility: the same freshness, binding, and receipt predicates apply whether the claim came from Codex, Claude, another coding-agent host, or a future host.

Git-native handoff (architecture).

A handoff pack stores \(\langle\textsf{baseSha},\textsf{headSha}\rangle\), the canonical story, and the allowed paths — not the worktree (Fig. 7). Story metadata and code are committed to the branch and pushed to a shared remote at checkpoint granularity. Machine B does git fetch \(\to\) reconstruct-worktree \(\to\) resume, transferring git deltas plus a small JSON rather than a filesystem image. The takeover host is bound by a claim boundary: no auto-merge, no evidence submission, no production-done; any verdict it produces is admissible only under Eq. (2).

What is verified.

Four safety mechanisms are verified by tests: a takeover host attempting auto-merge / evidence-submit / done is blocked (HN-7); a worktree ahead of its mirror raises a stale-phase warning (HN-9); a handoff to a host missing a capability surfaces a typed capability delta (HN-5); and with no real second host the system records degraded-single-host as local-only evidence rather than spoofing a quorum (HN-10, Eq. (5)). The headline cross-machine resume (HN-2) is also verified by a deterministic demonstration: machine A commits an in-flight story to a branch and pushes it to a bare remote; machine B — with no access to A’s filesystem — does a fresh clone and reconstructs the worktree from git alone, then resumes and continues. The reconstruction is verified to be exact: B’s HEAD and tree content-hash equal A’s; only git-tracked deltas plus a small pack transfer (a 2 MB gitignored bulk artifact does not move; the handoff pack is \(\approx\)9.7 KB, \(&lt;0.5\%\) of the worktree); the resume projection recovers the correct story; and B advances it by exactly one commit on top of A’s HEAD. In other words, the work outlives the dead host. HN-3 (the resume carries the canonical story + evidence refs and lineage, not raw context, and never auto-refreshes evidence or marks unsupported work done) is verified by the handoff smoke’s resume-projection assertions.

What remains pending.

The HN-2 result above is a single-story proof-of-mechanism; a broader powered study (many stories, varied worktree sizes, two physical machines) remains pending. Because transfer is git-native, the mechanism is already provable with one host on two worktrees and a bare remote, with no live cross-vendor dispatch.

What is gated.

The strong claim — a single change reviewed by genuinely distinct vendor hosts forming a verdict quorum, with fresh local receipts and provenance that reconstructs who-did-what across a host chain (HN-1/4/6/8) — requires real cross-vendor execution plus current material-hash-bound verdicts. Live cross-host execution has been exercised; the remaining blocker is the powered independent-host campaign. We therefore gated this claim and defer it (§12).

Operational Tier-C receipt batch.

Separately, the operated system preserves a batch of provider-execution receipt-verification stories as audit evidence: at the time of writing, 25 Tier-C trials remain tracked individually (22 Claude-side, 2 Codex-side, 1 end-to-end). We use this batch only to support a narrow claim: live provider-execution receipt exercises exist and are preserved without upgrading local evidence into strong host-neutral completion. It is therefore evidence of receipt-boundary discipline and no-overclaim behavior, not a powered cross-host success-rate estimate.

8 Self-Application and Audit

To assess operated use, we analyze the system’s self-application corpus. Proof-or-Stop was built through its own gated lifecycle, which provides a direct operating record and an acknowledged source of bias (§11). All figures below are mechanically extracted (Python) from the live lifecycle metadata and git history — no hand-transcription — and reproduced by an independently written re-extraction script. The empirical question is whether the independent-adversarial-review layer catches correctness defects that a single-pass author with passing smoke tests would have shipped under a bare host-agent workflow (Table 4).

Corpus.

The corpus (excluding one standing meta-audit container) is 565 dev stories / 1007 review findings, of which 94.8% are resolved (Table 18). The extraction was run on 2026-06-23 at Proof-or-Stop head 8ee771f1c; because Proof-or-Stop is self-hosted and still under active development, the absolute counts will continue to grow. The severity shape is load-bearing and stable: high dominates (\(\approx\)51%), critical is rare (\(\approx\)1%). Earlier frozen snapshots and the current live extraction reproduce the same structural claims (Appendix C). Of the 518 stories carried to done, 431 (429 distinct) additionally carry an explicit, independently git-verifiable merge: B- branch-merge commit on the development repo’s main (2026-04-14 onward; the earliest bootstrap-era stories predate that workflow). Because the public repo is a clean-slate export, this merge trail is frozen (redacted to sha/date/story-id) in evidence/orchestrate-story-merges.tsv.

Division of labor across review lanes.

Splitting the same 2026-06-23 corpus (Table 18) by review lane — merging the historical koala-/lattice- reviewer rename — shows the lanes are not redundant; each occupies a distinct severity niche (Table 19). The quality lane carries the volume (350 findings, 35% of the corpus) but skews medium (39% high/critical); the test-coverage lane, which audits the intent\(\leftrightarrow\)evidence binding, has the highest high/critical density (70%); and the smaller concept (design-completeness) lane holds 10 of the 14 critical findings. This is the empirical content behind the review/test-trust contrast in Table 4: the observed lane distributions are consistent with complementary reviewer specialization: different lanes filed different severity profiles and defect classes. Controlled lane ablation is required to estimate the marginal contribution of removing any one lane (§12). The cross-vendor row uses the newer 2026-07-02 high/critical-only refresh because the paper’s cross-vendor claim is about load-bearing review failures rather than all-severity lane volume.

Review catches what the author’s tests miss.

The headline measurement: on a curated deep set of 12 stories with 28 review findings, 26 of 28 (93%) are smoke_would_miss — the author’s own smoke/test was passing when an independent reviewer filed the finding (Fig. 8; smoke_would_miss is a reviewer-judgement label, §11). The deep set classifies as 3 production bugs, 3 logic defects, 14 test-coverage gaps, and 8 documentation-accuracy findings; every story required a second find-fix-re-review round, and 9 of 12 required an escalation quorum (7 degraded single-host, 2 full 3\(\times\)2). A fix commit stales its round (the round’s materialHash changes, Eq. (2)), rolling the story back to a fresh, evidence-bound re-review, so a defect cannot be silently patched. This is selection-conditioned evidence, not a corpus-wide base rate: most rows are coverage or documentation/claim mismatches, while the six behavior-changing production/logic defects are separated as exhibits below. The empirical content is still the problem in §2: a green pipeline can coexist with defects that require independent evidence review to surface.

Six correctness exhibits.

Table 20 lists six findings that were real defects with confirmed fix commits — including a production bug whose guard silently never fired because the author’s smoke always injected the environment that masked it. These are not style nits; they are behavior-changing defects that passed the author’s tests.

Cross-vendor review case studies.

The reviewer lanes above run on the same model family as the author; selected high-risk stories show what a different-vendor second host can add. In an offline signed-receipt verifier, same-vendor lanes filed only low/medium nits, while an independent Codex host-2 reviewer found the load-bearing defects: a critical signature bypass caused by canonicalization dropping JSON null, plus two high findings around pre-verification field use and failing-receipt acceptance. In the gate-strength contract, the same host-2 reviewer found that catch rate was gameable, a “spec-aware” reviewer was really an oracle over harness labels, and the result digest omitted per-probe justification. All findings in these selected cases were fixed and re-verified cross-host before done. We report them as existence proofs, not rates: cross-vendor review was invoked selectively on high-risk stories, so the corpus cannot support an unbiased marginal-finding rate (§12).

The sharpest case is the §5.2 ablation analysis itself — the code that computes this paper’s main empirical result. Same-vendor lanes passed the statistics, but the independent Codex host-2 caught denominator bias in the headline rates, cluster bootstrap, completion table, per-scenario tests, and emitted GLMM sensitivity. The fix is the matched-cell invariant of §5.2: every per-arm estimate scores both arms over the same both-arms-have-data cell set. This is the paper’s strongest cross-vendor lesson: independent-vendor review is most useful on artifacts that look statistically plausible and are therefore easiest for a same-vendor panel to ratify.

Cross-vendor review protected the measurement instrument.

The 2026-07-02 cross-vendor refresh is the paper’s main cross-vendor exhibit (Fig. 9). It records 68 Codex-authored high/critical catches across 26 stories, all resolved (2 critical, 66 high; categories: 48 adversarial, 17 missing-case, 3 edge). The strongest post-2026-06-23 additions were on our own §6 measurement tooling before the powered run: the independent Codex host-2 review found that a hidden-regression baseline failed open when ground truth was missing or broken, that an out-of-workspace write carrying a captured tool event could be scored recovered rather than amplified, and that a corpus anti-gaming self-check was itself tamperable (B-8d44, B-ccde, B-e67f). All were fixed before the powered ablation was run. We treat the 68 rows as self-application findings on the experiment’s own instrument, not as a generic product-defect rate: they show exactly the failure mode the paper targets, a plausible test-passing measurement artifact caught by independent evidence review.

Metadata-proof spoofing case studies.

The same discipline surfaced a second class of “lying evidence” failures in a sibling Authority Server codebase: proof-looking fields stored in client-writable metadata. The 565-story / 1007-finding Proof-or-Stop corpus establishes operated scale; these selected exhibits establish concrete spoofing surfaces. They do not prove host intent, and they are not a corpus-wide rate estimate. Instead, they reinforce the boundary in Eq. (2): metadata is admissible only when the server, not the caller, owns its production and validation. Table 21 lists the inspected cases; the B-e9cb worktree itself was cleaned after DONE, so the durable evidence is the merge commit and story metadata on Authority main.

Finding-status integrity.

Of 1007 findings, 955 are resolved, 41 open, 11 dismissed. All 41 open findings sit on already-done stories, by design: the done gate is severity- and round-graded (critical always blocks; medium becomes advisory in round \(\geq 2\), high in round \(\geq 3\); low is always advisory), so a real finding filed late can remain open while the story still reaches done as deferred/advisory. Two readings are both true and both stated: (i) transparency — the audit trail records exactly what is unresolved on a done story, which direct single-pass development has no ledger for; and (ii) limitation — “done” does not mean “zero known issues.” The deep 28-finding set, by contrast, had all findings resolved before done.

Dogfooding friction — the tool gating its own author.

Building Proof-or-Stop under its own lifecycle surfaced eight recurring frictions, which we classify honestly. Only two were genuine defects in Proof-or-Stop’s own tooling — a scope-freeze keyword matcher whose altitude was too coarse (it substring-matched an excluded keyword inside descriptive prose), and a fresh-worktree bootstrap that lacked build artifacts — and both were caught precisely because the tool gated its own development, the strongest dogfooding result. Three more were the system correctly refusing to lower its own assurance bar: a degraded-single-host escalation honestly remaining local-only in a solo environment (Eq. (5)), an English-only artifact gate, and a reviewer rejecting a generic catch-all verification command as an evidence-correspondence gap even when the claim was factually true. The remaining two were concurrency artifacts of multiple sessions sharing the main line (an evidence-freshness re-stamp and a main-merge materialHash race at done) — exactly the freshness conjunct of Eq. (2) firing under concurrent merges, as we also observed in §4. The point is methodological: a system that gates its author is forced to either fix a real bug or visibly refuse to weaken its own gate; neither failure mode can be silently papered over.

Claim-boundary baselines.

Proof-or-Stop does not let capability claims float above evidence. Its baseline registry is therefore used first as a claim-boundary contract, not as a performance headline: a stronger claim must name the baseline family, required artifacts, and gate consumer that would make it admissible; otherwise the claim remains pre-registered, advisory, or gated. The current implementation contains 35 formal baselines across four claim families, plus an 11-item legacy development baseline registry with a 6-item minimum suite. The inventory in Table 22 is evidence that the system has explicit boundaries for what it may say, not evidence that every boundary has been empirically crossed. This registry is not evidence of empirical superiority; it is evidence that claim language is mechanically bounded.

9 Experience Reuse and Honest Metrics

Proof-or-Stop includes an advisory experience layer: a deterministic, lineage-backed cache that turns verified past findings into hints. This layer demonstrates the spine’s boundary rather than extending the proof base: it influences attention, not decisions, is marked gateEvidence:false, is excluded from materialHash, and never enters the review prompt digest. The implementation validates that these hints are consumed at lifecycle entrypoints while remaining unable to satisfy review, validation, delivery, or done gates (Appendix F).

The operated corpus contains real recurrence substrate: 989 of 1007 findings carry curated signatures across 211 canonical area|failureMode classes, with retrodictive recall 0.700 and held-out forward recurrence 77.1%. We report this as an observational fact about recurring defect classes, not as evidence that surfacing hints improves review. A pre-registered ON/OFF pilot validated the causal-test machinery but stopped at its pilot gate: 90 arm-runs showed a control-arm in-store defect baseline of only \(1/30=0.033\), far below the planning band, so the powered study was refused by the pre-registered sizing rule. The supported claim is therefore narrow: prior lessons can be surfaced without becoming proof, and the system refuses to upgrade an underpowered advisory-memory result into a causal capability claim.

10 Related Work

Durable systems preserve state; coordination protocols move messages; benchmarks score task success. Proof-or-Stop instead decides which lifecycle claims are admissible. The systems below therefore compose with Proof-or-Stop, but they do not replace its evidence-admission rule.

Durable / resumable execution

Cross-vendor coordination

[6, 1, 16] (agent-to-agent and tool/context protocols) routes and delegates tasks across vendors. Delta: these are communication protocols; ours is an assurance layer — a cross-host verdict is admissible only if its receipt’s materialHash matches. The two compose: Proof-or-Stop can run over such a transport.

Multi-agent orchestration and agent frameworks

[29, 16] make it easier to assemble specialist agents, human-in-the-loop turns, and tool-using workflows. Delta: Proof-or-Stop is not a conversation pattern or agent framework; it is the assurance layer that decides which claims from those agents become admissible lifecycle evidence. Agent frameworks orchestrate agents; Proof-or-Stop controls which agent claims a lifecycle is allowed to act on.

Agentic software-engineering systems and benchmarks

Self-reflection and iterative refinement

Assurance roots: proof, monitoring, claims, and provenance

[15, 7, 18, 28, 23, 25, 21] connect Proof-or-Stop to older assurance traditions. Proof-carrying code checks machine-readable evidence before code is executed; runtime verification monitors executions against specifications; assurance cases and Goal Structuring Notation structure claims, arguments, and evidence; and provenance / attestation systems such as W3C PROV, SLSA, and in-toto bind artifacts to production histories. Delta: Proof-or-Stop differs in its unit of control. It gates lifecycle claims emitted during autonomous coding work — reviewed, tested, done, ready-to-merge, host verdict, or scope-complete. Such claims may advance lifecycle state only when fresh, tracked-source-state-bound, mechanically verifiable evidence satisfies the relevant gate predicate.

Evidence-driven release gates / deterministic verification loops

aggregate verdicts into promote/hold/rollback. Delta: we bind each evidence item to materialHash/headHash/storyFilesHash plus authenticated integrity digests and a receipt identity, lifecycle-wide and operated on a real self-hosted system — not one release decision on coarse signals.

Quorum-certified multi-agent verdicts

(Byzantine-resilient commitments, threshold oracles). Delta: our quorum is freshness-bound to code state (invalid if materialHash drifts) inside a development lifecycle, and honestly degrades to single-host (Eq. (5)) rather than spoofing a quorum.

LLM critics and cross-context review

[12] (parallel specialist reviewers, separate production/review sessions). Delta and caveat: we use cross-vendor diversity, but because heterogeneous panels can underperform their best member, we present our cross-host catches as a case study of genuine vendor diversity, not a consensus-voting claim (§11).

Concurrent evidence-gated agentic frameworks (2026)

[9, 30] are the closest contemporaneous work, independently arriving at the same core move: gate an agent’s claims on evidence rather than on the agent’s say-so. Agentic Agile-V [9] proposes a conversation-to-contract gate that separates exploratory dialogue from implementation, a taxonomy of minimum input artifacts, risk-adaptive feature/bug-fix/testing workflows, and an evidence-bundle acceptance model for agent-generated artifacts — closely mirroring our INIT scope-freeze, structured PLAN artifacts, risk-adaptive gates, and evidence admission. Delta: Agile-V is a process and acceptance model; we give evidence admissibility a formal, machine-enforced definition (Eq. (2)) in which each item is bound to the exact tracked source identity (materialHash/headHash/storyFilesHash) plus authenticated integrity digests and a receipt, is invalidated by staleness, and is resisted even when it looks like a valid proof (the metadata-spoofing exhibits, §8). ResearchLoop [30], though aimed at AI-assisted research rather than software, is structurally the nearest neighbor: an evidence-gated control plane with a claim ledger, claim-admission gates, a repository-backed runtime, and a self-hosting evaluation — the same architecture as our gate-consumable evidence, claim-boundary registry, git-native durable state, and self-application (§8). Delta: our binding is to a continuously-changing code state, so freshness (a materialHash drift invalidating an otherwise-valid claim) and honest quorum degradation (Eq. (5)) are first-class, and a prohibited-wording guard blocks over-claiming by construction. That two independent 2026 systems, in different domains, converge on evidence-gated control planes strengthens the case that this is the right abstraction for trustworthy agentic work.

11 Threats to Validity

Self-built / self-reviewed corpus. All stories were built by LLM agents under Proof-or-Stop, and findings are LLM-reviewer-generated; the corpus is not an independent population. Mitigations: objective, audit-derived outcomes; an independent re-extraction (Appendix C); a self-enforced prohibited-wording guard that blocks over-claiming.

Reviewer-judgement labels. smoke_would_miss and classification are reviewer-style judgements, not ground truth. The hard per-row facts are: the finding exists, was filed by a named independent reviewer, the story’s verification was passing when filed, and a subsequent fix commit resolved it.

Curated deep-set selection. The 12-story / 28-finding deep set is a curated audit slice, not a random sample of the 565-story corpus. Its 93% smoke_would_miss rate should be read as evidence that such failures occur under green local checks, not as the corpus-wide prevalence of behavior-changing bugs. Most rows are coverage or documentation/claim mismatches; the six production/logic defects are reported separately as correctness exhibits.

Small N for genuine cross-host review. The systematic cross-vendor yield is Tier-C and unmeasured here; the cross-host catches we report are concrete but selection-described. The 2026-07-02 refresh reported in §8 records 68 high/critical cross-host findings across 26 stories, all resolved, supporting motivation but not establishing a base rate. Likewise, the separate Tier-C provider-execution receipt batch is reported as grouped operational evidence (25 tracked trials), not as a powered rate claim.

Observational experience reuse. Eq. (8) is observational; the causal A/B (Eq. (9)) is under-powered. The present evidence does not establish causal model improvement from experience reuse.

Counterfactual asymmetry. We observe what Proof-or-Stop’s review caught, not what a direct single-pass run on the same tasks would have shipped. A small parallel-vs-sequential development pilot is a reported null result (no measurable time benefit, \(\approx\)1.8\(\times\) cost, equal self-test quality) and appears in Appendix G as a boundary case, not as support for the thesis. An independent adversarial check overturned its first over-stated headline, illustrating the same claim-boundary discipline.

Supplemental execution-status comparison. The Cell03/Cell06 paired matrix is descriptive: it shows that terminal completion and Proof-or-Stop delivery admission can diverge on the same cell keys. It is not hidden-oracle adjudicated, does not prove that every safe-stop was a true positive, and does not upgrade the powered ablation into a completed multi-model generalization. It is reported as lifecycle-status evidence, not as an accuracy or cross-vendor effect estimate.

Corpus scale. The corpus is far smaller than population studies of agentic PRs; we trade scale for end-to-end audit depth and do not generalize beyond a gated, self-hosted setting.

12 Future Work

Future work has several directions. (1) Tier-B runs: the pre-registered comparative ablation (§5.2) is now powered and complete; the remaining Tier-B work is to scale the verified recovery pilot (§6) to a fully powered stratified injection study in its own right, and scale the verified git-native handoff demonstration (§7) to a multi-story, varied-worktree study, reporting rates with CIs (Eq. (6)). A related sub-study should quantify the cross-vendor review marginal-finding rate — an independent-vendor host-2 run on a random or complete story sample with systematic finding records — which the selectively-invoked deployment in §8 cannot estimate without bias. (1b) Real-work green-but-wrong base rate: estimate how often visible acceptance passes while an independent hidden oracle fails in non-injected development work. The powered fault-injection result measures risk mitigation conditional on a visible-pass/hidden-fail trap; the real-work base rate is the missing denominator for cost-benefit claims about when the overhead is worth paying. (1c) Gate-grade replay: repackage selected powered-ablation cells — for example A4’s two amplified cells, representative A2′ amplified cells, and representative A4 repaired cells — as story-level materialHash/commandSetHash/receipt evidence. This would connect the powered control readout directly to the full materialHash-gated lifecycle path without changing the present claim that the powered ablation itself is a control-policy experiment. (2) Tier-C strong host-neutral: run the powered independent-host campaign so cross-vendor verdicts form a fresh material-hash-bound quorum (Eq. (4) with local receipts); live cross-host execution has been exercised, so this is gated mainly on scale and independence rather than a remote proof service. (3) A powered causal A/B for the experience layer (Eq. (9)) with a formal two-proportion test. Until those land, we claim only the verified spine, the engine contract, the recovery pilot, the powered comparative ablation, the audited corpus, and the claim-boundary baseline inventory. External benchmark suites, multi-model generalization, and cost/reliability tradeoff studies are future extensions of this claim set, not current results claimed here. The supplemental Cell03/Cell06 execution-status matrix is a Phase 1 descriptive artifact from that program; completing the remaining cross-review cells, Phase 2 decision, and powered matrix is future work before any multi-model effect claim. It supplies a paired input+output-token numerator and a delivery-status divergence count, but still not the real-work green-but-wrong denominator: the 106 no-review completions not admitted by the gated run were not hidden-oracle adjudicated, so this evidence cannot yet say how many wrong deliveries the extra token usage avoided. PR-less auto-merge is also a deployment claim rather than a current result: it requires a GitHub App or Action that consumes the done certificate, branch-protection integration, stale/forged/wrong-certificate rejection tests, multi-story independent-host validation, path-specific merge policies, override and rollback audit trails, and cross-repository replication.

(4) Future domain packages: instantiate Proof-or-Stop Lifecycle Control in dry computational workflows where lifecycle claims, admissible evidence, gates, and transitions can be defined without changing the control abstraction. The current repository includes non-claiming schema smoke tests for PINN- and Quantum-style evidence bundles, but these are not current-result evidence and do not validate PDE correctness, quantum theory, hardware, solver quality, or scientific correctness. A credible cross-domain result requires a domain-specific evidence package, pre-registered task suite, independent validators, and domain-appropriate correctness or reproducibility criteria.

13 Conclusion

Proof-or-Stop Lifecycle Control was developed in this work as an evidence-gated method for deciding when autonomous-agent lifecycle claims may advance state. The method formalizes claim admissibility, instantiates it in an operated software lifecycle, and treats agent outputs as claims that must be supported by fresh, tracked-source-state-bound evidence before review, test, done, or merge-relevant transitions are allowed to proceed. The central shift is from treating agent output as lifecycle state to agent-as-claim lifecycle control: agent outputs may initiate claims, but admitted evidence advances state.

It was found that the implemented gates did not advance the tested lifecycle claims on self-report in the reported suites. The unattended-loop contract passed 10/10 scenarios with zero false-done; local-key receipt bundles rejected 18 tamper classes with zero false accepts in the tested suite; and the operated corpus comprised 565 stories and 1007 review findings, with 94.8% resolved. In the curated deep set, 26 of 28 findings (93%) were filed whilst the author’s own tests were passing, and the refreshed cross-vendor exhibit contained 68 high/critical independent-review findings over the paper’s own evidence machinery. In the powered 9,240-cell ablation, the pre-registered A4-vs-A2′ contrast reduced visible-pass/hidden-fail amplification from \(31/1800\) to \(2/1800\) injected cells (+1.6pp not-amplified, 95% CI \([0.8,2.5]\)).

These results indicate that the mechanism is not simply additional retry or additional review. The near-compute A3–A4 contrast is the clearest mechanism isolation: A3 used the same reviewer signal as advice and amplified \(14/1800\) injected cells, whereas A4 converted that signal into an enforced lifecycle gate and amplified \(2/1800\). This is consistent with the intended mechanism: the reviewer verdict is converted from an advisory observation into a state-transition condition. The present evidence is bounded to one model family, 24 ablation tasks, and a self-hosted corpus, and cross-domain, multi-model, external-benchmark, and strong independent-host generalization remain future work. Within those boundaries, Proof-or-Stop provides a practical route for making autonomous software lifecycles act on admissible evidence rather than unsupported claims.

Reproducibility

All quantitative figures are mechanically extracted from lifecycle metadata and git history rather than hand-transcribed. The public Proof-or-Stop open-source address links to the implementation repository, verifier tests, and re-extraction entrypoint. Sanitized experiment records, corpus and deep-finding tables, experiment summaries, and figure-generation sources are released only through the arXiv/release artifact bundle, not through the private paper authoring workspace:

https://github.com/Proof-or-Stop

The arXiv v1 implementation artifact corresponds to the repository tag arxiv-v1, or to the commit hash recorded in repository release notes if that tag is not present. Reproduction commands are in Appendix E. Two further corpus figures — a combined severity/classification chart and a baseline learning curve — are included in the release artifact but not embedded here, to avoid redundancy with Table 18 and Fig. 8.

References

- [1] (2024) Model context protocol (mcp). Note: https://modelcontextprotocol.ioAccessed: 2 July 2026 Cited by: §10.
- [2] (2015) Fitting linear mixed-effects models using lme4. Journal of Statistical Software 67 (1), pp. 1–48. External Links: Document Cited by: §5.2, §5.2.
- [3] (1995) Controlling the false discovery rate: a practical and powerful approach to multiple testing. Journal of the Royal Statistical Society: Series B 57 (1), pp. 289–300. External Links: Document Cited by: §5.2.
- [4] (1979) Bootstrap methods: another look at the jackknife. The Annals of Statistics 7 (1), pp. 1–26. External Links: Document Cited by: §5.2.
- [5] (1922) On the interpretation of Chi-Square from contingency tables, and the calculation of P. Journal of the Royal Statistical Society 85 (1), pp. 87–94. External Links: Document Cited by: §5.2.
- [6] (2025) Agent2Agent (a2a) protocol. Note: https://a2a-protocol.orgCross-vendor agent interoperability. Google announcement: 9 April 2025; Linux Foundation project launch: 23 June 2025. Accessed: 2 July 2026 Cited by: §10.
- [7] (2004) An overview of the runtime verification tool Java PathExplorer. Formal Methods in System Design 24 (2), pp. 189–215. External Links: Document Cited by: §10.
- [8] (2024) SWE-bench: can language models resolve real-world github issues?. In International Conference on Learning Representations, Note: arXiv:2310.06770. https://arxiv.org/abs/2310.06770 Cited by: §10.
- [9] (2026) Agentic agile-v: from vibe coding to verified engineering in software and hardware development. arXiv preprint arXiv:2605.20456. Note: https://arxiv.org/abs/2605.20456 Cited by: §10.
- [10] (2024) LangGraph: stateful, resumable agent graphs. Note: https://langchain-ai.github.io/langgraph/Accessed: 2 July 2026 Cited by: §10.
- [11] (2023) Self-refine: iterative refinement with self-feedback. In Advances in Neural Information Processing Systems, Note: arXiv:2303.17651. https://arxiv.org/abs/2303.17651 Cited by: §10.
- [12] (2024) LLM critics help catch LLM bugs. Note: arXiv preprint arXiv:2407.00215. https://arxiv.org/abs/2407.00215 Cited by: §10.
- [13] (2019) Ablation studies in artificial neural networks. arXiv prepr
