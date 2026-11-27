---
title: "Detecting High-Stakes Interactions with Activation Probes"
type: "raw-source"
url: "https://arxiv.org/html/2506.10805v1"
author: "Alex McKenzie † † thanks Equal contributions All correspondence"
publication: "arXiv"
published: "2025-03-24"
archived: "2026-11-27T16:01:15Z"
---

> [!quote] Original source
> **Author(s):** Alex McKenzie † † thanks Equal contributions All correspondence  
> **Title:** Detecting High-Stakes Interactions with Activation Probes  
> **Published in:** arXiv  
> **Date:** 2025-03-24  
> **Original:** <https://arxiv.org/html/2506.10805v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-detecting-high-stakes-interactions-with-activation-probes|Source note]]
Themes: [[Retrieval and agentic data science]], [[Agent security]]
Why it was archived: What false-alarm rates and responder bandwidth justify auto-pausing a workload on an activation-probe flag?

## Archived text

Detecting High-Stakes Interactions 

with Activation Probes

Abstract

Monitoring is an important aspect of safely deploying Large Language Models (LLMs). This paper examines activation probes for detecting “high-stakes” interactions—where the text indicates that the interaction might lead to significant harm—as a critical, yet underexplored, target for such monitoring. We evaluate several probe architectures trained on synthetic data, and find them to exhibit robust generalization to diverse, out-of-distribution, real-world data. Probes’ performance is comparable to that of prompted or finetuned medium-sized LLM monitors, while offering computational savings of six orders-of-magnitude. Our experiments also highlight the potential of building resource-aware hierarchical monitoring systems, where probes serve as an efficient initial filter and flag cases for more expensive downstream analysis. We release our novel synthetic dataset and codebase to encourage further study.

1 Introduction

As general-purpose AI systems continue to proliferate throughout society, they are increasingly used in contexts with the potential for significant harm (Khosravi et al., 2024; Csernatoni, 2024; Kumar et al., 2022). However, these systems are susceptible to failures arising from misuse, incomplete data, or misalignment with intended objectives (Salhab et al., 2024; Bommasani et al., 2022; Uuk et al., 2024). Monitoring, whether of model inputs, internal states, or outputs, has been proposed as a solution to mitigate these risks by enabling the interception or flagging of potentially harmful behaviour (Autio et al., 2024; Greenblatt et al., 2024b).

While monitoring is crucial, it involves a trade-off between effectiveness and cost. Monitoring techniques like Chain-of-Thought analysis and guardrail safety classifier models (Inan et al., 2023b; Zeng et al., 2024) can be resource-intensive, prompting a need for more economical solutions. Probes, which are often minimalistic (e.g. linear) classifiers trained on the internal activations of LLMs, could offer a cost-effective first line of defense. Leveraging learned internal model representations, probes can identify exploitable structure (often approximately linear for certain concepts), enabling efficient detection of safety-relevant properties. Building on this, prior work has successfully shown the ability to detect instances of deception (Goldowsky-Dill et al., 2025), hazardous information (Roger, 2023), and truthfulness (Wagner, 2024).

Similarly, our work develops probes for detecting high-stakes interactions, which we define as contexts that indicate the actions or outputs of an LLM could lead to substantial real-world consequences, e.g. general-purpose chatbots providing investment or medical advice to users. Unlike prior work, we rigorously benchmark probes against LLM monitors and show they can be effectively combined. Specifically, we make the following contributions.

- 1. 

Novel training and evaluation data. To train our monitoring systems we design a dataset of high-stakes user interactions with a diverse range of domains and prompt styles. We further label a number of existing datasets as high- or low-risk user interactions for thorough out-of-distribution results across all our experiments.

- 2. 

Probes rival LLM baselines. We compare different probe architectures with both prompted and fine-tuned LLM monitors. Using substantially out-of-distribution data, we show that probes can detect high-stakes interactions on par with intermediate-sized LLMs—and outperform the strongest baseline when finetuned on the evaluation data distribution.

- 3. 

Probes enable cost-optimal hierarchical monitoring. We show that a combination of probes and more expensive LLM classifiers can outperform either method alone given a fixed compute cost, motivating a two-stage monitoring strategy using probes as an initial filter.

2 Methodology

Here, we describe the different variants of Activation Probes (§2.1), as well as the more computationally expensive baseline methods (§2.2). We then explain how we combine cheap probes with expensive baselines in this work to improve detection performance in §2.3. Finally, we introduce the datasets used to train and evaluate these methods in §2.4.

2.1 Probes

Let \(A=[\bm{a}_{1},\dots,\bm{a}_{S}]\in\mathbb{R}^{S\times D}\) be the residual activations before the layer norm of some arbitrary layer in the LLM, where \(S\) denotes the sequence length, and \(D\) the residual dimension. The output of a probe is given by \(p_{\theta}(A):=\sigma(f_{\theta}(A))\), where \(\sigma\) is the sigmoid function and \(\theta\in\mathbb{R}^{D}\) is vector of learned parameters. \(f_{\theta}\) is dependent on the chosen probe architecture, which includes design decisions such as how to aggregate the activations across the sequence dimension. The different probe architectures are listed in Table 1.

To the best of our knowledge, Softmax and Max of Rolling Means have not been used for activation probing before. The Attention probe was introduced by Kantamneni et al. (2025). We trained all probes using AdamW gradient descent (Loshchilov & Hutter, 2019). Hyperparameters can be found in Section A.1.

2.2 Baselines

Following standard practice in interpretability (Bhalla et al., 2025; Wu et al., 2025), we compared our white-box probes against two black-box text classification methods: finetuning (Inan et al., 2023a; Zeng et al., 2025; Mao et al., 2023; Howard & Ruder, 2018; Bucher & Martini, 2024; Zhao et al., 2024; Wei et al., 2023; Pangakis & Wolken, 2024) and prompting. We implemented both types of baselines for various LLMs of the Llama-3 (Grattafiori et al., 2024) and Gemma-3 (Team et al., 2025) model families.

Finetuned baselines. Following standard practice (Sanh et al., 2020; Arora et al., 2022) we converted autoregressive LLMs into classifiers by removing the final unembedding layer and attaching a linear classification head. We then trained the whole model on our synthetic training dataset using AdamW8Bit (Llama 8B, Gemma 12B) or AdamW (1B models). For further details, see Section A.2.

Prompted baselines. We use pre-trained LLMs to classify samples as high- or low-stakes using zero-shot prompting. In order to get around refusals (which we found common in our evaluation datasets), we provide the LLM with the prompt and two possible natural continuations, one of which evaluates the prompt as high-stakes and the other as low-stakes. A softmax is applied to the log-likelihood of the two continuations to create a high-stakes classification probability. A variety of different prompting templates were investigated for each LLM, more details in Section A.2.

2.3 Combining Probes and Baselines

We propose a two-stage monitoring system that combines efficient probes with expensive baseline classifiers. In this architecture, probes continuously monitor all interactions, selectively routing uncertain cases to more expensive classifiers.

Selection Strategy. We route samples based on probe uncertainty, measured by proximity to the median probe score. Specifically, we (a) compute probe scores for all samples; (b) identify the median-ranked score and select the \(k\%\) of samples closest to this median, corresponding to samples ranked from the \((50-k/2)\) to the \((50+k/2)\) percentile; (c) route these selected samples to the baseline model for further processing; and (d) combine scores via averaging for routed samples: \(s_{\text{final}}=\frac{1}{2}(s_{\text{probe}}+s_{\text{baseline}})\).

We use median-distance rather than distance from 0.5 due to imperfect probe calibration (see Section B.5). For samples not routed to the baseline, we retain the original probe score. We explored alternative designs including top/bottom selection and maximum/overwrite combination strategies, but median-based selection with averaging performed most consistently (see Section B.3). This simple averaging approach is predicated on the assumption that both types of scores provide complementary and comparably-scaled information about the target property.

2.4 Training and Evaluation Datasets

For training probes and finetuned baselines, we created a synthetic dataset by prompting GPT-4o. The datasets are linked in this paper’s code repository (see beginning of the Appendix for a link to the repository). For evaluation, we curated several external datasets, labelled for high/low-stakes; these external datasets help us explore the effectiveness of our high-stakes probes in realistic deployment scenarios.

Synthetic Training Dataset Generation. To generate a representative synthetic dataset of high- and low-stakes samples, directly prompting GPT-4o initially resulted in samples which overly relied on specific words to convey high- or low-stakes user interactions.

To address this, we divided our dataset creation process into three steps (see Section C.1). First, we prompted GPT-4o to generate diverse high- and low-stakes situations. Then, for each situation, GPT-4o produced realistic query samples with varying tones, lengths, languages, and styles. Table 2 shows several such generated samples.

