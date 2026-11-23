---
title: "HarnessOpt-Bench: Evaluating LLMs at Harness Optimization"
type: "raw-source"
url: "https://arxiv.org/html/2608.06301v1"
author: "Varun Ursekar Affiliation Scale AI"
publication: "arXiv"
published: "2023-06-23"
archived: "2026-11-22T17:00:51Z"
---

> [!quote] Original source
> **Author(s):** Varun Ursekar Affiliation Scale AI  
> **Title:** HarnessOpt-Bench: Evaluating LLMs at Harness Optimization  
> **Published in:** arXiv  
> **Date:** 2023-06-23  
> **Original:** <https://arxiv.org/html/2608.06301v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-harnessopt-bench-evaluating-llms-at-harness-optimization|Source note]]
Themes: [[Loop engineering]]
Why it was archived: How do layered evals interact with agentic harness evolution, where the harness itself is being optimized?

## Archived text

varun.ursekar@scale.com | https://scale.com/research

HarnessOpt-Bench: Evaluating LLMs at Harness Optimization

Abstract

As LLMs are increasingly deployed within agentic systems, their capabilities depend not only on the model weights but also on the harness: the prompts, tools, control flow, memory, and orchestration code surrounding them. This makes automated harness optimization – the iterative and evaluation-guided improvement of a harness by an AI system – both an important route to improving AI systems and a demanding capability for AI systems themselves. Yet the community lacks a common protocol for measuring how well frontier LLMs perform at this task. We introduce HarnessOpt-Bench, a benchmark for end-to-end harness optimization under expensive and stochastic evaluation. An optimizer, an LLM paired with a coding harness, receives a target agent’s seed harness, graded evaluation feedback, and a fixed target-evaluation budget. It edits the harness and nominates a final candidate, which is scored by its normalized gain over the seed on a held-out test partition that remains inaccessible throughout search. A trusted execution environment enforces the evaluation boundary, meters target-agent resource use, and preserves candidate versions for audit. We evaluate 5 frontier LLMs as optimizers both under a shared coding harness and under their native harnesses across 4 downstream tasks, over 111 scored runs. Experiment results show that optimizer models separate more than the coding harnesses they act through, native harnesses are not consistently superior, and gains vary substantially across tasks and seed regimes. These results establish harness optimization as a measurable and discriminative capability with large space for improvement.

1 Introduction

Language models are increasingly deployed within harnesses: the programs that specify their prompts, tools, control flow, context and memory, and the orchestration code invoking them [26, 25, 27]. The same model can exhibit substantially different capabilities under different harnesses [30, 38], which makes harness optimization – the iterative improvement of a harness on a measured outcome under a fixed budget – an increasingly important part of building capable AI systems.

Recent work asks whether AI systems can automate this process, extending a broader line on self-improving agents, agent meta-optimization, and automated research [20, 14, 28]. These approaches differ in the role they assign the model. ShinkaEvolve [11] and GEPA [1] use it as a mutation operator inside a larger evolutionary procedure, whereas VeRO [23] and MetaHarness [12] use coding agents as end-to-end optimizers that edit the harness as a codebase.

Which role a domain calls for depends on the cost of one reliable evaluation, and that cost is what makes harness optimization a test of more than coding ability. A test suite reports cheaply whether a code change is correct; the effect of a harness change must be estimated by running a stochastic agent over many cases, at substantial cost. An optimizer must therefore diagnose failures from incomplete evidence, implement system-level changes, spend a limited evaluation budget, separate real improvement from noise, and decide what to deploy. Where evaluation is cheap, selection over many candidates substitutes for reasoning about any one of them; where it is expensive and noisy, reasoning from prior evidence becomes the capability itself. As the systems being optimized grow more complex, evaluating them only gets more expensive, so the second regime is the one that increasingly matters. Our benchmark specifically targets tasks whose evaluation is itself costly and noisy (fixed-corpus research, terminal use) rather than ones that are cheap to score.

