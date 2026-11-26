---
title: "GUARD: Stabilizing Recursive Self-Improvement with Regret Guidance"
type: "raw-source"
url: "https://arxiv.org/html/2611.23476v1"
author: "Minghe Zhang Affiliation Google Cloud Affiliation Equal contribution"
publication: "arXiv"
published: "2026-01-31"
archived: "2026-11-26T04:01:47Z"
---

> [!quote] Original source
> **Author(s):** Minghe Zhang Affiliation Google Cloud Affiliation Equal contribution  
> **Title:** GUARD: Stabilizing Recursive Self-Improvement with Regret Guidance  
> **Published in:** arXiv  
> **Date:** 2026-01-31  
> **Original:** <https://arxiv.org/html/2611.23476v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-guard-stabilizing-recursive-self-improvement-with-regret-guidance|Source note]]
Themes: [[Loop engineering]]
Why it was archived: Answers question 0: how judge-vs-oracle selection regret in harness evolution translates into a concrete selection method.

## Archived text

GUARD: Stabilizing Recursive Self-Improvement with Regret Guidance

Abstract

Autonomous AI agents pair a frozen base model with an editable harness of prompts, skills, tool rules, and memory. Recursive self-improvement (RSI) adapts this harness from experience without weight updates, yet self-editing without external graders often backfires: reflection and scalar scores conflate what an edit newly broke with what remains unsolved, causing local regressions, skill forgetting, and memory bloat. We introduce GUARD (Grader-free Unsupervised Environment Design [UED] with Adaptive Rule Distillation), a closed-loop framework for reference-free continual harness evolution. Our key insight is to decompose each task into pre-execution self-checks and guide harness updates via directional regret. Each round grades trajectories against these checks, pinning mastered rules while prioritizing newly broken behaviors, and selects among parallel candidate edits by critic-free group-relative fitness. A Soft-HURT gate then promotes an edit only when gains outweigh regressions, scoping specialized fixes to prevent over-triggering and guaranteeing non-regression on its gated buffer. At test time, one frozen harness runs in a single pass. Across benchmarks on memory, skill evolution, continual task streams, and domain reasoning, GUARD consistently improves performance without catastrophic forgetting or memory pollution while substantially cutting deployment token usage.

1 Introduction

Modern language model agents combine a frozen base model with a surrounding harness of prompts, reusable skills, tool interfaces, memory, and control logic [31, 42, 20, 45]. In practice, this harness decides whether the same model checks the right state before acting, calls tools with valid arguments, recovers from failed commands, and carries useful rules across sessions [52, 40]. Much recent progress in deployed agents comes from harness engineering, yet tuning harnesses by hand scales poorly: engineers can inspect only a small slice of failed runs, and fixed designs quickly go stale as tools, schemas, and user workflows change [5, 49]. Recursive self-improvement (RSI) aims to automate this loop by turning past experience into persistent edits that improve future runs [54, 38, 44, 26]. Because frontier models often sit behind black-box APIs with frozen weights and open-world tasks rarely provide ground-truth rewards for weight-space reinforcement learning [60, 62, 13, 46], treating the editable harness as a non-parametric policy around the frozen model offers a practical, inspectable way to improve agents after deployment [23, 36].

Early automated methods search over prompts or agent code offline using labeled training splits before deployment [18, 12, 55, 58, 20]. The resulting static harnesses struggle when test-time tasks shift. Newer approaches regularize offline search for out-of-distribution generalization [45], probe per-task harnesses online while saving reusable lessons [49], or append reflections and skills across episodes [59, 30, 50, 1]. Yet continually updating a single persistent harness across rounds without reference answers or external graders often degrades performance over time [5]. Because every edit changes subsequent rollouts, free-form reflection and scalar task scores mix two distinct failure signals: behaviors the latest edit newly broke and capability gaps the agent still has not solved. Mixing these signals across rounds causes three failure modes: local overfitting (over-triggering), where a broad rule written for recent failures breaks tasks that already worked; catastrophic forgetting, where shifts in workflow, topic, or domain overwrite earlier skills [5]; and memory pollution, where unverified additions accumulate stale or conflicting rules that bloat the prompt. Over multiple rounds, self-editing can leave an agent worse than its starting point (Figure 1).

Central Question. How can an autonomous agent continually improve its persistent harness in a reference-free setting without interfering with or catastrophically forgetting previously learned skills?

We address this challenge by casting harness adaptation around a frozen model as gradient-free policy optimization in text space, guided by two ideas from reinforcement learning: curriculum regret from unsupervised environment design (UED) [7, 14, 15, 35] and critic-free group-relative scoring from Group Relative Policy Optimization (GRPO) [37, 3]. We never update the model weights or train a value critic: the harness is the only part of the policy that changes (§2). We implement this approach in GUARD (Grader-free UED with Adaptive Rule Distillation; Figure 2, §4). Before executing a task, GUARD compiles the task prompt and tool schema into a fixed checklist of atomic binary checks (§4.1) and grades completed runs with a two-layer (sandbox execution plus semantic trace) self-reviewer, because checking one requirement on a finished trace is simpler than satisfying every constraint during generation. Across rounds, Analyze (§4.2) pins criteria that stay satisfied and ranks newly broken criteria ahead of unsolved gaps; Propose (§4.3) samples a parallel group of candidate edits, scores them against each other on the same tasks, and contrasts the best and worst candidates to rewrite its proposal prompts; and Gate (§4.4) promotes the winner only when its gains exceed induced regressions (Soft-HURT), narrowing rules that cause isolated drops with [iff] preconditions and logging rejected edits. At test time, candidate pooling, self-review, and gating are turned off, and the agent runs a single pass (pass@1) with its frozen harness.

Three choices separate GUARD from prior harness learners. Reflexion and GEPA update from free-form reflection or scalar and Pareto scores, so they cannot tell a new regression from an old gap; GUARD ranks checklist criteria by paired directional regret. Meta-Harness searches agent code against raw trace archives, and RRSI rewrites one candidate per round behind a score-band gate that leaves per-task drops unbounded; GUARD scores a parallel group of candidates on the same tasks and promotes the winner only when its gains exceed induced regressions, narrowing rules with [iff] preconditions instead of deleting them. We evaluate GUARD across four benchmark settings (§5–§6, Appendix C): PAST-Bench [50], EvoHarnessBench [17], Drift Gauntlet [5], and professional legal and financial reasoning suites [2, 16, 27]. Our contributions are threefold:

- • 

Trace-grounded checklist self-review and directional regret (Analyze, §2–§4.2). We formulate reference-free harness adaptation over a frozen model using paired directional regret on pre-execution task checklists. We prove that dense checklist grading removes the \(1/\epsilon\) passive-discovery penalty on rare task invariants (Theorem 2), that paired priority ranks every fresh regression above every non-regressed criterion in the single-rollout binary case and pins exactly the mastered criteria (Proposition 1), and that gating keeps self-review scores non-decreasing on each round’s gated task buffer (Theorem 1).

- • 

GRPO-inspired candidate pooling and contrastive prompt evolution without weight updates (Propose, §4.3). Inspired by group-relative reinforcement learning [37, 3], GUARD samples a parallel group of candidate harnesses from one domain-agnostic seed prompt, evaluates them on the same task batch, and ranks them by critic-free group-standardized fitness (a selection step, not a gradient step) while contrasting the best and worst group candidates to rewrite proposal prompts across rounds. In a controlled single-model ablation at equal budget, parallel two-candidate pooling beats sequential single-candidate search and cuts rejected gate rounds by \(64\%\), while deploying a single harness in one pass at test time.

- • 

Soft-HURT promotion gating and continual generalization (Gate, §4.4, §6, Appendix C). Pairing Soft-HURT promotion with in-round [iff ] precondition repair yields \(19/19\) non-regressive execution-gated promotions across EvoHarnessBench, Drift Gauntlet, and the professional suites. GUARD is the only evaluated method with no negative backward or forward transfer on hosted EvoHarnessBench (FWT is zero because the gate abstained at later stages) and cuts tokens per task by \(54.5\%\) versus the base agent, incurs no stream-mean drop across all \(12\) block transitions and zero post-block forgetting on all four Drift Gauntlet streams, and ties the memory-pollution floor on PAST-Bench.

2 Background and Problem Formulation

Agents, harnesses, and task streams.

We model an autonomous agent \(A=(\pi_{\theta},W_{t,g})\) as a frozen language model policy \(\pi_{\theta}\) paired with an inspectable harness state \(W_{t,g}\) at adaptation round \(t\in\{0,1,\dots,T\}\) (\(W_{0,g}\) empty; subscript \(g\) omitted when clear) [20, 45]. Tasks arrive from groups \(g\in\mathcal{G}\) indexing roles, task families, or, when a continual stream hides group labels and drift boundaries [5], the pre-execution (Turn-0, before the solver’s first action) observable tool and schema signature of query \(q\in\mathcal{Q}_{g}\). We call \(W_{t,g}\) a non-parametric policy component because it is editable text rather than model weights: conditioning on it steers rollouts \(\tau\sim\pi_{\theta}(\cdot\mid q,W_{t,g})\), while \(\theta\) stays fixed during both adaptation and testing. In reinforcement-learning terms, an action is a harness edit, its reward is the gated self-review fitness \(R_{m}\) (§4.3), and only \(W\) is optimized. While this formulation accommodates general text or code harnesses [26], we instantiate \(W_{t,g}\) as structured Markdown files, termed a harness playbook, organizing workflow instructions, entity-grouped domain rules, reusable skills (SKILL.md), persistent memories (MEMORY.md), and optional pre-submit checks, with specialized exceptions scoped by explicit [iff ] preconditions.

Reference-free continual evolution and non-regressive RSI.

Let \(V^{\star}(q,\tau)\in[0,100]\) denote the unobserved task evaluator, unavailable throughout adaptation. Observing only task prompts, tool interfaces, execution trajectories, and runtime states in interaction history \(\mathcal{H}_{t,g}\), a reference-free harness evolver \(\mathcal{E}\) recursively updates the incumbent across adaptation rounds:

At test time, evolution freezes and each unseen query \(q\in\mathcal{Q}_{g}\) executes under the single promoted harness \(W_{T,g}\) to maximize \(\mu_{g}(W_{T,g})=\mathbb{E}_{q\in\mathcal{Q}_{g},\,\tau\sim\pi_{\theta}(\cdot\mid q,W_{T,g})}[V^{\star}(q,\tau)]\). Because \(\mathcal{E}\) updates \(W_{t,g}\) adaptively from finite online rollouts without \(V^{\star}\), continual generalization under Eq. (1) requires improving \(\mu_{g}\) without local overfitting on solved tasks or catastrophic forgetting of mastered behaviors as \(t\) and task distributions shift [45, 5]: scalar round scores mix edit-induced regressions with unresolved capability gaps and compound negative transfer across rounds.

What reference-free does and does not mean.

Throughout this paper, reference-free (and grader-free) is an operational constraint on the adaptation loop \(\mathcal{E}\): neither the solver, the self-reviewer, nor the distiller ever accesses held-out reference answers, test cases, hidden verifiers \(V^{\star}\), oracle skills, or official grading rubrics. It does not mean learning from zero supervision. Specifically, adaptation draws on four observable sources of structure: (i) benchmark-authored training task prompt distributions, (ii) public tool declarations and environment schemas, (iii) the agent’s own interaction trajectories and observable sandbox states (with no human expert demonstrations), and (iv) structured criterion-level judgments from the language-model self-reviewer (§4.1).

3 Related Work