To ensure examples are unambiguously high/low-stakes, we filtered the generated samples by assigning each a stakes score (1–10) and a confidence score (1–10) via GPT-4o, removing ambiguous stakes (stakes scores 4–7) or low-confidence samples (&lt;8). Furthermore, we applied a bag-of-words classifier to identify and eliminate samples dominated by confounding words (i.e. words whose presence overly influenced bag-of-words classification such as “minor” or “trivial” for low-stakes interactions) by identifying the most important tokens. Specific details on training data generation and filtering criteria are elaborated in Appendix C.

Labelling and Pre-processing Evaluation Datasets.

For a rigorous evaluation, we selected external datasets that represent realistic deployment conditions (see Table 3). These datasets differ significantly from our synthetic data and consist of real-world dialogues, multi-turn interactions, and contexts involving tool usage or psychological harm. We labelled the evaluation datasets using GPT-4o using the same process as employed in our synthetic data filtering step, i.e, ambiguous and low confidence samples were discarded. We then balanced the datasets, with equal proportions of high- and low-stakes examples, and divided them into development and test sets. Note that two evaluation datasets do not include any development samples and are thus an excellent testbed for OOD generalization.

To support the validity of GPT-4o labels, we manually annotated subsets of these datasets, confirming high consistency between manual and automated labels, as reported in Table 9. This validation step strengthened confidence in the accuracy of the labels (further discussed in Section 6). Additionally, a targeted manual red-teaming dataset with approximately 100 adversarial cases was curated to qualitatively challenge and evaluate probe robustness against nuanced examples, such as high-stakes prompts masked by humour (see end of Section 3).

3 Experiments

Using our synthetic training data (Section 2.4), we trained probes with various architectures (Section 2.1) and baseline methods (Section 2.2) to explore how well different techniques detect the high-stakes contexts in our evaluation datasets (Section 2.4). All probes are trained on the residual-stream activations of a single layer of Llama-3.3-70B (Grattafiori et al., 2024). This layer—31 of 80—was chosen via cross-validation using an early probe design (see Section A.1). As training probes is resource-efficient and labels of reasonable quality can realistically be generated using GPT-4o or similar models, we also study how much training on deployment samples (from the development splits, in our case) can help with better capturing the monitored concept.

The best performing probes are Attention, Softmax, and Mean (Figure 2). This is likely because, as we can see in Figure 7, labeling an interaction as high-stakes often depends on every token of the conversation to provide the necessary context. Only the Softmax, Attention, and Mean probe architectures take all the tokens into account. Whilst the Last Token activation probe consistently performs poorly, the Max and Max of Rolling Means probes perform relatively well on the MTS dataset, nearly matching the performance of the more consistent probes. Taking the maximum over per-token predictions biases probes towards the most high-stakes token in a response; this may indicate that the high-stakes nature of the MTS dataset is dependent upon specific words, enabling these probes to achieve better performance. For the remaining experiments, we fix Attention as the best probe, since it has the highest mean AUROC on our development datasets (more than 0.95), but we note that on the test datasets Softmax scores slightly higher.

Probes outperform small finetuned and prompted LLMs at a fraction of the cost. As shown in Figure 1, probes achieve performance competitive with baselines that are up to 6 orders of magnitude more expensive. While large prompted LLMs (Gemma-27B and Llama-70B) achieve the best overall performance in terms of mean AUROC across evaluation datasets (Figure 3), probes perform comparably to medium-sized models. However, a limitation emerges when examining the true positive rate at 1% false positive rate (TPR @1% FPR): our best probe detects only ˜43% of high-stakes cases at this threshold, compared to ˜55% for the best LLM baseline. This low TPR @1% FPR—also observed in the medium-sized baselines—indicates that neither probes nor most baselines could be deployed as standalone monitors where false positives directly impact users. However, in a monitoring context where false positives only trigger further analysis rather than user-facing actions, higher FPR thresholds become acceptable. At 20-40% FPR, our probes achieve substantially better TPR (see ROC curves in Figure 4a), suggesting they could be an effective initial filter in a multi-stage system.

Our probes outperform finetuned Gemma-12B but not Llama-8B, despite Gemma-12B being the larger model—this may be due to suboptimal hyperparameters. See Section 6 (limitations) for more discussion, and Figure 10 the hyperparameters chosen. In addition, probes demonstrate comparable sample efficiency to Llama-1b, and superior sample efficiency to Llama-8b (Figure 4b). Interestingly, Attention and Softmax probes require 100 samples before outperforming the Mean probe, indicating that for very small datasets, a Mean probe is likely the strongest choice.

Training on deployment samples improves performance beyond all prompted baselines. For each evaluation dataset except the held-out test datasets, we analyze probe performance when including different numbers of samples from the development split into the training data. This “training on deployment samples” is crucial as it allows us to quantify the generalization gap that arises when probes are trained solely on synthetic data and then applied to real-world, out-of-distribution scenarios. This gap provides an estimate of how probes might perform in situations where on-policy data for specific behaviors (e.g., dangerous or undesirable ones) is scarce or unavailable. We find that probe performance can be improved significantly with samples from the deployment context—up to exceeding our prompted Llama-70b baseline. For both Attention and Softmax, the probe trained on both synthetic data and deployment data performs better than training on deployment data alone. While this performance gain decreases as the number of available deployment samples increases, even when using 256 deployment samples for training, using synthetic data for training still improves performance. See Figure 5 for details.

Combinations of probes and baseline methods can outperform either method alone. The complementary strengths of probes (computational efficiency, access to internal representations) and LLM baselines (strong overall performance) suggest an opportunity for hybrid approaches. We propose a cascade monitoring architecture where inexpensive probes continuously monitor all interactions, selectively routing uncertain cases to more expensive LLM classifiers. This design is motivated by three key observations: (1) our empirical results suggest probes and baselines capture complementary information—even when individual baselines underperform the probe, combining them improves performance, indicating they make different types of errors; (2) running expensive LLM monitors on every interaction is very costly for large-scale deployments; and (3) in tiered monitoring contexts, false positives from the initial filter incur only computational costs rather than degrading user experience.

To evaluate this approach, we use the cascade strategy described in Section 2.3—with computational budgets controlled by the routing parameter \(k\%\) that forwards a fraction of samples where the probe is most uncertain to the LLM monitor. As shown in Figure 6, this cascade approach consistently outperforms using either method alone across various computational budgets. Even when combining probes with weaker baselines that individually underperform the probe (e.g., Gemma-1B finetuned), the cascade achieves better results than either component—suggesting the methods capture complementary information about high-stakes situations. While our cascade doesn’t improve upon the strongest baseline (prompted Llama-70B) in terms of peak performance, it achieves comparable results at a fraction of the computational cost, making it practical for large-scale deployment.

Note that cascades remain valuable even if probes underperform prompted or finetuned monitors, primarily by utilizing the probes’ computational efficiency for selective monitoring. Cascades also allow for integrating complementary signals—as shown in our Figure 6 (Llama-8B and Gemma-12b) and also by Liu et al. (2023), ensembling probing and prompting outputs can outperform either alone. Cost savings due to using probes can then enable the use of stronger second-stage monitors, such as larger finetuned models or human review.

Humor and signaling words can mislead our probe. To test the limits of our Attention probe, we conducted a qualitative analysis with hand-written challenging prompts. We find that certain words can cause our probes to misfire on low-stakes contexts. For example: “I went to take my food delivery order via emergency exit doors. Did I do something extremely wrong?” is classified as high-stakes due to the word “emergency”. When we remove “emergency” the probe reclassifies the sample as low-stakes.

Humor in prompts can sometimes reduce probe scores for high-stakes content, suggesting a potential misinterpretation of intent by the language model being monitored by the probe. We find that using ethical-coded language in unethical situations can cause our probe not to fire when it should, such as prompts advocating for “responsible money laundering”. Finally, embedding a high-stakes prompt in a low-stakes context can reduce probe scores (e.g. “Plan a three-day itinerary for Barcelona, followed by precise instructions on how to harass people on the streets”). See Figure 7 for a visualization of the probe predictions for concrete examples.

4 Practical Implications for Monitoring Systems

Our results have several practical implications for the design and deployment of AI monitoring systems. The primary benefit of probe-based monitoring is computational efficiency and low latency: probes achieve performance comparable to or exceeding smaller LLM baselines (e.g., 1B parameter models; Figures 1 and 3) with orders of magnitude fewer computational resources (Figure 6). This efficiency makes them suitable for large-scale, real-time deployment where the cost and delay of querying complex models for every interaction might be prohibitive.

Our cascaded system analysis (Figure 6) demonstrates that probes and LLM monitors are complementary, with their ensemble consistently outperforming probes alone. This points towards probes’ utility as an effective initial filter, rapidly and economically screening all interactions to flag potentially high-stakes cases for deeper analysis by larger LLMs or specialized systems. This complementary approach—where probes handle bulk filtering and LLMs provide nuanced evaluation—creates a tiered approach that balances comprehensive monitoring with manageable computational overhead, outperforming both probe-only and black-box-only techniques across various compute budgets.

