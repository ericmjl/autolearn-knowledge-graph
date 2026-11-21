---
type: "source-note"
title: "Notes on: Agentic Coding is a Trap (Lars Faye)"
raw: "agentic-coding-is-a-trap-lars-faye"
url: "https://larsfaye.com/articles/agentic-coding-is-a-trap"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---
- Archived full text: [[agentic-coding-is-a-trap-lars-faye|Full archived text, with credits]]
- Link: <https://larsfaye.com/articles/agentic-coding-is-a-trap>

## What it says

The essay argues that agentic coding workflows—where a human acts as an orchestrator generating specs and reviewing agent output—create real trade-offs: increased system complexity to manage non-determinism, skill atrophy, vendor lock-in, and fluctuating token costs. It contends that the critical thinking and debugging skills needed to supervise agents are being degraded by overuse, even among experienced engineers, and that this inverts a developer's priority list away from understanding, conciseness, and standards toward raw speed. The author recommends demoting AI to a secondary role: using LLMs for specs, planning, pseudo-code, and ad-hoc delegation while staying actively engaged in implementation and review. The piece frames this as a risky experiment analogous to social media's long-term effects, warning that outsourcing all thinking to agents guarantees obsolescence.

## Claims drawn from this source

- **Agentic coding increases surrounding system complexity.** The workflow requires more surrounding systems to mitigate the ambiguity of AI non-determinism, adding overhead beyond the code itself.
- **Coding skills atrophy quickly with overuse.** Evidence shows skills can atrophy and dissipate within months; an Anthropic study reported a 47% drop-off in debugging skills.
- **Paradox of supervision undermines agent use.** Effectively using coding agents requires supervision, which requires the very coding skills that atrophy from AI overuse.
- **Junior developers lose learning friction.** Replacing direct code work with reviewing generated code truncates juniors' learning; review is at best 50% of the learning process.
- **Vendor lock-in and token costs are real risks.** Teams have stalled during Claude outages, and token costs fluctuate and rise while employee costs stay fixed.
- **LLMs accelerate the wrong parts of development.** Agentic workflows focus on speed and volume of generated code, not understanding or conciseness; forced speed leads to lower accuracy.
- **Spec-driven orchestration disconnects humans from code.** LLMs fill ambiguity with assumptions or hallucinations, causing more review, revisions, tokens burned, and distance from the generated code.
- **Use LLMs as secondary processes, not primary drivers.** The author uses LLMs for specs/plans, pseudo-code, and ad-hoc delegation, stays engaged with implementation, and never generates more than can be reviewed in a sitting.
