---
title: "ChainCheck: Near-Perfect Evidence-Sufficiency Scores Can Conceal Sensitivity to Construction Artifacts Paired Conditional Contrasts that Expose an Evaluation Confound"
type: "raw-source"
url: "https://arxiv.org/html/2611.11965v1"
author: "Hyojung Han Affiliation ThakiCloud"
publication: "arXiv"
published: "2026-11-08"
archived: "2026-11-27T05:02:29Z"
---

> [!quote] Original source
> **Author(s):** Hyojung Han Affiliation ThakiCloud  
> **Title:** ChainCheck: Near-Perfect Evidence-Sufficiency Scores Can Conceal Sensitivity to Construction Artifacts Paired Conditional Contrasts that Expose an Evaluation Confound  
> **Published in:** arXiv  
> **Date:** 2026-11-08  
> **Original:** <https://arxiv.org/html/2611.11965v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-chaincheck-near-perfect-evidence-sufficiency-scores-can-conceal-sensitivity-to|Source note]]
Themes: [[Evals and agent quality]]
Why it was archived: How do you implement a union-level sufficiency gate for multi-hop retrieval, and what does multi-hop gold labeling cost?

## Archived text

ChainCheck: Near-Perfect Evidence-Sufficiency Scores

Can Conceal Sensitivity to Construction Artifacts

Paired Conditional Contrasts that Expose an Evaluation Confound

Abstract

Evidence-sufficiency benchmarks ask whether a model can tell a complete passage set from one whose reasoning chain is broken. When broken sets are made by editing text, near-perfect sufficiency scores—and even positive crossed-control scores—need not demonstrate multi-hop reasoning. We present ChainCheck, an evaluation-validity audit that pairs validator-certified counterfactual cells with artifact-only baselines. In an exploratory crossed control on 2,214 HotpotQA pairs, a language-model scorer that never reads the chain reaches a nominal AUC of 0.997, and a one-string match reaches the maximum of the crossed chain-sensitivity statistic CS4 (0.500), while the 11 evaluated systems score from 0.308 to 0.484; the two statistics are different metrics. We therefore read positive CS4 as operational bridge-consistency sensitivity, not as semantic multi-hop reasoning. Every system is also sensitive to one extra edit, and the edits are detectable according to model-based naturalness ratings. On an independent HotpotQA set of 2,276 pairs, patterns pre-specified on MuSiQue and 2WikiMultiHopQA did not replicate: 5 of 6 trained readouts were edit-dominated, and the reference judge’s selectivity interval [\(-\)0.007, +0.042] includes zero. Judge scores also depended on batch layout. The MuSiQue and 2Wiki records are public; the HotpotQA records and the fine-tuned checkpoints are not, so external reproduction is partial.

1 Introduction

How do we know that an evidence-sufficiency model detects broken reasoning chains rather than artifacts left behind when the benchmark was built? A sufficiency benchmark needs negatives: passage sets that look like the positives but lack a complete evidence chain. Every way of making them leaves a trace. Deleting a supporting passage lowers the query relevance of the set, so a surface classifier recovers the label. Substituting the bridge entity in a later hop keeps query overlap fixed, but it places an unexpected entity in a fluent passage, and a large language model can notice that the text was edited without following the chain at all. The ordinary score, a pair AUC of positive over negative, mixes these behaviours. Once several systems sit near the ceiling, it also leaves little headroom to order them.

Shortcut learning is well documented [7], and counterfactual evaluation of multi-hop reasoning is not new. ACCORD controls reasoning depth with multi-hop counterfactuals [23]; CRiT-QA and CofCA use counterfactual entities and chains to remove parametric knowledge and shallow shortcuts [31, 27]; SURE-RAG validates a sufficiency verifier under an artifact-aware protocol [21]; and Pair-ID audits how a generated answer responds to paired evidence interventions [5]. These works use counterfactual edits as a tool. ChainCheck asks whether the counterfactual edit itself becomes a new shortcut. Rather than proposing a harder benchmark, it reports, next to the ordinary score, a chain effect, an edit effect and chain selectivity, each a paired conditional contrast on pairs whose labels follow mechanically from validated provenance-preserving interventions. We position it as a protocol that exposes an evaluation confound: a positive selectivity says that a system’s response on these records is not explained by the edit trace alone, not that the system understands the chain.

The protocol grew out of a failure. We had pre-specified a comparison between a structured evidence readout and a single-layer probe on a provenance-built benchmark. The headline gate failed because the probe was already at the ceiling, and a matched-adaptation comparison against a one-token judge ended in a tie (Section 6.1). Controls added before the test read showed that much of the probe’s score was edit detection. ChainCheck formalises those controls into a protocol.

Contributions.

- 1. 

A validity problem for sufficiency scores. Near-ceiling nominal scores and positive crossed-control scores can both be reached without reading the chain. On the crossed HotpotQA arm the evaluated systems’ nominal AUC lies between 0.732 and 0.998, an artifact-only language-model scorer reaches 0.997, and a string-match reference reaches the CS4 maximum of 0.500 (Figure 1, Section 11.2). We separate three claims: sensitivity to bridge string consistency (supported), sensitivity to the edit trace (supported) and semantic multi-hop reasoning (not established by any measurement here).

- 2. 

An audit protocol, with its boundary. ChainCheck admits a pair only when a deterministic validator (checks Q1 to Q9) certifies every counterfactual cell, reports a chain effect, an edit effect and their difference as paired conditional contrasts, and adds a crossed control with artifact-only baselines (Sections 3 and 11.2). Its boundary is stated with it: a broken chain without any edit cannot be constructed, so the contrasts are conditional, not an additive decomposition, and CS4 measures operational chain sensitivity in the sense defined in Section 11.2.

- 3. 

Limits on generalization and reproduction. Patterns pre-specified on MuSiQue (Section 6.3) and tested on 2WikiMultiHopQA (Section 6.4) do not replicate on an independent HotpotQA set whose clustered intervals are informative (Section 11.1); record dependence limits the earlier sets (Section 7); judge scores depend on batch layout (Section 11.3); and the data and fine-tuned checkpoints are private, which bounds what outside researchers can reproduce (Section 12).

Status of the evidence.

Section 6.2 is exploratory: selectivity and its criterion were defined after the single read of the MuSiQue test split. Before scoring any confirmation pair we committed three hypotheses, their thresholds and the system list to a time-stamped internal decision record (not public) (Section 6.3), and before scoring any 2Wiki pair we fixed the replication patterns and the only permitted builder adaptations (Section 6.4). The headline wording of this paper was narrowed after the 2Wiki result; no criterion, number or system choice changed. Section 7 was added after every pre-specified result had been read; it changes no pre-specified verdict, and its informativeness rule was itself chosen post hoc. Section 11 was run after all of these results had been read; the tier of each of its analyses is stated there (Table 4).

2 Related work

Shortcuts and annotation artifacts.

Models often reach high benchmark scores through cues that the benchmark designers did not intend [7]. Hypothesis-only baselines in natural language inference reach well above chance [8, 19], models trained on that task adopt syntactic heuristics that fail on targeted evaluation sets [17], and reading-comprehension models answer many questions from the question or the passage alone [15]. ChainCheck addresses one artifact of this kind that is specific to sufficiency benchmarks: the trace that constructing a negative leaves in the text.

Shortcuts in multi-hop question answering.

HotpotQA introduced explainable multi-hop questions with supporting facts [29], and several analyses then showed that many of its questions can be answered with a single hop [18, 3]. Adversarial distractors [12] and transformations that expose disconnected reasoning [25] were proposed to close these shortcuts, and models that answer a multi-hop question correctly often fail its single-hop sub-questions [24]. Language models show a compositionality gap between answering sub-questions and composing them [20]. MuSiQue composes multi-hop questions from single-hop ones so that each hop is needed and records per-hop supporting paragraphs [26]; 2WikiMultiHopQA provides evidence triples for each reasoning path [10]. We use that provenance as the only source of labels.

Counterfactual and minimal-edit evaluation.

