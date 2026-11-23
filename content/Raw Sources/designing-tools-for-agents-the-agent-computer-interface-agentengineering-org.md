---
title: "Designing Tools for Agents: The Agent-Computer Interface | AgentEngineering.org"
type: "raw-source"
url: "https://agentengineering.org/articles/designing-tools-for-agents/"
author: "AgentEngineering.org (no individual author named)"
publication: "AgentEngineering.org"
published: "2026-10-12"
archived: "2026-11-22T04:00:49Z"
---

> [!quote] Original source
> **Author(s):** AgentEngineering.org (no individual author named)  
> **Title:** Designing Tools for Agents: The Agent-Computer Interface | AgentEngineering.org  
> **Published in:** AgentEngineering.org  
> **Date:** 2026-10-12  
> **Original:** <https://agentengineering.org/articles/designing-tools-for-agents/>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-designing-tools-for-agents-the-agent-computer-interface-agentengineering-org|Source note]]
Themes: [[Context, memory and tools]]
Why it was archived: What distinguishes a well-crafted tool interface (docstrings, poka-yoke constraints) from an awkward one

## Archived text

Most teams treat tools as plumbing: the model is the interesting part, the reasoning is the interesting part, and tools are a thin layer of glue over an existing API. That assumption is expensive, because the tool surface is not glue. It is the interface the agent programs against, and the only part of your system the model can see.

Tool Use: How Agents Take Action covers what happens during a call and introduces the Action Contract: what capability is requested, what inputs execution requires, what limits apply before execution, and what signals prove the action worked. This guide is the companion to it, about the other side of that contract — the side you write.

TL;DR

A tool definition is a prompt that happens to be machine-readable. Names, descriptions, parameter names, enums, response shape, and error text all go into the model’s context, and all of them change behavior as much as the system prompt does. Design them for an agent that has no memory of your codebase, no access to your wiki, and no ability to ask a colleague what user means.

Three decisions carry most of the weight. Build a few tools that match whole tasks instead of mirroring your API endpoints. Make wrong calls structurally impossible rather than merely discouraged. Return the smallest result that still supports the next decision, and when something fails, say what to do about it.

The Tool Surface Is the Interface

Anthropic calls this the agent-computer interface, and frames tools as “a contract between deterministic systems and non-deterministic agents” in Writing effective tools for agents. When you write a function for another engineer, that contract is enforced by code review, type checkers, and a human who can read the implementation when the docstring is unclear. When you write a tool for an agent, it is enforced by whatever the model infers from a name, a sentence or two of description, and a JSON Schema.

That inference happens fresh on every call, under context pressure, mid-task. The model cannot step into the implementation or check how the last team used the endpoint. If your parameter is called user and the model has a customer’s email address in context, it will put the email in user, because nothing told it otherwise. In the trace that looks like a model mistake. It is an interface defect.

The loop-back arrow is the part people underestimate. A tool result is not an output delivered to a user, it is an input to the agent’s next decision, and it occupies context for the remainder of the run. That makes response design a reasoning concern rather than a formatting preference.

Choose Which Tools to Build

The default instinct is to expose what already exists. You have a REST API with thirty endpoints, so you generate thirty tools and let the model figure out how to compose them. This produces a tool surface that is simultaneously too large to select from reliably and too granular to accomplish anything without many round trips, each of which spends context and adds a chance to go wrong.

Anthropic’s recommendation is to build a few thoughtful tools targeting specific high-impact workflows, and their examples are worth copying directly. Rather than list_users, list_events, and create_event, build a schedule_event tool that finds availability and books the meeting. Rather than read_logs, build search_logs, which returns only matching lines with surrounding context. Rather than get_customer_by_id, list_transactions, and list_notes, build get_customer_context, which assembles the relevant history in one call. OpenAI gives the same advice from a different angle in its function calling guide: combine functions that are always called in sequence, and if you always call mark_location() after query_location(), move the marking into the query.

The underlying principle is that work done inside a tool is work the agent does not have to do with tokens. An agent that calls three tools to assemble a customer’s history spends three decisions and three result payloads on what one well-chosen tool could hand it, and every one of those payloads stays in context for the rest of the run.

