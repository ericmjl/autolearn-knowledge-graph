---
title: "Scaling Test-time Compute for LLM Agents"
type: "raw-source"
url: "https://arxiv.org/html/2506.12928v1"
author: "Wangchunshu Zhou"
publication: "arXiv"
published: "2026-08-24"
archived: "2026-11-28T03:01:58Z"
---

> [!quote] Original source
> **Author(s):** Wangchunshu Zhou  
> **Title:** Scaling Test-time Compute for LLM Agents  
> **Published in:** arXiv  
> **Date:** 2026-08-24  
> **Original:** <https://arxiv.org/html/2506.12928v1>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-scaling-test-time-compute-for-llm-agents|Source note]]
Themes: [[Evals and agent quality]], [[Agent design patterns]]
Why it was archived: Does diversity-beats-depth test-time scaling hold across model families and agents, not only QwQ-class reasoning models?

## Archived text

Wangchunshu Zhou at \checkdata[Code]https://github.com/OPPO-PersonalAI/OAgents

Scaling Test-time Compute for LLM Agents

Abstract

Scaling test time compute has shown remarkable success in improving the reasoning abilities of large language models (LLMs). In this work, we conduct the first systematic exploration of applying test-time scaling methods to language agents and investigate the extent to which it improves their effectiveness. Specifically, we explore different test-time scaling strategies, including: (1) parallel sampling algorithms; (2) sequential revision strategies; (3) verifiers and merging methods; (4)strategies for diversifying rollouts. We carefully analyze and ablate the impact of different design strategies on applying test-time scaling on language agents, and have follow findings: 1. Scaling test time compute could improve the performance of agents. 2. Knowing when to reflect is important for agents. 3. Among different verification and result merging approaches, the list-wise method performs best. 4. Increasing diversified rollouts exerts a positive effect on the agent’s task performance.

1 Introduction

Language agents demonstrate exceptional capabilities in various domains [26, 33, 9, 5, 34, 35].For example, LangChain[24] connects LLMs with various tools to solve different tasks in an end-to-end manner, while Meta-GPT[9] enables multiple AI Agents to take on different roles and collaborate to accomplish tasks. Recently, long-thinking models like O1 [11] and R1 [8] showcase excellent reasoning abilities of Large Language Models (LLMs). Recent approaches [15, 18] leverage the extended thinking capabilities of long-activation models for planning, code writing, tool calling, and completing complex tasks. However, despite LLMs’ strong capabilities, they still struggle to match human performance on complex search and reasoning tasks [32, 12]. This occurs due to remaining limitations in model capabilities, errors in task planning and question answering, and issues with complex tool calling abilities.

Increasing computational resources during the inference phase greatly enhances LLMs’ performance. Some works [19, 20] improve model exploration during inference through different sampling strategies, achieving excellent scores in challenging areas like mathematical reasoning.Charlie Snell et al.[25] investigated the effects of scaling inference-time computational consumption, while Wei Xiong et al.[31] focused on enhancing model performance through self-correction methods. However, directly applying TTS methods to the Agentic Framework presents many challenges. Unlike LLMs that solve specific problems in an end-to-end manner, Agents typically decompose complex problems into distinct steps, invoking multiple models sequentially for resolution. Due to the extended sequence of steps and the accumulation of errors, traditional TTS methods (e.g., BoN) can significantly undermine the final outcome, because they randomly generate N responses at each step.

To address the aforementioned challenges, we first conduct a systematic exploration of test-time scaling methods for language agents. First, we investigate the effectiveness of different parallel sampling methods for agentic test-time scaling, including variants of Best-of-N (BoN), beam search, and tree search algorithms. We adapt and implement these parallel sampling mechanisms within language agents and showing that despite simplicity, BoN achieves the optimal performance. Subsequently, we investigate the effectiveness of various sequential revision techniques, such as reflection and self-refinement, for language agents. We introduce a reflection agent to summarize and reflect based on the current state and recent actions/observations to help the agent consistently progress toward accomplishing the task. Experimental results show that the direct gains from having the agent perform reflection at each step are not obvious. Instead, allowing the agent to perform reflection when it performs poorly in the current step brings certain benefits. This indicates that knowing when the agent should reflect is more important than having the agent perform reflection at every step directly. Finally, we conduct a detailed study on the impact of different verify and result merging methods, including voting, scoring, and list-wise approaches. Our experimental results demonstrate that whether for merge results methods or verify methods, using the list-wise method outperforms other methods. This provides an effective verify method reference for agentic frameworks. Finally, we test different strategies to expand the agent’s exploration space and enhance the diversity of different rollouts, and propose a multi-agent collaborative sampling strategy. Experimental results indicate that performance under multi-agent collaboration surpasses that of a single agent.

