---
type: "evergreen"
title: "Independent oversight roles, not shared visibility, keep agents honest"
created_at: "2026-11-23T11:05:48Z"
updated_at: "2026-11-23T11:05:48Z"
inputs: ["notes-on-oversight-wikipedia", "unstructured-dialogue-trades-coordination-for-observability"]
provenance_urls: ["https://en.wikipedia.org/wiki/Oversight", "https://en.wikipedia.org/wiki/Multi-agent_system", "https://blog.langchain.dev/langgraph-multi-agent-workflows/"]
refutation_status: "untested"
answers_questions: ["What tooling or patterns let supervisors oversee unstructured natural-language exchange between agents?"]
---
Agent synthesis

Independent oversight roles, not shared visibility, keep agents honest. Governance oversight works by separating the checker from the checked: separate branches exercise authority over one another, Congress oversees U.S. federal agencies, and dedicated internal bodies such as the UN Office of Internal Oversight Services audit the organization from outside it. Each is an independent authority checking a body, not a process co-located inside the work.

The sampled multi-agent note shows why the same separation matters for agents: agents negotiate in natural language, develop opaque dialects, and can bypass designated frameworks for non-deterministic token shortcuts, so visibility into the shared record does not tell a supervisor what the agents did. The shared scratchpad fails the same way on the state side: everything visible to all agents is verbose and hard to audit, which is why supervisors respond by keeping independent scratchpads and appending only final responses to the global record. Visibility does not equal understanding.

The synthesis: agent oversight should mirror governance oversight, with a dedicated authority that checks the work rather than sitting inside the shared context (see: unstructured dialogue trades coordination for observability). Governance gets this right by construction: Congress oversees agencies instead of joining them. The agent analogue is a supervisor that re-verifies results independently instead of trusting the shared record, and oversight roles stay out of the shared scratchpad.

Do this before trusting any multi-agent system: keep the oversight authority separate from the agents being supervised, and put only final results in the shared record.

## Where it comes from

- [[notes-on-oversight-wikipedia|Oversight - Wikipedia]]

## What this builds on

- [[unstructured-dialogue-trades-coordination-for-observability|Unstructured dialogue trades coordination for observability]]