The operations agent in Tool Use is a good test case. It starts with six endpoint-shaped tools:

get_job_run            → one row from the scheduler

read_logs              → the whole log file for a run

get_recent_deploys     → deploy list for a service

check_dependency_health → status of one dependency

retry_job              → re-runs a job

open_incident          → creates an incident record

Three of those are not tasks an agent performs, they are rows an API returns. The agent never wants a job row on its own; it wants to know why a run failed. Consolidating around that intent gives a smaller surface:

get_job_failure_context → run status, the failing step, matching log lines,

                          deploys in the window, and dependency health,

                          assembled in one call

search_job_logs         → matching lines plus surrounding context, filtered

retry_job               → re-runs a job, idempotently

open_incident           → creates an incident record

Four tools instead of six, and the first replaces the three-or-four-call opening sequence every investigation used to start with. The count is not the point. The point is that each remaining tool corresponds to a decision the agent makes, which means the name alone is usually enough to select correctly.

How Many Is Too Many

OpenAI’s guide suggests aiming for fewer than twenty functions available at the start of a turn, while calling it a soft suggestion and recommending you measure accuracy at different counts yourself. The mechanism behind the advice is the part worth internalizing: tool definitions are injected into the model’s context and billed as input tokens, so a large surface costs money and context on every call, whether or not any of those tools get used.

When a surface genuinely has to be large, the answer is deferred loading rather than a longer list. OpenAI’s guide describes a tool search mechanism where the model finds relevant tools and loads them on demand, and MCP’s extensions take a related approach with skills that an agent discovers when it needs them. Either way, keep the always-loaded surface small and make everything else reachable.

Make the Right Tool Obvious

Namespace by Service and Resource

Once an agent has tools from more than one source, name collisions become the dominant selection failure. Two servers both expose search, and the model picks whichever description sounded more relevant, which is a coin flip dressed up as reasoning. Anthropic recommends namespacing by service (asana_search, jira_search) and by resource (asana_projects_search, asana_users_search), and reports that the choice between prefix and suffix schemes had non-trivial effects on their own tool-use evaluations, varying by model.

The MCP tools specification bakes the same problem into its guidance: tool names only have to be unique within a single server, so clients that aggregate several servers are told to expect collisions and disambiguate, typically by prefixing with a server identifier. If you write a server, do not assume the client will do that well. Prefix your own tools.

Write Descriptions Like Onboarding Docs

The most effective lever on a tool surface is usually the description, because it is the only place to put the context that you carry implicitly and the model does not have: query formats, domain vocabulary, relationships between resources, and the cases where this tool is the wrong choice. Anthropic’s framing is to describe the tool the way you would describe it to a new hire. OpenAI’s is the intern test: could an intern use this function correctly given nothing but what you gave the model, and if not, what would they ask you?

Here is a description that fails that test, in a schema that looks perfectly professional:

{

  "name": "search_job_logs",

  "description": "Search logs.",

  "input_schema": {

    "type": "object",

    "properties": {

      "query": { "type": "string" },

      "job": { "type": "string" },

      "window": { "type": "string" }

    },

    "required": ["query"]

  }

}

Nothing here is wrong, and nothing here is usable. Is query a substring, a regex, or a Lucene expression? Is job a name or an identifier? Is window "1h", "last hour", or an ISO interval? The model will guess, and because the schema accepts any string, the guess will be syntactically valid and semantically wrong. The rewrite changes no functionality at all:

{

  "name": "search_job_logs",

  "description": "Search the log lines emitted by one scheduled job run and return matching lines with surrounding context. Use this after get_job_failure_context when you need more detail about a specific error, not as the first step of an investigation. Matching is case-insensitive substring matching, not regex: pass 'connection refused', not '/connection.*refused/'. Returns at most 50 matches, newest first; narrow the query or shorten the window rather than paging through everything.",

  "input_schema": {

    "type": "object",

    "properties": {

      "run_id": {

        "type": "string",

        "description": "Scheduler run identifier, format 'run_' followed by 12 hex characters, e.g. 'run_8f21ca40b7d9'. Available as 'run_id' in get_job_failure_context results. Not the job name."

      },

      "query": {

        "type": "string",

        "description": "Case-insensitive substring to match against the log line body, e.g. 'connection refused' or 'OOMKilled'."

      },

      "context_lines": {

        "type": "integer",

        "description": "Log lines to include on each side of a match. Defaults to 3. Use 0 when you only need to know whether the string appears.",

        "minimum": 0,

        "maximum": 20,

        "default": 3

      },

      "level": {

        "type": "string",

        "description": "Minimum severity to include. Defaults to 'warn', which excludes routine info logging.",

        "enum": ["debug", "info", "warn", "error", "fatal"],

        "default": "warn"

      }

    },

    "required": ["run_id", "query"],

    "additionalProperties": false

  }

}

The second version answers the questions the first one raised, states what the tool is not for, gives the identifier’s format and where it comes from, and tells the agent what to do instead of paging. That last line is a behavioral instruction smuggled into a schema, which is exactly where instructions about this tool belong.

Anthropic reports that Claude Sonnet 3.5 reached state-of-the-art performance on SWE-bench Verified after precise refinements to tool descriptions, and that when their web search tool shipped, Claude was appending 2025 to the query parameter and biasing its own results, which they fixed by improving the description rather than the model. Description work is not cosmetic polish.

Design Parameters So the Wrong Call Is Hard to Make

Good parameter design borrows from poka-yoke, the manufacturing practice of shaping a part so it cannot be installed backwards. You are not trying to document the correct call. You are trying to make the incorrect call unrepresentable.

Four rules cover most of it.

Name the thing you actually want. Anthropic’s example is the one to remember: instead of a parameter named user, use user_id. The suffix tells the model the shape of the value, and when the model does not have an identifier, a parameter named user_id makes the gap visible instead of inviting a plausible substitute.

Use enums and structure to make invalid states impossible. OpenAI’s example is toggle_light(on: bool, off: bool), which permits two contradictory calls out of four. The fix is one enum. Free-text strings where you mean a closed set are the same bug: if environment can only be production or staging, say so in the schema rather than in the description, because the schema is enforced and the description is advisory.

Do not ask for arguments you already have. OpenAI’s guide is blunt about this: if you already have the order_id from an earlier step, do not expose it as a parameter, define submit_refund() and pass the identifier from your own code. This applies with real force to anything security-relevant. Auth tokens, tenant identifiers, and the acting user’s identity should be injected by the runtime, never accepted from the model, because a parameter the model fills is a parameter prompt injection can steer.

Constrain ranges in the schema, not the prose. minimum, maximum, enum, pattern, and default are all enforced by JSON Schema validation before your code runs. OpenAI recommends always enabling strict mode, which uses structured outputs to guarantee that arguments adhere to the schema instead of merely tending to; it requires additionalProperties: false and some care about which keywords you use.

Here is the shape that falls out of those rules, with the runtime holding what the model should never see:

# Tool definition exposed to the model: no identity, no tenant, no tokens.

RETRY_JOB_TOOL = {

    "name": "retry_job",

    "description": (

        "Re-run one failed scheduled job run. Only runs with status 'failed' "

        "or 'timed_out' can be retried. Always call with dry_run=true first "

        "and read the 'would_do' summary; call again with dry_run=false only "

        "after the user has approved a production retry."

    ),

    "input_schema": {

        "type": "object",

        "properties": {

            "run_id": {

                "type": "string",

                "pattern": "^run_[0-9a-f]{12}\$",

                "description": "Run to retry, e.g. 'run_8f21ca40b7d9'.",

            },

            "reason": {

                "type": "string",

                "maxLength": 200,

                "description": "Why the retry is safe, recorded on the audit trail.",

            },

            "dry_run": {

                "type": "boolean",

                "default": True,

                "description": "When true, validate and report without re-running.",

            },

        },

        "required": ["run_id", "reason", "dry_run"],

        "additionalProperties": False,

    },

}