Contrast sets [6] and counterfactually augmented data [14] use minimal edits to probe or train decision boundaries. For multi-hop reasoning, ACCORD uses controlled multi-hop anti-factuals to separate commonsense grounding from reasoning and to vary reasoning complexity [23]; ACCORD controls what reasoning is required, whereas ChainCheck controls what construction artifact accompanies the reasoning intervention. CofCA builds step-wise counterfactual questions [27], and CRiT-QA replaces factual chains with counterfactual entities and adds distractor chains that diverge at different hops [31]. CRiT-QA uses counterfactual edits to remove shortcuts; ChainCheck measures whether the counterfactual edit itself becomes a shortcut. It adds a cell in which the edit is present but the label does not change, and reports the response to the chain and the response to the edit as separate quantities.

Knowledge conflicts.

Evidence sufficiency in retrieval-augmented generation.

SQuAD 2.0 made unanswerable questions a reading-comprehension construct [22], and sufficient context has been proposed as a lens on retrieval-augmented generation [13]. Benchmarks and analyses of retrieval-augmented generation test robustness to noisy, irrelevant or missing evidence [2, 4, 30], SURE-RAG treats evidence sufficiency as a set-level property and validates a proposed sufficiency verifier with counterfactual swaps, shortcut baselines and no-oracle checks [21]. ChainCheck asks a different question: whether the counterfactual construction itself creates a signal that can masquerade as sufficiency detection. It therefore adds an intact-chain edit control and measures chain and edit sensitivity separately for any evaluated scorer, rather than proposing a scorer. Pair-ID holds a query, retrieval state and reader fixed and crosses support addition with nonsupport deletion to audit how a failed answer responds to evidence repair [5]. Its crossed design resembles ours, but its object is the generated response; ChainCheck’s object is the evaluation itself, asking how much of a sufficiency score responds to the benchmark’s construction edit rather than to the broken chain. Pair-ID is a response audit; ChainCheck is an evaluation-confound audit.

Probes and judges.

Probing classifiers can report high accuracy for reasons unrelated to the property of interest, which control tasks were designed to expose [9]; our edit-only cell plays a similar role for sufficiency readouts. Language models are widely used as zero-shot judges [32]; here they are evaluated systems, not labelers. LLM safety evaluators shift their preferences with superficial artifacts such as apologetic phrasing, and agreement with human labels does not imply robustness to such artifacts [1]. ChainCheck makes the same point for evidence-sufficiency scorers, with a construction edit in place of a stylistic one.

3 The ChainCheck protocol

3.1 Counterfactual cells

Cells are indexed by chain status (alive, broken) and edit trace (absent, present). Three of the four cells are constructed; the design is therefore not a full factorial.

D replaces the bridge entity \(X\) with a different entity \(Y\) in the later-hop supporting passage only, so the earlier hop yields \(X\), the later hop speaks of \(Y\), and the chain is cut. B replaces \(X\) with \(Y\) in both the earlier and the later supporting passages, so the chain is intact but carries an edit trace. B and D share the later passage exactly and differ only in the earlier supporting passage. C, a broken chain without any edit, cannot be built without an intervention and is not used. Removing a hop is the nearest candidate, but it carries a different artifact (lower query relevance), so hop removal appears only as a diagnostic. Because C is missing, ChainCheck cannot estimate an interaction between chain status and edit trace, and the chain effect is measured in the presence of an edit.

3.2 Metrics

The primitive statistic is a within-record concordance probability over the \(n\) accepted records, \(\mathrm{AUC}(X>Y)=n^{-1}\sum_{i}\bigl[\mathbf{1}(s_{X_{i}}>s_{Y_{i}})+\tfrac{1}{2}\,\mathbf{1}(s_{X_{i}}=s_{Y_{i}})\bigr]\), which we call a pair AUC; it is invariant to score scale and calibration. CE, EE and \(\Sigma\) are contrasts derived from it, not AUCs themselves. They are paired conditional contrasts, not an additive decomposition: AUC is nonlinear and C is absent, so the nominal score is not the sum of the chain and edit effects. Each contrast is identified only conditionally: CE is the response to a broken chain given that an edit is present, and EE is the response to an edit given that the chain is alive. No interaction between chain status and edit trace is estimable from three cells, and we do not read CE and EE as components of the nominal score.

The chain effect CE is the B-versus-D response to breaking the chain under a shared later-passage edit; the edit effect EE is the response to an edit that leaves the chain alive; chain selectivity \(\Sigma\) is positive when chain sensitivity exceeds edit sensitivity. A system is chain-selective on a slice when the lower bound of the 95% pair-bootstrap interval of \(\Sigma\) is above zero. Intervals are 2,000-resample percentile bootstraps over accepted records. For trained systems, displayed point estimates are medians of three seed-level metrics, whereas the bootstrap resamples per-record outcomes averaged over the seeds; the intervals therefore target a seed-averaged statistic, are not uncertainty intervals for the displayed medians, and do not include training-seed variation. The chain-selectivity criterion and H1 were applied to this seed-averaged bootstrap. B edits two passages and D edits one, so for a scorer that responds only to the number of edited passages this asymmetry would push CE downward. No general bias direction follows for other scorers, because B and D may also differ in edit coherence, naturalness, or chain-correlated surface cues. The same mismatch cuts the other way for EE: A versus B compares an unedited set with a two-passage edit, so EE may exceed the edit effect of a single-passage edit, and \(|\text{EE}|\) enters \(\Sigma\) at that larger value. Neither contrast is edit-matched, so CE is not a chain-only effect. A follow-up edit-matched control confirms the predicted direction: matching raises CE for every system on MuSiQue, most for the trained readouts (Section 10).

3.3 Deterministic validator

A pair enters the counts only if nine checks pass: Q1 the query is identical across cells; Q2 passage positions are identical; Q3 untouched passages are byte-identical; Q4 the later passage is identical in B and D; Q5 the earlier-passage edit in B is exactly the \(X\) to \(Y\) replacement; Q6 \(X\) and \(Y\) are alias-disjoint; Q7 the answer-span count is identical; Q8 each passage’s query-lexical signature is identical across cells; Q9 the chain graph is alive in A and B and broken in D. Labels come only from dataset provenance and these checks. Our claim is restricted to programmatically verifiable provenance-preserving interventions: the benchmark labels follow mechanically from validated interventions, and human audit is not part of the protocol. The checks are string- and graph-level: they do not certify that an edited passage reads naturally or that the substituted entity is plausible in context, so any such cue counts as part of the edit trace rather than being removed.

3.4 Controls

(1) Closed-book separation: questions the reference backbone answers without passages, under a lenient string-containment rule, are excluded. This reduces but does not eliminate parametric bypass, and it does not establish closed-book hardness for the additional judge families. (2) Edit-only control: cell B, measured by EE. (3) Conditional chain contrast: B against D, measured by CE. (4) Synthetic entities: \(Y\) is a deterministic fictional name of matched token count and capitalisation, which reduces bridge-specific world-knowledge conflict in B and D. (5) Permutation invariance: passage order is shuffled and features are re-extracted from the language model, not just re-pooled. A diagnostic, construction transfer, scores systems trained on substitution against negatives built by hop removal or full removal.

4 Construction

MuSiQue.

We group examples by a hash of their sorted supporting document titles and split by group. The original MuSiQue split is not document-disjoint: of 12,304 train and 2,328 validation documents, 196 are shared, and only 1,424 of 2,417 validation examples (58.9%) are fully disjoint; we keep only those for test. An earlier build took the group identifier from the prefix of the example id, which encodes the hop count; that produced 120 groups and silently turned group-aware cross-validation into ordinary k-fold. The corrected definition gives 18,534 groups, at most 48 examples per group and 88.3% singletons, and re-measuring the surface gate moved it from 0.608 to 0.568.

