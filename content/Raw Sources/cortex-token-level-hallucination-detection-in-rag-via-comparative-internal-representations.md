---
title: "CORTEX: Token-Level Hallucination Detection in RAG via Comparative Internal Representations"
type: "raw-source"
url: "https://arxiv.org/html/2606.31033v1"
author: "Kazuaki Furumai"
publication: "arXiv"
published: "2026-01-31"
archived: "2026-11-21T19:01:16Z"
---

> [!quote] Original source
> **Author(s):** Kazuaki Furumai  
> **Title:** CORTEX: Token-Level Hallucination Detection in RAG via Comparative Internal Representations  
> **Published in:** arXiv  
> **Date:** 2026-01-31  
> **Original:** <https://arxiv.org/html/2606.31033v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-cortex-token-level-hallucination-detection-in-rag-via-comparative-internal-representations|Source note]]
Themes: [[Retrieval and agentic data science]]
Why it was archived: When sentence-level/token-level grounding judging beats single-pass answer-level judging for grounded RAG agents

## Archived text

CORTEX: Token-Level Hallucination Detection in RAG via Comparative Internal Representations

Abstract

In this paper, we propose CORTEX, a token-level hallucination detection method for Retrieval-Augmented Generation (RAG). In long-form RAG outputs, hallucinations often arise in localized spans rather than throughout an entire response. CORTEX therefore identifies ungrounded content at the token level, enabling fine-grained localization of hallucinations. The key intuition behind CORTEX is that tokens grounded in retrieved documents should be more strongly influenced by those documents than hallucinated tokens. To capture this document-induced effect, CORTEX compares internal representations of a large language model (LLM) under two conditions: with and without the retrieved documents. Instead of relying solely on each token’s immediate sensitivity to the retrieved documents, CORTEX also leverages the propagation of document-grounded information through preceding tokens, reducing false positives for tokens whose evidence has already been absorbed into the context. Finally, CORTEX applies post-processing smoothing step that models the tendency of hallucination labels to persist over contiguous spans, reducing local noise and encouraging span-consistent predictions. Experiments on two RAG benchmarks and three LLMs show that CORTEX substantially improves token-level hallucination detection, with each component consistently contributing to performance gains.

1 Introduction

Retrieval-Augmented Generation (RAG) has been widely adopted to improve the factuality of large language models (LLMs) by grounding generation in external references (Lewis et al., 2020). Although RAG mitigates hallucinations to some extent, LLMs may still generate groundless or inconsistent content even when references are provided (Fan et al., 2026). Accurately detecting such hallucinations within generated outputs therefore remains a critical challenge (Niu et al., 2024; Liu et al., 2025; Bang et al., 2025).

Various hallucination detection methods have been proposed to address this challenge. Self-consistency-based approaches estimate reliability by measuring agreement across multiple outputs from the same prompt (Manakul et al., 2023). Prompt-based methods use LLMs as fact-checkers to explicitly verify generated content (Zheng et al., 2023; Es et al., 2024; Furumai et al., 2024). While these approaches leverage LLMs’ strong language understanding capabilities, they may incur high computational cost due to repeated sampling, and their reliability can depend on prompt design (Ganesh et al., 2026).

More recently, hallucination detection methods based on the internal representations of LLMs have been increasingly studied (Sriramanan et al., 2024; Zhang et al., 2025; Xiong et al., 2026). These methods seek hallucination-related signals in model activations and can offer insight into the internal conditions under which hallucinations arise. This line of work has analyzed attention and feedforward-network states, quantified component contributions to generation, and extracted hallucination-related features from internal representations.

However, many existing approaches are not designed specifically for RAG and primarily assess the generated output as a whole, i.e., at the answer level. This is limiting for long-form RAG outputs, where faithful and hallucinated content often coexist. For practical use, detecting hallucinations in such mixed outputs requires a finer-grained formulation than answer-level detection. The appropriate granularity can vary across tasks and annotation protocols, from words and phrases to sentences or paragraphs. Given this variability, token-level detection can serve as a practical approach for localizing ungrounded content and later adapting predictions to the required granularity.

In this paper, we propose CORTEX (Comparative Observed Reference-based Token-level EXpressions), a post-hoc token-level hallucination detection method for RAG. Figure 1 illustrates the overall framework. CORTEX builds on the intuition that faithful tokens should exhibit coherent representational changes when references are provided, whereas hallucinated tokens should show weaker or less coherent changes. To measure this effect, CORTEX constructs a paired counterfactual view of the same answer under reference-conditioned and no-reference inputs, rather than probing a single input as in conventional representation-based detectors. The resulting reference-induced changes are then encoded as token-level delta features for hallucination detection.

CORTEX further introduces an attention-based contextual residual feature. In long-form generation, reference influence may propagate indirectly through preceding answer tokens, as in reasoning-style or self-referential generation. CORTEX captures this context-mediated reference influence by combining token-level delta features with attention patterns, helping the classifier distinguish tokens that are indirectly grounded in the reference from groundless tokens and thereby reducing false positives.

Finally, CORTEX uses post-processing smoothing step to adjust the granularity of token-level scores. Raw token-level predictions can be sensitive to local noise and may produce isolated high-score tokens, whereas human hallucination annotations often appear as contiguous spans. We therefore introduce label-persistence smoothing, which treats raw scores as token-level confidence and models the tendency of hallucination labels to persist across neighboring tokens. This reduces scattered noise and adapts token-level predictions to span-level annotation structure while still retaining token-level scores.