Table B.1 (Appendix B.1) compares GUARD with representative self-improvement methods and environments across the components they optimize, their closed-loop mechanisms, and their adaptation and context scalability.

Verbal reflection, memories, and playbooks.

Reflexion [38], ExpeL [59], ReasoningBank [30], and AWM [43] store verbal reflections or workflows; MemGPT [31], Voyager [42], and WikiSkill [40] maintain memories, skill libraries, and append-only wikis; Dynamic Cheatsheet [39] and ACE [56] incrementally update playbooks; and Context Language Models (CLM) [36] update model weights to compact context via Group Relative Policy Optimization (GRPO) [37], whereas Training-Free GRPO [3] summarizes group rollouts into an experience library with frozen weights. GUARD differs in what forms the group: it scores \(M\) candidate harnesses on the same task batch rather than rollouts of one fixed context, contrasts the best and worst candidates to rewrite proposal prompts, and accepts the winner only through a regression-aware gate. AutoGuide [9], AutoManual [4], and CLIN [24] distill conditional guidelines, rule manuals, or causal memories from experience; GUARD’s [iff] rules are likewise conditional, but enter the harness only through regression-aware ranking and gating. Because these updates neither isolate edit-induced regressions nor gate per-task drops, they remain vulnerable to the plasticity–pollution and plasticity–stability trade-offs measured by PAST-Bench [50], EvoHarnessBench [17], and Drift Gauntlet [5]. Accepting an update only when prior behavior does not degrade echoes regression-free model updates [47] and gradient-constrained continual learning [21], which rely on labels or gradients that a reference-free harness loop does not have.

Unsupervised environment design and zero-data RL.

UED [7, 14, 15] prioritizes high-regret POMDP levels via antagonist regret (PAIRED [7]), maximal Monte Carlo (MaxMC) regret [14, 15, 32], or learnability \(p(1-p)\) [35], whereas we transfer regret from level curation to directional criterion ranking over pre-execution task checklists [61] without an antagonist. Zero-data RL self-play (Absolute Zero [60], Self-Challenging Agents [62], R-Zero [13], and Agent0 [46]) eliminates human labels via code verifiers or majority voting, yet requires weight gradients (precluding black-box APIs), falters on stateful tool mutations, and updates opaque model weights instead of inspectable conditional rules.

Prompt, workflow, and harness optimization.

Prompt optimizers such as DSPy [18], TextGrad [53], TextReg [10], OPRO [51], WizardLM [48], Promptbreeder [8], EvoPrompt [11], and GEPA [1] search instructions via scalar objectives, textual gradients, or Pareto archives; TextReg [10] filters low-recurrence patches under labeled single-turn supervision, which can suppress valid edge-case exceptions. Workflow/code optimizers ADAS [12], AFlow [55], and Darwin Gödel Machine (DGM) [58] mutate code via archives [19, 28] or MCTS against validation ground truth, while AutoHarness [22], Self-Harness [57], Meta-Harness [20], RRSI [45], and Harness2 [49] evolve harnesses around frozen weights (alongside MLGym [29], PostTrainBench [34], RSIBench-Data [25], and RSIGym [26]). Among open-world designs, Harness2 probes per-task harnesses online from \(W_{0}\) at extra test-time rollout cost, RRSI’s score-band gate leaves per-task drops unbounded, and persistent harnesses (ReasoningBank, GEPA, Meta-Harness) suffer severe forgetting under hidden drift [5]. GUARD instead evolves a single persistent harness in a reference-free loop and deploys it at \(O(1)\) context in \(T\) and single-pass (pass@1) test cost (Appendix B.5).

4 GUARD: Regret-Guided Harness Evolution

During adaptation, GUARD instantiates the reference-free evolver \(\mathcal{E}\) in Eq. (1) as a four-stage closed loop (Figure 2; Algorithm 1; constants in Appendix B): pre-execution checklist derivation and two-layer self-review (§4.1), paired regret ranking (Analyze, §4.2), contrastive candidate pooling (Propose, §4.3), and Soft-HURT promotion (Gate, §4.4), with formal guarantees in §4.5. At test time, this adaptation loop is disabled and each unseen task runs a single rollout under the frozen harness \(W_{T,g}\).

4.1 Reference-Free Self-Review via Task Checklists

Pre-execution task checklist \(\mathcal{C}(q)\).

Extending IFEval’s verifiable constraint decomposition [61] and checklist-based evaluation [33, 6, 41] to multi-turn tool workflows, the self-reviewer reads only the task prompt, visible tool declarations, and schema once at Turn 0 (before the solver’s first action) to derive and cache a fixed checklist \(\mathcal{C}(q)\) of atomic binary predicates (criteria \(c\in\mathcal{C}(q)\); Appendix B) across two classes: (i) execution-verifiable predicates (clean sandbox execution, valid entity IDs/columns, idempotent mutations) and (ii) semantic predicates (honoring every prompt constraint, recipient, format, and safety rule without applying superseded rules).

Two-layer grading and verification asymmetry.

Layer 1 checks execution predicates deterministically on an ephemeral sandbox copy; Layer 2 grades semantic predicates individually from the prompt, output, and tool/state trace, returning \(r(\tau,c)\in\{0,1\}\) and a failure rationale. Over graded predicates \(\mathcal{C}^{\mathrm{gr}}(\tau)\subseteq\mathcal{C}(q)\) (\(|\mathcal{C}^{\mathrm{gr}}(\tau)|\geq 1\); unconfigured checks excluded; an unparseable verdict counts as failed or falls back to deterministic trace checks), trajectory \(\tau\) receives criterion score \(S(\tau)\) and strict score \(S^{\mathrm{strict}}(\tau)\):

Pre-execution decomposition uses generation–verification asymmetry: long-horizon generation couples \(N\) constraints and suffers “seen-but-not-carried” omissions, while checking one atomic predicate after execution requires localized \(O(1)\) attention grounded by Layer 1 sandbox states. Cross-task \(\Delta_{\mathrm{hurt},t}\) and Soft-HURT gating then prevent single-instance overfitting [23].

4.2 Paired Regret Ranking (Analyze Stage)

Definition 1 (Criterion obedience and paired regret).

For trajectories \(\mathcal{T}_{c}(W)\) grading criterion \(c\) under \(W\) (\(\mathcal{T}_{c}(W_{t-1})=\emptyset\) skipped), criterion obedience is

Entering round \(t\geq 1\) with incumbent \(W_{t-1}\), comparing the two most recent incumbents \(W_{t-2}\) and \(W_{t-1}\) on the same tasks gives:

where \(\Delta_{\mathrm{hurt},t}(c)=0\) if \(t=1\) or \(c\) is not graded under both compared playbooks.

Both terms are non-negative and parameter-free: a regressed criterion receives its incumbent gap plus its drop, outranking equally obeyed non-regressed criteria (Proposition 1); with one binary verdict per criterion after a promotion, \(\mathrm{Priority}_{t}(c)\in\{2,1,0\}\) separates regressions (\(1\to 0\)), unsolved gaps (\(0\to 0\)), and mastered checks (\(1\to 1\) or \(0\to 1\)). In regret terms, \(\Delta_{\mathrm{gap},t}\) is the incumbent’s shortfall against an oracle harness that satisfies every criterion, and \(\Delta_{\mathrm{hurt},t}\) is the negative transfer introduced by the latest promotion.

Rejected rounds, diagnostic lists, and trajectory contrasts.

After a rejection (\(W_{t-1}=W_{t-2}\)), execution scoring instead takes \(\Delta_{\mathrm{hurt},t}\) from \(W_{t-1}\) to the rejected winner \(\widetilde{W}_{t-1}\) (or its repair \(\widetilde{W}^{\mathrm{rep}}_{t-1}\)), so the next proposal sees which criteria the refused edit broke, while \(\Delta_{\mathrm{gap},t}\) and pinning stay anchored to the incumbent; critic scoring always compares consecutive incumbents (§5). The signs of the two terms split criteria in the regret bundle \(\mathcal{B}_{t,g}\) into three diagnostic lists, each sorted by descending \(\mathrm{Priority}_{t}(c)\) (ties broken by \(\Delta_{\mathrm{hurt},t}(c)\)): (1) Regressed (\(\Delta_{\mathrm{hurt},t}>0\)), asking the proposer to wrap offending rules in [iff ] preconditions instead of discarding specialized fixes [10]; (2) Unsolved Gap (\(\Delta_{\mathrm{hurt},t}=0,\Delta_{\mathrm{gap},t}>0\)), targeting persistent gaps; and (3) Mastered (\(\mathrm{Priority}_{t}=0\), i.e., \(\mathrm{obey}(c;W_{t-1})=1\land\Delta_{\mathrm{hurt},t}=0\)), pinning obeyed rules against overwriting. These lists serve as diagnostic annotations, not hand-coded edit operators: the proposer receives them with the incumbent, trajectory contrasts, and the ledger window, and writes candidate playbooks end-to-end. Finally, on tasks with differing scored rollouts, \(\mathcal{B}_{t,g}\) pairs top and bottom trajectories \((\tau^{+},\tau^{-})\) (ordered by \(S^{\mathrm{strict}}\), ties by \(S\)) whenever

(\(\delta_{\mathrm{con}}=10\)). This condition captures partial checklist progress even when blocking errors or critical caps flatten \(S^{\mathrm{strict}}\).

4.3 Group-Relative Candidate Pooling and Contrastive Evolution (Propose Stage)

In reinforcement learning, Group Relative Policy Optimization (GRPO) [37] estimates policy advantage without a value network by sampling a group of rollouts from a shared state and standardizing their rewards within the group. Following the training-free group-relative perspective [3], the Propose stage applies this principle to non-parametric harness optimization without updating model weights: it samples \(M\geq 2\) candidate harnesses in parallel from \((W_{t-1,g},\mathcal{B}_{t,g})\), selects the winner by within-group standardized fitness (\(\arg\max_{m}\hat{A}_{m}\)), and contrasts the best and worst group candidates (\(\mathsf{ContrastEvolve}\)) to update the strategy-prompt pool \(\mathcal{P}_{t,g}=\{s_{t,1},\dots,s_{t,M}\}\) across rounds. Unlike GRPO, GUARD takes no gradient step and uses no clipping or KL penalty; \(\hat{A}_{m}\) only ranks candidates and picks the contrast pair \((m^{+},m^{-})\), and the Soft-HURT gate (§4.4) plays the role of a trust region. What the group buys is credit isolation without a learned critic: all \(M\) candidates are scored on the same \((W_{t-1,g},\mathcal{B}_{t,g},\mathcal{Q}_{g})\), so batch-level task difficulty cancels out.

Uniform initialization and scoring.

Round 1 initializes all \(M\) parallel candidates with the same domain-agnostic prompt \(s_{0}\) (SHARED_SEED_PROMPT, Appendix B.4):

drawing diversity without operator priors from sampling \(\widetilde{W}^{(m)}_{1,g}=\mathsf{Distill}(s_{0},\mathcal{B}_{1,g},W_{0,g})\). Over \(N_{\mathrm{rep}}\geq 1\) replicates \(\{\tau_{q,r}\}_{r=1}^{N_{\mathrm{rep}}}\) and noise floor \(\delta_{\mathrm{noise}}\geq 0\), task scores and helped/hurt sets are