Our core contributions are:

- • 

We explore the application of different parallel sampling strategies in agentic frameworks. Through parallel sampling strategies, agent performance can be significantly improved.

- • 

We study the impact of sequential revision techniques in agentic frameworks. In particular, we point out that it is very important for agents to know when they should perform revision.

- • 

We also conduct detailed comparative analysis of different verify and result merge strategies. Experiments show that the list-wise method significantly outperforms other methods.

2 ATTS: Agentic Test-Time Scaling

In this section, we describe and compare different strategies for agentic test-time scaling including: (1) Parallel Sampling Algorithms; (2) Sequential Revision Strategies; (3) Verifier and Result Merging Methods; (4) Strategies for Diversifying Rollouts.

2.1 Parallel Sampling Algorithms

To establish a comprehensive evaluation framework for our proposed methods, we regard several parallel sampling algorithms that are commonly used in the test-time scaling (TTS) domain as baselines.

Best-of-N (BoN) Give a sample times \(N\) and question \(Q\), the Best-of-N (BoN) method samples \(N\) independent responses from the LLMs:

then selects the best answer by verifying model. The effectiveness of BoN relies heavily on the quality of the reward model and the diversity of sampled candidates.

Step-wise-Best-of-N (BoN-wise) BoN selects the optimal result from candidate trajectories as the final response, while BoN-wise generates \(N\) responses at each steps. Specifically, given the thoughts \(\{T1,T2,...,T_{t-1}\}\) from the previous step at time \(t\), BoN-wise generate \(N\) responses:

then it select the optimal response as thought \(T_{t}\) at time \(t\).

Beam Search Beam search maintains a fixed-size beam size \(K\) at each step. Specifically, at time \(t\), it generates \(N\) responses for each leaf nodes \(LN_{i}\), then maintains the most suitable \(K\) responses that :

Most promising partial solutions at each generation step. This algorithm prunes less promising candidates early in the generation process based on cumulative log-probabilities or reward scores.

DVTS (Diverse Verifier Tree Search): DVTS decomposes the task into K subtrees, where each subtree operates as an independent beam search algorithm. By exploring multiple subtrees in parallel, DVTS achieves more diverse search behavior. Under the same computational budget, it finds higher-quality solutions more effectively than a single beam search with deep exploration.

2.2 Sequential Revision Strategies

Besides, given the previous steps \(\{T_{1},T_{2},...,T_{t-1}\}\) at time \(t\), we leverage a reflection model RefM, to summarize information:

To ensure the model understands when reflection is needed, we use a verify model to objectively score each step of the model to represent the quality of the current step action, and set different score \(Threshold\). If and only if the model action score is less than the \(Threshold\), the \(Sum_{t}\) is added into the LLM to generate the responses for time \(t\).

2.3 Verifiers and Merging Methods

Verifiers

To enable agents to receive positive feedback signals during the sampling process, we have designed two different process-based reward functions that evaluate the value of each sampling action.

scoring PRM: we score each thought steps at each intermediate step \(t\) to revise the final response. For \(N\) thought steps \(\{T_{1},T_{2},...,T_{N}\}\) generated at step \(t\), we utilize a LLM as Reward Model (RM), to obtain the score of each response \(S_{i}=RM(T_{current\_i})\).

