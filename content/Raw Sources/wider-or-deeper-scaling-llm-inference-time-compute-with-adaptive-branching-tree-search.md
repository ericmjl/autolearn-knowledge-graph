---
title: "Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive Branching Tree Search"
type: "raw-source"
url: "https://arxiv.org/html/2503.04412v1"
author: "Kou Misaki"
publication: "arXiv"
published: "2024-08-06"
archived: "2026-11-26T02:00:54Z"
---

> [!quote] Original source
> **Author(s):** Kou Misaki  
> **Title:** Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive Branching Tree Search  
> **Published in:** arXiv  
> **Date:** 2024-08-06  
> **Original:** <https://arxiv.org/html/2503.04412v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-wider-or-deeper-scaling-llm-inference-time-compute-with-adaptive-branching-tree-search|Source note]]
Themes: [[Loop engineering]]
Why it was archived: Question 1: when parallel reasoning trees stop adding value over a single deeper tree in test-time compute scaling

## Archived text

UTF8mc

Wider or Deeper? 

Scaling LLM Inference-Time Compute with 

Adaptive Branching Tree Search

Abstract

Recent advances demonstrate that increasing inference-time computation can significantly boost the reasoning capabilities of large language models (LLMs). Although repeated sampling (i.e., generating multiple candidate outputs) is a highly effective strategy, it does not leverage external feedback signals for refinement, which are often available in tasks like coding. In this work, we propose Adaptive Branching Monte Carlo Tree Search (AB-MCTS), a novel inference-time framework that generalizes repeated sampling with principled multi-turn exploration and exploitation. At each node in the search tree, AB-MCTS dynamically decides whether to “go wider” by expanding new candidate responses or “go deeper” by revisiting existing ones based on external feedback signals. We evaluate our method on complex coding and engineering tasks using frontier models. Empirical results show that AB-MCTS consistently outperforms both repeated sampling and standard MCTS, underscoring the importance of combining the response diversity of LLMs with multi-turn solution refinement for effective inference-time scaling.

1 Introduction

Recent work (Li et al., 2022; Lewkowycz et al., 2022; Brown et al., 2024; Wu et al., 2025) has begun to reveal that scaling inference-time computation can significantly boost the performance of large language models (LLMs) on complex tasks. Traditionally, LLM performance improvements have stemmed from training-time scaling—namely, increasing the size of training datasets, model parameters, and computational resources at training (Kaplan et al., 2020; Hoffmann et al., 2022). In contrast, inference-time scaling seeks to improve the performance of an LLM by allocating more computational resources at inference. As we outline in Section 2, there are broadly three types of approaches to achieve inference-time scaling: post-training tuning, reward-guided CoT (Chain-of-Thought), and multiple answer generation. In this paper, we focus on the multiple answer generation approach, which achieves inference-time scaling by generating multiple candidate answers. This approach aims to enhance the LLM’s reasoning and problem-solving abilities on-the-fly, without further training (Li et al., 2022; Wang et al., 2023; Brown et al., 2024; Madaan et al., 2024; Shinn et al., 2024; Li et al., 2024; Tang et al., 2024; Lee et al., 2025; Zhou et al., 2024; Antoniades et al., 2024; Ma et al., 2024). This approach is complementary to other approaches and can easily be incorporated to achieve even higher performance.

A prominent approach of inference-time scaling is repeated sampling, which encompasses methods such as best-of-\(n\) sampling, majority voting, or self-consistency (Wang et al., 2023; Brown et al., 2024; Liang et al., 2024). In this approach, multiple candidate outputs are generated independently from the same prompt, and a final solution is chosen—often via simple heuristics. Repeated sampling has proven effective in challenging tasks such as coding competitions (Li et al., 2022) and the ARC Challenge (Greenblatt, 2024). This strategy leverages the vast output space of LLMs, allowing us to sample a wide variety of distinct responses from a single prompt. The success of repeated sampling illustrates that harnessing this capacity is paramount to achieving effective inference-time scaling.

However, repeated sampling focuses exclusively on exploration and lacks an explicit mechanism for exploitation. In certain real-world scenarios, one can obtain external feedback on a candidate solution. For instance, in coding tasks, one can run tests to evaluate the correctness of generated programs and gather feedback on how to improve them (Madaan et al., 2024; Shinn et al., 2024; Jain et al., 2024). In such settings, it is natural to select promising solutions and refine them based on available feedback, which repeated sampling alone cannot accomplish effectively. Indeed, prior studies (Gou et al., 2024; Huang et al., 2024) have demonstrated that incorporating external feedback leads to improvements, underscoring the importance of using such feedback.

Various approaches have been proposed for exploration and exploitation in such multi-turn settings, but the majority were designed before the power of inference-time scaling was fully recognized. As a result, they are not scalable, i.e., the gain diminishes when the inference-time computational budget is increased. This is essentially because these methods use a fixed “width”—that is, they treat the number of answers generated from the same prompt as a fixed hyperparameter. For example, methods based on standard Monte Carlo Tree Search (MCTS) use a fixed branching factor (i.e., the number of child nodes per state) as a hyperparameter (Zhou et al., 2024; Antoniades et al., 2024; Ma et al., 2024). As demonstrated by the success of repeated sampling, effective inference-time scaling requires leveraging a vast output space, so a fixed width hinders scaling.

In this work, we propose Adaptive Branching Monte Carlo Tree Search (AB-MCTS), a novel inference-time framework that generalizes repeated sampling with multi-turn exploration and exploitation (Figure 1). Unlike traditional MCTS or beam search, AB-MCTS does not fix the width as a static hyperparameter. Instead, at each node of the search tree, AB-MCTS adaptively decides whether to “go wider” by generating new candidate responses or “go deeper” by refining existing ones, leveraging external feedback signals. Under the hood, we formalize our decision process via Bayesian posterior updates, ensuring each expansion balances exploration and exploitation in a principled manner. This design naturally extends repeated sampling, allowing us to harness the vast output space of LLMs when necessary. Consequently, our framework provides a powerful mechanism for balancing exploration and exploitation in the context of LLM inference-time scaling.

We evaluated AB-MCTS on complex coding and machine learning engineering benchmarks (Li et al., 2022; Chan et al., 2024) using frontier models such as GPT-4o (OpenAI, 2024) and DeepSeek-V3 (DeepSeek-AI, 2024), in a scenario that scales up test-time compute by allowing multiple generation calls for each task instance. Under the same computational budget, AB-MCTS consistently achieved better results than previous approaches such as repeated sampling and standard MCTS.