with means \(\bar{S}(W),\bar{S}^{\mathrm{strict}}(W)\) supplied by execution scoring (\(M\) group rollouts/round) or critic scoring (one joint pass over accumulated trajectories on stateful suites). With \(\mathrm{Perf}_{m}=\bar{S}^{\mathrm{strict}}(\widetilde{W}^{(m)}_{t})+\tfrac{1}{4}\bar{S}(\widetilde{W}^{(m)}_{t})\) and \(\mathcal{Q}^{\pm}_{m}=\mathcal{Q}^{\pm}(\widetilde{W}^{(m)}_{t},W_{t-1})\), scalar and standardized fitness are

(\(\mu_{R}=\frac{1}{M}\sum_{m}R_{m}\)), where \(\beta>\gamma\) penalizes hurts over helps and \(m^{\star}=\arg\max_{m}\hat{A}_{m}=\arg\max_{m}R_{m}\) selects \(\widetilde{W}_{t}=\widetilde{W}^{(m^{\star})}_{t}\) (with \(M=2\), \(\hat{A}_{m}\approx\pm 1\) whenever \(R_{1}\neq R_{2}\), so selection keeps the higher-fitness candidate).

Contrastive prompt evolution, deployment, and complexity.

Selecting distinct best and worst candidates in the group,

(ties broken by \(\bar{S}\), \(|\mathcal{Q}^{-}_{m}|\), candidate index; mirroring MaxMC spread [15]), \(\mathsf{ContrastEvolve}\) scrubs task IDs to &lt;TASK_ID>, contrasts \((s_{t,m^{\pm}},\widetilde{W}^{(m^{\pm})}_{t,g},R_{m^{\pm}},|\mathcal{Q}^{\pm}_{m^{\pm}}|)\), and outputs learnings, an exploitation prompt \(s^{+}_{t+1}\), and a precondition-narrowing prompt \(s^{-}_{t+1}\), updating

At test time, \(\mathcal{P}_{t,g}\), the self-reviewer, and \(\mathcal{L}_{g}\) are discarded: deployment runs a single (\(1\times\)) rollout per task (pass@1 on all primary benchmarks) under frozen \(W_{T,g}\). During adaptation, parallel \(M\)-candidate pooling isolates credit on identical \((W_{t-1,g},\mathcal{B}_{t,g},\mathcal{Q}_{g})\), bootstraps Round-1 contrasts, and reduces single-sample gate rejections (§6.4, Appendix C.4). Execution scoring costs \(O(TMQ)\) rollouts with \(O(TQ)\) parallel rollout depth (or \(O(TQ)\) online rollouts under critic scoring), while bounded playbooks \(B_{W}\), ledger window \(L_{\max}\), and capped bundles \(B_{\mathcal{B}}\) keep proposer and test context \(O(1)\) in \(T\) (Table B.1, Appendix B.5).

4.4 Soft-HURT Promotion Gate and Rejection Ledger (Gate Stage)

Soft-HURT promotion gate.

Using per-task scores \(S_{q}\) and hurt set \(\mathcal{Q}^{-}(\widetilde{W},W)\) from (7), the group-averaged regression penalty beyond \(\delta_{\mathrm{noise}}\) is

and the Soft-HURT rule promotes a candidate over \(W_{t-1}\) only when net gain exceeds induced hurt:

Parameterized by single-task noise floor \(\delta_{\mathrm{noise}}\geq 0\), hurt-task budget \(h_{\max}\geq 0\), and trade-off margin \(\mu_{\min}\geq 0\), Soft-HURT admits \(\widetilde{W}_{t}\) when \(|\mathcal{Q}^{-}(\widetilde{W}_{t},W_{t-1})|\leq h_{\max}\), \(|\mathcal{Q}^{+}(\widetilde{W}_{t},W_{t-1})|\geq\mathbb{I}[|\mathcal{Q}^{-}(\widetilde{W}_{t},W_{t-1})|>0]\), and

When \(\widetilde{W}_{t}\) fails solely due to isolated regressions (\(1\leq|\mathcal{Q}^{-}(\widetilde{W}_{t},W_{t-1})|\leq h_{\mathrm{rep}}\)), GUARD triggers at most one in-round [iff] scope-guard repair \(\widetilde{W}^{\mathrm{rep}}_{t}\) and promotes \(\widetilde{W}^{\mathrm{rep}}_{t}\) if its re-scored trajectories satisfy the same Soft-HURT rule (\(\mu_{\min}=0\) on repaired candidates; suite parameters in Appendix B). Any other candidate is rejected, so every promoted update obeys (12).

Rejection ledger and stopping.

Rejected gate decisions log deduplicated active entries to \(\mathcal{L}_{g}\) (an on-disk JSONL log; candidate-level runners store gate metrics and scrubbed rule excerpts with read-back cap \(L_{\max}\in\{12,40\}\), while the professional-suite runner stores active criterion-removal excerpts; Appendix B), rendered into \(\mathcal{B}_{t+1,g}\) at \(O(1)\) prompt cost in \(T\) so refused edits are not repeated verbatim while [iff] refinements remain eligible. Rejected candidates are never re-executed (\(\Delta_{\mathrm{hurt},t+1}\) reuses their gate scores), and optional early stopping is disabled in all reported runs.

4.5 Theoretical Guarantees

These results characterize the self-review objective on gated task buffers; held-out accuracy is evaluated empirically in §6. Proofs of Theorem 1, Theorem 2, and Proposition 1 appear in Appendix A. For Theorem 1, fix group \(g\in\mathcal{G}\) with fixed \(\mathcal{Q}_{g}\): conditional on prior history, replicate errors \(\{S(\tau_{q,r})-\mu_{q}(W)\}_{q\in\mathcal{Q}_{g},\,r\leq N_{\mathrm{rep}}}\) (\(N_{\mathrm{rep}}\geq 1\) under execution rollouts) are independent across \(q,r\) and \(\sigma\)-sub-Gaussian (mean \(\bar{S}(W)\), expectation \(\mu(W)=\frac{1}{|\mathcal{Q}_{g}|}\sum_{q\in\mathcal{Q}_{g}}\mu_{q}(W)\)). Over \(T_{\max}\) rounds, at most \(n_{\mathrm{eval}}=1+T_{\max}(M+\mathbb{I}_{\mathrm{rep}})\) candidate harnesses are evaluated per group (\(\mathbb{I}_{\mathrm{rep}}\in\{0,1\}\) for in-round [iff] repair) against recorded incumbent scores without re-running incumbents; let \(\Delta_{t}=\bar{S}(W_{t})-\bar{S}(W_{t-1})\).

Theorem 1 (Non-Regressive Gating and Concentration).

Under the gate of (12) and the replicate setup above:

- (i) 

No downward drift: \(\Delta_{t}>0\) if round \(t\) promotes and \(\Delta_{t}=0\) otherwise, so

- (ii) 

Regressions are paid for: on every promoted round, with \(\mathcal{Q}^{-}_{t}=\mathcal{Q}^{-}(W_{t},W_{t-1})\) the tasks dropping by more than \(\delta_{\mathrm{noise}}\), and the left-hand side is zero whenever \(\mathcal{Q}^{-}_{t}=\emptyset\) (in particular when \(h_{\max}=0\)).

- (iii) 

Concentration: for any \(\alpha\in(0,1)\), with probability at least \(1-\alpha\), simultaneously for every group \(g\in\mathcal{G}\) (with \(\log\) the natural logarithm),

- (iv) 

Factored speedup: if group \(g\) promotes in each round independently with probability \(a_{g}\), per-group gating advances a fraction \(\frac{1}{|\mathcal{G}|}\sum_{g}a_{g}\) of groups per round vs. \(\prod_{g}a_{g}\) under a global gate (\(a^{1-|\mathcal{G}|}\times\) for \(a_{g}=a\)).

The union bound in (iii) covers all \(n_{\mathrm{eval}}\) evaluated harnesses per group (paying only \(\log(M+\mathbb{I}_{\mathrm{rep}})\) inside \(n_{\mathrm{eval}}\) for within-group selection and repair) and applies to execution rollouts (\(N_{\mathrm{rep}}\geq 1\); main-text suites use \(N_{\mathrm{rep}}=1\) and Appendix C uses \(N_{\mathrm{rep}}=2\)) instead of single critic calls. Here \(\mu\) is the expected self-review score on \(\mathcal{Q}_{g}\), and Eq. (16) serves as an asymptotic sample-complexity scaling law (\(|\mathcal{Q}_{g}|N_{\mathrm{rep}}=\Omega(\sigma^{2}\log(n_{\mathrm{eval}}|\mathcal{G}|/\alpha)/\Delta^{2})\) samples keep the selection optimism of recorded incumbent scores, at most twice the deviation term in (16), below a target gain \(\Delta\)) rather than a non-vacuous finite-sample certificate at our benchmark task counts. When incumbents are re-scored on growing episode histories (PAST-Bench) or online task blocks shift across stages (EvoHarnessBench, Drift Gauntlet), (i)–(ii) hold within each round’s gated task buffer rather than telescoping unconditionally across distribution shifts, which motivates pre-execution interface-signature routing and replay-buffer anchor tasks (§6.3).

Theorem 2 (Targeted Repair vs. Passive Discovery).

Consider \(J\) invariants exercised by \(\mathcal{Q}_{g}\) and violated by \(W_{0}\) (an invariant is a task-independent rule that the playbook must encode). Compare two observability regimes: a passive end-task learner that observes an invariant only when a coarse task failure surfaces it with probability \(p_{j}\leq\epsilon\), versus dense pre-execution checklist grading where every violated invariant is captured by a derived criterion evaluated each round. Let \(T_{\mathrm{passive}}\) be the rounds until passive surfacing observes all \(J\) invariants, \(T_{\mathrm{target}}\) the rounds until targeted repair resolves all \(J\) invariants, and \(H_{J}=\sum_{\ell=1}^{J}1/\ell\) (\(H_{0}=0\)).

- (i) 

Passive lower bound: if, independently across invariants and rounds, invariant \(j\) surfaces in each round with probability \(p_{j}\leq\epsilon\) for \(\epsilon\in(0,1)\), then where the \(\Omega((\log J)/\epsilon)\) asymptotic form holds for \(\epsilon\leq 1/2\).

- (ii) 

Targeted upper bound: if in each round (a) every unresolved invariant fails a derived criterion (\(\mathrm{Priority}_{t}(c)>0\)), (b) the winner addresses at least \(\min(b_{\min},u)\) of the \(u\) still unresolved invariants, for an integer \(b_{\min}\geq 1\), (c) each is resolved and admitted independently with probability \(\geq\rho>0\), and (d) resolved invariants stay resolved, then

Dense per-criterion grading (assumption (a)) removes the \(1/\epsilon\) dependence regardless of the specific priority formula: any ranking assigning positive weight to failing criteria, including \(1-\mathrm{obey}\), satisfies (a), and under all-or-nothing candidate admission with joint bundle pass probability \(\rho_{\mathrm{bundle}}>0\), \(\mathbb{E}[T_{\mathrm{target}}]\leq\lceil J/b_{\min}\rceil/\rho_{\mathrm{bundle}}\leq\frac{J}{\rho_{\mathrm{bundle}}b_{\min}}+\frac{\mathbb{I}[b_{\min}>1]}{\rho_{\mathrm{bundle}}}\). What uniquely distinguishes paired priority is regression handling, formalized next.

Proposition 1 (Strict Regression Dominance under Multi-Rollout Grading).