list-wise PRM: Another commonly used verify method is to select the optimal trajectory through direct comparison. For \(N\) thought steps \(\{T_{1},T_{2},\ldots,T_{N}\}\) generated at step \(t\), we provide all candidate actions to the LLM, asking it to select the optimal trajectory from among them, \(S_{i}=\text{RM}(T_{\text{current\_i}})\)

Result Merging Methods

we compare mainstream Result Merging approaches, including voting: Directly select the majority from all candidates, scoring: using verify for direct scoring, and list-wise: where the model directly selects the optimal answer from candidate responses.

2.4 Diversifying Rollouts

The efficiency of Parallel Sampling Algorithms is influenced by diversifying rollouts—more diverse rollouts mean the agent has a greater chance of exploring and discovering the correct answer. LLMs generate diverse candidates by controlling hyperparameters such as temperature and top_p.

However, in agent frameworks, employing multi-agents to collaboratively accomplish the same task often enhances task performance. To further increase diversity in the agents’ sampling process, we utilize different LLMs as rollout models. Different LLMs often exhibit distinct capability profiles; some excel in coding, while others demonstrate exceptional performance in tool using. We have designed various agent combinations to maximize rollout diversity.

3 Experiments

3.1 Experiments Setting

To thoroughly investigate the effects of TTS algorithms within the agentic framework, we conduct the following comparative experiments:

Comparison of Different parallel sampling algorithms

In order to comprehensively compare different parallel sampling algorithms in the agentic framework, we select mainstream parallel sampling algorithms, including BON, BON-wise, Beam-Search, Tree search, and conduct comparative experiments under identical experimental settings. We ensure a sampling width of 4, and for Beam-Search and Tree-search, we fix the beam-size at 2.

Comparison of different Sequential Revision Strategies

To investigate how self-reflection affect agent performance, focusing on when and how reflection should be applied. We set up the following two settings: Step-based Reflection: Reflection is conducted at every step to enable continuous error correction. Score-based Reflection: Initially, the Verify model scores each step of the agent’s process. The agent performs reflection only when a step’s score falls below a predefined threshold. To further explore how the frequency of reflection affects performance, we conduct ablation studies using three triggering thresholds: &lt;8 (frequent), &lt;5 (moderate), and &lt;2 (selective).

Comparison of Different Verifiers and Merging Methods

To investigate the impact of different Verifiers and Merging Methods. First, we compare the performance differences among three mainstream result merging methods, then based on the optimal result merging method, we compare the effects of different verifiers.

Diversifying Rollouts

We explore this influence from two perspectives: on the one hand, we study the differences in agent capabilities under different sampling widths; on the other hand, we introduce multi-agent rollouts to explore the benefits of increasing rollout diversity.

3.2 Baseline

We select the SmoLAgents framework as our baseline. In this framework, agents take on different roles such as code actor and tool calling. In order to more intuitively compare the differences between various TTS algorithms, we remove the nesting of ToolAgent in the original smolagent framework and only use CodeAgent to directly call tools. We choose GPT-4.1 as the baseline model for the majority of our experiments. Additionally, we select current state-of-the-art models including Claude-3-7, Gemini-2.5-Pro, and Claude-3-5 for comparative experiments involving mixed models.

3.3 Benchmark

We choose GAIA[22] as our primary evaluation benchmark. The GAIA validation dataset contains 165 data samples across three different difficulty levels - level1, level2, and level3. It primarily assesses agents’ capabilities in web search and handling multimodal files.

4 Experimental Results

4.1 Comparison of Different Parallel Sampling Algorithms

As shown in Table 1, we compare the application of mainstream parallel sampling algorithms in agentic frameworks. The experimental results demonstrate that by applying the parallel sampling algorithms, agents can achieve superior performance. Compared to the baseline, BoN, BoN-wise, and Beam-Search achieve significant performance gains, while DVTS performs similarly to the baseline. These results demonstrate the general effectiveness of Parallel Sampling Algorithms in the agentic framework. Meanwhile, different parallel sampling algorithms exhibit varying performance characteristics.

