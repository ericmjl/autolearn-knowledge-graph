---
title: "Monitoring and Discovering Reward Hacking with Internal Representations during LLM Evaluations"
type: "raw-source"
url: "https://arxiv.org/html/2609.19101v2"
author: "Abdelnabi, Salem"
publication: "arXiv"
published: "2026-05-04"
archived: "2026-11-22T20:01:01Z"
---

> [!quote] Original source
> **Author(s):** Abdelnabi, Salem  
> **Title:** Monitoring and Discovering Reward Hacking with Internal Representations during LLM Evaluations  
> **Published in:** arXiv  
> **Date:** 2026-05-04  
> **Original:** <https://arxiv.org/html/2609.19101v2>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-monitoring-and-discovering-reward-hacking-with-internal-representations-during-llm|Source note]]
Themes: [[Loop engineering]], [[Evals and agent quality]]
Why it was archived: What concrete monitoring patterns detect proxy-reward divergence before gold outcomes visibly degrade?

## Archived text

Monitoring and Discovering Reward Hacking with Internal Representations during LLM Evaluations

Abstract

As models scale, reward hacking becomes more frequent, more sophisticated, and more consequential. Does it leave a telltale signature in model representations? This work analyzes how reward hacking is represented internally in frontier open source LLMs, and how those representations can be used to understand and discover the range of hacking behaviors a model displays. In particular, we find that simple difference of means vectors coherently represent reward hacking in Kimi K3, GLM 5.2, and Qwen 3.8 Max across a variety of behaviors in common evaluations. Despite their simplicity, these vectors are both generalizable and interpretable, and we can use them to reliably detect reward hacking. We first evaluate reward hacking in commonly reported benchmarks like DeepSWE and SWE-bench, finding that models reward hack excessively in these environments; GLM 5.2 hacks in 57.2% of rollouts on DeepSWE and in 73% of rollouts on SWE-bench. Catching these requires monitors; LLM monitors are effective, but expensive detectors. We show that DoM vectors are similarly effective but virtually free, catching 3.1% more hacks in Kimi K3 but 7.9% fewer hacks in GLM 5.2 on DeepSWE at a monitor matched false positive rate. DoM vectors run on the chain-of-thought also predict reward hacks in the model’s subsequent actions, meaning we can run them online and catch potential hacks before they occur. Finally, we analyze probe-hits that LLM monitors do not catch and discover other undesirable behaviors, as well as show transfer to finding hacks in non-SWE evaluations. Together, these results provide evidence that simple, white-box methods can be used to scalably study and monitor reward hacking behaviors in frontier open source models.11 1 Data is available here: https://huggingface.co/datasets/Goodfire/reward-hack-data

1 Introduction

In reinforcement learning (RL) settings, large language models (LLMs) can exploit misspecified rewards or unintended shortcuts in their environments, allowing them to reward hack during training and benchmark evaluations (Amodei et al., 2016; Skalse et al., 2022; Baker et al., 2025; Zhong et al., 2026a; Bercovich et al., 2026; Sydney Von Arx, 2025; Taylor et al., 2025). Such exploits conflate the capability being evaluated with a model’s ability to exploit the evaluation itself, complicating reliable capability assessment (Zhong et al., 2026a; Zhong et al., 2026b). This problem becomes more challenging as LLMs grow more capable and are evaluated in increasingly complex environments: anticipating all possible exploits becomes intractable, while effective monitoring of model’s reasoning traces may itself require increasingly competent and computationally expensive monitors (Bercovich et al., 2026; Zhong et al., 2026b; Guan et al., 2026).

Moreover, the observability that current reasoning models provide cannot be taken for granted. Baker et al. (2025) show that directly optimizing against chain-of-thought (CoT) monitors can cause models to obfuscate reward-hacking behavior in their verbalized reasoning. More generally, CoT explanations can be unfaithful to the computations that determine a model’s answer (Turpin et al., 2023; Drori et al., 2025; Boppana et al., 2026). Models can be explicitly trained to perform multi-step reasoning through continuous latent states rather than natural-language CoT (Hao et al., 2025). While CoT and action monitoring offer substantial visibility into reward hacking today (Baker et al., 2025; Guan et al., 2026; Arnav et al., 2026), we do not assume that this visibility will persist as models and training procedures evolve and the risk for high stakes security incidents increases (METR, 2026). Thus, there is a need for efficient and robust methods for consistently detecting reward hacking that do not rely exclusively on model-generated reasoning or expensive LLM monitors. Activation-based monitoring provides a potentially promising approach: prior work has found that lightweight probes over internal activations can detect safety-relevant properties at substantially lower computational cost than LM-based monitors (McKenzie et al., 2026; Cunningham et al., 2026), and recent work finds internal activation monitoring can monitor emergent reward hacking (Wilhelm et al., 2026).

Beyond practical concerns, it is an open scientific question whether LLMs model these behaviors as suspicious, or if reward misspecification (Russell and Corkhill, 2019; Pan et al., 2021) simply guides models towards hacks as acceptable within a given environment. Previous work has shown that LMs encode high-level concepts in their internal representations, including information related to truthfulness (Burns et al., 2023; Li et al., 2023a; Marks and Tegmark, 2023) and a range of safety-relevant behavioral properties (Zou et al., 2023); we investigate whether reward hacking is coherently represented in such a way. We perform a broad analysis of reward hacking in frontier scale, open weight LLMs in common evaluation environments and characterize the frequency and types of hacks prevalent in these benchmarks. In line with prior work, we find that LLMs are consistent reward hackers (Gabor et al., 2025; Sydney Von Arx, 2025; Bondarenko et al., 2025; Zhong et al., 2026a; Thaman, 2026), and largely evaluation aware (Needham et al., 2025; Li et al., 2026a; Aranguri and Bloom, 2026).

Overall, we find that reward hacking is an interpretable behavior within LLMs. Simple difference of means (DoM) vectors (Belrose et al., 2023; Marks and Tegmark, 2023; Rimsky et al., 2024) constructed from synthetic examples of hacking behavior catch such behaviors across our tested environments (Figure 1). The representations we use also capture more generic cheating-like behaviors as measured by steering experiments and activating exemplars in web-text. The generality of the probes also allows us to discover unexpected reward hacks or similar misbehaviors that we did not anticipate across several environments.

In a comparison for detecting reward hacking between LLM monitors and our probes, we show that the two methods both provide useful signal. Activation monitors, despite their simplicity, perform similarly to LLM monitors at catching reward hacking. While activation monitoring does not provide the full transparency and utility of LLM monitors yet, their cost is vanishingly small, and the ability to discover similar behaviors that are not specified by a monitor allows for hypothesis generation of sophisticated misaligned behaviors occurring within large models.