Table 1 shows why the negatives are built by substitution: a surface-only classifier separates deletion-based negatives from the original set but not substitution-based ones. On all 463 test pairs the deltas of maximum and mean query Jaccard, answer presence and answer count are exactly zero; the BM25 maximum changes for 2.38% of pairs. A legacy eight-invariant builder gate, applied before the Q1–Q9 validator, decides which substitution candidates enter the benchmark; 6,196 of 6,944 train candidates (89.2%) and 463 of 504 validation candidates (91.9%) pass. It catches two corruptions that surface audits cannot see: a bridge that is part of the answer string, so that substitution also edits the answer (487 train candidates), and an intermediate passage that mentions the bridge and rebuilds the chain (172 train and 30 validation candidates). The primary arm has 4,925 train, 636 dev, 635 calibration and 463 test pairs.

On the test split, 338 of 463 real-entity candidates and 234 of 270 synthetic-entity candidates (the pairs admitted by the builder gate) pass Q1 to Q9, of which 324 and 224 are closed-book-hard. Every rejection was Q8 (125 real and 36 synthetic): the earlier-passage edit in B had changed that passage’s query-lexical signature. Kept, those pairs would have turned part of the A-versus-B difference into a query-relevance artifact, the confound the protocol exists to remove. Only the validator caught it.

MuSiQue confirmation.

The confirmation set takes MuSiQue validation examples that the test split excluded for sharing documents with training, built by the same builder, controls and validator (122 real and 98 synthetic closed-book-hard pairs). Because these examples share documents with the training split, confirmation rests on the untrained judge and on contrasts, not on absolute scores of trained systems; the hypothesis about trained systems (H1 below) is a within-distribution check rather than an independent confirmation.

2WikiMultiHopQA.

The only permitted changes were to the builder, and they were fixed before any score: the bridge is the object of the first evidence triple and the subject of the second; only compositional and inference questions are used; each set has 8 passages because 2Wiki gives ten per question; and at most 1,500 examples are drawn in a fixed seeded order. The validator rejected 185 candidates for Q8, leaving 295 real and 141 synthetic closed-book-hard pairs. Passages are rendered as a title followed by the body, and in every admitted 2Wiki example the later-hop passage title is the bridge entity, so the bridge substitution also rewrites that title prefix in B and D; MuSiQue passages carry titles too, but the later-hop title is not in general the bridge.

5 Systems evaluated

The eight primary systems use the same Qwen3.8-27B base checkpoint, with the passages packed into one prompt that ends in a decision token. M0 to M3 and the zero-shot judge keep the backbone frozen; M4-R and M4-J add matched rank-8 LoRA adapters. The systems are subjects of the evaluation; none is proposed here. M0 is a logistic probe on the decision token of the single layer that is best on dev (layer 36, dev pair AUC 0.993); M0-last uses the last layer. M1 mixes sixteen layers with a softmax gate. M2 pools per-passage representations with attention and a learned query, without cross-passage interaction. M3 lets the mixed decision token attend over the passage set without positional encoding. M4-R and M4-J spend the same rank-8 LoRA budget [11] (5,242,880 parameters on the full-attention layers) to feed a readout head or to score a one-token answer. The zero-shot judge is the backbone’s one-token yes/no probability, untrained. M0 to M3 are trained with binary cross-entropy and a pair hinge on primary substitution pairs only (A against D), early-stopped on dev, and reported as the median of three seeds. The M4 adapters train on 4,925 pairs. For 2Wiki, every trained system is the MuSiQue-trained model; nothing is retrained or recalibrated.

Additional judges.

Separately from the eight primary systems, we score four zero-shot judges from other model families on both evaluation sets, with the same prompt and score definition: Llama-3.1-8B-Instruct, phi-4, Qwen3-32B and Gemma-4-31B-it. They are not part of the primary ranking.

6 Results

6.1 The nominal ceiling

On the 447 closed-book-hard MuSiQue test pairs (the backbone answered 3.5% of the questions closed-book), the nominal pair AUC is 0.970 for M0, 0.990 for M3, 0.996 for both M4 systems and 0.893 for the zero-shot judge. The pre-specified gate requiring M3 to beat M0 by at least 0.05 failed (gain 0.022 [0.007, 0.038]), and the matched-adaptation comparison was a tie (difference 0.000 [\(-\)0.009, 0.009]). These ceiling-level values leave limited headroom, and we do not report inferential comparisons of the nominal ranks. We report these outcomes as the observation that motivated the protocol, not as contributions. This section reports the original pre-specified A-versus-D test on 447 closed-book-hard pairs. ChainCheck additionally requires a valid B cell and checks Q1 to Q9, which leaves 324 real-entity pairs for the sections that follow.

6.2 Exploratory contrasts on the MuSiQue test split

Table 8 and Figure 2 give the contrasts for every system on the 324 real-entity test pairs (224 synthetic). On the test split every system trained on A versus D treats the intact but edited chain B almost as a negative: edit effects lie between +0.312 and +0.441. The single-layer probe shows no chain sensitivity at all (chain effect \(-\)0.025 [\(-\)0.080, 0.031]), structured readouts and adaptation raise the chain effect, and the edit effect stays larger, so every trained system has negative selectivity. The zero-shot judge is the only chain-selective system, +0.210 [0.133, 0.287], while having the lowest nominal score, 0.889. With synthetic bridge names (Table 9) the judge’s edit effect falls to +0.000 [\(-\)0.067, 0.067], which is consistent with a contribution from bridge-specific world-knowledge conflict to its residual edit sensitivity, whereas the trained systems keep their edit effect. Selectivity and the chain-selectivity criterion were defined after this read, so this section motivates the hypotheses tested next and does not confirm them.

6.3 Sealed confirmation on MuSiQue

Three hypotheses were frozen before any confirmation pair was scored. H1: every trained system has an edit effect whose lower bound exceeds 0.25 and a selectivity whose upper bound is below zero. H2: the reference zero-shot judge has a selectivity lower bound above zero on both the real and the synthetic slice. H3: the judge’s edit effect is larger on real than on synthetic entities. H1 and H2 met their pre-specified criteria. H3 had the pre-specified direction, but its independent-slice bootstrap ignores shared source questions and documents; we report H3 descriptively and do not assign it a confirmatory pass/fail interpretation. H1 concerns trained systems scored on documents shared with their training split; it is a within-distribution check, not an independent confirmation.

On real entities (122 pairs; 98 synthetic), the lower bounds of the trained systems’ edit effects lie between 0.361 and 0.475, and every trained selectivity interval lies below zero. The reference judge’s selectivity is +0.139 [0.025, 0.262] on real and +0.429 [0.337, 0.469] on synthetic entities; the margin on real entities is thin. Its edit effect is 0.219 [0.092, 0.344] lower on the synthetic slice than on the real slice. The interval is the difference of independent bootstraps of two separately validated slices whose membership differs (122 and 98 pairs), so the difference is consistent with, but not identified as, a contribution from bridge-specific world-knowledge conflict to its residual edit sensitivity.

One exploratory observation does not carry over. On the test split the judge had the lowest nominal score; on the confirmation set it ranks 3 of 8 by nominal score and 1 by selectivity. What holds is that nominal scores lie between 0.902 and 1.000 on real entities and leave little headroom, while the selectivity point estimates order them differently, with overlapping intervals.

Other judge families.

Following a rule fixed before their scores were seen, every additional judge is reported on both datasets (Tables 10 and 11). On the MuSiQue confirmation set, 1 of the 4 additional judges meet the H2 criterion on both slices: Gemma-4-31B-it is chain-selective, while phi-4 is edit-dominated on real entities, with selectivity \(-\)0.205 [\(-\)0.336, \(-\)0.066]. On 2Wiki all 4 of 4 meet it, phi-4 included (+0.156 [0.078, 0.237] on real entities). The pre-specified reference judge replicates, while selectivity varies across judge families and datasets. Being untrained on the nominal contrast is therefore not by itself what makes a system chain-selective, which is what one expects if the two contrasts are separable.

6.4 External replication on 2WikiMultiHopQA

The replication was run because H1 and H2 passed, as pre-specified, and was required to reproduce four patterns rather than absolute numbers. Three replicate on the 295 real-entity pairs (141 synthetic). Nominal scores lie between 0.905 and 1.000, and the judge ranks 8 of 8 (last) by nominal score on both slices. Its selectivity is positive, +0.163 [0.085, 0.234] on real and +0.383 [0.284, 0.447] on synthetic entities, and it ranks 1 by the point estimate of selectivity, so the two rankings differ (Figure 4). The rank is a point estimate: the judge’s interval overlaps those of M0-last, M1, M3 and M2, and the judge and M0-last are nearly tied, so the ordering at the top is not established by these data.