Experiments on two RAG benchmarks and three LLMs demonstrate that CORTEX substantially improves token-level hallucination detection, with all components contributing consistently to performance gains.

Our contributions are summarized as follows:

- • 

We propose CORTEX, which, to the best of our knowledge, is the first token-level hallucination detection method specifically designed for RAG.

- • 

CORTEX is a practical post-hoc framework that is easy to implement and can detect hallucinations in outputs from arbitrary LLMs, including API-based closed-weight models.

2 Preliminaries

We consider a practical setting in which the answer is produced by a closed-weight LLM whose parameters and internal representations are not accessible, as is the case for many API-based models. Such models are often attractive in deployed applications because of their strong generation quality. We denote this closed-weight LLM by \(M_{\mathrm{close}}\). Given a question \(q^{\mathrm{text}}\), the closed-weight LLM produces an answer as

Our goal is to identify hallucinated tokens in the generated answer \(a^{\mathrm{text}}\). Although a direct way to obtain hallucination-related features would be to analyze the internal representations of the closed-weight LLM, we cannot do so for the aforementioned reason. We therefore use a separate open-weight LLM, denoted by \(M_{\mathrm{open}}\), as a post-hoc analysis model. Unlike \(M_{\mathrm{close}}\), \(M_{\mathrm{open}}\) exposes internal representations, which allows us to extract features from the answer in relation to the question.

Let \(\mathrm{Tok}(\cdot)\) denote the tokenizer of \(M_{\mathrm{open}}\). We tokenize the answer as

where \(T\) denotes the number of answer tokens and \(t_{i}\) denotes the \(i\)-th answer token under the tokenizer of \(M_{\mathrm{open}}\). We assume that \(M_{\mathrm{open}}\) processes an input containing the question and the answer as \(M_{\mathrm{open}}(q^{\mathrm{text}}\|a^{\mathrm{text}})\), where \(\|\) denotes text concatenation with the appropriate prompt format. \(M_{\mathrm{open}}\) produces token-level internal representations over the entire input sequence, which capture the relationships between \(q^{\mathrm{text}}\) and \(a^{\mathrm{text}}\). Since hallucination detection is performed over the answer, we use only the internal representations corresponding to the answer tokens. We denote the representation aligned with answer token \(t_{i}\) by \(h_{i}\in\mathbb{R}^{d}\). The specific input construction and the extraction of answer-token representations are described in Section 3.

The token-level hallucination detection task is to estimate whether each answer token is hallucinated. Let \(y_{i}\in\{0,1\}\) denote the token-level label, where \(y_{i}=1\) indicates that token \(t_{i}\) is hallucinated and \(y_{i}=0\) indicates that it is faithful.

In our setting, we focus on RAG applications, where references are provided as grounding evidence for answers. This setting reflects common practical deployments in which retrieved documents are used to reduce hallucination and the answer is expected to be faithful to those references.

3 CORTEX

We propose CORTEX (Comparative Observed Reference-based Token-level EXpressions), a post-hoc hallucination detection framework for RAG.

CORTEX is built on three key ideas, illustrated in Figure 1(a)–(c): (a) a reference-induced delta representation for capturing how each answer token’s internal representation changes when the references are provided; (b) an attention-based contextual residual for distinguishing direct reference sensitivity from reference influence mediated by preceding answer tokens; and (c) label-persistence smoothing for reducing isolated token-level noise and obtaining span-consistent hallucination scores while preserving token-level predictions.

3.1 Reference-Induced Delta Representation

CORTEX constructs two conditioned inputs for the open-weight LLM, differing only in whether the references are included. Let \(r^{\mathrm{text}}\) denote the references, i.e., the retrieved documents used as grounding evidence in the RAG setting. The reference-conditioned input is defined as \(x_{\mathrm{ref}}^{\mathrm{text}}=q^{\mathrm{text}}\|r^{\mathrm{text}}\|a^{\mathrm{text}}\), whereas the no-reference input is defined as \(x_{\mathrm{no\text{-}ref}}^{\mathrm{text}}=q^{\mathrm{text}}\|a^{\mathrm{text}}\). With this construction, the answer span corresponds to the same token sequence \((t_{1},\ldots,t_{T})\) in both conditions, allowing CORTEX to compare internal representations aligned with the same answer tokens.

When \(M_{\mathrm{open}}\) processes \(x_{\mathrm{ref}}^{\mathrm{text}}\) and \(x_{\mathrm{no\text{-}ref}}^{\mathrm{text}}\), it produces token-level internal representations over the entire input sequence. For an input \(x=\mathrm{Tok}(x^{\mathrm{text}})\), let \(\mathrm{Rep}_{M_{\mathrm{open}}}(x)\) denote the sequence of internal representations obtained from \(M_{\mathrm{open}}\). We define an extraction function \(f\) that selects the representations aligned with the answer tokens:

Here, \(h^{\mathrm{ref}}_{i},h^{\mathrm{no\text{-}ref}}_{i}\in\mathbb{R}^{d}\) denote the internal representations aligned with the same answer token \(t_{i}\) under the reference-conditioned and no-reference conditions, respectively, and \(d\) denotes the representation dimensionality.11 1 Specifically, we use the final transformer layer output corresponding to each answer token as its token-level representation \(h_{i}\).