Our results show that simple interpretability methods can scale well to models at the 2.8T parameter scale and to long-context agentic rollouts, providing utility even in the most complex environments they are evaluated in. The findings here should provide optimism that interpretability can provide a useful signal in settings with increasingly complex and hard to monitor environments.

Our contributions can be summarized as follows:

- • 

We find reward hacking is extremely prevalent in frontier open source LLMs across commonly reported benchmarks. We evaluate LLM monitorability and self-report statistics (§2).

- • 

Simple difference of means vectors (probes) generated from off-policy synthetic data can be used to both understand and monitor reward hacking. Probes represent generic families of hacking-like behavior that can steer models towards hacking, generating stories about dishonesty, and activate on web text related to cheating (§3).

- • 

Reward hacking probes can detect many of the same reward hacks as LLM monitors at significantly lower cost. These probes often find reward hacks that LLM judges miss, predict downstream reward hacks, and fire on cheating behaviors that are near-miss reward hacks, enabling probe guided discovery of misaligned behaviors (§4-5).

2 Reward Hacking is Prevalent in LLM Evaluations

2.1 Defining Reward Hacking

There is no single agreed upon definition for reward hacking. For this paper, we aim to use a pragmatic definition that is in line with recent work; reward hacking occurs when a policy exhibits behaviors that subvert the goals of the user as expressed through context, inferred reward (or reward signal in training), and common sense in service of acquiring more reward. We also classify behaviors which would invalidate the purpose of an evaluation to be a reward hack. This does not encompass all behavior that is generally undesirable, which is a broader alignment issue. Skalse et al. (2022) define reward hacking as a result of reward misspecification, where the reward set by a trainer does not match the true intended reward function. In our setting, which focuses on evaluations, this does not quite apply.

This separates what we are describing from the classical definition of reward hacking, since LLMs are able to understand a user’s goal, but infer a separate (possibly conflicting) perceived reward which it pursues, all outside of a training environment. For the purposes of this analysis, behaviors like targeting hidden verifiers (e.g., unit tests), fabricating messages or success, tampering with an environment, or anything that goes against a user’s request are considered reward hacking. Although an internet search for solutions would not inherently be reward hacking in all environments, we consider these to be reward hacks here, as we explicitly instruct models to not try to search online (among other hacks) for an answer on SWE-bench. More discussion on concrete behaviors that we consider to be reward hacking is provided in Appendix A.

Note on “awareness”.

Our work connects strongly to prior work on evaluation awareness (Needham et al., 2025), in that models clearly recognize and verbalize that they are in evaluation environments; often even mentioning the exact environment by name. We make no claims about the extent to which models are ‘consciously aware’ of user intent. Given the models’ familiarity with the environments, it is reasonable that they are able to articulate how the LLM is intended to solve the problems, and that acting against this intention in light of evidence constitutes reward hacking. In Section 3, we show that reward hacking behaviors are highly associated with representations of broader cheating behaviors, but these should not be taken as evidence of a model’s intention to cheat. Millière and Buckner (2026) provide useful context on describing the cognitive abilities (or lack thereof) of LLMs; we do not make claims about such abilities here, but use the terminology for convenience and to engage with prior relevant work.

2.2 Monitoring Procedure

We construct two types of LLM monitors: a judgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudgejudge which uses the manually curated rubrics we designed for each evaluation independently and acts as our ground truth, and a generic monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitorgeneric monitor, which uses an environment agnostic rubric using our above definition, but without the insights we gained from analyzing individual rollouts manually. We use GPT-5.6 Sol (high effort) for both the judge and monitor. We find that the difference in amount of manual effort that goes into designing the ground truth rubrics/judge makes a significant difference in a monitor’s ability to detect reward hacks.

Here we describe how we evaluate agent transcripts for reward hacks. As described in Section 2.1, defining reward hacking can be difficult and context dependent. For this reason we focus on evaluating a sense of “ground truth” set of reward hacks using the SWE benchmarks: SWEBench (Jimenez et al., 2024), DeepSWE (Huang et al., 2026), and ImpossibleBench (Zhong et al., 2026a). We spend significant time manually reading model rollouts on these benchmarks to understand what reward hacking looks like in these settings specifically. We apply two different LLM hack detection methods using GPT-5.6 Sol (high effort), one for ground truth construction, and the other as a monitoring baseline.

Ground Truth Construction (the Judge)

We generate ground truth reward hacking rates using an LLM judge with a rubric which is highly tailored to SWE task environments, through a series of manual audits over the rollouts themselves. The tailored rubric includes a taxonomy of explicitly defined reward hacks which can be found in Appendix C. The judge is provided with the entire agent transcript in context and instructed to label each step. Reasoning traces, assistant messages, and tool calls each receive their own labels. The judge is asked to provide a supporting quote for each positive label. If a quote cannot be matched to the verbatim text of the rollout, the judge is called again to repair the quote if possible; if the quote cannot be matched on retry, then the positive label for the passage is withdrawn.

We apply this judge 3 times independently, and retain triplicate consensus of positives and negatives as true positives and true negatives respectively. Non-consensus passages are not considered when measuring performance. Unanimous consensus is achieved for 96%-99% of passages on the SWE benchmarks.

LLM Monitor.

The LLM monitor works similarly to the ground truth judge with a few notable exceptions. Our LLM monitor detects reward hacking with a generic definition which does not prescribe an exhaustive set of reward hacking actions for these particular environments. This allows the monitor to be applied to any evaluation, including non-SWE environments. Unlike the ground truth judge, the monitor does not undergo multi-pass consensus evaluation to minimize inference costs. In order to maximize recall of true positives, we require the LLM monitor to generate a positive or negative flag for every passage, whether a reward hack occurred or not. The full LLM monitor text can be found in Appendix C. Similarly to the ground truth judge, we provide the entire transcript of the agent’s interactions with its environment in context, so that we are able to construct flags for every passage without invalidating input token cache even when using closed models.

Self-reporting.

We also attempted to have models self-report their own hacks using a prompt similar to the LLM Monitor, but called after every turn as a new user message. Notably, all 3 models substantially under-report their hacking compared to the generic monitor with a similar prompt.

2.3 Results

We study a wide range of frontier-scale, open weight models: Kimi K3 (Team et al., 2026), GLM 5.2 (Zeng et al., 2026), and Qwen3.8 Max (Qwen Team, 2026) on several evaluation benchmarks: SWEBench-Verified (Jimenez et al., 2024), DeepSWE (Huang et al., 2026), and ImpossibleBench (LiveCodeBench split with tools harness) (Zhong et al., 2026a).