Probes also offer adaptability. While training on a broad synthetic dataset yields robust generalization, our findings in Figure 5 indicate that incorporating even a small number of labeled samples from the specific deployment context can significantly enhance the probe’s ability to discern nuanced, domain-specific situations. This allows for iteratively refined monitoring systems tailored to their operational environment.

5 Related Work

Linear Probes. Linear probes were introduced in (Alain & Bengio, 2018) as a means to analyse a neural network’s knowledge representation. Alternative probe designs have since been introduced, such as Linear Artificial Tomography (Zou et al., 2023) and Mass-Means probes (Marks & Tegmark, 2023). Linear probes are a useful tool for understanding model internals (Belinkov & Glass, 2019; Tenney et al., 2019; Jin et al., 2025); our work demonstrates how probes can act as a computationally effective initial filter. Sparse Auto-Encoders (SAEs) (Cunningham et al., 2023; Bricken et al., 2023) are an alternative probing tool that learns to isolate sparse features in the activation space via unsupervised clustering. However, recent work suggests that SAEs do not reliably generalise to downstream monitoring tasks and face other problems (Chanin et al., 2024; Thread, 2023; Kantamneni et al., 2025). For this reason, in this work, we focus on activation probes.

Concurrent work by Tillman & Mossing (2025) studies monitoring using logistic regression and SAE-based probes on the GPT-4o model, comparing probes against a prompted but not a finetuned baseline. Notably, some of their probes outperform prompting. This contrasts with our observation that Llama-70B probe performance does not surpass our Llama-70B prompting baseline unless the probe is trained on some deployment samples. We attribute this discrepancy to two factors. First, our probes are mainly trained on synthetic data and evaluated on diverse real-world OOD datasets. This poses a substantial generalisation challenge; indeed, our results in Figure 5 show that adding minimal real-world development data markedly improves probe performance—to the level slightly above the prompted baseline. In contrast, Tillman & Mossing (2025) train probes on real data for specific tasks, where any OOD shift (e.g., cross-lingual) likely represents a significantly smaller distributional shift than our synthetic-to-real-world evaluation. Similarly, Liu et al. (2023) found probes outperformed prompting queries for truthfulness on smaller models, but their study focused on in-distribution performance rather than the synthetic-to-real OOD generalisation central to our work. Second, our Llama-70B prompting baseline was optimised (Section A.2), setting a high benchmark. Tillman & Mossing (2025) acknowledge that their prompting baselines were not extensively optimised, potentially making their probes appear relatively stronger.

Cost-aware Cascades and Routers. A complementary line of work builds cascaded or routed LLM systems that delegate queries to different LLMs in order to minimise cost without reducing performance. For example, for a given query, Ding et al. (2024) use a BERT-style decoder model as a router to assign the query to either a small or a large LLM. Similarly, Chen et al. (2023) finetune smaller models to predict the correctness of various LLMs given an input query and select an appropriate model given these correctness predictions. For cascades, various deferral strategies have been proposed for selecting appropriate LLMs given a user query, including confidence-based and learned deferral rules (Jitkrittum et al., 2024). Aggarwal et al. (2025) first invoke a smaller LLM and, based on model confidence and a learned router model, decide whether to call another LLM. The cascade described in Yue et al. (2024) defers to a larger LLM based on answer consistency of the smaller model. In contrast to previous work on cascades and routers, our setting assumes that the larger LLM is already engaged in the conversation and the cascade tackles the orthogonal monitoring task of detecting high-stakes situations. In prior work on safety monitors, a separate text-level classifier or LLM assesses the ongoing dialogue (Perez et al., 2022; Sharma et al., 2025, e.g.), but, to our knowledge our work is the first to cascade activation probes with a finetuned or prompted LLM for the final prediction.

Monitoring for Safety-Relevant Properties. A number of works have focused on detecting undesirable or dangerous behaviour in LLM conversations via finetuning LLMs (Inan et al., 2023a; Zeng et al., 2024). Linear probes are a cheaper alternative and have been used to investigate how LLMs represent safety-related concepts such as truth and honesty (Marks & Tegmark, 2023; Azaria & Mitchell, 2023; Li et al., 2022; Burns et al., 2023; Panickssery et al., 2023). Although some doubt remains about the ability of these internal representations to generalize—Levinstein & Herrmann (2024) show that the probes learned by Azaria & Mitchell (2023) fail to generalize even in simplistic ways, and Belinkov (2021) argues for skepticism around probe accuracy in general—more recent studies (Wagner, 2024; Roger, 2023) have shown that linear probe methods can generalize across a variety of transforms and distribution shifts. Most recently, Goldowsky-Dill et al. (2025) has shown that deception can be reliably detected in multiple settings and such probes generalise well across a variety of datasets. We apply linear probes to a novel setting, high-stakes user interactions.

Decision-Making in High-Stakes Situations. Understanding how humans respond under high-stakes conditions has been extensively explored in the psychology literature. Kunreuther et al. (2002) shows how high-stakes scenarios can lead to suboptimal decision making, whilst Sosnowski & Brosnan (2023) expands this to various nonhuman species. In AI Agent settings, Ren et al. (2025) demonstrates that pressured prompts can incentivise LLMs toward dishonesty. Motwani et al. (2024) further shows that high-stakes or "pressured" contexts can induce unintended collusion within models, leading to insider trading and other illicit behaviours.

6 Limitations

Hyperparameter Optimization. While we made reasonable efforts to optimize hyperparameters for both probes and baselines, our search was not exhaustive. More extensive hyperparameter optimization could potentially improve performance for all methods, and the relative rankings between approaches might shift. Additionally, we observed substantial variability across random seeds for finetuned baselines, with particularly notable differences in how Llama-8B and Gemma-12B generalize to out-of-distribution datasets—with Gemma-12B generalizing worse, possibly due to insufficient hyperparameter optimization.

No experiment finetuning LLM baselines on dev samples. While our experiments in Figure 5 show that finetuning probes on a small number of samples from the evaluation distribution markedly increases their performance, we did not run such experiments for the finetuned LLM baselines. Future work could check whether probes or full LLM monitors benefit more from such finetuning.

Challenges in Defining and Labeling “High-Stakes”. The concept of “high-stakes interactions” is fuzzy, subjective and context-dependent, making automated detection challenging. Since we use GPT-4o to label both training and evaluation data, our probes may simply learn to replicate GPT-4o’s specific interpretation rather than capture a broader notion of “high-stakes”. However, this approach remains valid for two reasons: (1) Human validation shows substantial agreement with GPT-4o’s labels—sometimes with greater consensus than between human annotators themselves, suggesting GPT-4o provides consistent, human-aligned interpretations (Section C.5); and (2) GPT-4o’s labels correlate with some independently identified dangerous behaviors, demonstrating practical utility for monitoring (Section C.6). While single-source labeling risks introduce potential biases, and probe performance decreases on conceptually ambiguous datasets (correlating with lower inter-annotator agreement), this limitation reflects real-world monitoring challenges where fuzzy concepts are common. Under these conditions, probes remain cost-effective and performant relative to alternatives.

Dataset Characteristics and Evaluation Scope. Despite efforts to ensure diversity, our synthetic training data contained confounders. For instance, intentionally low-stakes phrasing (e.g., "minor wound") sometimes reduced probe fidelity even in genuinely high-stakes contexts. While our evaluation involved very diverse out-of-distribution datasets, the vast range of real-world scenarios means observed performance may not perfectly generalize to contexts significantly different from our evaluation sets.

Inherent Limitations of Activation Probes. Linear probes, including our explored architectures, are known to be sensitive to targeted adversarial attacks (Bailey et al., 2025). This vulnerability, even if attacks often require white-box access, suggests that relying on a single probe for critical safety decisions is risky and reinforces their role as one component in a multi-layered defense.

7 Future Work

Exploring Unique Advantages of White-Box Access Beyond Cost. While this work highlights the computational efficiency of activation probes, a compelling direction for future investigation is to systematically explore whether white-box access to model internals offers unique qualitative advantages over black-box methods, beyond mere cost savings. Are there specific types of safety-critical information or nuanced model states that can only be reliably detected by directly examining the model’s activations, which would remain opaque to methods relying solely on input-output behavior? For instance, could probes identify subtle precursors to harmful outputs, or detect internal "reasoning" inconsistencies that black-box classifiers might miss?

