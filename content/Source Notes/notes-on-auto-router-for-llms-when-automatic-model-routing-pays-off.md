---
type: "source-note"
title: "Notes on: Auto Router for LLMs: When Automatic Model Routing Pays Off"
raw: "auto-router-for-llms-when-automatic-model-routing-pays-off"
url: "https://www.orcarouter.ai/blog/auto-router"
created_at: "2026-11-27T18:01:54Z"
updated_at: "2026-11-27T18:01:54Z"
---
- Archived full text: [[auto-router-for-llms-when-automatic-model-routing-pays-off|Full archived text, with credits]]
- Link: <https://www.orcarouter.ai/blog/auto-router>

## What it says

OrcaRouter's auto router article explains what an auto router does: it reads each prompt, grades how hard it is, and sends the easy majority to a cheap model while keeping genuinely hard requests on the frontier. It gives the accuracy bands for each classification style, reports savings numbers (coding-session example 79% down to $1.26, up to 85% claimed by RouteLLM), names the latency tax of each classifier, and lists cases where routing is the wrong answer (one model, latency-critical, tiny volume, must-be-auditable, unmeasurable quality). It recommends routing behind a quality floor, routing a slice first, and reading per-request routing logs.

## Claims drawn from this source

- **An auto router classifies each request, then assigns a model.** A router's job has two parts: classify the request, then assign a model. The classification step ranges from trivial to genuinely learned: keyword/regex rules under 1ms at roughly 50-65% accurate, prompt-length heuristics similar, a small classifier at 50-200ms at 70-80%, a trained domain classifier at 200-500ms at 85-95%, and LLM-as-judge at 1-5 seconds at 85-90%.
- **Routing saves real money when model prices differ a lot.** DeepSeek V4 Flash at $0.14/$0.28 per 1M tokens against Claude Opus 5 at $5.00/$25.00 is a 36x difference on input tokens alone. The documented coding-session example went from $6.00 with every call on the frontier to $1.26 with routing, and $1.36 after the router's $0.10 per 100 requests, still 77% cheaper.
- **Aggressive, balanced, and conservative routing save 60-75%, 35-45%, and 10-15%.** Open-source router configurations report the same shape at scale: aggressive cost routing saves 60-75%, a balanced policy saves 35-45%, and even conservative routing saves 10-15%.
- **The classification tax is the difference between cheap and free.** Every request pays a classification tax before the model starts: keyword rules under 1ms, small classifier 50-200ms, trained domain classifier 200-500ms. A production routing endpoint measured end-to-end overhead at roughly 55ms median, under 1% of a normal response time, but a 200ms classifier can be the difference between usable and not for a sub-300ms real-time requirement.
- **A router without a quality floor silently degrades output.** RouteLLM and follow-up work report savings of up to roughly 85% while preserving frontier-level quality, but only when the router is paired with a quality floor that stops it from cheaping out on requests that genuinely need the frontier. Without that floor, cost routing silently degrades output and nobody logs it.
- **Auto routing is the wrong answer for single-model, latency-critical, tiny-volume, auditable, or unmeasurable setups.** If you basically use one model, routing adds a hop and a classification tax for nothing. If responses must be instant (under roughly 300ms), pin the model. Under a few hundred dollars a month, your time is worth more than the savings. If the model must be auditable, log and pin the pick. Without an eval, aggressive cost routing quietly degrades output you never check.
- **A five-check afternoon evaluation separates a router worth keeping from a dashboard.** Route a slice while keeping the rest pinned; measure cost and quality before and after on a 50-prompt eval built from your own prompts; force the hard cases and check the router does not dump them on the cheap model; read the per-request routing logs (which model it picked and why); time real P50/P95 added latency with a stopwatch.
- **Managed auto routers ship balanced and adaptive policies and fail over mid-stream.** OrcaRouter's auto mode ships four policies: Cheapest, Balanced (default), Quality, and Adaptive. Grading is measured in under 1ms with total added latency under 50ms, and on rate-limit or 5xx the router fails over mid-stream in under 50ms. June 2026 RouterArena scores OrcaRouter at 75.5% against GPT-5 at 74.0, Azure at 72.8, Martian at 61.6, and NotDiamond at 60.8.