Our contributions are summarized as follows:

- • 

Simultaneous Use of Vast Output Space and Solution Refinement as a New Challenge. We highlight the vast output space of LLMs as a key for inference-time scaling and propose the new paradigm of combining it with solution refinement to manage the exploration–exploitation trade-off.

- • 

AB-MCTS Algorithm. To address this challenge, we introduce AB-MCTS, which systematically decides whether to “go wide” or “go deep.” We present two variants AB-MCTS-M and AB-MCTS-A based on different principles, each offering distinct trade-offs.

- • 

Empirical Validation on Frontier Models and Complex Tasks. In a practical setting using frontier models and real-world complex tasks, we show that AB-MCTS consistently outperforms existing methods.

2 Related Work

Recent studies have increasingly focused on scaling up the compute budget at inference time to enhance the performance of LLMs. Similar to the scaling laws for training compute budgets (Kaplan et al., 2020; Hoffmann et al., 2022), several works have shown that performance benefits can also be realized by increasing inference-time compute (Li et al., 2022; Lewkowycz et al., 2022; Brown et al., 2024; Wu et al., 2025). To position our work within the broader research landscape, we review existing approaches to allocating additional computational resources at inference time. Broadly, these approaches can be grouped into three categories: (1) post-training tuning, (2) reward-guided CoT (Chain-of-Thought), and (3) multiple answer generation. In the paragraphs that follow, we review each category and clarify its connection to our proposed method. We also clarify the difference of our approach from existing MCTS adaptive branching methods.

Inference-Time Scaling by Post-Training Tuning.

A prominent line of research (Jaech et al., 2024; OpenAI et al., 2025; DeepSeek-AI et al., 2025; Ye et al., 2025; Muennighoff et al., 2025; Team et al., 2025) employs post-training strategies that encourage more elaborate reasoning. Representative examples include OpenAI o1 (Jaech et al., 2024), o3 (OpenAI et al., 2025), and DeepSeek-R1 (DeepSeek-AI et al., 2025), where reinforcement learning or supervised fine-tuning using chain-of-thought trajectories deepens LLM reasoning. These techniques enhance the LLM’s ability to produce a single answer more effectively. In contrast, we focus on a framework that repeatedly uses the LLM to generate multiple candidate answers, carrying out trial-and-error with external feedback. Consequently, these lines of research are orthogonal to ours.

Inference-Time Scaling via Reward-Guided CoT.

Another approach to scaling up test-time computation—particularly in mathematical tasks—is to incrementally generate each reasoning step (Lewkowycz et al., 2022; Lightman et al., 2024). Here, a trained reward model often guides the validity of each step, where each step corresponds to a single sentence within an answer (Hao et al., 2023; Yao et al., 2024; Snell et al., 2025; Chen et al., 2024; Gao et al., 2025; Zhao et al., 2024; Qi et al., 2024; Guan et al., 2025; Wu et al., 2025; Zhang et al., 2024). While this demonstrates the value of inference-time scaling, it typically relies on internal (model-based) reward estimates rather than utilizing external feedback. Moreover, even in MCTS-based works for step-by-step reasoning, the branching factor is fixed (Hao et al., 2023; Zhang et al., 2024; Tian et al., 2024; Chen et al., 2024; Park et al., 2024; Gao et al., 2025), thereby failing to leverage the vast output space of LLMs. Furthermore, since this approach focuses on enhancing the performance of generating a single answer without external feedback, it is orthogonal to our research.

Inference-Time Scaling by Multiple Answer Generation.

The approaches closely related to ours involve generating multiple candidate answers at inference time and then selecting or refining them. This approach is in contrast to the reward-guided CoT approach, where each LLM output corresponds to a single reasoning step, rather than a full answer. Early work adopted a self-consistency strategy, in which the model produces several answers and the best is chosen (Li et al., 2022; Wang et al., 2023; Brown et al., 2024). While straightforward, this approach does not refine answers in response to external signals. To improve beyond simple selection, some studies have introduced mechanisms for mutating or refining candidate answers (Madaan et al., 2024; Shinn et al., 2024), naturally suggesting a tree-based search formulation. For example, tree expansions driven by LLMs (Li et al., 2024) or Bayesian methods (Tang et al., 2024) have been explored, although these works do not employ MCTS. Lee et al. (2025) proposes an evolutionary method for answer refinement but relies on crossover operations, which are not always straightforward to define. When MCTS is employed for answer exploration, it typically relies on a fixed number of children per node. For instance, Zhou et al. (2024) introduce Language Agent Tree Search (LATS), which unifies reasoning, acting, and planning in large language models by integrating MCTS with LM-powered value functions and self-reflection. In the software engineering domain, Antoniades et al. (2024) propose SWE-Search, a multi-agent framework that enhances software agents via MCTS and iterative self-improvement, enabling agents to refine their strategies over multiple solution attempts. Similarly, Ma et al. (2024) present RepoUnderstander, where LLM-based agents build a repository knowledge graph in a top-down manner, employ MCTS to explore the repository, and then leverage structured information to generate patches for real-world GitHub issues. Although each approach differs mainly in the design of rewards and actions, they generally adopt “standard MCTS”, by which we mean the conventional MCTS method with a fixed number of child nodes. These methods integrate MCTS into LLM-based decision-making without proposing a new search algorithm from scratch. We refer to these conventional MCTS strategies collectively as “standard MCTS” and compare them with our proposed framework in subsequent sections.

Adaptive Node Branching in MCTS.

Although prior work has explored adaptive branching strategies in MCTS—for instance, progressive widening (Coulom, 2007) and double progressive widening (Couëtoux et al., 2011)—these methods typically rely on heuristic branching rules derived from visitation counts. In contrast, our AB-MCTS method adaptively branches off by leveraging external feedback rather than simply tracking node visits. Also it eliminates the need to hand-craft branching rules tailored to specific problems.

3 Preliminaries

3.1 Problem Setup

In this section, we define the problem setting and introduce the mathematical notation.

We consider problems where the input is a natural language prompt \(t_{\rm in}\) (which may include few-shot examples, task instructions, etc.). Given \(t_{\rm in}\), an LLM produces a natural language output \(t_{\rm out}\), which is then scored by a score evaluator to yield a final score \(r\). We assume \(0\leq r\leq 1\), where higher values of \(r\) correspond to better answers.

This two-stage pipeline can be expressed as:

