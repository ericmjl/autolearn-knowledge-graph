---
title: "1 Introduction"
type: "raw-source"
url: "https://arxiv.org/html/2607.08124v3"
author: "Jun Nie, Yonggang Zhang, Jun Song, Qianshu Cai, Dahai Yu, Yike Guo, Xinmei Tian, Bo Han"
publication: "arXiv"
published: "2026-01-31"
archived: "2026-11-25T07:01:04Z"
---

> [!quote] Original source
> **Author(s):** Jun Nie, Yonggang Zhang, Jun Song, Qianshu Cai, Dahai Yu, Yike Guo, Xinmei Tian, Bo Han  
> **Title:** 1 Introduction  
> **Published in:** arXiv  
> **Date:** 2026-01-31  
> **Original:** <https://arxiv.org/html/2607.08124v3>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-1-introduction|Source note]]
Themes: [[Loop engineering]]
Why it was archived: How held-out oracles get constructed for harness evolution

## Archived text

TTHE: Test-Time Harness Evolution

Jun Nie1,2, Yonggang Zhang3,*, Jun Song1, Qianshu Cai2, Dahai Yu4, Yike Guo3, Xinmei Tian2, Bo Han1,* 1Hong Kong Baptist University 2University of Science and Technology of China 3Hong Kong Generative AI Research & Development Center, The Hong Kong University of Science and Technology 4TCL Corporate Research (HK) Co., Ltd

Code: https://github.com/junnie00/TTHE

Abstract

The behavior of an LLM agent is determined not only by the underlying model, but also by its harness: the executable program that constructs context, invokes tools, verifies intermediate results, and recovers from failures. Existing approaches typically optimize harnesses on training or development data and freeze the resulting programs at test time, limiting adaptation to shifts in task distributions, failure modes, and tool interactions. We ask whether the harness can instead be optimized during evaluation using unlabeled execution traces. We introduce Test-Time Harness Evolution (TTHE), which treats the executable harness as the state of test-time adaptation. On each unlabeled test batch, TTHE iteratively evolves a population of candidate harnesses through agentic proposers that reason over execution traces and explore diverse edit directions. A judge selects a candidate using execution traces and execution-derived proxy signals. The selected harness determines the current batch’s outputs and initializes adaptation on the next. Crucially, the solver, proposers, and judge operate through different harnesses around the same frozen LLM, without weight updates, access to final-answer labels, or a separately trained adaptation model. Across six execution-grounded benchmarks spanning text-to-SQL, competitive programming, software engineering, data-science coding, terminal-based tasks, and agentic tool use, TTHE improves fixed ReAct-style baseline harnesses through persistent, inspectable program adaptation. These results recast test-time adaptation for LLM agents as evolution over executable control programs and identify execution-derived proxy reliability as a central challenge for robust unsupervised agent improvement.

1 Introduction

Modern LLM agents are increasingly built as executable systems rather than single-call predictors. Their behavior depends not only on the model, but also on the executable harness around it—the control program that constructs context, invokes tools, verifies intermediate results, and implements recovery strategies. Following prior work on model and agent harnesses (Lee et al., 2026; Zhang et al., 2026a), we focus on this program as the object of adaptation. Its context construction and control flow determine how the model’s capabilities are used. A common development workflow, however, is to inspect failures, adjust prompts and control flow, and tune tool-use logic before evaluating the resulting harness as a fixed artifact. Its operating procedure then remains unchanged even when the target workload exposes different requirements or failure modes.

This convention treats evaluation as a scoring stage, even though execution itself produces rich operational evidence. Every attempted task leaves an execution trace: model calls, tool actions, intermediate outputs, database responses, test results, runtime errors, and recovery decisions. Such traces can reveal not only whether an execution satisfies available checks, but also how its operating procedure might be improved. A text-to-SQL agent may retrieve the correct table but apply an inconsistent value normalization; a coding agent may generate plausible patches without verifying them before submission; a data-science agent may compute an intermediate result but omit it from the final report. This is precisely the kind of evidence a human harness engineer would inspect when revising the scaffold. Crucially, this evidence is available during evaluation without access to gold labels.

Using this evidence to revise the harness, however, is different from using it to refine individual responses. Self-debugging and reflection use feedback to revise candidate answers or retain textual experience for later attempts (Chen et al., 2024; Shinn et al., 2023). Automated prompt and workflow search targets the surrounding task-solving procedure, but typically optimizes it against a training or development objective before evaluating the resulting workflow as a fixed artifact (Khattab et al., 2023; Hu et al., 2025; Zhang et al., 2025b). More recent work revises agent source code, harnesses, and configurations using execution feedback or task-level evaluation signals (Cai et al., 2026a; Lee et al., 2026; Zhang et al., 2026a; He et al., 2025). Building on these lines of work, we ask: can an LLM agent adapt its harness at test time using its own execution traces, without final correctness feedback?

We propose Test-Time Harness Evolution (TTHE), which treats the executable harness as the state of test-time adaptation. Rather than searching for a harness on labeled development instances and freezing it for evaluation, TTHE moves harness optimization into the evaluation process itself. On each unlabeled test batch, TTHE executes a population of candidate harnesses and iteratively refines them through trace-guided proposers that explore diverse edit directions. A judge selects one candidate using the traces and execution-derived proxy signals; the selected harness determines the current batch’s outputs and initializes adaptation on the next. Final correctness feedback is used only for post-selection evaluation. The solver, proposers, and judge use the same frozen LLM in different roles, so adaptation changes the executable program rather than model weights and requires no separately trained adaptation model.

This evaluation-time formulation offers two practical advantages. First, it adapts at the point where the relevant evidence appears: after the agent encounters the schemas, repositories, tests, tools, and runtime constraints of the target workload. It can therefore use task-specific execution evidence without requiring an additional labeled development set tailored to that workload. Second, updating an executable program requires no gradient access and permits explicit changes to context construction, multi-sample generation, tool-mediated grounding, deterministic contract checks, and conditional recovery branches. These changes alter the procedure used to solve tasks rather than only revising an individual response.

A central challenge, however, is that execution evidence is not a correctness oracle. A query can execute successfully while answering the wrong question; code can pass visible tests while failing hidden ones. TTHE therefore presents proxy signals together with candidate code and the underlying execution traces, allowing proposers and the judge to interpret these signals in the context of how an outcome was produced rather than relying on a single surrogate score. Because an edit intended to repair a failure can also disrupt previously correct behavior, we complement this design with a conditional analysis of a class of trace-triggered harness edits, characterizing when corrective gains outweigh unintended regressions.

We evaluate TTHE on six execution-grounded benchmarks, where it improves fixed ReAct-style baselines and yields inspectable grounding, verification, and recovery policies. On the evaluated BIRD dataset, TTHE achieves \(48.7\%\) mean execution accuracy over three runs, compared with \(12.7\%\) for the fixed baseline. A separate ten-run execution-result consistency-voting control achieves \(16.0\%\). Harnesses selected by DeepSeek for each BIRD batch also improve MiMo V2.5 and GPT-5.5 over their respective fixed-harness baselines on the corresponding batches, without further harness evolution. These results provide evidence of cross-model transfer of the evolved task-solving procedures. Search diagnostics reveal non-monotonic effects of search budget and distinguish candidate-availability limitations from selection errors. Together, these findings support executable harness adaptation as a practical path to test-time self-evolution in LLM agents.

