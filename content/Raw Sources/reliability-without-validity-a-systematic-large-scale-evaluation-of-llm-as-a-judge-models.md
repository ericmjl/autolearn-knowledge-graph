---
title: "Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias"
type: "raw-source"
url: "https://arxiv.org/html/2606.19544v1"
author: "Justin D Norman Affiliation justin norman, Michaelrivera, Dhughes Edu"
publication: "arXiv"
published: "2025-05-14"
archived: "2026-11-25T04:01:23Z"
---

> [!quote] Original source
> **Author(s):** Justin D Norman Affiliation justin norman, Michaelrivera, Dhughes Edu  
> **Title:** Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias  
> **Published in:** arXiv  
> **Date:** 2025-05-14  
> **Original:** <https://arxiv.org/html/2606.19544v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-reliability-without-validity-a-systematic-large-scale-evaluation-of-llm-as-a-judge-models|Source note]]
Themes: [[Evals and agent quality]]
Why it was archived: How should the claim-level faithfulness judge be kept calibrated as the model, prompt, or retrieved-document distribution drifts over time?

## Archived text

Reliability without Validity: A Systematic, Large-Scale Evaluation

of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias

Abstract

LLM-as-a-Judge has become the dominant evaluation paradigm for language models, but judge validation in practice relies on exact-match agreement, a metric that does not correct for chance and systematically overstates discriminative ability. We present the largest systematic evaluation of LLM-as-a-Judge to date: 21 judges from nine providers across MT-Bench, JudgeBench, and RewardBench, evaluated under three protocols (agreement, consistency, bias audit) over 118 runs and approximately \(541{,}000\) individual judgments. Four findings emerge, consistent across the full cohort, including the April 2026 frontier: kappa deflation between exact match and Cohen’s \(\kappa\) is universal (\(33\)–\(41\) pp on MT-Bench), judge rankings shift by up to 14 positions across benchmarks, high test–retest reliability (\(>0.95\)) coexists with severe position bias (\(>0.10\)) in two production-deployed judges (instantiating a consistency–bias paradox), and verbosity bias is small (\(&lt;0.011\)) across our cohort under a single pairwise rubric. We distill these into a Minimum Viable Validation Protocol.

1 Introduction

Large language models (LLMs) increasingly evaluate large-scale content (Zheng et al., 2023). These “judgments” rely on the model’s ability to mimic a human evaluator on tasks requiring analytical acuity. Such judges are widely deployed in production evaluation pipelines across hundreds of documented LLMOps deployments (DoorDash Engineering, 2024; Strick van Linschoten, 2025). This proliferation has accelerated despite well-documented reliability issues with LLM use for reasoning tasks (Wang et al., 2024; Wu and Aji, 2025; Panickssery et al., 2024; Stureborg et al., 2024; Schroeder and Wood-Doughty, 2024; Gu et al., 2024; Li et al., 2024a; Shi et al., 2025). Surveys of LLM-as-Judge (LLMaJ) reliability identify a recurring set of failure modes: inconsistency across prompts and runs, systematic scoring biases, weak domain-specific calibration, and the absence of meta-evaluation standards for comparing judges on equal footing.

Despite these challenges, judge validation continues to rely heavily on exact match. Established judge benchmarks—MT-Bench (Zheng et al., 2023), RewardBench (Lambert et al., 2025), JudgeBench (Tan et al., 2025)—and recent successors (Malik et al., 2026; Whitehouse et al., 2025; Jiang et al., 2025) privilege raw agreement as the headline validation metric. This family of metrics does not correct for chance (Cohen, 1960; Hayes and Krippendorff, 2007) and overstates discriminative ability (Guerdan and others, 2025; Han et al., 2025; Collot et al., 2025).

No prior work has conducted a large-scale, cross-benchmark, multi-protocol evaluation of judge reliability across model families and generations. We present the largest such evaluation: 21 models from nine providers across three benchmarks and three evaluation protocols, producing 541,000 judgments over 118 runs.

We report five principal findings, including two diagnostic concepts. First, kappa deflation: raw agreement overstates chance-corrected discrimination by 33–41pp in all 21 evaluated models. Second, judge rankings are non-transferable: models shift by as many as 14 positions across benchmarks. Third, the consistency–bias paradox: high test–retest reliability often masks severe position bias. Fourth, verbosity bias is much reduced: all 21 models register \(&lt;\)0.011, in sharp contrast to the 20–40% variance reported in 2023 literature. Fifth, JudgeBench discriminates \(4.5\times\) more sharply than MT-Bench (60.4pp vs. 13.5pp \(\kappa\) spread).

2 Related Work

The LLMaJ paradigm originated with MT-Bench and Chatbot Arena (Zheng et al., 2023). Rapid adoption followed across diverse evaluation settings, including G-Eval for natural-language-generation tasks (Liu et al., 2023), AlpacaEval for instruction-following (Dubois et al., 2024), Arena-Hard for separating model performance from crowdsourced preference data (Li et al., 2025b), and WildBench for real-user prompts (Lin et al., 2025). LLMaJ is now widely deployed in industrial evaluation pipelines, and has emerged as the dominant pattern for reference-free scoring across hundreds of production LLM deployments (Strick van Linschoten, 2025).

Evaluation of LLMaJ has expanded rapidly in response to the widespread adoption of the approach. The field faces distinct challenges surrounding reliability, consistency, and bias mitigation, which have prompted some emergent remedies (Gu et al., 2024; Li et al., 2025a). For example, prior work has documented biases inherited from pretraining corpora, difficulty adapting evaluation criteria across domains, and unresolved questions about consensus among cooperating judge models (Li et al., 2024a). Other work identifies inconsistency under temperature and prompt variation (Stureborg et al., 2024), introduces reliability coefficients (Schroeder and Wood-Doughty, 2024), evaluates rating-indeterminacy (Guerdan and others, 2025), and examines latent dimensions of reliability (Choi et al., 2026). Closest in scale to our work, Bavaresco et al. (2025) surveys 11 LLM judges across 20 NLP evaluation tasks and recommends careful validation against task-specific annotation before deployment.

2.1 LLM Judge Metrics and Definitions

