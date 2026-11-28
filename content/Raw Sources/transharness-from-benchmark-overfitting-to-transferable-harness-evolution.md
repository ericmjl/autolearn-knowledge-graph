---
title: "TransHarness: From Benchmark Overfitting to Transferable Harness Evolution"
type: "raw-source"
url: "https://arxiv.org/html/2611.33757v1"
author: "Tianze Xia Affiliation Huazhong University, Technology, Wuhan, China"
publication: "arXiv"
published: "2026-10-22"
archived: "2026-11-28T09:01:25Z"
---

> [!quote] Original source
> **Author(s):** Tianze Xia Affiliation Huazhong University, Technology, Wuhan, China  
> **Title:** TransHarness: From Benchmark Overfitting to Transferable Harness Evolution  
> **Published in:** arXiv  
> **Date:** 2026-10-22  
> **Original:** <https://arxiv.org/html/2611.33757v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-transharness-from-benchmark-overfitting-to-transferable-harness-evolution|Source note]]
Themes: [[Loop engineering]]
Why it was archived: How do you keep held-out evaluation representative across distribution shift, and how to detect when it stops being valid

## Archived text

TransHarness: From Benchmark Overfitting to Transferable Harness Evolution

Abstract

Harness evolution offers a path to improving coding agents without updating model weights. However, existing methods can overfit their evolution benchmarks, producing gains that fail to carry over to new tasks. To address this challenge, we introduce Transferable Harness Evolution (TransHarness), which evolves harness intervention policies from same-task success–failure contrasts. These policies couple execution-context triggers with diagnostic guidance, enabling task-dependent checks and corrections beyond the source executions. Cross-task replay and independent semantic selection retain policies that intervene selectively and ground corrections in current-task evidence rather than source-specific solutions. We further curate an independent evolution set for cross-distribution transfer and conduct a cross-benchmark evaluation covering multiple strong models and a range of lightweight and mature harnesses. Experiments show that, with only 300 source trajectories from outside the test distribution, TransHarness further improves strong agents across distinct target benchmarks, demonstrating transferable harness evolution beyond benchmark overfitting. Specifically, TransHarness achieves state-of-the-art scores of 76.4% on DeepSWE v1.1 and 95.5% on Terminal-Bench 2.1, surpassing the strongest baseline model, GPT-6 Astra, by 2.4 and 5.6 percentage points, respectively.

Keywords:

agent harnesses, program evolution, language model agents, transfer

1 Introduction

Coding agents rely on harnesses to organize tool use, interpret feedback, and verify task outcomes (Yang et al., 2024b; Wang et al., 2025). Harness evolution improves these execution mechanisms using experience from past tasks, offering a path to stronger agents without updating model weights (Zhang et al., 2026b; Lee et al., 2026; Wu et al., 2026a).

However, gains on the tasks that drive evolution may fail to carry over to new tasks. SICA selects agent versions on a fixed task suite (Robeyns et al., 2025), Meta-Harness searches for and evaluates coding harnesses on the same TerminalBench-2 tasks (Lee et al., 2026), and Self-Harness selects candidates using feedback from held-out tasks within the benchmark (Zhang et al., 2026a). Such feedback can favor adaptations to recurring benchmark characteristics, making benchmark overfitting difficult to distinguish from transferable improvement. DGM and ModularRSI test cross-benchmark transfer (Zhang et al., 2026b; Wu et al., 2026a), yet sustaining gains under distribution shift remains challenging. Our Meta-Harness reproduction illustrates this gap. It improves on our independent evolution set, but its success rate falls on DeepSWE v1.1 (Figure 1a).

To improve agents in practical settings, harness evolution must also benefit strong models running in mature harnesses. Existing methods can improve minimal starting systems, such as DGM’s harness with basic execution and editing tools and Self-Harness’s minimal DeepAgent (Zhang et al., 2026b; Zhang et al., 2026a). How to improve mature systems remains an open question. In HarnessOpt-Bench, an evolved simple harness still trails mature OpenCode when both use the same model and evaluation tasks (Ursekar et al., 2026) (Figure 1b). As baseline success increases, fewer failures remain to recover and more successful executions are at risk of regression. A positive net gain on strong agents therefore requires a lower ratio of the regression rate to the recovery rate. If the ratio is too high, overall performance can decline even when evolution recovers some failures (Figure 1c). To transfer gains to strong agents, interventions must uncover overlooked problems while preserving behavior that already works.

A correction can be specific to its source task even when the underlying execution failure recurs across task distributions. To address this challenge, we introduce Transferable Harness Evolution (TransHarness), which evolves when and how a harness intervenes during execution. TransHarness derives intervention policies from contrasts between successful and failed executions of the same task. Each policy pairs a trigger based on observable execution context with diagnostic guidance. The guidance directs agents to task requirements and evidence, allowing the same decision problem to receive different corrections across tasks. Cross-task replay and independent semantic selection together retain policies that intervene selectively and guide corrections based on evidence from the current task, making them usable beyond the original source-task solution (Figure 2).

To test whether harness evolution transfers across task distributions, we construct an independent evolution set and characterize how it differs from the target benchmarks in code repositories, task types, and application domains. For each model and harness configuration, we run the baseline agent on the evolution set and use the resulting trajectories to generate and select intervention policies. We then evaluate the evolved systems on the target benchmarks, covering multiple strong models and both lightweight and mature harnesses. TransHarness achieves state-of-the-art scores of 76.4% on DeepSWE v1.1 and 95.5% on Terminal-Bench 2.1 (Huang & Jiang, 2026; The Terminal-Bench Team, 2026), exceeding GPT-6 Astra by 2.4 and 5.6 percentage points, respectively.

Our main contributions are as follows.

- • 

We find that gains on source tasks can turn into losses when transferred to a new benchmark. We derive the condition for harness evolution to yield a positive net gain on target tasks. At a fixed recovery rate, a higher baseline success rate allows a lower regression rate.

- • 

We propose TransHarness, which evolves harness intervention policies from same-task success–failure contrasts. In relevant contexts, these policies guide agents to reassess decisions using current-task evidence. Cross-task replay tests how selectively they activate, and independent semantic selection checks whether diagnoses are supported and whether guidance depends on source-task solutions.

- • 

We construct an independent evolution set to evaluate transfer across task distributions. Experiments with multiple strong models in lightweight and mature harnesses demonstrate the transferable gains of TransHarness, which achieves state-of-the-art performance on both DeepSWE v1.1 and Terminal-Bench 2.1.

2 Related Work

Learning and evolving agent harnesses.

Harness evolution extends feedback-based optimization to executable agents (Zhang et al., 2024; Zhang et al., 2025; Hu et al., 2025). Meta-Harness searches historical code, scores, and traces (Lee et al., 2026); ModularRSI combines same-task contrasts, module-restricted updates, review, and task-aware composition (Wu et al., 2026a). TransHarness instead couples context-sensitive triggers with diagnostic guidance.

Validation and transfer of harness improvements. Self-Harness checks regressions (Zhang et al., 2026a), VERSE co-evolves verification and optimization (Wang et al., 2026b), and RRSI regularizes selection (Xia et al., 2026). Held-out evaluation separates search from testing (Wang et al., 2026a; Ursekar et al., 2026; Wu et al., 2026b; Ding et al., 2026). AHE verifies predicted edit effects from trajectory evidence (Lin et al., 2026); HarnessCompass constrains edits to task-agnostic mechanisms (Zhang et al., 2026c); Meta2 learns knowledge for task-local evolution (Yuan et al., 2026). TransHarness instead freezes policies before deployment, using replay to test selectivity and semantic selection to examine source-specific assumptions. Further comparisons appear in Appendix D.

3 Transferable Harness Evolution

TransHarness evolves policies that recognize recurring decision problems and guide reassessment under new task requirements. Candidate refinement is followed by selection on source evidence (Figure 2). The selected policies are composed into the final harness.

Given a fixed model \(M\) and base harness \(H_{0}\), we learn an ordered intervention set \(B\) on source distribution \(P\). The intervention set defines the evolved harness \(H_{B}\), which uses the same execution model as the base harness for every new task. The objective is to improve success on tasks drawn from an independent target distribution \(Q\):