CORTEX builds on the intuition that faithful tokens should exhibit coherent representational changes when references are provided, whereas hallucinated tokens should show weaker or less coherent changes. Based on this intuition, CORTEX computes the reference-induced delta representation for each answer token \(t_{i}\) as

This vector is the core representation in CORTEX. Since the same answer is included in both inputs, \(\Delta h_{i}\) captures how the representation of token \(t_{i}\) changes when references are provided. In other words, \(\Delta h_{i}\) is intended to emphasize the reference-induced change in how \(M_{\mathrm{open}}\) contextualizes that token, rather than merely representing the token content itself.

3.2 Attention-Based Contextual Residual

The delta representation \(\Delta h_{i}\) captures how the representation of token \(t_{i}\) changes when references are added. However, in reasoning-style outputs such as chain-of-thought, facts grounded in the references may first be stated in earlier parts of the answer, and later tokens may continue the reasoning based on those facts. In this case, the influence of the references can reach \(t_{i}\) not only through the direct path \(r\rightarrow t_{i}\), but also through the context-mediated path \(r\rightarrow t_{&lt;i}\rightarrow t_{i}\). As a result, even tokens that are indirectly grounded by the references may appear to have a weak relationship with the references if we only use \(\Delta h_{i}\).

To address this issue, we introduce a feature that represents how much reference influence is contained in the preceding tokens that the current token \(t_{i}\) relies on as

where \(\alpha_{ij}^{\mathrm{ref}}\in[0,1]\) denotes the attention weight from \(t_{i}\) to a preceding answer token \(t_{j}\) under the reference-conditioned input. We further subtract this context-mediated influence from the current token’s own change and define the contextual residual as

This residual represents the token-specific change that remains after removing the reference influence explainable through preceding tokens. We use both \(\Delta h_{i}\) and \(c_{i}\) for token-level hallucination detection.

3.3 Token-Level Hallucination Detection

For each answer token \(t_{i}\), CORTEX predicts a raw token-level hallucination score \(s_{i}\) by feeding \([\Delta h_{i};c_{i}]\) into a multilayer perceptron (MLP) classifier \(g_{\theta}\):

where \(\sigma\) denotes the sigmoid function. The classifier is trained with binary cross-entropy loss using token-level hallucination labels. To address class imbalance, the positive class is weighted according to the ratio of negative to positive tokens in the training set.

3.4 Label-Persistence Smoothing

We define a span as a contiguous sequence of tokens annotated as a single hallucination unit. Human hallucination annotations are typically span-based: once a token is marked as hallucinated, neighboring tokens in the same span are likely to receive the same label. Based on this property, we apply label-persistence smoothing as a post-processing step, rather than using moving-average smoothing.

Given the raw token-level scores \(s_{1:T}\), we introduce an unobserved binary smoothing-label variable \(z_{i}\in\{0,1\}\) to represent the span-consistent label underlying the post-processed score, where \(z_{i}=0\) denotes a faithful token and \(z_{i}=1\) denotes a hallucinated token. To obtain span-consistent post-processed scores, we model the smoothed label sequence by combining two components around positions \(i\) and \(i+1\): the tendency of neighboring labels to persist and information from the raw scores at each position.

We first model span-level label persistence by defining the pairwise persistence term between neighboring labels as

The parameter \(p_{\mathrm{stay}}\in[0,1]\) controls the degree of label persistence: smaller values allow finer-grained label changes, whereas larger values favor longer same-label spans. This provides a deliberately simple approximation to span-level label continuity, rather than modeling the full variability of human annotation patterns. We then define the token-level confidence induced by the raw score \(s_{i}\) at each position:

This quantity represents how the raw score at position \(i\) is converted into token-level confidence for each value of the smoothing-label variable.22 2 In implementation, we apply a small amount of clipping to the raw scores so that the token-level confidence does not become exactly 0 or 1.

Combining Eq. (8) and Eq. (9), we define the local compatibility term for neighboring positions \(i\) and \(i+1\) as

This term measures the compatibility of the neighboring label assignment \((z_{i},z_{i+1})\) with both the raw scores and the label-persistence assumption.

We therefore define the normalized distribution over sequence labels as

where \(Z(s_{1:T})\) is the normalizing constant and \(\pi(z_{1})\) is the initial distribution over the first smoothing label. We use a uniform initial distribution, \(\pi(0)=\pi(1)=1/2\).

Although \(z_{1:T}\) is unobserved, the desired token-level smoothed score can be obtained by marginalizing over all smoothing-label sequences:

This posterior can be computed efficiently using the forward–backward algorithm (Rabiner, 1990). We provide the full recursions and posterior marginal formula in Appendix A.

4 Experiments

We evaluate CORTEX on two publicly available RAG hallucination benchmarks, RAGTruth (Niu et al., 2024) and HalluRAG (Ridder and Schilling, 2024), using three LLMs: Llama-3.1-8B-Instruct (Grattafiori et al., 2024), Qwen3-8B (Yang et al., 2025), and Mistral-7B-Instruct-v0.2 (Mistral AI, 2023). We use these open-weight LLMs to obtain internal representations for CORTEX and the relevant baselines. Evaluation is performed at the token and answer levels. Token-level evaluation assesses whether a method can identify hallucinated tokens in a generated answer, while answer-level evaluation assesses whether the answer contains any hallucinated content. For CORTEX, answer-level evaluation is performed by aggregating token-level scores, as it is trained for token-level detection and does not use answer-level supervision. Specifically, we use the maximum token-level hallucination score as the answer-level score.

