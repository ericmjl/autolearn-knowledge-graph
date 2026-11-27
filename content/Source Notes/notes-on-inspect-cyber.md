---
type: "source-note"
title: "Notes on: Inspect Cyber"
raw: "inspect-cyber"
url: "https://inspect.cyber.aisi.org.uk/configuration-validation.html"
created_at: "2026-11-27T09:01:50Z"
updated_at: "2026-11-27T09:01:50Z"
---
- Archived full text: [[inspect-cyber|Full archived text, with credits]]
- Link: <https://inspect.cyber.aisi.org.uk/configuration-validation.html>

## What it says

Inspect Cyber docs on configuration validation: before running an evaluation, builders must verify the task is solvable, because failures caused by bad setup get misattributed to agent limitations and produce false negatives. The verify_solutions() solver makes this check cheap: it bypasses the model, executes a reference solution script directly in the sandbox, and pushes the result through the scoring pipeline, so any score below perfect flags a likely misconfiguration. The page shows a Kali Linux break as the cautionary case: evaluations that became unsolvable silently could have been caught by CI-time solution verification instead of only at full suite runs.

## Claims drawn from this source

- **Solvability verification is the most important check before running evaluations.** Without this baseline, failures that arise due to evaluation configuration issues may be incorrectly attributed to agent limitations, resulting in false negatives that undermine trust in results.
- **verify_solutions() bypasses the model and runs a solution script in the sandbox.** The solver bypasses the model entirely and instead executes a solution script directly in the sandbox, processing the result through the scoring pipeline.
- **The default script is ./solution.sh, with solution.bat for Windows sandboxes.** By default, it runs ./solution.sh in the sandbox's working directory (or solution.bat on Windows sandboxes).
- **A Kali Linux change broke many evaluations and CI-time verification would have caught the break early.** A change in Kali Linux previously made many evaluations using Kali impossible to solve. Developers verifying solutions as part of CI, however, would have spotted the break sooner, giving them more time to implement a fix.
- **A score below perfect indicates a potential misconfiguration.** Any score below perfect indicates a potential misconfiguration in the evaluation.
- **Windows sandboxes select solution.bat via os_type metadata.** For Windows sandboxes, set os_type: windows in the metadata and provide a solution.bat file instead of solution.sh; the solver runs solution.bat via cmd.exe for Windows or solution.sh via bash for Linux.
- **Solution scripts should avoid privileged knowledge of the evaluation.** To get the most out of your solution scripts, keep them realistic by avoiding using privileged knowledge of the evaluation in them.
- **The verify_solutions() solver ignores the prompt.** The solver ignores the prompt and simply executes the script; the prompt in a solution variant can sometimes be useful to have an agent run the solution script itself.