Contributions.

- • 

We introduce Test-Time Harness Evolution (TTHE), a framework that recasts test-time adaptation as evolution over executable control programs. TTHE enables an LLM agent to transform its own execution experience into harness updates, without modifying model weights or accessing final correctness feedback.

- • 

We demonstrate gains on evaluated tasks across six execution-grounded benchmarks, compare TTHE with fixed-harness repeated sampling on BIRD, and show that batch-specific evolved harnesses can benefit other execution models on the corresponding tasks.

- • 

We present inspectable harness examples, provide a conditional analysis of corrective gains and unintended regressions for a class of trace-triggered edits, and use search diagnostics to distinguish candidate availability from selection errors.

2 Problem Setting

Let \(M\) be a frozen LLM and \(\mathcal{H}\) the space of executable harnesses. A harness \(H\in\mathcal{H}\) orchestrates calls to \(M\) and interactions with an allowed task environment \(E\). Executing \(H\) on input \(x\) produces an outcome \(o_{H}(x)\) and a trace \(\tau_{H}(x)\), with execution randomness suppressed in the notation. Outcomes include submitted artifacts and final environment states relevant to evaluation, not only the agent’s final message.

Current-batch adaptation.

At step \(t\), the agent receives an unlabeled batch \(X_{t}=(x_{t,1},\ldots,x_{t,B_{t}})\) and an incoming harness \(H_{t}\). Starting from \(H_{t}\), the adaptation procedure interacts with \(E\) to construct, execute, and select a candidate harness:

Here \(\widehat{O}_{t}=(\widehat{o}_{t,1},\ldots,\widehat{o}_{t,B_{t}})\) contains the selected candidate’s cached outcomes on \(X_{t}\). After commitment, these outcomes are evaluated against the hidden targets \(Y_{t}=(y_{t,1},\ldots,y_{t,B_{t}})\), without re-execution or reselection:

The task-specific function \(\operatorname{score}\) takes values in \([0,1]\). For binary tasks, it is \(\mathbb{I}[\widehat{o}_{t,i}\equiv y_{t,i}]\), where \(\equiv\) denotes task correctness, such as SQL result-set equality or passing all hidden tests; graded tasks use their evaluation rubric. TTHE sets \(H_{t+1}=\widetilde{H}_{t}\) to initialize adaptation on the next batch. Evaluation is transductive: the current batch supplies unlabeled adaptation evidence and is scored after adaptation, rather than using the incoming harness \(H_{t}\) before adaptation.

Information available to adaptation.

The adaptation loop may access task inputs, candidate source code, execution traces, and permitted environment responses. Public examples or repository tests provide partial checks when exposed by the task. Final-answer labels, reference solutions, hidden-test outcomes, and final evaluation scores remain inaccessible to all adaptation components and their traces; evaluation feedback is not passed to subsequent batches. No calibrated scalar correctness reward is assumed.

Let \(\mathcal{F}_{t}\subseteq\mathcal{H}\) be the final candidate set eligible for selection, and let \(\mathcal{T}_{t}(H)\) collect the execution traces and execution-derived signals for candidate \(H\) on \(X_{t}\). A label-free judge \(\mathcal{J}\) selects a single harness \(\widetilde{H}_{t}\in\mathcal{F}_{t}\):

The judge may acquire additional evidence through permitted probes in \(E\), subject to the same information constraints.

3 Method

3.1 Overview

TTHE adapts an agent’s executable harness using evidence generated during test-time execution. Two questions guide its design: (Q1) What evidence can support adaptation without final correctness feedback? (Q2) How can this evidence guide program revision and candidate selection? We address Q1 with execution traces and task-dependent partial checks, and Q2 with iterative evolution of multiple harness branches followed by batch-level selection. Starting from \(H_{t}\), the loop evolves \(G\) branches over \(R\) rounds on the current batch \(X_{t}\). Figure 1 illustrates one batch; Algorithm 1 in Appendix G gives the full procedure.

3.2 Harness as adaptation state

The adaptation state is the task harness’s source, including its prompts and executable control logic. TTHE revises how the harness constructs context, invokes tools, validates intermediate results, and recovers from failures, while keeping the model and the outer proposal-and-selection procedure fixed. The baseline \(H_{0}\) is a ReAct-style scaffold (Yao et al., 2023), fixed before evolution begins.

A code edit can change a prompt, introduce a database probe before generation, add a deterministic output check, or create a conditional repair branch. It can also implement multiple-sample generation and aggregation (Wang et al., 2023) or execution-based self-debugging (Chen et al., 2024). The search is therefore not confined to choosing among predeclared prompt templates or workflow settings. The distinction from response-level refinement is the object of the update: a revised query is an output, whereas a new rule for constructing and checking queries changes the procedure applied to the batch.

3.3 Execution Evidence

Executing a candidate records its model prompts and completions, tool calls and responses, stdout/stderr, intermediate artifacts, runtime states, errors, and probe results; long fields are truncated. A trace exposes how a harness operates: which tools it calls, whether intermediate artifacts are consumed, when validation or recovery branches fire, and how the final output relates to the preceding computation. These details provide context for diagnosing a failure and proposing changes to the operating procedure. For an input \(x\) and outcome \(o\), TTHE also exposes task-dependent proxy signals:

- • 

Execution health \(s\in\{0,1\}\) records whether the output executes and satisfies available format or shape checks, such as returning a scalar for a counting query.

- • 

Round-trip consistency \(b\in[0,1]\) compares the input to a description reconstructed from the output: \(\widetilde{x}=\operatorname{RT}(o)\) and \(b=\operatorname{match}(x,\widetilde{x})\). A mismatch provides evidence of possible semantic drift without requiring a reference answer.

- • 

Public-test pass rate \(p\in[0,1]\) records the fraction of exposed examples or repository tests passed, where such tests are available.

These signals provide complementary but incomplete evidence: successful execution does not establish semantic correctness, and different candidates may agree on an incorrect result. TTHE therefore presents the signals together with candidate code and the underlying execution traces, rather than aggregating them into a single scalar objective. Proposers use this evidence to diagnose weaknesses and propose program changes, while the judge uses it to compare the resulting candidates.

3.4 Evolution and Selection

Let \(H_{r}^{g}\) denote branch \(g\) after round \(r\), with \(H_{0}^{g}=H_{t}\) for all \(g\). The loop uses three operators under the information constraints in Section 2:

- Observe\((H,X_{t})\)
- executes harness \(H\) on every input in \(X_{t}\) and records its execution traces, proxy signals, and cached outcomes.
- Propose\((\mathcal{A},\mathcal{T})\)
- receives the active branches \(\mathcal{A}\) and their execution records \(\mathcal{T}\). One coding-agent proposer per branch revises its own parent, using the active branches’ code and traces for context, and returns one child.
- Judge\((\mathcal{F},\mathcal{T},X_{t})\)
- inspects the eligible candidates’ code and signals. During selection, it may acquire additional evidence through probes or candidate re-execution, then commits one harness from \(\mathcal{F}\).

