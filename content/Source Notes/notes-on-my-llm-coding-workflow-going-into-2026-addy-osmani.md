---
type: "source-note"
title: "Notes on: My LLM coding workflow going into 2026 (Addy Osmani)"
raw: "my-llm-coding-workflow-going-into-2026-addy-osmani"
url: "https://addyosmani.com/blog/ai-coding-workflow/"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---
- Archived full text: [[my-llm-coding-workflow-going-into-2026-addy-osmani|Full archived text, with credits]]
- Link: <https://addyosmani.com/blog/ai-coding-workflow/>

## What it says

Addy Osmani argues that LLM coding tools in 2026 are powerful but require disciplined, structured workflows rather than push-button use. His recommended approach treats the LLM as a pair programmer needing clear direction, context, and oversight: start with a spec and plan, break work into small chunks, pack extensive context, choose the right model, use agents in a supervised way, keep humans verifying and testing everything, commit often, and customize the AI's behavior with rules and examples. The overarching stance is 'AI-assisted engineering' — leverage AI aggressively while remaining accountable for the software.

## Claims drawn from this source

- **Specs and plans come before code generation.** He brainstorms a detailed spec.md (requirements, architecture, data models, testing strategy) with the AI, then feeds it to a reasoning model to produce a step-by-step plan, iterating until coherent.
- **Break work into small, iterative chunks.** Large monolithic prompts cause inconsistency and duplication; focused tasks like one function or one bug fix keep the model on track and allow quick course-correction.
- **Provide extensive context and guidance.** Feed the model relevant code, docs, constraints, and pitfalls; use tools like MCP, gitingest, or repo2txt to package context, and give explicit instructions about what to avoid.
- **Choose the right model per task.** Different models have different personalities; swap or run multiple models in parallel to cross-check, and use the newest pro-tier versions when quality matters.
- **Use coding agents in a supervised way.** CLI and async agents (Claude Code, Codex CLI, Gemini CLI, Jules, Copilot Agent) accelerate mechanical work but should be guided with plans and specs, not left fully unattended.
- **Keep a human in the loop and test everything.** Never blindly trust LLM output; review line by line, run tests, and use a tight write-code/run-tests/fix loop, since agents without tests may falsely report success.
- **Commit often and use version control as a safety net.** Ultra-granular commits act as save points for rollback; branches and worktrees isolate parallel AI experiments so failures don't pollute main.
- **Customize AI behavior with rules and examples.** Rules files like CLAUDE.md, custom instructions, inline examples, and anti-hallucination clauses steer the model toward project conventions and reduce off-script output.