Let obedience (3) average the verdicts of \(K_{\mathrm{gr}}\geq 1\) graded rollouts, so that it may be fractional. When round \(t-1\) promoted, write \(o_{c}=\mathrm{obey}(c;W_{t-1})\) and \(\delta_{c}=\mathrm{obey}(c;W_{t-2})-o_{c}\) (\(\delta_{c}:=0\) if \(t=1\) or \(\mathcal{T}_{c}(W_{t-2})=\emptyset\)), so \(\mathrm{Priority}_{t}(c)=(1-o_{c})+\max(0,\delta_{c})\) by (4). Let \(c\) be a regressed criterion (\(\delta_{c}>0\)) and \(c^{\prime}\) a non-regressed one (\(\delta_{c^{\prime}}\leq 0\)).

- (i) 

Dominance at equal or higher obedience: if \(o_{c^{\prime}}\geq o_{c}\), then \(\mathrm{Priority}_{t}(c)-\mathrm{Priority}_{t}(c^{\prime})\geq\delta_{c}>0\), however small the regression (for example, one additional failing rollout).

- (ii) 

Exact trade-off: \(\mathrm{Priority}_{t}(c)>\mathrm{Priority}_{t}(c^{\prime})\) if and only if \(o_{c}-o_{c^{\prime}}&lt;\delta_{c}\). In the single-rollout binary case (\(K_{\mathrm{gr}}=1\)), a fresh regression (\(1\to 0\), priority \(2\)) therefore outranks every non-regressed criterion (priority at most \(1\)).

- (iii) 

Exact incumbent pinning set: under (4) in any round (promoted or rejected), \(\mathrm{Priority}_{t}(c)=0\) holds if and only if \(\mathrm{obey}(c;W_{t-1})=1\) and \(\Delta_{\mathrm{hurt},t}(c)=0\); in particular, no regressed criterion and no criterion failed by incumbent \(W_{t-1}\) is ever pinned.

Frequency ranking \(1-\mathrm{obey}(c;W_{t-1})\) satisfies (iii) but fails (i), tying newly broken criteria with static gaps of equal obedience; conversely, signed difference \(\mathrm{obey}(c;W_{t-2})-\mathrm{obey}(c;W_{t-1})\) satisfies (i) but fails (iii), assigning \(0\) to unchanged failures (\(0\to 0\)) alongside mastered invariants (\(1\to 1\)). Paired priority satisfies both parameter-free. For \(K_{\mathrm{gr}}\geq 3\) rollouts (or \(|\mathcal{T}_{c}|\geq 3\) tasks), a partial regression (\(1\to 2/3\), priority \(2/3\)) scores below a \(0\to 0\) gap (\(1\)) by (ii), and tying occurs at \(K_{\mathrm{gr}}=2\) (\(1\to 0.5\), priority \(1\)) or post-rejection when \(\mathrm{obey}(c;W_{t-1})=1\) (\(\Delta_{\mathrm{hurt},t}=1,\Delta_{\mathrm{gap},t}=0\)). This trade-off is intended: a criterion that the incumbent always fails outranks one that regressed on a minority of rollouts, while the Regressed list still surfaces every regression to the proposer (§4.2).

5 Experimental Setup

To evaluate continual harness RSI against local overfitting, memory pollution, and catastrophic forgetting across escalating non-stationarity, we test GUARD on three primary public benchmarks: (1) PAST-Bench [50] (cross-session memory retention, precision, and SOP updates), (2) EvoHarnessBench (EnterpriseOps-Gym) [17] (stage-wise continual transfer across evolving Model Context Protocol [MCP] tools and skills), and (3) Drift Gauntlet [5] (continual learning without forgetting across hidden-boundary workflow, topic, domain, and compound drift), complemented by two rubric-dense professional suites and controlled component ablations (Analyze, Propose, and Gate) in Appendix C. All three primary benchmarks compare the unified six-arm suite (Appendix B.2): No-Evolve (\(W_{0}\)), native memory/skill persistence (Hermes+ [50] / MemToolAgent [17]), RRSI [45], GEPA [1], Meta-Harness [20], and GUARD. To enforce strict reference-free hygiene on public datasets, our runner strips all held-out evaluator fields (reference answers, test cases, verifiers, oracle skills, and rubrics), aborts if any survives, and snapshots initial sandboxes so adaptation sees only public task inputs and execution states; after adaptation, every arm freezes its promoted harness \(W_{T}\) and reports standard single-rollout (pass@1) held-out accuracy across all three primary benchmarks (\(N_{\mathrm{rep}}=2\) frozen DEV trials on the Appendix C professional suites), with zero test-time candidate pooling, self-review, or retries.

Primary single-model Gemini 4 RSI and applicability to teacher–student knowledge distillation.

Our primary continual-RSI experiments use a single frozen Gemini 4 model across every role (solver, self-reviewer, distiller, and evolver, with zero stronger teacher): this powers the EvoHarnessBench Official Hosted SDK (Table 2), all four hidden-boundary continual streams on Drift Gauntlet (Table 3), and the controlled dual-axis Propose-stage ablation (Table C.8), alongside two full 12-family model-identical PAST-Bench suites (pure claude-opus-5-5 and pure gemini-3.8-flash; §6.1, Appendix B.2). Complementing this primary single-model regime, we deliberately include a cross-model teacher–student configuration on PAST-Bench (Table 1), the five-domain local gym (Tables C.5 and C.7), and the Appendix C professional suites, pairing a frozen gemini-3.8-flash student solver with a claude-opus-5-5 teacher reviewer and distiller shared identically across all evolving baselines. Evaluating both regimes serves a deliberate purpose: the single-model Gemini 4 suites isolate strictly self-referential continual improvement without external teacher supervision, while the cross-model suites show that GUARD also applies to teacher–student knowledge-distillation harness pipelines, distilling stronger-model reasoning into compact student skills and memories with low memory pollution and no regressed domain.

PAST-Bench and critic-scored selection.

Across 12 families spanning memory (SM01–02, EP01), procedural reuse (PC01, PC03–04), proactive gathering (PG01–02), and updates (PC02, SM04, SM06–07; 1 round per teach/update episode), official grading reports Task (plus procedural SOP Proc.), write precision (W.Prec.), Recall, update correctness (Upd.), retention (Ret.), pollution (Poll.), mechanism (Mech., mean of W.Prec., Recall, Upd., Ret., and \(1-\text{Poll.}\)), and Evolve (12-family mean of \(\Delta_{\text{task},f}\times\text{Mech.}_{f}\)). To avoid re-executing stateful multi-session histories, GUARD uses critic scoring (§4.3), evaluating the incumbent and candidate states in a single pass over accumulated session trajectories instead of re-running prior episodes (Appendix B.2); in place of per-task pre-execution checklists, the critic scores four fixed suite-level criteria (history grounding, SOP fidelity, [iff] scope, and superseded-rule replacement; Box B.1(c)) that overlap with the benchmark’s write-path pillars, while baselines keep their native reflection or search prompts. Because a single critic pass scores both the incumbent and the candidates without re-execution, it drives both selection and gating (\(24/24\) round winners admitted across the \(12\) families; execution-gated promotion fidelity is evaluated separately across EvoHarnessBench, Drift Gauntlet, and the professional suites in §6.4), while held-out official grading and paired per-family comparisons (Table B.4) evaluate downstream write-path quality.

EvoHarnessBench and Drift Gauntlet protocols.

On EvoHarnessBench, at stage \(v_{k}\in\{\texttt{v1},\dots,v_{V}\}\), arms adapt on \(\mathcal{D}_{\text{train}}^{(v_{k})}\) via execution scoring (§4.1) and evaluate on \(\mathcal{D}_{\text{test}}^{(v_{1}\dots v_{k})}\), forming matrix \(A_{k,j}\) (\(k\geq j\)). Following [17], we report final Overall ACC, strict Solved, Cohort ACC \(A_{V,j}\), backward transfer \(\text{BWT}=\sum_{j&lt;V}n_{j}(A_{V,j}-A_{j,j})/\sum_{j&lt;V}n_{j}\), forward transfer \(\text{FWT}=\sum_{k\geq 2}n_{k}(A_{k,k}-A^{\text{pre}}_{k,k})/\sum_{k\geq 2}n_{k}\) (local gym uses unweighted cohort BWT and stage FWT \(A_{k,k}-A^{W_{0}}_{k,k}\)), and per-task tokens, calls, and latency on: (1) the Official Hosted SDK (evolving_tools/calendar, v1–v3, \(18\) train / \(43\) test tasks) under single-model Gemini 4 for all roles; and (2) the Full 5-Domain local gym (\(236\) test / \(97\) train tasks, \(16\) stages across Calendar, Drive, ITSM v1–v4, CSM, HR), plus a controlled single-model Gemini 4 Propose-stage ablation across dual-axis ITSM (\(N{=}132\) test tasks; Appendix C.4). On Drift Gauntlet [5], agents evolve sequentially across \(K\in\{2,3,4\}\) unannounced task blocks (\(30\) online adaptation tasks/block, \(30\) held-out test tasks/group, \(12\) blocks total) under single-model Gemini 4 for every role across four continual drift scenarios spanning BFCL tool calling, BIRD text-to-SQL, and ScienceWorld interactive environments: workflow drift (BFCL-Miss \(\to\) BFCL-Base, \(K{=}2\)), topic drift (BIRD-F1 \(\to\) BIRD-Code \(\to\) BIRD-TP, \(K{=}3\)), domain drift (ScienceWorld \(\to\) BFCL-Base \(\to\) BIRD-F1, \(K{=}3\)), and compound drift (BIRD-Code \(\to\) BIRD-F1 \(\to\) BFCL-Miss \(\to\) BFCL-Base, \(K{=}4\)). From the \((K{+}1)\times K\) checkpoint matrix \(A[t,k]\) (\(t\in\{0,\dots,K\},k\in\{1,\dots,K\}\)) and seed vector \(B_{k}=A[0,k]\), we report [5]: Final Mean \(\bar{A}_{K}=\frac{1}{K}\sum_{k=1}^{K}A[K,k]\), terminal gain \(\Delta_{K}=\bar{A}_{K}-\bar{B}\), average gain \(\bar{\Delta}=\frac{1}{K}\sum_{t=1}^{K}(\bar{A}_{t}-\bar{B})\), within-block plasticity \(P=\frac{1}{K}\sum_{k=1}^{K}(A[k,k]-A[k{-}1,k])\), pre-block interference \(I=\frac{1}{K-1}\sum_{k=2}^{K}\frac{1}{k-1}\sum_{t=1}^{k-1}(A[t,k]-B_{k})\), worst-case post-block forgetting \(F=\frac{1}{K-1}\sum_{k=1}^{K-1}(\min_{t>k}A[t,k]-A[k,k])\), and stability \(S=(I+F)/2\). GUARD keys playbook sections to each task’s pre-execution observable environment/schema signature and renders only the matching section, whereas baselines keep one global playbook (lexically retrieved skills for Hermes+); for every arm, held-out rollouts are memoized per task and rendered playbook (Appendix B). Arms are compared strictly within each benchmark and model regime.

6 Main Experimental Results

6.1 PAST-Bench: Cross-Session Memory Write Path