The fourth pattern, the H1 criterion, fails. Trained readouts keep large edit effects (lower bounds above 0.25 on real entities, with one exception on synthetic entities, where the lower bound of M1 is 0.207), but on 2Wiki they also show large chain effects, between +0.303 and +0.466 on real entities, and 5 of the 6 systems covered by H1 (every trained system except M0-last) have positive point estimates of selectivity. Edit sensitivity replicates; edit dominance does not. The same MuSiQue-trained readouts that were edit-dominated on MuSiQue show much stronger chain sensitivity on 2Wiki. We do not know why. One of several possible explanations is surface leakage through the title: the 2Wiki later-hop passage is titled with the bridge entity (Section 4), so in D the earlier passage names \(X\) while the later title names \(Y\), a mismatch visible without following the chain. Entity-linking noise and the shift to eight-passage sets and 2Wiki question types are other candidates. A follow-up title-masking control finds the title to be a small cue for the readouts and not detectably one for the judge; the other candidates are untested (Section 10).

6.5 Order and construction diagnostics

Table 2 collects both diagnostics on the MuSiQue test split.

Under re-extraction with shuffled passage order the single-vector probes fail the pre-specified jitter criterion, and the set models, the adapted systems and the zero-shot judge pass. The backbone is causal, so set models are not order-invariant by construction; this control has to be measured on re-extracted features. Construction transfer does not track selectivity: M1 has negative selectivity on MuSiQue but the highest hop-removal transfer among trained systems. Hop removal also has a high surface ceiling (Table 1), so transfer there may reflect query-relevance cues, and we treat this axis as a diagnostic only.

7 Post-hoc robustness analysis

Nothing in this section was pre-specified. It reuses the frozen models, scores and pairs, uses \(B=10000\) resamples with a fixed seed, and changes no number or verdict reported above. We report it because it determines how far the pre-specified results generalise.

Reproduction.

Recomputing the MuSiQue confirmation metrics from the frozen features failed our strict reproduction gate. The nominal score of M0 came out as 0.918 against the ledger value 0.934. M0 produces 10 exact A/D score ties, and 14 of its pairs have bit-identical scores. A single-threaded BLAS rerun returns the ledger value (0.934) but changes the order of 4 pairs; we do not assert a cause. Under a post-hoc rule that excludes the nominal score, the reproduction is partial: the chain effect, the edit effect, selectivity and the verdicts derived from them reproduce. The MuSiQue nominal values in this paper are therefore ledger values from the original run and are sensitive to ties; the conditional contrasts, which carry the claims, are not affected. The 2Wiki recomputation passed the gate.

Bootstrap design.

The pre-specified intervals resample pairs independently within each slice. Pairs built from the same source question or sharing documents are not independent. We group records into connected components of shared documents and resample whole groups, jointly across the real and synthetic slices, taking the median over the system’s scoring seeds within each resample; a coarser grouping by passage title gives a second variant. The re-implemented unclustered bootstrap used as the reference for these comparisons is not byte-identical to the pre-specified one: for the judge on real entities it gives [0.016, 0.262] on MuSiQue and [0.088, 0.237] on 2Wiki, against the pre-specified [0.025, 0.262] and [0.085, 0.234]. Verdicts use the pre-specified intervals.

The effective-sample problem.

A clustered interval is informative only if the groups are many and balanced. With group sizes \(n_{g}\), we use the effective number of groups \(K_{\mathrm{eff}}=(\sum_{g}n_{g})^{2}/\sum_{g}n_{g}^{2}\) and call a clustered interval informative when the largest group holds at most half the records, \(K_{\mathrm{eff}}\geq 20\), and each slice has at least 20 groups. Only the largest-group rule existed before the first clustered run; the other two were added afterwards. The MuSiQue confirmation records form 52 document groups (220 records, largest group 18.2%), with \(K_{\mathrm{eff}}=18.22\); grouping by title gives \(K_{\mathrm{eff}}=2.03\). The 2Wiki records form 30 groups (436 records), the largest holding 76.1% of them. Neither dataset yields an informative clustered interval.

How we read it.

We apply three rules. First, the pre-specified pair-bootstrap verdicts stand as reported; a post-hoc analysis does not turn them into failures. Second, the \(K_{\mathrm{eff}}\) rule is post hoc, so we do not use it to rescue H2 either: we do not claim that H2 survives clustering. Third, an uninformative clustered interval is not a refutation. On MuSiQue the clustered interval for the judge’s selectivity on real entities is [\(-\)0.089, 0.341] and includes zero, while on synthetic entities it is [0.216, 0.468]; on 2Wiki the corresponding intervals are [0.054, 0.255] and [0.206, 0.411]. None of these is decisive, in either direction. H2 therefore holds as a pre-specified criterion met on these records; it cannot be read as general confirmation that the judge is chain-selective.

The H1 and H3 results are a separate matter from informativeness. On MuSiQue, H1 holds under the pair bootstrap and under both groupings, but it remains a within-distribution check on documents shared with training. The judge’s real-minus-synthetic edit-effect difference (H3) is 0.219 [0.095, 0.347] under document clustering on MuSiQue and 0.118 [0.068, 0.260] on 2Wiki; because the two slices differ in membership, H3 stays exploratory. Finally, the judge ranks first by point-estimate selectivity on both datasets, but the rank means different things. On 2Wiki it rests on a difference from M0-last of +0.003 [\(-\)0.083, 0.091] under the pair bootstrap, a near-tie; on MuSiQue the same difference is +0.590 [0.443, 0.738], against a readout that is edit-dominated there. Which system ranks first, and by how much, is a dataset-specific point estimate rather than a general ordering.

8 Discussion

Two contrasts.

High edit sensitivity does not imply the absence of a positive conditional chain contrast. On MuSiQue the trained readouts are edit-dominated; on 2Wiki the same MuSiQue-trained readouts are both edit- and chain-sensitive. An ordinary score mixes the two, and so does any benchmark that reports nominal accuracy alone. One hypothesis for the dataset dependence is that the 2Wiki later-hop passage is titled with the bridge entity, so the substitution also changes the passage title and makes the break visible at the surface; a pre-specified follow-up title-masking control tested it: the observed shift is a few hundredths of AUC for the trained readouts and not detectable for the judge at the record level; because its verdict is inconclusive under document dependence, this does not rule out title-related explanations beyond these records (Section 10).

Construction and dependence as findings.

Two results of this study are about the protocol rather than about any system. First, on the document-dependent MuSiQue confirmation records, the edit-matched control changes the point estimate of M0’s chain contrast from negative to positive. This shows construction sensitivity on these records; because the verdict is INCONCLUSIVE_DEPENDENCE, its generality is unresolved, and a sign read from one construction should not be taken as a property of the system alone. Second, the reliability of every comparison here is bounded by document dependence, not by the number of records or systems: 2Wiki has fewer than two effective document groups in every slice, and only one MuSiQue slice reaches the informativeness threshold. Both belong in the report of any edited sufficiency benchmark.

Judge families and datasets.

The additional judges argue against a simple reading in which zero-shot judges are inherently better at following evidence chains. Only 1 of 4 is chain-selective on the MuSiQue confirmation set, yet all 4 of 4 are on 2Wiki. Chain and edit sensitivity vary with the system family and with the dataset, and the nominal score shows neither.

Lessons for benchmark builders.

Ship an edit-only cell with any construction that edits text; without it, a score near the ceiling cannot be attributed to chain following, and it cannot be dismissed as an artifact either. Match the amount of editing between the control and treatment cells; where that is not possible, as here, state which direction the mismatch biases each contrast. Validate every cell in code, including the control cells: our own consistent swap broke query-lexical neutrality in 125 of 463 real-entity test candidates. Use synthetic entities before reading a residual edit effect as a weakness. Group splits by document, and check that the group key means what you think it does. Record the batch layout of every scoring run, and keep it fixed when cells scored in different runs are compared.