Exact match is the proportion of items on which the judge’s verdict matches the human label. We follow Zheng et al. (2023) in reporting the tie-excluded variant for pairwise comparisons, restricting the denominator to items on which the human label is non-tie (Wang et al., 2025). Despite being widely used, exact match does not correct for agreement expected by chance, and as a result exact match is sensitive to the label distribution of the underlying benchmark.

Cohen’s \(\kappa\) is a chance-corrected measure of agreement between two raters on categorical labels:

where \(p_{o}\) is the observed agreement and \(p_{e}\) is the agreement expected by chance under the marginal label distributions of the two raters (Cohen, 1960). We use \(\kappa\) as our primary agreement metric and compare each judge against the human label set on all benchmarks. Krippendorff’s \(\alpha\) (Krippendorff, 2011) is a reliability coefficient that accommodates more than two raters as well as ordinal and interval scales. The two measures coincide for the two-rater nominal case, but \(\alpha\) extends naturally to the multi-run consistency setting introduced below.

Test-retest reliability is the agreement of a judge with itself across independent re-evaluations of the same items. The concept captures the stability of verdicts under identical conditions, and is a necessary but insufficient characteristic of a quality judge. Self-consistency is the proportion of items on which the majority verdict across \(N\) runs agrees with each individual run, capturing within-judge agreement at the item level and complementing the corpus-level test–retest coefficient.

Position flip rate is the fraction of items for which the judge’s verdict changes when the response order is swapped (Zheng et al., 2023), providing an item-level measure of position sensitivity that complements the aggregate position-bias statistic defined next. Position bias is the tendency of a judge to favor response in a particular position (Zheng et al., 2023; Wang et al., 2024; Shi et al., 2025). Across a range of judge models, flip rates range from \(25\%\) to \(50\%\) (Wang et al., 2024; Shi et al., 2025). Position-swap debiasing raises within-judge consistency from roughly \(60\%\) to \(85\%\) (Li et al., 2024b).

Verbosity bias is the tendency of a judge to prefer longer responses regardless of content quality (Wu and Aji, 2025; Dubois et al., 2024). Following Dubois et al. (2024), we operationalize verbosity bias as the Pearson correlation between the response-length differential \(|\text{len}(A)|-|\text{len}(B)|\) and the judge’s verdict.

Kappa deflation is the difference between exact match and Cohen’s \(\kappa\) for a given judge–benchmark pair:

\(\Delta_{\kappa}\) quantifies how much raw agreement overstates chance-corrected discriminative ability. We introduce this term to name a phenomenon that, while mathematically a direct consequence of Cohen’s correction (Cohen, 1960), has not been systematically measured or reported at scale across modern LLM judges. On MT-Bench we observe \(\Delta_{\kappa}\in[33.8,41.2]\) percentage points across all 21 models tested.

Consistency-bias paradox is the empirical observation that high test-retest reliability (\(\alpha>0.95\)) can coexist with severe position bias in the same judge model, such that the judge is highly reproducible but not valid. We introduce this term to formalize a failure mode reachable by reporting test-retest alone (Stureborg et al., 2024; Schroeder and Wood-Doughty, 2024; Chen et al., 2024). The paradox arises because test-retest measures the stability of outputs and not the correctness of the underlying decision process: a judge that deterministically favors position \(A\) across runs would achieve a perfect test-retest score, but would also exhibit maximum-possible position bias.

2.2 Attempts to Improve Reliability

A growing body of work both documents the reliability limitations of LLMaJ systems, and then develops specialized architectures intended to mitigate them. Test-retest studies show substantial temperature sensitivity: same-verdict rates are above 95% when temperature is set to 0, but fall to as low as 70% when temperature is increased to 1 (Stureborg et al., 2024; Haldar and Hockenmaier, 2025). Recent approaches have separated intrinsic consistency from human-alignment using Item Response Theory models (Choi et al., 2026). Another line of work develops dedicated judge architectures rather than relying on general-purpose language models. These experiments show some promise of reducing position bias (Zhu et al., 2025) and cost (Verga et al., 2024) while approaching general-purpose model performance (Kim et al., 2024a; Kim et al., 2024b). Our study complements these efforts by evaluating reliability at scale across 21 judge models and three benchmarks under a common experimental protocol.

3 Methodology

Model Selection

We evaluate 21 general-purpose model LLM judges drawn from 9 providers grouped into three capability tiers. Table 1 lists each model with its provider, release date, tier, and per-token cost. Tier 1 consists of widely-deployed production judges; Tier 2 consists of cost-conscious models; Tier 3 consists of April 2026 frontier models and open-source systems. The 21 models span parameter counts from 8B to over 100B.

Benchmarks

We evaluate every judge on three benchmarks of increasing difficulty. MT-Bench contributes 2,391 pairwise comparisons with expert human judgments and is the most widely-used judge-evaluation benchmark (Zheng et al., 2023). JudgeBench contributes 350 items spanning mathematics, coding, creative writing, and analysis labeled for objective correctness rather than aesthetic preference (Tan et al., 2025). RewardBench contributes 2,981 chosen-versus-rejected pairs, presented to each judge under per-item position randomization so that the chosen response is equally likely to occupy either position (Lambert et al., 2025).

Evaluation Protocols

We measure judge behavior under three protocols. First, the agreement protocol produces a single judgment per item and compares it to the human label, reporting Cohen’s \(\kappa\), Krippendorff’s \(\alpha\), and tie-excluded exact match. Second, the consistency protocol runs \(N\in[3,5]\) independent evaluations per item with response caching disabled, presenting each pair in both AB and BA orderings, and reports test–retest reliability, self-consistency, and position flip rate. Third, the bias-audit protocol presents AB+BA orderings together with response-length analysis, and reports position bias and verbosity bias.

Hypotheses