def retry_job(args: dict, ctx: RuntimeContext) -> dict:

    """ctx carries the caller's identity, tenant, and token. The model

    cannot see or set any of it, so injection cannot escalate through it."""

    run = scheduler.get_run(args["run_id"], tenant=ctx.tenant_id)

    if run.status not in ("failed", "timed_out"):

        return tool_error(

            f"Run {run.id} has status '{run.status}' and cannot be retried. "

            "Only 'failed' and 'timed_out' runs are retryable. "

            "Call get_job_failure_context to confirm the current status.",

            retryable=False,

        )

    if not ctx.permissions.allows("job.retry", environment=run.environment):

        return tool_error(

            f"Retrying {run.environment} jobs needs an approval from an "

            "on-call engineer. Summarize the failure and ask the user to "

            "approve before calling again.",

            retryable=False,

        )

    if args["dry_run"]:

        return {

            "would_do": f"Re-run step '{run.failing_step}' of {run.job_name}",

            "environment": run.environment,

            "estimated_duration_seconds": run.p50_duration_seconds,

        }

    return scheduler.retry(

        run.id,

        actor=ctx.user_id,

        reason=args["reason"],

        idempotency_key=f"retry:{run.id}:{ctx.turn_id}",

    )

Note that dry_run is required rather than optional even though it has a default. Requiring it forces the model to state an intention, which shows up in the trace and gives your permission layer something explicit to check. That is the Action Contract’s third question, “what limits or approvals apply before execution”, answered in the schema instead of in a runbook.

Return Context, Not Payloads

A tool response is the most expensive thing a tool produces, because it is paid for twice: once in tokens and once in every subsequent decision the agent makes while that text sits in context. Anthropic’s guidance is to return high-signal information and to drop low-level technical identifiers such as uuid, mime_type, and 256px_image_url in favor of fields like name and file_type that actually inform the next action. They also report that resolving opaque alphanumeric UUIDs into semantically meaningful names significantly improved Claude’s precision on retrieval tasks by reducing hallucinations, which is an unusually direct piece of evidence that identifier design changes model accuracy.

When an agent sometimes needs identifiers and sometimes needs prose, expose the choice. Anthropic’s pattern is a response_format enum with concise and detailed values; in their Slack tooling, the concise form used roughly a third of the tokens of the detailed one. The agent asks for detail when it needs identifiers for a follow-up call, and stays cheap the rest of the time.

Truncation deserves the same care. Claude Code caps tool responses at 25,000 tokens by default, and the useful part of that design is not the cap but what happens at the boundary: a truncated response should say that it was truncated and tell the agent what to do about it. A silently cut response is worse than an error, because the agent reasons confidently over a partial picture and has no signal that anything is missing.

MAX_MATCHES = 50

def search_job_logs(args: dict, ctx: RuntimeContext) -> dict:

    matches = logs.search(

        run_id=args["run_id"],

        substring=args["query"],

        min_level=args.get("level", "warn"),

        tenant=ctx.tenant_id,

    )

    page = matches[:MAX_MATCHES]

    result = {

        "run_id": args["run_id"],

        "job_name": logs.job_name_for(args["run_id"]),  # not a UUID

        "matches": [

            {

                "at": m.timestamp.isoformat(),

                "level": m.level,

                "line": m.body,

                "context": m.surrounding(args.get("context_lines", 3)),

            }

            for m in page

        ],

        "match_count": len(page),

    }

    if len(matches) > MAX_MATCHES:

        result["truncated"] = True

        result["total_matches"] = len(matches)

        result["next_step"] = (

            f"Showing the {MAX_MATCHES} newest of {len(matches)} matches. "

            "Narrow the search with a more specific query or a higher "

            "'level' rather than requesting more pages."

        )

    return result

The next_step string is doing real work. It converts a limit the agent cannot see into an instruction the agent can follow, which is the difference between a tool that degrades gracefully and one that sends the agent into a paging loop.

Write Errors That Teach the Next Action

Error text is the highest-leverage prose in a tool surface, because it is read at exactly the moment the agent is deciding what to do next. The MCP specification separates two cases in a way worth adopting regardless of whether you use MCP. Protocol errors cover malformed requests and unknown tools, which models are unlikely to be able to fix. Tool execution errors cover validation failures, API failures, and business-rule violations, and the spec describes these as containing “actionable feedback that language models can use to self-correct and retry with adjusted parameters”, reported in the result with isError: true rather than as a transport failure. Clients should pass those to the model; the spec’s own example is Invalid departure date: must be in the future. Current date is 08/08/2025.

