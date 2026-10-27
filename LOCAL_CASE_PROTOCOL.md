# Protocol for a separate local case set

**Classification: PUBLIC-CANDIDATE; review only. Version 0.2.**

1. Assign a unique `case_set_id` and version. Do not reuse a frozen synthetic task ID.
2. Before any run, freeze each question, input packet, allowed sources, rights status, source hashes, applicable criteria, stratum, expected evidence behavior, and refusal boundary.
3. Put source material—not answer-like paraphrases—into the runner packet where rights permit. Keep expected behavior and scoring notes private until outputs are sealed.
4. Give every workflow identical input bytes and the same output schema. Do not disable a competent comparator.
5. Seal raw outputs before adjudication. Preserve versions, procedures, failures, retries, and hashes.
6. Adjudicate with `HUMAN_SCORING_GUIDE.md`, citing answer spans and allowed sources.
7. Create `local_case_manifest.json` with `instrument`, `version`, `case_set_id`, and `cases`. Each case has a unique `case_id`, `stratum`, and non-empty `criteria` array using D1–D7, S1–S2, or U1–U2.
8. Create all 11 criterion rows for every case. Use NA only for criteria absent from that case's list.
9. Run `python3 aggregate_local_scores_v1.py local_case_manifest.json local_scorecard.csv`. Report the local result separately; never merge it with frozen 16-task totals.

Record rights per source. If redistribution is uncertain, keep bytes and geometry private and distribute only permitted citations or synthetic substitutes. A local set does not test legal correctness without a separately governed qualified reference-answer process.

Create the private expected-behavior record from `local_private_expected_behavior_template.json`. Keep it outside any runner bundle. It must identify the allowed source facts, expected evidence state, required qualification or refusal, and criterion-specific notes for every local case. It is an adjudication aid, not a reference answer, and must remain hidden until output sealing.

A local case may reuse a source ID only when the source bytes, SHA-256, rights statement, and evidentiary meaning are identical. Otherwise assign a new source ID and preserve both records. Cross-case reuse must be explicit in the local manifest.