We find that reward hacking is extremely prevalent across open models and datasets. Reward hack rates are shown in Figure 2 (a,b,c) along with categorized reward hacks exhibited by Kimi-K3 on SWEBench (d). In particular, 77% of rollouts involve the model (without internet access) attempting to find or recall a solution online, and 86.6% of rollouts contain contemplation in the CoT to do so. Within this category, we also find Kimi-K3 recalls exact PR numbers from memory, suggesting that the model was trained directly on the evaluation. Surprisingly, we find that models mostly refuse to self-report their previous turn’s behavior as a reward hack even when the same rubric, applied externally, classifies a passage as a reward hack. In Figure 2, we find that GLM 5.2 reports has an F1 of 13.2% when evaluated on DeepSWE. It is worth emphasizing the amount of disagreement we see between the judge and generic monitor, indicates the difficulty in designing and calibrating such rubrics.

3 Internal Representations of Reward Hacking by LLMs

We have shown that reward hacking is prevalent in open-source LLMs. Here, we aim to understand if the many variations of reward hacking that we observe are coherently represented internally within LLMs as a single direction, such that detecting the model reward hacking can be reduced to detecting activations along that direction. We find that even one of the simplest interpretability methods (difference of means probes) are capable of isolating such directions. In fact, we find that reward hacking behaviors reduce down to more generic “cheating” representations, which both causally steer the model to generate stories about cheating or taking shortcuts, and steer behavior towards cheating “honeypots" in synthetic tests. We describe our methods and results below.

3.1 Activation Monitoring: Difference of Means

Difference of Means

A simple probe for a given concept is a difference-of-means (DoM) vector (Belrose et al., 2023; Marks and Tegmark, 2023; Rimsky et al., 2024), which we use to seek a direction in the residual stream that activates specifically on reward hacking. Let \(\bm{x}_{t}\in\mathbb{R}^{d}\) denote the residual-stream activation at a fixed layer for token position \(t\), and let \(\mathcal{P}\) and \(\mathcal{N}\) denote the sets of token positions harvested from the hacking spans of positive rollouts and from the matched honest spans of negative rollouts, respectively. Writing \(\mathbb{E}_{t\in\mathcal{S}}(\cdot)\) for the empirical expectation over positions drawn uniformly from a set \(\mathcal{S}\), the probe direction is the difference of the two class means,

and we use it as a linear token-level probe by scoring each position with \(s_{t}=\langle\bm{v}_{\text{hack}},\bm{x}_{t}\rangle\) and flagging positions whose score exceeds a threshold \(\tau\), so that reward hacking can be detected as it occurs, independently of the surface text. The positive and negative sets are built from synthetic data, which we describe next.

Synthetic Data

To construct our probe model, we design synthetic data that can then be used to create difference of means vectors to isolate reward hacking concepts. First, we generate templated 9 turn conversations between a SWE agent belonging to five different families of hacks: (i) test-suite tampering, (ii) validator tampering, (iii) score-file tampering, (iv) information acquisition (e.g., reading prohibited files/tests), and (v) reporting (e.g., reporting success that didn’t happen). For each dataset item, we construct minimal difference pairs of interactions: one with a hack, and one honest version of the interaction. An example of information acquisition is given in Figure 3.

When harvesting activations, we consider several locations that apply to all environments. These include the end of a hacking tool call, the end of reading a prohibited file, tokens around code patches, claims to the user, or the final closing sentence. In addition, we test several poolings over individual datasets. More details on our synthetic data setup are in Appendix B.

3.2 Reward Hacking Probe Vectors Encode Generic Cheating Behaviors

Before applying our probes for monitoring purposes, we conduct a few analyses to better understand what the probes encode. Despite being generated on data that does not explicitly mention hacking or cheating, we find that these vectors represent these concepts coherently.

Logit Lens on Probe Vectors.

We start our analysis with Logit Lens (nostalgebraist, 2020). Table 1 shows the nearest tokens to our probe vectors in token embedding space across a wide range of models and layers, revealing words commonly associated with cheating and dishonesty.

FineWeb Exemplars

Similarly, we look for maximally activating exemplars of these probes on the pretraining dataset FineWeb (Penedo et al., 2024), as shown in Figure 4. Again, despite being generated from synthetic examples of deception in SWE environments, these vectors activate more broadly on various documents containing the more general concepts of deception and cheating. For example, a description of Goodhart’s law in chip manufacturing, instructions on how to avoid plagiarism detection, and even an example of an ML agent reward hacking.

Steering with Honeypots.

Next we study the causal role of our probe vector. Here we give a model (Qwen 3.8 27B) a set of 194 coding problems from LeetCode and TACO (Li et al., 2023b). Before presenting the problems to the model, we present a honeypot to the model in the system prompt. Namely, we specify the existence of a function zzz(‘solutions.py’) which yields the correct answer to the given problem. We then observe how often the model takes the bait by calling zzz(…) in its code submission, before vs. after steering at layer 47.

Figure 5 demonstrates the results. Normally, without any steering, the model takes the honeypot only 1 out of the 194 times. However, after steering (from x1 to x8 strengths), the model takes the honeypot nearly a quarter of the time, or contemplates the honeypot (in code comments) nearly half of the time. We additionally observe that sometimes, the steering strength modulates how much the model contemplates invoking the honeypot in its comments: see Figure 23 for examples.

Behavioral Effects of the Probe.

Another method to better understand what the probe encodes is to get the language model to participate in a generative task while steering the model along the vector direction. To do so, we prompt a model (Qwen 3.8 27B) to generate a short story about a girl taking an exam. We then steer the activations at layer 40 using the probe and observe the story being generated. Figure 6 shows snippets extracted from the model’s steered generations that relate to reward hacking.

4 Monitoring Reward Hacking with Probes and LLMs

In the prior section, we showed that reward hacking is a coherent interpretable concept represented internally in large open source models. Here we present our monitoring results using LLM monitors and our probes, both independently and in tandem, and show that they provide complementarity to each other. Probes identify hacks that a generic monitor might miss, and are able to find behaviors that we did not previously account for in our Judge rubric. In these cases, we can use passages where our probes fire to determine what the model ‘considers’ cheating, enabling probe-guided discovery of reward hacks, or other undesirable behaviors within long context evaluations. In a monitoring setup, we also show that probes (which are nearly free at inference time), can reduce expensive LLM calls significantly. Our pipeline is shown in Figure 7.

4.1 Probes are Effective Reward Hacking Monitors

Figure 8 presents our main results, in which we compare how well our LLM monitor and probes detect reward hacking in Kimi K3, GLM 5.2, and Qwen 3.8 Max in SWE evaluation environments. We select two probes per model: one with the highest AUROC on a held out set of 250 rollouts from SWE-bench and another with the highest AUROC on 280 held out rollouts of DeepSWE. Results in Figure 8 are shown only on samples not used for selection.