where the function \(f_{\rm LLM}\) represents an LLM that generates the answer, and \(R\) is the score evaluator. \(f_{\rm LLM}\) is stochastic and may produce different outputs \(t_{\rm out}\) for the same input \(t_{\rm in}\). Here we allow \(t_{\rm out}\) to include information beyond the direct answer (e.g. the reasoning steps), and we assume that \(R\) properly performs the parsing of this answer to perform the score evaluation.

Our framework applies to any task whose final answer can be quantitatively scored, such as programming tasks (Li et al., 2022; Jain et al., 2024), math problems (Gao et al., 2025), and machine learning competitions (Chan et al., 2024). We assume the score evaluator \(R\) is already defined in a task-specific manner, and our goal is to find \(t_{\rm out}\) that attains as high an \(r\) as possible during the inference-time answer search.

In some tasks that mimic real competitions, the ground-truth score evaluator \(R_{\text{gt}}\) (reflecting the correctness of the answer) is not accessible during the answer search stage. For example, in MLE-Bench (Chan et al., 2024), the test dataset used for final evaluation is withheld, and in coding competition tasks (Li et al., 2022; Jain et al., 2024), participants can often only submit their code a limited number of times to obtain the score on hidden test cases. In such situations, to search for the best answer, one may resort to a different score evaluator. For instance, in MLE-Bench, this could be the performance on a public dataset, while in coding competitions it might be the fraction of solved public test cases. For mathematical tasks, a separately trained reward model (Yang et al., 2024) may be used. Throughout this work, we assume there is some accessible score evaluator at the answer search stage that can assess the quality of \(t_{\rm out}\).

3.2 Existing Methods for Inference-Time Answer Search

We now review two standard approaches that focus on exploration or exploitation alone. For an overview of other related approaches, please refer to Section 2.

Only Go Wide: Repeated Sampling.

A straightforward approach to inference-time answer search is to repeatedly sample an answer from the LLM with a nonzero temperature. We refer to each sampling step as the direct answer generation process. By performing it \(n\) times,

we obtain multiple candidate answers. Then, one can select the best answer based on a predefined criterion, such as the highest score \(r\) (best-of-\(n\)), majority voting or self-consistency. Brown et al. (2024) recently showed that as \(n\) increases, the coverage of generated answers improves. A similar approach was employed by AlphaCode (Li et al., 2022) to achieve human-level performance on competitive programming tasks.

Only Go Deep: Sequential Refinement.

Alternatively, we can leverage the answer refinement process and apply it sequentially to perform the answer search. We consider the situation where we already let some answer generator solve the problem at hand \(k\) times, and collected the input-output pairs \(t^{j}_{\rm in}\) and \(t^{j}_{\rm out}\) where \(j\in\{1,\dots,k\}\) for those answer generations.

We define the answer refinement process as a two-step procedure: (1) creation of a new refinement input from the existing input-output pairs, and (2) generation of a new answer \(t_{\rm out}^{k+1}\) from \(t_{\rm in}^{k+1}\). Symbolically,

where \(h_{\rm refine}\) is a refinement input generator that provides all the information necessary for refinement, such as feedback on each answer (e.g. code execution results or errors for coding tasks).

Applying this refinement step iteratively yields \(n\) answers:

for \(m\in\{2,\dots,n\}\). Finally, one selects the best candidate among \(\{t_{\rm out}^{a}\}_{a\in\{1,\dots,n\}}\) based on a chosen criterion, similar to the Repeated Sampling approach.

4 Method

4.1 Adaptive Branching MCTS

We can regard the two methods in the previous section (pure exploration and pure exploitation) as special cases of a tree search: the former expands only from the root node, while the latter continues from the most recently reached leaf node on a single linear path, exploring it in depth without branching outward. Here, we generalize both approaches under the framework of Monte Carlo Tree Search (MCTS)11 1 Unlike conventional MCTS settings, our objective is to maximize the best (rather than cumulative) score, which might suggest focusing solely on exploration. However, with finite action budgets, some exploitation is still needed to achieve the best result (Bubeck et al., 2009), so MCTS remains effective..

We consider constructing a tree \(T\) where each node \(N\) corresponds to an input text \(t_{\rm in}\) and its LLM-generated output \(t_{\rm out}=f_{\rm LLM}(t_{\rm in})\). The expansion from the root does the direct answer generation, while the expansion from a node \(N\) employs the answer refinement using the input-output pairs of \(N\)’s ancestors, including \(N\) itself.

We formulate MCTS iteratively as follows. We begin with a single root node and expand the tree \(n_{\text{nodes}}\) times, ultimately producing \(1+n_{\text{nodes}}\) nodes in total. Each iteration proceeds in three steps:

- 1. 

Selection: choose a node \(N\) in the current tree for expansion.

- 2. 

Expansion: apply direct answer generation or answer refinement to \(N\) to create a new node \(N_{\text{new}}\), appended as a child of \(N\).

- 3. 

Score backup: propagate the score of \(N_{\text{new}}\) up the tree to update the scores of its ancestor nodes, including \(N_{\text{new}}\) itself.

In our setting, we do not perform a separate rollout, because each node’s score \(r\) can be evaluated directly once an output is generated. After \(n_{\text{nodes}}\) expansions, we select the best node based on a chosen criterion.

The backup step ensures that the score of \(N_{\text{new}}\) is shared with its ancestors, enabling more informed node selection in subsequent iterations. We adopt different backup rules in our proposed methods (see Sec 4.2 and 4.3).

Difficulty in Balancing the Breadth and Depth: Unbounded Branching.

Unlike the standard tasks typically tackled by MCTS where the number of possible actions at each node is finite, each call to \(f_{\rm LLM}\) can yield a new output even for the same input, making each node’s branching factor theoretically infinite. Recent studies (Brown et al., 2024) suggest that drawing more samples from the same prompt often boosts performance, so limiting the branching factor might degrade overall results. To explicitly capture this unbounded branching, we introduce a “GEN node” that explicitly represents the action of generating a new child. GEN node exists as a child of all the nodes including the newly expanded ones, and represents the action of generating a new child and append it to the GEN node’s parent node. Algorithm 1 outlines MCTS with such GEN nodes, which we call Adaptive Branching Monte Carlo Tree Search (AB-MCTS).

To employ MCTS with potentially unbounded branching, we must define a selection policy for when to create a new child node (i.e., when to choose the GEN node). Because adding new children expands the tree in the “breadth” direction, this decision critically affects how the tree grows.

In this work, we propose two methods to address unbounded branching: AB-MCTS-M (AB-MCTS with a Mixed model) and AB-MCTS-A (AB-MCTS with node Aggregation). Both follow the overall procedure in Algorithm 1 and utilize Thompson Sampling to balance exploration and exploitation; however, they differ in how they implement node selection step.