Independent of its place in that self-improvement loop, harness optimization is also long-horizon, plays out over a diverse and complex tool ecosystem rather than a narrow action space, and requires reasoning-driven interpretation of a stochastic system in pursuit of a measured metric rather than production of a single correct step. Each property is already the target of separate benchmarks; a task that combines all three is a demanding test of frontier capability in its own right.

Measuring the capability requires controlling how apparent improvement can arise. Methods are today evaluated with their own target agents, seeds, budgets, disclosure policies, and scoring protocols, so their results conflate the optimizer model, the coding harness it acts through, the target agent, and the protocol. Separating them requires three conditions: the target model, environment, and verifier held fixed; the final evaluation held out throughout search, so improvement reflects generalization rather than fit to a visible score; and a trusted execution boundary that enforces the budget, blocks access to held-out state, and preserves every candidate for audit. Under these conditions three questions become answerable: whether frontier models can be distinguished at this task (RQ1), where they fall short (RQ2), and how much the optimizer’s own coding harness contributes relative to the model (RQ3).

We make the following contributions:

- • 

A controlled benchmark for harness optimization. We introduce HarnessOpt-Bench, in which an optimizer—an LLM paired with a coding harness—receives a target agent’s seed harness, graded development and validation feedback, and a fixed target-evaluation budget. It edits the harness and nominates a final candidate, which is scored by its normalized gain over the seed on a held-out test partition that remains inaccessible throughout search.

- • 

A trusted, reproducible evaluation protocol. The suite comprises 4 downstream tasks with pinned seeds, fixed and non-overlapping development, validation, and test splits, graded disclosure, and recorded baselines for both the seed and off-the-shelf harnesses. A trusted execution environment, building on VeRO [23], enforces access and target-evaluation budgets, isolates held-out state, meters resource use, and versions every candidate for audit (Figure 1).

- • 

A controlled evaluation of optimizer models and coding harnesses. We evaluate five frontier optimizer models under a shared coding harness and their respective native harnesses across 4 downstream tasks, yielding 111 scored optimizer runs, and evaluate two additional coding harnesses on one task. Under this paired design, differences among optimizer models using the shared harness are larger on average than the corresponding differences between shared and native harnesses. Native harnesses provide no consistent advantage, and achievable gains vary substantially across tasks and seed regimes (RQ1, RQ3).

- • 

Evidence of remaining capability gaps. Release-level experiments show that HarnessOpt-Bench resolves variation among successive optimizer-model releases on OfficeQA (Section 5.2). Instrumented search trajectories show that broader intervention is associated with greater held-out gain, whereas detailed failure-trace inspection is rarely used and is not positively associated with gain (Section 5.3).

Although our experiments use coding agents as end-to-end optimizers, HarnessOpt-Bench is agnostic to optimizer design: any system that operates within the prescribed budget, edits the seed harness, and nominates a final candidate can enter. In this way, HarnessOpt-Bench turns harness engineering from an optimizer-specific demonstration into a reproducible evaluation target for measuring and developing systems that improve AI agents.

2 Related Work

Automated code and harness optimization.

A long line of work, encompassing OPRO, FunSearch, AlphaEvolve, and ShinkaEvolve, has applied LLMs within larger search scaffolds to discover novel or optimized programs [29, 22, 17, 11]. Existing approaches to harness optimization differ along two axes: which parts of the harness they may modify, and the role assigned to the LLM during search. Prompt optimization methods such as DSPy [10] optimize prompts while holding the surrounding program fixed. Meta Context Engineering [31] searches over skills and context artifacts in a bi-level procedure. TextGrad [34], Trace [7], and LLM-AutoDiff [32] optimize arbitrary text components in chained workflows by back-propagating textual feedback using LLMs. GEPA [1] optimizes textual artifacts by using reflective feedback to guide an evolutionary process. A second line expands the search space to the agent program itself: STOP [35] recursively improves a scaffolding program. ADAS [8] searches over agent designs represented as code. AFlow [37] performs tree search over code-defined workflows. Darwin Gödel Machine [36], Gödel Agent [33], and SICA [21] study recursive self-modification.