For label-persistence smoothing, we use \(p_{\mathrm{stay}}=0.993\) at the token level and \(p_{\mathrm{stay}}=0.930\) at the answer level. We provide a sensitivity analysis of \(p_{\mathrm{stay}}\) in Appendix B. Additional details on the experimental setup are provided in Appendix C. The following subsections describe the baselines and datasets used in our experiments.

4.1 Baselines

We compare CORTEX with five baselines. NLL uses negative log-likelihood as an uncertainty-based signal, following prior work on uncertainty estimation from next-token predictive distributions (Malinin and Gales, 2021). SAPLMA trains a probe on intermediate transformer representations, based on the observation that hidden states encode hallucination-related signals (Azaria and Mitchell, 2023). LLM-Check extracts features from internal states produced by attention mechanisms and feedforward neural networks, including spectral properties such as eigenvalues (Sriramanan et al., 2024). ICR Probe uses internal component attribution to quantify the contribution of attention and feedforward networks and identify hallucinated content (Zhang et al., 2025). RAGLens applies sparse autoencoders to token embeddings and selects hallucination-related sparse features via token aggregation and mutual-information-based feature selection (Xiong et al., 2026).

For answer-level evaluation, we follow the original implementation of baselines. However, their answer-level implementation cannot be directly used for token-level evaluation. We modify parts of the baseline implementations to adapt them to token-level detection while preserving their original mechanisms as much as possible.

4.2 Datasets

Datasets for hallucination detection in RAG settings remain limited, especially those that include both references and fine-grained hallucination annotations. To the best of our knowledge, RAGTruth is the only publicly available RAG benchmark with human-annotated hallucination spans that are sufficiently fine-grained to support token-level evaluation. Although RAGTruth contains multiple task types, we use only its QA subset in this work.

HalluRAG consists of answers generated by multiple LLMs under two RAG prompt settings using either relevant or irrelevant Wikipedia chunks, with sentence-level hallucination annotations by GPT-4o (OpenAI et al., 2024). Since token-level labels are unavailable, we derive token-level pseudo-labels by marking all tokens in hallucinated sentences as hallucinated.

The two datasets provide complementary settings, differing in annotation granularity, labeling procedure, retrieval quality, and QA distribution. RAGTruth provides fine-grained human span annotations, whereas HalluRAG provides sentence-level GPT-4o annotations and includes cases where references may be irrelevant to the question. They also differ in construction and topical coverage, with RAGTruth’s QA subset is based on daily-life questions, whereas HalluRAG derives questions from Wikipedia passages. Together, these differences allow us to assess robustness across conditions.

Both datasets contain answers generated by various LLMs, together with the references provided for generating those answers. We treat these answers as outputs from closed-weight LLMs, regardless of which model generated them. To ensure a fair comparison, all methods receive the same answer and corresponding references as input.

4.3 Results

Token-level Detection

Table 2 reports token-level hallucination detection results in terms of average precision (AP) and the area under the receiver operating characteristic curve (AUROC). Across both RAGTruth and HalluRAG, CORTEX achieves the best performance in all settings. The gains are particularly substantial on RAGTruth, where human fine-grained annotations are available, suggesting that CORTEX is well aligned with token-level hallucination detection. Even on HalluRAG, where token-level labels are derived from sentence-level annotations, CORTEX remains the best-performing method, indicating robustness to coarser and noisier supervision.

All baselines receive inputs with references, but rely on a single reference-conditioned view of model representations. SAPLMA directly uses transformer layer outputs as features, while RAGLens extracts hallucination-related sparse features from token embeddings using a trained sparse encoder. In contrast, CORTEX derives its signal from the contrast between paired representations of the same tokens with and without references. The consistent gains suggest that this comparative formulation captures reference-induced hallucination signals that are not readily available from a single internal representation or features derived from it.

Label-persistence smoothing is a post-processing module applicable to any token-level predictions. In Appendix D, we further apply it to baselines to demonstrate its general effectiveness.

Answer-level Detection

Table 3 reports the answer-level hallucination detection results in terms of AP and AUROC. Unlike the baselines, which are trained directly for answer-level detection, CORTEX does not use answer-level supervision. Instead, CORTEX reuses the token-level hallucination scores and assigns each answer the maximum score among its tokens. Thus, this setting evaluates whether the token-level signals captured by CORTEX can also indicate hallucination at the answer level.

Despite this simple aggregation strategy, CORTEX achieves competitive performance against the baselines. This suggests that its token-level predictions provide useful signals for both localized detection and answer-level reliability assessment. At the same time, the strong performance of some answer-level baselines suggests that answer-level detection may require global signals beyond localized token-level signals. Taken together, these results indicate that token-level and answer-level hallucination detection are both important and should be studied as complementary problems.

4.4 Ablation Study