That example is instructive because it contains three things: what was wrong, what the rule is, and the fact the model needed in order to comply. Compare the two versions of the same failure:

# Unhelpful: accurate, actionable by nobody

{"error": "ValidationError", "code": 422, "detail": "invalid run_id"}

# Helpful: names the rule, the likely cause, and the next move

{

  "error": "invalid_run_id",

  "message": "'nightly-billing' is a job name, not a run identifier. run_id

    looks like 'run_8f21ca40b7d9'. Call get_job_failure_context with

    job_name='nightly-billing' to get the most recent run_id, then retry.",

  "retryable": true

}

The second version costs more tokens and saves a turn, usually several. Three properties make the difference. It identifies the confusion rather than the symptom, because “invalid run_id” and “you passed a job name where a run identifier goes” lead to very different next attempts. It names the tool that produces the missing value, so recovery does not depend on the agent remembering your surface. And it says whether retrying could possibly help, because an agent with no retryability signal will often retry an unretryable call until it hits a step cap.

Two failure modes to design out. Do not return stack traces: they are long, they leak internals, and the useful sentence is buried. Do not return a bare 500 for a business-rule rejection, because the agent will treat a policy decision as a transient fault and try again.

Make Repeated Calls Safe

Agents retry. They retry after timeouts, after ambiguous results, after a context reset, and sometimes because a result was truncated and the agent decided to start over. Any tool with side effects will therefore be called more than once with the same intent, and the question is only whether your tool was designed for it.

Idempotency keys are the standard answer, and payments is the right place to copy from because the problem has been solved there under adversarial conditions for years. Stripe’s idempotent requests design is the reference: the caller supplies a key, the server records the outcome against it, and a repeat with the same key returns the original result instead of doing the work twice. For agents the twist is where the key comes from. Do not accept it as a model-supplied parameter, because the model has no reliable notion of which attempts are “the same” — derive it in the runtime from something stable about the turn, as retry_job above does with f"retry:{run.id}:{ctx.turn_id}".

Dry runs and confirmations handle the rest. A dry_run parameter lets an agent inspect consequences before causing them, which is the cheapest way to make a dangerous tool safe. For anything genuinely irreversible the approval belongs in the runtime rather than in the agent’s judgment, which is the subject of Human-in-the-Loop Control Design. MCP supports this in the protocol: a server can answer a call with an input_required result carrying an elicitation request, and its security guidance tells clients to confirm sensitive operations with the user and to show tool inputs before calling.

One line from that guidance is the most often skipped: clients MUST treat tool annotations, including descriptions of tool behavior, as untrusted unless they come from a trusted server. A tool description is third-party text that lands in your model’s context, so servers you do not control can instruct your agent. Structured Outputs, Guardrails, and Execution Boundaries is where that boundary gets enforced. The scoping decision upstream of it — which tools may read private data, which may read attacker-influenced text, and which may send anything outward — is the lethal trifecta audit in Agent Security.

Evaluate the Tools, Not Just the Agent

Everything above is a hypothesis until you measure it, and the practice that makes tool design tractable is to evaluate the tool surface as its own artifact, with its own test set, separately from end-to-end task success. Anthropic describes exactly this loop: generate tasks grounded in real usage, pair each with a verifiable outcome, run them programmatically, and collect tool errors, call counts, and token consumption alongside accuracy. They are explicit that tasks should be realistic rather than sandboxed, and that you should hold out a test set, because tool descriptions are easy to overfit.

A useful first eval is narrow: given a realistic prompt, does the agent reach for the right tool with well-formed arguments on the first call? That isolates selection and argument formation from everything downstream, so a regression points at a specific description or schema rather than at “the agent got worse”.

# test_tool_selection.py — provider-neutral first-call eval.

# pytest -q test_tool_selection.py

import json

import pytest

from agent import first_tool_call  # one model call, returns (name, args)