Closest to the regime HarnessOpt-Bench measures are optimizers that act end-to-end: Ursekar et al. [23] and Lee et al. [12] let a coding agent read the target source, inspect scores and execution traces from prior candidates, and choose what evidence to gather, rather than orchestrating mutations in a fixed search algorithm. Other systems in this regime include Agentic Harness Engineering [13] and HarnessX [5]. Several of these works contribute optimization methods, evaluated on method-specific seeds, budgets, search spaces, and scoring protocols, which makes their reported outcomes difficult to compare. HarnessOpt-Bench is complementary: it fixes the optimization problem and the evaluation protocol so that optimizer models, harnesses, and search algorithms can be compared on common ground. HarnessOpt-Bench builds upon the infrastructure and protocol in VeRO and contributes a suite of optimization tasks.

Coding agent benchmarks.

Coding agent evaluation has grown from function-level synthesis [4, 2] to repository-scale tasks in real execution environments [9], and tasks requiring iterative optimization, such as machine learning engineering [3] and kernel optimization [19]. HarnessOpt-Bench similarly requires coding agents to navigate the target system codebase and iterate on environmental feedback; it differs in what the optimization target is (i.e. a harness), the noisiness of evaluation feedback, and the types of bounds imposed on its search.

3 HarnessOpt-Bench: Harness Optimization as a Task

Harness optimization is a constrained, stochastic program-optimization problem. Algorithm 1 summarizes the interaction protocol an optimizer must satisfy; this section defines each element in its general form, then fixes it for this work.

3.1 The optimization problem

Candidates and invariants.

A candidate harness \(H\) is an executable codebase. No semantic partition is imposed between prompts, tool definitions, memory, and control flow. The optimizer may edit, add, or delete files subject to a fixed execution interface and a small set of immutable paths. We write \(\mathcal{H}\) for the feasible set and \(H_{0}\in\mathcal{H}\) for the pinned seed. A task additionally fixes invariants \(\theta=(\mathcal{M},E,V)\): the models \(\mathcal{M}\) available to a candidate, the environment \(E(x)\) associated with each case \(x\), and the verifier \(V\) mapping a completed trajectory to a score in \([0,1]\). The optimizer may change \(H\) but not \(\theta\); changing \(\theta\) defines a different task, not a different candidate. A harness’ web access, for example, might be controlled by \(E\).

Evaluation and disclosure.

Cases are partitioned into disjoint development, validation, and test sets, \(\mathcal{D}^{\mathrm{dev}}\), \(\mathcal{D}^{\mathrm{val}}\), and \(\mathcal{D}^{\mathrm{test}}\). Executing harness \(H\) on case \(x\) produces a stochastic trajectory \(\tau\sim\operatorname{Rollout}(H,\theta,x)\), to which the verifier assigns score \(V(\tau,x)\). We define the expected score on partition \(\mathcal{D}\) as

and abbreviate \(\mathcal{E}_{\theta}(H;\mathcal{D}^{\mathrm{test}})\) as \(\mathcal{E}_{\theta}(H)\). During search, the optimizer may request an evaluation of \(H\) on a subset \(Q\subseteq\mathcal{D}^{\mathrm{dev}}\) or \(Q\subseteq\mathcal{D}^{\mathrm{val}}\):

where \(\hat{s}\) estimates aggregate performance on \(Q\) (e.g. sample mean) and \(\varphi\) contains per-case outcomes and execution traces. A partition-specific disclosure policy \(\pi_{\mathcal{D}}\) determines which of these outputs the optimizer observes. Development reveals case inputs, per-case outcomes, and traces to support diagnosis; validation reveals only an aggregate score to support selection. The test partition is inaccessible during search and is evaluated by the trusted server only after the optimizer nominates a candidate.

Budget.

Each evaluation request \(j\) incurs a non-negative cost vector \(c_{j}\in\mathbb{R}_{\geq 0}^{d}\), and search must satisfy \(\sum_{j}c_{j}\leq B\) componentwise for a fixed budget vector \(B\), so the optimizer chooses what to evaluate and at what fidelity. In HarnessOpt-Bench, the primary components of \(B\) are caps of 100 evaluation calls per partition and four full case passes on each of the development and validation partitions, plus a cap on total expendable target-model tokens. The optimizer’s own inference is metered for observability but uncapped in this work, though the framework permits capping it.

