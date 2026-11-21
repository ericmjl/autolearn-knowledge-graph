---
title: "ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., ICLR 2023)"
type: "raw-source"
url: "https://arxiv.org/abs/2210.03629"
author: "Shunyu Yao et al."
publication: "arXiv"
published: "2022-10-06"
archived: "2026-11-21T03:02:23Z"
---

> [!quote] Original source
> **Author(s):** Shunyu Yao et al.  
> **Title:** ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., ICLR 2023)  
> **Published in:** arXiv  
> **Date:** 2022-10-06  
> **Original:** <https://arxiv.org/abs/2210.03629>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-react-synergizing-reasoning-and-acting-in-language-models-yao-et-al-iclr-2023|Source note]]
Themes: [[Agent design patterns]], [[Loop engineering]]
Why it was archived: One of the original seed sources this graph started from in July 2026 (kept in the 2026-11-20 rebuild).

## Archived text

Computer Science > Computation and Language

  [Submitted on 6 Oct 2022 (v1), last revised 10 Mar 2023 (this version, v3)]

Title:ReAct: Synergizing Reasoning and Acting in Language Models

View PDF HTML (experimental)

            Abstract:While large language models (LLMs) have demonstrated impressive capabilities across tasks in language understanding and interactive decision making, their abilities for reasoning (e.g. chain-of-thought prompting) and acting (e.g. action plan generation) have primarily been studied as separate topics. In this paper, we explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner, allowing for greater synergy between the two: reasoning traces help the model induce, track, and update action plans as well as handle exceptions, while actions allow it to interface with external sources, such as knowledge bases or environments, to gather additional information. We apply our approach, named ReAct, to a diverse set of language and decision making tasks and demonstrate its effectiveness over state-of-the-art baselines, as well as improved human interpretability and trustworthiness over methods without reasoning or acting components. Concretely, on question answering (HotpotQA) and fact verification (Fever), ReAct overcomes issues of hallucination and error propagation prevalent in chain-of-thought reasoning by interacting with a simple Wikipedia API, and generates human-like task-solving trajectories that are more interpretable than baselines without reasoning traces. On two interactive decision making benchmarks (ALFWorld and WebShop), ReAct outperforms imitation and reinforcement learning methods by an absolute success rate of 34% and 10% respectively, while being prompted with only one or two in-context examples. Project site with code: this https URL
    
Submission history

From: Shunyu Yao [view email]

[v1] Thu, 6 Oct 2022 01:00:32 UTC (538 KB)

[v2] Sun, 27 Nov 2022 22:55:54 UTC (538 KB)

[v3] Fri, 10 Mar 2023 01:00:17 UTC (1,256 KB)

Current browse context:

cs.CL

References & Citations
    
    Loading...

Bibliographic and Citation Tools

            Bibliographic Explorer (What is the Explorer?)
          
            Connected Papers (What is Connected Papers?)
          
            Litmaps (What is Litmaps?)
          
            scite Smart Citations (What are Smart Citations?)
          
Code, Data and Media Associated with this Article

            alphaXiv (What is alphaXiv?)
          
            CatalyzeX Code Finder for Papers (What is CatalyzeX?)
          
            DagsHub (What is DagsHub?)
          
            Gotit.pub (What is GotitPub?)
          
            Hugging Face (What is Huggingface?)
          
            ScienceCast (What is ScienceCast?)
          
Demos

Recommenders and Search Tools

              Influence Flower (What are Influence Flowers?)
            
              CORE Recommender (What is CORE?)
            
arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? Learn more about arXivLabs.
