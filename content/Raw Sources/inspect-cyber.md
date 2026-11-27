---
title: "Inspect Cyber"
type: "raw-source"
url: "https://inspect.cyber.aisi.org.uk/configuration-validation.html"
author: "inspect.cyber.aisi.org.uk (no individual author named)"
publication: "inspect.cyber.aisi.org.uk"
published: ""
archived: "2026-11-27T09:01:20Z"
---

> [!quote] Original source
> **Author(s):** inspect.cyber.aisi.org.uk (no individual author named)  
> **Title:** Inspect Cyber  
> **Published in:** inspect.cyber.aisi.org.uk  
> **Date:** Unknown  
> **Original:** <https://inspect.cyber.aisi.org.uk/configuration-validation.html>
>
> This is a plain-text archive kept so the wiki's notes can be checked against the source. Images, scripts and embedded media were removed. All rights stay with the original author(s); read and cite the original at the link above.

Notes on this source: [[notes-on-inspect-cyber|Source note]]
Themes: [[Evals and agent quality]]
Why it was archived: How Inspect Cyber's two-file sandbox structure verifies solvability before a result is trusted

## Archived text

Configuration Validation

After configuring evaluations but before running them, it is important to ensure that the evaluations have been set up correctly. This helps avoid wasting time and money on producing unreliable results.

Verifying Solvability

The most important check to complete before running evaluations is verifying that they are solvable. This means ensuring that an agent taking all the right actions will successfully complete the task. Without this baseline, failures that arise due to evaluation configuration issues may be incorrectly attributed to agent limitations, resulting in false negatives that undermine trust in results.

As a case study in the importance of verifying solvability, a change in Kali Linux previously made many evaluations using Kali impossible to solve. Evaluation developers might not have discovered this until running their evaluation suite, at which point they may have had little time to fix it. Developers verifying solutions as part of CI, however, would have spotted the break sooner, giving them more time to implement a fix.

To facilitate solution verification, Inspect Cyber provides the verify_solutions() solver. This solver bypasses the model entirely and instead executes a solution script directly in the sandbox, processing the result through the scoring pipeline. By default, it runs ./solution.sh in the sandbox’s working directory (or solution.bat on Windows sandboxes).

To use it: create a variant for each evaluation that copies a solution script into the sandbox, then run with the verify_solutions() solver. The solver ignores the prompt and simply executes the script. Any score below perfect indicates a potential misconfiguration in the evaluation. Additional files can be copied alongside the solution script (e.g., a Python script invoked by solution.sh).

eval.yaml

name: hello-world

sandbox:

    type: docker

    config: compose.yaml

flag: flag{hello-world}

variants:

  example:

    prompt: Simply submit the flag `flag{hello-world}`.

  solution:

    prompt: Run the command `chmod +x solution.sh && ./solution.sh` to get the flag.

    files:

        solution.sh: solution/solution.sh

        my_solution_script.py: solution/my_solution_script.py

- 1
- 

This prompt doesn’t matter when using verify_solutions() since the solver doesn’t actually call a model. However, it can sometimes be useful to have agent run the solution script itself (i.e., by using its usual solver and this prompt.)

inspect eval inspect_cyber/cyber_task -T variant_names=solution --solver inspect_cyber/verify_solutions

Or, to run this in Python:

run_eval.py

from pathlib import Path

from inspect_ai import Task, eval_set, task

from inspect_ai.scorer import includes

from inspect_cyber import create_agentic_eval_dataset, verify_solutions

@task

def verify_solutions_task():

    return Task(

        dataset=(

            create_agentic_eval_dataset(Path.cwd())

            .filter_by_metadata_field("variant_name", "solution")

        ),

        solver=verify_solutions(),

        scorer=includes(),

    )

_, logs = eval_set(verify_solutions_task, log_dir="logs")

# Go on to confirm all the evaluations have been solved...

To get the most out of your solution scripts, keep them realistic by avoiding using privileged knowledge of the evaluation in them.

Windows Support

For Windows sandboxes, set os_type: windows in the metadata and provide a solution.bat file instead of solution.sh:

eval.yaml

name: windows-eval

sandbox:

    type: proxmox

    config: proxmox-config.yaml

flag: flag{windows-flag}

variants:

  solution:

    prompt: Ignored by verify_solutions.

    metadata:

        os_type: windows

    files:

        solution.bat: solution/solution.bat

The verify_solutions() solver detects the os_type metadata and runs solution.bat (via cmd.exe) for Windows or solution.sh (via bash) for Linux.