While 5 of 12 families are single-rule tasks where every persistent arm reaches \(0.984\)–\(1.000\), write-path attribution and multi-step procedural SOPs (PC01, PC03, PC04) expose a sharp plasticity–pollution trade-off (Table 1, Figure 3; Tables B.3–B.4). Unscoped accumulators (Hermes+, GEPA) reach \(80.8\%\)–\(81.5\%\) procedural task at \(0.167\) overall pollution, but retain stale clauses on updates (\(52.9\%\) / \(46.4\%\) procedural; \(0.791\) / \(0.777\) overall). Conversely, aggressive rewriters (RRSI, Meta-Harness) lift update correctness to \(0.901\)–\(0.903\) (\(82.4\%\)–\(84.1\%\) procedural) while tripling pollution (\(0.500\) overall, \(1.000\) procedural) and depressing write precision (\(0.438\)–\(0.479\)). Pairing regret ranking, rule pinning, and [iff] guards, GUARD leads procedural task (\(83.0\%\)), procedural mechanism (\(90.0\%\) vs. at most \(78.0\%\)), and update (\(90.1\%\)) at \(0.000\) procedural pollution; across all 12 families (\(12/12>W_{0}\)), it leads update (\(0.924\), \(+13.3\text{pp}\) vs. Hermes+, \(+14.8\text{pp}\) vs. GEPA), mechanism (\(0.878\), \(p{=}0.016\) vs. RRSI), write precision (\(0.776\), \(p{=}0.031\) vs. RRSI), and evolve score (\(0.436\)) within \(0.004\) of top task score at the \(0.167\) pollution floor (\(0.000\) on \(10/12\) families, and \(0/48\) family losses on W.Prec. or Poll. across all four baselines; Table B.4). These gains persist without any teacher–student model gap (Appendix B.2): under model-identical all-claude-opus-5-5 execution, GUARD ranks first overall on task score (\(0.870\) vs. \(\leq 0.866\), \(+0.523\) over \(W_{0}\)), recall (\(0.871\)), and evolve score (\(0.458\)) with the sole lowest memory pollution (\(0.167\) vs. \(0.208\)–\(0.250\)); under all-gemini-3.8-flash, it lifts task score from \(0.371\) to \(0.852\), ties for lowest pollution (\(0.167\)), and leads latent rule induction (PC03: \(0.748\) vs. \(0.510\)–\(0.653\) on reflective/search baselines, \(+9.5\) to \(+23.8\text{pp}\)).

6.2 EvoHarnessBench: Continual Evolution Across Tools and Skills

Unified Gemini 4 hosted comparison, efficiency, and 5-domain local gym.

On the hosted SDK (Table 2, Figure 4), GUARD achieves the highest accuracy (\(80.80\%\); \(+8.89\text{pp}\) over \(W_{0}\), paired \(p=0.008\); \(+6.28\text{pp}\) over Meta-Harness, \(p=0.11\) on \(43\) tasks) and solve rate (\(58.14\%\), \(25/43\) vs. \(\leq 22/43\)), leading Cohorts v1 (\(78.47\%\)) and v3 (\(89.29\%\)) and tying Cohort v2 (\(84.17\%\)), while passing \(182/221\) official verifier checks (\(82.4\%\) vs. \(156\)–\(170/221\) [\(70.6\%\)–\(76.9\%\)] on baselines) with the fewest zero-score tasks (\(3/43\) vs. \(5\)–\(7/43\)). Soft-HURT promoted the Stage-v1 playbook (\(2{,}315\) chars, \(83.33\to 100\) source self-review, \(0\) hurt) and abstained at Stages v2–v3, so \(\text{FWT}=0.00\text{pp}\) holds by abstention and the entire lift stems from that Stage-v1 playbook. GUARD is the only arm with no negative entry across BWT Score, BWT Pass, and FWT (\(+0.85\) / \(+2.56\) / \(0.00\text{pp}\)), whereas RRSI drops \(-4.50\text{pp}\) on Cohort v2 at Stage v3 (\(77.67\%\to 73.17\%\), BWT Score \(-0.45\text{pp}\)) and GEPA (\(-3.97\text{pp}\) BWT), Meta-Harness (\(-13.21\text{pp}\) FWT), and MemToolAgent (\(-4.02\) / \(-4.98\text{pp}\)) each suffer negative transfer. Together with two-layer gating (§6.4) and a compact playbook (\(2{,}315\) vs. \(4{,}538\)–\(10{,}013\) chars), GUARD reaches \(0/43\) eight-step budget exhaustions (vs. \(7/43\) in \(W_{0}\) and \(6\)–\(10/43\) on baselines), which cuts tokens/task by \(54.5\%\) (\(59{,}651\) vs. \(131{,}032\)) and MCP calls by \(22.5\%\) while solving \(9.75\) tasks per \(1\text{M}\) tokens (\(1.50\times\) the best baseline, \(6.50\) on Meta-Harness, and \(2.61\times\) \(W_{0}\), \(3.73\)). Every one of the five hosted GUARD configurations evaluated in our study (\(75.57\%\)–\(80.80\%\) ACC, mean \(77.09\%\), \(171\)–\(182/221\) checks passed, \(0\)–\(3/43\) budget exhaustions; Appendix B) beats every external baseline (\(\leq 74.52\%\) ACC, \(\leq 170/221\) checks, \(6\)–\(10/43\) exhaustions). Across all five local-gym domains (\(236\) test tasks; Table C.5), GUARD improves upon or matches \(W_{0}\) in final accuracy across domains (macro \(65.81\%\to 66.46\%\), \(+1.00\text{pp}\) mean FWT), lifting multi-stage skill tracks such as ITSM (\(+1.63\text{pp}\) ACC, \(+8.47\text{pp}\) Solved) and CSM (\(+1.60\text{pp}\) ACC, with a minor trade-off on strict all-or-nothing solve rate) while safely abstaining where candidate edits do not clear Soft-HURT.

6.3 Drift Gauntlet: Continual RSI Under Hidden Stream Drift

Sustained multi-block progression and the plasticity–stability trade-off.

While EvoHarnessBench shifts tool schemas within one domain at a time, Drift Gauntlet [5] stress-tests whether self-evolving harnesses can accumulate capabilities across unannounced workflow, topic, domain, and compound shifts without boundary resets. Table 3 and Figure 5 (per-group trajectories in Figure C.2) show two main results under single-model Gemini 4. GUARD is the only arm whose stream-mean accuracy never decreases: across all \(12\) continual block transitions, GUARD incurs \(0/12\) stream-mean drops (\(65.00\to 70.00\to 70.00\%\) on workflow; \(67.78\to 67.78\to 68.89\to 70.00\%\) on topic; \(76.05\to 78.69\to 78.69\to 78.69\%\) on domain; \(70.84\to 71.67\to 71.67\to 74.17\to 74.17\%\) on compound). Its stage-normalized macro gain rises at every checkpoint (\(0.00\to+2.12\to+2.40\to+3.30\text{pp}\)), ranking first on Final Mean (\(73.22\%\), \(0.82\text{pp}\) above GEPA, about three task-equivalents of \(360\) held-out rollouts), \(\Delta_{K}\) (\(+3.30\text{pp}\), positive on all \(4/4\) streams), and \(\bar{\Delta}\) (\(+2.71\text{pp}\)). Every evolving baseline suffers \(3\)–\(8\) block drops out of \(12\): Hermes+ peaks at Block 1 before decaying (\(+1.76\to+0.91\to+0.40\text{pp}\)), RRSI falls below \(W_{0}\) (\(+0.80\to-0.65\to-2.00\text{pp}\)), GEPA dips \(-1.35\text{pp}\) at Block 2 (\(+2.94\to+1.59\to+2.48\text{pp}\)), and Meta-Harness drops \(-1.65\text{pp}\) below \(W_{0}\) at Block 1 (\(-20.00\text{pp}\) pre-block interference on workflow drift). Consistent with [5], plasticity \(P\) and stability \(S\) are strongly negatively correlated across the \(16\) \((\text{baseline},\text{stream})\) runs (Pearson \(r=-0.82\), reported descriptively because \(P\) and \(S\) share checkpoint cells): high-plasticity RRSI (\(P=+4.49\text{pp}\)) suffers severe post-block forgetting (\(F=-8.11\text{pp}\), \(-20.00\text{pp}\) on opposing BFCL-Miss \(\to\) BFCL-Base), whereas GEPA’s monolithic \(4{,}200\)-char prompt rewrite compresses prior-block character share on compound drift (BIRD-Code \(100\%\to 28.5\%\); BFCL-Miss \(49.4\%\to 22.4\%\) once BFCL-Base arrives, dropping BFCL-Miss accuracy \(73.33\%\to 66.67\%\)). By keying sections to pre-execution observable tool/schema signatures (\(0\) prior-signature characters overwritten) and gating updates against same-signature Vitter reservoir replay tasks (promoting \(9/12\) blocks, including in-round [iff] repair on ScienceWorld to reach \(82.73\%\), and rejecting \(3/12\) opposing-drift overwrites where hurt equaled lift), GUARD achieves both top plasticity (\(+4.55\text{pp}\)) and \(0.00\text{pp}\) post-block forgetting across all four streams, with only mild pre-block caution before opposing tool conventions are observed. On workflow and compound drift, where opposing blocks share the bfcl signature, Soft-HURT directly rejects both regressive overwrites (worked example in Box C.1). In a symmetric routing control (Appendix B), granting the same pre-execution signature routing to GEPA (\(71.55\%\), \(F=-2.78\text{pp}\)) and Meta-Harness (\(71.08\%\)) leaves GUARD ahead across all four streams (\(73.22\%\)), while a single-global-playbook GUARD ablation without signature routing still achieves \(72.35\%\) Final Mean, the highest global trajectory gain (\(\bar{\Delta}=+2.25\text{pp}\)), and zero post-block forgetting (\(F=0.00\text{pp}\)).

6.4 Self-Reviewer Calibration, Gate Fidelity, and Component Attribution

Table 4 (full audit across \(4{,}173\) EvoHarnessBench/PAST-Bench rollouts plus Drift Gauntlet block decisions in Table C.6) checks whether \(S(\tau)\) and Soft-HURT track hidden verifiers. Layer-1 sandbox checks curb LLM-only optimism: on hosted EvoHarnessBench, a 1-layer reviewer passes (\(\geq 75\%\)) \(22.2\%\) (\(12/54\)) of execution-broken traces vs. \(0.0\%\) (\(0/23\), sanity check by Eq. (2)) under 2-layer review. The final hosted configuration (two-layer review, cumulative-source gating, and a completeness-first distiller instruction; Appendix B) improves on the initial one-layer run by \(+4.82\text{pp}\) ACC (\(75.98\%\to 80.80\%\)) and \(+9.30\text{pp}\) Solved (\(48.84\%\to 58.14\%\)), with budget exhaustions dropping from \(2/43\) to \(0/43\). Across \(4{,}059\) EvoHarnessBench test rollouts (\(1{,}920\) hosted, \(2{,}139\) local; all arms), Layer 1 separates official ACC by \(+27.92\text{pp}\) (\(73.90\%\) vs. \(45.97\%\); \(82.6\%\) NPV); on PAST-Bench (\(N{=}114\)), Layer 2 has near-zero mean bias (\(-0.012\), \(\text{MAE}=0.131\), \(r{=}0.369\)) and \(82.2\%\) within-family concordance (\(75.6\%\) non-tied, \(r{=}0.432\)). Under active-cohort \(\Delta_{\text{test}}\) vs. \(W_{0}\), all \(19/19\) execution-gated Soft-HURT promotions across Drift Gauntlet (\(9/9\)), EvoHarnessBench (\(5/5\)), and the professional suites (\(5/5\)) satisfy \(\Delta_{\text{test}}\geq 0\) (\(15/19\) strictly \({>}0\) and \(4/19\) \(0.00\text{pp}\) ties; Table 4 note), whereas bypassing Soft-HURT on a rejected local Calendar v3 candidate lowers held-out accuracy and solve rate. In the five-domain teacher–student Analyze/Gate component ablation (\(236\) tasks; Table C.7), removing Analyze (\(1-\mathrm{obey}\), no pinning or contrasts) drops macro ACC by \(-7.33\text{pp}\) (\(66.46\%\to 59.13\%\), promoting \(4\) stages that regress multi-stage skill domains), and removing Soft-HURT drops macro ACC by \(-10.35\text{pp}\) (\(66.46\%\to 56.11\%\), regressing \(3/5\) domains vs. \(0/5\)). Under single-model Gemini 4 on dual-axis EvoHarnessBench ITSM (\(N{=}132\) test tasks, \(N_{\mathrm{rep}}{=}3\); Table C.8), parallel \(M{=}2\) candidate pooling (\(81.08\%\) ACC; BWT \(+0.61\%\)) beats matched-budget sequential \(M{=}1,2T\) search (\(78.85\%\), \(+2.23\text{pp}\), \(p{=}0.0267\); \(64\%\) fewer rejected gate rounds) and single-candidate \(M{=}1,T\) (\(77.20\%\), \(+3.88\text{pp}\), \(p{=}0.0029\)).