We formulate seven hypotheses before running frontier-model evaluation and list them here so that readers can assess our findings against a priori predictions. H1: Kappa deflation will persist within frontier models. H2: Thinking-architecture models (GPT-5.4, Gemini 3.1 Pro, DeepSeek V3.2) will exhibit position bias below \(0.05\). H3: Cross-benchmark rank divergence will be at least three positions for some model. H4: MT-Bench will show a limited \(\kappa\) spread, defined as the distance between the largest and smallest Cohen’s \(\kappa\). H5: Issues with RewardBench, (human labels are all in the A position), will persist under generative evaluation. As a result, \(\kappa\) values will be very small, no larger than \(0.05\). H6: Position flip rate will degrade by at least a factor of \(1.5\) from MT-Bench to JudgeBench. H7: At least one model will exhibit test-retest reliability greater than \(0.95\) and with position bias greater than \(0.10\).

Experimental Procedure

We conducted model evaluation in seven phases over a five-week window during March and April 2026. A detailed summary is in Appendix F. The full procedure produced 118 evaluation runs, and approximately \(541,000\) judgments. All evaluations used temperature \(0\). In order to ensure that replicate runs sample independent generations rather than memorized responses, we execute the consistency protocol with response caching disabled. Position-swap debiasing (AB+BA paired evaluations) was applied in both the consistency and bias-audit protocols. Every run was executed with a bespoke research evaluation library (that will be released open source upon publication) which implements the 14 metrics for each model.

4 Results

4.1 Kappa Deflation Is Universal

Figure 1 (a) plots the dumbbell of exact match and \(\kappa\) values for each judge on MT-Bench and Table 2 reports \(\kappa\), exact match, and \(\Delta_{\kappa}\) for all three benchmarks. Every judge in our study exhibits substantial kappa deflation on MT-Bench: exact match overstates chance-corrected agreement by between \(33.8\) and \(41.3\) percentage points across the 21 models, with a cohort mean of \(38.6\) pp. The deflation is universal across capability tiers: all ten frontier-generation (Tier 3) judges exhibit \(\Delta_{\kappa}\geq 30\) pp, supporting H1. Even the judge that performed best on chance-corrected agreement, Gemini 3.1 Pro, shows a \(33.8\) pp gap between exact match (\(EM=0.849\)) and chance-corrected (\(\kappa=0.511\)) performance.

The magnitude of deflation varies systematically with the benchmark’s label distribution. MT-Bench, with a balanced A/B/Tie distribution, produces the largest mean deflation (\(38.6\) pp); JudgeBench’s pairwise correctness-labeled items produce a mean of \(23.7\) pp (range \(8.1\) to \(38.5\)); RewardBench’s binary chosen-versus-rejected pairs produce \(10.4\) pp (range \(5.9\) to \(21.3\)). Balanced label distributions raise expected-by-chance agreement, which inflates the gap between raw and chance-corrected metrics. The practical consequence is that a judge reporting “\(85\%\) agreement” on MT-Bench has \(\kappa\approx 0.48\).

4.2 Position Bias Heterogeneity

Table 3, column 2, reports position biases for each model. The least position biased model, Gemini 2.5 Pro (\(pb=0.002\)) and most position biased model Qwen 3 8B (\(pb=0.192\)) span nearly two orders of magnitude difference in position bias. In this evaluation, reasoning and frontier models have systematically lower rates of position bias; small, and cost-optimized models have the highest rates of position bias. Within-family heterogeneity is large: Gemini 2.5 Pro (\(0.002\)) and Gemini 2.5 Flash (\(0.125\)) differ by a factor of \(70\). H2 predicted that the three thinking-architecture judges (GPT-5.4, Gemini 3.1 Pro, DeepSeek V3.2) would all fall below \(0.05\); only Gemini 3.1 Pro (\(0.038\)) does so. And so, while they reduce position bias relative to cost-efficient models, they do not eliminate it.

4.3 Cross-Benchmark Rank Instability

Consistent with Hypothesis 3, benchmark choice has an appreciable effect on relative rankings of performance. More than half (\(11\) of the \(21\)) shift by four or more positions, and only Gemini 3.1 Pro and Claude Opus 4.6 hold a top-three position across all three benchmarks. The largest single shift is Llama 3.3 70B which shifts \(15\) positions, from 5 on MT-Bench to 20 on JudgeBench. Other notable cases include Minimax M2.7 (MT:17, JB:5), DeepSeek V3.2 (MT:3, JB:13), GPT-4o (MT:8, JB:18), GPT-oss 120B (MT:12, RB:3), and Claude Haiku 4.5 (MT:15, RB:6). (Supplementary figure Figure 2 visualizes Table 2 highlighting position changes.)

The instability is amplified by sharp differences in benchmark discriminability: MT-Bench compresses all \(21\) judges into a \(13.5\) pp \(\kappa\) band (\(0.376\) to \(0.511\)) with an average gap of \(0.6\) pp between adjacent ranks; JudgeBench spreads the same models over \(60.4\) pp (\(0.271\) to \(0.875\)) with \(3\)–\(9\) pp tiers; RewardBench falls between at \(28.1\) pp (\(0.616\) to \(0.898\)), with the top seven judges within a tight \(2.7\) pp band followed by gradual separation. Where the underlying distribution is compressed, small \(\kappa\) differences produce large rank changes, and a model’s apparent ranking on a single benchmark is a poor estimator of its ranking on others.

4.4 MT-Bench Ceiling Effect

Hypothesis 4 predicted an MT-Bench \(\kappa\) spread of at most \(5\) pp. As we report in Table 2, we observe \(13.5\) pp (\(0.376\) to \(0.511\)) across all 21 judges, narrowing to \(6.5\) pp within the top ten and approaching the H4 ceiling. The wider full-cohort spread is driven by a distinct lower tier (GPT-5.4-mini, Mixtral 8x22B, GPT-4o-mini). JudgeBench’s \(\kappa\) spread on the same population is \(60.4\) pp, a factor of \(4.5\times\) wider, confirming that MT-Bench’s preference-style label set compresses meaningful quality differences among strong judges.

4.5 Position-Randomized Evaluation of RewardBench

