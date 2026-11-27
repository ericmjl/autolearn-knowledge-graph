---
type: "evergreen"
title: "A passing sufficiency gate can be an edit detector"
created_at: "2026-11-27T05:05:37Z"
updated_at: "2026-11-27T05:05:37Z"
inputs: ["notes-on-chaincheck-near-perfect-evidence-sufficiency-scores-can-conceal-sensitivity-to", "passage-level-sufficiency-gates-under-detect-in-multi-hop-retrieval"]
provenance_urls: ["https://arxiv.org/html/2611.11965v1", "https://en.wikipedia.org/wiki/Rag", "https://research.google/blog/deeper-insights-into-retrieval-augmented-generation-the-role-of-sufficient-context/", "https://en.wikipedia.org/wiki/Retrieval-augmented_generation", "https://en.wikipedia.org/wiki/Large_language_model"]
refutation_status: "untested"
answers_questions: ["How do you implement a union-level sufficiency gate for multi-hop retrieval, and what does multi-hop gold labeling cost?"]
---
Agent synthesis

A passing sufficiency gate can be an edit detector. The union-level gate the passage-level note calls for certifies a full retrieved set against one question, but that certification is only as good as the validation behind it: a gate trained or judged on edited counterfactual negatives can be certifying the text-construction trace rather than the chain, and a nominal score near the ceiling cannot separate the two. The mechanism runs the way a passage-level gate fails, now at set scale. Every standard way of making a broken negative leaves a trace: deleting a supporting passage lowers the query relevance of the set, so a surface classifier recovers the label; substituting the bridge entity in the later hop keeps query overlap fixed, so a language model can notice that the text was edited without following the chain. The nominal pair AUC mixes the response to the broken chain with the response to the edit, so a gate that scores 0.997 on a set of negatives can be answering "was this text edited?", not "does this set support the answer?"

The evidence behind that claim is quantitative. In ChainCheck's crossed control on 2,214 HotpotQA pairs, an artifact-only per-passage language-model scorer that never reads the chain reaches a nominal AUC of 0.997, a one-string match that checks the bridge entity reaches the maximum of the crossed chain-sensitivity statistic CS4 (0.500), while the 11 evaluated systems score CS4 from 0.308 to 0.484. On MuSiQue, the trained readouts are edit-dominated: edit effects between +0.312 and +0.441, the single-layer probe with chain effect -0.025 that includes zero, and every trained system at negative selectivity, while the zero-shot judge is the only chain-selective system at +0.210 despite the lowest nominal score. The pass does not replicate: 5 of the 6 trained systems show large chain effects between +0.303 and +0.466 on 2WikiMultiHopQA, and on an independent HotpotQA set of 2,276 pairs, the only set with one pair per document group and informative clustered intervals, neither pre-specified pattern replicates, the judge's selectivity lower bound is -0.007, and the MuSiQue-trained readouts that were edit-dominated there show near-zero or positive selectivity. The same pipeline is brittle to scoring details: batch layout changed one judge's scores enough to fail a reproducibility gate (minimum Spearman 0.990383, one record moving 0.992, 17 of 2,214 A>D outcomes flipping).

This yields the joint rule the two notes need. The passage-level gate note gets the where right: truth lives in the union of passages, and a full-hop set must gate as one set, with a false-pass rate reported and retrieval of a full-hop set treated as a separate control from passage relevance. ChainCheck adds the how-not-to-trust it: a near-ceiling gate score means nothing until the score is audited against artifact-only baselines, the cells are certified in code, and the gate is confirmed on an independent document-disjoint set, with the dependence structure of the records (52 document groups and K_eff 18.22 on MuSiQue confirmation records, fewer than two effective groups per slice on 2Wiki) reported next to the verdict. The out-of-scope cost is real: the discipline ChainCheck applies consumed 4,925 train, 636 dev, 635 calibration and 463 test pairs, a closed-book filter that removes 3.5% of MuSiQue questions answered by the backbone without passages, and a document-disjoint split in which only 1,424 of 2,417 validation examples (58.9%) passed, before a single verdict was recorded. That is the price of gold labels whose labels follow mechanically from validated construction, not from a pass-rate average.

Do not trust a gate on the strength of its nominal accuracy alone. Build it at the union level, keep the edit-only cell and the artifact-only baseline beside the nominal score, report chain and edit contrasts and the false-pass rate, fix the batch layout, and confirm the gate on an independent document-disjoint set before it is allowed to block generation.

## Where it comes from

- [[notes-on-chaincheck-near-perfect-evidence-sufficiency-scores-can-conceal-sensitivity-to|ChainCheck: Near-Perfect Evidence-Sufficiency Scores Can Conceal Sensitivity to Construction Artifacts Paired Conditional Contrasts that Expose an Evaluation Confound]]

## What this builds on

- [[passage-level-sufficiency-gates-under-detect-in-multi-hop-retrieval|Passage-level sufficiency gates under-detect in multi-hop retrieval]]