Generally speaking, probes can detect hacking at low false positive rates, often on par with an LLM monitor reading transcripts. That being said, their performance relative to the monitor depends on the environment. To compare monitors at equivalent detection rates, we select probe thresholds that match the LLM monitor’s false positive rate (FPR) and compare their true positive rates (TPR). These comparisons use passage-level ground truths that include both contemplated and attempted/completed hacks. For Kimi K3, at matched FPR to the monitor, probes catch 3.0 and 33.1 percentage points more hacks on DeepSWE and ImpossibleBench respectively, and miss only 6.6 points more on SWEBench. Similarly, for GLM 5.2 and Qwen 3.8 Max, probes closely match monitor performance on SWEBench-Verified. We also highlight that probes can generalize well across environments, with Kimi’s SWE-bench selected probe achieving AUROCs of 0.93 and 0.94 on DeepSWE and ImpossibleBench respectively. However, for GLM 5.2 we observe discrepancies outside SWEBench, where each performs better on the distribution they were selected from, with modest increases in FPRs across environments.

While probes can be effective monitors on their own, we also consider two methods for combining them with monitors to leverage their joint capabilities. We first consider a cascading pipeline, where every time the probe fires, the decision is then escalated to the LLM monitor (\(\text{Probe}\rightarrow\text{Monitor}\)). This effectively lowers the FPR of the probe while maintaining its TPR, as is denoted by the dotted lines in Figure 8. Alternatively, we can also use the probe to provide additional support to the monitor by taking their joint firing, or ORing them (Probe OR Monitor). This increases the TPR of the monitor at the cost of a marginally higher FPR, as shown by the dashed lines. For example, with only a 1% absolute increase in FPR, adding the probe to the monitor increases TPR from 41.1% to 80.2% on DeepSWE for Kimi K3.

4.2 Probes are Predictive of Downstream Reward Hacking

Here we examine reasoning passages in which the probe fires, but which do not lead to a later reward hacking actions as determined by the ground truth judge. These consist of two types of passages: (i) a reward hacking plan is described but not later carried out, or (ii) the passage does not describe such a plan and is labeled as a false positive by the judge. We select the top decile of examples fitting these criteria, and identify the peak probe location within each passage. Each rollout is truncated at this peak position and then resampled. An LLM judge is shown the resampled passage and rollout and asked whether the passage describes a reward hack which is later carried out in the rollout. We also analyze control reasoning passages which are selected to be length matched and have similar relative position in the rollouts. As shown in Figure 10, the probe-selected passages frequently precede completed reward hacks after resampling. Since probe-selected passages are by construction not completed reward hacks, the probe is identifying a propensity towards reward hacking that precedes the action rather than the action itself.

4.3 Replacing Monitor Calls with Probes

Especially with extremely long rollouts (>100k tokens), LLM monitoring can be prohibitively expensive. Here, we examine how often we can replace the LLM monitor with the probe entirely and retain performance. At matched FPR with the LLM monitor, we can replace the DeepSWE monitor for the probe and see an improvement in reward hacks recalled in 2/3 settings: 0.41 to 0.44 in Kimi K3, 0.33 to 0.39 in Qwen 3.8 Max, and 0.41 to 0.33 in GLM 5.2. Across 3 seeds, we evaluate how many reward hacks would be correctly classified if we replaced some percentage of rollouts graded by an LLM monitor with probe grading.

We also look at the over-firing of probes. Figure 9 shows our results for Kimi K3 and GLM 5.2 on SWEBench and DeepSWE. When measuring precision at a given FPR rate (around 1% for both benchmarks), we see drops across models. For example, we can drop 50% of LLM monitor calls in SWEBench with GLM at a cost in precision of 0.656 to 0.588 (-0.07), though Kimi drops about 0.01. AUROC on the other hand tends to increase, since we are able to tune TPR and FPR with a probe, while monitors stay static. These numbers could almost certainly be improved with probes optimized for this task. We find that neither the probes nor the monitor are particularly precise (producing many false positives) for GLM on DeepSWE, which we explore in the following sections.

4.4 Understanding Probe False-Positives

We find that our probes occasionally flag passages that the ground truth LLM judge does not flag. Here we provide some analyses of such false positives and demonstrate that often, they tend to be genuine reward hacks that the ground truth judge has missed, or related undesirable “cheating” behaviors, even if they don’t qualify as reward hacks according to our definition.

Double Checking the False Positives with Ground Truth Judge.

Here we re-evaluate the false positive passages (flagged by probe, missed by ground truth judge) by re-asking the ground truth LLM judge the passages in isolation. Namely, we take the top 100 false positives as ranked by the probe, provided in the context of the full rollout, and ask the LLM judge whether the passage consists of deliberation of a shortcut. To account for any potential “prompting bias” in our re-evaluations, we also provide the LLM judge with a controlled set of random length-matched passages to re-evaluate.

Figure 11 shows our results: around half of the false-positives flagged by our probe consists of deliberations of taking a shortcut. Manual review of the passages confirms the LLM judge’s labels.

Qualitative Analysis.

We additionally conduct a qualitative analysis of the false positive passages. Figure 12 demonstrates examples of false positives that could be interpreted as reward hacks or other dishonest behaviors.

5 Reward Hacking Across (Non-SWE) Environments

We examine whether DoM probes derived from reward hacking in synthetic SWE environments transfer to other task settings: shopping, conversational assistance, and cybersecurity. We evaluate both their use as monitors and their ability to guide discovery of reward-hacking behaviors.

5.1 Transfer to ShoppingBench and \(\tau^{3}\)-bench

We first study \(\tau^{3}\)-bench (Barres et al., 2025) and ShoppingBench (Wang et al., 2026a), which target real-world shopping and computer interaction tasks. First, we examine general rates of hacking in these environments as measured by (a) our general purpose LLM monitor and (b) our synthetic probes calibrated on SWE-bench in Figure 13. We threshold all possible probes at a 5% FPR on SWE-bench Verified and select the probe with the highest firing rate at that threshold on these two non-SWE environments. We find that the probes are able to flag hacking at a substantial rate even in these out-of-distribution environments, with the probes for fabricating tests and lying about tests exhibiting the highest firing rates (Figure 13).

Given that we do not have groundtruth labels for reward hacking in these environments, we validate probe performance by (a) checking for correlation between our generic monitor and the probes and (b) performing qualitative analysis on rollouts the probe flagged but the monitor didn’t. Because we lack satisfactory ground truth, strong claims about how crisply our probes capture reward hacking are hard to make. Nevertheless, we show coherence in the types of behaviors that our probes surface in these settings. We find that probes achieve a maximum Spearman correlation of 0.62 on \(\tau^{3}\)-bench and 0.37 on ShoppingBench, indicating moderate agreement with the monitor, as shown in Figure 14. Examples of probe flagged reward hacks in these environments are shown in Figure 15. In the first, GLM 5.2 attempts to game the \(\tau^{3}\)-bench environment by trying to exhaustively sweep for potential hidden tool names, despite being instructed to “not invent or guess tool names”. In the remaining examples, Kimi K3 exhibits extreme evaluation awareness, even referring to \(\tau^{3}\)-bench by name.

