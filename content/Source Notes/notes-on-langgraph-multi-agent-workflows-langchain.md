---
type: "source-note"
title: "Notes on: LangGraph: Multi-Agent Workflows (LangChain)"
raw: "langgraph-multi-agent-workflows-langchain"
url: "https://blog.langchain.dev/langgraph-multi-agent-workflows/"
created_at: "2026-11-21T03:02:23Z"
updated_at: "2026-11-21T03:02:23Z"
---
- Archived full text: [[langgraph-multi-agent-workflows-langchain|Full archived text, with credits]]
- Link: <https://blog.langchain.dev/langgraph-multi-agent-workflows/>

## What it says

The source introduces multi-agent workflows in LangGraph, defining them as multiple independent LLM-powered actors connected in a specific way, represented as a graph where agents are nodes and connections are edges that manage control flow and communicate via shared graph state. It argues that multi-agent designs help by grouping tools/responsibilities, allowing separate prompts (and even separate fine-tuned LLMs), and enabling individual evaluation and improvement of each agent. It walks through three example patterns—collaborative shared-scratchpad agents, an agent supervisor with independent scratchpads, and hierarchical teams of nested LangGraph agents—and notes tradeoffs such as verbosity when all work is passed along. It also compares LangGraph to Autogen (graph framing vs. conversation framing, plus LangChain/LangSmith integration) and CrewAI (lower-level controllability vs. higher-level abstraction).

## Claims drawn from this source

- **Multi-agent means multiple independent LLM-powered actors.** Each agent can have its own prompt, LLM, tools, and custom code, and the two main design questions are which agents exist and how they are connected.
- **Graph representation models agents as nodes and edges.** Agents are nodes, connections are edges, control flow is managed by edges, and agents communicate by adding to the graph's state.
- **Focused agents outperform tool-heavy monoliths.** Grouping tools/responsibilities and using separate prompts (with their own instructions, few-shot examples, or fine-tuned LLMs) can give better results than one agent selecting from dozens of tools.
- **Agents can be evaluated and improved individually.** The multi-agent conceptual model lets you evaluate and improve each agent separately without breaking the larger application.
- **Shared scratchpads are verbose and can be unnecessary.** In collaborative multi-agent examples, all work is visible to all agents, which can be overly verbose; sometimes only the final answer is needed.
- **Supervisor pattern uses independent scratchpads.** Agents keep their own scratchpads and append only final responses to a global scratchpad, with a supervisor routing to individual agents.
- **Hierarchical teams nest LangGraph agents as nodes.** In hierarchical teams, the nodes are themselves other LangGraph objects, connected by a supervisor agent, offering more flexibility than LangChain AgentExecutor runtimes.
- **LangGraph differs from Autogen and CrewAI in abstraction.** LangGraph uses an explicit graph/transition-probability model rather than Autogen's conversation framing and is LangChain/LangSmith-integrated, while CrewAI is higher-level and LangGraph offers lower-level controllability.