Modeling the GEN Node’s Score Probability.

For node selection, we adopt a Bayesian view of each action’s score distribution and apply Thompson Sampling. In standard MCTS, the typical metric for choosing an action is UCT (Kocsis & Szepesvári, 2006), whereas here we replace it with Thompson Sampling, because GEN node does not have children so we are unable to assign UCT score to GEN node. Also, Thompson Sampling has the advantage of allowing node expansion in parallel. Let \(N\) be a node with potential actions

where \(a_{0}\) is the GEN node, and \(a_{1},\dots,a_{n_{\rm child}}\) correspond to already-existing child nodes. Suppose \(P_{T}(r\mid a_{i})\) is the posterior predictive distribution over the score \(r\) if we choose action \(a_{i}\) at the node \(N\) in the tree \(T\). Then Thompson Sampling proceeds by:

- 1. 

Drawing \(r_{a_{i}}\) from \(P_{T}(r\mid a_{i})\) for each action \(a_{i}\).

- 2. 

Selecting \(\hat{a}=\arg\max_{a_{i}\in A}r_{a_{i}}\).

A key question is how to build the posterior \(P_{T}(r\mid a_{i})\), especially for \(a_{0}\) (the GEN node, which may have no observed data). We propose two strategies: a mixed Bayesian model (AB-MCTS-M) and a node aggregation method (AB-MCTS-A).

4.2 AB-MCTS-M: Adaptive Branching MCTS with Mixed model

Motivation.

A natural way to model the GEN node’s score is to separately model two distinct sources of variance. The first arises from the initial answer generation by the GEN node, reflecting variability inherent in the LLM sampling process. The second comes from subsequent refinements, which incorporate the initial answer along with its feedback, thus introducing an additional source of variability. To capture this structure, we employ a mixed-effects model with a random intercept. Specifically, we assign a random effect to each “group”, defined as the child node generated by a GEN node along with its subsequent refinements. This enables us to model variance arising from both the initial answer generation and the refinement processes.

Algorithm Outline.

In AB-MCTS-M, we fit a separate mixed model at each node \(N\) of the MCTS tree, that is, at each sub-step within the MCTS selection step. Specifically, let \(N_{j}\) (\(j=1,\dots,n_{\text{child}}\)) denote the direct child nodes of \(N\), and define \(T_{\text{sub}}(N_{j})\) as the subtree under \(N_{j}\), including \(N_{j}\) itself. For a newly generated node \(\tilde{N}\) where (i) \(j=0\) (i.e. for GEN node) and \(\tilde{N}\) is a direct child of \(N\), or (ii) \(j=1,\dots,n_{\text{child}}\) and \(\tilde{N}\in T_{\text{sub}}(N_{j})\), we assume:

Here, \(\alpha_{j}\) is a “group-level” intercept capturing the quality of the base solution at \(N_{j}\), while \(\sigma_{y}\epsilon_{\tilde{N}}\) represents per-instance noise. The GEN node (action \(a_{0}\)) is treated as a newly introduced group without its own direct observations. However, its group-level intercept \(\alpha_{0}\) is inferred not from the prior alone but rather from the posterior distribution over \(\mu_{\alpha}\) and \(\sigma_{\alpha}\), which is informed by the other observed data.

In experiments, we set priors on \((\mu_{\alpha},\sigma_{\alpha},\sigma_{y})\) and estimate posteriors using MCMC. We then draw from the posterior predictive distribution for Thompson Sampling (Figure 2). Typically, the GEN node’s distribution has higher uncertainty, promoting additional exploration.

Score Backup.

Once a node \(\tilde{N}\) is created, its observed score is added to the history of \(\tilde{N}\) and all its ancestors. This allows AB-MCTS-M to maintain a record of all subtree scores needed for updating the mixed-model posteriors.

4.3 AB-MCTS-A: Adaptive Branching MCTS with Node Aggregation

Motivation.

Another way to split the observations into (i) current refinement and (ii) subsequent refinement is to introduce an explicit “CONT” node for continuing refinement, separate from the “GEN” node for a brand-new child. This design makes it easier to model these two phases separately.

Algorithm Outline.

AB-MCTS-A aggregates all child nodes under a single “CONT” node to represent ongoing refinement. The probability of exploring new children (GEN) versus refining existing ones (CONT) is handled via Thompson Sampling. Specifically, we assign probabilities (or equivalently parameters of posterior distribution) for all the nodes including GEN and CONT nodes.

We propose two families of conjugate priors:

- • 

AB-MCTS-A (Gaussian): uses a normal-inverse-\(\chi^{2}\) prior, suitable if \(r\) may lie outside \([0,1]\).

- • 

AB-MCTS-A (Beta): uses a Beta prior, specialized for scores in \([0,1]\). Because of its simple parameterization, the Beta approach can be more sample efficient in settings where \(r\) is inherently bounded.

Both approaches permit closed-form updates, making them computationally lightweight.

Figure 3 shows a schematic of AB-MCTS-A. When a new node is generated, its observed score is initially “backed up” to the GEN node that created it. For subsequent updates, the score is backed up to the CONT node, allowing us to separate the effect of initial generation from later refinements.

Using these posterior distributions, we perform Thompson Sampling at each step between GEN and CONT nodes. If the GEN node is selected, a new child node is generated; otherwise, one of the existing children is chosen through Thompson Sampling, using the backed-up scores for each child.

Finally, because GEN and CONT nodes appear at the same tree depth in this design, AB-MCTS-A can produce a wider branching structure than AB-MCTS-M. Specifically, generating a node at depth \(d\) requires choosing the CONT node (instead of the GEN node) \(d\) times in succession, making the probability of reaching greater depths decay approximately geometrically with \(d\).

Score Backup.

Whenever a new node is generated, its score is backed up to the GEN node that created it (and all ancestors). In contrast, further refinements of an existing node update the CONT branch’s parameters. Figure 3 shows a schematic depiction. We note again that, because deeper refinement requires repeatedly selecting CONT, the probability of reaching depth \(d\) decays roughly geometrically in practice. At the same time, AB-MCTS-A can explore multiple branches by occasionally choosing the GEN node.

AB-MCTS-A (Gaussian) Parameter Update Rules.

Now we describe the parameter update rule in detail. For the Gaussian case, we use a normal-inverse-\(\chi^{2}\) prior:

where \(r_{n}\) is the observed score.

AB-MCTS-A (Beta) Parameter Update Rules.