Optimizer.

An optimizer \(O\) is any program satisfying the interface of Algorithm 1 that receives \(H_{0}\), interacts with \(F_{\theta}\) under disclosure \(\pi\) and budget \(B\), produces candidates \(H_{1},\ldots,H_{T}\in\mathcal{H}\), and nominates a final candidate \(H^{+}\). In our work, the optimizer is an LLM operating through a coding harness.

Objective.

The optimizer maximizes the expected improvement of its nominated candidate over the pinned seed on the held-out partition,

Since \(H_{0}\) is pinned, \(\mathcal{E}_{\theta}(H_{0})\) is a constant within a task. Because test disclosure is empty, the optimizer never observes the quantity it maximizes. Raw improvement may not be comparable across tasks whose scoring scales differ, so wherever tasks are compared we use normalized gain

where negative values indicate a nominated candidate worse than the seed.

3.2 The HarnessOpt-Bench suite

Every pinned seed \(H_{0}\) across HarnessOpt-Bench tasks is a small, deliberately untuned Python harness that leaves obvious headroom. Three of the four are competent but naive; the OfficeQA seed, for example, is a \(\sim\)130-line agent built on the OpenAI API, with three tools, a 24-turn loop, and a generic system prompt. GAIA’s is a non-functional stub.

Table 3 in the appendix compares the pinned seeds \(H_{0}\) to a number of open-source harnesses, showing that they perform comparably or worse than the weakest ones, providing ample headroom for improvement. The environment and the verifier are taken directly from each benchmark; environmental constraints such as limited network access and strict wall clock bounds are used without modification. Across all tasks, \(|\mathcal{M}|=1\), i.e. we use one pinned target model per task; these are listed in Table 3. Target models were chosen so that the seed would land in a measurable mid-range rather than at the floor or the ceiling.

Each task’s \(\mathcal{E}_{\theta}(H_{0})\) is measured once, averaged over \(K{=}3\) independent rounds, and pinned for reproducibility; a nominated candidate is likewise scored three times per test case and averaged. Because repeated scores can differ, we summarize this evaluation noise with a task-specific resolution band (Section 4); smaller differences are treated as unresolved.

Figure 1 details our execution infrastructure. Each optimizer is run in an isolated sandbox with evaluation results, task data, and the target harness in the filesystem. Similarly, each target agent rollout is performed in an ephemeral sandbox to control for noise introduced by environmental drift.

4 Experimental Setup

Task grid.

We evaluate five optimizer models from three developers on all four optimization tasks in our suite: claude-opus-5, claude-sonnet-5, gpt-5.6-sol, gpt-5.6-terra, and kimi-k3, chosen as the current frontier release of each family. Each model is paired with two coding harnesses: a shared harness (opencode), held fixed across all models, and the model’s native harness, namely claude-code for the Claude models, codex for the GPT models, and kimi-cli for Kimi. We refer to each model–harness pair as an optimizer configuration, giving 10 configurations in our core grid. Comparing models under opencode holds the coding harness fixed; comparing a model across opencode and its native harness measures sensitivity to scaffold choice. We run two additional harnesses – goose and mini-swe-agent– across all models on GAIA to compare sensitivity across optimizer harnesses. Finally, for two of the five models – claude-opus and gpt-5.x – we run earlier releases of the same family using each family’s native harness on OfficeQA, supporting the capability ladder we present in Section 5.2. The complete per-task results, including observed run ranges and properties of the generated harnesses, are reported in Appendix A (Table 2).

Scoring protocol.

Scoring follows the protocol of Section 3.2: each held-out evaluation is the mean of three attempts per test case, matching the \(K{=}3\) pooling behind each task’s pinned baseline. Each optimizer configuration is run twice; we report ranges in Table 2. The optimizer model’s inference is metered but left uncapped, so these results estimate what is achievable when the optimizer model’s reasoning is not the scarce resource.

Analysis protocol.

Three choices govern the analyses in Section 5.

- • 

