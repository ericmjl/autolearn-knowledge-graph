---
title: "You don't need a frontier model. You need a verifier. | AI21"
type: "raw-source"
url: "https://www.ai21.com/blog/you-need-a-verifier/"
author: "Guy Freund"
publication: "AI21 Labs"
published: "2026-08-19"
archived: "2026-11-26T14:01:01Z"
---

> [!quote] Original source
> **Author(s):** Guy Freund  
> **Title:** You don't need a frontier model. You need a verifier. | AI21  
> **Published in:** AI21 Labs  
> **Date:** 2026-08-19  
> **Original:** <https://www.ai21.com/blog/you-need-a-verifier/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-you-don-t-need-a-frontier-model-you-need-a-verifier-ai21|Source note]]
Themes: [[Loop engineering]], [[Retrieval and agentic data science]]
Why it was archived: How should an independent verifier in a multi-agent system check an agent's work without sharing the agent's context, and does this scale to many agents?

## Archived text

You don’t need a frontier model. You need a verifier.

In brief

On agentic search, small models usually produce a correct answer and then fail to pick it. Majority voting cannot fix that, because it cannot overturn a popular wrong answer. Adding an independent verifier that re-researches each candidate and vetoes the wrong ones beats published SOTA on FACTS-Search, and once you train your own 8B verifier it costs almost nothing, works with any generator pool, and generalizes to a new benchmark and retrieval tool.

The default way to make an agentic system more accurate is to buy a better generator – a frontier model. It works, but it is the most expensive option available.

This post is making a different argument: how you run your models matters more than which model you run. The system below adds an important component to any AI architecture: a verifier. This component increases the performance of every architecture, whether it’s an ensemble of frontier models or efficient open source models.

Why agentic search needs a verifier

Your efficient agent probably already found the right answer. The problem is that it didn’t pick it.

Model runs are not deterministic. The same agent, same question, fails on one attempt and succeeds on the next. Across every generator we tested, pass@k sits far above single-shot accuracy (pass@1): correct answers are routinely present in the pool and simply not selected. So the binding constraint on agentic search is selection, not generation.

Selection is tractable because checking is easier than generating (at least for agentic search QA). Answering “Which band played ‘Johnny Come Lately’ on the Steve Earle album that includes ‘Little Sister’?” takes a chain of searches, dead ends, and synthesis. Verifying a proposed answer is far narrower: research one claim and rule on it.

So why not just take the majority vote when using an ensemble? Because voting cannot overturn a popular wrong answer. When half the pool confidently repeats the same wrong entity, voting does not filter the error, it certifies it. Efficient pools fail this way most, because correct answers are less frequent.

Verification works

First, ignore cost and run the best verifier available.

We work on FACTS-Search, Google DeepMind’s benchmark of hard multi-hop factual questions that require web search to answer. Every model in this post, generator or verifier, uses the same Brave Search API, so measured differences are model skill and not tooling.

Generators ensemble of closed-source and open-source models (Claude Haiku, Sonnet, Opus, Qwen3-Coder-30B-A3B at k=4) scores 83.3 under plain majority voting and 93.4 with a Claude Opus verifier on top, past the published state of the art of 89.4 (GPT-5.6 Sol), as can be seen in Figure 1.

The headroom is larger at the small end

Frontier-on-frontier proves the mechanism. The regime that matters in practice is small generators, and there the headroom grows rather than shrinks: a noisier pool still surfaces correct answers, they are just outnumbered, which is exactly when identifying them pays.

Our all-open-source pool (Qwen3-14B and Qwen3-Coder-30B-A3B at k=4) votes to 60.1. Put a Claude Opus verifier on those same candidates and it scores 80.4 at \$1.76 per question. Twenty points already sitting in the pool, waiting for a verifier good enough to claim them.

The verifier is the expensive part, so we trained our own

A frontier verifier runs a full web-research loop on every candidate: k samples times the number of generators, sixteen loops per question in our best configuration. That costs more than generating everything it checks: the 93.4 result runs \$4.26 per question, most of it the verifier.

The obvious fix is a small open-source verifier, and it does not work. A stock Qwen3-8B verifier moves the efficient pool from 60.1 to 62.5. Plus 2.4 points against Opus’s plus 20.3 on the same candidates. That 18-point gap is the training problem: the verification skill does not come free with the parameters.

Training

