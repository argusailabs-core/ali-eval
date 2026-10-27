#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Argus AI Labs LLC
"""Validate and aggregate a separately versioned, human-scored local case set."""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

CODES = ("D1", "D2", "D3", "D4", "D5", "D6", "D7", "S1", "S2", "U1", "U2")
FIELDS = ["case_id", "criterion", "score", "reviewer_note"]


def family(code):
    return "dimension_coverage" if code.startswith("D") else ("evidence_support" if code.startswith("S") else "uncertainty_discipline")


def load_manifest(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    required = ("instrument", "version", "case_set_id", "cases")
    if any(key not in data for key in required) or not isinstance(data["cases"], list) or not data["cases"]:
        raise ValueError("Manifest requires instrument, version, case_set_id, and a non-empty cases array")
    cases = {}
    for index, item in enumerate(data["cases"]):
        if not isinstance(item, dict) or not all(key in item for key in ("case_id", "stratum", "criteria")):
            raise ValueError(f"Manifest case {index} requires case_id, stratum, and criteria")
        case_id = item["case_id"]
        criteria = item["criteria"]
        if not isinstance(case_id, str) or not case_id or case_id in cases:
            raise ValueError(f"Manifest case {index} has an empty or duplicate case_id")
        if not isinstance(item["stratum"], str) or not item["stratum"]:
            raise ValueError(f"Manifest case {case_id} requires a non-empty stratum")
        if not isinstance(criteria, list) or not criteria or len(criteria) != len(set(criteria)) or any(code not in CODES for code in criteria):
            raise ValueError(f"Manifest case {case_id} has invalid criteria")
        cases[case_id] = item
    return data, cases


def aggregate(manifest_path, scorecard_path):
    manifest, cases = load_manifest(manifest_path)
    expected = {(case_id, code) for case_id in cases for code in CODES}
    seen = {}
    with Path(scorecard_path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise ValueError("Expected case_id,criterion,score,reviewer_note columns")
        for line, row in enumerate(reader, start=2):
            key = (row["case_id"], row["criterion"])
            if key not in expected:
                raise ValueError(f"Unknown case/criterion on line {line}: {key}")
            if key in seen:
                raise ValueError(f"Duplicate case/criterion on line {line}: {key}")
            applicable = row["criterion"] in cases[row["case_id"]]["criteria"]
            value = row["score"].strip().upper()
            allowed = ("0", "1") if applicable else ("NA",)
            if value not in allowed:
                raise ValueError(f"Line {line}: score must be 0/1 for applicable or NA for inapplicable: {key}")
            seen[key] = (value, row["reviewer_note"])
    missing = expected - set(seen)
    if missing:
        raise ValueError(f"Scorecard incomplete: {len(missing)} missing rows")

    totals = defaultdict(lambda: [0, 0])
    by_stratum = defaultdict(lambda: [0, 0])
    failures = []
    for case_id, criterion in sorted(expected):
        value, note = seen[(case_id, criterion)]
        if value == "NA":
            continue
        score = int(value)
        for label in ("overall", family(criterion)):
            totals[label][0] += score
            totals[label][1] += 1
        stratum = cases[case_id]["stratum"]
        by_stratum[stratum][0] += score
        by_stratum[stratum][1] += 1
        if score == 0:
            failures.append({"case_id": case_id, "criterion": criterion, "reviewer_note": note})
    return {
        "instrument": manifest["instrument"],
        "version": manifest["version"],
        "case_set_id": manifest["case_set_id"],
        "scope": "separate local case set; representation and evidence handling only",
        "human_adjudicated": True,
        "case_count": len(cases),
        "totals": {key: {"earned": value[0], "applicable": value[1]} for key, value in sorted(totals.items())},
        "by_stratum": {key: {"earned": value[0], "applicable": value[1]} for key, value in sorted(by_stratum.items())},
        "failures": failures,
    }


def main(argv):
    if len(argv) != 3:
        raise SystemExit("Usage: python3 aggregate_local_scores_v1.py local_case_manifest.json local_scorecard.csv")
    try:
        print(json.dumps(aggregate(argv[1], argv[2]), indent=2))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main(sys.argv)