Outcome. We report the normalized gain \(g\) of Eq. 3: the fraction of the headroom above the pinned baseline that an optimizer captured.

- • 

Measurement resolution. We estimate evaluation noise by scoring the same candidate twice on the same cases and carry the median discrepancy to the \(K{=}3\) normalized-gain scale used for held-out scoring. The resulting task-specific resolution band is a descriptive threshold: differences smaller than the band are treated as unresolved, not as formal significance-test results. Table 1 reports each task’s band.

- • 

Composite model score. Normalized gain is defined within a task; normalization places tasks in common headroom units but does not remove systematic differences among them. To obtain a cross-task score for optimizer model \(m\), let \(g_{mtr}\) denote its normalized gain on task \(t\) in qualifying replicate \(r\) under the shared harness, and first average replicates: We then decompose these configuration-level gains as where \(\tau_{t}\) absorbs task-level differences and \(\lambda_{m}\) is the optimizer model effect. Because the shared-harness grid is balanced, We define \(\operatorname{LSS}_{\lambda}(m)=\widehat{\lambda}_{m}\). Thus LSS-\(\lambda\) is the model’s task-adjusted mean performance relative to the evaluated models’ grand mean, expressed in normalized-gain units; higher is better. The primary score uses the shared-harness runs on the tasks with competent seeds. Native-harness runs are excluded to hold the scaffold fixed.

5 Results

Table 1 compares the core experimental configurations across tasks on normalized gain. Appendix A reports the same results in Table 2, together with run ranges and properties of the generated harnesses by task.

5.1 Distinguishing frontier models

Model choice has a larger effect than coding-harness choice. Holding task and harness fixed, changing the optimizer model moves gain by 0.142 on average; holding task and model fixed, changing the harness moves it by 0.079. The model contrast is therefore about \(1.8\times\) larger. Both exceed the task resolution bands, although the harness contrast does so narrowly.

The extremes separate more clearly than the middle. The strongest configuration captures roughly two thirds of the available OfficeQA headroom and half of the BrowseComp-Plus headroom, while the weakest is unresolved from zero on BrowseComp-Plus and Terminal-Bench. Differences among intermediate configurations are often smaller than their round-to-round variation, supporting tiers rather than a complete ranking. Figure 2 shows the run-level spread and the corresponding task-adjusted model effects.

5.2 Tracking model progress

We test sensitivity to model progress using two OfficeQA release series, holding the target model, seed, budget, and coding harness fixed within each series. Across 5 GPT releases, gain rises monotonically from +0.03 to +0.49, with three of its four steps exceeding the task’s resolution band. Across 5 Claude Opus releases, gain ranges from +0.37 to +0.59; gain is non-monotonic, but the first-to-last spread exceeds the task’s resolution band.

5.3 Where current optimizers fall short

Trajectory-derived measures characterize how optimizers search; they are not independent measures of held-out capability.

Broader search is associated with greater gain.

We identified eight harness levers on OfficeQA before examining the other tasks: prompt, context management, step cap, retry and timeout policy, tool schema, answer extraction, retrieval policy, and reasoning effort. The fraction touched during search is positively associated with gain on every task, with \(\rho\) ranging from \(+0.34\) to \(+0.88\) (Figure 4). No other process measure we investigated had the same direction on all four tasks.

This is exploration rather than final candidate breadth. An optimizer may inspect or modify a lever without retaining the change: one configuration touched three quarters of the levers and made seven edits but shipped the original seed. Breadth is also correlated with total modification volume, so the data do not isolate breadth from search effort.

Trace reading is not associated with higher gain.

The share of actions spent reading evaluation output is negatively associated with gain across the four tasks, from \(-0.31\) to \(-0.64\). Optimizers rely mainly on per-case score summaries: detailed trace spans were requested only 16 times by 7 of the 111 cells. This does not establish that diagnosis is unnecessary. For these tasks, per-case summaries may localize failures well enough that reading full traces does not justify its context cost.

Case passes, not evaluation calls, bind.

The development and validation partitions each permit 200 evaluation invocations and four full case passes. The median optimizer uses 8 calls (4%) but 82% of its case allowance, and 55 of 100 cells exhaust at least one partition’s case budget. Thus the case allowance constrains search, whereas the call cap does not.