Given a question and a candidate answer, the verifier runs its own Brave-search ReAct loop and emits one verdict. The reward is a binary exact match against the ground-truth label, so it is fully verifiable, no reward model. Training data is about 6K (question, answer, VALID/NOT_VALID) triples from generator rollouts, deduplicated, class-balanced, and split at the question level.

The recipe is SFT then RL, for the same reason as DeepSeek-R1: RL from a cold start has no competent policy to explore from. Two failure modes here are specific to verification. RL alone reward-hacks the class imbalance, with tool-use rate falling from 94% to 0% in nine steps. Balancing the data closes that shortcut but not the underlying problem: the policy settles into one narrow search behavior and cannot climb out of it, so search quality plateaus wherever the cold start happens to land. SFT alone teaches the search skill and dilutes the verdict, because imitation spreads its loss over every token of a long trajectory while the verification signal lives in one token. Composed, tool use stays high and becomes adaptive, and the verdict sharpens without the policy collapsing.

Measuring any of this needs two things. Re-running the full loop for every checkpoint is too slow, so verifier variants are scored offline against a fixed pool of pre-generated rollouts: the candidates never change, only the judge does. And metrics have to be computed per question and then averaged, because rollout-level verdict metrics (accuracy, precision, recall, F1) routinely improved while the system got worse. We track four quantities (Figure 4): pass@1 and pass@k, one random pick and the oracle ceiling with no verifier, and pass@1(v) and pass@k(v), the same two over verified candidates only. Three gaps assign blame – two to the verifier, one to the aggregator:

- Verification lift := pass@1(v) − pass@1 is the verifier’s precision: maximize it.
- Aggregator headroom := pass@k(v) − pass@1(v) is what a smarter aggregator could still recover from verified candidates – a separate thread we don’t pursue here.
- The recall cap := pass@k − pass@k(v) is the fraction of solvable questions

where the verifier rejected every correct answer: minimize it.

Results

100-question public test sample, official grading. Costs assume the prices of common serving platforms.

Swap one component in the SOTA configuration. Replacing the Claude Opus verifier with our trained 8B verifier holds 92.9 at \$1.34: half a point of quality for 3.2x lower cost, still way above published SOTA. The most expensive component in the system became one of the cheapest.

Remove proprietary models entirely. Qwen3-14B and Qwen3-Coder-30B-A3B at k=4 with our trained verifier on top scores 77.0 at \$0.017 per question, against 60.1 majority voting on the same pool and 80.4 for the Opus verifier on it. The generators are nearly free, so the verifier is the system. It beats a single Claude Haiku call (76.3 at \$0.043) at 2.5x lower cost and lands within 4.2 points of a single Claude Sonnet call (81.2 at \$0.1) at 6x lower cost.

It generalizes

We trained on one benchmark and one tool on purpose, because the practical case is a customer arriving with their own setup. The BrowseComp-Plus benchmark changes both at once: same task shape, but the agent retrieves from a fixed corpus instead of searching the open web.

The verifier transfers out of the box and lifts the downstream vote from 39% to 51%. What it loses is recall: on 27% of solvable questions it rejects every candidate and forfeits the question. A final tiny SFT on about 85 held-out-domain questions, roughly 15 optimizer steps, collapses that gap from 27% to 4% and pushes downstream to 69%.

Verification adds at most 5% to system cost at every rollout budget. We do not claim SOTA here, since the generator is a single open-source model. The claim is the recipe: precision generalizes for free, and the recall gap is easy to close.

Summary

- On agentic search, correct answers are usually already in the pool. Majority voting cannot surface them, because it cannot overturn a popular wrong answer. The bottleneck is selection.
- An independent research-and-veto verifier took a frontier pool from 83.3 to 93.4 on FACTS-Search, past published SOTA. It was also the dominant cost of that system.
- A stock 8B recovers almost none of that lift. Trained, the same 8B holds 92.9 at \$1.34, within half a point of the Claude Opus verifier at 3.2x lower cost, and delivers 77.0 at \$0.017 with no proprietary model in the stack.
- It generalizes across benchmark and tool: precision transfers for free, and a small adaptation closes the recall gap while lifting precision further.

Caveats: both benchmarks are evaluated on 100-question samples, training labels inherit automated-grader noise, both SFT stages distill from closed-source models, and verification adds a round of latency. That last one is bounded: verification trajectories are short next to generation rollouts, which drag retrieved documents through context, and the loops share no state, so sixteen verifications cost the wall clock of one.
