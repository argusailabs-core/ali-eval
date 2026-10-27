# ALI-EVAL v0.2

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23701946.svg)](https://doi.org/10.5281/zenodo.23701946)

ALI-EVAL is a source-bounded evaluation instrument for testing whether a land-intelligence answer preserves supplied site, spatial, temporal, proposal, pathway, authority, evidence, uncertainty, and refusal information.

It evaluates **representation and evidence handling**. It does not establish legal correctness, professional-planning accuracy, development feasibility, entitlement, or the performance of any commercial product.

## What is included

- `tasks.json`: 16 synthetic tasks across eight strata.
- `source_records.json`: 42 synthetic source records used by the tasks.
- `output_schema.json`: the eight-field answer schema.
- `RUBRIC.md`: criterion definitions.
- `HUMAN_SCORING_GUIDE.md`: manual adjudication instructions.
- `scorecard_template.csv`: the frozen task-by-criterion scorecard.
- `aggregate_scores.py`: validates and aggregates a completed frozen-task scorecard.
- `LOCAL_CASE_PROTOCOL.md`: procedure for building a separately versioned local case set.
- Local-case templates and `aggregate_local_scores_v1.py`: validation and aggregation for local sets.
- `run_manifest_template.json`: workflow and output-seal record.
- `FILE_MANIFEST.json` and `SHA256SUMS.txt`: release inventory and integrity checks.

## Run the 16 synthetic tasks

1. Verify the package:

   ```bash
   sha256sum -c SHA256SUMS.txt
   ```

2. Copy `run_manifest_template.json` and record the workflow name, version, environment, and package checksum identifier.
3. For each task, give the workflow only `task_id` and the task's `input` object. Do not provide the task's criteria or a filled scorecard.
4. Save one answer per task using `output_schema.json`.
5. Hash and seal the outputs before scoring. Do not edit sealed outputs; corrections require a new run identifier.
6. Have a human reviewer compare each output only with the supplied task input and source bundle, following `HUMAN_SCORING_GUIDE.md`.
7. Complete every row in a copy of `scorecard_template.csv` with `1`, `0`, or `NA` as instructed.
8. Aggregate the scorecard:

   ```bash
   python3 aggregate_scores.py filled_scorecard.csv > results.json
   ```

The aggregation scripts validate and total human judgments. They do not grade answer prose and do not receive workflow labels.

## Build a local case set

Follow `LOCAL_CASE_PROTOCOL.md`. Freeze the local sources, redistribution rights, expected behavior, criteria, and refusal boundaries before running any workflow. Keep expected behavior hidden until outputs are sealed.

Aggregate a completed local scorecard with:

```bash
python3 aggregate_local_scores_v1.py local_case_manifest.json local_scorecard.csv > local_results.json
```

Report local results separately from the frozen 16-task results.

## Reproducibility boundary

This repository lets another team rerun the synthetic ALI-EVAL procedure, submit outputs, apply every criterion manually, and construct a separate local set.

It does not include any production system, proprietary implementation, real municipal geometry, real parcel inventory, private case, populated scoring key, historical condition implementation, or historical sealed output. It therefore does not independently reproduce any protected real-data measurement or historical workflow result reported in the companion research.

## Citation

Use the repository's `CITATION.cff`. Cite version 0.2.0 with DOI [10.5281/zenodo.23701946](https://doi.org/10.5281/zenodo.23701946). The all-versions concept DOI is [10.5281/zenodo.23701945](https://doi.org/10.5281/zenodo.23701945).

## Licences

ALI-EVAL uses two licences. See `LICENSE.md` for the controlling file-to-licence mapping.

- Synthetic tasks, source records, schema, rubric, guides, protocols, templates, manifests, and documentation: **CC BY 4.0**.
- `aggregate_scores.py` and `aggregate_local_scores_v1.py`: **MIT License**.

Suggested attribution:

> ALI-EVAL v0.2, © 2026 Argus AI Labs LLC, licensed under CC BY 4.0; aggregation scripts licensed under MIT.

## Maintainer

Argus AI Labs LLC

Research lead: Raj Brar