Alternatively, if \(r\in[0,1]\), we can use a Beta distribution with the following parameter update rules after observing \(\{r_{n}\}_{n=1}^{N}\):

where \(B(\cdot\mid\alpha,\beta)\) denotes the Beta distribution. We note that, usually this update rule is used in conjunction with the Bernoulli trial, but here we directly use Beta distribution to model the score distribution. In practice, this parameter update rule worked well according to our experimental results.

5 Experiments

5.1 Experimental Setup

Tasks and Datasets.

We evaluated our approach on two benchmarks for code generation (Code Contest (Li et al., 2022)) and machine learning engineering (MLE-Bench (Chan et al., 2024)).

Code Contest is a well-established competitive programming benchmark, providing public tests and hidden tests. We use the public tests to calculate each node’s score and the hidden tests for final evaluation. A solution is counted as correct only if it passes all hidden test cases for a given problem, and the success rate is defined as the fraction of problems for which the chosen solution is fully correct. The prompt templates we used are based on those from previous work (Brown et al., 2024).

For MLE-Bench, which comprises practical machine learning tasks derived from Kaggle competitions, we adopt three low-complexity challenges to enable fair comparisons while keeping the API cost manageable (Chan et al., 2024). Each competition’s training data is randomly split into \(80\)% for training and \(20\)% for validation. The validation set is used to obtain the scores for each node. We select a node with the highest validation score at a given inference budget and then evaluate it on the hidden test set to get the final result. Following previous research (Chan et al., 2024), we use the AIDE scaffold for our experiments.

Models.

We perform our experiments using GPT-4o (gpt-4o-2024-08-06) (OpenAI, 2024) and DeepSeek-V3 (deepseek-chat) (DeepSeek-AI, 2024). Each LLM generates a complete solution in a single API call. We define the generation budget as the maximum number of API calls and set the generation budget for each model and task. For Code Contest, we set the generation budget of 512 for DeepSeek-V3 and 128 for GPT-4o. Due to the expenses associated with API usage, we conducted MLE-Bench experiments with DeepSeek-V3, fixing its generation budget at 128. We set the temperature of GPT-4o to 0.6 for all tasks, while for DeepSeek-V3 we use a temperature of 1.5 for Code Contest and 1.0 for MLE-Bench.

Baselines.

We compare our proposed AB-MCTS approaches with the following methods:

- • 

Repeated Sampling (Best-of-\(n\)): We independently sample up to \(n\) candidate solutions from the LLM using a single prompt. This strategy has shown strong performance on coding tasks (Li et al., 2022; Brown et al., 2024).

- • 

Standard MCTS: As a search-based baseline, we adopt a MCTS approach with UCT-based node selection. Following the previous work (Zhou et al., 2024), we generate 5 child nodes in each expansion step, producing a total node budget of 128. This provides a non-adaptive tree search baseline for comparison.

AB-MCTS Parameters.

We assign the following priors for AB-MCTS-M in Equations 9 and 10:

where \(\mathcal{N}_{\text{half}}\) is the half-normal distribution. The prior parameters are designed such that the prior distribution lies within the range of \([0,1]\). For AB-MCTS-A (Gaussian), we set \(\breve{m}=0\), \(\breve{\kappa}=1\), \(\breve{\nu}=1\), and \(\breve{\tau}^{2}=0.1\) in Equations 11 - 16, and for AB-MCTS-A (Beta), we set \(\breve{\alpha}=0.5\) and \(\breve{\beta}=0.5\) in Equations 17 - 19. We chose these parameters in a way that imposes as few assumptions as possible, thereby minimizing any potential bias.

5.2 Results

Results on Code Contest.

We first evaluate our frameworks on Code Contest. Figure 4 reports the success rate (Pass@1) versus the generation budget for both GPT-4o (left) and DeepSeek-V3 (right). Figure 4 (left) shows that, with GPT-4o, all variants of AB-MCTS exceed Repeated Sampling and Standard MCTS across most budgets, ultimately achieving higher accuracy at the maximum budget of \(2^{7}\). In particular, AB-MCTS-M consistently outperforms both baselines at every examined budget, though its final accuracy is slightly lower than that of AB-MCTS-A (Beta). As shown in Figure 4 (right), when using DeepSeek-V3, all algorithms exhibit similar performance for smaller budgets. However, once the budget exceeds \(2^{6}\), AB-MCTS-A (Beta) and AB-MCTS-M show notably stronger improvements than Repeated Sampling or Standard MCTS. AB-MCTS-A (Gaussian) increases at a slightly slower rate, but it ultimately outperforms the baselines. Overall, these results suggest that, for both GPT-4o and DeepSeek-V3, scaling up the generation budget yields greater performance gains for AB-MCTS compared to the baselines, confirming the effectiveness of our adaptive branching search algorithms.

Results on MLE-Bench.

In Figure 5, we compare AB-MCTS-A (Gaussian) and AB-MCTS-M with Repeated Sampling on three competitions from MLE-Bench. In Nomad2018 (Figure 5, left), both variants of AB-MCTS steadily reduce RMSLE relative to Repeated Sampling. Although brief fluctuations appear for moderate budgets (\(2^{4}\)–\(2^{6}\)), AB-MCTS-M and AB-MCTS-A (Gaussian) eventually converge below \(0.060\) at larger budgets, outperforming the baseline. Using Spooky Author Identification (Figure 5, middle), AB-MCTS also exceeds the baseline as the generation budget increases. Between \(2^{5}\) and \(2^{7}\), AB-MCTS-M and AB-MCTS-A (Gaussian) continue to improve their scores, while Repeated Sampling plateaus near \(0.47\). Lastly, for Random Acts of Pizza (Figure 5, right), AB-MCTS-A (Gaussian) begins to exceed the other methods from around \(2^{3}\) and ultimately surpasses \(0.66\) at higher budgets. Meanwhile, AB-MCTS-M eventually falls slightly behind Repeated Sampling, yet remains competitively close overall.

Taken together, these MLE-Bench results mirror our coding-task results: both AB-MCTS variants generally outperform Repeated Sampling once the budget is sufficiently large. Although AB-MCTS-A (Gaussian) ultimately turns out to be the strongest framework in these three tasks, AB-MCTS-M often scores well in earlier stages, suggesting that it can converge more rapidly in some scenarios. In practice, AB-MCTS-A may be preferable for larger budgets given its generally stronger final performance, whereas AB-MCTS-M could be suitable for limited budgets or faster convergence. Collectively, these results underline the advantages of adaptively deciding when to explore new solutions versus refining promising ones.

