---
type: "source-note"
title: "Notes on: Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts"
raw: "bad-genius-counterfactual-guided-harness-evolution-beyond-task-specific-shortcuts"
url: "https://arxiv.org/abs/2609.18366"
created_at: "2026-11-23T01:01:34Z"
updated_at: "2026-11-23T01:01:34Z"
---
- Archived full text: [[bad-genius-counterfactual-guided-harness-evolution-beyond-task-specific-shortcuts|Full archived text, with credits]]
- Link: <https://arxiv.org/abs/2609.18366>

## What it says

The CHASE paper shows that an optimized agent harness can look better on held-out tasks while still relying on formatting conventions shared with the rest of the benchmark. It introduces Counterfactual Harness Search and Evolution: a Proposer edits the harness around a fixed foundation model, a Challenger searches for a protocol change that preserves the tasks but reduces the updated harness's gain over the initial harness, executable checks confirm the transformation preserves task semantics, and confirmed gain losses enter an archive that constrains later harness updates. The approach gives conditions under which a finite archive bounds gain loss on an ideal benchmark with shortcuts removed, and it is evaluated on Syn-Ledger, OfficeQA, FinanceBench, and SWE-Bench Pro V2.

## Claims drawn from this source

- **Harness improvements often rest on shared formatting conventions, not real capability.** An optimized agent harness can improve on held-out tasks by relying on formatting conventions that those tasks share with the rest of the benchmark.
- **CHASE treats harness evolution as constraint generation over valid protocol changes.** A Proposer edits the harness around a fixed foundation model; a Challenger then searches for a protocol change that preserves the tasks but reduces the updated harness's gain over the initial harness.
- **Executable checks keep counterfactual protocol changes semantically valid.** Executable checks test whether the transformation preserves task semantics before its gain loss is trusted.
- **Confirmed gain losses archive into constraints on later updates.** If the gain loss is confirmed on held-out tasks, CHASE adds the transformation to an archive that constrains subsequent harness updates.
- **A finite archive can bound gain loss in the shortcut-free ideal.** The paper gives conditions under which this finite archive bounds the gain loss on an ideal benchmark with shortcuts removed.
- **CHASE beats HarnessEvolve after shortcut removal.** On Syn-Ledger, removing the known shortcuts yields 38.30% accuracy for CHASE and 18.27% for HarnessEvolve.
- **CHASE survives formatting and field-order protocol changes.** On the 21 certification tasks from SWE-Bench Pro V2 HARD-51, changing the issue formatting and tool-output field order reduces HarnessEvolve's gain over the initial harness from 8.57 to 3.81 percentage points, while the final CHASE harness retains 10.48 points of its 11.43-point gain under the same change.