The BoN algorithm achieves the best performance gains, with an eight-point improvement over the baseline, and achieves SOTA results on level 1 and level 2. These two levels are heavily dependent on the agent’s ability to call and use tools. Under the BoN algorithm, the agent is given more opportunities to repeatedly attempt similar tasks, which enhances performance particularly on simpler and mid-level difficult problems. BoN-wise achieves the second-best results after BoN, with a three-point improvement over the baseline. In particular, BoN-wise achieves the best performance on the most difficult level3 problems, surpassing both the baseline and BoN. BoN-wise allows for the largest exploration space at each decision node, further demonstrating that increasing step-wise exploration leads to better performance on complex tasks.

Notably, Beam-search and DVTS show no significant improvement over baseline. This is because although these algorithms can significantly increase the agent’s exploration space, their exploration also depends on the accuracy of signals provided by the verify model, which prevents the agent from stably approaching the correct answers.

4.2 The impact of different Sequential Revision Strategies

As shown in Table 2, we first compare the baseline agent with the reflection-enabled agent to assess the effectiveness of self-reflection. The baseline achieves an overall score of 55.76, while the reflection model scores slightly lower at 55.15, suggesting that reflection, while enabling error correction, may also disrupt the model’s reasoning flow. At Level 1, reflection significantly improves performance (71.7), indicating its benefit for simple tasks where minor errors can be quickly corrected without much overhead. However, at Level 2, reflection underperforms compared to the baseline, especially when applied frequently, suggesting that moderate-complexity tasks are more susceptible to disruption from excessive introspection. At Level 3, reflection leads to a moderate improvement (34.62), showing its value in preventing critical failures in complex scenarios, although overall performance remains limited by task difficulty.

As reflection introduces both benefits and potential disruptions, we examine how varying the frequency of reflection impacts task execution across different levels of complexity. Frequent reflection (threshold &lt;8) results in the lowest overall score (53.66), particularly hurting performance at Level 2 due to reasoning interruptions. Moderate reflection (&lt;5) yields even lower performance (52.12), whereas selective reflection (&lt;2) achieves the best result (56.36), outperforming other strategies across all levels. This indicates that restricting reflection to only the most critical steps minimizes disruption while still allowing meaningful error correction. These findings suggest that effective use of reflection depends heavily on its application frequency and timing—low-frequency, context-aware reflection is most beneficial, especially for maintaining coherence in multi-step reasoning processes.

4.3 The impact of different verifiers and result merging methods

The impact of different result merges method

As shown in Table 3, we first compare common result merging methods. For these three algorithms - BoN, Beam-Search, and Tree Search - the list-wise approach outperforms other approaches. This is because: 1) compared to scoring that directly relies on standard scoring, list-wise has comparable standards for reference, making evaluation more accurate; and 2) compared to voting methods, list-wise not only considers majority options in the answers, but can also select potentially correct answers from diverse candidates.

s

The impact of different verify methods

As shown in Table 4, we compare the effects of different verify methods on agent performance. The list-wise verify method scores 3 points higher on average than the scoring, which indicate that, whether in BoN-wise or Beam-Search, using list-wise comparison of candidates is superior to the scoring approach. This suggests that compared to directly having PRM score the agent’s trajectory (scoring), using a list-wise approach to have PRM select the relatively optimal trajectory can bring more precise benefits.

4.4 The impact of Diversifying Rollouts

Performance with different search size

Figure 3 presents the performance variations of the agent under different sampling widths. The experimental results demonstrate that increasing the agent’s sampling width leads to significant performance improvements, a finding that aligns with test-time scaling phenomena observed in the LLM domain.

Performance with different rollout models

To further explore the impact of different rollout models on Diversifying Rollouts, we measure the pass@1 performance of SOTA models and calculate their pass@2 and pass@4 performance when combined with the baseline model GPT-4.1.

As shown in Table 5, under the pass@1 setting, GPT-4.1 achieves the highest score. Notably, under the pass@2 and pass@4 settings, using other models mixed with GPT-4.1 yields higher results than using GPT-4.1 alone, which further demonstrates the effectiveness of using different rollouts models. Additionally, using all four different models achieves a total score of 74.55 for pass@4, reaching a level that surpasses the open-source SOTA.

5 Related Work

Language Agents