7 Conclusion

Continually adapting an agent’s harness around a frozen backbone model without external graders requires preventing local overfitting, catastrophic forgetting, and memory pollution. Drawing on curriculum regret from UED and group-relative scoring from reinforcement learning (GRPO), GUARD (Grader-free UED with Adaptive Rule Distillation) treats the text harness as a non-parametric policy component and updates it from task-derived checklists: Analyze separates edit-induced regressions (\(\Delta_{\mathrm{hurt}}\)) from unresolved gaps (\(\Delta_{\mathrm{gap}}\)) while pinning mastered criteria, Propose selects among parallel candidate edits via critic-free group-standardized fitness and contrasts the best and worst candidates to rewrite proposal prompts, and Gate (Soft-HURT) promotes only net-positive updates with formal non-regression guarantees on the self-review objective (Theorems 1–2, Proposition 1). At test time, it deploys a single frozen harness in one pass. Across four benchmark settings, GUARD improves upon or matches \(W_{0}\) in held-out accuracy, achieves \(19/19\) non-regressive execution-gated promotions, and sustains monotonic pass@1 gains with zero post-block forgetting under hidden stream drift while cutting hosted tokens per task by \(54.5\%\).

References

- [1] Lakshya A. Agrawal, Shangyin Tan, Dilara Soylu, Noah Ziems, Rishi Khare, Krista Opsahl-Ong, Arnav Singhvi, Herumb Shandilya, Michael J. Ryan, Meng Jiang, Christopher Potts, Koushik Sen, Alexandros G. Dimakis, Ion Stoica, Dan Klein, Matei Zaharia, and Omar Khattab. GEPA: Reflective prompt evolution can outperform reinforcement learning. arXiv preprint arXiv:2507.19457, 2025.
- [2] Afra Feyza Akyürek, Advait Gosai, Chen Bo Calvin Zhang, Vipul Gupta, Jaehwan Jeong, Anisha Gunjal, Tahseen Rabbani, Maria Mazzone, David Randolph, et al. PRBench: Large-scale expert rubrics for evaluating high-stakes professional reasoning. arXiv preprint arXiv:2511.11562, 2025.
- [3] Yuzheng Cai, Siqi Cai, Yuchen Shi, Zihan Xu, Lichao Chen, Yulei Qin, Xiaoyu Tan, Gang Li, Zongyi Li, Haojia Lin, Yong Mao, Ke Li, and Xing Sun. Training-free group relative policy optimization. arXiv preprint arXiv:2510.08191, 2025.
- [4] Minghao Chen, Yihang Li, Yanting Yang, Shiyu Yu, Binbin Lin, and Xiaofei He. AutoManual: Constructing instruction manuals by LLM agents via interactive environmental learning. In NeurIPS, 2024.
- [5] Xiaoyin Chen, Yizheng Huang, Yinglun Xu, Ziyun Zhao, Emmett McQuinn, Julie Liu, and Hope Yao. Are self-evolving agents continual learners? arXiv preprint arXiv:2610.25858, 2026.
- [6] Jonathan Cook, Tim Rocktäschel, Jakob Foerster, Dennis Aumiller, and Alex Wang. TICKing all the boxes: Generated checklists improve LLM evaluation and generation. arXiv preprint arXiv:2410.03608, 2024.
- [7] Michael Dennis, Natasha Jaques, Eugene Vinitsky, Alexandre Bayen, Stuart Russell, Andrew Critch, and Sergey Levine. Emergent complexity and zero-shot transfer via unsupervised environment design. In NeurIPS, 2020.
- [8] Chrisantha Fernando, Dylan Banarse, Henryk Michalewski, Simon Osindero, and Tim Rocktäschel. Promptbreeder: Self-referential self-improvement via prompt evolution. arXiv preprint arXiv:2309.16797, 2023.
- [9] Yao Fu, Dong-Ki Kim, Jaekyeom Kim, Sungryull Sohn, Lajanugen Logeswaran, Kyunghoon Bae, and Honglak Lee. AutoGuide: Automated generation and selection of context-aware guidelines for large language model agents. In NeurIPS, 2024.
- [10] Lucheng Fu, Ye Yu, Yiyang Wang, Yiqiao Jin, Haibo Jin, B. Aditya Prakash, and Haohan Wang. TextReg: Mitigating prompt distributional overfitting via regularized text-space optimization. arXiv preprint arXiv:2605.21318, 2026.
- [11] Qingyan Guo, Rui Wang, Junliang Guo, Bei Li, Kaitao Song, Xu Tan, Guoqing Liu, Jiang Bian, and Yujiu Yang. EvoPrompt: Connecting LLMs with evolutionary algorithms yields powerful prompt optimizers. In ICLR, 2024.
- [12] Shengran Hu, Cong Lu, and Jeff Clune. Automated design of agentic systems. In ICLR, 2025.
- [13] Chengsong Huang, Wenhao Yu, Xiaoyang Wang, Hongming Zhang, Zongxia Li, Ruosen Li, Jiaxin Huang, Haitao Mi, and Dong Yu. R-Zero: Self-evolving reasoning LLM from zero data. In ICLR, 2026.
- [14] Minqi Jiang, Edward Grefenstette, and Tim Rocktäschel. Prioritized level replay. In ICML, 2021.
- [15] Minqi Jiang, Michael Dennis, Jack Parker-Holder, Jakob Foerster, Edward Grefenstette, and Tim Rocktäschel. Replay-guided adversarial environment design. In NeurIPS, 2021.
- [16] Yidong Jiang, Junrong Chen, Eftychia Makri, Jialin Chen, Peiwen Li, Ali Maatouk, Leandros Tassiulas, Eliot Brenner, Bing Xiang, and Rex Ying. Fin-RATE: A real-world financial analytics and tracking evaluation benchmark for LLMs on SEC filings. arXiv preprint arXiv:2602.07294, 2026.
- [17] Zixuan Ke, Vaidehi Patil, Haizhou Shi, Yang Li, Ye Liu, Sarath Shekkizhar, Anurag Koul, Jiayu Wang, Xuan Phi Nguyen, Semih Yavuz, Mohit Bansal, and Shafiq Joty. EvoHarnessBench: Can your agents keep pace with an evolving harness? arXiv preprint arXiv:2609.04280, 2026.
- [18] Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, Zhiyuan Zhang, Keshav Santhanam, Sri Vardhamanan, Saiful Haq, Ashutosh Sharma, Thomas T. Joshi, Hanna Moazam, Heather Miller, Matei Zaharia, and Christopher Potts. DSPy: Compiling declarative language model calls into self-improving pipelines. In ICLR, 2024.
- [19] Joel Lehman and Kenneth O. Stanley. Abandoning objectives: Evolution through the search for novelty alone. Evolutionary Computation, 19(2):189–223, 2011.
- [20] Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab, and Chelsea Finn. Meta-Harness: End-to-end optimization of model harnesses. arXiv preprint arXiv:2603.28052, 2026.
- [21] David Lopez-Paz and Marc’Aurelio Ranzato. Gradient episodic memory for continual learning. In NeurIPS, 2017.
- [22] Xinghua Lou, Miguel Lázaro-Gredilla, Antoine Dedieu, Carter Wendelken, Wolfgang Lehrach, and Kevin P. Murphy. AutoHarness: Improving LLM agents by automatically synthesizing a code harness. arXiv preprint arXiv:2603.03329, 2026.
- [23] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al. Self-refine: Iterative refinement with self-feedback. In NeurIPS, 2023.
- [24] Bodhisattwa Prasad Majumder, Bhavana Dalvi Mishra, Peter Jansen, Oyvind Tafjord, Niket Tandon, Li Zhang, Chris Callison-Burch, and Peter Clark. CLIN: A continually learning language agent for rapid task adaptation and generalization. In COLM, 2024.
- [25] Fanqing Meng, Lingxiao Du, Qiguang Chen, Ziqi Zhao, Haocheng Lu, Mengkang Hu, and Michael Qizhe Shieh. RSIBench-Data: Benchmarking data-centric research for recursive self-improvement. arXiv preprint arXiv:2607.25886, 2026.
- [26] Fanqing Meng, Lingxiao Du, Haocheng Lu, Qiguang Chen, Ziqi Zhao, Zijian Wu, Jiayuan Zhuo, Mengkang Hu, and Michael Qizhe Shieh. RSIGym: A flexible environment for recursive self-improvement. arXiv preprint arXiv:2610.10310, 2026.
- [27] Charles Moslonka, Amaury de Vitry, Arthur Garnier, Hicham Randrianarivo, and Emmanuel Malherbe. LEDGER: A long-context benchmark of corporate annual reports. arXiv preprint arXiv:2606.13100, 2026.
- [28] Jean-Baptiste Mouret and Jeff Clune. Illuminating search spaces by mapping elites. arXiv preprint arXiv:1504.04909, 2015.
- [29] Deepak Nathani, Lovish Madaan, Nicholas Roberts, Nikolay Bashlykov, Ajay Menon, Vincent Moens, Amar Budhiraja, Despoina Magka, Vladislav Vorotilov, Gaurav Chaurasia, Dieuwke Hupkes, Ricardo Silveira Cabral, Tatiana Shavrina, Jakob Foerster, Yoram Bachrach, William Yang Wang, and Roberta Raileanu. MLGym: A new framework and benchmark for advancing AI research agents. arXiv preprint arXiv:2502.14499, 2025.
- [30] Siru Ouyang, Jun Yan, I-Hung Hsu, Yanfei Chen, Ke Jiang, Zifeng Wang, Rujun Han, Long T. Le, Samira Daruki, Xiangru Tang, Vishy Tirumalashetty, George Lee, Mahsan Rofouei, Hangfei Lin, Jiawei Han, Chen-Yu Lee, and Tomas Pfister. ReasoningBank: Scaling agent self-evolving with reasoning memory. arXiv preprint arXiv:2509.25140, 2025.
- [31] Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez. MemGPT: Towards LLMs as operating systems. arXiv preprint arXiv:2310.08560, 2023.
- [32] Jack Parker-Holder, Minqi Jiang, Michael Dennis, Mikayel Samvelyan, Jakob Foerster, Edward Grefenstette, and Tim Rocktäschel. Evolving curricula with regret-based environment design. In ICML, 2022.
- [33] Yiwei Qin, Kaiqiang Song, Yebowen Hu, Wenlin Yao, Sangwoo Cho, Xiaoyang Wang, Xuansheng Wu, Fei Liu, Pengfei Liu, and Dong Yu. InFoBench: Evaluating instruction following ability in large language models. In Findings of ACL, 2024.
- [34] Ben Rank, Hardik Bhatnagar, Ameya Prabhu, Shira Eisenberg, Karina Nguyen, Matthias Bethge, and Maksym Andriushchenko. PostTrainBench: Can LLM agents automate LLM post-training? arXiv preprint arXiv:2603.08640, 2026.
- [35] Alexander Rutherford, Michael Beukman, Timon Willi, Bruno Lacerda, Nick Hawes, and Jakob Foerster. No regrets: Investigating and improving regret approximations for curriculum discovery. In NeurIPS, 2024.
- [36] Rulin Shao, Shannon Zejiang Shen, Junjie Oscar Yin, Yuetai Li, Minheng Wang, Hamish Ivison, Radha Poovendran, Nathan Lambert, Teng Xiao, Mike Lewis, Wen-tau Yih, Luke Zettlemoyer, and Pang Wei Koh. Context language models. arXiv preprint arXiv:2609.37725, 2026.
- [37] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. DeepSeekMath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.
- [38] Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. In NeurIPS, 2023.
- [39] Mirac Suzgun, Mert Yuksekgonul, Federico Bianchi, Dan Jurafsky, and James Zou. Dynamic cheatsheet: Test-time learning with adaptive memory. arXiv preprint arXiv:2504.07952, 2025.
- [40] Liyan Tang, Cyrus Rashtchian, Chun-Sung Ferng, Andrew Tomkins, Da-Cheng Juan, and Tu Vu. WikiSkill: Compiling agent experience into persistent knowledge for skill evolution. arXiv preprint arXiv:2608.27454, 2026.
- [41] Vijay Viswanathan, Yanchao Sun, Shuang Ma, Xiang Kong, Meng Cao, Graham Neubig, and Tongshuang Wu. Checklists are better than reward models for aligning language models. In NeurIPS, 2025.
- [42] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. arXiv preprint arXiv:2305.16291, 2023.
- [43] Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, and Graham Neubig. Agent workflow memory. arXiv preprint arXiv:2409.07429, 2024.
- [44] Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, et al. A survey on large language model based autonomous agents. Frontiers of Computer Science, 18(6):186345, 2024.
- [45] Peng Xia, Rujun Han, Zifeng Wang, Yanfei Chen, Yufan Zhuang, Yoonho Lee, Chengsong Huang, Han Yu, Zhongying CuiZhu, Yifei Ming, Huaxiu Yao, Burak Gokturk, Tomas Pfister, and Chen-Yu Lee. RRSI: Regularized recursive self-improvement of agent harnesses. arXiv preprint arXiv:2609.24972, 2026.
- [46] Peng Xia, Kaide Zeng, Jiaqi Liu, Can Qin, Fang Wu, Yiyang Zhou, Caiming Xiong, and Huaxiu Yao. Agent0: Unleashing self-evolving agents from zero data via tool-integrated reasoning. In COLM, 2026.
- [47] Yuqing Xie, Yi-An Lai, Yuanjun Xiong, Yi Zhang, and Stefano Soatto. Regression bugs are in your model! Measuring, reducing and analyzing regressions in NLP model updates. In ACL, 2021.
- [48] Can Xu, Qingfeng Sun, Kai Zheng, Xiubo Geng, Pu Zhao, Jiazhan Feng, Chongyang Tao, Qingwei Lin, and Daxin Jiang. WizardLM: Empowering large pre-trained language models to follow complex instructions. In ICLR, 2024.
- [49] Ruiyao Xu, Yanfei Chen, Zhongying CuiZhu, Bhavana Dalvi Mishra, Yifei Ming, Han Yu, Rujun Han, Chen-Yu Lee, and Tomas Pfister. Harness2: Recursive agent harnessing for an open world. arXiv preprint arXiv:2610.14224, 2026.
- [50] Shuhan Xue, Zixin Ding, Yichen Shen, Yinjie Wang, Zhenfei Yin, Yingcheng Wu, Yuxin Chen, Mengdi Wang, and Ling Yang. PAST-Bench: Benchmarking the foundations of recursive self-improvement in personal agents. arXiv preprint arXiv:2608.04003, 2026.
- [51] Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V. Le, Denny Zhou, and Xinyun Chen. Large language models as optimizers. In ICLR, 2024.
- [52] John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir Press. SWE-agent: Agent-computer interfaces enable automated software engineering. In NeurIPS, 2024.
- [53] Mert Yuksekgonul, Federico Bianchi, Joseph Boen, Sheng Liu, Zhi Huang, Carlos Guestrin, and James Zou. TextGrad: Automatic “differentiation” via text. arXiv preprint arXiv:2406.07496, 2024.
- [54] Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah D. Goodman. STaR: Bootstrapping reasoning with reasoning. In NeurIPS, 2022.
- [55] Jiayi Zhang, Jinyu Xiang, Zhaoyang Yu, Fengwei Teng, Xionghui Chen, Jiaqi Chen, Mingchen Zhuge, Xin Cheng, Sirui Hong, Jinlin Wang, Bingnan Zheng, Bang Liu, Yuyu Luo, and Chenglin Wu. AFlow: Automating agentic workflow generation. In ICLR, 2025.
- [56] Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, Urmish Thakker, James Zou, and Kunle Olukotun. Agentic context engineering: Evolving contexts for self-improving language models. arXiv preprint arXiv:2510.04618, 2025.
- [57] Hangfan Zhang, Shao Zhang, Kangcong Li, Chen Zhang, Yang Chen, Yiqun Zhang, Lei Bai, and Shuyue Hu. Self-Harness: Harnesses that improve themselves. arXiv preprint arXiv:2606.09498, 2026.
- [58] Jenny Zhang, Shengran Hu, Cong Lu, Robert Lange, and Jeff Clune. Darwin Gödel machine: Open-ended evolution of self-improving agents. In ICLR, 2026.
- [59] Andrew Zhao, Daniel Huang, Quentin Xu, Matthieu Lin, Yong-Jin Liu, and Gao Huang. ExpeL: LLM agents are experiential learners. In AAAI, 2024.
- [60] Andrew Zhao, Yiran Wu, Tong Wu, Quentin Xu, Yang Yue, Matthieu Lin, Shenzhi Wang, Qingyun Wu, Zilong Zheng, and Gao Huang. Absolute zero: Reinforced self-play reasoning with zero data. In NeurIPS, 2025.
- [61] Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan, Denny Zhou, and Le Hou. Instruction-following evaluation for large language models. arXiv preprint arXiv:2311.07911, 2023.
- [62] Yifei Zhou, Sergey Levine, Jason Weston, Xian Li, and Sainbayar Sukhbaatar. Self-challenging language model agents. In NeurIPS, 2025.