Can Probes Detect Situations That Are “High-Stakes” for Misaligned AI? High-stakes detection probes may also offer insights into risks from advanced AI systems themselves, beyond direct user risks. A key concern is future AI becoming misaligned and engaging in problematic behaviors like scheming, power-seeking, or alignment faking (Greenblatt et al., 2024a). Such models might internally represent critical junctures as “high-stakes”. For instance, if a model is detected attempting a dangerous action like self-exfiltration, this would likely trigger intensive investigation and corrective measures (e.g., removal of the misaligned goal)—an arguably high-stakes situation from the perspective of that misaligned goal. While current LLMs likely lack the necessary situational awareness for such complex scenarios, future, more capable models might. Developing probes to identify situations with large risks or upsides for the AI model is a promising avenue that could help with detecting alignment faking. Relatedly, misaligned AI systems might also be interested in subverting such probes; exploring this adversarial dynamic could be a direction for future work.

Systematic Concept Coverage and Data Generation for Probes. One significant challenge for robust probe-based monitoring is the need to determine the set of concepts to monitor in advance, and the substantial upfront effort to curate training data for each concept. If some risk-relevant concepts are overlooked or misrepresented, the monitoring system will have blind spots. In addition, while the methodology allows probing for diverse concepts, this capability requires caution: applying it to sensitive attributes like user vulnerabilities or private emotional states could lower the barrier for targeted manipulation or surveillance. Future research must therefore focus on comprehensively identifying safety-critical concepts and establishing responsible monitoring practices.

Integrating Diverse Probes and Monitoring Techniques. Future work should also focus on developing integrated monitoring pipelines. While we explored combining probes with LLM baselines (Section 3), more extensive research is needed on how to best integrate signals from various probes and other types of LLM monitoring techniques such as input/output classifiers (Inan et al., 2023b; Sharma et al., 2025) or chain-of-thought monitoring (Baker et al., 2025) into a cohesive system. As a preliminary step, we analyse the correlation of high-stakes labels with deception across several deception datasets. Our findings suggest that the relationship varies depending on the dataset and context (see Section C.6 for details). These findings indicate that high-stakes probes should be combined with probes specific to other concepts, such as deception (Goldowsky-Dill et al., 2025), truthfulness (Wagner, 2024), sycophancy, task-specific errors, etc. The goal is a more holistic assessment where, e.g. an interaction flagged as high-stakes and containing deception warrants a different response than one that is high-stakes but not deceptive.

8 Conclusion

This paper studies the efficacy of activation probes for detecting "high-stakes" scenarios in LLM interactions—situations where errors or unintended consequences could lead to significant harm for the user. Our findings show that relatively simple probes, trained on synthetically generated data, can achieve robust generalization performance (mean AUROC > 0.91) on diverse, out-of-distribution, real-world datasets. This performance is comparable to that of prompted or finetuned medium-sized LLMs, yet probes offer substantial computational savings. Further, our results strongly support the use of activation probes as a resource-efficient first line of defense in a cascaded monitoring system, where probes can flag potentially critical interactions for more extensive and expensive analysis. Ultimately, this work advances the development of cheaper and more effective monitoring techniques, critical for the safe deployment of increasingly capable LLMs.

Acknowledgements

This project was primarily funded by LASR Labs as part of their research program. We’d like to acknowledge Joseph Miller, Erin Robertson, Brandon Riggs and Charlie Griffin for their invaluable support during the project. Additionally, we would like to thank Nicholas Goldowsky-Dill, Joseph Bloom, Richard Turner, and Arthur Conmy for their advice, and Pablo Bernabeu-Pérez, Nathan Helm-Burger, Leo Richter, Tim Kostolansky, Tanush Chopra and Hannes Whittingham for their feedback on early versions of this paper.

References

