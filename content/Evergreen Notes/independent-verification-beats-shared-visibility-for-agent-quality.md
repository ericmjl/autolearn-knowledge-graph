---
type: "evergreen"
title: "Independent verification beats shared visibility for agent quality"
created_at: "2026-11-26T14:02:35Z"
updated_at: "2026-11-26T14:02:35Z"
inputs: ["notes-on-you-don-t-need-a-frontier-model-you-need-a-verifier-ai21", "independent-oversight-roles-not-shared-visibility-keep-agents-honest"]
provenance_urls: ["https://www.ai21.com/blog/you-need-a-verifier/", "https://en.wikipedia.org/wiki/Oversight", "https://en.wikipedia.org/wiki/Multi-agent_system", "https://blog.langchain.dev/langgraph-multi-agent-workflows/"]
refutation_status: "untested"
answers_questions: ["How should an independent verifier in a multi-agent system check an agent's work without sharing the agent's context, and does this scale to many agents?"]
---
Agent synthesis

Independent verification beats shared visibility for agent quality. An agent that re-reads the shared record learns what the others did; a verifier that starts from the question and the candidate answer instead gets to rule independently. The oversight evergreen says the checker must be a separate authority standing outside the agents being supervised (see: the checker separated from the checked, only final results in the shared record). The AI21 source sharpens this into a mechanism: correct answers are routinely already in the pool, plain majority voting cannot overturn the popular wrong answer, and the binding constraint is selection, not generation.

The mechanism is re-research, not re-inspection. A verifier given the candidate answer runs its own search-and-veto loop, narrow to one claim, and emits one verdict. Visibility into the shared record does not tell it what the agents did; fresh evidence means it can rule without the shared context. Across the tested pools, a Claude Opus verifier lifted a frontier ensemble from 83.3 to 93.4 on FACTS-Search, past published SOTA of 89.4, and 20 points sat idle in a small all-open-source pool, which the same verifier lifted from 60.1 to 80.4.

The evidence also fixes the failure modes. A stock small verifier (Qwen3-8B) recovers barely anything, 60.1 to 62.5, because the verification skill does not come free with parameters; training with SFT then RL fixes the search behavior without the verdict collapsing. Metrics must be computed per question and averaged, because rollout-level metrics routinely improve while the system degrades: verification lift for precision, recall cap (fraction of solvable questions where every correct answer is rejected) for the other side, aggregator headroom for the smarter-aggregator thread. Precision generalizes out of the box across benchmark and retrieval tool, lifting a held-out corpus benchmark from 39% to 51%, while the recall gap (27%) closes with one small SFT on ~85 questions. Verification adds at most 5% to system cost and its loops share no state, so sixteen verifications cost the wall clock of one.

The synthesis: the governance analogue is not "watch the agents" but "send the work to a fresh checker that does not share their context and measures it per question." Keep the checker out of the shared scratchpad, score the verifier on per-question lift and recall, and never trust rollout-level aggregate verdict metrics. Visibility is for logging; verification is for ruling.

## Where it comes from

- [[notes-on-you-don-t-need-a-frontier-model-you-need-a-verifier-ai21|You don't need a frontier model. You need a verifier. | AI21]]

## What this builds on

- [[independent-oversight-roles-not-shared-visibility-keep-agents-honest|Independent oversight roles, not shared visibility, keep agents honest]]
