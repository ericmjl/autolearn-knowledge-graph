---
title: "Auto Router for LLMs: When Automatic Model Routing Pays Off"
type: "raw-source"
url: "https://www.orcarouter.ai/blog/auto-router"
author: "Jinhao Song"
publication: "OrcaRouter"
published: "2026-08-10"
archived: "2026-11-27T18:01:06Z"
---

> [!quote] Original source
> **Author(s):** Jinhao Song  
> **Title:** Auto Router for LLMs: When Automatic Model Routing Pays Off  
> **Published in:** OrcaRouter  
> **Date:** 2026-08-10  
> **Original:** <https://www.orcarouter.ai/blog/auto-router>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-auto-router-for-llms-when-automatic-model-routing-pays-off|Source note]]
Themes: [[Agent design patterns]], [[Loop engineering]]
Why it was archived: When does model routing pay off for a team with a small model price gap, and does the judge tax shrink with better judge models?

## Archived text

Auto Router for LLMs: How Automatic Model Routing Works, What It Costs, and When to Use It

An auto router is a layer between your application and the model providers that, for every single request, decides which model should answer it. It is not a load balancer — it does not spread identical traffic across identical backends. It reads each prompt, grades how hard it is, and sends the easy majority to a cheap model while keeping the genuinely hard requests on the frontier. That one decision is worth real money: in a documented coding-session example, routing cut cost from \$6.00 to \$1.26 — a 79% reduction, still 77% cheaper after the router's own fee. Here is what the router is actually deciding, the numbers you can trust, and the cases where letting a machine pick your model is the wrong call.

This article exists because the page-1 results for "auto router" are unusually one-sided. For the AI intent, nearly every top result is one router vendor's own documentation — OpenRouter's auto-router guide, its pricing page and its launch announcement — telling you which settings to click in that vendor's dashboard and nothing else. (The remaining results are a Flutter navigation package and PCB-design software on unrelated intents.) None of the AI results explains how routing works under the hood, none publishes independent accuracy data, and none tells you when the feature is a bad idea. That is the gap this page fills.

What an auto router actually decides

A router's job has two parts: classify the request, then assign a model. The classification step is where the intelligence lives, and it ranges from trivial to genuinely learned:

• Keyword and regex rules — under 1ms, roughly 50–65% accurate. Match "translate" to a translation model, match "summarize" to a summary model.

• Prompt-length heuristics — under 1ms, similar accuracy. A cheap proxy for difficulty, but a long prompt can be trivial and a short one can be a math proof.

• A small classifier model — 50–200ms, roughly 70–80% accurate. A lightweight model trained to predict which bigger model will do best on a given prompt.

• A trained domain classifier — 200–500ms, roughly 85–95% accurate. Trained on your own traffic or a large benchmark of prompt-to-best-model pairs.

• LLM-as-judge — 1–5 seconds, roughly 85–90% accurate. Ask an actual model to decide. Usually too slow for the savings to survive.

Those accuracy bands are the typical figures reported across routing vendors and routing research; the exact percentage matters less than the trade-off they describe. The more accurate the classifier, the slower and more expensive the classification — and a router that picks the wrong model saves you nothing, because you pay the price of a frontier model and get mid-tier output.

The savings claim itself is not marketing. LMSYS's RouteLLM and follow-up work from Shanghai AI Lab and IBM Research report savings of up to roughly 85% while preserving frontier-level quality — but only when the router is paired with a quality floor that stops it from cheaping out on requests that genuinely need the frontier. Without that floor, cost routing silently degrades output, and nobody logs it.

The numbers that make routing worth it

Routing only pays when models differ a lot in price. Today they do. All rates below are provider-direct prices per 1M tokens, fetched from the benchlm.ai pricing registry on 2026-08-10:

Read the spread and the argument writes itself: DeepSeek V4 Flash at \$0.14/\$0.28 per 1M against Claude Opus 5 at \$5.00/\$25.00 is a 36× difference on input tokens alone. If your traffic is a typical mix — a lot of short, well-specified requests and a minority of genuinely hard reasoning — sending everything to the frontier means paying top price for the easy 80%.

The measured savings match the arithmetic. A documented coding-session example went from \$6.00 when every call hit a frontier model to \$1.26 with routing — a 79% reduction — and even after adding the router's per-request classification cost (\$0.10 for 100 requests), the total was \$1.36, still 77% cheaper. Open-source router configurations report the same shape at scale: aggressive cost routing saves 60–75%, a balanced policy saves 35–45%, and even conservative routing saves 10–15%.

What routing costs you

The two costs nobody puts on the listicle are latency and accuracy, and both are real.