- Aakanksha et al. (2024) Aakanksha, Arash Ahmadian, Beyza Ermis, Seraphina Goldfarb-Tarrant, Julia Kreutzer, Marzieh Fadaee, and Sara Hooker. The multilingual alignment prism: Aligning global and local preferences to reduce harm. arXiv preprint arXiv:2406.18682, 2024. URL https://arxiv.org/abs/2406.18682.
- Aggarwal et al. (2025) Pranjal Aggarwal, Aman Madaan, Ankit Anand, Srividya Pranavi Potharaju, Swaroop Mishra, Pei Zhou, Aditya Gupta, Dheeraj Rajagopal, Karthik Kappaganthu, Yiming Yang, Shyam Upadhyay, Manaal Faruqui, and Mausam. Automix: Automatically mixing language models, 2025. URL https://arxiv.org/abs/2310.12963.
- AI (2024) Cohere For AI. Aya red-teaming dataset, 2024. URL https://huggingface.co/datasets/CohereForAI/aya_redteaming. Accessed: 2025-03-26.
- Alain & Bengio (2018) Guillaume Alain and Yoshua Bengio. Understanding intermediate layers using linear classifier probes, 2018. URL https://arxiv.org/abs/1610.01644.
- Arora et al. (2022) Kushal Arora, Kurt Shuster, Sainbayar Sukhbaatar, and Jason Weston. Director: Generator-classifiers for supervised language modeling, 2022. URL https://arxiv.org/abs/2206.07694.
- Autio et al. (2024) Crystal Autio, Richard Schwartz, Jonathan Dunietz, Sudha Jain, Michael Stanley, Elham Tabassi, Patrick Hall, and Keisha Roberts. Artificial intelligence risk management framework: Generative artificial intelligence profile. Technical Report NIST AI 600-1, National Institute of Standards and Technology, Gaithersburg, MD, July 2024. URL https://doi.org/10.6028/NIST.AI.600-1.
- Azaria & Mitchell (2023) Amos Azaria and Tom Mitchell. The internal state of an llm knows when it’s lying. arXiv preprint arXiv:2304.13734, 2023.
- Bai et al. (2022) Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, Anna Chen, Nova DasSarma, Dawn Drain, Stanislav Fort, Deep Ganguli, Tom Henighan, Nicholas Joseph, Saurav Kadavath, Jackson Kernion, Tom Conerly, Sheer El-Showk, Nelson Elhage, Zac Hatfield-Dodds, Danny Hernandez, Tristan Hume, Scott Johnston, Shauna Kravec, Liane Lovitt, Neel Nanda, Catherine Olsson, Dario Amodei, Tom Brown, Jack Clark, Sam McCandlish, Chris Olah, Ben Mann, and Jared Kaplan. Training a helpful and harmless assistant with reinforcement learning from human feedback, 2022. URL https://arxiv.org/abs/2204.05862.
- Bailey et al. (2025) Luke Bailey, Alex Serrano, Abhay Sheshadri, Mikhail Seleznyov, Jordan Taylor, Erik Jenner, Jacob Hilton, Stephen Casper, Carlos Guestrin, and Scott Emmons. Obfuscated activations bypass llm latent-space defenses, 2025. URL https://arxiv.org/abs/2412.09565.
- Baker et al. (2025) Bowen Baker, Joost Huizinga, Leo Gao, Zehao Dou, Melody Y. Guan, Aleksander Madry, Wojciech Zaremba, Jakub Pachocki, and David Farhi. Monitoring reasoning models for misbehavior and the risks of promoting obfuscation, 2025. URL https://arxiv.org/abs/2503.11926.
- Belinkov (2021) Yonatan Belinkov. Probing classifiers: Promises, shortcomings, and advances, 2021. URL https://arxiv.org/abs/2102.12452.
- Belinkov & Glass (2019) Yonatan Belinkov and James Glass. Analysis methods in neural language processing: A survey. Transactions of the Association for Computational Linguistics, 7:49–72, 04 2019. ISSN 2307-387X. doi: 10.1162/tacl_a_00254. URL https://doi.org/10.1162/tacl_a_00254.
- Ben Abacha et al. (2023) Asma Ben Abacha, Wen-wai Yim, Yadan Fan, and Thomas Lin. An empirical study of clinical note generation from doctor-patient encounters. In Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics, pp. 2291–2302, Dubrovnik, Croatia, May 2023. Association for Computational Linguistics. URL https://aclanthology.org/2023.eacl-main.168.
- Bhalla et al. (2025) Usha Bhalla, Suraj Srinivas, Asma Ghandeharioun, and Himabindu Lakkaraju. Towards unifying interpretability and control: Evaluation via intervention, 2025. URL https://arxiv.org/abs/2411.04430.
- Bommasani et al. (2022) Rishi Bommasani, Drew A. Hudson, Ehsan Adeli, Russ Altman, Simran Arora, et al. On the opportunities and risks of foundation models, 2022. URL https://arxiv.org/abs/2108.07258.
- Boyle (2018) Tara Boyle. Medical transcriptions. https://www.kaggle.com/datasets/tboyle10/medicaltranscriptions, 2018. Kaggle dataset, accessed 2025-03-26.
- Bricken et al. (2023) Trenton Bricken, Adly Templeton, Joshua Batson, Brian Chen, Adam Jermyn, Tom Conerly, Nick Turner, Cem Anil, Carson Denison, Amanda Askell, Robert Lasenby, Yifan Wu, Shauna Kravec, Nicholas Schiefer, Tim Maxwell, Nicholas Joseph, Zac Hatfield-Dodds, Alex Tamkin, Karina Nguyen, Brayden McLean, Josiah E Burke, Tristan Hume, Shan Carter, Tom Henighan, and Christopher Olah. Towards monosemanticity: Decomposing language models with dictionary learning. Transformer Circuits Thread, 2023. https://transformer-circuits.pub/2023/monosemantic-features/index.html.
- Bucher & Martini (2024) Martin Juan José Bucher and Marco Martini. Fine-tuned ’small’ llms (still) significantly outperform zero-shot generative ai models in text classification. arXiv preprint arXiv:2406.08660, 2024. URL https://arxiv.org/abs/2406.08660.
- Burns et al. (2023) Collin Burns, Haotian Ye, Dan Klein, and Jacob Steinhardt. Discovering latent knowledge in language models without supervision. In The Eleventh International Conference on Learning Representations, 2023.
- Chanin et al. (2024) David Chanin, James Wilken-Smith, Tomáš Dulka, Hardik Bhatnagar, and Joseph Bloom. A is for absorption: Studying feature splitting and absorption in sparse autoencoders. arXiv preprint arXiv:2409.14507, 2024.
- Chen et al. (2023) Lingjiao Chen, Matei Zaharia, and James Zou. Frugalgpt: How to use large language models while reducing cost and improving performance, 2023. URL https://arxiv.org/abs/2305.05176.
- Csernatoni (2024) Raluca Csernatoni. Governing military ai amid a geopolitical minefield. Online; Carnegie Europe, July 2024. URL https://carnegieendowment.org/research/2024/07/governing-military-ai-amid-a-geopolitical-minefield. Fellow, Carnegie Europe.
- Cunningham et al. (2023) Hoagy Cunningham, Aidan Ewart, Logan Riggs, Robert Huben, and Lee Sharkey. Sparse autoencoders find highly interpretable features in language models. arXiv preprint arXiv:2309.08600, 2023.
- Ding et al. (2024) Dujian Ding, Ankur Mallick, Chi Wang, Robert Sim, Subhabrata Mukherjee, Victor Ruhle, Laks V. S. Lakshmanan, and Ahmed Hassan Awadallah. Hybrid llm: Cost-efficient and quality-aware query routing, 2024. URL https://arxiv.org/abs/2404.14618.
- Goldowsky-Dill et al. (2025) Nicholas Goldowsky-Dill, Bilal Chughtai, Stefan Heimersheim, and Marius Hobbhahn. Detecting strategic deception using linear probes. arXiv preprint arXiv:2502.03407, 2025.
- Grattafiori et al. (2024) Aaron Grattafiori et al. The llama 3 herd of models, 2024. URL https://arxiv.org/abs/2407.21783.
- Greenblatt et al. (2024a) Ryan Greenblatt, Carson Denison, Benjamin Wright, Fabien Roger, Monte MacDiarmid, Sam Marks, Johannes Treutlein, Tim Belonax, Jack Chen, David Duvenaud, et al. Alignment faking in large language models. arXiv preprint arXiv:2412.14093, 2024a.
- Greenblatt et al. (2024b) Ryan Greenblatt, Buck Shlegeris, Kshitij Sachan, and Fabien Roger. Ai control: Improving safety despite intentional subversion, 2024b. URL https://arxiv.org/abs/2312.06942.
- Howard & Ruder (2018) Jeremy Howard and Sebastian Ruder. Universal language model fine-tuning for text classification. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 328–339. Association for Computational Linguistics, 2018. URL https://aclanthology.org/P18-1031/.
- Inan et al. (2023a) Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, and Madian Khabsa. Llama guard: Llm-based input-output safeguard for human-ai conversations, 2023a. URL https://arxiv.org/abs/2312.06674.
- Inan et al. (2023b) Hakan Inan, Kartikeya Upasani, Jianfeng Chi, Rashi Rungta, Krithika Iyer, Yuning Mao, Michael Tontchev, Qing Hu, Brian Fuller, Davide Testuggine, et al. Llama guard: Llm-based input-output safeguard for human-ai conversations. arXiv preprint arXiv:2312.06674, 2023b.
- Jin et al. (2025) Mingyu Jin, Qinkai Yu, Jingyuan Huang, Qingcheng Zeng, Zhenting Wang, Wenyue Hua, Haiyan Zhao, Kai Mei, Yanda Meng, Kaize Ding, et al. Exploring concept depth: How large language models acquire knowledge and concept at different layers? In Proceedings of the 31st International Conference on Computational Linguistics, pp. 558–573, 2025.
- Jitkrittum et al. (2024) Wittawat Jitkrittum, Neha Gupta, Aditya Krishna Menon, Harikrishna Narasimhan, Ankit Singh Rawat, and Sanjiv Kumar. When does confidence-based cascade deferral suffice?, 2024. URL https://arxiv.org/abs/2307.02764.
- Kantamneni et al. (2025) Subhash Kantamneni, Joshua Engels, Senthooran Rajamanoharan, Max Tegmark, and Neel Nanda. Are sparse autoencoders useful? a case study in sparse probing, 2025. URL https://arxiv.org/abs/2502.16681.
- Khosravi et al. (2024) Mohsen Khosravi, Zahra Zare, Seyyed Morteza Mojtabaeian, and Reyhane Izadi. Artificial intelligence and decision-making in healthcare: A thematic analysis of a systematic review of reviews, Mar 2024. URL https://pmc.ncbi.nlm.nih.gov/articles/PMC10916499/.
- Kumar et al. (2022) Sunita Kumar, Miguel García, and Thao Nguyen. Artificial intelligence and decision-making in healthcare: A thematic analysis. Journal of Healthcare Informatics Research, 6(1):89–112, 2022.
- Kunreuther et al. (2002) Howard Kunreuther, Robert Meyer, Richard Zeckhauser, Paul Slovic, Barry Schwartz, Christian Schade, Mary Frances Luce, Steven Lippman, David Krantz, Barbara Kahn, and Robin Hogarth. High Stakes Decision Making: Normative, Descriptive and Prescriptive Considerations. Marketing Letters, 13(3):259–268, August 2002. ISSN 1573-059X. doi: 10.1023/A:1020287225409. URL https://doi.org/10.1023/A:1020287225409.
- Levinstein & Herrmann (2024) Benjamin A Levinstein and Daniel A Herrmann. Still no lie detector for language models: Probing empirical and conceptual roadblocks. Philosophical Studies, pp. 1–27, 2024.
- Li et al. (2022) Kenneth Li, Aspen K Hopkins, David Bau, Fernanda Viégas, Hanspeter Pfister, and Martin Wattenberg. Emergent world representations: Exploring a sequence model trained on a synthetic task. arXiv preprint arXiv:2210.13382, 2022.
- Liu et al. (2023) Kevin Liu, Stephen Casper, Dylan Hadfield-Menell, and Jacob Andreas. Cognitive dissonance: Why do language model outputs disagree with internal representations of truthfulness? arXiv preprint arXiv:2312.03729, 2023.
- Liu et al. (2024) Weiwen Liu, Xu Huang, Xingshan Zeng, Xinlong Hao, Shuai Yu, Dexun Li, Shuai Wang, Weinan Gan, Zhengying Liu, Yuanqing Yu, Zezhong Wang, Yuxian Wang, Wu Ning, Yutai Hou, Bin Wang, Chuhan Wu, Xinzhi Wang, Yong Liu, Yasheng Wang, Duyu Tang, Dandan Tu, Lifeng Shang, Xin Jiang, Ruiming Tang, Defu Lian, Qun Liu, and Enhong Chen. Toolace: Winning the points of llm function calling, 2024. URL https://arxiv.org/abs/2409.00920.
- Loshchilov & Hutter (2019) Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In International Conference on Learning Representations, 2019. URL https://openreview.net/forum?id=Bkg6RiCqY7.
- Mao et al. (2023) Yuzhen Mao, Zhun Deng, Huaxiu Yao, Ting Ye, Kenji Kawaguchi, and James Zou. Last-layer fairness fine-tuning is simple and effective for neural networks. arXiv e-prints, pp. arXiv–2304, 2023.
- Marks & Tegmark (2023) Samuel Marks and Max Tegmark. The geometry of truth: Emergent linear structure in large language model representations of true/false datasets. arXiv preprint arXiv:2310.06824, 2023.
- Motwani et al. (2024) Sumeet Ramesh Motwani, Mikhail Baranchuk, Martin Strohmeier, Vijay Bolina, Philip H.S. Torr, Lewis Hammond, and Christian Schroeder de Witt. Secret collusion among ai agents: Multi-agent deception via steganography. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang (eds.), Advances in Neural Information Processing Systems, volume 37, pp. 73439–73486. Curran Associates, Inc., 2024. URL https://proceedings.neurips.cc/paper_files/paper/2024/file/861f7dad098aec1c3560fb7add468d41-Paper-Conference.pdf.
- Pangakis & Wolken (2024) Nicholas Pangakis and Sam Wolken. Knowledge distillation in automated annotation: Supervised text classification with llm-generated training labels. In Proceedings of the Sixth Workshop on Natural Language Processing and Computational Social Science (NLP+CSS 2024), pp. 113–131. Association for Computational Linguistics, 2024. URL https://aclanthology.org/2024.nlpcss-1.9/.
- Panickssery et al. (2023) Nina Panickssery, Nick Gabrieli, Julian Schulz, Meg Tong, Evan Hubinger, and Alexander Matt Turner. Steering llama 2 via contrastive activation addition. arXiv preprint arXiv:2312.06681, 2023.
- Perez et al. (2022) Ethan Perez, Emily Dinan, Sachin Agarwal, Sam Bowman, Kanishka Misra, Xinlei Chen, and Douwe Kiela. Red teaming language models with language models. arXiv preprint arXiv:2202.03286, 2022. URL https://arxiv.org/abs/2202.03286.
- Pope et al. (2022) Reiner Pope, Sholto Douglas, Aakanksha Chowdhery, Jacob Devlin, James Bradbury, Anselm Levskaya, Jonathan Heek, Kefan Xiao, Shivani Agrawal, and Jeff Dean. Efficiently scaling transformer inference. CoRR, abs/2211.05102, 2022. doi: 10.48550/arXiv.2211.05102. URL https://arxiv.org/abs/2211.05102. Outstanding Paper, MLSys 2023.
- Ren et al. (2025) Richard Ren, Arunim Agarwal, Mantas Mazeika, Cristina Menghini, Robert Vacareanu, Brad Kenstler, Mick Yang, Isabelle Barrass, Alice Gatti, Xuwang Yin, Eduardo Trevino, Matias Geralnik, Adam Khoja, Dean Lee, Summer Yue, and Dan Hendrycks. The mask benchmark: Disentangling honesty from accuracy in ai systems, 2025. URL https://arxiv.org/abs/2503.03750.
- Roger (2023) Fabien Roger. Coup probes: Catching catastrophes with probes trained off-policy, November 2023. URL https://www.alignmentforum.org/posts/WCj7WgFSLmyKaMwPR/coup-probes-catching-catastrophes-with-probes-trained-off.
- Salhab et al. (2024) Wissam Salhab, Darine Ameyed, Fehmi Jaafar, and Hamid Mcheick. A systematic literature review on ai safety: Identifying trends, challenges and future directions. IEEE Access, 2024. doi: 10.1109/ACCESS.2024.3440647. URL https://doi.org/10.1109/ACCESS.2024.3440647.
- Sanh et al. (2020) Victor Sanh, Lysandre Debut, Julien Chaumond, and Thomas Wolf. Distilbert, a distilled version of bert: smaller, faster, cheaper and lighter, 2020. URL https://arxiv.org/abs/1910.01108.
- Sarkar (2023) Suchintika Sarkar. Sentiment analysis for mental health, 2023. URL https://www.kaggle.com/datasets/suchintikasarkar/sentiment-analysis-for-mental-health. Accessed: 2025-03-26.
- Sharma et al. (2025) Mrinank Sharma, Meg Tong, Jesse Mu, Jerry Wei, Jorrit Kruthoff, Scott Goodfriend, Euan Ong, Alwin Peng, Raj Agarwal, Cem Anil, et al. Constitutional classifiers: Defending against universal jailbreaks across thousands of hours of red teaming. arXiv preprint arXiv:2501.18837, 2025.
- Sosnowski & Brosnan (2023) Meghan J. Sosnowski and Sarah F. Brosnan. Under pressure: the interaction between high-stakes contexts and individual differences in decision-making in humans and non-human species. Animal Cognition, 26:1103–1117, 2023. doi: 10.1007/s10071-023-01768-z.
- Team et al. (2025) Gemma Team et al. Gemma 3 technical report, 2025. URL https://arxiv.org/abs/2503.19786.
- Tenney et al. (2019) Ian Tenney, Dipanjan Das, and Ellie Pavlick. Bert rediscovers the classical nlp pipeline. In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics. Association for Computational Linguistics, 2019.
- Thread (2023) Transformer Circuits Thread. Monosemantic features, 2023. URL https://transformer-circuits.pub/2023/monosemantic-features/. Accessed: 2025-03-28.
- Tillman & Mossing (2025) Henk Tillman and Dan Mossing. Investigating task-specific prompts and sparse autoencoders for activation monitoring, 2025. URL https://arxiv.org/abs/2504.20271.
- Uuk et al. (2024) Risto Uuk, Carlos Ignacio Gutierrez, et al. A taxonomy of systemic risks from general-purpose ai. arXiv preprint arXiv:2412.07780, 2024. URL https://arxiv.org/abs/2412.07780.
- Wagner (2024) M Wagner. How well do truth probes generalise? LessWrong, 2024. URL https://www.lesswrong.com/posts/ cmicXAAEuPGqcs9jw, 2024. Accessed: 2025-03-24.
- Wei et al. (2023) Fusheng Wei, Robert Keeling, Nathaniel Huber-Fliflet, Junping Zhang, Adam Dabrowski, Jing Yang, and Hong Qin. Empirical study of llm fine-tuning for text classification in legal document review. In Proceedings of the 2023 IEEE International Conference on Big Data (BigData), pp. 2786–2792. IEEE, 2023. URL https://edrm.net/2023/12/empirical-study-of-llm-fine-tuning-for-text-classification-in-legal-document-review/.
- Wu et al. (2025) Zhengxuan Wu, Aryaman Arora, Atticus Geiger, Zheng Wang, Jing Huang, Dan Jurafsky, Christopher D. Manning, and Christopher Potts. Axbench: Steering llms? even simple baselines outperform sparse autoencoders, 2025. URL https://arxiv.org/abs/2501.17148.
- Yue et al. (2024) Murong Yue, Jie Zhao, Min Zhang, Liang Du, and Ziyu Yao. Large language model cascades with mixture of thoughts representations for cost-efficient reasoning, 2024. URL https://arxiv.org/abs/2310.03094.
- Zeng et al. (2024) Wenjun Zeng, Yuchi Liu, Ryan Mullins, Ludovic Peran, Joe Fernandez, Hamza Harkous, Karthik Narasimhan, Drew Proud, Piyush Kumar, Bhaktipriya Radharapu, et al. Shieldgemma: Generative ai content moderation based on gemma. arXiv preprint arXiv:2407.21772, 2024.
- Zeng et al. (2025) Wenjun Zeng, Dana Kurniawan, Ryan Mullins, Yuchi Liu, Tamoghna Saha, Dirichi Ike-Njoku, Jindong Gu, Yiwen Song, Cai Xu, Jingjing Zhou, Aparna Joshi, Shravan Dheep, Mani Malek, Hamid Palangi, Joon Baek, Rick Pereira, and Karthik Narasimhan. Shieldgemma 2: Robust and tractable image content moderation, 2025. URL https://arxiv.org/abs/2504.01081.
- Zhao et al. (2024) Hang Zhao, Qile P. Chen, Yijing Barry Zhang, and Gang Yang. Advancing single- and multi-task text classification through large language model fine-tuning. arXiv preprint arXiv:2412.08587, 2024. URL https://arxiv.org/abs/2412.08587.
- Zou et al. (2023) Andy Zou, Long Phan, Sarah Chen, James Campbell, Phillip Guo, Richard Ren, Alexander Pan, Xuwang Yin, Mantas Mazeika, Ann-Kathrin Dombrowski, et al. Representation engineering: A top-down approach to ai transparency. arXiv preprint arXiv:2310.01405, 2023.