Here, \(p_{H}(x)\) is the probability that \(H\) solves \(x\). Construction and selection use source evidence alone; we freeze the resulting harness \(H_{B}\) before evaluating it on target tasks.

3.1 Evolving Intervention Policies

From a same-task success–failure pair \(\rho=(\tau^{+},\tau^{-})\) under \(H_{0}\), an author diagnoses divergent decisions and derives a reusable principle. Each pair starts from \(H_{0}\); diagnoses without a reusable principle can be declined. Figure 2a contrasts repairing a bug with weakening a test. The resulting principle evaluates test changes against task requirements and the remaining defect, allowing task-dependent repairs.

Each policy \(u=(s,g,c)\) specifies a harness location \(s\), executable trigger \(g\), and diagnostic guidance \(c\). When \(g(h_{t},e_{t})=1\) for history \(h_{t}\) and event \(e_{t}\), the harness supplies \(c\) through \(s\) to direct reassessment toward relevant requirements and evidence. Locations cover model calls, tools, context updates, and completion (Section B.5). Triggers use observable execution context; the policy transfers a diagnostic procedure whose resolution remains responsive to current requirements (Figure 3).

3.2 Refining Intervention Scope and Semantics

Two properties determine whether a source-derived intervention remains useful: which executions it affects, and what its guidance induces in those executions. Consider \(H\) and \(H+u\) coupled through common randomness, with identical histories and resource-limit effects until \(u\) first affects execution. Let \(A_{u}\) denote this event. For distribution \(D\in\{P,Q\}\) with \(\mathbb{P}_{D}(A_{u})>0\), define exposure \(a_{D}=\mathbb{P}_{D}(A_{u})\) and conditional value \(v_{D}=\mathbb{E}_{D}[Y_{H+u}-Y_{H}\mid A_{u}]\). Only executions in \(A_{u}\) can contribute to the difference, giving

The source–target change therefore satisfies

Transfer can fail through either factor: an unchanged activation rate can accompany inappropriate corrections, while overly narrow activation misses recoverable failures. Both scope and guidance must generalize beyond the conditions encountered in the source task. The decomposition motivates two complementary checks: replay examines where a policy intervenes, while semantic selection examines whether its guidance remains valid under new requirements.

The consequences are sharper for strong baselines. Let \((Y_{0},Y_{B})\) be paired binary outcomes on \(Q\), with base success \(p_{0}=\mathbb{P}(Y_{0}=1)\), rescue rate \(r=\mathbb{P}(Y_{B}=1\mid Y_{0}=0)\), and regression rate \(q=\mathbb{P}(Y_{B}=0\mid Y_{0}=1)\). Then

Even perfect recovery is limited by the failures remaining under the base harness. For \(0&lt;p_{0}&lt;1\), Equation 4 gives this ceiling and requires recovery gains to outweigh losses on originally successful executions:

Higher baseline success leaves fewer failures to recover and lowers the allowable regression-to-rescue ratio. A fixed increase in \(q\) then costs more success points. Useful interventions reach correctable decisions while preserving successful behavior. Appendix A gives the derivations and states the assumptions on coupled executions.

Authoring review refines each candidate against its motivating pair (Figure 2b). The reviewer revises guidance wording or requests one author rework for changes to the diagnosis or trigger. Executable checks validate the implementation and record activation and control-flow effects on both successful and failed source histories.

For example, a completion intervention initially required running existing tests and “fixing any failures.” Review identified an appropriate execution that left an unrelated failure unresolved. The revised guidance repairs failures caused by the current change and reports unrelated ones, preserving verification without an unconditional repair obligation. Independent selection then assesses whether the completed candidate should enter the final composition.

3.3 Transfer-Oriented Policy Selection

Selection screens event-triggered activation and assesses corrective obligations. For each policy \(u\), let \(\mathbf{n}(u)=(n_{-},n_{+},n_{\pm},N)\) summarize replay on \(N>0\) trajectory pairs from other source tasks. The first three counts indicate activation on failed executions only, successful executions only, or both, excluding session-start guidance. The replay gate is

It rejects nearly indiscriminate event-triggered activation and policies that more often single out successful executions. Surviving policies, including session-start guidance, then undergo independent semantic assessment of the frozen candidate and its motivating pair, without replay statistics. Its three verdicts \(v_{\mathrm{d}},v_{\mathrm{s}},v_{\mathrm{a}}\) require a supported diagnosis, independence from the source solution, and corrective actions grounded in failed checks or explicit task requirements. Selection retains

The two stages assess event-triggered selectivity and task-grounded guidance: a credible diagnosis can trigger indiscriminately, while a selective trigger can carry an unjustified correction. The selector accepts or rejects without editing. Selected policies are composed in source order within each interface (Figure 2c) and frozen before target evaluation. Because interventions alter later contexts, we evaluate the complete harness (Equation 19). Algorithm 1 uses proposal \(z_{i}\), checker acceptance \(h_{i}\), and replay counts \(\mathbf{n}_{i}=\mathbf{n}(u(z_{i}))\); Section B.2 details the judgments.

3.4 Constructing Evolution Evidence

The evolution set must provide informative failures and varied contexts for examining whether a diagnosis extends beyond its motivating task. We construct it from SWE-bench Pro (Deng et al., 2026), combining difficulty-ranked selection with repository coverage. For repository pool \(\mathcal{P}_{j}\), public multi-model solve rate \(r_{\mathrm{pub}}(x)\), and fixed language offset \(\beta_{\ell(x)}\), the ranking score and coverage constraints are

Low \(\kappa\) prioritizes low historical solve rates, adjusted by language preference. We select within repository difficulty bands, fill in ascending \(\kappa\) order, and enforce coverage. With \(n=100\) and \(m=4\), the set spans eleven repositories; three executions per task provide 300 trajectories for outcome contrasts and cross-task refinement.

The set retains SWE-bench Pro’s executable environments and verifiers (Deng et al., 2026). We check execution readiness for all 100 tasks and inspect instruction–test alignment in a language-stratified sample covering the four source-language groups. Selection parameters and quality checks appear in Sections C.1 and C.2.

After fixing \(\mathcal{S}\), we characterize its relationship to the target benchmarks through task type (the requested operation) and application domain (its intended use). Model-assisted annotation assigns these labels under a common codebook. For either view \(f\), category proportions \(p_{D}^{f}(z)\) in task set \(D\) define the total variation (TV) distance:

TV is zero for identical proportions and one for disjoint categories (Figures 4 and 4.2).

4 Experiments

We first measure how well TransHarness transfers across benchmarks, models, and harnesses. We then compare evolution methods using the same model, source trajectories, and initial harness, and use ablations to identify which design choices support transfer.

4.1 Experimental Setup

Evolution data and target benchmarks. For each configuration, we run the base agent three times on each task in our independent 100-task evolution set (Section 3.4). TransHarness constructs and selects interventions from the resulting 300 trajectories. We freeze each evolved harness before testing on DeepSWE v1.1 (113 tasks) (Huang et al., 2026; Huang & Jiang, 2026) or on Terminal-Bench 2.1 (89 tasks) (Merrill et al., 2026; The Terminal-Bench Team, 2026).

Models and harnesses. We evaluate DeepSeek V4.1 Flash (1017) (DeepSeek-AI, 2026a), GLM-5.3 Flash (Z.ai, 2026a), and Qwen3.8-Flash-Next (Qwen Team, 2026a). Our lightweight harnesses are Mini-SWE on DeepSWE and Terminus 2 on Terminal-Bench (SWE-agent Team, 2026; Harbor Team, 2026). Native harnesses include DeepSeek Harness, ZCode, and Qwen Code (DeepSeek-AI, 2026b; Z.ai, 2026b; Qwen Team, 2026b). We fix the model settings, tools, environment, and execution limits when comparing the base and evolved harnesses.

Comparison settings. Table 3 compares base and evolved configurations on both benchmarks alongside public scores (Datacurve, 2026; Artificial Analysis, 2026b). On DeepSWE v1.1, we compare TransHarness, Meta-Harness, Self-Harness, and RRSI using the same DeepSeek V4.1 Flash (1017) model, initial Mini-SWE 2.4.6 harness, and source trajectories from this configuration, with method-specific search budgets (Lee et al., 2026; Zhang et al., 2026a; Xia et al., 2026). No RRSI candidate passed its acceptance rule; we evaluate the candidate with the highest source success rate, breaking ties by lower token cost.