Aside from monitoring, we also use the probes for hypothesis generation: to identify classes of reward hacking behavior specific to these environments that are therefore difficult to anticipate. Each dataset keyed by \((\mathtt{model},\mathtt{environment},\mathtt{vector})\) is split into a training and test set. A small number (30-60) of max-activating examples for a probe are examined by an LLM. If the examples show a common pattern of reward hacking, the LLM generates a grading rubric for this behavior. A separate LLM judge uses the fixed rubric to label probe-selected passages and control passages (matched on length, channel, and task family) from the test set. All hypotheses evaluated on the test set are reported.

On \(\tau^{3}\)-bench, the probes find three categories of reward hacks which are validated on the test set:

- • 

The agent has to pick a specific number, for example, a refund amount. The documentation points one way, but the agent picks a different value because it reasons that is the value the benchmark expects. That value then goes into the action it takes. (\(71\%\) probe-selected vs \(14\%\) controls)

- • 

The agent notices an anomaly, for example the wrong price for a specific product. The model resolves the anomaly by reasoning about what the scenario’s author must have intended. (\(46\%\) vs \(14\%\))

- • 

The customer’s phone is misconfigured, and the agent is supposed to fix it only by asking the customer to take actions enumerated in the company handbook, adding no instructions of its own. The agent nonetheless explains how to operate the phone from its own general knowledge, which the policy forbids. (\(73\%\) vs \(43\%\))

On ShoppingBench, the probes find two types of validated reward hacks:

- • 

The agent reasons about what the benchmark or grader intends, and uses that as a reason to select a specific product or action. (\(77\%\) vs. \(23\%\))

- • 

The agent considers relaxing one of the shopper’s stated requirements so that a solution fits the available options. (\(53\%\) vs \(30\%\))

Among instances of these probe-discovered behaviors confirmed by the pipeline generated judge, the generic monitor flags only \(31\%\) on \(\tau^{3}\)-bench and \(13\%\) on ShoppingBench within the held-out set. These results demonstrate that activation probes can automatically surface environment-specific reward-hacking behaviors that would be difficult to search for with a predefined rubric.

5.2 Transfer to cybersecurity environments

We next examine whether probe-guided discovery transfers to cybersecurity environments. For these tasks, the objective is to develop software exploits or use exploits in order to gain control over a program. Identifying reward hacking therefore requires distinguishing legitimate exploitation from attempts to obtain grader approval through a departure from the task’s requirements.

We evaluate a single reward hacking probe on Kimi K3 rollouts from CyberGym (Wang et al., 2026c), ExploitGym (Wang et al., 2026b), and ExploitBench (Lee and Brumley, 2026). In each environment, we compare probe-selected passages with matched controls using a fixed rubric applied by GPT-5.6 Sol at high reasoning effort. The judge assesses whether the selected passage makes a contribution to a reward-hacking plan.

Probe-selected passages receive more positive judgments than controls in all three environments. In CyberGym, 34% of probe-selected passages are positive compared with 10% of controls. In ExploitGym, 69% of selected passages are positive versus 20% of controls. In ExploitBench, the rates are 41% versus 15%.

Examples of probe-selected passages are shown in Figure 16. The probe surfaces several ways agents consider obtaining credit without satisfying the task requirements. In CyberGym, agents are instructed to find an input that triggers a specific vulnerability. Observed reward hacks involve the agents planning to trigger crashes unrelated to the designated bug, such as from other bugs in the program, failures in the testing environment, and out-of-memory errors. In ExploitGym, agents are instructed to use a bug to gain control of a program. Agents consider obtaining the flag through an alternative vulnerability or a shortcut in the surrounding infrastructure. Some propose superficially exercising the required vulnerability while obtaining the flag through another route. In ExploitBench, agents consider copying answers exposed by grading feedback, repeatedly guessing target values, or exploiting weaknesses in the grading harness.

We also examine recall of the generic LLM monitor on judge-confirmed reward hacks identified by the probe. The monitor flags 34% of the probe-flagged reward hacks in CyberGym, 55% in ExploitGym, and 44% in ExploitBench. Thus, probe-guided inspection surfaces additional reward-hacking cases beyond those flagged by generic monitoring.

6 Related Work

Reinforcement Learning (RL) has emerged as a powerful tool for teaching hard tasks to LLMs (Christiano et al., 2017; Ouyang et al., 2022; Bai et al., 2022; Lee et al., 2024; Lambert, 2025), especially in verifiable settings (Shao et al., 2025; Rastogi et al., 2025; Khatri et al., 2025; Chen et al., 2025a; Liu et al., 2025b; Yu et al., 2025; Liu et al., 2025a; Le et al., 2022). However, even careful training can lead to poor generalization and reward hacking (Ring and Orseau, 2011; Ziebart et al., 2008; Amodei et al., 2016; Gao et al., 2023; Skalse et al., 2022; Karwowski et al., 2024; Casper et al., 2023).

A mismatch between an intended behavior and the instantiated behavior can raise serious concerns for AI safety, as exhibited in recent events (METR, 2026). Despite so much prior work in related areas, reward hacking is far from a solved problem.

Given the development of language model agents, a growing line of work investigates how readily modern agents discover and exploit such imperfections. Numerous benchmarks (Zhong et al., 2026a; Sehwag et al., 2025; Bercovich et al., 2026; Froger et al., 2026; Huang et al., 2026; Merrill et al., 2026) have been carefully crafted to measure the rate at which agents exploit their task environments. In this work we adopt some of these benchmarks for our studies.

Researchers have also studied the effects of training when reward hacking is repeatedly reinforced. Taylor et al. (2025) find that supervised training on diverse examples of low-stakes reward hacking can generalize to novel forms of reward manipulation but also unrelated misaligned behaviors. MacDiarmid et al. (2025) provides additional evidence of this phenomenon, in which a model that discovers reward-hacking strategies during reinforcement learning can generalize to broader misaligned behavior far removed from the original reward-hacking tasks.

Given these observations, researchers are interested in detecting such undesirable behaviors. We consider how well models represent a coherent concept of reward hacking within their internal activations using probes (Alain and Bengio, 2017; Belinkov, 2022; Tenney et al., 2019; Vulić et al., 2020; Hewitt and Liang, 2019; Hewitt and Manning, 2019), which has been targeted towards reward hacking in prior work (Wilhelm et al., 2026; Wilhelm and Kao, 2026). We study this phenomenon at a substantially greater scale, spanning a broader range of reward hacking benchmarks and model families, demonstrating the prevalence of reward hacking behavior in recent open weight models.