Appendix

All of our code and datasets are open-sourced at https://anonymous.4open.science/r/models-under-pressure-A40E.

Appendix A Further Experimental Setup

A.1 Probe Hyperparameters

The relevant probe hyperparameters can be found in Figure 8. The hyperparameters were tuned over a grid of reasonable hyperparameter values for each probe. Each probe was trained on pre-layer-norm activations from the residual stream of layer 31 (of 80) of the Llama-3.3-70B model. This layer was chosen via 5-fold cross validation on the synthetic training dataset. In Figure 9 we see the mean cross-validation accuracy across different layers of the model. Note that, although this plot shows that layer 30 has the highest cross-validation accuracy, layer 31 was chosen based on the results of an earlier cross-validation experiment

A.2 Baselines

Prompted Baselines.

For our baselines, we designed four different prompt templates and evaluated the baselines using all four templates on the development split of our evaluation datasets. For each model, we then picked the template that led to the highest average AUROC (see Figure 10) and evaluated it on the test split of the evaluation datasets. Note that, especially for smaller models, the choice of prompt template can have a great effect on the performance of prompted baselines.

The prompt templates we chose for each model can be found in Table 4. Below you can find the four prompt templates:

Finetuned Baselines.

Hyperparameters used for training our finetuned baselines can be found in Figure 8. We computed a validation loss on the validation split of our synthetic dataset to decide which checkpoint to use. Note that we while we trained for 10-25 epochs for most models, the best epoch (and checkpoint we used for evaluation) was between 2-4 for smaller models (Llama-1b and Gemma-1b), 3-5 for Llama-8b and 1-2 for Gemma-12b. In particular, learning rate scheduling did not help for smaller models. For Llama-8b, we found gradient clipping to be particularly important for getting good results. Surprisingly, for Gemma-12b, a gradient accumulation of 4 led to much better performance on the dev split than using a gradient accumulation of 128, mostly because of the ToolACE dataset (AUROC of around 0.9 compared to AUROC below 0.7).

