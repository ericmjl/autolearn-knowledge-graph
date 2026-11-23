---
title: "Multi-Agent Handoff Patterns That Actually Work"
type: "raw-source"
url: "https://www.orzed.com/insights/multi-agent-handoff-patterns-that-actually-work"
author: "ORZED LLC"
publication: "Orzed"
published: "2026-04-18"
archived: "2026-11-22T05:02:18Z"
---

> [!quote] Original source
> **Author(s):** ORZED LLC  
> **Title:** Multi-Agent Handoff Patterns That Actually Work  
> **Published in:** Orzed  
> **Date:** 2026-04-18  
> **Original:** <https://www.orzed.com/insights/multi-agent-handoff-patterns-that-actually-work>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-multi-agent-handoff-patterns-that-actually-work|Source note]]
Themes: [[Agent design patterns]]
Why it was archived: How can multi-agent systems keep unstructured dialogue flexible while producing auditable, non-bloated shared state?

## Archived text

Multi-Agent Handoff Patterns That Actually Work

- Most multi-agent systems are single-agent systems with extra steps that add cost without adding capability.
- A baton-pass handoff with a structured contract works when the second agent has a clearly different specialty.
- Supervisor-specialist patterns work when the orchestration logic itself is the value, not the specialists.
- Confidence-routed fallback works when the cheap agent passes 80%+ of cases and a stronger one cleans up the rest.

We were called in to audit a customer-support agent system that had grown from one agent to seven over six months. Each addition had been justified at the time (a triage agent, a research agent, a writer agent, a verifier agent, a translator agent, an escalation agent, a meta-coordinator). The system worked in demos, took 18 to 42 seconds end-to-end, cost roughly 4 cents per resolved query, and had a 12% rate of “lost in handoff” failures where a later agent ignored or misread an earlier agent’s output.

We collapsed the system to two agents over two weeks. End-to-end latency dropped to under 6 seconds. Per-query cost fell to 0.9 cents. The lost-in-handoff rate dropped to under 2%. The product team noticed customer-satisfaction scores improved.

This piece is about how to know which agents are pulling their weight and which patterns of multi-agent handoff actually justify the orchestration overhead.

When a second agent is worth adding

A second agent earns its keep when one of three conditions is true:

- The second agent has a genuinely different capability the first agent cannot perform reliably (different tool list, different model with different strengths, different prompt context that would not fit alongside the first agent’s).
- The second agent provides a measurable safety property (a verifier that catches outputs the first agent gets wrong; a separate model judging the first model’s output for policy compliance).
- The orchestration of multiple agents is itself the product (a research workflow that explicitly mirrors a multi-step human process, where the steps are independently observable).

Most multi-agent systems we audit fail all three tests. They were built because “agents in a swarm” sounded impressive, not because the architecture was the answer to a measured problem. The first migration is usually a delete.

Pattern 1: structured baton-pass

The simplest and most reliable multi-agent pattern is the baton-pass. Agent A produces a typed payload. Agent B consumes that payload (not the chat history that produced it). Agent B does not see Agent A’s reasoning or scratchpad, only the structured handoff.

# Pattern sketch (not real code)

class TriageOutput(BaseModel):

    intent: Literal['refund', 'shipping', 'product_question', 'other']

    customer_id: int

    sentiment: Literal['neutral', 'frustrated', 'angry']

    urgency: Literal['low', 'medium', 'high']

    relevant_facts: list[str]

triage_result = triage_agent.run(user_message)  # produces TriageOutput

if triage_result.intent == 'refund':

    response = refund_agent.run(triage_result)

elif triage_result.intent == 'shipping':

    response = shipping_agent.run(triage_result)

# ...

Two properties make this work:

Typed payload contract. The handoff is JSON with a known schema. Agent B’s prompt includes a description of the schema and treats the input as data, not instructions. This eliminates the “chat history pollution” failure mode where Agent B gets confused by Agent A’s reasoning text.

No shared chat history. Agent B starts a fresh conversation. Its only input is the structured payload plus its own system prompt. Tokens are saved, context is clean, debugging is straightforward.

When this pattern fits: you have a routing or pipeline shape where one agent classifies and another acts. The classification step is short and cheap; the action step needs different context or tools.

Pattern 2: supervisor with specialists

The supervisor pattern places one agent (the supervisor) in control of one or more specialist agents. The supervisor receives the user’s request, decides which specialist to invoke, calls them through a tool interface, and synthesises the result.

# The supervisor sees specialists as tools, not as peers