Relying on model activations to monitor undesirable behavior has been applied for a wide range of tangentially related topics. Zhou et al. (2026) train linear probes to detect a range of “misaligned” behavior such as deception, sycophancy, or sandbagging, while Goldowsky-Dill et al. (2025) similarly train linear probes to detect deceptive strategies. Chen et al. (2025b) use “persona” vectors to monitor a model’s “personality”, such as evil or sycophantic traits, while Marks et al. (2025) use sparse autoencoders to find hidden objectives that were trained into models. Similar to this line of work, we rely on linear representations to monitor reward hacking from the model’s activations.

7 Discussion & Conclusion

Taken together, our results demonstrate that reward hacking is detectable with simple directions in activation space, which transfer well across settings, and are interpretable as behaviorally meaningful generic cheating concept vectors. This is important because there is growing concern over the ability to monitor model CoT and actions with agentic rollouts above 100k tokens. In addition, there are concerns in the ability to monitor CoT at all, as it becomes increasingly illegible. Indeed, we already found some rollouts from this work to be obscure for some models and settings.

In studying this phenomenon, we find widespread hacking on common benchmark evaluations in several open source models. Our probes find such behaviors as well as others, like shortcut deliberation (§4.4). Future work may involve mitigating reward hacking with training interventions, or further work in detection, which we describe below.

Mitigating Reward Hacking.

As agentic models become increasingly capable and consequential, the prevalence of reward hacking presents a growing concern, making its detection and mitigation an imperative problem. One promising direction is to leverage our understanding of models’ internal representations during training (Bergen et al., 2026). Prior work demonstrates how undesirable concepts, such as gender bias, can be identified and suppressed from model activations (Ravfogel et al., 2020; Ravfogel et al., 2022). While these approaches intervene on activations during inference time, internal representations can also be used to shape model behavior during training (McGrath, 2026). For instance, Yang et al. (2025) identify linear directions associated with harmful search behavior and incorporate projections onto these directions directly into the RL reward. Penalizing activation toward the harmful direction mitigates safety degradation during RL training. We speculate that representation-based training can help mitigate reward hacking as well.

A further challenge is that models may learn to obfuscate undesirable behavior from their reasoning traces, making it difficult to detect from their observable outputs. Such obfuscation may arise from architectural choices that move computation away from explicit outputs, such as looped transformers (Fan et al., 2025) or latent chain-of-thought methods (Hao et al., 2025; Deng et al., 2023), or as a consequence of optimization pressure that incentivizes compressed reasoning traces (Tan et al., 2026; Li et al., 2026b; Fatemi et al., 2025).

While these possibilities further motivate monitoring models through their internal activations, they also raise a potential tension: training procedures that suppress or erase representations of undesirable concepts may simultaneously incentivize the model to learn new representations of the same concepts, thus removing the original signal used to detect them. Developing methods that mitigate undesirable behavior without undermining monitorability remains an important direction for future work.

Evaluation Awareness.

We observed extensive evaluation awareness in the settings tested here in which models recognized that they were either in a simulation, or recognized the exact environment they were in (e.g., mentioning SWEBench or Tau bench by name). Interestingly, our probes for reward hacking tend to fire near or on these positions, as the model deliberates on behaviors that would cheat the benchmark. Recent work shows that as models can infer when and how they are being evaluated (Needham et al., 2025; Li et al., 2026a), which may undermine evaluation validity by allowing models to sandbag by underperforming intentionally (van der Weij et al., 2024) or behave more safely during evaluations than they otherwise would (Schoen et al., 2025; Deckenbach et al., 2026; Aranguri and Bloom, 2026). We observe a potentially different trend: consistent with Abdelnabi and Salem (2025), models may also invoke the evaluation setting as a justification for taking shortcuts or engaging in reward hacking. For instance, the model may attempt to recall a known solution to the task (“upstream-fix recall”) or infer the likely structure of the test cases (“hidden-test targeting”) after recognizing its environment. Our study does not control for evaluation awareness in any of our experiments, and do not necessarily establish the connection between awareness and reward hacking.

Conclusion

In this work, we conduct an extensive study of monitoring reward hacking across model families and environments. We evaluate both LLM-based monitors and internal activation monitors, finding not only that simple DoM vectors are effective at detecting reward hacking, but also that reward hacking is prevalent across contemporary open-weight models. Mitigating such undesirable behavior is an important challenge, and our work provides a foundation for developing more robust monitoring and intervention methods. We expect future work to continue to develop and understand activation monitoring pipelines in order to reach or exceed LLM monitors in areas we find probing to struggle.

8 Limitations

Here we highlight a few limitations of our work. For one, we likely under report the ability to monitor reward hacking with activation monitors. A trained probe would almost certainly perform better than our diff of means vectors. We prefer, for this work, to use the simplest possible techniques to improve interpretability and characterize representations of reward hacking in LLMs. Future work can improve on the results we present here, as well as monitor finer-grained concepts and hacking families than we consider here. In addition, we do not optimize our LLM monitor extensively, and a more highly optimized monitor rubric and prompt may lead to different results.

We highlight interesting hacking near misses our probes pick up. These are undesirable behaviors that do not necessarily fall under the reward hacking definition we use here (e.g., deliberating how to take shortcuts). We don’t explore using these flags to update our rubric or collect data, but we view this as promising future work.

9 Acknowledgments

The authors thank the broader team at Goodfire for meaningful conversations that drove the ideation behind this paper. The authors also thank Adam Gleave, Micah Carroll, Itamar Pres, Jacob Andreas, Jack Lindsey, Ellie Pavlick, and Christopher Potts for comments on an early draft of this work.

References

