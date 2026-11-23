---
title: "Introducing the Evaluation Engine: Build High-Accuracy Evaluators and Guardrails Fitted to Your Agents | Splunk"
type: "raw-source"
url: "https://www.splunk.com/en_us/blog/artificial-intelligence/introducing-evaluation-engine.html"
author: "Paul Lacey, Pratik Bhavsar"
publication: "Splunk"
published: "2026-11-10"
archived: "2026-11-23T03:01:18Z"
---

> [!quote] Original source
> **Author(s):** Paul Lacey, Pratik Bhavsar  
> **Title:** Introducing the Evaluation Engine: Build High-Accuracy Evaluators and Guardrails Fitted to Your Agents | Splunk  
> **Published in:** Splunk  
> **Date:** 2026-11-10  
> **Original:** <https://www.splunk.com/en_us/blog/artificial-intelligence/introducing-evaluation-engine.html>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-introducing-the-evaluation-engine-build-high-accuracy-evaluators-and-guardrails-fitted-to|Source note]]
Themes: [[Evals and agent quality]]
Why it was archived: How accurate are purpose-built small evaluators versus frontier judges on every transaction, and what accuracy can teams tolerate at the per-call layer?

## Archived text

Introducing the Evaluation Engine: Build High-Accuracy Evaluators and Guardrails Fitted to Your Agents

Artificial Intelligence Paul Lacey ,

Key Takeaways

- The Evaluation Engine in Splunk Agent Observability turns your traces and expert feedback into custom evaluators and runtime guardrails that follow your own policies.
- The the evaluation tuner builds an evaluator in an afternoon, with no data science team, once you have trustworthy examples.
- Splunk’s Eval-G1 models match the most accurate frontier LLM judges on PII and toxicity and catch 99.4% of leaked personal data, more than any model we tested.
- Each verdict takes about a third of a second, up to 14× faster than frontier LLM judges, at a fraction of their cost per evaluation.
- Available now for Splunk Agent Observability customers in US regions.

Every business runs on its own rules. Evals encode those rules for agents to follow them. A bank's AI assistant must apply the lending policies that define its business model, and a doctor’s agent should adhere to their acceptable writing style with patients. Those rules are what set your business apart.

General-purpose LLMs learn from the world's data, so when you use them to eval your agents they do it against everyone's average. And average is where differentiation dies. They miss what matters most: your policies, your voice and your definition of done.

Today, Splunk Agent Observability introduces the Evaluation Engine, which brings AI agent evaluation in line with your own standards. At its heart is the the evaluation tuner, which turns your traces and your experts' feedback into specialized SLM models to evals your agents. You can build one in an afternoon and get each verdict in about a third of a second.

What Makes the Evaluation Tuner Different

The evaluation tuner starts from your rules rather than a model's average and these four things set it apart:

- Accuracy on your terms. Evaluators learn from your traces and your experts' labels, so every verdict follows your standards.
- From failure to guardrail in one place. Splunk Agent Observability surfaces hidden failure patterns you didn't know to check for. The evaluation tuner turns each pattern into a custom evaluator model that also acts as a runtime guardrail to block policy violations before they occur in production.
- No data science team required. The evaluation tuner generates the training data, tunes the evaluator and checks it against your standard before anything goes live.
- Built for production volume. Because each evaluation predicts a single token, verdicts come back in about a third of a second at up to 98% lower cost than frontier LLM judges.

Benchmark Results for AI Agent Evaluation

In this test, we tuned three evaluators: PII and toxicity, which cover universal checks, and a custom conciseness evaluator for a healthcare assistant that follows a detailed rubric. We evaluated each one against five LLM judges and Jev on the same held-out test sets with the same prompt or rubric.

The PII evaluator caught 99.4% of leaked personal data at 0.958 F1, ahead of every model we tested. On conciseness, the tuned evaluator beat three of five frontier judges and came within 1.3 points of the best. Each verdict took about a third of a second, up to 14× faster than frontier LLM judges.

Table 1. F1 by evaluation

Accuracy is only half the story, because at production volume speed and cost decide how much traffic you can evaluate. A tuned Eval-G1 model matches the most accurate LLM judges on PII and toxicity while answering in a third of a second.

Figure 2. Accuracy against latency on PII and toxicity, with the cost to run 1,000 evaluations as bubble size. Cost is per evaluation run, not API or model list pricing. Results pending final benchmark sign-off.

Why Tune Your Own Evaluator Models

The numbers point to three lessons for anyone deciding how to grade their agents.

1. A small tuned model can match a frontier judge on a judgment call

Conciseness is a judgment call about whether every sentence is needed in the response. With the same 549-word rubric, the tuned evaluator scored 0.871 F1 and beat three of five frontier judges. It came within 1.3 points of Claude Opus 5.5 while outputting a single token instead of wasting thousands on a long verdict.

2. Inline guardrails need sub-second answers

A guardrail has to decide before the customer sees the reply. Frontier LLM judges took 2.2 to 4.7 seconds per evaluation on PII and toxicity, which is a long pause to add to each response they guard. The custom evaluator models took about a third of a second, fast enough to block a response before anyone notices. The only LLM judges that matched its accuracy on PII and toxicity were GPT 6 Sol, at about 16 times the cost per evaluation, and GPT 6 Luna, at a similar cost but eight times slower. That makes Splunk Eval-G1 cheap enough to score up to 100% of your production traffic.