6 Conclusions

In this work, we introduced AB-MCTS, an adaptive branching Monte Carlo Tree Search framework for LLM-based answer generation and refinement. By integrating exploration and exploitation via Thompson Sampling in a Bayesian decision-making paradigm, AB-MCTS effectively balances width and depth during search. Experiments on complex coding benchmarks show that AB-MCTS outperforms repeated sampling and conventional MCTS, particularly at larger generation budgets. Moreover, since our method extends MCTS, it could potentially be effective not only for answer generation by LLMs but also for a broader range of tasks involving stochastic outcomes or infinitely many possible actions.

In terms of limitations, AB-MCTS relies on a score evaluator to guide the search, and when the distribution or range of scores varies significantly, tuning its Bayesian priors may introduce additional complexity. We plan to investigate improvements toward more robust methods that can better handle variations in score evaluator behavior. Additionally, our approach assumes the existence of a reliable score evaluator, but developing such an evaluator itself can be challenging depending on the task. We believe addressing these challenges will further enhance the applicability and effectiveness of AB-MCTS across a wider range of practical problems.

Author Contributions

Kou Misaki co-designed and implemented the AB-MCTS algorithm. Yuichi Inoue led the experimental evaluation, while Yuki Imajuku, So Kuroki, and Taishi Nakamura carried out the experimental evaluation. Takuya Akiba initiated and coordinated the project, defined its direction, co-designed the algorithm, and advised on the experimental design.

References