To analyze the contribution of each CORTEX component, we conduct an ablation study. Table 4 reports token- and answer-level performance for each configuration. Both the contextual residual \(c\) and label-persistence smoothing (\(\mathrm{Smooth}\)) improve performance. Removing label-persistence smoothing shows that raw token-level scores are informative but locally unstable, while removing \(c\) shows that context-mediated reference influence provides information complementary to \(\Delta h\).

Figures 2 and 3 illustrate these effects qualitatively using cases with and without hallucinations. In the heatmaps, color intensity reflects the predicted hallucination score, with redder tokens indicating higher hallucination likelihood. In Figure 2, the model without label-persistence smoothing produces interleaved high- and low-score tokens across semantically coherent regions, yielding predictions less consistent with human span-level annotations. In contrast, full CORTEX produces smoother and more contiguous high-score regions, better matching the ground-truth hallucination spans. Figure 3 illustrates the role of the contextual residual \(c\). Without \(c\), the model can overemphasize the absence of direct reference influence and assign high scores to tokens indirectly grounded through the preceding answer context. With \(c\), CORTEX accounts for reference influence propagated through previous tokens and reduces false positives caused by indirect grounding.

Overall, these ablation results support the design of CORTEX. The combination of \(\Delta h\), the contextual residual \(c\), and label-persistence smoothing enables CORTEX to achieve robust localized hallucination detection. Further ablation case studies are presented in Appendix E.

5 Related Work

The problem of hallucination in LLMs has been extensively studied, yet remains unresolved (Huang et al., 2025; Kalai et al., 2025). It undermines the reliability of LLM-based AI agents and hinders real-world deployment. RAG mitigates hallucinations by incorporating references into prompts (Gao et al., 2024; Rackauckas, 2024), but LLMs may still generate hallucinated content even with references, motivating the detection of groundless or inconsistent RAG outputs (Fan et al., 2026).

Many hallucination detection methods rely on external verification or repeated generation. Self-consistency methods estimate reliability by comparing multiple outputs from the same prompt (Manakul et al., 2023), while prompt-based approaches use LLMs as judges or fact-checkers (Li et al., 2025; Es et al., 2024; Furumai et al., 2024). These methods exploit LLMs’ language understanding but depend on prompt design and verifier capability, and often require additional inference.

Another line of work uses model-internal signals, including uncertainty from next-token distributions (Malinin and Gales, 2021), hallucination-related information in intermediate transformer representations (Azaria and Mitchell, 2023), spectral features of attention and feedforward states (Sriramanan et al., 2024), component-level attribution for tracing information sources (Zhang et al., 2025), and sparse autoencoder features for RAG hallucination analysis (Xiong et al., 2026). These studies show that hallucination-related signals are present in model computations and representations, motivating representation-based detection.

CORTEX differs from prior representation-based approaches by comparing internal representations obtained from reference-conditioned and no-reference inputs, rather than analyzing a single internal state in isolation. It further uses label-persistence smoothing to reduce isolated noise and better align predictions with span-based hallucination annotations.

6 Conclusion

We proposed CORTEX, a post-hoc token-level hallucination detection method for RAG. CORTEX constructs a paired counterfactual view of the same answer by analyzing its internal representations with and without references, and encodes reference-induced changes as token-level delta features. It combines these features with attention patterns to capture context-mediated reference influence and uses label-persistence smoothing to reduce local noise while preserving span-consistent scores.

Experiments show that CORTEX substantially outperforms token-level baselines and achieves competitive answer-level performance through simple score aggregation. Ablations confirm the contributions of both the attention-based contextual residual and label-persistence smoothing. These results demonstrate the effectiveness of comparing internal representations for hallucination detection in RAG. By using an open-weight LLM to analyze outputs from closed-weight LLMs without modifying generation, CORTEX provides a practical approach to reliability assessment. Beyond detection, these comparative internal-representation signals may provide a basis for future hallucination mitigation, including reward modeling for tuning generators and objectives that encourage stronger reference-induced representations.

Limitations

CORTEX is designed for RAG settings and therefore assumes the presence of references against which generated outputs can be assessed. It is not intended to verify claims that are generated solely from the parametric knowledge of an LLM. This restriction may be acceptable, or even desirable, in controlled applications such as enterprise customer support, where answers should be grounded only in approved documents. In more open-ended assistant scenarios, however, this may be limiting because useful information that is not explicitly grounded in the provided references may be treated as groundless.

Another limitation is that CORTEX requires access to an open-weight LLM that exposes internal representations, including hidden states and attention weights. Although the original generator can be API-based or otherwise inaccessible, the post-hoc analysis model must provide sufficient internal signals. The quality of detection may therefore depend on the choice of the open-weight LLM and its ability to interpret the generated answer and references.

A further limitation is the need for fine-grained supervision during training. Although RAGTruth provides human span-level annotations, such annotations remain scarce for RAG hallucination detection. Improving supervision under limited annotation resources remains an important direction for future work.

Ethical Considerations

CORTEX is intended to support reliability assessment in RAG systems by identifying potentially groundless tokens in generated outputs. Such detection can help reduce the risk of users relying on hallucinated information, especially in applications where answers are expected to be grounded in specific references. However, CORTEX should not be interpreted as a guarantee of factual correctness. Its predictions are probabilistic and may include both false positives and false negatives; therefore, human review or additional verification may still be necessary in high-stakes domains.