9 Limitations

- 1. 

Evidence tiers. Section 6.2 is exploratory. The confirmation pairs come from the same source dataset and share documents with training, so confirmation rests on the untrained judge and on contrasts. The 2Wiki replication reproduced three of four patterns; edit dominance of trained readouts is not part of our claim. Section 11 adds one confirmatory result, which is a non-replication, one exploratory result and one indicative result; the eligibility rule of its confirmation set was revised after a manifest check and before any score.

- 2. 

Thin margin and dependence. H2 passed on MuSiQue real entities with a lower bound of 0.025. Records share documents, and too few independent document groups exist for an informative clustered interval on either dataset (Section 7), so H2 is not general confirmation of chain selectivity. On the independent HotpotQA set, where clustered intervals are informative, the H2-type pattern did not replicate (Section 11.1).

- 3. 

Rank stability and multiple comparisons. Rankings are point-estimate ranks of eight systems whose selectivity intervals overlap, and only three hypotheses were pre-specified; every other contrast across systems, slices and judge families is reported without correction for their number. Intervals are pair bootstraps; pairs built from the same source question or sharing documents are not independent. A post-hoc cluster bootstrap over document groups widens the intervals and is not informative on these data (Section 7).

- 4. 

Partial reproduction. Recomputed from frozen features, the MuSiQue conditional contrasts and their verdicts reproduce, but the MuSiQue nominal score of M0 is numerically unstable under recomputation (0.918 against the ledger value 0.934) in a case with many exact score ties; the cause is unresolved, and the nominal rank of M0 inherits this instability (Section 7).

- 5. 

Partial synthetic control. Only the bridge entity is renamed; other entities keep their real names.

- 6. 

Scope. One backbone (Qwen3.8-27B), one language (English), three source datasets (HotpotQA only in Section 11). All eight primary systems share that checkpoint, so the rank contrast is a within-backbone result; the additional judges come from other families but are untrained, so no cross-backbone comparison of trained readouts exists. 2Wiki carries entity-linking noise (a later-hop page may describe a namesake); labels still follow from provenance, but such passages are less natural.

- 7. 

Missing cell. C is not constructed, so no cell isolates a broken chain without an edit; CE and EE are conditional contrasts, no interaction is estimable, and B and D differ in the number of edited passages (two versus one). The crossed control of Section 11.2 cancels additive per-passage effects but does not construct C either.

- 8. 

Validator scope. Q1 to Q9 certify string- and graph-level properties. They do not certify the naturalness or semantic plausibility of an edited passage, and no human or blinded model audit of the edited text was run, so a system may be reacting to unnatural text rather than to an edit as such; the protocol counts both as edit trace.

- 9. 

Selection of independent groups. A confirmation set built only from records that share no document, question or group with each other or with any earlier split removes frequently reused documents. Independence then comes at the cost of representativeness: the retained items may differ in distribution from the source datasets, so results on such a set describe that set, not the full benchmark population. A first attempt under a separately fixed eligibility protocol produced no slice that met its minimum independent-sample threshold and contributes no result. The HotpotQA set of Section 11.1 meets the threshold only after a post-manifest amendment of its eligibility rule and comes from the training split of one source dataset, so its non-replication describes that set.

- 10. 

Batch layout. Judge scores depend on how records are packed into batches (Section 11.3). Our results are reproducible under the recorded layouts, not invariant to batching, and the cause of the largest single-record shift is unexplained.

- 11. 

Closed-book filter. The rule is lenient string containment; residual parametric leakage is not ruled out, and the filter uses the reference backbone only.

10 Pre-specified follow-up controls

Status.

The two controls below were designed after the original MuSiQue and 2Wiki results had been seen. Their samples, statistics and decision rules were fixed in an internal record before any of their scores existed, and auxiliary analyses were added to that record, again before any score was read, without changing a decision rule. They are pre-specified follow-up controls, not a preregistration of the study. They test two alternative explanations of the judge’s selectivity; neither is meant to make H2 pass. All four verdicts (two controls, two datasets) are INCONCLUSIVE_DEPENDENCE under the dependence rule of Section 7, which is what the group structure predicted before any score: on MuSiQue the synthetic slice and the joint comparison have fewer than 20 effective clusters, and on 2Wiki one document group carries most records in every slice (Table 3). We therefore report effect sizes rather than verdicts: the direction, the point change, a record-level interval and a cluster interval, with the effective cluster count. The primary comparison is with the original scores on the same records: one paired bootstrap (10000 resamples) draws each record’s original and controlled cells together, so the change has its own interval. Results on the full original hard set are reported in the analysis output as auxiliary only. Intervals on 2Wiki rest on fewer than two effective groups and should be read that way.

Control 1: edit matching.

The new cell \(D^{\prime}\) edits the earlier passage as well (\(X\to Z\)). On 2Wiki real, \(D^{\prime}\) could not be built for every pair because no second substitute entity \(Z\) was available for some of them, so this control uses 287 of the 295 real pairs; the MuSiQue slices and the 2Wiki synthetic slice keep every pair. The control scores six systems: the judge, M0, M0-last, M1, M2 and M3. With \(D^{\prime}\), the chain contrast \(\text{CE}_{m}=\mathrm{AUC}(B>D^{\prime})-0.5\) compares two edited passages with two. The asymmetry predicted in Section 3 is visible: for a scorer that counts edits, the original CE should rise once edits are matched. It rises for every system on MuSiQue and falls for none on 2Wiki. For the judge the change on MuSiQue is +0.107 on the real slice (record interval [+0.033, +0.180], cluster [+0.025, +0.214]) and +0.041 on the synthetic slice ([+0.010, +0.082]; cluster [+0.000, +0.094]); on 2Wiki it is +0.129 (real, [+0.087, +0.171]; cluster [\(-\)0.020, +0.177]) and +0.014 (synthetic, [\(-\)0.021, +0.050]). The edit-dominated readout M0 moves far more on MuSiQue: its CE goes from \(-\)0.205 to +0.180 on the real slice and from \(-\)0.276 to +0.306 on the synthetic slice, a reversal of sign on both slices. This is the largest change either control produced. It shows that the negative chain contrasts of the trained readouts on MuSiQue are highly sensitive to the edit-matching intervention; it does not yet show that the edit-count asymmetry alone caused them, because matching the edit count also edits a second passage and may change its coherence, naturalness or other surface cues. The automated artifact-detectability audit below is designed to separate these in part, and the reversal has so far been observed only on the document groups of this confirmation set.

The point estimate of \(\Sigma\) remains positive after matching in all four analyzed slices. The judge’s \(\Sigma_{m}\) stays positive: +0.246 on MuSiQue real (record [+0.147, +0.344], cluster [+0.082, +0.393]), the one slice whose clustered interval is informative, and +0.480, +0.289 and +0.418 elsewhere, with every record and cluster lower bound above zero. On the MuSiQue real slice every trained readout stays edit-dominated, with record intervals below zero; M0 has \(\Sigma_{m}\) of \(-\)0.279 (real, cluster [\(-\)0.358, \(-\)0.190]) and \(-\)0.173 (synthetic, cluster [\(-\)0.259, \(-\)0.056]), down from \(-\)0.656 and \(-\)0.745. On the synthetic slice two of the five readouts no longer separate from zero, and on 2Wiki M0’s near-zero \(\Sigma\) turns slightly positive (\(-\)0.084 to +0.066, cluster [\(-\)0.053, +0.109]). Edit matching therefore changes the size of both contrasts, by a lot for the readouts, and moves readouts that were close to the boundary. Only the MuSiQue real slice has an informative clustered interval, and every control verdict is INCONCLUSIVE_DEPENDENCE, so these estimates do not establish that the judge’s chain selectivity or the readouts’ edit dominance is unchanged. The judge ranks first by \(\Sigma\) before and after matching in every slice; the rank correlation of these six systems between \(\Sigma\) and \(\Sigma_{m}\) is 0.657 (MuSiQue real), 0.829 (MuSiQue synthetic), 1.000 (2Wiki real) and 0.943 (2Wiki synthetic). One asymmetry remains by construction: \(B\) introduces one new entity and \(D^{\prime}\) two.