Visible validation scores are optimistic.

Most cells in Figure 13 fall below the identity line: the submitted candidate’s test score is lower than the best validation score observed during search. The held-out partition is therefore necessary to measure realized gain. The figure cannot distinguish selection-induced overfitting from a validation–test mismatch, so we claim only that the visible best score is optimistic.

5.4 The effect of the optimizer’s own harness

Across the 20 model–task pairs evaluated under both conditions, the shared harness wins 11, the native harness wins 9, and 0 are tied. Native harnesses therefore have no consistent advantage. Restricting evaluation to a model’s native tooling would not provide a reliable estimate of its harness-optimization ability.

In 11 pairs, the difference exceeds the task’s resolution band, but the direction varies by model and task. The aggregate near-tie therefore reflects heterogeneous effects rather than uniformly small ones.

Figure 5 shows where the effect does live, on GAIA — the only task whose harness axis has more than two levels. The harnesses do not hold their rank across models, and the native-harness advantage is concentrated rather than absent: both GPT models are four to five resolution bands better under codex, while the two Claudes and Kimi sit within a band or two of zero. Reading only the shared harnesses would miss this, and would suggest that sensitivity to the harness scales with model capability; adding each model’s native harness removes that pattern.

6 Conclusion

Harness engineering is becoming a model capability, not merely infrastructure around one. HarnessOpt-Bench makes that capability an empirical object: can a model diagnose, modify, and improve an agent as measured via a held-out reward? Current frontier models can, but unevenly. The strongest search broadly, yet their gains remain task-dependent and often too close to support a fine-grained ranking. By releasing HarnessOpt-Bench, we make this capability reproducible to measure and concrete to optimize. The next frontier is not merely better agents, but models that reliably make agents better.

Limitations

HarnessOpt-Bench is designed to be hack-resistant, not hackproof. The optimizer cannot access the test partition or alter the target model, environment, or verifier, but repeated development and validation feedback may still reward strategies specific to a fixed evaluation. Future versions should introduce per-run jitter in cases, tool behavior, and verifier implementation to distinguish general improvements from exploitation of stable evaluator artifacts.

The seed harness is itself a task-specific prior. Improving a mature agent tests diagnosis and refinement; starting from a stub tests construction. Our suite contains both regimes but does not vary seed complexity systematically. LSS-\(\lambda\) should therefore be interpreted relative to the present distribution of tasks and seeds. A controlled ladder of harness completeness and architectural complexity would reveal how optimizer performance changes with the strength of this prior.

Finally, candidates are restricted to Python and each task uses one pinned target model. Generalization to other languages, runtimes, agent architectures, and target models remains untested. Broader coverage, matched compute conditions, and additional replication are needed before treating HarnessOpt-Bench as a comprehensive measure of tool-integrated reasoning.

Ethics Statement

This work studies whether and how well LLMs can improve the code of other LLM agents. Automating agent improvement carries a dual-use tension, since the same capability that repairs and strengthens a benign agent could in principle be turned toward a harmful one. The benchmark’s design limits this exposure. The optimization target is always a bounded, benign downstream task (document QA, deep research, multi-step reasoning, or terminal use), the score is the task’s own verifier on a held-out split and nothing else, and every optimizer runs inside a trusted harness that meters spend, versions every change for audit, and confines the target to a fixed model behind an allow-list – a concrete precaution given evidence that comparable agent benchmarks can be gamed via evaluator hijacking or judge prompt-injection [24]. Nothing in the setup rewards or requires acquiring new capabilities, tools, or resources beyond editing a fixed agent’s code.

Our benchmark reuses existing public datasets and benchmarks under their respective licenses and adds seed agents and split definitions that we release. The downstream corpora are public documents, and we introduce no personal or sensitive data. Because agent evaluation is compute-intensive, we report token usage as a first-class metric to make the cost of this line of work visible, and we keep the search budget denominated in evaluation calls and case-runs so that comparisons do not implicitly favor optimizers with larger compute budgets. Finally, we report the completed evaluation, including repeated runs, with explicit caveats (see the Limitations section) and avoid over-claiming fine-grained model rankings.