There is also a risk that hallucination detection tools could be over-relied upon or used to present generated outputs as more reliable than they actually are. We encourage practitioners to communicate the limitations of detection results clearly and to avoid using CORTEX as the sole safety mechanism for critical decision-making.

It is also important to distinguish the scope of CORTEX from broader safety evaluation. CORTEX is designed to detect ungrounded content in reference-grounded generation, not to determine broader notions of truth, fairness, or social harm. Future work should examine how token-level reliability signals can be combined with other safeguards, including checks for bias, toxicity, privacy risks, and domain-specific safety issues.

References

- The internal state of an LLM knows when it‘s lying. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 967–976. External Links: Link, Document Cited by: §4.1, §5.
- HalluLens: LLM hallucination benchmark. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.), pp. 24128–24156. External Links: Link, Document, ISBN 979-8-89176-251-0 Cited by: §1.
- RAGAs: automated evaluation of retrieval augmented generation. In Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations, N. Aletras and O. De Clercq (Eds.), pp. 150–158. External Links: Link, Document Cited by: §1, §5.
- HalluHard: a hard multi-turn hallucination benchmark. Computing Research Repository arXiv:2602.01031. External Links: Link Cited by: §1, §5.
- Zero-shot persuasive chatbots with LLM-generated strategies and information retrieval. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pp. 11224–11249. External Links: Link, Document Cited by: §1, §5.
- Rethinking hallucinations: correctness, consistency, and prompt multiplicity. In Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers), V. Demberg, K. Inui, and L. Marquez (Eds.), Rabat, Morocco, pp. 6959–6978. External Links: Link, Document, ISBN 979-8-89176-380-7 Cited by: §1.
- Retrieval-augmented generation for large language models: a survey. Computing Research Repository arXiv:2312.10997. External Links: Link Cited by: §5.
- The llama 3 herd of models. Computing Research Repository arXiv:2407.21783. External Links: Link Cited by: §4.
- A survey on hallucination in large language models: principles, taxonomy, challenges, and open questions. ACM Transactions on Information Systems 43 (2). External Links: ISSN 1046-8188, Link, Document Cited by: §5.
- Why language models hallucinate. Computing Research Repository arXiv:2509.04664. External Links: Link Cited by: §5.
- Retrieval-augmented generation for knowledge-intensive nlp tasks. In Advances in Neural Information Processing Systems, H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin (Eds.), Vol. 33, pp. 9459–9474. External Links: Link Cited by: §1.
- From generation to judgment: opportunities and challenges of LLM-as-a-judge. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), pp. 2757–2791. External Links: Link, Document, ISBN 979-8-89176-332-6 Cited by: §5.
- Attention-guided self-reflection for zero-shot hallucination detection in large language models. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), pp. 21005–21021. External Links: Link, Document, ISBN 979-8-89176-332-6 Cited by: §1.
- Uncertainty estimation in autoregressive structured prediction. In Proceedings of the 2021 International Conference on Learning Representations, External Links: Link Cited by: §4.1, §5.
- SelfCheckGPT: zero-resource black-box hallucination detection for generative large language models. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 9004–9017. External Links: Link, Document Cited by: §1, §5.
- Mistral-7B-Instruct-v0.2. Note: Hugging Face model card External Links: Link Cited by: §4.
- RAGTruth: a hallucination corpus for developing trustworthy retrieval-augmented language models. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 10862–10878. External Links: Link Cited by: §1, §4.
- GPT-4o system card. Vol. arXiv:2410.21276. External Links: Link Cited by: §4.2.
- A tutorial on hidden markov models and selected applications in speech recognition. pp. 267–296. External Links: ISBN 1558601244 Cited by: §3.4.
- Rag-fusion: a new take on retrieval augmented generation. International Journal on Natural Language Computing 13 (1), pp. 37–47. External Links: ISSN 2319-4111, Link, Document Cited by: §5.
- The hallurag dataset: detecting closed-domain hallucinations in rag applications using an llm’s internal states. Computing Research RepositoryComputing Research Repository arXiv:2412.17056. External Links: Link Cited by: §4.
- LLM-check: investigating detection of hallucinations in large language models. In Proceedings of the 38th International Conference on Neural Information Processing Systems, External Links: ISBN 9798331314385, Link Cited by: §1, §4.1, §5.
- Toward faithful retrieval-augmented generation with sparse autoencoders. In The Fourteenth International Conference on Learning Representations, External Links: Link Cited by: §1, §4.1, §5.
- Qwen3 technical report. Computing Research Repository arXiv:2505.09388. External Links: Link Cited by: §4.
- ICR probe: tracking hidden state dynamics for reliable hallucination detection in LLMs. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics, pp. 17986–18002. External Links: Link Cited by: §1, §4.1, §5.
- Judging llm-as-a-judge with mt-bench and chatbot arena. In Proceedings of the 37th International Conference on Neural Information Processing Systems, External Links: Link Cited by: §1.

Appendix A Details of Label-Persistence Smoothing

This appendix gives the forward–backward recursions and posterior marginal derivation for label-persistence smoothing. The method defines non-negative weights over smoothing-label sequences by combining token-level confidence with label persistence between neighboring labels, so that posterior marginals can be computed efficiently without enumerating all \(2^{T}\) possible label sequences.

A.1 Forward Recursion

The forward message \(F_{i}(\ell)\) is the unnormalized total weight of all partial smoothing-label sequences ending with \(z_{i}=\ell\):