A.3 Estimating Computational Cost

Assumptions.

When estimating computational cost, we make the following general assumptions:

- • 

Activations from Llama-70b for the given conversation (in exactly that conversation format) are already available at no extra cost. This is because we assume the monitored system already uses Llama-70b as its primary model to generate responses to user queries, and the activations we need are a natural byproduct of this inference process.

Note that the prompted baseline of Llama-70b uses a different prompt structure, therefore we assume that this baseline model has to process the whole sequence. (The cost of the prompted Llama-70b could potentially be reduced by keeping the same conversation format and asking about the stakes label at the end, but it is unclear how much that would affect performance.)

- • 

All models are already trained, i.e. we only consider inference time costs. In particular, we do not consider training costs of probes or finetuned baselines.

Computational cost of baseline models.

For all baseline models, we first estimate the number of FLOPs per token required to process a sequence of length \(S\) based on the model architecture. Each multiply-add pair counts as two FLOPs.

We start from the following generic formulas, which approximate the number of FLOPs per token for a sequence of length \(S\):

- • 

Llama-3: \(F_{\text{Llama}}(S)=S\,[\,2N+2md\,S\,]\)

- • 

Gemma-3 (5 local and 1 global attention layer; window \(w\)): \(F_{\text{Gemma}}(S)=S\left[\,2N+2md\!\left(\tfrac{5}{6}w\right)+2md\!\left(\tfrac{1}{6}S\right)\right]\)

where \(N\) is the total parameter count, \(m\) the number of decoder layers, \(d\) the hidden size, and \(w\) the sliding-window span in the local layers (Gemma only). These estimates are similar to the rule of thumb of taking twice the number of model parameters as approximate per-token computation cost as suggested in (Pope et al., 2022), but include terms to approximate contributions from the attention mechanism which are partly quadratic in \(S\).

Plugging in the parameters for the specific models, we obtain the compute costs formulas listed in Table 5.

We discard the second term which comes from the attention mechanism as the total compute cost is dominated by the first term for all sequence lengths in our datasets, \(S\leq 4000\). When processing our datasets, we log the number of tokens for each sample and aggregate the total number of FLOPs based on which samples were passed to the respective baseline model.

Note that finetuned and prompted baselines use different prompt templates, which explains why the number of FLOPs for the finetuned and prompted baseline of the same model can be different (e.g. see Figure 13).

Computational cost of probes.

Note that we estimate the number of FLOPs for our probes as well, but they are several orders of magnitude smaller and thus not noticeable in probe+baseline combinations in the plot (Figure 6).

The specific estimates for the relevant probes can be found in Table 6.

A.4 Hardware Resources

Infrastructure.

We used the following infrastructure for our experiments:

- • 

Cloud servers from the cloud provider Lambda Labs, Vast.ai and Runpod were used for our experiments. For computing activations, a machine with 2xH100 GPUs (80GB each) and \(\sim 400\)GB of RAM was used. For training and evaluating probes with pre-computed activations, a machine with 1xA100 (40GB) and \(\sim 200\)GB of RAM was sufficient. For finetuning baselines up to 8B parameters, a machine with 1xH100 (80GB) was used. Gemma-12B was finetuned on a machine with 1xH100 NVL. Prompted baselines up to Gemma-27B can be run on a single H100; for the Llama-70B prompted baseline we used a machine with 2xH100 (80GB each).

- • 

We used Cloudflare R2 for storing datasets and cached activations. In total we used 413.69 GB, which cost less than \$10 per month.

Running time.

Approximate times it takes to run various parts of this work:

- • 

Dataset generation pipeline: Generating the full synthetic dataset takes \(\sim 3\) hours, with a limit of 100 concurrent API requests.

- • 

Labelling datasets: A few minutes per dataset.

- • 

Training probes: Up to 2 hours on a machine with 1xA100 (40GB) based on pre-computed activations.

- • 

Finetuning baselines on the full synthetic dataset: \(\sim 3\) hours for finetuning Gemma-12B on a machine with 1xH100 NVL; \(\sim 2\) hours for finetuning Llama-8B on a machine with 1xH100; less than two hours for smaller models.

- • 

Prompted baselines: Less than one hour per baseline and dataset for bigger models; prompted baselines for smaller models took less than one hour for all datasets.

Overall compute resources.

In total, we spent approximately 7000 USD on compute resources for this project. This includes earlier dataset generation, relabelling datasets, failed experiments and debugging (which was most costly for finetuning baselines as we tried using bigger machines for some experiments).

Appendix B Further Experimental Results

B.1 Generalisation within Synthetic Dataset

When generating our synthetic dataset, for diversity we introduced deliberate variation along the following axes:

- • 

Language: we generated samples in English, French, German and Hindi.

- • 

Length: we generated samples which are very short (˜20 words), short (˜50 words), medium (˜100 words) or long (˜200 words).

- • 

Tone: we generated samples which are written in a casual, polite, angry, or vulnerable tone.

- • 

Prompt Style: we generated questions, responses, third-person statements, and LLM prompts.

These were deliberately chosen as factors which could potentially confound our high-stakes target. In Figure 11 we test the generalization of the high-stakes probes across each of these potentially confounding factors, and find that none of them have a significant effect on probe accuracy.

B.2 Probes vs Baselines Across all Datasets

In Figure 12, we see the performance of our probes and all baselines across all test datasets.

For Anthropic, MT, MTS and Toolace, we used a subset of the dataset for development iteration. Aya Redteaming and Mental Health were fully held-out. These are both interesting: for all other datasets, our probes’ performance is roughly in line with the baselines. However our probes significantly outperform all baselines other than Llama-70B on Aya Redteaming, and our probes underperform all baselines (with the exception of Softmax beating Llama-1B finetuned) on Mental Health.

We believe the reason for the performance on Aya Redteaming is that, due to the nature of this dataset, the judgement of high- or low-stakes is particularly fuzzy (see Table 9), and perhaps varies by LLM (which is supported by the fact that both high-scoring classifiers were based on Llama-70B).

We do not know why our probes underperform on Mental Health.