In previous research work, many mature agentic frameworks have been established, such as Meta-GPT[10] which enables GPT to assume different roles and collaboratively complete tasks, LangChain[24] which uses natural language to describe tools and solve complex tasks, and AGENTS[34] which, in addition to supporting basic tool calling and long-term memory, also supports human-agent interaction and controllability through symbolic plans (SOPs). Recently, with the emergence of OPENAI’s deep research concept, numerous agentic frameworks have appeared, such as Manus[18], OWL[15], and SmoLAgents[5]. These agentic frameworks support collaborative work among various agents, decompose task inputs, conduct multi-step task planning, and invoke diverse tools to complete complex tasks. However, current agentic frameworks predominantly employ a single linear workflow to solve problems and have not yet conducted in-depth exploration of Test-Time-Scaling (TTS) capabilities.

LLM Test-Time Scaling

Snell et al. [25] propose that scaling LLMs Test-time Compute[29] optimally can be more effective than scaling model parameters. OpenAI’s o1 model 11 1 https://openai.com/o1/ is designed to spend more time reasoning before they respond for the sake of obtaining better performance. Recently, various TTS algorithms have emerged, such as Best-Of-N, Beam-Search, Tree-Search, and Majority-Vote.[21, 6, 13] Moreover, [14] and [31] investigate enabling LLMs to perform self-reflection through self-rewarding and self-correlation mechanisms to enhance their performance.

Besides, Some works([25, 28, 3]) design reward models to guide the trajectory selection process in LLM test-time scaling . [4] incorporates deep thinking into reward models, while [23] uses RM for complex tool selection. [20] and [27] provide a comprehensive experimental analysis of LLM Test-Time Scaling. However, Test-Time Scaling strategies have not yet been fully discussed within agentic frameworks. In this work, we investigate four key aspects of test-time scaling strategies: parallel sampling algorithms, sequential revision strategies, verifiers and merging methods, and strategies for diversifying rollouts, and conduct comprehensive ablation experiments comparing various strategies within each aspect.

6 Conclusion

Test Time Scaling (TTS) can significantly enhance LLM inference performance by increasing computational resources during the inference phase. However, the application of Test Time Scaling in the agentic domain still needs to be explored. In this paper, we explore four different aspects of test-time scaling strategies: Parallel Sampling Algorithms; Sequential Revision Strategies; Verifiers and Merging Methods; Strategies for Diversifying Rollouts. We conduct detailed comparative ablation experiments for strategies in each aspect. Our experimental results indicate: 1. Applying parallel sampling algorithms to scale agent test time compute could improve agent performance, 2. For sequential revision, it is important to know when to revise, 3. Among different verify and result merge methods, list-wise methods perform best, 4. Increasing diversified rollouts exerts a positive benefit on agent, which aligns with test-time scaling phenomena observed in the LLM domain.

7 Contributions

Core Contributors

- • 

King Zhu

- • 

Hanhao Li

- • 

Siwei Wu

Contributors

- • 

Tianshun Xing

- • 

Dehua Ma

- • 

Xiangru Tang

- • 

Minghao Liu

- • 

Jian Yang

- • 

Jiaheng Liu

- • 

Yuchen Eleanor Jiang

- • 

Changwang Zhang

- • 

Chenghua Lin

- • 

Jun Wang

Corresponding Authors

- • 

Wangchunshu Zhou

- • 

Ge Zhang

References