References

- [1] (2026) GEPA: reflective prompt evolution can outperform reinforcement learning. In The Fourteenth International Conference on Learning Representations, External Links: Link Cited by: §1, §2.
- [2] (2021) Program synthesis with large language models. arXiv preprint arXiv:2108.07732. External Links: Link Cited by: §2.
- [3] (2025) MLE-bench: evaluating machine learning agents on machine learning engineering. In International Conference on Learning Representations (ICLR), External Links: Link Cited by: §2.
- [4] (2021) Evaluating large language models trained on code. arXiv preprint arXiv:2107.03374. External Links: Link Cited by: §2.
- [5] (2026) HarnessX: a composable, adaptive, and evolvable agent harness foundry. External Links: 2606.14249, Link Cited by: §2.
- [6] (2026) BrowseComp-plus: a more fair and transparent evaluation benchmark of deep-research agent. External Links: Link Cited by: Table 3, Appendix B.
- [7] (2024) Trace is the next AutoDiff: generative optimization with rich feedback, execution traces, and LLMs. Advances in Neural Information Processing Systems (NeurIPS). External Links: Link Cited by: §2.
- [8] (2025) Automated design of agentic systems. In The Thirteenth International Conference on Learning Representations, External Links: Link Cited by: §2.
- [9] (2024) SWE-bench: can language models resolve real-world GitHub issues?. In International Conference on Learning Representations (ICLR), External Links: Link Cited by: §2.
- [10] (2024) DSPy: compiling declarative language model calls into self-improving pipelines. In International Conference on Learning Representations (ICLR), External Links: Link Cited by: §2.
- [11] (2025) ShinkaEvolve: towards open-ended and sample-efficient program evolution. External Links: 2509.19349, Link Cited by: §1, §2.
- [12] (2026) Meta-harness: end-to-end optimization of model harnesses. External Links: 2603.28052, Link Cited by: §1, §2.
- [13] (2026) Agentic harness engineering: observability-driven automatic evolution of coding-agent harnesses. External Links: 2604.25850, Link Cited by: §2.
- [14] (2026) RSIBench-data: benchmarking data-centric research for recursive self-improvement. External Links: 2607.25886, Link Cited by: §1.
- [15] (2026) Terminal-bench: benchmarking agents on hard, realistic tasks in command line interfaces. External Links: 2601.11868, Link Cited by: Table 3, Appendix B.
- [16] (2024) GAIA: a benchmark for general AI assistants. In International Conference on Learning Representations (ICLR), External Links: Link Cited by: Table 3, Appendix B.
- [17] (2025) AlphaEvolve: a coding agent for scientific and algorithmic discovery. arXiv preprint arXiv:2506.13131. External Links: Link Cited by: §2.
- [18] (2026) OfficeQA pro: an enterprise benchmark for end-to-end grounded reasoning. External Links: 2603.08655, Link Cited by: Table 3, Appendix B.
- [19] (2025) KernelBench: can LLMs write efficient GPU kernels?. In Forty-second International Conference on Machine Learning, External Links: Link Cited by: §2.
- [20] (2026) PostTrainBench: can llm agents automate llm post-training?. External Links: 2603.08640, Link Cited by: §1.
- [21] (2025) A self-improving coding agent. arXiv preprint arXiv:2504.15228. External Links: Link Cited by: §2.
- [22] (2024) Mathematical discoveries from program search with large language models. Nature 625, pp. 468–475. External Links: Document Cited by: §2.
- [23] (2026) VeRO: a harness for agents to optimize agents. In Forty-third International Conference on Machine Learning, External Links: Link Cited by: 2nd item, §1, §2.
- [24] (2026) Do androids dream of breaking the game? systematically auditing ai agent benchmarks with benchjack. External Links: 2605.12673, Link Cited by: Ethics Statement.
- [25] (2024) A survey on large language model based autonomous agents. Frontiers of Computer Science 18 (6), pp. 186345. External Links: Document Cited by: §1.
- [26] (2023) LLM powered autonomous agents. Note: https://lilianweng.github.io/posts/2023-06-23-agent/ Cited by: §1.
- [27] (2026) Harness engineering for self-improvement. lilianweng.github.io. External Links: Link Cited by: §1.
- [28] (2025) RE-bench: evaluating frontier ai r&d capabilities of language model agents against human experts. External Links: 2411.15114, Link Cited by: §1.
- [29] (2024) Large language models as optimizers. In International Conference on Learning Representations (ICLR), External Links: Link Cited by: §2.
- [30] (2026) Harness-bench: measuring harness effects across models in realistic agent workflows. External Links: 2605.27922, Link Cited by: §1.
- [31] (2026) Meta context engineering via agentic skill evolution. External Links: 2601.21557, Link Cited by: §2.
- [32] (2025) LLM-AutoDiff: auto-differentiate any LLM workflow. arXiv preprint arXiv:2501.16673. External Links: Link Cited by: §2.
- [33] (2025) Gödel agent: a self-referential agent framework for recursive self-improvement. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics, External Links: Link Cited by: §2.
- [34] (2024) TextGrad: automatic "differentiation" via text. External Links: 2406.07496, Link Cited by: §2.
- [35] (2024) Self-taught optimizer (STOP): recursively self-improving code generation. In First Conference on Language Modeling, External Links: Link Cited by: §2.
- [36] (2025) Darwin Gödel machine: open-ended evolution of self-improving agents. arXiv preprint arXiv:2505.22954. External Links: Link Cited by: §2.
- [37] (2025) AFlow: automating agentic workflow generation. In International Conference on Learning Representations (ICLR), External Links: Link Cited by: §2.
- [38] (2026) Stop comparing LLM agents without disclosing the harness. External Links: 2605.23950, Link Cited by: §1.