3. A guardrail is judged by what it lets through

Three frontier judges were precise on toxicity but caught fewer than 60% of toxic messages. A guardrail that misses more than four in ten violations isn't much of a guardrail. On PII, where every miss is a leak, the tuned evaluator caught 99.4% of all violations.

Teams running agents under strict policies feel this gap first.

From Failure to Guardrail in an Afternoon, Once You Have Examples

You don't need a data science team for any of this. Here is one failure followed from the first alert to a live guardrail, at a fictional bank with step times from product-team estimates. The afternoon assumes the team already has trustworthy examples. Without a ground truth dataset, plan for two to three days, because agreeing on those examples takes longer than tuning.

Figure 3. One afternoon in The evaluation tuner, with time per step drawn to scale.

- 12:00 p.m. Signals in Splunk Agent Observability flags a pattern. Fee disputes at a retail bank are climbing and Signals traces them to one failure: the assistant says the \$12 monthly fee is waived when it isn't. The fee policy is in its prompt, yet the assistant still treats money moved from the customer's own savings as a direct deposit.
- 12:15 p.m. Experts label the conversations. Three people from the deposits team split 60 similar conversations, mark each one pass or fail, and talk through the cases where they disagree. Their labels define what "correct" means, which makes this the step that matters most.
- 1:15 p.m. The team writes the rule down. The rubric is short: the waiver needs \$500 or more in direct deposits, and transfers between your own accounts don't count. When the team runs an LLM judge with that rubric against their labels, it still passes some of the transfers the assistant got wrong.
- 2:00 p.m. The evaluation tuner expands the examples. It grows the 60 conversations into about 5,000 training examples covering paychecks, transfers, rephrasings, and near misses.
- 2:15 p.m. The evaluator trains. A custom Eval-G1 evaluator model is trained on those examples while the team gets on with their day.
- 4:15 p.m. The team validates. The evaluation tuner compares the tuned evaluator with an LLM judge on conversations neither has seen. The team reviews each disagreement and decides whether to deploy the new SLM evaluator.
- 4:45 p.m. The guardrail goes live. After a final check, the team turns it on, and by 5:00 pm the evaluator scores fee conversations in about a third of a second, and as a runtime guardrail it stops a wrong waiver before the customer hears it.

Your experts spent about two and a half hours of that afternoon, and the evaluation tuner did the rest. Figure 4 shows what the new evaluator sees.

Figure 4. The same answer to two customers, two verdicts. Inputs shortened; probabilities illustrative.

Both customers hear that their fee is waived, but only one should. The rule was never a secret: it sat in the assistant's prompt, and an LLM judge can read it too. General-purpose models still slip on exceptions like this one, whether they write the answer or grade it. The tuned Eval-G1 evaluator learned the rule from many examples, so it applies it the same way every time.

Inside the Evaluation Engine

Every evaluator you build runs on the Evaluation Engine in Splunk Agent Observability. It has three layers, and the evaluation tuner is the one you work in:

Splunk Agent Observability keeps traces, evaluators, guardrails, and every verdict in one record.

Splunk Eval-G1

Figure 5. One evaluation, from a trace to a decision.

An LLM judge writes its reasoning before it gives a verdict, which can mean hundreds of tokens to generate and parse. Splunk Eval-G1 reads the input once and predicts a single token, and the probability it assigns each label is the score. Every evaluator is a small adapter on one shared base model, so multiple tuned evaluators can run on a single inference engine.

Your Standards at Production Volume

Every business runs on its own rules and now its agents can follow them. The evaluation tuner converts the rubric you would write for an LLM judge into a tuned SLM evaluator that is fast and cost-effective enough to run on your production traffic, not just a sample of it.

Today's evals are tomorrow's guardrails.

The Evaluation Engine, new Eval-G1 models, and the evaluation tuner are available for Splunk Agent Observability customers today, with Splunk-hosted Eval-G1 models available in US regions.

Methodology

How we ran the benchmark:

- Evaluations: PII and toxicity on internal human-labeled test sets; conciseness on a synthetic healthcare dataset with a held-out test set.
- Custom evaluator models: Splunk Eval-G1 tuned on labeled examples for each evaluation (for conciseness, from the same rubric the baselines received), with no test examples used in tuning.
- Baselines: GPT 6 Sol, GPT 6 Luna, Gemini 3.8 Flash, Claude Opus 5.5, and Claude Sonnet 5, and Jev, called through their public APIs with the same prompt or full rubric, at the reasoning settings listed after Appendix A.
- Metric: F1 for the positive class of each evaluation. Latency is the average end-to-end time per evaluation on the PII and toxicity test sets (Appendix B).

Appendix A. Precision, recall, and F1

LLMs were evaluated with the reasoning settings below. Splunk Eval-G1 does not have a reasoning setting.

- Claude Sonnet 5: high
- Claude Opus 5.5: medium
- GPT 6 Sol and GPT 6 Luna: medium
- Gemini 3.8 Flash: medium

Appendix B. Latency per evaluation

Average end-to-end time per evaluation, in seconds.