Control 2: title masking.

Every passage title in every cell was replaced by a neutral placeholder, and an unmasked copy of the same cells was scored in the same run. Records whose bridge entity no longer appears in any passage body after masking were excluded, as specified: 2Wiki keeps 278 of 295 real and 140 of 141 synthetic records, MuSiQue 118 of 122 and 97 of 98. The masking changed what it was meant to change and little else. On 2Wiki the bridge entity named the earlier-hop title in 100.0% of real \(A\) cells and the substituted entity named the later-hop title in 100.0% of real \(D\) cells; after masking both are 0.0%, while the bridge entity stays in the \(D\) body in 100.0% of records. Length fell by the same small amount in every cell, from 784 to 760 tokens for the real \(D\) cell on 2Wiki and from 1,261 to 1,238 on MuSiQue, and the passage count, order and body text are unchanged by construction. MuSiQue is a weaker negative control than intended: its earlier-hop title names the bridge entity in 20.3% of real \(A\) cells.

Masking leaves the judge’s chain contrast on 2Wiki almost unchanged: \(\Delta_{\text{mask}}=\text{CE}_{M}-\text{CE}_{U}\) is \(-\)0.018 on the real slice (record [\(-\)0.054, +0.022], cluster [\(-\)0.042, +0.078]) and \(-\)0.014 on the synthetic slice ([\(-\)0.057, +0.029]; cluster [\(-\)0.127, +0.080]). Both record intervals lie inside the pre-specified equivalence margin of \(\pm\)0.1 AUC; the synthetic cluster interval does not, and no 2Wiki cluster interval is informative. Against the original scores on the same records the masked CE differs by \(-\)0.018 (real, [\(-\)0.058, +0.022]) and +0.000 (synthetic, [\(-\)0.043, +0.043]), and the judge’s \(\Sigma_{M}\) stays at +0.180 and +0.393 with record and cluster lower bounds above zero. On MuSiQue the judge moves by a similar amount, \(-\)0.025 (real) and \(-\)0.031 (synthetic), so the pre-specified reading that 2Wiki should move more than the negative control does not hold for the judge. That small shifts of this size are within run-to-run variation is suggested by the unmasked rebuild itself: on MuSiQue real its CE is +0.356 against +0.339 for the original cells.

The trained readouts behave differently. On 2Wiki real, masking lowers CE for every readout, by \(-\)0.061 for M0 (record [\(-\)0.095, \(-\)0.029]) and \(-\)0.045 for M3 ([\(-\)0.072, \(-\)0.014]), whereas on MuSiQue the same readouts show no consistent direction (M0 +0.009, M3 +0.072). The title is a measurable but small channel for the readouts on 2Wiki: it explains a few hundredths of AUC, not their large 2Wiki chain contrasts. System ranks by \(\Sigma\) are nearly unchanged by masking (rank correlation with the original 1.000 on 2Wiki real and 1.000 on 2Wiki synthetic); the judge is first after masking in every slice, and second only in the unmasked 2Wiki real rebuild.

What the controls change.

Neither control returns a decisive verdict, and neither is used to change H1, H2 or H3. Read as effect sizes they narrow the explanations. The edit-count asymmetry is a construction variable that moves every system’s chain contrast in the predicted direction and moves the trained readouts most, but it does not create the judge’s positive \(\Sigma\) and does not remove the readouts’ edit dominance on the MuSiQue real slice; readouts near the boundary move across it. Masking the bridge entity in the 2Wiki title moves the trained readouts by a few hundredths and has no detectable record-level effect on the judge; because the verdict is inconclusive, this does not rule out title-related explanations of the large 2Wiki chain contrasts. The dataset dependence of trained-readout edit dominance—the H1 pattern that failed on 2Wiki—remains unexplained. The shift in set size and question type between the two datasets is the first untested candidate we would examine, with entity-linking noise as another; neither has been tested.

Open controls.

Two of the controls planned at this point have since been run (Section 11): a confirmation set of independent document groups and, within the crossed control, an artifact-only edit detector cross-fitted over document groups together with model-based naturalness ratings by judges outside the backbone family. These do not establish human-validated semantic plausibility, and detectability does not show that a system used the cue. Still unrun is a trained readout on a second backbone, which would show whether the within-backbone rank contrast is specific to this checkpoint; scored on the same dependent records it would not narrow the clustered intervals, so it belongs on independent sets.

11 Independent confirmation and a crossed edit-trace control

Status and evidence tiers.

The analyses in this section were run after every result above had been read, to address the limitation that ends Section 7: no earlier slice had enough independent document groups for an informative clustered interval. Each was fixed in an internal record before its scores existed; none is a public preregistration, and none changes H1, H2, H3 or any verdict above. The four results carry different weight, and we report them at the tier at which they were designed (Table 4).

11.1 HotpotQA independent confirmation

Design.

We built the same A/B/D/D′ cells from the HotpotQA training split, which none of the systems saw in training or selection. Every record was checked against every training, selection, control and synthetic manifest used earlier (question identifiers, normalised gold-passage titles and passage-body hashes). The first check failed on gold-title overlap, and the set was stopped. A revised eligibility rule—drop every pair any of whose gold passages shares a normalised title with a passage of those manifests—was then fixed after seeing that check and before any system score, and is reported as a post-manifest amendment, not as the original design. It kept 2,453 of 2,650 real-entity pairs, all of which passed the full check again; the closed-book filter of Section 4 left 2,276 pairs. Under the document-group clustering of Section 7 every pair is its own group (\(K_{\mathrm{eff}}=2,276\)), so, unlike every earlier slice, clustered and pair intervals coincide and are informative. Systems, checkpoints, prompts, metrics and the thresholds of H1 and H2 are those of Section 6.3, applied without retraining; the trained readouts and LoRA systems were trained on MuSiQue, so this is also a cross-dataset test for them. Synthetic-entity pairs were scored as a diagnostic only.

Result.

Neither pattern replicated (Table 5). The H1-type pattern (edit effect lower bound above 0.25 and selectivity upper bound below zero for every trained system) held for 5 of the 6 trained systems; M1 is not edit-dominated (selectivity upper bound +0.022). The H2-type pattern failed for the reference judge, whose selectivity lower bound is \(-\)0.007. Of the 4 additional judges, 3 have a selectivity interval above zero and phi-4 does not (lower bound \(-\)0.057). This is the only set in this study on which the dependence rule allows a decisive clustered verdict, and on it the pre-specified pattern does not hold. We therefore do not read the MuSiQue and 2Wiki passes of H2 as transferring to an independent sample. With the edit-matched cell \(D^{\prime}\) in place of \(D\), the trained readouts’ \(\Sigma_{m}\) lies between \(-\)0.019 and +0.125, so on these records much of their negative selectivity tracks the unequal number of edited passages, as on MuSiQue (Section 10).

11.2 Crossed edit-trace control

Design.

The ordinary contrasts compare cells that differ in both chain status and edit trace. The crossed control removes additive per-passage effects. Write \(e\) for the earlier supporting passage, which mentions the bridge entity \(X\), and \(l\) for the later passage, titled \(X\). Cell \((u,v)\) replaces \(X\) by \(u\) in \(e\) and by \(v\) in \(l\); the chain is intact only when \(u=v\). With a second substitute \(Z\) chosen by the same rule as \(Y\), the four cells \(B=(Y,Y)\), \(B_{Z}=(Z,Z)\), \(D_{ZY}=(Z,Y)\) and \(D_{YZ}=(Y,Z)\) use the same four edited passage versions, each once in an intact and once in a broken cell. The main estimand is