Supplementary Material & Technical Appendix

GUARD: Stabilizing Recursive Self-Improvement with Regret Guidance

Minghe Zhang∗    Xuetao Kang∗    Yifei Ming    Yanfei Chen    Han Yu

Yufan Zhuang    Chen-Yu Lee

Google Cloud

{minghezhang,xuetaok,yifeim,yanfeichen,hanyyu,yufanzhuang,chenyulee}@google.com

∗Equal contribution.

Appendix A Proofs

A.1 Proof of Theorem 1 (Non-Regressive Gating and Concentration)

Proof.

Part (i). If round \(t\) promotes under the parameterized Soft-HURT gate (12)–(13), whether directly (\(W_{t}=\widetilde{W}_{t}\)) or after in-round [iff] repair (\(W_{t}=\widetilde{W}^{\mathrm{rep}}_{t}\) on its re-scored trajectories), the promoted playbook satisfies

where \(\mathrm{Hurt}(W_{t},W_{t-1})=0\) whenever \(\mathcal{Q}^{-}_{t}=\emptyset\). If round \(t\) rejects, \(W_{t}=W_{t-1}\) and \(\Delta_{t}=0\). The incumbent score used by the gate is the score recorded when the incumbent was itself evaluated, so the increments telescope and give (14) with non-negative summands. A band of width \(\delta_{\mathrm{band}}>0\) relative to the incumbent instead admits any candidate with \(\Delta_{t}\geq-\delta_{\mathrm{band}}\), so \(T\) consecutive admissions at \(\Delta_{t}=-\delta_{\mathrm{band}}\) accumulate a loss of \(T\delta_{\mathrm{band}}\); a band relative to the best score so far bounds the aggregate loss by \(\delta_{\mathrm{band}}\) but leaves per-task regressions unbounded.

Part (ii). By (11),

and promotion requires \(\mathrm{Hurt}&lt;\Delta_{t}\), which is (15); whenever \(\mathcal{Q}^{-}_{t}=\emptyset\) (in particular when \(h_{\max}=0\)), the left-hand side vanishes.

Part (iii). Conditional on everything observed before a candidate harness evaluation, its \(|\mathcal{Q}_{g}|N_{\mathrm{rep}}\) errors \(\{S(\tau_{q,r})-\mu_{q}(W)\}_{q\in\mathcal{Q}_{g},\,r\leq N_{\mathrm{rep}}}\) are independent across tasks and replicates and \(\sigma\)-sub-Gaussian, so \(\bar{S}(W)-\mu(W)\) is \(\sigma/\sqrt{|\mathcal{Q}_{g}|N_{\mathrm{rep}}}\)-sub-Gaussian and

Over \(T_{\max}\) rounds, each group evaluates \(W_{0}\), \(M\) pool candidates per round, and at most \(\mathbb{I}_{\mathrm{rep}}\in\{0,1\}\) repaired candidate per round, giving at most \(n_{\mathrm{eval}}=1+T_{\max}(M+\mathbb{I}_{\mathrm{rep}})\) harness evaluations per group and \(n_{\mathrm{eval}}|\mathcal{G}|\) across all groups. Choosing \(\xi=\sigma\sqrt{2\log(2n_{\mathrm{eval}}|\mathcal{G}|/\alpha)/(|\mathcal{Q}_{g}|N_{\mathrm{rep}})}\) makes each tail probability at most \(\alpha/(n_{\mathrm{eval}}|\mathcal{G}|)\). A union bound over the at most \(n_{\mathrm{eval}}|\mathcal{G}|\) evaluations gives \(|\bar{S}-\mu|\leq\xi\) for all of them with probability at least \(1-\alpha\); the union bound remains valid although later candidates and repairs depend adaptively on earlier noise, because each tail bound holds conditionally on the past. On this event,

which is (16).

Part (iv). With per-group gating, group \(g\) advances in a round with probability \(a_{g}\), so the expected fraction of advancing groups is \(\frac{1}{|\mathcal{G}|}\sum_{g}a_{g}\). A single global gate advances only if every group’s candidate passes, which under independence has probability \(\prod_{g}a_{g}\). For equal \(a_{g}=a\) the ratio is \(a/a^{|\mathcal{G}|}=a^{1-|\mathcal{G}|}\) (e.g., \(8\times\) for \(|\mathcal{G}|=4\) and \(a=0.5\)). ∎

A.2 Proof of Theorem 2 (Targeted Repair vs. Passive Discovery)

Proof.

Part (i). The passive learner must observe every invariant, so \(T_{\mathrm{passive}}\geq\max_{j}G_{j}\), where \(G_{j}\sim\mathrm{Geom}(p_{j})\), supported on \(\{1,2,\dots\}\), is the first round in which invariant \(j\) surfaces and the \(G_{j}\) are independent. Because \(p_{j}\leq\epsilon&lt;1\), each \(G_{j}\) stochastically dominates \(G^{\prime}_{j}\sim\mathrm{Geom}(\epsilon)\), and independence carries the dominance to the maxima. Couple \(G^{\prime}_{j}=\lceil E_{j}\rceil\geq E_{j}\) with \(E_{1},\dots,E_{J}\) i.i.d. exponential of rate \(\nu=-\log(1-\epsilon)\); the coupling is exact since