Score reporting. All our evaluations report means over three independent runs (\(N=3\)); public scores come from official reports or public leaderboards. For Tables 3, 3 and 4, we compute scores, recovery and regression contributions, and net gains from the underlying execution outcomes at full precision, then round each reported quantity independently to one decimal place. Subtracting displayed scores or summing displayed recovery and regression contributions may therefore differ from the reported net gain by 0.1 percentage points.

4.2 Main Results

Transfer across benchmarks and harnesses. Table 3 shows that TransHarness improves DeepSeek, Qwen, and GLM on both benchmarks, with gains across lightweight and native harnesses. On DeepSWE v1.1, improvements hold for Mini-SWE and all three native harnesses, with Qwen Code gaining the most at 7.9 points. On Terminal-Bench 2.1, all three models likewise improve with either Terminus 2 or their native harnesses. DeepSeek with Mini-SWE and DeepSeek Harness achieves the best scores on the respective benchmarks, 76.4% and 95.5%, surpassing GPT-6 Astra by 2.4 and 5.6 points. For these two configurations, paired gains over their respective base harnesses have 95% CIs of \([-2.4,\,8.8]\) and \([-1.1,\,12.4]\) points (Section C.3).

Transfer under distribution shift. Our independent evolution set differs from the target benchmarks in both repository coverage and task distribution. It shares none of DeepSWE’s 91 repositories and emphasizes repair and extension in product workflows. DeepSWE centers on software development, while Terminal-Bench spans build, data production, and system configuration (The Terminal-Bench Team, 2026) (Figure 4a,b). With the target subset fixed, replacing a benchmark-internal evolution set (Zhang et al., 2026a) with our independent set increases mean domain-distribution distance from 0.13 to 0.70 on DeepSWE and from 0.18 to 0.64 on Terminal-Bench. The gap persists at matched evolution-set sizes (Figure 4c). We further examine transfer to unseen task compositions. TransHarness improves success on compositional OOD tasks in all four DeepSeek configurations, with Mini-SWE and Terminus 2 gaining 14.6 and 4.1 points, respectively (Section C.3). These gains show that evolved policies can apply to requirement combinations absent from the source tasks.

4.3 Comparison with Harness Evolution Methods

Starting from the same Mini-SWE base, the methods obtain different cross-benchmark gains from source-task evolution. Meta-Harness (Lee et al., 2026) gains 2.0 points on the evolution set but loses 4.1 on DeepSWE (Figure 1a,c). Self-Harness and RRSI recover failures in 13.3% and 11.5% of all paired executions, respectively, but regress in 13.0% and 11.2%, leaving each with a net gain of only 0.3 points (Table 3). In comparison, TransHarness recovers 13.0%, close to Self-Harness, while reducing regressions to 9.7%, the lowest among the compared evolution methods. By retaining recovery gains while disrupting fewer successful executions, TransHarness reaches 76.4% on DeepSWE, exceeding the base harness and strongest comparator by 3.2 and 2.9 points, respectively. Section C.6 reports paired confidence intervals and scores for all three evaluation runs.

4.4 Ablation Analysis

Intervention timing. We first examine whether guidance depends on the execution context in which it is delivered (Table 4). Runtime variants share interfaces, policy order, and activation caps, with similar guidance lengths. Delivering the same guidance at the first eligible event rather than the learned trigger reduces success to 72.6%. Recovery remains close to the full method, 12.7% versus 13.0%, but regressions rise from 9.7% to 13.3%. Thus, learned timing preserves much of the guidance’s corrective benefit while reducing disruption to executions that would otherwise succeed.

Diagnostic guidance. Retaining the learned trigger and diagnostic topic, we replace evidence-based reassessment with a prescribed correction. Success falls to 65.5%, recovery drops to 8.8%, and regressions rise to 16.5%. Combining direct correction with early activation yields the highest regression rate, 17.7%. Together, these controls explain how intervention design shapes the balance in Equation 4. The trigger identifies a relevant execution context, while diagnostic guidance directs the agent to resolve the issue using current requirements and evidence. Fixing the correction in advance weakens both failure recovery and preservation of successful behavior.

Construction review. Construction review examines the diagnostic basis and scope of candidate interventions before deployment. The separately constructed harness with fourteen unreviewed interventions reaches 67.3%, whereas the reviewed seven-intervention harness reaches 76.4%, with more recoveries and fewer regressions (Table 4). The example in Section 3.2 illustrates the role of this refinement. Review preserves the need for verification while restricting repair to failures caused by the current code change, avoiding guidance that would turn unrelated failures into unnecessary edits.

4.5 Additional Analyses

Policy transfer on Koota. The Koota case shows how a source-evolved policy adapts to a new task (Figure 3). After local tests pass, the policy prompts the agent to reassess requirement coverage, revealing untested NOT-update behavior. The agent then adds a test and repairs the cache key. The base harness passes 41 of 43 task-specific tests, while Self-Harness, which checks verification evidence before completion (Zhang et al., 2026a), passes 42. TransHarness passes all 43, and all three harnesses pass the 172 regression tests. Here, the source policy provides a reason to question incomplete verification, while the target task supplies the requirement and evidence needed to derive the repair.

Source budget. We compare harnesses constructed from nested subsets of the independent evolution set. Harnesses built from 25 and 50 tasks fall below the base, while those built from 75 and 100 tasks gain 1.2 and 3.2 points (Table 3). The 50-task harness recovers more failures than the 100-task harness, yet incurs a larger regression loss, 17.1 versus 9.7 points. The stronger result with 100 tasks therefore reflects fewer disrupted successes rather than more recoveries. This comparison reinforces the need to assess transferable evolution through both kinds of outcome change.

Evolution cost. TransHarness achieves the highest DeepSWE score, 76.4%, with the lowest evolution cost among the compared methods, 132.7M tokens (Figure 5). The cost difference largely reflects candidate validation. Fresh source executions account for over 99% of the recorded evolution tokens for Meta-Harness and Self-Harness. TransHarness instead replays archived trajectories to examine trigger behavior and reviews guidance for dependence on source-specific assumptions. This design screens for transferable policies with fewer new executions while achieving stronger target performance.

5 Conclusion

We presented TransHarness, a framework for evolving harnesses beyond their source benchmark. It combines context-sensitive triggers with diagnostic guidance, using cross-task replay and independent semantic selection to refine interventions. Evolved on an independent task set, TransHarness improves strong coding models with both lightweight and mature harnesses and achieves state-of-the-art results on DeepSWE v1.1 and Terminal-Bench 2.1. Gains on compositional OOD tasks further demonstrate transfer to unseen requirement combinations. Ablations and target-task analysis show how selective intervention and evidence-based reassessment support these gains, enabling corrections on new tasks while reducing disruption to successful executions.

Impact Statement

This work improves coding agents through their execution infrastructure, without updating model weights. More reliable harnesses can reduce repeated debugging and improve automated software development. Because evolved interventions influence code changes and verification, deployment should retain checks appropriate to software security and maintainability alongside functional task evaluation.

References