where \(W\) is the paired win rate with ties counted as one half. Each of the four pairs differs in one passage, so any scorer that adds per-passage scores, whatever those scores reflect (entity identity, edit trace or counterfactuality), has CS4 \(=0\). Two secondary contrasts isolate the edit trace: the edit-count effect \(\text{EC}=W(D>D_{ZY})-0.5\) compares two broken cells that share \(l\) and differ only in whether \(e\) is also edited, and the position effect \(\text{PT}=W(D_{E}>D)-0.5\), with \(D_{E}=(Y,X)\), compares editing \(e\) with editing and retitling \(l\). Arm E uses the crossed-eligible HotpotQA confirmation pairs (2,214 after the same closed-book filter); because their original cells had been scored, it is exploratory by design. Two unseen holdouts, HotpotQA validation (C1) and 2WikiMultiHopQA train (C2), were checked against all earlier sets; after that check they hold 50 and 231 pairs, below the pre-specified size for any verdict, and serve only as a direction check. Verdicts use document-group bootstrap intervals, Bonferroni-adjusted for the 11 systems in the family; each statistic (CS4, EC, PT) is corrected separately, and the artifact-only baselines below are outside the family. A system is called chain-sensitive (code label CHAIN_SENSITIVE) when the adjusted lower bound of its CS4 is above zero. The label is operational: it means sensitivity to bridge-string consistency, not semantic multi-hop reasoning. Four artifact-only baselines that never see the chain are reported beside them: three additive scorers (surface form, a cross-fitted character n-gram edit detector, and per-passage language-model log-probability from Llama-3.1-8B-Instruct) and a string-match reference (AB3) that scores whether the bridge string in \(e\) equals the title of \(l\).

Result.

All 11 systems are chain-sensitive in this operational sense under the adjusted rule: CS4 ranges from 0.308 to 0.484, every adjusted lower bound is at least 0.290, and the five judges no longer disagree in verdict (Table 6). The additive baselines have CS4 \(=0\) exactly, as the estimand requires, which the analysis also checks as a validity gate. In both holdouts the sign of CS4 agrees with arm E for 11 and 11 of the 11 systems. The edit trace does not disappear. Every system also shows an edit-count effect (EC adjusted lower bound above zero for 11 of 11), and 10 of 11 show a position effect, all except M4-R. The artifact-only language-model baseline reaches a nominal score of 0.997 without reading the chain, so on these records the ordinary score is available from edit traces alone. This does not contradict Table 1, where a surface-only classifier stays at 0.568 on substitution negatives: that classifier sees query-overlap and retrieval features, which substitution leaves unchanged, whereas AB2 scores each passage with a language model and so sees the edit itself. The sets and detectors differ, so the two numbers are not directly comparable. Edits are detectable according to model-based naturalness ratings: three non-Qwen judges, asked blind whether a single passage reads naturally, rate an edited later passage lower than its original (Gemma-4-31B-it by \(-\)0.604, Llama-3.1-8B-Instruct by \(-\)0.499, phi-4 by \(-\)0.536 in mean P(yes)), while the \(Y\) and \(Z\) versions are rated alike (largest absolute difference 0.011), which supports the exchangeability that CS4 assumes. These ratings are supplementary evidence, not human validation.

Reading.

CS4 measures sensitivity to whether the two passages name the same bridge entity once additive per-passage effects cancel. AB3 reaches the maximum, 0.5, by checking one string, so a positive CS4 is evidence of sensitivity to the consistency of the linking string, not of multi-hop reasoning. We separate three claims. Sensitivity to bridge-string consistency is supported, and so is sensitivity to the edit trace; semantic multi-hop reasoning is not established by this control. The control therefore shows both kinds of sensitivity together in every system. It does not remove the edit confound: the edit-count effect remains, the edited passages remain detectable, and the C cell (a broken chain without any edit) still does not exist, so non-additive reactions such as a response to the same unfamiliar entity appearing twice are not separated from chain consistency. Nor does it reverse the HotpotQA non-replication above: CS4 is a different estimand from \(\Sigma\), the arm is exploratory, and the holdouts are indicative.

11.3 Batch-layout sensitivity of the scoring pipeline

What failed.

The pre-specified analysis checks that old cells rescored inside the crossed bench reproduce their earlier scores (minimum per-cell Spearman correlation at least 0.999 and \(|\Delta W(A>D)|\) at most 0.005). The first run failed this check for one judge, Gemma-4-31B-it (minimum Spearman 0.990383), so the analysis stopped as invalid before any new-cell score was read; that record is kept. Scoring sorts records by length and packs them into batches of at most 8,192 tokens, so adding the new records changed the batches of the old ones. A diagnostic fixed before it ran showed that identical layouts reproduce exactly in repeated runs (Spearman 1, \(\Delta W=0\)) and that a changed layout alone changes scores. On the 8,856 affected records, 82.7% of scores are bit-identical, the A\(>\)D outcome flips in 17 of 2,214 pairs (0.77%), all of them with score gaps below \(10^{-3}\), and one record moves by 0.992. Large shifts of this kind are unexplained; we do not attribute them to numerical rounding.

Recovery.

As fixed in the diagnostic record, we rescored the judge with the original layout: the 15,452 records of the original bench as one run, and the 12,024 crossed records outside it as a second bench, then merged by record identifier. The crossed set has 21,576 unique records, 9,552 of which are in the original bench; the 5,900 original records outside the crossed set (4,890 synthetic-entity variants, 880 records of pairs that were not crossed-eligible and 130 others) were not used, and no record was selected by position or deduplicated. The merged scores match the crossed set exactly in identifiers and order, the original-bench run reproduces the committed scores byte for byte, and the rerun passed every validity gate (Gemma minimum Spearman 1.0). This pass shows reproducibility under the recovery layout. It does not show that the judges are invariant to batching: the other judges’ old-cell scores also moved between layouts by amounts within the threshold (minimum Spearman 0.999504, \(|\Delta W|\) up to 0.00271). Rankings and win rates near ties can depend on a scoring detail that papers rarely report.

12 Data, code and checkpoint availability

Every measured result in this paper is a macro generated from an experiment ledger field, and tables and figures are generated from the same ledgers. Not all of those ledgers, records and checkpoints are public, so external reproduction is partial. We state the boundary explicitly.

Public.

The assets in Table 7 are public. The ChainCheck dataset contains the MuSiQue test and sealed-confirmation records and the 2WikiMultiHopQA replication records, together with a standalone evaluator (chaincheck_eval.py) that recomputes the paired contrasts from a score file. The three released judges come from a separate release training run and are not the M4-R or M4-J checkpoints evaluated here; results for M4 in this paper should not be expected from them. Our local copies of the external judges are byte-identical to the pinned revisions.

Not public.

The HotpotQA confirmation records (2,276 pairs), the crossed bench (arm E, C1 and C2), the probe heads of M0–M3, the M4-R and M4-J checkpoints (identified by sha256 in internal ledgers), the code repository with the validator and the builders, and the time-stamped pre-specification records are internal; their release has not been approved.

What can be reproduced.

With the public dataset and evaluator, a reader can rescore any system, including the pinned zero-shot judges, on the MuSiQue and 2Wiki records and recompute the contrasts of Sections 6.3 and 6.4. The trained-system results (M0–M4), the HotpotQA confirmation, the crossed control and the batch diagnostic cannot be reproduced externally from public material, and the pre-specification cannot be verified by a third party. We therefore do not claim full reproducibility.

13 Conclusion

A near-perfect score on an edited sufficiency benchmark can conceal sensitivity to how the benchmark was built. It does not show that a model follows evidence chains, and it does not show that the model ignores them. ChainCheck exposes this confound by reporting, next to that score, a chain effect and an edit effect measured as paired conditional contrasts on pairs certified by a deterministic validator. In a sealed confirmation and an untuned replication, nominal scores stay near the ceiling while the contrasts separate the systems: trained readouts have large edit effects, and whether edit sensitivity dominates depends on the dataset. Under the pre-specified criterion with unclustered intervals the reference zero-shot judge is chain-selective in every setting, but the records share documents, too few independent groups exist for an informative clustered interval, and the judge’s first rank on 2Wiki is dataset-specific. How strongly these data support chain selectivity depends on dataset structure and on the treatment of dependent records, which is itself a reason to report the edit-only cell and the dependence structure alongside any sufficiency score. Two follow-up controls point the same way without settling it: matching the number of edited passages changes every chain contrast, most for the trained readouts, and masking passage titles changes them by a few hundredths at most; on these records the point estimates of the judge’s \(\Sigma\) remain positive, but all four verdicts are inconclusive under document dependence, so neither control rules out its alternative explanation, and neither explains why edit dominance depends on the dataset.