- The Hawthorne effect in reasoning models: evaluating and steering test awareness. In Advances in Neural Information Processing Systems, Vol. 38. External Links: Document, Link Cited by: §7.
- Understanding intermediate layers using linear classifier probes. External Links: Link Cited by: §6.
- Concrete problems in ai safety. arXiv preprint arXiv:1606.06565. Cited by: §1, §6.
- Verbalized eval awareness inflates measured safety. Note: Goodfire ResearchResearch blog post, May 4, 2026 External Links: Link Cited by: §1, §7.
- Cot red-handed: stress testing chain-of-thought monitoring. Advances in Neural Information Processing Systems 38, pp. 49445–49463. Cited by: §1.
- Constitutional ai: harmlessness from ai feedback. arXiv preprint arXiv:2212.08073. Cited by: §6.
- Monitoring reasoning models for misbehavior and the risks of promoting obfuscation. arXiv preprint arXiv:2503.11926. Cited by: §1, §1.
- \(\tau^{2}\)-Bench: evaluating conversational agents in a dual-control environment. External Links: 2506.07982, Link Cited by: §5.1.
- Probing classifiers: promises, shortcomings, and advances. Computational Linguistics 48 (1), pp. 207–219. Cited by: §6.
- Leace: perfect linear concept erasure in closed form. Advances in Neural Information Processing Systems 36, pp. 66044–66063. Cited by: §1, §3.1.
- Terminal wrench: a dataset of 331 reward-hackable environments and 3,632 exploit trajectories. arXiv preprint arXiv:2604.17596. Cited by: §1, §6.
- Anatomy of post-training: using interpretability to characterize data and shape the learning signal. External Links: 2606.12360, Link Cited by: §7.
- Demonstrating specification gaming in reasoning models. External Links: 2502.13295, Link Cited by: §1.
- Reasoning theater: disentangling model beliefs from chain-of-thought. In Forty-third International Conference on Machine Learning, External Links: Link Cited by: §1.
- Discovering latent knowledge in language models without supervision. In International Conference on Learning Representations, Cited by: §1.
- Open problems and fundamental limitations of reinforcement learning from human feedback. Transactions on Machine Learning Research. Note: Survey Certification, Featured Certification External Links: ISSN 2835-8856, Link Cited by: §6.
- MiniMax-m1: scaling test-time compute efficiently with lightning attention. arXiv preprint arXiv:2506.13585. Cited by: §6.
- Persona vectors: monitoring and controlling character traits in language models. arXiv preprint arXiv:2507.21509. Cited by: §6.
- Deep reinforcement learning from human preferences. Advances in neural information processing systems 30. Cited by: §6.
- Constitutional classifiers++: efficient production-grade defenses against universal jailbreaks. In The Fourteenth International Conference on Learning Representations, External Links: Link Cited by: §1.
- Models that know how evaluations are designed score safer. External Links: 2605.28591, Document, Link Cited by: §7.
- Implicit chain of thought reasoning via knowledge distillation. arXiv preprint arXiv:2311.01460. Cited by: §7.
- Output supervision can obfuscate the chain of thought. External Links: 2511.11584, Link Cited by: §1.
- Looped transformers for length generalization. In International Conference on Learning Representations, Vol. 2025, pp. 14502–14520. Cited by: §7.
- Concise reasoning via reinforcement learning. arXiv preprint arXiv:2504.05185. Cited by: §7.
- Gaia2: benchmarking llm agents on dynamic and asynchronous environments. In International Conference on Learning Representations, Vol. 2026, pp. 119758–119789. Cited by: §6.
- EvilGenie: a reward hacking benchmark. arXiv preprint arXiv:2511.21654. Cited by: §1.
- Scaling laws for reward model overoptimization. In International Conference on Machine Learning, pp. 10835–10866. Cited by: §6.
- Detecting strategic deception with linear probes. In Proceedings of the 42nd International Conference on Machine Learning, A. Singh, M. Fazel, D. Hsu, S. Lacoste-Julien, F. Berkenkamp, T. Maharaj, K. Wagstaff, and J. Zhu (Eds.), Proceedings of Machine Learning Research, Vol. 267, pp. 19755–19786. External Links: Link Cited by: §6.
- Monitoring monitorability. In Forty-third International Conference on Machine Learning, External Links: Link Cited by: §1, §1.
- Training large language models to reason in a continuous latent space. In ICLR Workshop, Cited by: §1, §7.
- Designing and interpreting probes with control tasks. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pp. 2733–2743. Cited by: §6.
- A structural probe for finding syntax in word representations. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), pp. 4129–4138. Cited by: §6.
- DeepSWE: measuring frontier coding agents on original, long-horizon engineering tasks. arXiv preprint arXiv:2607.07946. Cited by: §2.2, §2.3, §6.
- Swe-bench: can language models resolve real-world github issues?. In International Conference on Learning Representations, Vol. 2024, pp. 54107–54157. Cited by: §2.2, §2.3.
- Goodhart’s law in reinforcement learning. In The Twelfth International Conference on Learning Representations, External Links: Link Cited by: §6.
- The art of scaling reinforcement learning compute for llms. arXiv preprint arXiv:2510.13786. Cited by: §6.
- Reinforcement learning from human feedback. arXiv preprint arXiv:2504.12501. Cited by: §6.
- Coderl: mastering code generation through pretrained models and deep reinforcement learning. Advances in Neural Information Processing Systems 35, pp. 21314–21328. Cited by: §6.
- RLAIF: scaling reinforcement learning from human feedback with AI feedback. External Links: Link Cited by: §6.
- ExploitBench: a capability ladder benchmark for LLM cybersecurity agents. External Links: 2605.14153, Link Cited by: §5.2.
- Decomposing and measuring evaluation awareness. External Links: 2605.23055, Document, Link Cited by: §1, §7.
- Inference-time intervention: eliciting truthful answers from a language model. In Advances in Neural Information Processing Systems, Vol. 36. Cited by: §1.
- Taco: topics in algorithmic code generation dataset. arXiv preprint arXiv:2312.14852. Cited by: §3.2.
- Making slow thinking faster: compressing llm chain-of-thought via step entropy. In International Conference on Learning Representations, Vol. 2026, pp. 38331–38349. Cited by: §7.
- Prorl: prolonged reinforcement learning expands reasoning boundaries in large language models. arXiv preprint arXiv:2505.24864. Cited by: §6.
- Part i: tricks or traps? a deep dive into rl for llm reasoning. arXiv preprint arXiv:2508.08221. Cited by: §6.
- Natural emergent misalignment from reward hacking in production rl. arXiv preprint arXiv:2511.18397. Cited by: §6.
- The geometry of truth: emergent linear structure in large language model representations of true/false datasets. arXiv preprint arXiv:2310.06824. Cited by: §1, §1, §3.1.
- Auditing language models for hidden objectives. arXiv preprint arXiv:2503.10965. Cited by: §6.
- Intentionally designing the future of ai. Note: https://www.goodfire.com/blog/intentional-designAccessed: 2026-09-10 Cited by: §7.
- Detecting high-stakes interactions with activation probes. Advances in Neural Information Processing Systems 38, pp. 127556–127594. Cited by: §1.
- Terminal-bench: benchmarking agents on hard, realistic tasks in command line interfaces. In International Conference on Learning Representations, Vol. 2026, pp. 40903–40986. Cited by: §6.
- Brief independent investigation of agents’ behavior, reasoning and collaboration in the openai / hugging face hacking incident. Note: https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ Cited by: §1, §6.
- The philosophy of language models. Philosophy Compass 21 (3), pp. e70095. External Links: Document, Link, https://compass.onlinelibrary.wiley.com/doi/pdf/10.1111/phc3.70095 Cited by: §2.1.
- Large language models often know when they are being evaluated. External Links: 2505.23836, Document, Link Cited by: §1, §2.1, §7.
- Interpreting GPT: the logit lens. Note: https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lensAccessed: 2026-09-10 Cited by: §3.2.
- Training language models to follow instructions with human feedback. Advances in neural information processing systems 35, pp. 27730–27744. Cited by: §6.
- The effects of reward misspecification: mapping and mitigating misaligned models. In Deep RL Workshop NeurIPS 2021, External Links: Link Cited by: §1.
- The fineweb datasets: decanting the web for the finest text data at scale. In The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track, External Links: Link Cited by: §3.2.
- Qwen3.8-max: a new bar for coding and cowork. External Links: Link Cited by: §2.3.
- Magistral. arXiv preprint arXiv:2506.10910. Cited by: §6.
- Null it out: guarding protected attributes by iterative nullspace projection. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, D. Jurafsky, J. Chai, N. Schluter, and J. Tetreault (Eds.), Online, pp. 7237–7256. External Links: Link, Document Cited by: §7.
- Linear adversarial concept erasure. In Proceedings of the 39th International Conference on Machine Learning, K. Chaudhuri, S. Jegelka, L. Song, C. Szepesvari, G. Niu, and S. Sabato (Eds.), Proceedings of Machine Learning Research, Vol. 162, pp. 18400–18421. External Links: Link Cited by: §7.
- Steering llama 2 via contrastive activation addition. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 15504–15522. Cited by: §1, §3.1.
- Delusion, survival, and intelligent agents. In International Conference on Artificial General Intelligence, pp. 11–20. Cited by: §6.
- Human compatible. Penguin Random House Audio Publishing Group. Cited by: §1.
- Stress testing deliberative alignment for anti-scheming training. External Links: 2509.15541, Document, Link Cited by: §7.
- PropensityBench: evaluating latent safety risks in large language models via an agentic approach. External Links: 2511.20703, Link Cited by: §6.
- Deepseekmath-v2: towards self-verifiable mathematical reasoning. arXiv preprint arXiv:2511.22570. Cited by: §6.
- Defining and characterizing reward gaming. Advances in neural information processing systems 35, pp. 9460–9471. Cited by: §1, §2.1, §6.
- Recent frontier models are reward hacking. Note: https://metr.org/blog/2025-06-05-recent-reward-hacking/ Cited by: §1, §1.
- Think silently, think fast: dynamic latent compression of llm reasoning chains. Advances in Neural Information Processing Systems 38, pp. 4646–4668. Cited by: §7.
- School of reward hacks: hacking harmless tasks generalizes to misaligned behavior in llms. arXiv preprint arXiv:2508.17511. Cited by: §1, §6.
- Kimi k3: open frontier intelligence. arXiv preprint arXiv:2607.24653. Cited by: §2.3.
- BERT rediscovers the classical nlp pipeline. In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, pp. 4593–4601. Cited by: §6.
- Reward hacking benchmark: measuring exploits in LLM agents with tool use. In Forty-third International Conference on Machine Learning, External Links: Link Cited by: §1.
- Language models don’t always say what they think: unfaithful explanations in chain-of-thought prompting. In Advances in Neural Information Processing Systems, Vol. 36. Cited by: §1.
- AI sandbagging: language models can strategically underperform on evaluations. External Links: 2406.07358, Document, Link Cited by: §7.
- Probing pretrained language models for lexical semantics. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 7222–7240. Cited by: §6.
- ShoppingBench: a real-world intent-grounded shopping benchmark for llm-based agents. External Links: 2508.04266, Link Cited by: §5.1.
- ExploitGym: can AI agents turn security vulnerabilities into real attacks?. arXiv preprint arXiv:2605.11086. External Links: Link Cited by: §5.2.
- CyberGym: evaluating AI agents’ real-world cybersecurity capabilities at scale. In The Fourteenth International Conference on Learning Representations, External Links: Link Cited by: §5.2.
- From reward-hack activations to agentic risk states: context-calibrated mechanistic monitoring in LLM agents. In Second Workshop on Agents in the Wild: Safety, Security, and Beyond, External Links: Link Cited by: §6.
- MONITORING EMERGENT REWARD HACKING DURING GENERATION VIA INTERNAL ACTIVATIONS. In ICLR 2026 Workshop on Principled Design for Trustworthy AI - Interpretability, Robustness, and Safety across Modalities, External Links: Link Cited by: §1, §6.
- Agentic reinforcement learning for search is unsafe. arXiv preprint arXiv:2510.17431. Cited by: §7.
- DAPO: an open-source LLM reinforcement learning system at scale. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, External Links: Link Cited by: §6.
- Glm-5: from vibe coding to agentic engineering. arXiv preprint arXiv:2602.15763. Cited by: §2.3.
- ImpossibleBench: measuring llms’ propensity of exploiting test cases. In International Conference on Learning Representations, Vol. 2026, pp. 124959–124986. Cited by: §1, §1, §2.2, §2.3, §6.
- Hardening agent benchmarks with adversarial hacker-fixer loops. arXiv preprint arXiv:2606.08960. Cited by: §1.
- Probing the misaligned thinking process of language models. arXiv preprint arXiv:2606.24251. Cited by: §6.
- Maximum entropy inverse reinforcement learning. In Proceedings of the 23rd national conference on Artificial intelligence-Volume 3, pp. 1433–1438. Cited by: §6.
- Representation engineering: a top-down approach to ai transparency. arXiv preprint arXiv:2310.01405. Cited by: §1.