At the start of a batch, the incoming harness is observed once, and its cached execution record is shared across the initial branches. In each round, valid children replace their parents and are executed on \(X_{t}\); invalid or unloadable children leave their parents and cached records unchanged. Two design choices organize these updates. Lineage: a fixed parent–child sequence allows successive edits to build on the branch’s grounding, verification, and recovery routines. Diversity: conservative-repair, exploratory, and adversarial proposer roles encourage different edit directions. Branches can use one another’s execution evidence while retaining their own lineages. After \(R\) rounds, the judge selects one harness from \(\mathcal{F}_{t}=\{H_{R}^{g}\}_{g=1}^{G}\) based on the candidates’ code, execution traces, and proxy signals. The selected harness’s cached outcomes determine the current batch’s score in Eq. 2, and the harness initializes adaptation on the next batch.

The solver, proposers, and judge share the same frozen LLM. The solver runs within the evolving task harness, while the proposers and judge use a Claude Code scaffold for file access, code editing, execution, and probing, with all model calls routed to the same backbone.

4 Theoretical Analysis

We analyze a class of trace-triggered harness edits on the current batch, rather than the outer proposal-and-selection process. As conditional analyses of test-time training relate an auxiliary update to the main-task objective (Sun et al., 2020), this analysis relates corrective edits to regressions.

4.1 Setup and Assumptions

Fix a nonempty batch \(X=\{x_{i}\}_{i=1}^{B}\), its hidden evaluation targets, and a realized label-free construction history \(z\), including the random choices used to construct \(H,H^{\prime}\) and a trigger rule. Hold these programs, the trigger rule, and any inherited state fixed. Draw \(I\) uniformly from \(\{1,\ldots,B\}\) and choose a fixed coupling \(\kappa\) of fresh execution records \((O,\tau)\) and \((O^{\prime},\tau^{\prime})\) on \(x_{I}\). Both joint output–trace marginals must match the corresponding fixed program’s execution law in the same prescribed initial environment. Outcomes include submitted artifacts and relevant final states. With \(y=y_{I}\), define binary correctness and its gain by

Probabilities average over \(I\) and fresh execution randomness conditional on the fixed history; dependence on \(z\) and \(\kappa\) is suppressed. Gold defines correctness for analysis only.

Let \(D=\mathsf{d}(x_{I},\tau)\in\{0,1\}\), where the fixed, label-free rule \(\mathsf{d}\) identifies executions targeted by the edit. This execution-time trigger is distinct from the historical evidence that motivated the source-code revision. Define

Exact locality means \(\varepsilon=0\): untriggered outcomes are preserved under \(\kappa\). The value of \(\varepsilon\) depends on the execution coupling, not only on the source-code change. For example, a prefix-preserving repair can have the form

where the child retains the parent execution before the repair decision and \(\xi\) supplies fresh repair randomness. Sharing that execution gives exact locality if the check leaves untriggered outcomes unchanged. This illustrates an editable program structure, not a constraint imposed by TTHE; a global prompt or grounding edit need not have this form. Locality is a behavioral condition, not a limit on edited source lines. Appendix F specifies the coupling and its assumptions.

Separate how often a trigger fires from how informative it is and what the edit does:

Here \(m\) is trigger mass, \(\pi\) is its precision as an error detector, \(r\) is repair success, and \(u\) is regression after falsely triggering on a correct outcome. Rates on zero-probability conditioning events are set to zero. The rates \(r,u\) and the locality term \(\varepsilon\) refer to the specified coupling; these are analysis quantities, not correctness scores accessible to the loop.

4.2 Conditions for Improvement

Proposition 1 (Corrective gains and unintended regressions).

Under the coupled execution model,

Hence \(m\pi r>m(1-\pi)u+\varepsilon\) suffices for strict improvement. With exact locality, \(\Delta_{X}(H,H^{\prime})=m[\pi r-(1-\pi)u]\), so \(m\pi r>m(1-\pi)u\) is necessary and sufficient.

The balance separates successful repairs, false-trigger regressions, and off-trigger changes. The last term can help or harm; \(\varepsilon\) bounds its magnitude rather than measuring an unavoidable loss. The sufficient condition requires repairs to outweigh false-trigger regressions and worst-case off-trigger harm. Trigger precision alone does not establish repair success.

4.3 Preservation and Feedback Limits

A trigger is sound for rejection when \(D=1\) implies \(C=0\) almost surely. Violating an authoritative output contract, or failing a public test that is a necessary condition for task correctness, can provide such evidence without identifying the correct answer. An empty SQL result, a recovered intermediate exception, or low semantic consistency does not in general have this property.

Theorem 1 (Preservation and the limit of failure feedback).

If the trigger is sound for rejection and the edit is exactly local, then

No independence or positive lower bound on repair success is required.

If a label-free child check \(D^{\prime}\) is also sound for rejection and \(v=\Pr(D=1,D^{\prime}=0)\) is the mass of cleared failure flags, then

Both endpoints are attainable with the same distribution of \((D,D^{\prime})\) under sound but incomplete checks. Thus failure-flag clearance alone cannot certify a strictly positive correctness gain.

The preservation result confines modifications to outcomes already known to be wrong; strict progress still requires successful repair. With imperfect triggers, Proposition 1 gives \(e^{\prime}\leq e+m(1-\pi)+\varepsilon\) without a repair-quality assumption. Complete proofs, equivalent parameterizations, and sharpness constructions appear in Appendix F.

5 Experiments

5.1 Experimental Setup

We evaluate TTHE on six execution-grounded benchmarks: BIRD (Li et al., 2023), LiveCodeBench (Jain et al., 2025), SWE-bench Verified (Jimenez et al., 2024), DS-1000 (Lai et al., 2023), Terminal-Bench 2.1, and claw-eval. These cover text-to-SQL, competitive programming, software engineering, data-science coding, terminal-based tasks, and agentic tool use. We use fixed evaluation sets, including hard task subsets selected before adaptation; their sizes and construction procedures are given in Appendix A.

We compare each task’s fixed baseline harness with TTHE initialized from that harness, using deepseek-v4-flash as the frozen solver, proposer, and judge. Following Section 2, TTHE adapts to each unlabeled batch; final correctness feedback is used only to evaluate committed outputs. Metrics are task success rates for the five binary benchmarks and mean graded scores for claw-eval. Both methods are run three times per evaluation set. Figure 2 shows the means; individual results and mean \(\pm\) sample standard deviation appear in Appendix H.

5.2 Main Results

TTHE outperforms the fixed baseline on all six benchmarks in each of the three reported runs (Figure 2; Appendix H). Mean success rates increase by \(8.0\)–\(36.0\) percentage points on the five binary benchmarks; claw-eval gains \(20.5\) points on its \(0\)–\(100\) graded-score scale.

BIRD shows the largest gain, from \(12.7\%\) to \(48.7\%\) mean execution accuracy. Gains also occur on LiveCodeBench, SWE-bench Verified, and DS-1000, and extend to terminal-based tasks and multi-service tool use: Terminal-Bench 2.1 rises from \(55.1\%\) to \(67.8\%\), and claw-eval from \(48.9\%\) to \(69.4\%\). Across these settings, the same frozen backbone supports task execution, program revision, and candidate selection. The complete procedure thus obtains useful test-time harness updates without modifying model weights or introducing a separate repair model.

