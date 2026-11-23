---
type: "source-note"
title: "Notes on: Designing Tools for Agents: The Agent-Computer Interface | AgentEngineering.org"
raw: "designing-tools-for-agents-the-agent-computer-interface-agentengineering-org"
url: "https://agentengineering.org/articles/designing-tools-for-agents/"
created_at: "2026-11-22T04:01:18Z"
updated_at: "2026-11-22T04:01:18Z"
---
- Archived full text: [[designing-tools-for-agents-the-agent-computer-interface-agentengineering-org|Full archived text, with credits]]
- Link: <https://agentengineering.org/articles/designing-tools-for-agents/>

## What it says

Anthropic's tool-design guidance translated into a practical guide: a tool surface is the contract the agent programs against, so names, descriptions, parameter schemas, response shapes, and error text are all prompt-engineering surfaces, not glue. The guide argues for building few task-shaped tools rather than mirroring API endpoints, making wrong calls structurally unrepresentable (poka-yoke), returning the smallest context-supporting results, writing errors that teach the next action, and evaluating the tool surface as its own artifact rather than relying on end-to-end task success.

## Claims drawn from this source

- **Tool definitions are prompts that behave like the system prompt.** Names, descriptions, parameter names, enums, response shape, and error text all go into the model's context and change behavior as much as the system prompt does.
- **Build few task-shaped tools instead of endpoint-shaped ones.** Rather than list_users/list_events/create_event, build schedule_event; rather than read_logs, build search_logs returning only matching lines with context; OpenAI recommends combining functions always called in sequence.
- **Smaller always-loaded surfaces select more reliably.** OpenAI suggests staying under twenty functions at the start of a turn, with overlap hurting more than raw count; beyond that, deferred tool loading keeps the always-loaded surface small.
- **Descriptions are the most effective lever on a tool surface.** Anthropic describes tools like onboarding docs and uses the intern test (could an intern use this given nothing but what the model is given?); Claude Sonnet 3.5 reached state-of-the-art on SWE-bench Verified after precise refinements to tool descriptions, and an append-2025 web search bug was fixed by description work, not model changes.
- **Make wrong calls structurally unrepresentable.** Poka-yoke rules: name the thing actually wanted (user_id not user), use enums and structure to rule out invalid states, do not expose identifiers already known in the runtime, constrain ranges in the schema rather than prose, and let the runtime inject identity/tenant/tokens rather than accept them from the model.
- **Responses and errors should carry the next decision.** Return high-signal information, resolve opaque UUIDs into semantically meaningful names (reported to improve Claude's retrieval precision), expose a response_format enum (concise used about a third of detailed tokens in Slack tooling), and make truncation explicit with a next_step; error text should identify the confusion, name the tool that produces the missing value, and say whether retrying helps.
- **Evaluate the tool surface separately from end-to-end success.** Anthropic describes a loop of realistic, verifiable tasks run programmatically, collecting tool errors, call counts, and token consumption; first-call selection evals isolate selection from downstream behavior, and held-out sets are needed because descriptions are easy to overfit.