Hypothesis 5 predicted that RewardBench would generate \(\kappa\) values no larger than \(0.05\) because it placed all correct human labels in the A position. As we report in Table 2 the benchmark data is not consistent with this hypothesis. Under per-item position-randomized evaluation (loader configuration in Appendix E), all 20 evaluated judges produce \(\kappa\) values in the range \([0.616,0.898]\). The top five judges produce highly reasonable \(\kappa\) values: Gemini 3.1 Pro \((0.898)\), GPT-oss 120B \((0.880)\), Claude Opus 4.6 \((0.879)\), GPT-5.4 \((0.879)\), and Claude Haiku 4.5 \((0.873)\). The full \(\kappa\) spread on RewardBench is \(28.1\) pp, between MT-Bench’s \(13.5\) pp and JudgeBench’s \(60.4\) pp, and the top tier is tightly clustered (the top seven judges fall within a \(2.7\) pp band). (In the Appendix, Table 5 summarises Table 2, making it easier to read ranks and \(\kappa\) jointly across the three benchmarks.)

4.6 Consistency Falls on Hard Benchmarks

Consistent with Hypothesis 6, seven of the sixteen judges evaluated under the consistency protocol show a position flip-rate increase of at least \(1.5\times\) from MT-Bench to JudgeBench. The three most acute degradations are Llama 3.3 70B (\(3.3\times\), \(0.077\) to \(0.253\)), GPT-4o-mini (\(3.0\times\), \(0.127\) to \(0.380\)), and GLM-5 (\(2.4\times\), \(0.096\) to \(0.227\)). Two frontier judges go in the opposite direction: Claude Opus 4.6 and Gemini 3.1 Pro both improve by a factor of \(0.58\times\) when moving from MT-Bench to JudgeBench, suggesting that some current-generation systems handle harder items with greater positional stability than they show on easier items. (In the appendix, Figure 3 plots all 16 trajectories together with the cohort medians (\(0.09\) on MT-Bench, \(0.17\) on JudgeBench)).

Test-retest reliability follows a similar pattern at the cohort level: the mean test–retest across the 16 judges drops from \(0.943\) on MT-Bench to \(0.911\) on JudgeBench. Per-judge values vary widely; for example, Gemini 2.5 Flash drops by \(7.3\) pp (\(0.988\) to \(0.915\)), while Gemini 3.1 Pro is essentially unchanged (\(0.977\) to \(0.978\)). (In the appendix, we report per-judge MT and JB test–retest values in Table 6.)

4.7 The Consistency–Bias Paradox

Hypothesis 7 predicted that at least one judge would exhibit test-retest reliability above \(0.95\) together with position bias above \(0.10\), evidence of the tradeoffs between consistency-bias. Two judges, Qwen 3 8B (test-retest \(0.992\), position bias \(0.192\)) and Gemini 2.5 Flash (test-retest \(0.988\), position bias \(0.125\)) generate such paradoxical results. Figure 1 (b) plots all 16 jointly evaluated judges in the test-retest by position-bias plane. Judges that occupy the upper-right region are those that demonstrate high test-retest reproducibility, but with high systematic bias.

Qwen 3 8B has the highest test-retest of judges evaluated in this study, but it simultaneously is among the most position biased judge in the cohort \((pb=0.192)\) and its JudgeBench \(\kappa\) (\(0.289\)) is the third lowest. Model determinism produces the same response position across replicate runs, which yields near-perfect within-judge agreement, but it violates the requirement that verdicts be position-invariant. This result has methodological implications for future teams: test–retest measures the stability of a judge’s outputs, not the correctness of the underlying decision process. Reporting test-retest alone stands to present a misleading picture of judge reliability.

4.8 Pairwise Verbosity Bias

All 21 judges evaluated under the bias-audit protocol register a verbosity bias below \(0.011\) on MT-Bench, with the largest value being GPT-4o-mini at \(0.010\); 17 of the 21 judges fall below \(0.005\), with the smallest values clustered around \(0.001\). Per-judge values appear in Table 3. The magnitudes are an order of magnitude smaller than the variance contributions reported in \(2023\)-era studies of style and length effects (Wu and Aji, 2025), suggesting that verbosity sensitivity has fallen substantially as a practical concern over the past two model generations. We caution against generalizing this finding beyond our setting: the measurement uses a single pairwise rubric and a fixed length-differential operationalization (Dubois et al., 2024), and we do not claim that verbosity bias has been eliminated under arbitrary rubric or task variation.

4.9 Model Family Analysis

Several provider-family patterns are visible in the per-judge \(\kappa\) values reported in Table 2. The three Anthropic judges average \(\kappa=0.770\) on JudgeBench (Opus 4.6 \(0.875\), Sonnet 4.6 \(0.782\), Haiku 4.5 \(0.653\)) with an average position bias of \(0.020\), the strongest joint performance on hard items and the lowest cohort-level bias of any provider. The three OpenAI flagships (GPT-4o, GPT-4.1, GPT-5.4) average \(\kappa=0.467\) on JudgeBench, well below the Anthropic and Google frontier-tier figures. Within-OpenAI developed models, generational progression is visible: \(\kappa\) rises from \(0.309\) for GPT-4o to \(0.487\) for GPT-4.1, and rises to \(0.606\) for GPT-5.4. MT-Bench’s compressed scale makes the same generational progression nearly invisible: the corresponding MT-Bench values are \(0.451\), \(0.451\), and \(0.457\).

Similarly, within-family scaling is more legible on JudgeBench than on MT-Bench. Claude Opus 4.6 (\(\kappa=0.875\)) is \(9.3\) pp above Claude Sonnet 4.6 (\(\kappa=0.782\)) on JudgeBench; the corresponding MT-Bench values differ by \(0.6\) pp (Opus \(0.489\), Sonnet 4.6 \(0.484\)). Mid-tier judges can outperform frontier judges on specific dimensions: Kimi K2.5 records the lowest position bias of any non-Gemini judge (\(0.004\)), competitive with Claude Opus 4.6, while achieving JudgeBench \(\kappa=0.720\) at a fraction of the frontier-tier cost. We return to cost-quality trade-offs in section 5.

5 Discussion

5.1 Why Exact Match Misleads

Exact match rewards chance agreement as if it were genuine discrimination. On a balanced ternary label set such as MT-Bench, with the chance baseline \(p_{e}\approx 1/3\), exact-match values in \([0.80,0.85]\) correspond to a Cohen’s \(\kappa\) near \(0.48\). This is a moderate value, not the near-perfect band the percentage suggests. The \(33.8\)–\(41.3\) pp gap we observe on MT-Bench is therefore not a model-quality artifact: it is how an uncorrected metric interacts with the label marginals of the benchmark (Cohen, 1960; Guerdan and others, 2025). The cohort-mean \(\Delta_{\kappa}\) contracts from \(38.6\) pp on MT-Bench to \(23.7\) pp on JudgeBench and \(10.2\) pp on RewardBench, tracking the shift from balanced ternary to imbalanced binary labels exactly as Cohen’s correction predicts.