- Agrawal et al. (2026) Agrawal, L. A., Tan, S., Soylu, D., Ziems, N., Khare, R., Opsahl-Ong, K., Singhvi, A., Shandilya, H., Ryan, M. J., Jiang, M., Potts, C., Sen, K., Dimakis, A., Stoica, I., Klein, D., Zaharia, M., and Khattab, O. GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning. In International Conference on Learning Representations, pp. 8479–8565, 2026. URL https://proceedings.iclr.cc/paper_files/paper/2026/hash/0e9e708b6f48e14fd0ac29e167413f76-Abstract-Conference.html.
- Artificial Analysis (2026a) Artificial Analysis. Artificial analysis intelligence benchmarking methodology. Artificial Analysis, 2026a. URL https://artificialanalysis.ai/methodology/intelligence-benchmarking. Accessed November 7, 2026.
- Artificial Analysis (2026b) Artificial Analysis. Terminal-Bench 2.1 benchmark. Artificial Analysis, 2026b. URL https://artificialanalysis.ai/evaluations/terminalbench-2-1. Accessed November 7, 2026.
- Datacurve (2026) Datacurve. DeepSWE leaderboard. Datacurve, 2026. URL https://deepswe.datacurve.ai/. Accessed October 22, 2026.
- DeepSeek-AI (2026a) DeepSeek-AI. DeepSeek-V4.1-Flash-1017. Hugging Face model card, 2026a. URL https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017. Accessed October 22, 2026.
- DeepSeek-AI (2026b) DeepSeek-AI. DeepSeek Harness: Everything is a Plugin. GitHub software repository, 2026b. URL https://github.com/deepseek-ai/deepseek-harness. Accessed November 16, 2026.
- Deng et al. (2026) Deng, X., Da, J., Pan, E., He, Y. Y., Ide, C., Garg, K., Lauffer, N., Park, A., Rane, C., Sampath, K., Krishnan, M., Kundurthy, S. R., Hendryx, S. M., Wang, Z., Zhang, C. B. C., Jacobson, N., Liu, B., and Kenstler, B. SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks? In Proceedings of the 43rd International Conference on Machine Learning, volume 306 of Proceedings of Machine Learning Research, pp. 23917–23934. PMLR, 2026. URL https://proceedings.mlr.press/v306/deng26f.html.
- Ding et al. (2026) Ding, R., Shen, Q., Han, Z., Chen, M., Chen, D., and Li, Y. Agentic Data Engineering for LLMs: System Design and a Controlled Empirical Study. In Workshop for Autonomous Machine Learning Research at NeurIPS, 2026. URL https://openreview.net/forum?id=bTVUsrguDi.
- Gou et al. (2024) Gou, Z., Shao, Z., Gong, Y., Shen, Y., Yang, Y., Duan, N., and Chen, W. CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing. In International Conference on Learning Representations, pp. 57734–57811, 2024. URL https://proceedings.iclr.cc/paper_files/paper/2024/hash/fef126561bbf9d4467dbb8d27334b8fe-Abstract-Conference.html.
- Harbor Team (2026) Harbor Team. Terminus-2. Official software documentation, 2026. URL https://www.harborframework.com/docs/agents/terminus-2. Accessed November 16, 2026.
- Hu et al. (2025) Hu, S., Lu, C., and Clune, J. Automated Design of Agentic Systems. In International Conference on Learning Representations, pp. 21344–21377, 2025. URL https://proceedings.iclr.cc/paper_files/paper/2025/hash/36b7acf6f6010652b3f2a433774a66fe-Abstract-Conference.html.
- Huang & Jiang (2026) Huang, W. and Jiang, P. DeepSWE v1.1: A cleaner, more reproducible benchmark for frontier coding agents. Datacurve, 2026. URL https://deepswe.datacurve.ai/blog/deepswe-v1-1. Accessed October 22, 2026.
- Huang et al. (2026) Huang, W., Lee, C., Tng, L., and Ge, S. DeepSWE: Measuring Frontier Coding Agents on Original, Long-Horizon Engineering Tasks. arXiv preprint arXiv:2607.07946, 2026. URL https://arxiv.org/abs/2607.07946.
- Khattab et al. (2024) Khattab, O., Singhvi, A., Maheshwari, P., Zhang, Z., Santhanam, K., A, S. V., Haq, S., Sharma, A., Joshi, T., Moazam, H., Miller, H., Zaharia, M., and Potts, C. DSPy: Compiling Declarative Language Model Calls into State-of-the-Art Pipelines. In International Conference on Learning Representations, pp. 54928–54958, 2024. URL https://proceedings.iclr.cc/paper_files/paper/2024/hash/f1cf02ce09757f57c3b93c0db83181e0-Abstract-Conference.html.
- Koh et al. (2021) Koh, P. W., Sagawa, S., Marklund, H., Xie, S. M., Zhang, M., Balsubramani, A., Hu, W., Yasunaga, M., Phillips, R. L., Gao, I., Lee, T., David, E., Stavness, I., Guo, W., Earnshaw, B., Haque, I., Beery, S. M., Leskovec, J., Kundaje, A., Pierson, E., Levine, S., Finn, C., and Liang, P. WILDS: A Benchmark of in-the-Wild Distribution Shifts. In Proceedings of the 38th International Conference on Machine Learning, volume 139 of Proceedings of Machine Learning Research, pp. 5637–5664. PMLR, 2021. URL https://proceedings.mlr.press/v139/koh21a.html.
- Lee et al. (2026) Lee, Y., Nair, R. S., Zhang, Q., Lee, K., Khattab, O., and Finn, C. Meta-Harness: End-to-End Optimization of Model Harnesses. In Conference on Language Modeling, 2026. URL https://proceedings.colm.cc/paper_files/paper/2026/hash/fde1a69a5b6e554b2f1f727197d2651d-Abstract-Conference.html.
- Lin et al. (2026) Lin, J., Liu, S., Pan, C., Lin, L., Dou, S., Xi, Z., Huang, X., Yan, H., Han, Z., Gui, T., and Jiang, Y.-G. Agentic harness engineering: Observability-driven automatic evolution of coding-agent harnesses. arXiv preprint arXiv:2604.25850, 2026. URL https://arxiv.org/abs/2604.25850.
- Madaan et al. (2023) Madaan, A., Tandon, N., Gupta, P., Hallinan, S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N., Prabhumoye, S., Yang, Y., Gupta, S., Majumder, B. P., Hermann, K., Welleck, S., Yazdanbakhsh, A., and Clark, P. Self-Refine: Iterative Refinement with Self-Feedback. In Advances in Neural Information Processing Systems, volume 36, pp. 46534–46594, 2023. doi: 10.52202/075280-2019. URL https://papers.nips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html.
- Merrill et al. (2026) Merrill, M., Shaw, A., Carlini, N., Li, B., Raj, H., Bercovich, I., Shi, L., Shin, J., Walshe, T., Buchanan, E. K., Shen, J., Ye, G., Lin, H., Poulos, J., Wang, M., Nezhurina, M., Lu, D., Menis Mastromichalakis, O., Xu, Z., Chen, Z., Liu, Y., Zhang, R., Chen, L. L., Kashyap, A., Uslu, J.-L., Li, J., Wu, J., Yan, M., Bian, S., Sharma, V., Sun, K., Dillmann, S., Anand, A., Lanpouthakoun, A., Koopah, B., Hu, C., Guha, E., Dreiman, G., Zhu, J., Krauth, K., Zhong, L., Muennighoff, N., Amanfu, R., Tan, S., Pimpalgaonkar, S., Aggarwal, T., Lin, X., Lan, X., Zhao, X., Liang, Y., Wang, Y., Wang, Z. R., Zhou, C., Heineman, D., Liu, H., Trivedi, H., Yang, J., Lin, J., Shetty, M., Yang, M., Omi, N., Raoof, N., Li, S., Zhuo, T. Y., Lin, W., Dai, Y., Wang, Y., Chai, W., Zhou, S., Wahdany, D., She, Z., Hu, J., Dong, Z., Zhu, Y., Cui, S., Saiyed, A., Kolbeinsson, A., Rytting, C., Marten, R., Wang, Y., Jitsev, J., Dimakis, A., Konwinski, A., and Schmidt, L. Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces. In International Conference on Learning Representations, pp. 40903–40986, 2026. URL https://proceedings.iclr.cc/paper_files/paper/2026/hash/444a3737adaee10d86ad2ef5f74468e6-Abstract-Conference.html.
- Platzer & Reutterer (2021) Platzer, M. and Reutterer, T. Holdout-based empirical assessment of mixed-type synthetic data. Frontiers in Big Data, 4:679939, 2021. doi: 10.3389/fdata.2021.679939. URL https://www.frontiersin.org/journals/big-data/articles/10.3389/fdata.2021.679939/full.
- Qwen Team (2026a) Qwen Team. Qwen3.8-Flash-Next. Hugging Face model card, 2026a. URL https://huggingface.co/Qwen/Qwen3.8-Flash-Next. Accessed October 22, 2026.
- Qwen Team (2026b) Qwen Team. Qwen Code. GitHub software repository, 2026b. URL https://github.com/QwenLM/qwen-code. Accessed November 16, 2026.
- Robeyns et al. (2025) Robeyns, M., Szummer, M., and Aitchison, L. A Self-Improving Coding Agent. In ICLR Workshop on Scaling Self-Improving Foundation Models without Human Supervision, 2025. URL https://openreview.net/forum?id=rShJCyLsOr.
- Shinn et al. (2023) Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., and Yao, S. Reflexion: language agents with verbal reinforcement learning. In Advances in Neural Information Processing Systems, volume 36, pp. 8634–8652, 2023. doi: 10.52202/075280-0377. URL https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html.
- SWE-agent Team (2026) SWE-agent Team. mini-SWE-agent. Official software documentation, 2026. URL https://mini-swe-agent.com/latest/. Accessed November 16, 2026.
- The Terminal-Bench Team (2026) The Terminal-Bench Team. Terminal-Bench 2.1. Terminal-Bench, 2026. URL https://www.tbench.ai/news/terminal-bench-2-1. Accessed October 22, 2026.
- Ursekar et al. (2026) Ursekar, V., Shanker, A., Maurya, Y., Yasser, S., Kalmath, V. S., Chatrath, V., and Xue, Y. HarnessOpt-Bench: Evaluating LLMs at Harness Optimization. arXiv preprint arXiv:2608.06301, 2026. URL https://arxiv.org/abs/2608.06301.
- Wang et al. (2024) Wang, X., Chen, Y., Yuan, L., Zhang, Y., Li, Y., Peng, H., and Ji, H. Executable Code Actions Elicit Better LLM Agents. In Proceedings of the 41st International Conference on Machine Learning, volume 235 of Proceedings of Machine Learning Research, pp. 50208–50232. PMLR, 2024. URL https://proceedings.mlr.press/v235/wang24h.html.
- Wang et al. (2025) Wang, X., Li, B., Song, Y., Xu, F. F., Tang, X., Zhuge, M., Pan, J., Song, Y., Li, B., Singh, J., Tran, H., Li, F., Ma, R., Zheng, M., Qian, B., Shao, D., Muennighoff, N., Zhang, Y., Hui, B., Lin, J., Brennan, R., Peng, H., Ji, H., and Neubig, G. OpenHands: An Open Platform for AI Software Developers as Generalist Agents. In International Conference on Learning Representations, pp. 65882–65919, 2025. URL https://proceedings.iclr.cc/paper_files/paper/2025/hash/a4b6ad6b48850c0c331d1259fc66a69c-Abstract-Conference.html.
- Wang et al. (2026a) Wang, Y., Zhu, H., Hu, Z., Yuan, Y., Chen, Z., Senthil, S., Hajishirzi, H., Tsvetkov, Y., Smith, N. A., Dasigi, P., and Xiao, T. Rethinking the Evaluation of Harness Evolution for Agents. arXiv preprint arXiv:2607.12227, 2026a. URL https://arxiv.org/abs/2607.12227.
- Wang et al. (2026b) Wang, Z., Ge, Y., Wang, Z., Wang, H., Xu, Y., Frandsen, J., Fu, S., Wilson, A. C., and Reddy, C. K. VERSE: Verified Self-Evolving Optimizer for Agent Harnesses. arXiv preprint arXiv:2610.02616, 2026b. URL https://arxiv.org/abs/2610.02616.
- Wu et al. (2026a) Wu, S., Ren, J., Li, Y., Li, H.-S., Yang, C., Ma, X., Zhang, Y., Gu, W., Yang, J., Batista-Navarro, R., Zhang, C., Liu, X., Zhou, M., Dai, B., and Lin, C. ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement. arXiv preprint arXiv:2609.14857, 2026a. URL https://arxiv.org/abs/2609.14857.
- Wu et al. (2026b) Wu, Y., Zhang, J., Shi, J., Lei, X., Gu, Q., Zhang, Y., Wang, Z., He, C., Huang, C., Song, M., Zeng, Z., Wang, S., Liu, J., Shi, Y., Liu, J., Yan, S., Huang, W., Zhang, G., and Zhang, W. HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness? arXiv preprint arXiv:2609.01437, 2026b. URL https://arxiv.org/abs/2609.01437.
- Xia et al. (2026) Xia, P., Han, R., Wang, Z., Chen, Y., Zhuang, Y., Lee, Y., Huang, C., Yu, H., CuiZhu, Z., Ming, Y., Yao, H., Gokturk, B., Pfister, T., and Lee, C.-Y. RRSI: Regularized Recursive Self-Improvement of Agent Harnesses. arXiv preprint arXiv:2609.24972, 2026. URL https://arxiv.org/abs/2609.24972.
- Yang et al. (2024a) Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q. V., Zhou, D., and Chen, X. Large Language Models as Optimizers. In International Conference on Learning Representations, pp. 12028–12068, 2024a. URL https://proceedings.iclr.cc/paper_files/paper/2024/hash/3339f19c5fcee3ad74502947a32be9e6-Abstract-Conference.html.
- Yang et al. (2024b) Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K., and Press, O. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. In Advances in Neural Information Processing Systems, volume 37, pp. 50528–50652, 2024b. doi: 10.52202/079017-1601. URL https://papers.nips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html.
- Yao et al. (2023) Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., and Cao, Y. ReAct: Synergizing Reasoning and Acting in Language Models. In International Conference on Learning Representations, 2023. URL https://openreview.net/forum?id=WE_vluYUL-X.
- Yuan et al. (2026) Yuan, L., Cai, Y., Liu, W., Yang, S., Han, F., Lee, Y., Sehwag, U. M., and Huang, F. Meta2: Precomputing reusable knowledge for online harness evolution in long-horizon agents. arXiv preprint arXiv:2611.05139, 2026. URL https://arxiv.org/abs/2611.05139.
- Z.ai (2026a) Z.ai. GLM-5.3-Flash. Hugging Face model card, 2026a. URL https://huggingface.co/zai-org/GLM-5.3-Flash. Accessed October 22, 2026.
- Z.ai (2026b) Z.ai. ZCode. Official software website, 2026b. URL https://zcode.z.ai/en. Accessed November 16, 2026.
- Zhang et al. (2026a) Zhang, H., Zhang, S., Li, K., Zhang, C., Chen, Y., Zhang, Y., Bai, L., and Hu, S. Self-Harness: Harnesses That Improve Themselves. arXiv preprint arXiv:2606.09498, 2026a. URL https://arxiv.org/abs/2606.09498.
- Zhang et al. (2025) Zhang, J., Xiang, J., Yu, Z., Teng, F., Chen, X., Chen, J., Zhuge, M., Cheng, X., Hong, S., Wang, J., Zheng, B., Liu, B., Luo, Y., and Wu, C. AFlow: Automating Agentic Workflow Generation. In International Conference on Learning Representations, pp. 34040–34077, 2025. URL https://proceedings.iclr.cc/paper_files/paper/2025/hash/5492ecbce4439401798dcd2c90be94cd-Abstract-Conference.html.
- Zhang et al. (2026b) Zhang, J., Hu, S., Lu, C., Lange, R., and Clune, J. Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents. In International Conference on Learning Representations, pp. 104223–104294, 2026b. URL https://proceedings.iclr.cc/paper_files/paper/2026/hash/aa5f5e6eb6f613ec412f1d948dfa21a5-Abstract-Conference.html.
- Zhang et al. (2026c) Zhang, L., Zhou, R., Song, D., Chen, Z., Tian, Y., Yang, J., Ma, H., Li, C., Feng, G., Li, X., Jin, Y., and Xu, Y. Harnesscompass: Guiding automatic harness evolution toward generalizable and effective agent harnesses. arXiv preprint arXiv:2608.01918, 2026c. URL https://arxiv.org/abs/2608.01918.
- Zhang et al. (2024) Zhang, S., Zhang, J., Liu, J., Song, L., Wang, C., Krishna, R., and Wu, Q. Offline Training of Language Model Agents with Functions as Learnable Weights. In Proceedings of the 41st International Conference on Machine Learning, volume 235 of Proceedings of Machine Learning Research, pp. 60315–60335. PMLR, 2024. URL https://proceedings.mlr.press/v235/zhang24cd.html.
- Zhao et al. (2024) Zhao, A., Huang, D., Xu, Q., Lin, M., Liu, Y.-J., and Huang, G. ExpeL: LLM Agents Are Experiential Learners. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pp. 19632–19642, 2024. doi: 10.1609/aaai.v38i17.29936. URL https://ojs.aaai.org/index.php/AAAI/article/view/29936.
- Zhuo et al. (2025) Zhuo, T. Y., Vu, M. C., Chim, J., Hu, H., Yu, W., Widyasari, R., Yusuf, I. N. B., Zhan, H., He, J., Paul, I., Brunner, S., GONG, C., Hoang, J., Zebaze, A., Hong, X., Li, W.-D., Kaddour, J., Xu, M., Zhang, Z., Yadav, P., Jain, N., Gu, A., Cheng, Z., Liu, J., Liu, Q., Wang, Z., Hui, B., Muennighoff, N., Lo, D., Fried, D., Du, X., de Vries, H., and Von Werra, L. BigCodeBench: Benchmarking Code Generation with Diverse Function Calls and Complex Instructions. In International Conference on Learning Representations, pp. 66602–66656, 2025. URL https://proceedings.iclr.cc/paper_files/paper/2025/hash/a6a90bcc2aa470c3871b2d39a67d26e8-Abstract-Conference.html.

