---
title: "Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts"
type: "raw-source"
url: "https://arxiv.org/abs/2609.18366"
author: "Zhu, Guojun, Huang, Xunheng, Yin, Peng, Xie, Jiahui, Zhang, Sanguo, Zhou, Doudou"
publication: "arXiv.org"
published: "2026-09-16"
archived: "2026-11-23T01:01:09Z"
---

> [!quote] Original source
> **Author(s):** Zhu, Guojun, Huang, Xunheng, Yin, Peng, Xie, Jiahui, Zhang, Sanguo, Zhou, Doudou  
> **Title:** Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts  
> **Published in:** arXiv.org  
> **Date:** 2026-09-16  
> **Original:** <https://arxiv.org/abs/2609.18366>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-bad-genius-counterfactual-guided-harness-evolution-beyond-task-specific-shortcuts|Source note]]
Themes: [[Loop engineering]]
Why it was archived: How much held-out signal does harness evolution need before the held-out oracle itself becomes the bottleneck?

## Archived text

Computer Science > Artificial Intelligence

  [Submitted on 16 Sep 2026 (v1), last revised 18 Nov 2026 (this version, v4)]

Title:Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts

View PDF HTML (experimental)

            Abstract:An optimized agent harness can improve on held-out tasks by relying on formatting conventions that those tasks share with the rest of the benchmark. We introduce Counterfactual Harness Search and Evolution (CHASE) to test whether harness improvements survive changes to the evaluation protocol. A Proposer edits the harness around a fixed foundation model. A Challenger then searches for a protocol change that preserves the tasks but reduces the updated harness's gain over the initial harness. Executable checks test whether the transformation preserves task semantics. If the gain loss is confirmed on held-out tasks, CHASE adds the transformation to an archive that constrains subsequent harness updates. We give conditions under which this finite archive bounds the gain loss on an ideal benchmark with shortcuts removed. We evaluate CHASE on Syn-Ledger, OfficeQA, FinanceBench, and SWE-Bench Pro V2. On Syn-Ledger, removing the known shortcuts yields 38.30% accuracy for CHASE and 18.27% for HarnessEvolve. On the 21 certification tasks from SWE-Bench Pro V2 HARD-51, changing the issue formatting and tool-output field order reduces HarnessEvolve's gain over the initial harness from 8.57 to 3.81 percentage points. The final CHASE harness retains 10.48 points of its 11.43-point gain under the same change.
    
Submission history

From: Guojun Zhu [view email]

[v1] Wed, 16 Sep 2026 09:21:33 UTC (509 KB)

[v2] Fri, 18 Sep 2026 06:03:43 UTC (513 KB)

[v3] Thu, 24 Sep 2026 07:59:20 UTC (521 KB)

[v4] Wed, 18 Nov 2026 05:17:43 UTC (704 KB)

Additional Features

Current browse context:

cs.AI

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