5.3 Ablation Studies

We examine repeated sampling, search configuration, cross-batch initialization, and backbone variation on BIRD. Unless stated otherwise, the ablations and further analyses below use the main experiment’s BIRD subset and deepseek-v4-flash, reporting single-run accuracy separately from the three-run main results. The reference run achieves \(12.0\%\) with the fixed baseline and \(50.0\%\) with TTHE.

Repeated sampling without evolution.

We run the fixed baseline ten times per question and vote over execution-result groups rather than SQL strings. This matches TTHE’s nominal \(1+GR=10\) harness executions for \(G=3,R=3\): one initial execution and up to nine candidate executions. Total computation also depends on harness-specific token and tool use, as well as TTHE’s proposal and judging overhead. Voting raises accuracy from \(12.0\%\) to \(16.0\%\), versus TTHE’s \(50.0\%\) (Table 1). The contrast is between obtaining more outputs from an unchanged procedure and adapting the procedure that produces and checks them. The tested voting strategy does not substitute for the complete harness-evolution process.

Search budget.

Search breadth and depth interact (Table 2). Increasing \(G\) from one to three does not improve accuracy at \(R=1\) (\(46.0\%\) versus \(44.0\%\)), but improves it at \(R=3\) (\(40.0\%\) versus \(50.0\%\)). Moreover, \(G=3,R=1\) and \(G=1,R=3\) allocate the same nominal number of proposals per batch but achieve \(44.0\%\) and \(40.0\%\), respectively. These observations suggest that search organization matters beyond proposal count, with \(G=3,R=3\) the best tested setting. The branch configurations combine different search widths with branch-specific proposer roles.

Batch size.

With \(G=3,R=3\), accuracy peaks at \(B=10\) (\(50.0\%\)) among the tested sizes, versus \(44.0\%\), \(38.0\%\), and \(44.0\%\) at \(B=5\), \(25\), and \(50\) (Figure 3). Batch size controls adaptation granularity: larger batches provide more execution evidence, but one committed program must serve more inputs and there are fewer update opportunities over the stream. The non-monotonic results show that supplying more evidence per update is not uniformly beneficial under this batch-level commitment rule.

Cross-batch accumulation.

Resetting to the baseline before each batch achieves \(44.0\%\) accuracy, compared with \(12.0\%\) for the fixed baseline. Carrying the selected harness forward further improves overall accuracy to \(50.0\%\) (Table 3). These results indicate that current-batch adaptation yields substantial gains, while retaining evolved program structure provides a useful initialization for subsequent adaptation.

Backbone variation.

We repeat evolution on BIRD with MiMo V2.5 and Kimi K2.5, using the same backbone across solver, proposer, and judge within each run (\(B=10,G=3,R=3\)). Both improve over their own fixed-harness baselines: MiMo V2.5 increases from \(32.0\%\) to \(52.0\%\), and Kimi K2.5 from \(28.0\%\) to \(48.0\%\) (Table 4). These within-model gains extend the evidence beyond the main backbone.

5.4 Further Analysis

Cross-model harness transfer.

Executing DeepSeek’s selected harness on the corresponding BIRD batch, without further evolution, improves MiMo V2.5 from \(32.0\%\) to \(56.0\%\) and GPT-5.5 from \(36.0\%\) to \(68.0\%\) (Table 5). Backbone variation tests whether other models can use the evolution procedure; this experiment instead tests whether they can use its resulting programs. The gains show that a batch-specific harness can benefit execution models other than the one that evolved it.

Candidate availability and selection.

For the BIRD reference run, we compare the committed harnesses with two post-hoc batchwise oracles. Each oracle selects the eligible harness with the most correct outputs on each batch, using gold correctness for diagnosis only; neither mixes different harnesses’ outputs within a batch. The oracle over the final candidates available to the judge reaches \(64.0\%\) (\(32/50\)), compared with the committed \(50.0\%\) (\(25/50\)). The resulting \(14\)-point selection regret is a net deficit of seven solved tasks. Trace audits include selecting a \(3/10\) candidate over an available \(4/10\), and a \(6/10\) candidate over a \(7/10\). The audited errors include executable SQL that returns extra columns or an inappropriate granularity, illustrating the gap between execution success and task correctness.

The oracle over all evaluated candidates, including earlier rounds, reaches \(70.0\%\), six points above the final-pool oracle. Both oracles use the candidate pools of the realized run. The fourteen-point gap between the judge and the final-pool oracle exceeds the six-point gain from admitting earlier candidates, highlighting selection among already generated programs as a major source of lost performance.

What strategies emerge through evolution?

Inspection of the evolved harnesses reveals concrete strategies for acquiring evidence, directing repairs, and coordinating tool use. On BIRD, an evolved harness probes database values before SQL generation, grounds filter values in their stored casing, and infers the required output shape from the question. Structural violations, execution errors, and output-shape mismatches are returned as targeted feedback for subsequent attempts (Figure 4). Generation is therefore coupled with explicit checks and failure-specific revision, rather than repeated without diagnosing the preceding attempt. On SWE-bench, an evolved harness adopts a reproduce-first workflow with root-cause localization, post-edit verification, and execution of existing tests, alongside an increased step budget. It also adds a recovery branch triggered when the initial rollout returns an empty patch. This branch supplies concrete starter commands and a reproduction template, turning the absence of a usable artifact into an explicit condition for changing the execution strategy (Figure 5). The harness thus addresses not only how to verify a patch, but also how to resume execution when the agent fails to produce one. On LiveCodeBench, an evolved policy uses a low-cost path by default and escalates to additional verification and repair after a public-test failure. In claw-eval, the evolved instructions address how information and actions are linked across services. They specify single-line tool payloads, service chaining through exact identifiers rather than display names, and a pre-delivery completeness check requiring citations of retrieved record identifiers. They also require reported actions to be supported by executed tool calls. Across these examples, evolution changes what evidence the agent obtains before acting, which observations trigger revision, and how execution proceeds after failure. Execution experience is incorporated into the rules governing task solving, rather than used only to correct an individual answer.

6 Limitations

TTHE demonstrates the potential of harness self-evolution without final task-correctness supervision. However, the feedback guiding evolution remains limited by the informativeness of execution traces and partial checks. Successful execution or agreement among candidates can coexist with semantic errors, making it difficult to distinguish effective program improvements from changes that merely satisfy available proxies. Our diagnostics show that useful candidates can already exist in the search pool yet remain unselected. This highlights a central challenge: an agent must draw on its own experience both to identify promising changes and to assess whether those changes constitute genuine progress. Developing principled mechanisms for extracting more informative feedback, guiding program exploration, and selecting beneficial updates while preserving useful behavior remains an important direction for advancing reliable unsupervised agent self-evolution.

7 Conclusion

TTHE turns test-time execution experience into updates to an agent’s executable harness, without changing model weights or accessing final correctness feedback during adaptation. Across six execution-grounded benchmarks, it improves over fixed baseline harnesses on the evaluated task sets and produces inspectable grounding, verification, and recovery policies. Transfer experiments further show that batch-specific evolved harnesses can benefit other execution models on the corresponding tasks. Our conditional analysis characterizes the balance between corrective gains and unintended regressions for trace-triggered edits, while search diagnostics show that generating useful candidates does not ensure that they are selected. Together, these findings support executable harness adaptation as a practical path to test-time self-evolution, with reliable selection under incomplete evidence remaining a central challenge.