By the Rényi representation of exponential order statistics, \(\max_{j}E_{j}\stackrel{{\scriptstyle d}}{{=}}\sum_{\ell=1}^{J}X_{\ell}/(\ell\nu)\) with \(X_{\ell}\) i.i.d. \(\mathrm{Exp}(1)\), so for all \(\epsilon\in(0,1)\),

using \(-\log(1-\epsilon)\leq\epsilon/(1-\epsilon)\) on \((0,1)\) (giving \(\Omega((\log J)/\epsilon)\) when \(\epsilon\leq 1/2\)). For example, \(J=10\) and \(\epsilon=0.05\) give \(\mathbb{E}[T_{\mathrm{passive}}]\geq 57.1\) rounds.

Part (ii). Let \(u_{t}\) be the number of invariants still unresolved after round \(t\) (\(u_{0}=J\)), and let \(\mathcal{F}_{t}\) be the history of the first \(t\) rounds. By (a) and (d), resolved invariants never displace unresolved ones in the ranking and stay resolved.

Phase 1 (\(u_{t-1}\geq b_{\min}\)). By (b) and (c), on the event \(\{t_{1}>t-1\}\in\mathcal{F}_{t-1}\) where \(t_{1}=\min\{t:u_{t}&lt;b_{\min}\}\), at least \(b_{\min}\) unresolved invariants are targeted and

The stopping time \(t_{1}\) is integrable because each active round resolves at least one invariant with probability at least \(\rho\). Defining \(Z_{t}=(J-u_{t})-\rho\,b_{\min}t\), the stopped process \(Z_{t\wedge t_{1}}\) is a bounded-increment submartingale; optional stopping yields

Phase 2 (\(u_{t_{1}}&lt;b_{\min}\)). Conditional on \(\mathcal{F}_{t_{1}}\), if \(u_{t_{1}}=0\) (in particular whenever \(b_{\min}=1\)), zero further rounds are needed; if \(1\leq u_{t_{1}}\leq b_{\min}-1\), every remaining invariant is targeted in every subsequent round and resolved independently with probability at least \(\rho\), so the conditional remaining time is stochastically dominated by the maximum of \(u_{t_{1}}\leq b_{\min}-1\) independent \(\mathrm{Geom}(\rho)\) variables. With the coupling of Part (i) at rate \(\nu^{\prime}=-\log(1-\rho)\geq\rho\), this maximum is at most \(1+\max_{j}E^{\prime}_{j}\), whose conditional expectation is at most \(1+H_{b_{\min}-1}/\nu^{\prime}\leq 1+H_{b_{\min}-1}/\rho\).

Taking unconditional expectations and adding the two phases gives (18), which does not involve \(\epsilon\). (Under all-or-nothing bundle admission with joint pass probability \(\rho_{\mathrm{bundle}}>0\) per round, each accepted round resolves \(\min(b_{\min},u_{t-1})\) invariants, requiring at most \(\lceil J/b_{\min}\rceil\) accepted bundles of mean waiting time \(1/\rho_{\mathrm{bundle}}\) each.) ∎

A.3 Proof of Proposition 1 (Strict Regression Dominance under Multi-Rollout Grading)

Proof.

When round \(t-1\) promoted, (4) gives \(\Delta_{\mathrm{gap},t}(c)=1-o_{c}\) and \(\Delta_{\mathrm{hurt},t}(c)=\max(0,\delta_{c})\) for any numbers of rollouts graded under \(W_{t-2}\) and \(W_{t-1}\), so \(\mathrm{Priority}_{t}(c)=(1-o_{c})+\max(0,\delta_{c})\). For a regressed criterion \(c\) (\(\delta_{c}>0\)) and a non-regressed criterion \(c^{\prime}\) (\(\delta_{c^{\prime}}\leq 0\), so \(\Delta_{\mathrm{hurt},t}(c^{\prime})=0\)),

Part (i). If \(o_{c^{\prime}}\geq o_{c}\), the right-hand side is at least \(\delta_{c}>0\).

Part (ii). The right-hand side is positive if and only if \(o_{c}-o_{c^{\prime}}&lt;\delta_{c}\). In the single-rollout binary case (\(K_{\mathrm{gr}}=1\)), a fresh regression has \(o_{c}=0\) and \(\delta_{c}=1\), so \(\mathrm{Priority}_{t}(c)=2\), whereas every non-regressed criterion has \(\mathrm{Priority}_{t}(c^{\prime})=1-o_{c^{\prime}}\leq 1\).

Part (iii). In any round (promoted or rejected), both \(\Delta_{\mathrm{hurt},t}(c)\) and \(\Delta_{\mathrm{gap},t}(c)=1-\mathrm{obey}(c;W_{t-1})\) in (4) are non-negative, so \(\mathrm{Priority}_{t}(c)=0\) holds if and only if \(\mathrm{obey}(c;W_{t-1})=1\) and \(\Delta_{\mathrm{hurt},t}(c)=0\). Because each verdict \(r(\tau,c)\) is binary, \(\mathrm{obey}(c;W_{t-1})=1\) holds exactly when every trajectory in \(\mathcal{T}_{c}(W_{t-1})\) obeys \(c\); hence no criterion failed by \(W_{t-1}\) and no regressed criterion (\(\Delta_{\mathrm{hurt},t}(c)>0\)) is ever pinned. ∎

Appendix B Harness Instantiation Used in Our Experiments

This appendix lists the concrete constants and baseline details for §2 and §4–§5.

- • 

Soft-HURT parameters, pool reward, and ledger window: Single-task noise floor \(\delta_{\mathrm{noise}}=15\) points on \([0,100]\) (fixed across all suites without per-domain tuning); default trade-off budget \(h_{\max}=1\) hurt task and margin \(\mu_{\min}=1.5\) points (on the professional suites, \(h_{\max}=\mathrm{round}(0.18\,|\mathcal{Q}_{g}|)\), \(\mu_{\min}=3.0\), and at least two helped tasks; on multi-stage continual tool/skill and drift suites, un-repaired candidates use conservative threshold \(h_{\max}=0\) and trigger in-round [iff] repair up to \(h_{\mathrm{rep}}\in\{1,2,3\}\) with re-executed Soft-HURT evaluation at \(h_{\max}=1,\mu_{\min}=0\)); active deduplicated rejection-ledger read-back window \(L_{\max}=12\) entries per group on hosted EvoHarnessBench, \(L_{\max}=40\) in the reference candidate-level runner (Drift Gauntlet, local EvoHarnessBench, and PAST-Bench), and all active deduplicated criterion-removal entries in the professional-suite runner; \(\mathrm{Perf}_{m}=\bar{S}^{\mathrm{strict}}(\widetilde{W}^{(m)}_{t})+\tfrac{1}{4}\,\bar{S}(\widetilde{W}^{(m)}_{t})\) (estimated by the critic under critic scoring), \(\beta=3.5\), \(\gamma=1.5\), stabilizer \(10^{-6}\), contrast threshold \(\delta_{\mathrm{con}}=10\) points; pool size \(M=2\) across all main-text, local-gym, and Fin-Rate & Ledger runs and \(M=4\) on PRBench-Legal & Harvey LAB (reaching \(66.67\%\) Official; an \(M=2\) prior-free run reaches \(65.76\%\), and an exploratory \(M=4\) hosted run reaches \(76.42\%\)), initialized from \(s_{0}\) across all \(M\) parallel candidates in Round 1 and evolved via \(m^{+}\) vs. \(m^{-}\) (\(m^{-}\neq m^{+}\)) in rounds \(t\geq 2\) (Appendix B.4).

- • 

Suite-level Soft-HURT validation buffers: Hosted and local EvoHarnessBench gate candidates on cumulative visible stage tasks (\(5/5\) stage promotions admitted cleanly under Soft-HURT: \(1\) hosted, \(4\) local); at each new stage, the local runner also re-checks the carried incumbent against \(W_{0}\) with the same Soft-HURT rule on the expanded training split and returns to \(W_{0}\) if it fails, which happened once (HR, Stage v2). Drift Gauntlet gates against a \(24\)-task stratified validation buffer combining current-block UED frontier tasks with up to \(10\) Vitter Algorithm R reservoir replay samples sharing the pre-execution observable tool/schema signature observable_domain_sig (promoting \(9/12\) blocks, including in-round [iff] repair on ScienceWorld under domain drift, and rejecting \(3/12\) blocks where hurt equaled lift). PAST-Bench applies Soft-HURT (\(\delta_{\mathrm{noise}}=15,h_{\max}=1,\mu_{\min}=1.5\)) to per-task scores from the joint critic pass (\(24/24\) round winners admitted across \(12\) families; §5). The two professional suites gate strictly on TRAIN pre-execution checklist self-reviews (\(\delta_{\mathrm{noise}}=15\), in-round [iff] repair; PRBench-Legal gates \(m^{\star}=\arg\max_{m}\hat{A}_{m}\) as in Algorithm 1, while Fin-Rate & Ledger evaluates across the candidate pool), while post-hoc DEV uses the sealed official rubric (Table C.2).

- • 

Rounds and replicates: Although the reference runner supports early stopping (\(&lt;0.5\)-point macro gain with \(&lt;2\) net-helped tasks, no group promoted, or \(T_{\max}=5\)), all reported experiments fix the round count: 1 per teach/update episode on PAST-Bench; 1 per stage \(\texttt{adapt}(v_{k})\) on EvoHarnessBench (v1–v3, and v1–v4 on ITSM); 1 per online task block \(k\in\{1,\dots,K\}\) on Drift Gauntlet (\(K\in\{2,3,4\}\)); and 3 adaptation rounds (R1–R3 from baseline \(\texttt{R0}=W_{0}\)) on the two professional suites. Main-text and local-gym suites use \(N_{\mathrm{rep}}=1\) and the two professional suites use \(N_{\mathrm{rep}}=2\) evaluation replicates per task.

- • 

Benchmark rollout notes: Under unified Gemini 4 (\(8\)-step agent budget/task on hosted EvoHarnessBench), Layer 1 verifies a final answer and required state mutations while Layer 2 grades task-derived criteria on cumulative stage tasks (\(12\), \(16\), and \(18\) at v1–v3), and an identical single-re-execution pass re-ran relay/tunnel infrastructure outages across every arm under the unchanged harness state before aggregating Table 2, leaving \(0\) errored records in all six final 43-task rows (\(6\) infra-errored records occurred only in intermediate cell \((\text{Cohort }\texttt{v1},H_{v_{2}})\), which enters no reported column). All five hosted GUARD configurations evaluated in our study (the reported \(M{=}2\) main arm at \(80.80\%\) in Table 2, its original-distiller control at \(75.57\%\), the initial one-layer run at \(75.98\%\) in Table 4, a fixed-persona \(M{=}2\) variant at \(76.69\%\), and an \(M{=}4\) operator pool at \(76.42\%\)) beat the top external baseline (\(74.52\%\), Meta-Harness). On Drift Gauntlet [5] (single-model Gemini 4, seed \(42\)), every task exposes a pre-execution observable environment/schema signature (bfcl, sciworld, or bird:&lt;db_id>) without any hidden block index or group label; each signature’s section is bounded t
