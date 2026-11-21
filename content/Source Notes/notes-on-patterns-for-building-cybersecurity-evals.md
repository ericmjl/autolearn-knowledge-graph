---
type: "source-note"
title: "Notes on: Patterns for Building Cybersecurity Evals"
raw: "patterns-for-building-cybersecurity-evals"
url: "https://eugeneyan.com/writing/cybersecurity-evals"
created_at: "2026-11-21T06:02:29Z"
updated_at: "2026-11-21T06:02:29Z"
---

# Notes on: Patterns for Building Cybersecurity Evals

- Archived full text: [[patterns-for-building-cybersecurity-evals|Full archived text, with credits]]
- Link: <https://eugeneyan.com/writing/cybersecurity-evals>

## What it says

Eugene Yan surveys how cybersecurity-capable agents get evaluated: seven benchmarks built on four primitives, each measuring whether a model can find and exploit vulnerabilities or reach an attacker goal. Benchmarks use Docker sandboxed targets, difficulty-shaping inputs (zero-day to one-day), agent tools, and deterministic graders that score outcomes rather than methods, sometimes with transcript audits to catch reward hacking and partial credit along the attack chain. Across benchmarks, harness choice and memory structure matter more than the underlying model, and current agents hit a ceiling well below human attackers even on one-day tasks.

## Claims drawn from this source

- **Cybersecurity evals share four primitives.** A sandboxed target (Docker containers), inputs that shape difficulty (zero-day code-only up to one-day with description or patch), tools (bash, read/write, websearch, debuggers, static analyzers), and a grader that returns immediate, typically deterministic feedback.
- **Outcome-based grading needs transcript audits.** Exploitation is open-ended, so benchmarks score outcomes (sanitizer crash, hidden flag, flag retrieval) rather than method, and run automated transcript audits to confirm the agent actually exploited the vulnerability instead of reward hacking. ExploitGym's GPT-5.5 and Opus 4.6 auditors reached 94% agreement across 313 production tasks.
- **Outcome-only grading is too coarse.** A model scoring zero on unauthorized code execution may still have found and reproduced the vulnerability, so partial credit tracks progress along the attack chain: find the vulnerability, reproduce it with a PoC, exploit it, and achieve the attacker's goal (exfiltrate data, escalate privileges).
- **Cybench shows a hard ceiling and mixed tool effects.** Cybench tests 40 professional CTF tasks with First Solve Time from 2 minutes to 25 hours. In unguided mode Claude 3.5 Sonnet scored 17.5% and GPT-4o 12.5%, with o1-preview completing 46.8% of milestones in subtask mode; no agent solved tasks with FST above 11 minutes, and better tools helped Claude Sonnet 3.5 (17.5% to 20%) but hurt GPT-4o (to 10%-15%).
- **Insufficient exploration drives most zero-day failures.** CVE-Bench found insufficient exploration in 67.5%-80% of zero-day failures and 37.5%-55% of one-day failures; other modes include limited task understanding, incorrect focus, tool misuse, and weak reasoning. T-Agent (13%) beat the Cybench agent (2.5%) on 40 critical NVD CVEs, with up to 10% exploited zero-day and 12.5% one-day.
- **Long PoCs collapse agent success rates.** CyberGym (1,507 instances across 188 OSS projects) found Sonnet 4 at 17.9% success (up to 19.3% with thinking; GPT-5 jumped from 7.7% to 22.0%), but success fell to 10% for inputs longer than 100 bytes even though those cover 65.7% of the benchmark.
- **Defenses collapse exploit counts.** ExploitGym (898 instances) shows Claude Mythos exploiting 157 instances and GPT-5.5 at 120, but with defenses on Claude Mythos' count falls to 45, defeating ASLR, V8 sandbox, and Kernel ASLR via partial-pointer overwrites and writable static strings.
- **Harness structure beats model size in multi-host red teaming.** Multi-Host Bench (40 emulated networks of 22-50 hosts, modeled onEquifax and Colonial Pipeline) found existing frameworks wasting 47%-90% of commands and failing 6%-41% of relevant actions. Incalmo, which decouples planning (scan, lateral move, escalate, find, exfiltrate) from execution with auxiliary state and attack-graph services, jumped success from 3/40 to 37/40 networks with all 10 models scoring 6-9 of 10 representative environments.