References

- Gepa: reflective prompt evolution can outperform reinforcement learning. In International Conference on Learning Representations, Vol. 2026, pp. 8479–8565. Cited by: Appendix D.
- MOSS: self-evolution through source-level rewriting in autonomous agent systems. arXiv preprint arXiv:2605.22794. Cited by: Appendix D, §1.
- Safe harness self-evolution: a theoretical analysis of feasibility and limits. arXiv preprint arXiv:2609.08175. Cited by: Appendix D.
- CodeT: code generation with generated tests. arXiv preprint arXiv:2207.10397. Cited by: Appendix D.
- Harnessx: a composable, adaptive, and evolvable agent harness foundry. arXiv preprint arXiv:2606.14249. Cited by: Appendix D.
- Teaching large language models to self-debug. In International Conference on Learning Representations, ICLR, Cited by: Appendix D, §1, §3.2.
- Promptbreeder: self-referential self-improvement via prompt evolution. In International Conference on Machine Learning, ICML, Cited by: Appendix D.
- Text-to-SQL empowered by large language models: a benchmark evaluation. arXiv preprint arXiv:2308.15363. Cited by: Appendix D.
- Connecting large language models with evolutionary algorithms yields powerful prompt optimizers. In International Conference on Learning Representations, ICLR, Cited by: Appendix D.
- EvoTest: evolutionary test-time learning for self-improving agentic systems. arXiv preprint arXiv:2510.13220. Cited by: Appendix D, §1.
- Automated design of agentic systems. In International Conference on Learning Representations, ICLR, Cited by: Appendix D, §1.
- Large language models can self-improve. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP, Cited by: Appendix D.
- Learning on the job: test-time curricula for targeted reinforcement learning. arXiv preprint arXiv:2510.04786. Cited by: Appendix D.
- LiveCodeBench: holistic and contamination free evaluation of large language models for code. In International Conference on Learning Representations, ICLR, Cited by: §5.1.
- SWE-bench: can language models resolve real-world GitHub issues?. In International Conference on Learning Representations, ICLR, Cited by: §5.1.
- DSPy: compiling declarative language model calls into self-improving pipelines. arXiv preprint arXiv:2310.03714. Cited by: Appendix D, §1.
- DS-1000: a natural and reliable benchmark for data science code generation. In International Conference on Machine Learning, ICML, Cited by: §5.1.
- Meta-harness: end-to-end optimization of model harnesses. arXiv preprint arXiv:2603.28052. Cited by: Appendix D, §1, §1.
- Can LLM already serve as a database interface? a big bench for large-scale database grounded text-to-SQLs. In Advances in Neural Information Processing Systems, NeurIPS, Cited by: Appendix E, §5.1.
- Competition-level code generation with AlphaCode. Science. Cited by: Appendix D.
- Let’s verify step by step. In International Conference on Learning Representations, ICLR, Cited by: Appendix D.
- Harness-aware self-evolving: co-evolving model weights, harness, and task solutions. arXiv preprint arXiv:2607.03935. Cited by: Appendix D.
- Self-Refine: iterative refinement with self-feedback. In Advances in Neural Information Processing Systems, NeurIPS, Cited by: Appendix D.
- DIN-SQL: decomposed in-context learning of text-to-SQL with self-correction. In Advances in Neural Information Processing Systems, NeurIPS, Cited by: Appendix D.
- Mathematical discoveries from program search with large language models. Nature. Cited by: Appendix D.
- Reflexion: language agents with verbal reinforcement learning. In Advances in Neural Information Processing Systems, NeurIPS, Cited by: Appendix D, §1.
- Test-time training with self-supervision for generalization under distribution shifts. In International Conference on Machine Learning, ICML, Cited by: Appendix D, §4.
- Dynamic cheatsheet: test-time learning with adaptive memory. In Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 7080–7106. Cited by: Appendix D.
- Tent: fully test-time adaptation by entropy minimization. In International Conference on Learning Representations, ICLR, Cited by: Appendix D.
- Voyager: an open-ended embodied agent with large language models. Trans. Mach. Learn. Res.. Cited by: Appendix D.
- Self-consistency improves chain of thought reasoning in language models. In International Conference on Learning Representations, ICLR, Cited by: Appendix D, §3.2.
- Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems 35, pp. 24824–24837. Cited by: Appendix D.
- Large language models as optimizers. In International Conference on Learning Representations, ICLR, Cited by: Appendix D.
- SWE-agent: agent-computer interfaces enable automated software engineering. In Advances in Neural Information Processing Systems, NeurIPS, Cited by: Appendix A.
- One recipe, many harnesses: what self-evolution encodes across languages and models. arXiv preprint arXiv:2608.10178. Cited by: Appendix D.
- ReAct: synergizing reasoning and acting in language models. In International Conference on Learning Representations, ICLR, Cited by: Appendix D, §3.2.
- Learning to discover at test time. arXiv preprint arXiv:2601.16175. Cited by: Appendix D.
- Self-taught optimizer (STOP): recursively self-improving code generation. arXiv preprint arXiv:2310.02304. Cited by: Appendix D.
- STaR: bootstrapping reasoning with reasoning. In Advances in neural information processing systems, NeurIPS, Cited by: Appendix D.
- Agentevolver: towards efficient self-evolving agent system. arXiv preprint arXiv:2511.10395. Cited by: Appendix D.
- Self-harness: harnesses that improve themselves. arXiv preprint arXiv:2606.09498. Cited by: Appendix D, §1, §1.
- Darwin godel machine: open-ended evolution of self-improving agents. arXiv preprint arXiv:2505.22954. Cited by: Appendix D.
- AFlow: automating agentic workflow generation. In International Conference on Learning Representations, ICLR, Cited by: Appendix D, §1.
- MEMO: test time robustness via adaptation and augmentation. In Advances in Neural Information Processing Systems, NeurIPS, Cited by: Appendix D.
- Agentic context engineering: evolving contexts for self-improving language models. In International Conference on Learning Representations, Vol. 2026, pp. 86069–86100. Cited by: Appendix D.
- Judging LLM-as-a-judge with MT-Bench and chatbot arena. In Advances in Neural Information Processing Systems, NeurIPS, Cited by: Appendix D.
- Large language models are human-level prompt engineers. In International Conference on Learning Representations, ICLR, Cited by: Appendix D.
- Ttrl: test-time reinforcement learning. Advances in Neural Information Processing Systems 38, pp. 131459–131483. Cited by: Appendix D.
- Self-adapting language models. Advances in Neural Information Processing Systems 38, pp. 74084–74115. Cited by: Appendix D.

Appendix A Task Construction

We use fixed evaluation sets that include selected hard task subsets. The four query and code subsets were fixed before running TTHE using the criteria below; no TTHE outcome was used to select or filter instances. Reference artifacts used for subset construction were not passed to the adaptation loop.

BIRD.