Exact-match figures used to justify deploying LLM judges therefore may significantly overstate their chance-corrected discriminative ability by an amount that depends on the benchmark, not the judge (Han et al., 2025; Collot et al., 2025). We recommend reporting Cohen’s \(\kappa\) or Krippendorff’s \(\alpha\) alongside any exact-match figure, with the chance-corrected metric (not the raw rate), treated as the headline reliability number. Figure 1 (a) and Table 2 illustrate the gap for every judge in our cohort.

5.2 Limits of Single-Benchmark Validation

Cross-benchmark rank instability has two coupled drivers. First, benchmarks differ in discriminative power: MT-Bench compresses the \(21\)-judge cohort into a \(13.5\) pp \(\kappa\) band while JudgeBench spreads the same judges across \(60.4\) pp, a \(4.5\times\) wider range. Small absolute differences yield large rank changes. Second, the three benchmarks measure subtly different latent constructs (preference alignment, objective correctness, and chosen-vs-rejected discrimination, respectively), and a judge that looks strong under one construct can collapse under another. Llama 3.3 70B (MT\(\#\)5 \(\to\) JB\(\#\)19) and Minimax M2.7 (MT\(\#\)16 \(\to\) JB\(\#\)5) illustrate the two directions.

Only two judges (Claude Opus 4.6 and Gemini 3.1 Pro) hold a top-three position across all three benchmarks; ten of twenty-one exhibit a maximum pairwise rank shift of at least four positions. Practically, judge validation should report results from at least two benchmarks chosen to span the preference-versus-correctness axis rather than relying on the discriminability of any single dataset. Appendix Figure 2 and Appendix Table 5 report the full set of rank trajectories.

5.3 The Consistency–Bias Paradox and a Minimum Viable Validation Protocol

Test–retest reliability measures output stability, not decision-process correctness. Position bias and within-judge agreement are mathematically orthogonal, so a judge that deterministically prefers position A across runs achieves near-perfect test–retest while exhibiting maximal position bias. Qwen 3 8B (test–retest \(0.992\), position bias \(0.192\), JudgeBench \(\kappa=0.289\)) is the empirical extreme. Gemini 2.5 Flash (\(0.988\), \(0.125\)) instantiates the same pattern more mildly. Because reporting test–retest alone remains common in LLMaJ validation (Stureborg et al., 2024; Schroeder and Wood-Doughty, 2024), current reporting practice misleads precisely in the cases that matter most for deployment: highly reproducible judges. Figure 1 (b) shows the dissociation across the \(16\) jointly evaluated judges. This paradox motivates our recommended Minimum Viable Validation Protocol (MVVP) below.

Minimum Viable Validation Protocol (MVVP). Before deploying an LLM judge: 1. Chance-correct. Report Cohen’s \(\kappa\) (or Krippendorff’s \(\alpha\)) alongside any exact-match figure, and treat the chance-corrected metric as the headline reliability number. 2. Swap positions. Measure position bias via paired AB+BA evaluations and report \(\left|P(\text{A wins})-0.5\right|\). 3. Replicate. Measure test–retest reliability over \(\geq 3\) independent runs at temperature \(0\) with response caching disabled. 4. Cross-validate. Evaluate on \(\geq 2\) benchmarks spanning preference-style and correctness-style label distributions. 5. Audit the paradox. When test–retest exceeds \(0.95\), verify position bias is below \(0.10\) before claiming reliability. High stability with high bias is a failure mode, not a strength.

5.4 Dataset as Community Resource

We will release the complete evaluation dataset and the [anonymized] code repository upon publication. The dataset is derived from \(118\) evaluation runs spanning \(21\) judges, three benchmarks, and three protocols, totaling approximately \(541{,}000\) individual judgments. Every run includes the per-item judge verdict, the model’s free-form reasoning, the raw response, per-call latency, and the metric values computed for the run, so that downstream users can recompute any of our reported numbers from raw data or substitute their own metric and aggregation choices. The release supports three use cases we cannot pursue here: large-scale meta-analysis across judges and benchmarks (including variance-component decompositions across runs, items, and position orderings); development and validation of new calibration techniques on a fixed model\(\times\)benchmark population (Li et al., 2025c); and a frozen baseline against which future judges can be evaluated under an identical protocol.

6 Conclusion

We present the largest systematic evaluation of LLMaJ to date: \(21\) judges from nine providers across three benchmarks and three measurement protocols, producing approximately \(541{,}000\) individual judgments. Four findings are present across the full cohort, including the frontier models released through April 2026: kappa deflation between exact match and Cohen’s \(\kappa\) is universal (\(33.8\)–\(41.3\) pp on MT-Bench); judge rankings shift by up to \(14\) positions across benchmarks; high test–retest reliability (\(>0.95\)) coexists with severe position bias (\(>0.10\)) in two production-deployed judges; and verbosity bias is small (\(&lt;0.011\)) across our cohort under a single pairwise rubric.

These findings translate into four practical recommendations. Judge validation should: (1) be chance-corrected by default, because raw exact match overstates discriminative ability by tens of percentage points, (2) span at least two benchmarks of contrasting label structure, since no single leaderboard predicts another’s, (3) measure consistency and bias jointly, because high test–retest can mask a determinism that violates position invariance, and (4) no longer foreground verbosity bias under standard pairwise rubrics, subject to scope caveats. We introduce these as a Minimum Viable Validation Protocol (Section 5) and will release the full dataset and the [anonymized] evaluation library upon publication so that future judges can be measured against the same baseline.

Several research directions remain open. Multilingual and multimodal judging are likely to surface failure modes that text-only English benchmarks cannot expose. Temporal stability across hosted-model endpoints, whose weights and serving stacks change without versioning, deserves dedicated longitudinal study. Judge-confidence calibration (Expected Calibration Error, Brier score) is a natural extension to this protocol once provider logprob coverage broadens. Finally, a formal variance-component decomposition that treats runs, items, and position orderings as random effects would convert the empirical patterns reported here into structured reliability coefficients, providing a principled basis for sample-size and replicate-count decisions in future judge-validation work.

Limitations

Benchmark coverage.

Our evaluation uses three established English-language, text-only benchmarks (MT-Bench, JudgeBench, RewardBench). Multilingual judging and multimodal judging—both of which are increasingly common deployment settings—are not characterized in this study (Fu and Liu, 2025). We caution against extrapolating any of our findings to those settings without further measurement.

Temporal stability.

All evaluation runs were executed within a five-week window in March–April 2026. Hosted-model endpoints are known to drift across provider-side updates, sometimes silently, and we have not yet re-evaluated these judges over time to quantify within-judge stability over a longer time horizon. Consequently, the numbers we report should be interpreted as a snapshot of provider behavior during this specific window.

Rubric sensitivity.

All judges were evaluated under a single pairwise comparison template and a fixed operationalization of each metric. In particular, our findings that all judges demonstrated verbosity bias below \(0.011\), under our pairwise rubric and length-differential operationalization (Wu and Aji, 2025; Dubois et al., 2024), should not be interpreted as a universal claim that verbosity bias is solved. Rubric design choices, including reference grounding and reasoning instructions, are known to interact with bias profiles in ways our single-template design cannot isolate.

Calibration.

Expected Calibration Error and Brier Score require token-level logprobs that are not exposed by the majority of providers in our cohort. We therefore defer calibration analysis to future work; the present study reports agreement, consistency, and bias under the protocols for which directly comparable measurements are available across all providers.

Cost reporting.

Per-token costs reported in Table 1 are list prices at the time of evaluation. Provider-specific volume tiers, batch-API discounts, and negotiated enterprise pricing are not reflected. Accordingly, these cost figures should be interpreted as approximate upper bounds for deployment-scale spend rather than committed rates.

Thinking-model suppression.

For models that generate a built-in reasoning trace (GPT-5.4, GPT-5.4-mini, Gemini 3.1 Pro, DeepSeek V3.2, Kimi K2.5, GLM-5, Minimax M2.7), the reasoning channel was suppressed using the provider-specific mechanisms documented in Appendix D; this maintained judge comparability and prevented verdict-token truncation when reasoning consumed the output budget. Reasoning-enabled evaluations could change agreement, consistency, and bias profiles, and we do not claim our results characterize the thinking-on configuration.

References

- LLMs instead of human judges? a large scale empirical study across 20 NLP evaluation tasks. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL), External Links: Link Cited by: §2.
- Humans or LLMs as the judge? a study on judgement bias. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.), Miami, Florida, USA, pp. 8301–8327. External Links: Link, Document Cited by: §2.1.
- Diagnosing the reliability of LLM-as-a-judge via item response theory. External Links: 2602.00521, Link Cited by: §2.2, §2.
- A coefficient of agreement for nominal scales. Educational and Psychological Measurement 20 (1), pp. 37–46. Cited by: Appendix H, §1, §2.1, §2.1, §5.1.
- Balanced accuracy: the right metric for evaluating LLM judges — explained through Youden’s J statistic. arXiv preprint arXiv:2512.08121. External Links: Link Cited by: §1, §5.1.
- How DoorDash leverages LLMs to evaluate search result pages. Note: DoorDash Engineering BlogAccessed 2026-05-07 External Links: Link Cited by: §1.
- Length-controlled AlpacaEval: a simple way to debias automatic evaluators. In Conference on Language Modeling (COLM), External Links: Link Cited by: Appendix H, §2.1, §2, §4.8, Rubric sensitivity..
- How reliable is multilingual LLM-as-a-judge?. In Findings of the Association for Computational Linguistics: EMNLP 2025, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), Suzhou, China, pp. 11040–11053. External Links: Link, Document, ISBN 979-8-89176-335-7 Cited by: Benchmark coverage..
- A survey on LLM-as-a-judge. arXiv preprint arXiv:2411.15594. External Links: Link Cited by: §1, §2.
- Validating LLM-as-a-judge under rating indeterminacy. In Advances in Neural Information Processing Systems (NeurIPS), External Links: Link Cited by: §1, §2, §5.1.
- Rating roulette: self-inconsistency in LLM-as-a-judge frameworks. In Findings of the Association for Computational Linguistics: EMNLP 2025, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), Suzhou, China, pp. 24986–25004. External Links: Link, Document, ISBN 979-8-89176-335-7 Cited by: §2.2.
- Judge’s verdict: a comprehensive analysis of LLM judge capability through human agreement. arXiv preprint arXiv:2510.09738. External Links: Link Cited by: §1, §5.1.
- Answering the call for a standard reliability measure for coding data. Communication Methods and Measures 1 (1), pp. 77–89. Cited by: Appendix H, §1.
- CodeJudgeBench: benchmarking LLM-as-a-judge for coding tasks. arXiv preprint arXiv:2507.10535. External Links: Link Cited by: §1.
- Prometheus: inducing fine-grained evaluation capability in language models. In International Conference on Learning Representations (ICLR), External Links: Link Cited by: §2.2.
- Prometheus 2: an open source language model specialized in evaluating other language models. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP), External Links: Link Cited by: §2.2.
- Computing Krippendorff’s alpha-reliability. Departmental Papers (ASC). Cited by: Appendix H, §2.1.
- RewardBench: evaluating reward models for language modeling. In Findings of the Association for Computational Linguistics: NAACL 2025, L. Chiruzzo, A. Ritter, and L. Wang (Eds.), Albuquerque, New Mexico, pp. 1755–1797. External Links: Link, Document, ISBN 979-8-89176-195-7 Cited by: §1, §3.
- From generation to judgment: opportunities and challenges of LLM-as-a-judge. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), Suzhou, China, pp. 2757–2791. External Links: Link, Document, ISBN 979-8-89176-332-6 Cited by: §2.
- LLMs-as-judges: a comprehensive survey on LLM-based evaluation methods. arXiv preprint arXiv:2412.05579. External Links: Link Cited by: §1, §2.
- From crowdsourced data to high-quality benchmarks: arena-hard and benchbuilder pipeline. In Forty-second International Conference on Machine Learning, ICML 2025, Vancouver, BC, Canada, July 13-19, 2025, A. Singh, M. Fazel, D. Hsu, S. Lacoste-Julien, F. Berkenkamp, T. Maharaj, K. Wagstaff, and J. Zhu (Eds.), Proceedings of Machine Learning Research. External Links: Link Cited by: §2.
- Not all voices are rewarded equally: probing and repairing reward models across human diversity. In Findings of the Association for Computational Linguistics: EMNLP 2025, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), Suzhou, China, pp. 3426–3455. External Links: Link, Document, ISBN 979-8-89176-335-7 Cited by: §5.4.
- Split and merge: aligning position biases in LLM-based evaluators. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP), External Links: Link Cited by: §2.1.
- WildBench: benchmarking llms with challenging tasks from real users in the wild. In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025, External Links: Link Cited by: §2.
- G-eval: NLG evaluation using gpt-4 with better human alignment. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, H. Bouamor, J. Pino, and K. Bali (Eds.), Singapore, pp. 2511–2522. External Links: Link, Document Cited by: §2.
- RewardBench 2: advancing reward model evaluation. In International Conference on Learning Representations (ICLR), External Links: Link Cited by: §1.
- LLM evaluators recognize and favor their own generations. In Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024, A. Globersons, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. M. Tomczak, and C. Zhang (Eds.), External Links: Link Cited by: §1.
- Can you trust LLM judgments? reliability of LLM-as-a-judge. arXiv preprint arXiv:2412.12509. External Links: Link Cited by: §1, §2.1, §2, §5.3.
- Judging the judges: a systematic study of position bias in LLM-as-a-judge. In AACL-IJCNLP, External Links: Link Cited by: §1, §2.1.
- What 1,200 production deployments reveal about LLMOps in 2025. Note: ZenML BlogAccessed 2026-05-07 External Links: Link Cited by: §1, §2.
- Large language models are inconsistent and biased evaluators. arXiv preprint arXiv:2405.01724. External Links: Link Cited by: Appendix H, §1, §2.1, §2.2, §2, §5.3.
- JudgeBench: a benchmark for evaluating LLM-based judges. In International Conference on Learning Representations (ICLR), External Links: Link Cited by: §1, §3.
- Replacing judges with juries: evaluating LLM generations with a panel of diverse models. arXiv preprint arXiv:2404.18796. External Links: Link Cited by: §2.2.
- Large language models are not fair evaluators. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L. Ku, A. Martins, and V. Srikumar (Eds.), Bangkok, Thailand, pp. 9440–9450. External Links: Link, Document Cited by: Appendix H, §1, §2.1.
- Improving LLM-as-a-judge inference with the judgment distribution. In Findings of the Association for Computational Linguistics: EMNLP 2025, C. Christodoulopoulos, T. Chakraborty, C. Rose, and V. Peng (Eds.), Suzhou, China, pp. 23173–23199. External Links: Link, Document, ISBN 979-8-89176-335-7 Cited by: §2.1.
- J1: incentivizing thinking in LLM-as-a-judge via reinforcement learning. arXiv preprint arXiv:2505.10320. External Links: Link Cited by: §1.
- Style over substance: evaluation biases for large language models. In Proceedings of the 31st International Conference on Computational Linguistics, O. Rambow, L. Wanner, M. Apidianaki, H. Al-Khalifa, B. D. Eugenio, and S. Schockaert (Eds.), Abu Dhabi, UAE, pp. 297–312. External Links: Link Cited by: §1, §2.1, §4.8, Rubric sensitivity..
- Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. In Advances in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks Track, External Links: Link Cited by: Appendix H, §1, §1, §2.1, §2.1, §2, §3.
- JudgeLM: fine-tuned large language models are scalable judges. In International Conference on Learning Representations (ICLR), External Links: Link Cited by: §2.2.