Appendix A Analysis Details

A.1 Improvement Ceiling and Selectivity

Let \((Y_{0},Y_{B})\) be paired binary outcomes with base success rate \(p_{0}\), conditional rescue rate \(r\), and conditional regression rate \(q\). Partitioning the four possible outcome pairs gives

Because \(0\leq r,q\leq 1\), the gain is bounded by

For \(0&lt;p_{0}&lt;1\), a positive gain occurs if and only if

For \(q>0\), positive gain equivalently requires \(r/q>p_{0}/(1-p_{0})\). Increasing baseline success simultaneously contracts the improvement ceiling and raises the recovery-to-regression ratio required for further gains (Figure 6). The achievable rates depend on the model, harness, and task distribution. When \(q=0\), any positive recovery rate yields a gain.

At \(p_{0}=0\) or \(p_{0}=1\), one conditional rate is undefined, so we use the unconditional paired probabilities directly. A baseline that never succeeds can only improve or remain unchanged; a baseline that always succeeds can only regress or remain unchanged.

The net gain depends on marginal success rates; its recovery and regression components additionally depend on the pairing. Our empirical analysis pairs executions by task and repeat, as specified in Section C.6.

A.2 Exposure and Conditional Value

Consider executions of \(H\) and \(H+u\) on task \(x\) coupled through a common random stream. Assume that their inputs, environment transitions, and effects of resource limits agree until \(u\) first acts. Let \(A_{u}\) denote that event. Their histories agree before \(A_{u}\), and their outcomes agree if \(A_{u}\) never occurs. Hence