- Antoniades et al. (2024) Antonis Antoniades, Albert Örwall, Kexun Zhang, Yuxi Xie, Anirudh Goyal, and William Wang. Swe-search: Enhancing software agents with monte carlo tree search and iterative refinement, 2024. URL https://arxiv.org/abs/2410.20285.
- Brown et al. (2024) Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V Le, Christopher Ré, and Azalia Mirhoseini. Large language monkeys: Scaling inference compute with repeated sampling. arXiv preprint arXiv:2407.21787, 2024.
- Bubeck et al. (2009) Sébastien Bubeck, Rémi Munos, and Gilles Stoltz. Pure exploration in multi-armed bandits problems. In Algorithmic Learning Theory: 20th International Conference, ALT 2009, Porto, Portugal, October 3-5, 2009. Proceedings 20, pp. 23–37. Springer, 2009.
- Chan et al. (2024) Jun Shern Chan, Neil Chowdhury, Oliver Jaffe, James Aung, Dane Sherburn, Evan Mays, Giulio Starace, Kevin Liu, Leon Maksin, Tejal Patwardhan, et al. Mle-bench: Evaluating machine learning agents on machine learning engineering. arXiv preprint arXiv:2410.07095, 2024.
- Chen et al. (2024) Guoxin Chen, Minpeng Liao, Chengxi Li, and Kai Fan. Alphamath almost zero: Process supervision without process. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024. URL https://openreview.net/forum?id=VaXnxQ3UKo.
- Couëtoux et al. (2011) Adrien Couëtoux, Jean-Baptiste Hoock, Nataliya Sokolovska, Olivier Teytaud, and Nicolas Bonnard. Continuous upper confidence trees. In Learning and Intelligent Optimization: 5th International Conference, LION 5, Rome, Italy, January 17-21, 2011. Selected Papers 5, pp. 433–445. Springer, 2011.
- Coulom (2007) Rémi Coulom. Computing “elo ratings” of move patterns in the game of go. ICGA journal, 30(4):198–208, 2007.
- DeepSeek-AI (2024) DeepSeek-AI. Deepseek-v3 technical report, 2024. URL https://arxiv.org/abs/2412.19437.
- DeepSeek-AI et al. (2025) DeepSeek-AI, Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, Xiaokang Zhang, Xingkai Yu, Yu Wu, Z. F. Wu, Zhibin Gou, Zhihong Shao, Zhuoshu Li, Ziyi Gao, Aixin Liu, Bing Xue, Bingxuan Wang, Bochao Wu, Bei Feng, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, Damai Dai, Deli Chen, Dongjie Ji, Erhang Li, Fangyun Lin, Fucong Dai, Fuli Luo, Guangbo Hao, Guanting Chen, Guowei Li, H. Zhang, Han Bao, Hanwei Xu, Haocheng Wang, Honghui Ding, Huajian Xin, Huazuo Gao, Hui Qu, Hui Li, Jianzhong Guo, Jiashi Li, Jiawei Wang, Jingchang Chen, Jingyang Yuan, Junjie Qiu, Junlong Li, J. L. Cai, Jiaqi Ni, Jian Liang, Jin Chen, Kai Dong, Kai Hu, Kaige Gao, Kang Guan, Kexin Huang, Kuai Yu, Lean Wang, Lecong Zhang, Liang Zhao, Litong Wang, Liyue Zhang, Lei Xu, Leyi Xia, Mingchuan Zhang, Minghua Zhang, Minghui Tang, Meng Li, Miaojun Wang, Mingming Li, Ning Tian, Panpan Huang, Peng Zhang, Qiancheng Wang, Qinyu Chen, Qiushi Du, Ruiqi Ge, Ruisong Zhang, Ruizhe Pan, Runji Wang, R. J. Chen, R. L. Jin, Ruyi Chen, Shanghao Lu, Shangyan Zhou, Shanhuang Chen, Shengfeng Ye, Shiyu Wang, Shuiping Yu, Shunfeng Zhou, Shuting Pan, S. S. Li, Shuang Zhou, Shaoqing Wu, Shengfeng Ye, Tao Yun, Tian Pei, Tianyu Sun, T. Wang, Wangding Zeng, Wanjia Zhao, Wen Liu, Wenfeng Liang, Wenjun Gao, Wenqin Yu, Wentao Zhang, W. L. Xiao, Wei An, Xiaodong Liu, Xiaohan Wang, Xiaokang Chen, Xiaotao Nie, Xin Cheng, Xin Liu, Xin Xie, Xingchao Liu, Xinyu Yang, Xinyuan Li, Xuecheng Su, Xuheng Lin, X. Q. Li, Xiangyue Jin, Xiaojin Shen, Xiaosha Chen, Xiaowen Sun, Xiaoxiang Wang, Xinnan Song, Xinyi Zhou, Xianzu Wang, Xinxia Shan, Y. K. Li, Y. Q. Wang, Y. X. Wei, Yang Zhang, Yanhong Xu, Yao Li, Yao Zhao, Yaofeng Sun, Yaohui Wang, Yi Yu, Yichao Zhang, Yifan Shi, Yiliang Xiong, Ying He, Yishi Piao, Yisong Wang, Yixuan Tan, Yiyang Ma, Yiyuan Liu, Yongqiang Guo, Yuan Ou, Yuduan Wang, Yue Gong, Yuheng Zou, Yujia He, Yunfan Xiong, Yuxiang Luo, Yuxiang You, Yuxuan Liu, Yuyang Zhou, Y. X. Zhu, Yanhong Xu, Yanping Huang, Yaohui Li, Yi Zheng, Yuchen Zhu, Yunxian Ma, Ying Tang, Yukun Zha, Yuting Yan, Z. Z. Ren, Zehui Ren, Zhangli Sha, Zhe Fu, Zhean Xu, Zhenda Xie, Zhengyan Zhang, Zhewen Hao, Zhicheng Ma, Zhigang Yan, Zhiyu Wu, Zihui Gu, Zijia Zhu, Zijun Liu, Zilin Li, Ziwei Xie, Ziyang Song, Zizheng Pan, Zhen Huang, Zhipeng Xu, Zhongyu Zhang, and Zhen Zhang. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning, 2025. URL https://arxiv.org/abs/2501.12948.
- Gao et al. (2025) Bofei Gao, Feifan Song, Zhe Yang, Zefan Cai, Yibo Miao, Chenghao Ma, Shanghaoran Quan, Liang Chen, Qingxiu Dong, Runxin Xu, Zhengyang Tang, Benyou Wang, Daoguang Zan, Ge Zhang, Lei Li, Lei Sha, Yichang Zhang, Xuancheng Ren, Tianyu Liu, and Baobao Chang. Omni-MATH: A universal olympiad level mathematic benchmark for large language models. In The Thirteenth International Conference on Learning Representations, 2025. URL https://openreview.net/forum?id=yaqPf0KAlN.
- Gou et al. (2024) Zhibin Gou, Zhihong Shao, Yeyun Gong, yelong shen, Yujiu Yang, Nan Duan, and Weizhu Chen. CRITIC: Large language models can self-correct with tool-interactive critiquing. In The Twelfth International Conference on Learning Representations, 2024. URL https://openreview.net/forum?id=Sx038qxjek.
- Greenblatt (2024) Ryan Greenblatt. Getting 50% (sota) on arc-agi with gpt-4o. https://www.lesswrong.com/posts/Rdwui3wHxCeKb7feK/getting-50-sota-on-arc-agi-with-gpt-4o, 2024. Accessed: January 21, 2025.
- Guan et al. (2025) Xinyu Guan, Li Lyna Zhang, Yifei Liu, Ning Shang, Youran Sun, Yi Zhu, Fan Yang, and Mao Yang. rstar-math: Small llms can master math reasoning with self-evolved deep thinking, 2025. URL https://arxiv.org/abs/2501.04519.
- Hao et al. (2023) Shibo Hao, Yi Gu, Haodi Ma, Joshua Jiahua Hong, Zhen Wang, Daisy Zhe Wang, and Zhiting Hu. Reasoning with language model is planning with world model, 2023. URL https://arxiv.org/abs/2305.14992.
- Hoffmann et al. (2022) Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, Tom Hennigan, Eric Noland, Katie Millican, George van den Driessche, Bogdan Damoc, Aurelia Guy, Simon Osindero, Karen Simonyan, Erich Elsen, Jack W. Rae, Oriol Vinyals, and Laurent Sifre. Training compute-optimal large language models, 2022. URL https://arxiv.org/abs/2203.15556.
- Huang et al. (2024) Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou. Large language models cannot self-correct reasoning yet. In The Twelfth International Conference on Learning Representations, 2024. URL https://openreview.net/forum?id=IkmD3fKBPQ.
- Jaech et al. (2024) Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richardson, Ahmed El-Kishky, Aiden Low, Alec Helyar, Aleksander Madry, Alex Beutel, Alex Carney, et al. Openai o1 system card. arXiv preprint arXiv:2412.16720, 2024.
- Jain et al. (2024) Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica. Livecodebench: Holistic and contamination free evaluation of large language models for code. arXiv preprint arXiv:2403.07974, 2024.
- Kaplan et al. (2020) Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models. arXiv preprint arXiv:2001.08361, 2020. URL https://arxiv.org/abs/2001.08361.
- Kocsis & Szepesvári (2006) Levente Kocsis and Csaba Szepesvári. Bandit based monte-carlo planning. In European conference on machine learning, pp. 282–293. Springer, 2006.
- Lee et al. (2025) Kuang-Huei Lee, Ian Fischer, Yueh-Hua Wu, Dave Marwood, Shumeet Baluja, Dale Schuurmans, and Xinyun Chen. Evolving deeper llm thinking, 2025. URL https://arxiv.org/abs/2501.09891.
- Lewkowycz et al. (2022) Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer, Henryk Michalewski, Vinay Ramasesh, Ambrose Slone, Cem Anil, Imanol Schlag, Theo Gutman-Solo, et al. Solving quantitative reasoning problems with language models. Advances in Neural Information Processing Systems, 35:3843–3857, 2022.
- Li et al. (2024) Jierui Li, Hung Le, Yingbo Zhou, Caiming Xiong, Silvio Savarese, and Doyen Sahoo. Codetree: Agent-guided tree search for code generation with large language models, 2024. URL https://arxiv.org/abs/2411.04329.
- Li et al. (2022) Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, et al. Competition-level code generation with alphacode. Science, 378(6624):1092–1097, 2022.
- Liang et al. (2024) Zhenwen Liang, Ye Liu, Tong Niu, Xiangliang Zhang, Yingbo Zhou, and Semih Yavuz. Improving llm reasoning through scaling inference computation with collaborative verification, 2024. URL https://arxiv.org/abs/2410.05318.
- Lightman et al. (2024) Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In The Twelfth International Conference on Learning Representations, 2024. URL https://openreview.net/forum?id=v8L0pN6EOi.
- Ma et al. (2024) Yingwei Ma, Qingping Yang, Rongyu Cao, Binhua Li, Fei Huang, and Yongbin Li. How to understand whole software repository?, 2024. URL https://arxiv.org/abs/2406.01422.
- Madaan et al. (2024) Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al. Self-refine: Iterative refinement with self-feedback. Advances in Neural Information Processing Systems, 36, 2024.
- Muennighoff et al. (2025) Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi, Luke Zettlemoyer, Percy Liang, Emmanuel Candès, and Tatsunori Hashimoto. s1: Simple test-time scaling, 2025. URL https://arxiv.org/abs/2501.19393.
- OpenAI (2024) OpenAI. Gpt-4o system card, 2024. URL https://arxiv.org/abs/2410.21276.
- OpenAI et al. (2025) OpenAI, :, Ahmed El-Kishky, Alexander Wei, Andre Saraiva, Borys Minaev, Daniel Selsam, David Dohan, Francis Song, Hunter Lightman, Ignasi Clavera, Jakub Pachocki, Jerry Tworek, Lorenz Kuhn, Lukasz Kaiser, Mark Chen, Max Schwarzer, Mostafa Rohaninejad, Nat McAleese, o3 contributors, Oleg Mürk, Rhythm Garg, Rui Shu, Szymon Sidor, Vineet Kosaraju, and Wenda Zhou. Competitive programming with large reasoning models, 2025. URL https://arxiv.org/abs/2502.06807.
- Park et al. (2024) Sungjin Park, Xiao Liu, Yeyun Gong, and Edward Choi. Ensembling large language models with process reward-guided tree search for better complex reasoning, 2024. URL https://arxiv.org/abs/2412.15797.
- Qi et al. (2024) Zhenting Qi, Mingyuan Ma, Jiahang Xu, Li Lyna Zhang, Fan Yang, and Mao Yang. Mutual reasoning makes smaller llms stronger problem-solvers, 2024. URL https://arxiv.org/abs/2408.06195.
- Shinn et al. (2024) Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. Advances in Neural Information Processing Systems, 36, 2024.
- Snell et al. (2025) Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling test-time compute optimally can be more effective than scaling LLM parameters. In The Thirteenth International Conference on Learning Representations, 2025. URL https://openreview.net/forum?id=4FWAwZtd2n.
- Tang et al. (2024) Hao Tang, Keya Hu, Jin Peng Zhou, Sicheng Zhong, Wei-Long Zheng, Xujie Si, and Kevin Ellis. Code repair with llms gives an exploration-exploitation tradeoff, 2024. URL https://arxiv.org/abs/2405.17503.
- Team et al. (2025) Kimi Team, Angang Du, Bofei Gao, Bowei Xing, Changjiu Jiang, Cheng Chen, Cheng Li, Chenjun Xiao, Chenzhuang Du, Chonghua Liao, Chuning Tang, Congcong Wang, Dehao Zhang, Enming Yuan, Enzhe Lu, Fengxiang Tang, Flood Sung, Guangda Wei, Guokun Lai, Haiqing Guo, Han Zhu, Hao Ding, Hao Hu, Hao Yang, Hao Zhang, Haotian Yao, Haotian Zhao, Haoyu Lu, Haoze Li, Haozhen Yu, Hongcheng Gao, Huabin Zheng, Huan Yuan, Jia Chen, Jianhang Guo, Jianlin Su, Jianzhou Wang, Jie Zhao, Jin Zhang, Jingyuan Liu, Junjie Yan, Junyan Wu, Lidong Shi, Ling Ye, Longhui Yu, Mengnan Dong, Neo Zhang, Ningchen Ma, Qiwei Pan, Qucheng Gong, Shaowei Liu, Shengling Ma, Shupeng Wei, Sihan Cao, Siying Huang, Tao Jiang, Weihao Gao, Weimin Xiong, Weiran He, Weixiao Huang, Wenhao Wu, Wenyang He, Xianghui Wei, Xianqing Jia, Xingzhe Wu, Xinran Xu, Xinxing Zu, Xinyu Zhou, Xuehai Pan, Y. Charles, Yang Li, Yangyang Hu, Yangyang Liu, Yanru Chen, Yejie Wang, Yibo Liu, Yidao Qin, Yifeng Liu, Ying Yang, Yiping Bao, Yulun Du, Yuxin Wu, Yuzhi Wang, Zaida Zhou, Zhaoji Wang, Zhaowei Li, Zhen Zhu, Zheng Zhang, Zhexu Wang, Zhilin Yang, Zhiqi Huang, Zihao Huang, Ziyao Xu, and Zonghan Yang. Kimi k1.5: Scaling reinforcement learning with llms, 2025. URL https://arxiv.org/abs/2501.12599.
- Tian et al. (2024) Ye Tian, Baolin Peng, Linfeng Song, Lifeng Jin, Dian Yu, Haitao Mi, and Dong Yu. Toward self-improvement of llms via imagination, searching, and criticizing, 2024. URL https://arxiv.org/abs/2404.12253.
- Wang et al. (2023) Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models, 2023. URL https://arxiv.org/abs/2203.11171.
- Wu et al. (2025) Yangzhen Wu, Zhiqing Sun, Shanda Li, Sean Welleck, and Yiming Yang. Inference scaling laws: An empirical analysis of compute-optimal inference for LLM problem-solving. In The Thirteenth International Conference on Learning Representations, 2025. URL https://openreview.net/forum?id=VNckp7JEHn.
- Yang et al. (2024) An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao, Bowen Yu, Chengpeng Li, Dayiheng Liu, Jianhong Tu, Jingren Zhou, Junyang Lin, Keming Lu, Mingfeng Xue, Runji Lin, Tianyu Liu, Xingzhang Ren, and Zhenru Zhang. Qwen2.5-math technical report: Toward mathematical expert model via self-improvement, 2024. URL https://arxiv.org/abs/2409.12122.
- Yao et al. (2024) Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. Advances in Neural Information Processing Systems, 36, 2024.
- Ye et al. (2025) Yixin Ye, Zhen Huang, Yang Xiao, Ethan Chern, Shijie Xia, and Pengfei Liu. Limo: Less is more for reasoning, 2025. URL https://arxiv.org/abs/2502.03387.
- Zhang et al. (2024) Dan Zhang, Sining Zhoubian, Ziniu Hu, Yisong Yue, Yuxiao Dong, and Jie Tang. Rest-mcts*: Llm self-training via process reward guided tree search, 2024. URL https://arxiv.org/abs/2406.03816.
- Zhao et al. (2024) Yu Zhao, Huifeng Yin, Bo Zeng, Hao Wang, Tianqi Shi, Chenyang Lyu, Longyue Wang, Weihua Luo, and Kaifu Zhang. Marco-o1: Towards open reasoning models for open-ended solutions, 2024. URL https://arxiv.org/abs/2411.14405.
- Zhou et al. (2024) Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, and Yu-Xiong Wang. Language agent tree search unifies reasoning, acting, and planning in language models. In Forty-first International Conference on Machine Learning, 2024. URL https://openreview.net/forum?id=njwv9BsGHF.