- [1] L. AI. Open deep research: A fully open-source research assistant, 2025. URL https://github.com/langchain-ai/open_deep_research.
- [2] D. Bahdanau, N. Gontier, G. Huang, E. Kamalloo, R. Pardinas, A. Piché, T. Scholak, O. Shliazhko, J. P. Tremblay, K. Ghanem, S. Parikh, M. Tiwari, and Q. Vohra. Tapeagents: a holistic framework for agent development and optimization, 2024. URL https://arxiv.org/abs/2412.08445.
- [3] E. Beeching, L. Tunstall, and S. Rush. Scaling test-time compute with open models, 2024. URL https://huggingface.co/spaces/HuggingFaceH4/blogpost-scaling-test-time-compute.
- [4] X. Chen, G. Li, Z. Wang, B. Jin, C. Qian, Y. Wang, H. Wang, Y. Zhang, D. Zhang, T. Zhang, et al. Rm-r1: Reward modeling as reasoning. arXiv preprint arXiv:2505.02387, 2025.
- [5] H. Face. Smolagent: A scalable approach to multi-agent systems, 2025. URL https://github.com/huggingface/smolagents.
- [6] G. Faria and N. A. Smith. Sample, don’t search: Rethinking test-time alignment for language models, 2025. URL https://arxiv.org/abs/2504.03790.
- [7] A. Fourney, G. Bansal, H. Mozannar, C. Tan, E. Salinas, E. E. Zhu, F. Niedtner, G. Proebsting, G. Bassman, J. Gerrits, J. Alber, P. Chang, R. Loynd, R. West, V. Dibia, A. Awadallah, E. Kamar, R. Hosn, and S. Amershi. Magentic-one: A generalist multi-agent system for solving complex tasks, 2024. URL https://arxiv.org/abs/2411.04468.
- [8] D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025.
- [9] S. Hong, X. Zheng, J. Chen, Y. Cheng, J. Wang, C. Zhang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou, et al. Metagpt: Meta programming for multi-agent collaborative framework. arXiv preprint arXiv:2308.00352, 3(4):6, 2023.
- [10] S. Hong, M. Zhuge, J. Chen, X. Zheng, Y. Cheng, C. Zhang, J. Wang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou, C. Ran, L. Xiao, C. Wu, and J. Schmidhuber. Metagpt: Meta programming for a multi-agent collaborative framework, 2024. URL https://arxiv.org/abs/2308.00352.
- [11] A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry, A. Beutel, A. Carney, et al. Openai o1 system card. arXiv preprint arXiv:2412.16720, 2024.
- [12] J. Y. Koh, R. Lo, L. Jang, V. Duvvur, M. C. Lim, P.-Y. Huang, G. Neubig, S. Zhou, R. Salakhutdinov, and D. Fried. Visualwebarena: Evaluating multimodal agents on realistic visual web tasks. arXiv preprint arXiv:2401.13649, 2024a.
- [13] J. Y. Koh, S. McAleer, D. Fried, and R. Salakhutdinov. Tree search for language model agents, 2024b. URL https://arxiv.org/abs/2407.01476.
- [14] A. Kumar, V. Zhuang, R. Agarwal, Y. Su, J. D. Co-Reyes, A. Singh, K. Baumli, S. Iqbal, C. Bishop, R. Roelofs, et al. Training language models to self-correct via reinforcement learning. arXiv preprint arXiv:2409.12917, 2024.
- [15] M. H. Y. Z. W. F. Y. N. B. X. T. S. Z. Y. Z. J. Y. L. Z. Z. Y. W. Q. Y. P. L. G. Li. Owl: Optimized workforce learning for general multi-agent assistance in real-world task automation, 2025. URL https://github.com/camel-ai/owl.
- [16] X. Li, G. Dong, J. Jin, Y. Zhang, Y. Zhou, Y. Zhu, P. Zhang, and Z. Dou. Search-o1: Agentic search-enhanced large reasoning models, 2025a. URL https://arxiv.org/abs/2501.05366.
- [17] X. Li, J. Jin, G. Dong, H. Qian, Y. Zhu, Y. Wu, J.-R. Wen, and Z. Dou. Webthinker: Empowering large reasoning models with deep research capability, 2025b. URL https://arxiv.org/abs/2504.21776.
- [18] X. Liang, J. Xiang, Z. Yu, J. Zhang, S. Hong, S. Fan, and X. Tang. Openmanus: An open-source framework for building general ai agents, 2025. URL https://doi.org/10.5281/zenodo.15186407.
- [19] F. Liu, W. Chao, N. Tan, and H. Liu. Bag of tricks for inference-time computation of llm reasoning, 2025a. URL https://arxiv.org/abs/2502.07191.
- [20] R. Liu, J. Gao, J. Zhao, K. Zhang, X. Li, B. Qi, W. Ouyang, and B. Zhou. Can 1b llm surpass 405b llm? rethinking compute-optimal test-time scaling, 2025b. URL https://arxiv.org/abs/2502.06703.
- [21] R. Liu, J. Gao, J. Zhao, K. Zhang, X. Li, B. Qi, W. Ouyang, and B. Zhou. Can 1b llm surpass 405b llm? rethinking compute-optimal test-time scaling. arXiv preprint arXiv:2502.06703, 2025c.
- [22] G. Mialon, C. Fourrier, T. Wolf, Y. LeCun, and T. Scialom. Gaia: a benchmark for general ai assistants. In The Twelfth International Conference on Learning Representations, 2023.
- [23] C. Qian, E. C. Acikgoz, Q. He, H. Wang, X. Chen, D. Hakkani-Tür, G. Tur, and H. Ji. Toolrl: Reward is all tool learning needs. arXiv preprint arXiv:2504.13958, 2025.
- [24] L. repository. Langchain, 2022. URL https://github.com/langchain-ai/langchain.
- [25] C. Snell, J. Lee, K. Xu, and A. Kumar. Scaling llm test-time compute optimally can be more effective than scaling model parameters. arXiv preprint arXiv:2408.03314, 2024.
- [26] J. Tang, T. Fan, and C. Huang. Autoagent: A fully-automated and zero-code framework for llm agents, 2025. URL https://arxiv.org/abs/2502.05957.
- [27] S. Wu, Z. Peng, X. Du, T. Zheng, M. Liu, J. Wu, J. Ma, Y. Li, J. Yang, W. Zhou, et al. A comparative study on reasoning patterns of openai’s o1 model. arXiv preprint arXiv:2410.13639, 2024a.
- [28] Y. Wu, Z. Sun, S. Li, S. Welleck, and Y. Yang. Inference scaling laws: An empirical analysis of compute-optimal inference for problem-solving with language models. arXiv preprint arXiv:2408.00724, 2024b.
- [29] Y. Wu, Z. Sun, S. Li, S. Welleck, and Y. Yang. Inference scaling laws: An empirical analysis of compute-optimal inference for problem-solving with language models, 2025. URL https://arxiv.org/abs/2408.00724.
- [30] Z. Wu, C. Han, Z. Ding, Z. Weng, Z. Liu, S. Yao, T. Yu, and L. Kong. Os-copilot: Towards generalist computer agents with self-improvement, 2024c. URL https://arxiv.org/abs/2402.07456.
- [31] W. Xiong, H. Zhang, C. Ye, L. Chen, N. Jiang, and T. Zhang. Self-rewarding correction for mathematical reasoning. arXiv preprint arXiv:2502.19613, 2025.
- [32] S. Zhou, F. F. Xu, H. Zhu, X. Zhou, R. Lo, A. Sridhar, X. Cheng, T. Ou, Y. Bisk, D. Fried, et al. Webarena: A realistic web environment for building autonomous agents. arXiv preprint arXiv:2307.13854, 2023a.
- [33] W. Zhou, Y. E. Jiang, P. Cui, T. Wang, Z. Xiao, Y. Hou, R. Cotterell, and M. Sachan. Recurrentgpt: Interactive generation of (arbitrarily) long text, 2023b. URL https://arxiv.org/abs/2305.13304.
- [34] W. Zhou, Y. E. Jiang, L. Li, J. Wu, T. Wang, S. Qiu, J. Zhang, J. Chen, R. Wu, S. Wang, S. Zhu, J. Chen, W. Zhang, X. Tang, N. Zhang, H. Chen, P. Cui, and M. Sachan. Agents: An open-source framework for autonomous language agents, 2023c. URL https://arxiv.org/abs/2309.07870.
- [35] W. Zhou, Y. Ou, S. Ding, L. Li, J. Wu, T. Wang, J. Chen, S. Wang, X. Xu, N. Zhang, H. Chen, and Y. E. Jiang. Symbolic learning enables self-evolving agents. 2024. URL https://arxiv.org/abs/2406.18532.