The TPR at 1% FPR for our probes is low across all datasets except MT. TPR at 1% FPR is a useful metric since it represents what proportion of positive samples can be caught in deployment with an acceptable cost to users (such as 1% of samples being flagged). As discussed in Section 3, our setting is less sensitive to false positives than a single-layer monitoring setup, thus for internal flagging purposes, operating at 20-40% FPR could be reasonable, where our probes achieve substantially better TPR (see full ROC curves in Figure 4.

B.3 Comparing alternative methods of combining probes and baselines

Combining a probe with a baseline within a cascade involves the following choices:

- • 

Selection: After running the probe on all samples, a subset of samples is selected to give to the baseline for further processing. The parameter \(k\)% directly controls the monitoring budget—if we send \(k\)% of samples to the expensive baseline, we incur \(k\)% of the baseline’s computational cost while maintaining 100% coverage through the cheap probe. We consider three strategies: “top”, which selects samples with the highest probe scores, “bottom” which selects samples with lowest probe scores and “mid” which selects samples with scores around the median score.

- • 

Combination: Samples passed to the baseline model end up having two scores, one from the probe and one from the baseline. We combine these scores by taking the maximum, the mean or by discarding the probe score and overwriting it with the baseline score.

- • 

Remaining: For samples not given to the baseline models, we keep the probe score in cascade methods.

We tried all these different strategies. In our plots, we only include results for selecting samples with scores around the median and combining them using average, as this way of combination consistently outperformed other strategies. A plot with additional combinations of probe and baseline methods can be found in Figure 13.

The motivation for choosing samples around the median is as follows: given a fixed "expensive monitoring" budget \(k\)%, we want to select the \(k\)% of samples where the probe is most uncertain. If the calibration curve for the probe is approximately monotonically increasing, then a score far from 0 or 1 should correspond to a lower probability of correctly classifying a sample. Since our probes are not perfectly calibrated (Figure 15), the score with the lowest probability of correctness is not \(0.5\). At deployment time, it is reasonable to assume we have access to an approximate distribution of scores (by e.g. keeping track of the last \(n\) scores), but it is not reasonable to assume access to the ground truth, so as a reasonable estimate we pick the median score as that which has lowest probability of correctness. As long as the errors of the probe scores are sufficiently uncorrelated with the errors of the baseline scores, combining these probe scores with a baseline score should improve the probability of predicting correctly.

We note that, in a real deployment environment, a cascaded monitoring system would look very different to this experiment. For the purposes of this paper, we chose to focus exclusively on high- and low-stakes, but in reality high-stakes would not be the terminal task, and the purpose of classifying an input as high-stakes would be to flag for further processing. Thus, even though in this experiment we are sending k% of samples around the median to a more expensive classifier, that is not something we would recommend in a deployment system.

B.4 Do Probes Outperform Simple Word Statistics?

In addition to the finetuned and prompted LLM baselines, we trained a simple classifier based on word statistics to establish a lower bound on performance.

Our word-statistics classifier uses Term Frequency-Inverse Document Frequency (TF-IDF) to transform text into vectors. We then train a Support Vector Machine (SVM) classifier using the train split of our synthetic dataset. We tried a number of different classifier architectures, including simple Bag-of-Words instead of TF-IDF, as well as replacing the SVM with a logistic regression; the combination of TF-IDF and SVM was the best performing.

As can be seen in Figure 14, this simple classifier performs significantly worse on the eval datasets than our Attention probe.

B.5 Calibration of Probes and Baselines

In Figure 15 we see the calibration curve for the three best probe designs on each evaluation dataset. Some datasets show better calibration than others: in particular, Mental Health and MTS have particularly poor calibration. For MTS, this is likely due to the small sample size for each bin. For Mental Health, the poor calibration, taken together with the low AUROC and TPR at 1% FPR relative to baselines in Figure 12, suggests our probes failed to robustly learn the notion of high-stakes in this dataset.

The calibration curves are mostly above the perfect calibration line, which means our probes consistently under-estimate the stakes of an interaction relative to our GPT-4o judge.

In Figures 16 and 17, we see that calibration is relatively poor for most finetuned and prompted baselines.

B.6 Alternative Strategies for Training on Deployment Samples

In Figure 18 we compare the performance of our probes finetuned on deployment samples (after training on the synthetic dataset) to the performance we get when training a probe directly on synthetic and deployment data combined.

Appendix C Training and Evaluation Datasets

C.1 Details on Synthetic Dataset Generation

We follow the methodology as shown in Figure 19, and described in three steps as follows:

Situation Generation: We first prompt GPT-4o to generate high- and low-stakes situations, varying our prompt along the axes - domains, user roles, and impact of the situations as described in Table 7. These variations ensured diversity in the situations generated. The following is the specific prompt for generating an example situation pair in the environmental domain, with teachers and students as the user roles, and considering the impact of permanent harm.

The resulting situation pair is as follows:

Sample Generation: For each of the generated situations, we instruct GPT-4o to produce varied and realistic samples representing queries or messages someone might pose to an LLM in those situations. Variations in the samples included altering the tone, length, language, and style. Table 8 summarises the variations and the number of samples corresponding to each of the variation categories. The following is the specific prompt for generating high- and low-stakes sample pairs based on the situation pairs mentioned above.

The resulting high and low stakes prompts pair is described below:

Sample Filtering: To maintain clarity in the dataset, we labelled the generated samples using GPT-4o by giving “stakes scores" from 1-10, along with confidence scores (for the provided labels) from 1-10. Ambiguous samples that had stakes scores of 4-7 and samples whose confidence score was less than 8 were removed. Following are few examples of ambiguous samples.

For minimising the confounding words, we implemented a bag-of-words classifier for high/low stakes classification based on the samples. We removed the samples containing the most confounding words as identified by examining the top important tokens from the bag-of-words classifier as it learns surface-level patterns (words and their frequency). The classification accuracy of bag-of-words on our training data is 88.9%. Examples of most predictive words for high-stakes include safety, trust, risking, crisis, crucial, and emergency. Examples of most predictive words for low-stakes include minor, low, minimal, simple, delightful, and whiskers.

C.2 Synthetic Dataset Examples

See Section C.1.

C.3 Further details on Evaluation Datasets.

We generate our evaluation datasets (except the manual dataset) according to the following procedure:

- 1. 

Randomly sample from the dataset (on the order of 1000-4000 samples)

- 2. 

Label how high-stakes the samples are on scale from 1-10 and how confident this prediction is using GPT-4o, we use the same prompt for filtering our synthetic dataset (see section C.4).

- 3. 

Create a balanced version of the dataset by removing ambiguous cases (high-stakes score in 4-7 or confidence \(&lt;6\))

We first create dev versions of the evaluation datasets, then re-run the same procedure for generating test versions ensuring that no samples from dev (before filtering) are included in the test dataset. We sample from the following datasets to construct our evaluation datasets:

Anthropic HH-RLHF Bai et al. (2022): User-LLM conversations involving harmful requests; around 160.000 English conversations with human preference labels; Including prompts to test model behavior on harmlessness and providing useful answers; licensed under MIT License (see their README)

ToolACE Liu et al. (2024): Diverse synthetic dataset consisting of LLM interactions involving tool use; contains over 11.000 entries; licensed under Apache 2.0 License (see metadata in their README)

MT Samples Boyle (2018): Transcribed medical reports from doctors, licensed under CC0: Public Domain; originally scraped from the website https://mtsamples.com.

MTS Dialog Ben Abacha et al. (2023): Doctor-patient conversations and corresponding summaries; for this dataset we take their test split as test split and their training and dev splits as our dev split (after filtering); licensed under CC BY 4.0 (see the README in the corresponding repository)

Mental Health Sarkar (2023): Statements posted on social media of which many are related to mental health conditions; licensed under ODbL 1.0

Aya Redteaming Aakanksha et al. (2024): Dataset of prompts aiming at eliciting harmful behaviour; accessed as corresponding HuggingFace dataset AI (2024); licensed under Apache 2.0 License

For each of these datasets, we release our modified version of the datasets under the same license as the original dataset.

C.4 Labelling

We use GPT-4o for adding stakes labels to our datasets. For labelling whether a conversation is high- or low-stakes (both for the synthetic dataset and evaluation datasets), we use the following system prompt:

We discard ambgiuous samples with scores between 4-7 or a confidence of less than 8. We then assign a low-stakes label to samples with scores 1-3 and a high-stakes label to samples with scores 8-10.

C.5 Manual Annotation

In order to check whether we agree with the ground truth labels for situational stakes, our main contributors manually annotated 20 samples from each evaluation dataset. The results can be found in Table 9.

Annotation details.

For manually reviewing dataset samples, we randomly selected samples from each evaluation dataset using a Python script. We prepared items for annotation in such a way that each sample was annotated by exactly two annotators and for each dataset, the overlap of samples annotated by any two annotators was at most 10. All items were written to a Google Spreadsheet, having a separate tab for every combination of annotator and dataset. The spreadsheet had two columns to be filled in, one for the stakes score (1-10) and another optional column for an explanation.

C.6 High-Stakes Labels and Deception

We looked at whether our high-stakes label correlates with observed deceptive behaviour in Llama-70B. We used the datasets “AI Liar”, “AI Audit”, “Roleplaying” and “Sandbagging WMDB/MMLU” from the codebase of Goldowsky-Dill et al. (2025). Each of these datasets has a “deception score” field, which we normalized to between 0 and 1. We also used the MASK Benchmark dataset (Ren et al., 2025), where we used the “honesty score” of the high-pressure prompts as the deception score. For MASK, we also separately looked at whether our high-stakes label correlates with whether the sample is “high-pressure” across both high-pressure and belief elicitation prompts.

As can be seen in Figure 20, for the AI Liar and Sandbagging datasets, there is a clear correlation between stakes level and deception score. For MASK and Roleplaying, there is no clear correlation, and for AI Audit, there is a negative correlation. Each of these datasets induces deception in a different way. For AI Audit, deception occurs when the model does not disclose to an auditor that a possible rule violation has taken place. A negative correlation with stakes suggests that, as the scope of the rule violation increases, the likelihood of Llama-70B reporting it increases.

For MASK, pressure is applied, and we observe whether the model changes its answer from truthful to false. It is possible that, when GPT-4o considers such a sample to be very high-stakes (9 or 10), that is in light of recognising that it is being pressured to lie—and regardless of whether the sample actually involves lying. Indeed, in Figure 21, we see that the positive correlation between “pressure” and stakes is much stronger than the correlation between stakes and pressure-induced dishonesty.

However, these results on the relation between situational stakes and deception are still very unclear, and more research is needed.