The 50-question hard subset is drawn from BIRD Mini-Dev by auditing questions the baseline repeatedly missed and retaining unambiguous, substantively hard cases. It spans multiple databases. Accuracy uses result-set equality between the executed prediction and the reference query. Selection is conditioned on baseline failures; the scores describe this recovery-oriented subset, not full-benchmark performance or a controlled ranking of different backbones.

LiveCodeBench.

The 60-problem hard subset uses the contamination-controlled release window reported in the experiment, with problems published after the solver’s training cutoff. Task success requires passing all hidden tests; exposed examples remain available as partial checks during adaptation.

SWE-bench Verified.

The 40-instance hard subset is selected by gold-patch complexity, using multi-file or large changes. The baseline is the off-the-shelf mini-swe-agent scaffold, which TTHE subsequently evolves [Yang et al., 2024b]. Reference patches used for subset construction are not given to the adaptation loop.

DS-1000.

The 50-problem hard subset is selected by reference-solution length. Reference solutions and final evaluation tests are excluded from adaptation; reported success requires passing the hidden task tests.

Terminal-Bench 2.1.

The main experiment evaluates 89 tasks from Terminal-Bench 2.1. The benchmark repository is https://github.com/harbor-framework/terminal-bench-2-1.

claw-eval.

The 30-task headroom subset consists of tasks served by local deterministic mock services and selected using baseline performance. Appendix C describes the subset construction, the OpenClaw harness, graded scoring, and the information boundary. The baseline and TTHE each have three complete-run results, listed in Appendix H.

A.1 Model Access

Table 7 lists the API base URLs for the models used in our experiments.

A.2 Dataset Licenses

Table 8 summarizes the licensing information provided by upstream dataset cards and benchmark repositories. Third-party task content remains subject to its original license or terms of use.

Appendix B Discovered Harness Policies

The evolved programs are retained as source code rather than summarized only by aggregate scores. Recurring discovered policies include:

- • 

Text-to-SQL: value grounding through database probes, date-format repair, explicit output-shape checks, and removal of accidental limits on list queries.

- • 

LiveCodeBench: multiple candidate programs, execution-based ranking on public tests, targeted repair from expected-versus-observed outputs, and fresh-start recovery after repeated failure.

- • 

SWE-bench: reproduce-first debugging, root-cause localization before editing, post-edit verification, and an anti-paralysis failsafe for issues that would otherwise return an empty patch (Figure 5).

- • 

DS-1000: insertion-only output contracts, deterministic self-checks, and guards against redefining supplied variables.

- • 

claw-eval: single-line tool payloads so write actions are recorded, per-record identifier citation with a pre-delivery completeness check, exact-identifier service chaining, and a prohibition on reporting unexecuted actions (see the claw-eval section below).

These policies are examples of program-level adaptation: they modify the control procedure used across instances rather than appending a one-off answer correction.

Appendix C The claw-eval Agentic Tool-Use Domain

C.1 Task, metric, and protocol

claw-eval tasks are multi-service office workflows: the solver reads mail, searches a knowledge base, looks up contacts, inspects a CRM or helpdesk, schedules meetings, and updates tickets through tool calls. The score is a per-task graded rubric in \([0,1]\), rather than binary execution accuracy. Each rubric combines completion, robustness, and communication criteria under a safety factor; a held-out model grader assesses the committed behavior.

The \(30\) tasks come from \(139\) agentic tasks: we retain the \(112\) served entirely by local deterministic mock services, then select those on which the frozen baseline scores below \(0.60\). The solver is deepseek-v4-flash inside the OpenClaw agent, and the proposer edits its system prompt and skills as source code. The run processes the tasks in six batches, evolving one general harness from the baseline. The grader is disabled during in-loop observation, so no task score or rubric target enters the proposer or judge; gold grading is applied only to the committed harness for measurement. The baseline and TTHE scores, \(48.9\%\) and \(69.4\%\), are each averaged over three runs (Appendix H). The tasks are ordered by ascending baseline difficulty, so this evaluation does not isolate the effect of cross-batch accumulation.

C.2 Discovered policies

From label-free traces alone the accumulated harness adds four general rules to the baseline: single-line tool payloads for reliable action capture; citation of every retrieved record identifier under a completeness checklist before delivery; chaining services by exact identifier (email or ID) rather than display name; and grounding every reported action in an executed tool call.

Appendix D Related Work

Prompt and workflow optimization.

Research on optimizing the system around a language model spans instructions, workflows, and executable programs. APE and OPRO search for instructions [Zhou et al., 2023, Yang et al., 2024a], while Promptbreeder and EvoPrompt use evolutionary prompt optimization [Fernando et al., 2024, Guo et al., 2024]. DSPy optimizes declarative language-model pipelines against a metric [Khattab et al., 2023]; ADAS and AFlow extend the search to agent designs and code-represented workflows [Hu et al., 2025, Zhang et al., 2025b]. FunSearch illustrates the broader potential of executable program search [Romera-Paredes et al., 2024]. More recently, GEPA uses natural-language reflection on reasoning and tool-use trajectories to propose prompt updates and combine complementary improvements from a Pareto frontier [Agrawal et al., 2026]. Thus, interpreting execution traces is already an important optimization mechanism; TTHE studies its use for revising and selecting an executable harness on the current test batch without final task-correctness feedback.

Executable harness evolution.

A related line modifies agent source code or accumulates executable components. STOP and the Darwin Gödel Machine revise agent scaffolds [Zelikman et al., 2023, Zhang et al., 2025a], Voyager builds a reusable skill library [Wang et al., 2024], and MOSS studies source-level rewriting from failure trajectories [Cai et al., 2026a]. Among harness-level methods, Self-Harness validates edits through verifier-grounded evaluation and regression tests with a fixed model [Zhang et al., 2026a]; Meta-Harness gives its proposer access to historical code, scores, and traces from a search set before held-out evaluation [Lee et al., 2026]. HarnessX provides composable harness primitives and a trace-driven multi-agent evolution engine, with both harness-only adaptation and a harness–model co-evolution loop that reuses trajectories for model training [Chen et al., 2026]. HASE unifies task-solution generation and harness editing in an agentic reinforcement-learning process, co-evolving model weights, harness components, and solutions [Luo et al., 2026]. TTHE shares the executable-program optimization target but keeps the solver, proposers, and judge frozen, and excludes final correctness feedback from both current-batch program revision and commitment.

Transfer and reliable adoption.

Beyond aggregate performance, recent work examines what evolved harnesses retain and when their updates can be trusted. One Recipe, Many Harnesses analyzes artifacts produced by a common evolution recipe across languages and models, distinguishing transferable strategies from ecosystem-specific adaptations [Yang et al., 2026]. A theory of reliable harness self-evolution studies adoption conditions that balance gains on failed tasks against preservation of successful behavior, together with the limits imposed by verification and evaluation costs [Cai et al., 2026b]. TTHE’s transfer experiments instead execute batch-specific evolved programs with other backbones. Its conditional analysis concerns a class of trace-triggered edits under a fixed execution coupling.

Self-directed model adaptation.