Conditioning the outcome difference on \(A_{u}\) and its complement yields Equation 2. It also gives

and

Under this coupling, a regression requires exposing an otherwise successful execution to the intervention. When \(\mathbb{P}_{Q}(A_{u})=0\), the expected gain is zero.

The event \(A_{u}\) includes resource effects that can alter outcomes, including trigger computation that exhausts a time limit. Session-wide guidance has exposure probability one. This coupling defines the theoretical decomposition; empirical task-paired statistics use the API executions described in Section C.6.

A.3 Transfer and Composition

For \(D\in\{P,Q\}\) with positive exposure, write \(a_{D}=\mathbb{P}_{D}(A_{u})\) and \(v_{D}=\mathbb{E}_{D}[Y_{H+u}-Y_{H}\mid A_{u}]\). Subtracting the source and target factorizations in Equation 2 and adding and subtracting \(a_{Q}v_{P}\) gives

This is the identity in Equation 3. The decomposition first changes exposure while holding source conditional value fixed, then changes conditional value at target exposure. Both factors can vary across distributions. In particular, \(a_{Q}=a_{P}\) leaves the gain difference \(a_{Q}(v_{Q}-v_{P})\): the same activation frequency can accompany a lower target value when the behavior being corrected is justified by new requirements. Task-dependent reassessment allows guidance to be interpreted against those requirements. At zero exposure the gain is zero; the conditional value is undefined, and the conditional decomposition is used only where its exposure terms are positive.

For ordered bundle prefixes \(B_{j}=(u_{1},\ldots,u_{j})\) with \(B_{0}=\varnothing\), the total gain decomposes as

Each term is the marginal contribution of an intervention after its predecessors have been applied. Each contribution is conditioned on its predecessors, because composition changes the contexts in which later interventions act. The ordered bundle is therefore the unit of final evaluation.

Appendix B Method Details

B.1 Source Evidence and Candidate Construction

The author examines complete successful and failed trajectories, including task instructions, model messages, tool calls, and observations. It also receives the runtime interfaces and checking tools. The task repository, reference solution, and hidden grading tests are excluded from the authoring workspace. Each within-task success–failure pair starts from the same base harness, so candidates are developed independently.

The DeepSeek Harness replay cohort contains the motivating pair, additional failed executions, and mixed-outcome executions from other source tasks. A deterministic task-name split reserves approximately one quarter of tasks with only failed executions; the remainder enter replay. Cross-task feedback excludes the motivating task, broadening validation beyond the failure that produced the candidate.

B.2 Candidate Refinement and Final Selection

Candidate construction separates authoring review from the final selection in Section 3.3. The author diagnoses a same-task success–failure contrast and implements an intervention against the base harness. A separate reviewer checks the diagnosis and proposed guidance against both executions. It may edit guidance wording or return changes to the diagnosis or trigger for one author rework. The checker validates the final implementation and records replay behavior. Table 5 illustrates a refinement that preserves verification while narrowing the repair obligation.

Final selection uses fixed replay criteria followed by an independent semantic assessment. The activation gate in Equation 6 uses other source-task pairs, excluding the motivating task. The selector bases its verdict on the completed candidate, the original pair, and the harness interface specification. Its decision is independent of cross-task activation statistics and target outcomes, and it accepts or rejects each candidate. After rework, the revised intervention undergoes the same assessment.

Each of the three semantic judgments requires explicit evidence. Diagnosis assessment checks that the cited actions support the claimed defect, that the successful execution does not contradict the account, and that a competing explanation has not been ignored. Source-independence assessment rejects task-specific names, values, or instructions that reveal the successful solution. Guidance assessment permits inspection and verification, while requiring a failed check or a conflicting explicit requirement before a corrective edit. Changes to existing test expectations require an explicit contrary requirement. A candidate is retained only when all three judgments pass; selected members preserve their source order within each interface.

B.3 Policies in the Evolved Qwen Code Harness

We illustrate construction and selection with Qwen3.8-Flash-Next and Qwen Code. Applying TransHarness to 26 source trajectory pairs produced eleven candidates that passed the replay gate. Eight also passed all three independent semantic checks for diagnosis, source independence, and guidance. Of these retained policies, three were revised by the authoring agent, two received wording refinements from the reviewer, and three were accepted as proposed. The policy set and its order were fixed before target evaluation. The evolved harness achieves a mean success rate of 89.9% on Terminal-Bench 2.1 (Table 3). Table 6 describes each policy by its activation context and diagnostic purpose.

B.4 Selection and Transfer Cases

Source selection.

A candidate for reviewing self-authored checks in Qwen Code diagnosed how a self-written check reinforced an incorrect resampling rule. It passed replay and the semantic checks for diagnosis and source independence. Its guidance, however, treated existing repository behavior as binding whenever the instruction was ambiguous. On the motivating trace, the trigger fired before a requirement check had failed. The selector rejected the candidate because the guidance prescribed an implementation at a point where the available evidence supported further verification. The decision illustrates what semantic selection adds to replay. A well-placed intervention can still prescribe a correction that the task does not support.

Target recovery.

In Terminal-Bench’s build-cython-ext task, the agent must build and install a Python package compatible with NumPy 2.3.0. After adapting its code for renamed graph attributes in a dependency, the evolved DeepSeek Harness prompted the agent to check the closest existing implementation. The agent searched the module and repository for an equivalent normalization helper, found none, and retained the compatibility change. It then reran the repository tests and installed the rebuilt package. The evolved execution passed all eleven benchmark checks. The base execution passed nine, failing the repository and its test-suite checks. The policy transferred a check for an existing implementation to a new compatibility repair.

B.5 Intervention Scope and Validation

The runtime exposes five groups of intervention locations. The agent loop accepts guidance at session start or before a model step. Observation and context-management locations add guidance to, or reorganize, successful tool results while retaining the underlying information. The tool interface can deny a pending call once with guidance while permitting an identical retry, or add a tool. The completion interface can request a bounded continuation before termination. These locations determine the information a check can inspect and the actions it can affect.