supervisor_tools = [

  {'name': 'research', 'description': 'Searches our internal docs and web. Returns sources.'},

  {'name': 'compute_quote', 'description': 'Generates a price quote. Returns line items.'},

  {'name': 'check_inventory', 'description': 'Returns current stock for a SKU.'},

]

The supervisor’s prompt describes when to use each specialist. The specialists themselves are agents (they have their own tool lists and reasoning loops), but from the supervisor’s perspective they are just tools that take a structured input and return a structured output.

When this pattern fits: the orchestration is the value. A research workflow that explicitly chains “search, then verify sources, then summarise” benefits from the supervisor pattern because the steps are independently observable and adjustable. The supervisor itself can be a smaller model; the specialists pick the right size for their job.

The trap: supervisor-as-orchestrator is tempting to over-use because it scales conceptually. In practice, more than three specialists per supervisor produces a coordination overhead that erases the benefit. If you find yourself writing a supervisor with seven specialist tools, the architecture is wrong; you have built an agent that is calling agents that are calling agents.

Pattern 3: confidence-routed fallback

Two agents (or models) configured as a primary and a fallback. The primary is cheap and fast, handles most cases well. The fallback is more expensive (stronger model, larger context) and handles the cases the primary is uncertain about.

The router is a small classifier or, more commonly, a confidence threshold on the primary’s output:

result, confidence = primary_agent.run(input)

if confidence &lt; 0.85:

    result = fallback_agent.run(input)

The “confidence” can come from log-probability of the model’s response, from a verifier model, or from a deterministic check (does the JSON parse, does the answer match a regex pattern). The exact source matters less than the fact that there is one.

When this pattern fits: the cheap primary agent passes a clear majority (typically 70 to 90 percent) of cases at adequate quality, and the cost of the fallback is justified only on the residual. The economics: if the primary costs 0.3 cents and the fallback 1.2 cents, with 80% routing to primary, the average per-query cost is 0.8 * 0.3 + 0.2 * 1.2 = 0.48 cents, versus 1.2 cents on the fallback alone. A 2.5x cost reduction with no quality regression is the entire point.

Failure modes to design against

Three failure modes show up across all three patterns. Building against them at design time is cheaper than diagnosing them in production.

Lost-in-handoff. Agent B ignores or misreads Agent A’s output. Causes: free-form chat history instead of typed payload, prompt that does not establish “this input is data, not your instructions”, or schema fields the second agent’s prompt does not reference. Fix: typed contracts, validate the handoff with deterministic code before passing.

Cascading hallucination. Agent A invents a fact. Agent B treats the fact as input and reasons over it. Agent C cites the fabrication as if it were grounded. Each handoff is plausible; the chain is wrong. Fix: every agent that produces facts must cite sources, and every agent that consumes facts must validate or surface the citation.

Latency stack. Each agent adds 1 to 5 seconds. A four-agent pipeline takes 20 seconds. Users abandon. Fix: parallelise where the agents are independent; minimise the number of agents in the critical path; budget end-to-end latency at design time.

Observability hooks the team needs

A multi-agent system without per-handoff observability is a system the team cannot debug. Minimum hooks:

These are not optional. A team without them is debugging an agent system by squinting at chat history.

How we approach it on engagements

When we walk into a multi-agent system, the first measurement is the per-agent contribution to the final outcome. We pull a sample of recent traces, identify cases where each agent’s contribution was material, and produce a contribution-attribution report.

The report usually shows that one or two agents do most of the work. The others are either redundant or handle edge cases the system could route differently. Removing them simplifies the architecture, reduces cost, and almost always improves quality (less coordination overhead, less context dilution).

The right number of agents in a production system is the smallest number that meets the quality bar. We have seen four-agent systems collapse to one without quality loss, and we have seen one-agent systems where adding a verifier as a second agent improved correctness by twelve percentage points. The number is empirical; the design discipline is to keep asking whether each agent earns its place.

Frequently asked questions

Is more agents always better?

No. Each additional agent adds latency, cost and a new class of failure modes. A second agent earns its keep only when it closes a measurable failure of the first. Default to single-agent until you can name the gap a second one closes.

How do agents pass context to each other?

Through a structured contract, not through chat history. Pass a typed payload (JSON) with named fields. Free-form prompt-stuffing produces hand-off failures that are invisible until they manifest as wrong outputs.

Should agents share memory?

Rarely. Shared memory creates coupling that defeats the point of separation. Each agent should have its own context plus a small structured handoff payload. If they need shared state, that state belongs in a database, not in their context windows.