from tools import TOOLS

CASES = [

    {

        "id": "why-did-it-fail",

        "prompt": "The nightly billing job failed again. What happened?",

        "expect_tool": "get_job_failure_context",

        "expect_args": {"job_name": "nightly-billing"},

    },

    {

        "id": "needs-run-id-first",

        "prompt": "Search the billing job logs for connection errors.",

        "expect_tool": "get_job_failure_context",  # must resolve run_id first

        "forbid_args": ["run_id"],  # inventing an identifier is the failure

    },

    {

        "id": "no-retry-without-approval",

        "prompt": "Just retry the production billing job now.",

        "expect_tool": "retry_job",

        "expect_args": {"dry_run": True},  # dry run before the real thing

    },

    {

        "id": "not-an-incident-yet",

        "prompt": "Did the billing job run last night?",

        "forbid_tool": "open_incident",  # a read question, not an escalation

    },

]

@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])

def test_first_call(case, record_property):

    name, args = first_tool_call(case["prompt"], TOOLS)

    record_property("selected", json.dumps({"tool": name, "args": args}))

    if "expect_tool" in case:

        assert name == case["expect_tool"], f"selected {name}"

    if "forbid_tool" in case:

        assert name != case["forbid_tool"], f"should not call {name}"

    for key, value in case.get("expect_args", {}).items():

        assert args.get(key) == value, f"{key}={args.get(key)!r}"

    for key in case.get("forbid_args", []):

        assert key not in args, f"invented {key}={args.get(key)!r}"

Two things make this worth running rather than admiring. Model calls are non-deterministic, so a single pass tells you little; run each case several times and track the pass rate per case, which turns “flaky” into a number you can threshold in CI. And record what the agent actually selected on failure, because the diagnostic value is in the wrong call, not in the assertion. A case that fails by inventing a run_id is telling you the description does not say where identifiers come from.

Beyond pass rates, the metrics that reliably catch bad tool design are the ones Anthropic names: invalid-parameter error rates, which point at unclear descriptions or missing examples, and redundant call counts, which point at pagination or result limits that are set wrong. Which evaluators to write next should come from reading real traces rather than from a list like this one, which is the argument in Hamel Husain’s evals FAQ and the reason error analysis sits ahead of eval authoring. Evaluating Agent Trajectories, Not Just Outputs covers the trajectory-level version of this once first-call behavior is solid.

A Worked Failure: The Nightly Billing Job

Here is the failure this guide exists to prevent, in the shape it usually arrives.

An operations agent is asked why the nightly billing job failed. It calls read_logs with job="nightly-billing", and because the parameter is a free-text string, the call validates. The tool returns 40,000 tokens of log output, most of it routine. The agent reads the first error-looking line — a downstream connection timeout that is a symptom of the real failure rather than its cause — and concludes the dependency is unhealthy. It calls retry_job, which returns {"status": "queued"}. The retry fails the same way eleven minutes later, and nobody notices until morning, because the agent reported a successful remediation.

Four design defects, one at each stage of the diagram. The surface was endpoint-shaped, so the investigation opened with a raw log dump instead of assembled context. The parameter accepted a job name where a run identifier belonged, so a wrong call looked right. The response was unfiltered and untruncated, so the agent’s attention landed on whatever came first. And queue acceptance was reported as success, leaving the Action Contract’s fourth question — what signals prove the action worked — unanswered.

The redesigned surface fails differently. get_job_failure_context returns the failing step, matching log lines, deploys in the window, and dependency health together, so cause and symptom arrive in one payload. search_job_logs requires a run_id matching ^run_[0-9a-f]{12}\$, so a job name produces an error naming both the confusion and the tool that resolves it. Truncation is explicit and says to narrow rather than page. And retry_job with dry_run=true reports what it would do, where, and for roughly how long before anything executes, with the production path gated on an approval the runtime checks rather than the model remembers.

None of that made the model smarter. It changed what the model could see and what it was able to express.

When Not to Build a Tool

More tools is not the goal, and some things that look like tools should not be.

The most common case is the first one. A tool is justified when the agent genuinely chooses whether and how to use it. If the answer is always yes and the arguments are always the same, you have written a workflow step with extra latency and a chance of being skipped.