Appendix A Full optimizer results

Table 2 expands the compact gain comparison in Table 1. It reports the observed range across replicate runs and two properties of the resulting harnesses for every core contestant; the two additional harnesses evaluated on GAIA are included here as well. The generational-ladder runs remain in Figure 3, where release order is the comparison of interest.

Appendix B The suite

Table 3 gives each task’s design constants — its pinned target model, its exact split, and its seed agent’s held-out baseline — together with what the same task scores under each off-the-shelf coding harness on the same held-out partition. Gain is measured against the seed baseline alone (Eq. 3); the off-the-shelf columns are context, not the reference — they say what the task’s headroom is worth to an existing harness that nobody optimized.

Appendix C Model effects

Table 4 gives the model effect in gain units, the numeric form of the ordering Figure 2 plots. Two further estimators of the same quantity are computed and agree with it exactly on the ordering, so the ranking does not rest on the additive assumption; only the gain-unit estimator is reported, because it is the one the body quotes and the only one in units a reader can read directly as a fraction of headroom.

Appendix D Supporting figures

All figures use the same run store and analysis set as the body. Where applicable, points average replicate rounds for one optimizer configuration on one task, and \(\rho\) is Spearman correlation within a task. As in the body, GAIA gain is its raw held-out score and is not pooled with the other tasks.

Appendix E Reproducibility

Each task pins its dataset by immutable reference and its split by a committed manifest. Splits are exact \(20/40/40\) with no overlap, and the split generator verifies the committed tree byte-for-byte. Baselines are the seed agent’s held-out score pooled over \(K{=}3\) rounds and are re-pinned whenever a seed commit moves, using a script that reuses the original evaluation path. Every candidate an optimizer produces is an immutable Git commit, dependencies are pinned by lockfile, and each evaluation runs in an isolated sandbox with per-case timeouts taken from the dataset’s own declared agent clock. The trusted gateway meters each evaluation’s token usage as an input, cached, output, and total split, and stamps request-log records so that per-trial token attribution is reproducible from the run artifacts. Every quantity we report about an optimizer’s process is recomputed from its own execution trace and from the evaluator’s record of which evaluations it ran, so the analysis is reproducible from the released artifacts without re-running any search. The seed agents, split manifests, build configurations, and evaluation harness are released with the benchmark.