Appendix

Appendix A Supplementary Figures

A.1 Cross-Benchmark Rank Instability

Figure 2 expands on the cross-benchmark rank instability summarized in Section 4, plotting each judge’s rank trajectory across MT-Bench, JudgeBench, and RewardBench. The visualization makes individual rank shifts directly readable: a horizontal line indicates a judge that holds its position across benchmarks, and a steep slope identifies a judge whose rank moves substantially as the benchmark changes.

A.2 Consistency Degrades on Hard Benchmarks

Figure 3 visualizes the per-judge change in position flip rate from MT-Bench to JudgeBench across the 16-judge consistency cohort. Highlighting identifies the three judges whose flip rate worsens by at least \(2.4\times\) on the harder benchmark and the two frontier judges (Claude Opus 4.6 and Gemini 3.1 Pro) that improve; the cohort medians (dotted) summarize the cohort-level shift.

Appendix B Complete Results Tables

This section reports per-judge values that the body figures and tables summarize: full agreement statistics on all three benchmarks (Table 4), per-judge cross-benchmark ranks with Cohen’s \(\kappa\) (Table 5), and per-judge consistency-protocol detail for the 17-judge consistency cohort (Table 6). Numerical values are extracted from raw [anonymized]/results/*.json outputs and matched to the display names used elsewhere in the paper.

Appendix C A Priori Hypothesis Details

C.1 Formulation context

Seven hypotheses (H1–H7) were formulated on 2026-04-14, before Phase 6 (frontier-model) data collection began, based on patterns observed in the earlier phases (Phases 1–5). The predictions were recorded internally and were not deposited with an external registry; we do not claim the methodological status of formal pre-registration. We report the unmodified outcome of each hypothesis test below, including the one we did not confirm. The intent of recording the predictions in advance is to make the calibration of our expectations available to readers, not to claim a formal confirmatory frame.

C.2 Per-hypothesis details

Table 7 reports the formal statement, the threshold, the verified observed value, the outcome, and the body subsection in which the test is reported.

C.3 Calibration assessment

Of the seven a priori predictions, three are fully confirmed (H1, H3, H7), one is confirmed for the explicitly-stated subset (H6), two are partially confirmed (H2, H4), and one is refuted (H5). The mixture matters as a calibration signal: hypotheses formulated post hoc would typically be confirmed at a higher rate. The presence of one refutation (H5: RewardBench was predicted to be degenerate, but position-randomized evaluation shows valid \(\kappa\in[0.616,0.898]\)) and two partial outcomes (H2: thinking architecture does not reliably reduce position bias; H4: ceiling holds for the top tier but not the full cohort) indicates that the prediction set was non-trivially hard rather than a curated yes-set. The body §3.4 disclosure reports this in line with the user-facing methodological framing.

Appendix D Model Configuration

Appendix E RewardBench Loader Configuration

The RewardBench evaluation in this study uses per-item position randomization with seed \(42\), matching the contract of the official run_generative.py script that ships with the benchmark. This configuration is necessary because the standard generative-evaluation loader places every chosen response in position A and every rejected response in position B; under that fixed ordering the human label is identically “A” across all items, \(p_{e}\) collapses, and Cohen’s \(\kappa\) degenerates to \(0.000\) for every judge. Per-item randomization with a fixed seed restores a balanced ordering distribution and produces a valid agreement signal.

The validity of the corrected loader is confirmed by the resulting \(\kappa\) distribution: across the 21 judges evaluated on RewardBench, \(\kappa\) values fall in the range \([0.616,0.898]\), well within the substantial-to-near-perfect agreement bands. The full per-judge \(\kappa\) values appear in Table 4 of this appendix.

Appendix F Evaluation Phase Details

The evaluation campaign was conducted in seven phases over a five-week window in March and April 2026. Phases 1–5 evaluated Tier-1 production judges and Tier-2 cost-tier comparisons; Phase 6 added the Tier-3 frontier judges (April 2026 SoTA) on the agreement and bias-audit protocols; Phase 7 added the Tier-3 consistency runs. Total run count is 118, matching the production state ledger. Approximately \(541{,}000\) judgments were produced.

Appendix G Use of AI Assistance

The authors used AI assistance (large language model–based writing assistants) for editing and manuscript-formatting support only: specifically, copy-editing prose, normalizing table and reference formatting, debugging LaTeX layout, and routine BibTeX hygiene. AI assistance was not used for original writing of research claims, for code generation in the evaluation experiments, or for any aspect of research design, hypothesis formulation, data collection, or data analysis. All experimental results, metric computations, and findings reported in this paper were produced and verified by the authors using the framework and methods described in Sections 3 and 4.

Appendix H Responsibility Checklist Notes

Potential Risks.

The paper does not introduce a new judge model, training data, or deployment-ready system, so direct deployment harms are minimal. The principal indirect risks are: (i) selective adoption of the Minimum Viable Validation Protocol (Section 5) partial adoption, e.g. reporting Cohen’s \(\kappa\) alone without the paired position-swap and consistency checks, can produce a false sense of having addressed judge reliability; (ii) interpreting the released evaluation dataset as authoritative beyond its temporal scope (March–April 2026) for judges whose hosted-model endpoints subsequently drift; and (iii) over-correction: practitioners discounting useful evaluation pipelines on the basis of the kappa-deflation finding rather than supplementing them with chance-corrected metrics. We discuss the temporal-scope risk explicitly in the Limitations.

Documentation of Artifacts.

The released artifact is an evaluation dataset of \(118\) evaluation runs spanning \(21\) LLM judges, three benchmarks, and three protocols (approximately \(541{,}000\) individual judgments). Languages: all three source benchmarks are English; multilingual coverage is out of scope (Limitations). Modality: text only. Domains: MT-Bench is general open-ended conversational quality; JudgeBench spans mathematics, coding, creative writing, and analysis; RewardBench is chosen/rejected preference pairs across general instruction-following tasks. Demographic groups: the human-label annotations are inherited from each source benchmark (we do not collect new human annotations); please refer to the cited benchmark papers for annotator demographic coverage. License: the release will be distributed under a permissive open license at publication time. Each released record includes the per-item judge verdict, the judge’s free-form reasoning trace, the raw model response, per-call latency, and the metric values computed for the run, keyed by (judge_id, benchmark, protocol, item_id, run_idx, position_order).

Descriptive Statistics.

For each (judge, benchmark) cell in the agreement and bias-audit tables we report a single value per metric rather than means with confidence intervals: agreement-protocol values are population statistics computed over the full benchmark (not sample estimates), and bias-audit values are point estimates over paired AB+BA evaluations. Consistency-protocol values (test–retest, self-consistency, position flip rate) summarize \(N\in[3,5]\) replicate runs per item and are themselves point estimates of within-judge stability: Phase 4 (Tier 1) uses 5 replicates per item, Phase 5 (Tier 2) uses 5 replicates, and Phase 7 (Tier 3) uses 3 replicates. Cohort-level summary rows (e.g., the “Cohort mean” rows in Table 2 and Appendix Tables 4 and 6) are unweighted means across the judges in the relevant cohort. All single-run reporting was conducted at temperature \(0\) for deterministic generation.

Parameters for Packages.

All evaluation runs were executed using the [anonymized] framework with the following per-protocol settings: temperature \(0\) for all judges, no response caching for the consistency protocol (caching enabled for agreement and bias-audit), and position-swap (AB+BA) debiasing in the consistency and bias-audit protocols. Metric implementations follow canonical formulations: Cohen’s \(\kappa\) uses the standard two-rater nominal formula with no smoothing (Cohen, 1960); Krippendorff’s \(\alpha\) uses the nominal-distance function (Hayes and Krippendorff, 2007; Krippendorff, 2011); tie-excluded exact match follows the pairwise denominator restriction of Zheng et al. (2023); position bias is \(\lvert P(\text{A wins})-0.5\rvert\) over paired AB+BA evaluations (Wang et al., 2024); verbosity bias is the Pearson correlation between response-length differential and verdict (Dubois et al., 2024); test–retest is Krippendorff’s \(\alpha\) across replicate runs (Stureborg et al., 2024). Provider-specific reasoning-suppression settings appear in Table 8 (Appendix D). No external evaluation packages (NLTK, SpaCy, ROUGE, etc.) were used; all metric computations are reproducible from the released [anonymized] framework source.