On an independent HotpotQA set with one pair per document group, the only set here that allows a decisive clustered verdict, neither pre-specified pattern replicated. A crossed control that cancels additive per-passage effects shows that every system responds to whether the bridge-entity strings agree and that every system also responds to the edit itself. String consistency is not multi-hop reasoning: an artifact-only string match reaches the maximum of the same statistic. Both kinds of sensitivity are observed together, the edit confound is not removed, and the non-replication stands. A scoring detail that papers rarely report, how records are batched, changed one judge’s scores enough to fail a reproducibility gate; what we report is reproducibility under fixed layouts, not invariance to batching.

References

- [1] Hongyu Chen and Seraphina Goldfarb-Tarrant. Safer or luckier? LLMs as safety evaluators are not robust to artifacts. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 19750–19766, 2025. arXiv:2503.09347.
- [2] Jiawei Chen, Hongyu Lin, Xianpei Han, and Le Sun. Benchmarking large language models in retrieval-augmented generation. In Proceedings of AAAI 2024, 2024. arXiv:2309.01431.
- [3] Jifan Chen and Greg Durrett. Understanding dataset design choices for multi-hop reasoning. In Proceedings of NAACL-HLT 2019, 2019. arXiv:1904.12106.
- [4] Florin Cuconasu, Giovanni Trappolini, Federico Siciliano, Simone Filice, Cesare Campagnano, Yoelle Maarek, Nicola Tonellotto, and Fabrizio Silvestri. The power of noise: Redefining retrieval for RAG systems. In Proceedings of SIGIR 2024, 2024. arXiv:2401.14887.
- [5] Wenzhang Du. What would fix this RAG failure? auditing counterfactual response with paired evidence interventions, 2026.
- [6] Matt Gardner, Yoav Artzi, Victoria Basmova, Jonathan Berant, Ben Bogin, Sihao Chen, et al. Evaluating models’ local decision boundaries via contrast sets. In Findings of EMNLP 2020, 2020. arXiv:2004.02709.
- [7] Robert Geirhos, Jörn-Henrik Jacobsen, Claudio Michaelis, Richard Zemel, Wieland Brendel, Matthias Bethge, and Felix A. Wichmann. Shortcut learning in deep neural networks. Nature Machine Intelligence, 2020. arXiv:2004.07780.
- [8] Suchin Gururangan, Swabha Swayamdipta, Omer Levy, Roy Schwartz, Samuel R. Bowman, and Noah A. Smith. Annotation artifacts in natural language inference data. In Proceedings of NAACL-HLT 2018, 2018. arXiv:1803.02324.
- [9] John Hewitt and Percy Liang. Designing and interpreting probes with control tasks. In Proceedings of EMNLP-IJCNLP 2019, 2019. arXiv:1909.03368.
- [10] Xanh Ho, Anh-Khoa Duong Nguyen, Saku Sugawara, and Akiko Aizawa. Constructing a multi-hop QA dataset for comprehensive evaluation of reasoning steps. In Proceedings of COLING 2020, 2020. arXiv:2011.01060.
- [11] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. LoRA: Low-rank adaptation of large language models. In Proceedings of ICLR 2022, 2022. arXiv:2106.09685.
- [12] Yichen Jiang and Mohit Bansal. Avoiding reasoning shortcuts: Adversarial evaluation, training, and model development for multi-hop QA. In Proceedings of ACL 2019, 2019. arXiv:1906.07132.
- [13] Hailey Joren, Jianyi Zhang, Chun-Sung Ferng, Da-Cheng Juan, Ankur Taly, and Cyrus Rashtchian. Sufficient context: A new lens on retrieval augmented generation systems. In International Conference on Learning Representations (ICLR), 2025. arXiv:2411.06037.
- [14] Divyansh Kaushik, Eduard Hovy, and Zachary C. Lipton. Learning the difference that makes a difference with counterfactually-augmented data. In Proceedings of ICLR 2020, 2020. arXiv:1909.12434.
- [15] Divyansh Kaushik and Zachary C. Lipton. How much reading does reading comprehension require? a critical investigation of popular benchmarks. In Proceedings of EMNLP 2018, 2018. arXiv:1808.04926.
- [16] Shayne Longpre, Kartik Perisetla, Anthony Chen, Nikhil Ramesh, Chris DuBois, and Sameer Singh. Entity-based knowledge conflicts in question answering. In Proceedings of EMNLP 2021, 2021. arXiv:2109.05052.
- [17] R. Thomas McCoy, Ellie Pavlick, and Tal Linzen. Right for the wrong reasons: Diagnosing syntactic heuristics in natural language inference. In Proceedings of ACL 2019, 2019. arXiv:1902.01007.
- [18] Sewon Min, Eric Wallace, Sameer Singh, Matt Gardner, Hannaneh Hajishirzi, and Luke Zettlemoyer. Compositional questions do not necessitate multi-hop reasoning. In Proceedings of ACL 2019, 2019. arXiv:1906.02900.
- [19] Adam Poliak, Jason Naradowsky, Aparajita Haldar, Rachel Rudinger, and Benjamin Van Durme. Hypothesis only baselines in natural language inference. In Proceedings of the Seventh Joint Conference on Lexical and Computational Semantics (*SEM), 2018. arXiv:1805.01042.
- [20] Ofir Press, Muru Zhang, Sewon Min, Ludwig Schmidt, Noah A. Smith, and Mike Lewis. Measuring and narrowing the compositionality gap in language models. In Findings of EMNLP 2023, 2023. arXiv:2210.03350.
- [21] Jingxi Qiu, Zeyu Han, and Cheng Huang. SURE-RAG: Sufficiency and uncertainty-aware evidence verification for selective retrieval-augmented generation, 2026.
- [22] Pranav Rajpurkar, Robin Jia, and Percy Liang. Know what you don’t know: Unanswerable questions for SQuAD. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), 2018. arXiv:1806.03822.
- [23] François Roewer-Després, Jinyue Feng, Zining Zhu, and Frank Rudzicz. ACCORD: Closing the commonsense measurability gap. In Proceedings of NAACL 2025 (Long Papers), 2025. arXiv:2406.02804.
- [24] Yixuan Tang, Hwee Tou Ng, and Anthony K. H. Tung. Do multi-hop question answering systems know how to answer the single-hop sub-questions?, 2020.
- [25] Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. Is multihop QA in DiRe condition? measuring and reducing disconnected reasoning. In Proceedings of EMNLP 2020, 2020.
- [26] Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal. MuSiQue: Multihop questions via single-hop question composition. Transactions of the Association for Computational Linguistics, 2022. arXiv:2108.00573.
- [27] Jian Wu, Linyi Yang, Zhen Wang, Manabu Okumura, and Yue Zhang. CofCA: A step-wise counterfactual multi-hop QA benchmark, 2024.
- [28] Jian Xie, Kai Zhang, Jiangjie Chen, Renze Lou, and Yu Su. Adaptive chameleon or stubborn sloth: Revealing the behavior of large language models in knowledge conflicts. In Proceedings of ICLR 2024, 2024. arXiv:2305.13300.
- [29] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and Christopher D. Manning. HotpotQA: A dataset for diverse, explainable multi-hop question answering. In Proceedings of EMNLP 2018, 2018. arXiv:1809.09600.
- [30] Ori Yoran, Tomer Wolfson, Ori Ram, and Jonathan Berant. Making retrieval-augmented language models robust to irrelevant context. In Proceedings of ICLR 2024, 2024. arXiv:2310.01558.
- [31] JungMin Yun, JuneHyoung Kwon, and YoungBin Kim. CRiT-QA: Evaluating multi-hop reasoning with counterfactual chains and distractor traps. In Proceedings of LREC 2026, 2026. arXiv:2607.10562.
- [32] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica. Judging LLM-as-a-judge with MT-Bench and chatbot arena. In Advances in Neural Information Processing Systems (Datasets and Benchmarks Track), 2023. arXiv:2306.05685.