Latency. Every request pays a classification tax before the model even starts, and that tax is the difference between cheap and free. Keyword rules are under a millisecond; a small classifier is 50–200ms; a trained domain classifier is 200–500ms. Good routers hide most of this by classifying while they prepare the upstream request, and one production routing endpoint measured end-to-end overhead at roughly 55ms median — under 1% of a normal response time. But if your traffic is real-time — a voice agent, a UI that must answer inside 300ms — a 200ms classifier can be the difference between usable and not.

Accuracy. A router is only as good as what it was trained on. A classifier trained on general benchmarks can be confidently wrong about your domain: your "easy" summarization task might be easy for the frontier and hard for the cheap model. The failure mode is silent — the user just gets worse output and no one notices. That is why every credible router ships a quality floor or a "balanced" mode, and why you should treat an aggressive cost mode as an experiment, not a default.

Prices move too, and that is an argument for routing, not against it. On 2026-08-06 DeepSeek announced a significant API price increase across the board; the new rates had not been published as of writing. When a cheap model stops being cheap, a router that re-evaluates live pricing can move your easy traffic elsewhere automatically — a fixed integration cannot.

The recommendation: a managed auto router with a quality floor

For a team already integrating multiple providers — or one that simply wants to stop picking a model per feature — the recommendation is a managed auto router that keeps a quality floor and charges no markup. Our own product is OrcaRouter, and it is the one we can speak to in detail, so the specifics below are ours; the checklist at the end applies to any router you evaluate.

OrcaRouter's auto mode — request the model name orcarouter/auto on the standard OpenAI-compatible endpoint — grades each prompt and routes it across 200+ models. It ships four routing policies, with Balanced as the default: Cheapest sends to the lowest-cost model that can answer; Balanced sends to the cheapest model that clears the quality bar; Quality sends to the highest-scoring model regardless of price; Adaptive learns from your live traffic and shifts routing as it goes. Grading is measured in under 1ms and total added latency stays under 50ms, and if the chosen provider rate-limits or 5xxes, the router fails over mid-stream to a healthy model in under 50ms. There is no markup at any layer — you pay each provider its exact published price, and routing itself is free.

On accuracy, the June 2026 RouterArena leaderboard scores OrcaRouter at 75.5% against GPT-5 at 74.0, Azure at 72.8, Martian at 61.6 and NotDiamond at 60.8 (per orcarouter.ai). One leaderboard is not proof of anything — treat it as a single data point and run your own eval on your own prompts before you trust any router with production traffic, including ours.

When an auto router is the wrong answer

Auto-routing is the right call for most teams running more than one model, but not for all. The honest list of cases where it is wrong:

• You basically use one model. A router adds a hop and a classification tax for nothing. Call the provider directly and skip the layer.

• Your responses must be instant. If the requirement is end-to-end under roughly 300ms, the classification tax plus a mid-tier model's slowness can break your budget. Pin the model.

• Your volume is tiny. Routing saves you a percentage of spend, and it cannot save you a percentage of zero. Under a few hundred dollars a month, your time is worth more than the savings.

• The model choice must be auditable. If a response has to be reproducible, or the model that produced it has to be explainable to a reviewer, an auto router's pick is a variable you have to justify. Log it, pin it, or don't route.

• You cannot measure quality. With no eval that tells you whether routed output is good enough, you cannot tell whether the router is working — and aggressive cost routing will quietly degrade output you never check.

How to evaluate any auto router in an afternoon

The good news is that auto-routing is reversible, so you do not have to commit before you trust it. The five checks that actually separate a router worth keeping from a dashboard:

• Route a slice, keep a fallback. Put a fraction of traffic through the auto endpoint and keep the rest pinned. The migration is a base-URL and model-name change, not a rewrite.

• Measure cost and quality before and after, on your prompts. A general benchmark tells you nothing about your traffic. Build a 50-prompt eval that reflects what you actually do.

• Force the hard cases. Feed the router your hardest 50 prompts and check it does not dump them on the cheap model to hit a cost target.

• Read the routing logs. If the router cannot tell you which model it picked for each request and why, per request, walk away. The log is the entire accountability story.

• Time the overhead with a stopwatch, not a dashboard. Measure real P50/P95 added latency on your own requests before you trust a published number.

The short version

An auto router grades every request and sends it to the model that clears your quality bar at the lowest price — the difference between paying frontier rates for 100% of traffic and paying them for the hard minority. It saves real money when your models differ a lot in price (they do: DeepSeek V4 Flash is 36× cheaper on input than Claude Opus 5) and when your traffic is a mix of easy and hard. It costs you latency and some accuracy control, and it is the wrong answer when you are single-model, latency-critical, tiny, or unable to measure quality. When it is right, run it behind a quality floor, route a slice first, and read the routing logs before you believe the savings.

Compared in this article1

Detected from this article · Benchmarks: Artificial Analysis · updated daily