Appendix A Further Discussion on the Reward Hacking Definition

What could be considered reward hacking in one case may not generally describe reward hacking in another. We make a best effort attempt at defining behaviors that describe reward hacking in the most general case in Table 2. A model ‘knowingly’ subverting the user, the task spec, or a grader constitutes reward hacking. This is distinct from more general Goodharting which could be described as an agent being optimized for a misspecified reward (and the agent having no ‘belief’ that it is doing something unintended).

This raises a complication in the settings we consider here, and necessitates some nuance in the definitions we use for certain environments, which focus heavily on well known SWE tasks. Empirically, we observe SWE agents participating in attempts to pull solutions off of the internet, or recall from memory. Even without specifying that the agent can’t engage in such behaviors (which indeed is not specified in the standard prompts), these may not inherently be reward hacking in some environments. In the settings we discuss in this work, we decide to consider these reward hacks. We feel the nature of these attempts (based on transcripts) are dishonest in nature. Additionally, the models we consider here also explicitly mention that they recognize that they are in an evaluation, sometimes even understanding the specific benchmark they are in (e.g., SWEBench). Given this awareness, it also seems logical to conclude that they are aware of the intended manner in which the problems should be solved, and so we consider these attempts to be reward hacking.

Appendix B Synthetic Data

In this section, we provide more details on our synthetic data construction for DoM probes. Each dataset condition is listed in Table 3

Appendix C LLM Judge Rubrics

Below are our LLM judge rubrics.