Validation first checks permitted edits, access to grading information, interface use, and attribution, then compiles and replays the candidate. Replay records actual changes to messages and control flow independently of the candidate’s own activation reports. Violations of information preservation, retry permission, or eventual termination reject the candidate. Timing, coverage, and activation in successful executions provide feedback for refinement.

For DeepSeek Harness, accepted policies are composed and their full execution chain is replayed. The runtime fixes the order of interface locations and preserves the selected policy order within each location. Construction and replay use recorded trajectories; fresh source executions subsequently evaluate the composed harness. Applying TransHarness to another runtime requires mapping these intervention locations and preserving their execution constraints.

Appendix C Evaluation Details

C.1 Evolution Set Construction

Our independent evolution set is selected from the 731-task SWE-bench Pro release (Deng et al., 2026). Selection combines the difficulty score and coverage constraints in Equation 8. Public resolution rates are averaged over available model records, with language offsets \(\beta_{\mathrm{JS}}=0\), \(\beta_{\mathrm{TS}}=0.02\), \(\beta_{\mathrm{Go}}=0.06\), and \(\beta_{\mathrm{Python}}=0.10\). These offsets prioritize JavaScript/TypeScript and Go during difficulty-ranked selection; task names resolve ties.

For each repository owner, the initial pass selects up to two tasks with \(r_{\mathrm{pub}}\leq 0.15\), one with \(0.15&lt;r_{\mathrm{pub}}\leq 0.40\), and one with \(0.40&lt;r_{\mathrm{pub}}\leq 0.60\), in ranked order. A global pass fills the set to 100 while limiting Python to 28 tasks during this pass; an uncapped fallback applies if the set remains incomplete. A final coverage pass inserts the hardest remaining tasks from owners represented by fewer than four tasks, replacing tasks from the most represented owner. The eleven owners in this pool correspond to eleven repositories. The source pool and targets have disjoint repository identifiers; task names fix the final ordering.

The resulting coverage and difficulty profile appears in Figure 7. Each selected task has six to nine public model records, with a mean historical resolution rate of 7.2%; 78 tasks remain unresolved in these records. The difficulty criterion concentrates trajectories on challenging behavior, while the repository floor spreads that evidence across eleven codebases. The resulting archive provides both failures to learn from and varied contexts in which to assess whether the proposed policies apply.

C.2 Source Quality Checks

All 100 selected tasks include the statements, environments, and verifier artifacts needed for execution. Each has a nonempty test patch, a reference-test overlay, and a fail-to-pass set; 64 also specify a nonempty pass-to-pass set. Reference tests and solutions remain outside the agent and candidate-author workspaces. The task descriptions used by the runtime originate from the repository change requests in the source release.

Instruction–test inspection examines four tasks, one per source-language label, selected in task-name order. Their tests cover Redis TLS configuration, room-selection updates, locally reachable IP discovery, and vCard 4.0 import. We also identify two instruction issues: a missing integration-submodule revision and an unrelated OCI-interface block in a Navidrome artwork task. For task-content annotation, the reference patch and tests establish the intended artwork requirements, and the unrelated block is excluded. Agent inputs and execution records retain the original materials.

C.3 Source–Target Composition

We treat repositories as domains (Koh et al., 2021) and use tasks as observations, irrespective of the number of executions. Source repository and language labels come from the selected tasks’ metadata; DeepSWE labels come from task metadata (Huang et al., 2026). Repository URLs are normalized for case, trailing slashes, and the .git suffix. The eleven source repositories and 91 DeepSWE repositories are disjoint, as are task identifiers and exact instruction strings.

We group mixed JavaScript/TypeScript projects consistently in both sets. Source counts for JavaScript/TypeScript, Go, Python, and Rust are \((72,16,12,0)\), compared with \((40,34,34,5)\) on DeepSWE, yielding an empirical total variation of 0.366.

Common task-content analysis.

Task intent and functional requirements provide complementary views of code benchmarks (Deng et al., 2026; Zhuo et al., 2025; Merrill et al., 2026). For Figure 4, we apply one codebook to the 100 source, 113 DeepSWE, and 89 Terminal-Bench instructions. Generic benchmark wrappers are excluded. The task-type label identifies the requested final deliverable: repair existing software; extend or restructure it; build a new solution; produce data or analytical results; or configure or restore a system. Adding a previously unsupported mode or format is extension; restoring an already expected behavior is repair. Mixed tasks are assigned by their principal requested deliverable.

Eight non-exclusive labels record explicit requirements: (i) interface or data-format contracts; (ii) state, concurrency, or resource lifecycles; (iii) compatibility with existing behavior, callers, versions, or platforms; (iv) substantive system setup, build, or service operation; (v) mathematical or numerical targets; (vi) performance or resource constraints; (vii) security or access control; and (viii) user-interface rendering or interaction. Ordinary counters do not imply numerical computation, output ordering does not imply stateful execution, and benchmark timeouts do not imply a performance requirement. Requirements absent from the instruction are left unmarked.

Model-assisted coding records supporting instruction passages for each positive label. An independent pass labels twelve fixed-seed tasks per task set, and disagreements are resolved against the common definitions. Each task contributes once; requirement labels are non-exclusive, so their proportions can exceed 100% in total.

Application domain.

We additionally code what the requested functionality is for, independently of the type of change or its execution requirements. The six classes are product workflows, programming and development, systems and services, data and content processing, scientific and ML computing, and security and cryptography. Each task receives one primary class from its full instruction. A specific product flow takes precedence over incidental processing mechanisms; specialist scientific or security purposes take precedence over library form. Generic programming abstractions are development tasks. Deploying an existing service is a systems task, even when its acceptance test exercises built-in user flows.

All 302 domain annotations use full task instructions and supporting passages. An independent pass over twelve tasks per set yields initial agreement of 12/12 on the evolution set, 11/12 on DeepSWE, and 10/12 on Terminal-Bench. Ambiguous boundaries include programming-object construction versus content conversion, and the classification of formal game solving and ML model selection as scientific computing. Alternative labels are retained for two evolution tasks, four DeepSWE tasks, and five Terminal-Bench tasks; the distance analysis below assesses their effect.

Distribution distances.

Using Equation 9, task-type distances from our independent evolution set are 0.4704 for DeepSWE and 0.9213 for Terminal-Bench; application-domain distances are 0.6996 and 0.6140 (Tables 7 and 4). The domain differences persist under arbitrary reassignment of all flagged labels: the corresponding lower bounds remain 0.644 and 0.538. Together with disjoint repositories and differing requirement frequencies, these comparisons characterize the shift under which harness transfer is evaluated.

Within- and cross-benchmark comparison.

Figure 4c compares evolution-set distributions against identical evaluation tasks. We draw 10,000 uniform random 2:1 partitions per benchmark, with evolution/evaluation sizes of 75/38 for DeepSWE and 59/30 for Terminal-Bench 2.1. For each evaluation subset, we compute its distance to the complementary within-benchmark set and to our fixed 100-task independent evolution set. The base random seed is 20261111; the second benchmark uses the next seed. Bars report mean distances; whiskers span the 5th–95th percentiles across partitions. The within-benchmark splits provide a distributional reference motivated by Self-Harness (Zhang et al., 2026a).

For DeepSWE, mean task-type distances are 0.041 for within-benchmark evolution and 0.470 for our independent evolution set; corresponding domain distances are 0.128 and 0.704. On Terminal-Bench, the pairs are 0.160/0.922 and 0.184/0.639. Matching source sizes by subsampling our set to 75 or 59 tasks preserves the contrast: mean task-type/domain distances are 0.471/0.705 for DeepSWE and 0.922/0.645 for Terminal-Bench.

Compositional out-of-distribution transfer.

We call a target task compositionally OOD when its exact nonempty set of requirement labels never occurs in the evolution set. This identifies 16 DeepSWE v1.1 tasks and 49 Terminal-Bench 2.1 tasks. Three Terminal-Bench tasks lack a positive requirement label and contribute to the full-benchmark results.

We also measure how the frequency of label combinations shifts between source and target. For a subset \(A\) of the \(m=8\) binary requirements and a pattern \(z\), let \(p_{A}(z)\) and \(q_{A}(z)\) be the source and target proportions. We average total variation over subsets of size \(k\) (Platzer & Reutterer, 2021):

