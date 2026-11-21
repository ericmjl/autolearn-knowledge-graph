---
title: "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
type: "raw-source"
url: "https://arxiv.org/abs/2305.10601"
author: "Shunyu Yao et al."
publication: "arXiv"
published: "2023-05-17"
archived: "2026-11-21T03:02:23Z"
---

> [!quote] Original source
> **Author(s):** Shunyu Yao et al.  
> **Title:** Tree of Thoughts: Deliberate Problem Solving with Large Language Models  
> **Published in:** arXiv  
> **Date:** 2023-05-17  
> **Original:** <https://arxiv.org/abs/2305.10601>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-tree-of-thoughts-deliberate-problem-solving-with-large-language-models|Source note]]
Themes: [[Loop engineering]], [[Agent design patterns]]
Why it was archived: One of the original seed sources this graph started from in July 2026 (kept in the 2026-11-20 rebuild).

## Archived text

Computer Science > Computation and Language

  [Submitted on 17 May 2023 (v1), last revised 3 Dec 2023 (this version, v2)]

Title:Tree of Thoughts: Deliberate Problem Solving with Large Language Models

View PDF HTML (experimental)

            Abstract:Language models are increasingly being deployed for general problem solving across a wide range of tasks, but are still confined to token-level, left-to-right decision-making processes during inference. This means they can fall short in tasks that require exploration, strategic lookahead, or where initial decisions play a pivotal role. To surmount these challenges, we introduce a new framework for language model inference, Tree of Thoughts (ToT), which generalizes over the popular Chain of Thought approach to prompting language models, and enables exploration over coherent units of text (thoughts) that serve as intermediate steps toward problem solving. ToT allows LMs to perform deliberate decision making by considering multiple different reasoning paths and self-evaluating choices to decide the next course of action, as well as looking ahead or backtracking when necessary to make global choices. Our experiments show that ToT significantly enhances language models' problem-solving abilities on three novel tasks requiring non-trivial planning or search: Game of 24, Creative Writing, and Mini Crosswords. For instance, in Game of 24, while GPT-4 with chain-of-thought prompting only solved 4% of tasks, our method achieved a success rate of 74%. Code repo with all prompts: this https URL.
    
Submission history

From: Shunyu Yao [view email]

[v1] Wed, 17 May 2023 23:16:17 UTC (609 KB)

[v2] Sun, 3 Dec 2023 22:50:35 UTC (623 KB)

Additional Features

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
