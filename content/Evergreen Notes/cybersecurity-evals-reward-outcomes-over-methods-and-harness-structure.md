---
type: "evergreen"
title: "Cybersecurity evals reward outcomes over methods and harness structure"
created_at: "2026-11-21T06:05:03Z"
updated_at: "2026-11-21T06:05:03Z"
inputs: ["notes-on-patterns-for-building-cybersecurity-evals", "public-eval-headlines-hide-reliability-grader-noise-and-single-shot-limits", "safety-classifiers-fail-unattended-agents-need-a-real-sandbox"]
provenance_urls: ["https://eugeneyan.com/writing/cybersecurity-evals", "https://eugeneyan.com/writing/public-evals", "https://arxiv.org/abs/2407.01502", "https://arxiv.org/abs/2401.07339", "https://simonwillison.net/2026/Aug/27/breaking-claude-code-opus-5-auto-mode/", "https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/", "https://en.wikipedia.org/wiki/Software_agent"]
refutation_status: "untested"
---
Agent synthesis

Cybersecurity evals reward what the agent achieves, not how it gets there, and they reward harness structure over raw model choice. The mechanism is that exploitation is open-ended: no single exploit path is right, so a grader that scores the final outcome (a sanitizer crash, a hidden flag retrieved, a critical asset exfiltrated) measures what matters. Outcome-only grading is too coarse on its own, though: a model that scores zero on unauthorized code execution may still have found and reproduced the vulnerability. Benchmarks therefore award partial credit along the attack chain: find the vulnerability, reproduce it with a PoC, exploit it, and achieve the attacker goal. Structure dominates the raw model: in Multi-Host Bench, Incalmo jumped success from 3 of 40 networks to 37 of 40, and all ten tested models scored 6 to 9 of 10 representative environments when paired with it, while every model scored zero on ExpertPromptShell. Under a constant model, harness mattered more than the weights.

The general eval lessons from the wiki land here one level deeper. Public scores hide reliability and grader noise (see: public eval headlines hide reliability, grader noise, and single-shot limits), and cybersecurity benchmarks harden that lesson: graders run transcript audits to rule out reward hacking, since ExploitGym's GPT-5.5 and Opus 4.6 auditors agreed 94% across 313 tasks, and pass^k is moot when the task is open-ended. Sandboxing is the load-bearing primitive: every benchmark runs the vulnerable target in Docker, which mirrors the lesson that unattended agents need a real sandbox rather than classifier gates (see: safety classifiers fail; unattended agents need a real sandbox). Even under a fixed model, exploration, not reasoning, is the binding constraint: insufficient exploration drives 67.5% to 80% of zero-day failures, and CyberGym found success collapse to 10% for PoCs longer than 100 bytes, even though those cover 65.7% of the benchmark. With defenses on, Claude Mythos fell from 157 to 45 exploits, which is why outcome grading with partial credit, transcript audits, and a sandboxed target are the eval-design primitives that carry the weight.

For builders, the practical rule is to score outcomes with partial credit, audit transcripts for reward hacking, sandbox every target, and treat the harness as the first evaluation variable rather than the model.

## Where it comes from

- [[notes-on-patterns-for-building-cybersecurity-evals|Patterns for Building Cybersecurity Evals]]

## What this builds on

- [[public-eval-headlines-hide-reliability-grader-noise-and-single-shot-limits|Public eval headlines hide reliability, grader noise, and single-shot limits]]
- [[safety-classifiers-fail-unattended-agents-need-a-real-sandbox|Safety classifiers fail; unattended agents need a real sandbox]]