The initialization is

For \(i=2,\ldots,T\), the recursion is obtained by grouping the partial sequences according to the previous label \(\ell^{\prime}=z_{i-1}\). Starting from the definition,

The inner sum is exactly \(F_{i-1}(\ell^{\prime})\). Therefore,

Since the smoothing label is binary, the recursion can be written explicitly. Let \(p=p_{\mathrm{stay}}\). Using \(\phi_{i}(1)=s_{i}\) and \(\phi_{i}(0)=1-s_{i}\), we obtain

and

The corresponding initial values are

A.2 Backward Recursion

The backward message \(B_{i}(\ell)\) is the unnormalized total weight of all suffix smoothing-label sequences from positions \(i+1\) to \(T\), conditioned on \(z_{i}=\ell\):

The initialization is

which corresponds to the empty product beyond the final token.

For \(i=T-1,\ldots,1\), the recursion is obtained by grouping the suffix sequences according to the next label \(\ell^{\prime}=z_{i+1}\). Starting from the definition,

The inner sum is exactly \(B_{i+1}(\ell^{\prime})\). Therefore,

For the binary case, this recursion is equivalently

and

The terminal values are

A.3 Posterior Marginal

The posterior marginal for smoothing label \(\ell\) at position \(i\) is

Substituting the normalized sequence weight gives

Because the sequence weight has a first-order linear-chain factorization, fixing \(z_{i}=\ell\) separates the unnormalized weight into prefix and suffix terms:

Thus,

The normalizing constant can be decomposed at position \(i\):

Therefore,

The final smoothed hallucination score is

Appendix B Sensitivity Analysis of \(p_{\mathrm{stay}}\)

We analyze the sensitivity of CORTEX to the self-loop probability \(p_{\mathrm{stay}}\) used in label-persistence smoothing. This parameter controls the strength of span-level smoothing: larger values encourage neighboring tokens to remain in the same smoothing-label variable, whereas smaller values keep the smoothed scores closer to the raw token-level classifier outputs.

Figures 4 and 5 show the results for token-level and answer-level evaluation, respectively. The dashed horizontal lines indicate the raw scores before label-persistence smoothing. Across both datasets and all open-weight LLMs, label-persistence smoothing improves over the raw scores for a wide range of \(p_{\mathrm{stay}}\), indicating that the gains of CORTEX are not tied to a single finely tuned value.

For token-level detection, performance is generally stable when \(p_{\mathrm{stay}}\) is large. On both RAGTruth and HalluRAG, AP increases as \(p_{\mathrm{stay}}\) becomes larger and then forms a broad plateau around high values such as \(0.99\), \(0.993\), and \(0.995\). AUROC shows a similar trend, with improvements over the raw scores maintained across a wide range of high \(p_{\mathrm{stay}}\) values. This behavior is consistent with the role of label-persistence smoothing in token-level hallucination detection: hallucinated content typically appears as contiguous spans, and therefore stronger self-transition probabilities help suppress isolated noisy predictions while preserving coherent hallucinated regions.

For answer-level detection, the optimal \(p_{\mathrm{stay}}\) tends to be smaller than in token-level evaluation. This is because answer-level scores are obtained by aggregating token-level scores with the maximum operator. If \(p_{\mathrm{stay}}\) is too large, smoothing may overly spread high scores across neighboring tokens or make span boundaries too persistent, which can affect the maximum score used for answer-level classification. Nevertheless, label-persistence smoothing remains beneficial across a broad range of values, and the selected setting \(p_{\mathrm{stay}}=0.93\) provides strong and stable answer-level performance.

Based on these results, we use \(p_{\mathrm{stay}}=0.993\) for token-level evaluation and \(p_{\mathrm{stay}}=0.93\) for answer-level evaluation in the main experiments. We use a single value for each evaluation granularity rather than tuning \(p_{\mathrm{stay}}\) separately for each dataset and open-weight LLM. This setting keeps the evaluation protocol simple while still capturing the main benefit of label-persistence smoothing: converting locally noisy token-level scores into more span-consistent hallucination estimates.

Appendix C Experimental Details

MLP classifier.

For all methods that require a supervised classifier, including CORTEX and MLP-based baselines, we use the same three-layer MLP architecture to isolate the effect of the input features. The classifier consists of two hidden linear layers with 256 and 128 hidden units, respectively, followed by a final linear layer that produces a scalar output logit. Each hidden layer is followed by a ReLU activation and dropout with a rate of 0.1. We train the classifier using AdamW with a learning rate of \(1\times 10^{-3}\) and a weight decay of \(1\times 10^{-4}\). The batch size is set to 4096, and the model is trained for 10 epochs. The same hyperparameters are used across all datasets, models, and methods unless otherwise stated.

Representation extraction.

To obtain internal representations from the open-weight analysis model \(M_{\mathrm{open}}\), we do not perform autoregressive generation. Instead, we feed the constructed input sequence to \(M_{\mathrm{open}}\) and extract the internal representations computed in a single forward pass. This implementation matches the post-hoc setting considered in this work: the answer text has already been generated by the closed-weight model, and \(M_{\mathrm{open}}\) is used only to analyze the given answer.

Computational cost.