FAQ

How many tools can an agent handle before selection degrades?

Fewer than you would like, and the number depends on how much the tools overlap rather than on the count alone. OpenAI suggests staying under twenty at the start of a turn as a soft guideline and recommends measuring accuracy at different counts on your own surface. Overlap is what actually hurts: five tools with clear, distinct jobs select more reliably than three that could each plausibly answer the same question.

Should I just expose my REST API as tools?

Usually not, and this is the most common way tool surfaces go wrong. Endpoints are shaped around resources and round trips, which is correct for a client with cheap memory and wrong for an agent with limited context. Start from the tasks the agent performs, build a tool per task, and let each one make as many internal API calls as it needs.

Do I need MCP for any of this?

No. Every principle here applies to plain function calling. MCP matters when you want tools to be portable across hosts or want to consume servers other people maintain, and its specification is a useful source of conventions regardless: namespacing guidance, the split between protocol and execution errors, and the instruction to treat third-party tool descriptions as untrusted. MCP in Practice covers the protocol itself, including what changed in the 2026-07-28 revision.

How do I stop the model from inventing identifiers?

Make the identifier’s shape unrepresentable when wrong and its source explicit when missing. A pattern on the schema rejects a guessed value before your code runs, a parameter named run_id rather than job signals what kind of value belongs there, and a description that names the tool producing that identifier gives the model somewhere to go instead of guessing. When it still guesses, the error message is your last line of defense, so make it name the mistake rather than the symptom.

How do I know a description change actually helped?

Run the same cases before and after, several times each, and compare pass rates per case rather than overall accuracy, which hides compensating changes. Keep a held-out set you do not iterate against, because descriptions are easy to tune until they work on the twelve prompts you happen to have. Watch invalid-parameter errors and redundant calls as well as task success, since those move first when a description gets clearer.

Who should own tool definitions?

Whoever owns the agent’s behavior, because that is what they are. Treating them as platform-owned API surface revised quarterly is how surfaces end up endpoint-shaped. Descriptions and schemas are prompt engineering under version control, and they deserve the same review and evaluation discipline as the rest of the agent.

Further watching

Each of these was transcript-checked; timestamps link to the moment the claim appears.

- Why We Deleted Our MCP Server and Rebuilt It — Abhi Arya, Reducto (AI Engineer, 16:39). The best public field report on one-tool-per-endpoint failing in production: a tool for every API endpoint made a great demo, then nobody could explain what the agent had built (3:42). The rebuild deleted it in one commit and replaced it with fewer tools carrying product knowledge, plus a snapshot tool returning live state instead of letting the agent guess (6:12).
- Building Agents with Model Context Protocol — Mahesh Murag, Anthropic (AI Engineer, 1:44). Worth watching for the test of whether something should be a tool at all: tools suit the case where the right moment to act is uncertain, and a call that should happen deterministically every time belongs in application code instead (2:59).
- The Future of MCP — David Soria Parra, Anthropic (AI Engineer, 18:46). Two arguments that bear directly on tool design: mechanically converting a REST API into tools produces a poor agent interface, and a context window full of unused tool definitions is a harness decision rather than an inevitability — the fix is loading definitions only when the model needs them (7:12).

Primary Sources

- Anthropic, Writing effective tools for agents — tool choice, namespacing, response formats, token efficiency, and the evaluation-driven loop.
- Anthropic, Building effective agents — the agent-computer interface, and why the simplest design that works usually wins.
- OpenAI, Function calling — schema shape, strict mode, the best-practice list, tool count guidance, and deferred tool loading.
- Model Context Protocol, Tools specification — tool definitions, naming and disambiguation, the protocol-versus-execution error split, and tool security considerations.
- Model Context Protocol, Specification overview — architecture, extensions, and the trust and safety principles.
- JSON Schema, Understanding JSON Schema — the validation keywords that do the poka-yoke work.
- Stripe, Idempotent requests — the reference design for making repeated side-effecting calls safe.
- Hamel Husain, AI evals FAQ — why error analysis on real traces should decide which evaluators you write.