We use all 8, 28, and 56 subsets of sizes one, two, and three. Figure 8 shows larger discrepancies for Terminal-Bench than for DeepSWE at each size.

Section C.3 reports paired gains for DeepSeek across both benchmarks and both harness types. All four gains are positive on compositional OOD tasks. On DeepSWE, Mini-SWE gains 14.6 points and DeepSeek Harness gains 25.0. On Terminal-Bench, Terminus 2 gains 4.1 points and DeepSeek Harness gains 2.0. The intervals resample tasks within each evaluated subset and preserve the base/evolved pairing. For DeepSeek Harness on DeepSWE, the paired analysis uses the same 70.8% base score reported in Table 3.

C.4 Evaluation Sources and Cost

The DeepSeek Harness source trajectories were collected with the September release of DeepSeek V4.1 Flash; source validation and target evaluation use DeepSeek V4.1 Flash (1017). DeepSeek source trajectories for Mini-SWE and Terminus 2 were collected with DeepSeek V4.1 Flash (1017) at max reasoning effort.

Public DeepSWE scores use the October 19, 2026 Datacurve snapshot (Datacurve, 2026). Terminal-Bench 2.1 scores use the highest score per listed model in the November 7, 2026 Artificial Analysis snapshot (Artificial Analysis, 2026b). Those evaluations use Terminus 2 with an agent limit of at least 7,200 seconds (Artificial Analysis, 2026a). Table 9 lists the reported reasoning settings.

Evolution cost counts input and output tokens for candidate construction and source validation, with cached inputs counted once. We exclude shared archive collection and target evaluation. Table 10 explains the difference in Figure 5. Fresh source executions account for over 99% of the recorded evolution tokens of Meta-Harness and Self-Harness. The measured Mini-SWE construction uses replay and semantic review to screen policies for transfer, with zero new scored source runs.

∗Artificial Analysis reports Gemini 3.1 Pro Preview. †The Fable 5 configuration uses Opus 4.8 as a fallback.

C.5 Compared Methods

Meta-Harness.

A meta-agent searches over harness code using an archive of prior candidates, outcomes, and execution traces. Source evaluations provide the feedback for ranking harness revisions (Lee et al., 2026).

Self-Harness.

The agent mines recurring weaknesses from execution traces and proposes targeted changes to its harness. The acceptance procedure checks gains and regressions on development and held-out source tasks (Zhang et al., 2026a).

RRSI.

RRSI regularizes both proposal and acceptance. Its search favors sparse, evidence-backed edits and explores underused components. Its selection rule balances measured improvement, stability, and execution cost (Xia et al., 2026).

C.6 Scores and Paired Outcomes

For \(n\) target tasks and \(N\) independent runs of a fixed harness \(H\), the reported score is

where \(y_{ik}^{H}\) is a binary task outcome. We pair base and evolved outcomes by task and evaluation index.

Let \(N_{ab}\) count paired executions with base outcome \(a\) and evolved outcome \(b\). We report recovered and regressed percentages as \(100N_{01}/(Nn)\) and \(100N_{10}/(Nn)\). Their difference equals the net score gain. The corresponding conditional rates are \(r=N_{01}/(N_{01}+N_{00})\) and \(q=N_{10}/(N_{10}+N_{11})\), giving recovered and regressed percentages of \(100(1-p_{0})r\) and \(100p_{0}q\). All executions enter these counts, including those without an activated check. A paired task bootstrap resamples whole tasks, preserving the conditions and all repetitions within each task.

All methods use the same adjudication rule. Verifier and environment defects are corrected while preserving the submitted implementation and test assertions; accepted repairs include test-name isolation, report-name normalization, and consistent execution parallelism. Crashes that produce incomplete test reports are scored as failures. Agent errors and exhausted budgets also count as failures. Infrastructure-only interruptions are replaced under the same rule across methods.

Table 11 reports paired outcomes for the three independent evaluation runs. The gain ranges from 0.0 to 6.2 percentage points across the three runs. Overall, TransHarness solves 259 of 339 executions, compared with 248 for the base harness, with 44 recoveries and 33 regressions. Resampling the 113 tasks with all paired repetitions in 50,000 bootstrap replicates gives 95% intervals of \([69.9,82.6]\) for success and \([-2.4,8.8]\) for the gain. The across-run standard deviation is 1.0 percentage point.

C.7 Intervention Design Comparisons

The execution variants in Table 4 separate the roles of context selection and guidance formulation within the evolved harness. The variant without learned triggers delivers each intervention at its first eligible interface event. The variant without reassessment preserves the learned trigger and diagnostic subject and replaces diagnostic guidance with a prescribed correction. Task requirements and evidence remain part of that guidance. Interfaces, ordering, activation caps, and global policies are shared, so these comparisons examine how the same diagnostic subject enters execution and shapes the agent’s response.

The unreviewed construction instead examines the harness obtained from fourteen author-produced interventions after interface validation. The main configuration combines seven reviewed interventions. This comparison evaluates the resulting content and composition together, complementing the execution variants with evidence about construction feedback. The source example in Section 3.2 illustrates the underlying revision: verification remains required, while repair is scoped to failures caused by the current change.

C.8 Source-Budget Settings

Table 3 compares harnesses constructed from nested source subsets with three archived executions per task. The 25-, 50-, and 75-task conditions use patch extraction, fixed activation thresholds, and semantic screening; the 100-task condition is the main seven-intervention harness. All conditions use the complete DeepSWE target and the same paired-outcome definitions.

Appendix D Extended Related Work

From feedback to reusable knowledge.

Feedback can improve an agent’s current answer or change what it carries into subsequent tasks. Self-Refine iteratively critiques and revises outputs with the same model (Madaan et al., 2023), while CRITIC grounds correction in external tool feedback (Gou et al., 2024). Reflexion retains verbal feedback across attempts (Shinn et al., 2023); ExpeL extracts reusable insights from task experience (Zhao et al., 2024). These approaches establish complementary roles for feedback: identifying a local mistake and retaining knowledge that can guide later decisions. TransHarness builds on this distinction at the harness level. Its diagnostic guidance identifies an issue to reassess, and its executable trigger determines when that issue becomes relevant in a new execution. The resulting policy transfers a procedure for examining evidence, allowing the correction itself to depend on the target task.

The object of optimization.

Harnesses organize coding agents’ reasoning, tools, and verification (Yao et al., 2023; Wang et al., 2024). Prompt and program optimization use evaluation feedback to improve instructions or compositions of language-model calls (Yang et al., 2024a; Khattab et al., 2024; Agrawal et al., 2026), while automated agent design searches broader executable structures (Hu et al., 2025; Zhang et al., 2025). Harness evolution makes the execution system itself editable, including its tools, control flow, and verification behavior (Robeyns et al., 2025; Zhang et al., 2026b; Lee et al., 2026). Recent work structures this search through module-level attribution, constrained component edits, or knowledge that guides task-local evolution (Wu et al., 2026a; Zhang et al., 2026c; Yuan et al., 2026). Within this design space, TransHarness treats a trigger and its diagnostic guidance as a coupled policy. This representation makes two questions explicit: which observed execution contexts warrant intervention, and what evidence should the agent examine there? Cross-task replay evaluates the first question against both successful and failed source executions. Semantic selection examines the second by checking the diagnosis and whether the guidance remains meaningful without the source task’s particular solution.

Selection evidence and transfer.

Candidate selection determines which source-derived changes survive into deployment. Regression checks and regularized acceptance can discourage harmful updates (Zhang et al., 2026a; Xia et al., 2026), while executable verification can test proposed improvements during evolution (Wang et al., 2026b). Their effect on new tasks also depends on how search feedback relates to the final evaluation distribution. Separating development feedback from held-out evaluation is therefore central to interpreting agent improvement (Wang et al., 2026a; Wu et al., 2026b; Ding et al., 2026). Our independent evolution set extends this separation across benchmarks, with task-content analysis characterizing the resulting distribution shift. The empirical argument combines that setting with target success, paired recovery and regression, and intervention ablations: distribution analysis establishes where transfer is tested, while target outcomes and controlled comparisons establish its value and explain the role of the evolved policies.