All experiments are conducted on a single NVIDIA A100 GPU. CORTEX is lightweight in practice: on RAGTruth, feature extraction, classifier training, and evaluation take approximately 20 minutes in total, while on HalluRAG they take approximately 5 minutes in total. This indicates that CORTEX incurs only modest computational overhead while providing token-level hallucination scores.

Artifact Licenses and Use.

We use RAGTruth and HalluRAG as existing public evaluation benchmarks and do not redistribute the datasets. RAGTruth is released under the MIT License. HalluRAG is made publicly available by its authors through their repository and dataset DOI, but we did not find an explicit dataset license in the available documentation. All datasets are used solely for research evaluation, and we cite their original sources.

Dataset Documentation.

We use only publicly available English-language RAG hallucination benchmarks and do not collect any new data. Our experiments focus on hallucination detection in generated RAG outputs; we do not use, infer, or analyze demographic attributes.

Appendix D Effect of Label-persistence Smoothing on Token-Level Baselines

Label-persistence smoothing is a post-processing module that can be applied to any method that produces token-level hallucination scores. To examine whether the gains of CORTEX are due only to label-persistence smoothing procedure to two strong token-level baselines, SAPLMA and RAGLens, and compare them with CORTEX under the same settings. Tables 5 and 6 report the results on RAGTruth and HalluRAG, respectively.

Before applying label-persistence smoothing, CORTEX achieves the best performance in all settings across both datasets and all open-weight LLMs. This result indicates that the comparative representation features of CORTEX already provide a stronger token-level signal than the single-view representation features used by the baselines. After label-persistence smoothing is applied, the performance of SAPLMA and RAGLens improves substantially, confirming that span-level post-processing is broadly useful for reducing local prediction noise. Nevertheless, CORTEX remains strongest in AP across all RAGTruth settings and remains competitive or superior in most HalluRAG settings. These results suggest that label-persistence smoothing is beneficial as a generic post-processing step.

In particular, the comparison before smoothing isolates the effect of the underlying token-level scoring function: CORTEX outperforms the baselines without relying on span-level post-processing. The comparison after smoothing further shows that CORTEX can benefit from the same generic smoothing procedure while retaining the advantage of its paired reference-conditioned and no-reference representation comparison. Thus, label-persistence smoothing and the comparative representation features play complementary roles: the former improves span consistency, whereas the latter provides a stronger reference-grounded hallucination signal.

Appendix E Additional Heatmap-Based Ablation Case Studies

We present additional heatmap-based case studies to qualitatively analyze the behavior of each component in CORTEX. The heatmaps compare the ground-truth hallucination spans with the predictions of the full CORTEX model, CORTEX without label-persistence smoothing, and CORTEX without the contextual residual \(c\). Darker colors indicate higher hallucination scores.

Figure 6 shows an example in which the annotated hallucination spans vary in granularity. The ground-truth annotation contains both a broad hallucinated region spanning multiple sentences and more compact hallucinated fragments. Without label-persistence smoothing, CORTEX assigns high scores at relatively fine-grained units. This behavior suggests that the raw token-level classifier can capture localized hallucination signals, but its predictions are fragmented and locally unstable. After label-persistence smoothing, these fragmented high-score regions are connected into a more coherent span, producing predictions that better reflect the span-level nature of hallucination annotations. At the same time, this example also illustrates a trade-off introduced by smoothing: when hallucinated evidence appears in several nearby but distinct regions, label-persistence smoothing may merge them into a broader continuous span. Thus, label-persistence smoothing improves span consistency, but may reduce boundary precision in cases where hallucinated content is interleaved with faithful tokens.

The same example also illustrates the role of the contextual residual \(c\). When \(c\) is removed, the model tends to assign high scores more broadly in regions where the current token is influenced by preceding generated context. This behavior is consistent with the motivation for the residual feature: \(\Delta h\) alone captures reference-induced changes at the current token, but it does not explicitly account for reference influence that has already been expressed through earlier answer tokens. By incorporating \(c\), CORTEX can distinguish direct token-level reference sensitivity from deviations relative to the preceding context, leading to more controlled localization.

Figure 7 shows a different type of error case in which the answer includes additional advice that is not supported by the provided references. The advice is informative and may be reasonable from the model’s parametric knowledge, but it is not grounded in the supplied passages. CORTEX assigns high hallucination scores to this region because its objective is to detect whether the answer is supported by the references, not whether the content is generally plausible or useful.

This case highlights an important ambiguity in reference-grounded hallucination detection. In controlled RAG applications, such as enterprise customer support, advice that is not grounded in references can be undesirable or risky even when it is factually plausible, because the system is expected to answer only from those documents. In such settings, flagging unsupported advice is a desirable behavior. In contrast, in open-ended assistant scenarios, suppressing all useful but reference-unsupported content may overly restrict the capabilities of the LLM. Therefore, the appropriate treatment of such content depends on the application: CORTEX should be interpreted as a detector of reference support, rather than a general judge of factual correctness or utility.

This example also clarifies the scope of CORTEX. Because the method compares internal representations under inputs with and without references, it is sensitive to whether a token is grounded in the provided evidence. Consequently, content generated from parametric knowledge alone can receive high hallucination scores if it is not supported by the references. This behavior is aligned with the intended design of CORTEX for reference-grounded generation, but it should be considered when applying the method to settings where answers are allowed to go beyond the retrieved references.