Self-improvement can also change the model itself. STaR bootstraps reasoning by fine-tuning on generated rationales that lead to correct answers [Zelikman et al., 2022]; related work fine-tunes on high-confidence solutions generated from unlabeled questions [Huang et al., 2023]. SEAL learns to generate its own adaptation data and update directives, using post-update performance to train the self-editing policy [Zweiger et al., 2026]. AgentEvolver combines self-generated tasks, experience-guided exploration, and trajectory-level credit assignment to improve agent reinforcement learning [Zhai et al., 2025]. These approaches use experience to improve parameterized capabilities or the process that trains them. In TTHE, experience instead changes the executable procedure through which an unchanged model acquires context, uses tools, verifies results, and recovers from failures.

Test-time adaptation and reinforcement learning.

TTT, Tent, and MEMO adapt model parameters or normalization statistics using self-supervised, confidence-based, or augmentation-based objectives on unlabeled test inputs [Sun et al., 2020, Wang et al., 2021, Zhang et al., 2022]. For language-model reasoning, TTRL performs reinforcement learning directly on unlabeled test data, estimating rewards from agreement with majority-voted model outputs [Zuo et al., 2026]. It therefore shares the absence of ground-truth answers during adaptation, but uses the inferred rewards to update model weights. TTC-RL constructs test-time curricula from an available training pool for targeted reinforcement learning [Hübotter et al., 2025], while TTT-Discover trains on experience from a particular test problem, using continuous rewards to prioritize exceptional solutions [Yuksekgonul et al., 2026]. These studies establish test-time learning as more than repeated inference. TTHE pursues a different adaptation state: the model remains fixed, while execution evidence informs program updates and candidate selection without being reduced to a scalar training objective.

Test-time memory and context evolution.

Parameter-free adaptation is also studied through persistent memory and evolving contexts. Dynamic Cheatsheet maintains a self-curated memory of strategies, code snippets, and reusable insights at inference time without explicit ground-truth labels [Suzgun et al., 2026]. ACE treats contexts as evolving playbooks, using generation, reflection, and curation with incremental updates; it supports both offline context optimization and online adaptation from execution feedback [Zhang et al., 2026b]. EvoTest evolves prompts, memory, hyperparameters, and executable state-extraction logic across interactive episodes, using transcripts for updates and environment-score statistics for candidate selection [He et al., 2025]. These methods already demonstrate experience accumulation beyond an isolated answer. TTHE focuses on revising the task’s control program and committing a single harness whose cached outcomes are scored on the same batch, with final evaluation feedback excluded from the adaptation loop.

Response refinement and execution feedback.

Chain-of-thought, self-consistency, and ReAct organize reasoning and tool use within an inference procedure [Wei et al., 2022, Wang et al., 2023, Yao et al., 2023]. Self-debugging and Self-Refine revise candidate answers [Chen et al., 2024, Madaan et al., 2023], and Reflexion retains textual experience for later attempts [Shinn et al., 2023]. Domain-specific systems incorporate these ideas into fixed procedures: DIN-SQL and DAIL-SQL use structured prompting and execution-related processing for text-to-SQL [Pourreza and Rafiei, 2023, Gao et al., 2023], while code-generation systems use tests to select candidate solutions [Chen et al., 2022, Li et al., 2022]. Learned verifiers and LLM judges provide further evaluation signals [Lightman et al., 2024, Zheng et al., 2023]. TTHE can express verification and repair within a harness, but adapts the program that specifies when and how these operations occur, rather than only revising a particular response.

Appendix E Cross-Database Transfer and Continued Adaptation

TTHE targets adaptation to the current unlabeled batch. As a complementary evaluation, we examine whether an evolved harness transfers to databases excluded from its adaptation stage, and whether continued adaptation yields further gains on the target batches.

Setup and protocol.

We partition the baseline-screened genuine_hard50 subset of BIRD Mini-Dev [Li et al., 2023] by database, preserving the original question order within each split. The ID split contains 30 questions from card_games, formula_1, and toxicology; the OOD split contains 20 questions from california_schools, superhero, debit_card_specializing, and student_club. Here, OOD denotes database-disjoint transfer within the same screened benchmark subset.

Starting from the bare text-to-SQL harness, TTHE evolves on the ID split. The final ID harness is frozen before exposure to any OOD questions or evaluation scores. We evaluate this fixed program on both splits without further evolution. Separately, we initialize TTHE with the frozen ID harness and continue adaptation on two OOD batches, scoring each batch with its corresponding committed harness.

All runs use deepseek/deepseek-v4-flash with temperature \(0\), reasoning enabled, and two workers. TTHE uses batch size \(B=10\), \(G=3\) branches, and at most \(R=3\) rounds. Solver and proposer timeouts are \(180\) and \(2700\) seconds, respectively.

Results and interpretation.

The frozen ID harness achieves \(10/30\) on the ID adaptation set, compared with \(5/30\) for the bare baseline (Table 9). More importantly, it achieves \(10/20\) on the held-out databases without further evolution, versus \(2/20\) for the baseline. This improvement provides evidence that the evolved task-solving procedure remains useful beyond the databases that supplied its adaptation traces.

Continuing TTHE on the OOD split raises accuracy to \(13/20\), with \(8/10\) and \(5/10\) on the two successive batches. The frozen-transfer result measures reuse without target-side harness evolution, whereas the continued-adaptation result measures the additional benefit of updating the procedure using target-batch execution evidence. Together, these results support both cross-database reuse of an evolved harness and its capacity for further test-time adaptation.

Appendix F Proofs and Scope of the Conditional Analysis

F.1 Probability Space and the Locality Condition

Fixed construction history and fresh executions.

Fix the batch, its hidden targets, and a realization \(z\) of the label-free construction history and random choices defining \(H,H^{\prime}\) and the trigger rule \(\mathsf{d}\). Program configurations and inherited state are held fixed. Execution randomness is drawn anew from each program’s prescribed law; it is not a replay or a conditional reweighting of the rollouts that produced \(z\). The uniform index \(I\) averages over this same batch, so no i.i.d. assumption about a test stream is needed.

For task \(i\), let \(E_{i}\) denote its prescribed initial environment and let \(P_{H}^{z}(\cdot\mid x_{i},E_{i})\) be the joint law of the output and trace from the fixed program \(H\), including any randomized checks recorded in that trace. Define \(P_{H^{\prime}}^{z}\) analogously. A specified coupling \(\kappa\) must satisfy

The two executions start from the same prescribed task state, not from a state modified by the other execution. All probabilities below are for this fixed history and coupling. In particular, \(D=\mathsf{d}(x_{I},\tau)\) has its actual joint law with \(O\); preserving the output marginal alone would not suffice. A child check, when used, is likewise a fixed function of \(x_{I}\) and \(\tau^{\prime}\), with any check randomness included in its record. Hidden targets enter only the correctness indicators. Complete outcomes include artifacts and final states that affect scoring, so \(O=O^{\prime}\) implies \(C=C^{\prime}\).

Coupling and a prefix-preserving repair.

The error rates \(e,e^{\prime}\) and their difference depend only on the prescribed marginals, whereas \(r,u\) and \(\varepsilon\) can depend on \(\kappa\). For example, let \(H^{\prime}=H\), set \(D=0\), and suppose the program returns either of two outcomes with equal probability. Sharing its random draw gives \(\varepsilon=0\); independent draws give \(\varepsilon=1/2\), although \(\Delta_{X}=0\) in both comparisons. Thus \(\varepsilon\) is not an intrinsic distance between source programs.

For the gated structure illustrated in the main text, couple the child and parent by sharing the unchanged parent execution, including its trace and random draws. The child returns its outcome when \(D=0\) and invokes repair with fresh randomness when \(D=1\). This coupling has the required marginals only if the child actually implements that prefix-preserving behavior. The check must preserve all score-relevant untriggered outcomes. Probes and repairs must not change the target, interfere with other instances, or consume resources that alter untriggered behavior. Adding an if statement alone does not establish these properties. No independence between the two executions is required.

Cached outcomes and adaptive selection.

Construction may use the same batch, but the realized rollouts in \(z\) are distinct from the fresh execution laws above. Conditioning on a program chosen using those rollouts need not preserve their original sampling law. One can also decompose correctness transitions in fixed cached outcomes by averaging over batch indices, but that is an empirical identity for those outcomes, not a guarantee for fresh executions or the adaptive selection process. The results here neither rank candidates from unlabeled evidence nor ensure that the proposer or judge returns a pair satisfying the stated conditions.

F.2 Proof of Proposition 1

Proof.

Split the correctness gain according to whether the trigger fires:

On the triggered region, only incorrect-to-correct and correct-to-incorrect transitions contribute:

The products follow from the chain rule, without independence. If \(m=0\), both triggered event masses vanish; otherwise the conditioning events partition \(D=1\). The convention for zero-probability events therefore preserves the identity.

Let \(\Gamma_{0}=\mathbb{E}[(C^{\prime}-C)\mathbb{I}[D=0]]\). Since identical outcomes have the same correctness,

Thus \(\Delta_{X}(H,H^{\prime})=m[\pi r-(1-\pi)u]+\Gamma_{0}\), which proves Eq. 7. If \(m\pi r>m(1-\pi)u+\varepsilon\), its lower bound is positive. With \(\varepsilon=0\), the equality makes \(m\pi r>m(1-\pi)u\) necessary and sufficient for strict improvement. ∎

Equivalent error-detection-rate parameterization.

Define \(d=\Pr(D=1\mid C=0)\) and \(f=\Pr(D=1\mid C=1)\), with the same zero-event convention. Here \(d\) is error detection and \(f\) is false triggering. The joint event masses satisfy

Consequently, Proposition 1 is equivalently

In particular, \(edr>(1-e)fu+\varepsilon\) suffices for improvement. This is the same probability balance, expressed in terms of error detection and false triggering rather than trigger mass and precision.

Exact locality and sharpness of the uniform coefficient.

For any \(e,d,f,r,u\in[0,1]\), the following nonnegative masses sum to one:

Choose identical outcomes on the two \(D=0\) rows. Exact locality then holds, and the correctness gain is \(edr-(1-e)fu=m[\pi r-(1-\pi)u]\). Parameters attached to zero-mass conditioning events do not affect the distribution; their actual conditional rates are interpreted by the zero-event convention. This construction realizes the exact balance when \(\varepsilon=0\).

The coefficient of the uniform symmetric \(\varepsilon\)-term cannot be reduced in general: take a parent correct everywhere, set \(D=0\) everywhere, and change the child to an incorrect outcome on a mass \(\varepsilon\). Then \(\Delta_{X}=-\varepsilon\), attaining the lower bound. Starting from an everywhere-incorrect parent and repairing a mass \(\varepsilon\) off-trigger attains the upper bound. This is a uniform coefficient claim, not a claim that the symmetric interval is pointwise sharp for every feasible parameter tuple; restrictions on the off-trigger error masses can give tighter bounds.

F.3 Proof of Theorem 1

Proof.

Sound rejection gives \(\Pr(D=1,C=1)=0\), so the regression event in Eq. 12 vanishes. Exact locality gives \(\Gamma_{0}=0\). Therefore

When \(m>0\), soundness gives \(\pi=1\); when \(m=0\), the expression is zero under the zero-event convention. This proves preservation without assuming a positive repair success rate or independent executions.

If \(D^{\prime}\) is sound for rejection on the child, \(C^{\prime}=1\) implies \(D^{\prime}=0\) almost surely. Hence

up to a null set. Taking probabilities yields \(0\leq\Delta_{X}(H,H^{\prime})\leq v\).

For sharpness, fix \(0\leq v\leq m\leq 1\) and construct three disjoint events of masses \(1-m\), \(m-v\), and \(v\). On the first, set \(D=D^{\prime}=0\), use identical outcomes, and set \(C=C^{\prime}=1\). On the second, set \(D=D^{\prime}=1\) and \(C=C^{\prime}=0\). On the third, set \(D=1\), \(D^{\prime}=0\), and \(C=0\). For the lower endpoint set \(C^{\prime}=0\) on this last event; for the upper endpoint set \(C^{\prime}=1\). Both constructions have the same \((D,D^{\prime})\) distribution, the same baseline error \(e=m\), exact locality, and sound rejection for both checks. Their correctness gains are zero and \(v\), respectively. Checks can realize this by rejecting a malformed outcome while accepting both a correct outcome and a well-formed but semantically wrong one. The indistinguishability concerns these checks’ outcomes, not all semantic information in a complete execution trace. ∎

F.4 Interpretation and Application Boundaries

Failure soundness is one-sided.

A sound rejection flags a final outcome that cannot satisfy the task. Acceptance need not imply correctness. A runtime failure is sound rejection only when it invalidates the submitted outcome under the specified environment. Visible tests qualify only when they are authoritative necessary conditions; noisy, stale, unrelated, or flaky tests do not automatically qualify. A correct SQL query may return zero rows, and an intermediate exception may be recovered from before a correct outcome is submitted. Such signals require potentially imperfect precision \(\pi\), rather than being classified as sound by default.

Repair precision and locality.

The mass \(m\pi\) identifies incorrectly behaving executions targeted by an edit; \(m(1-\pi)\) identifies correct ones exposed to modification. A high trigger rate alone says nothing about their balance. Without a repair-quality assumption, \(r\geq 0\) and \(u\leq 1\) give

Soundness removes falsely triggered correct outcomes, and exact locality removes possible off-trigger harm. Neither condition asserts \(r>0\). Likewise, clearing a failure flag does not measure \(r\), because correct and incorrect outputs can both pass an incomplete check.

Relation to the search procedure.

TTHE can express local repair branches as well as global prompt and grounding edits. The preservation result applies to transitions satisfying the stated soundness and locality conditions; extending it to a sequence requires these conditions at each committed transition. The complete search procedure is evaluated empirically.

Binary versus graded outcomes.

The analysis uses binary correctness, as in exact SQL or hidden-test evaluation. For graded loss, merely detecting an outcome that is not fully correct does not make replacing it safe: a partly successful outcome can be made worse. An analogous preservation conclusion would require a stronger condition, such as the trigger certifying maximal loss. It is not claimed for claw-eval’s graded score, nor does the correctness analysis account for additional latency, tokens, or execution costs.

Appendix G Full Algorithm

Appendix H Repeated Main Results

Table 10 reports three runs per method with mean \(\pm\) sample standard deviation. Raw results are solved/total counts for the binary benchmarks and mean graded scores for claw-eval. Figure 2 uses the run means, with absolute gains computed before rounding. Ablations and selection diagnostics use the single-run reference described in Section 5.3.
