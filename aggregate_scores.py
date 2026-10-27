#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Argus AI Labs LLC
"""Validate and aggregate a human-adjudicated ALI scorecard; no automatic prose grading."""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODES = ["D1","D2","D3","D4","D5","D6","D7","S1","S2","U1","U2"]

def family(code):
    return "dimension_coverage" if code.startswith("D") else ("evidence_support" if code.startswith("S") else "uncertainty_discipline")

def main(scorecard):
    package = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))
    tasks = {item["task_id"]: item for item in package["tasks"]}
    expected = {(name, code) for name in tasks for code in CODES}
    seen = {}
    with Path(scorecard).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["task_id","criterion","score","reviewer_note"]:
            raise ValueError("Expected task_id,criterion,score,reviewer_note columns")
        for line, row in enumerate(reader, start=2):
            key = (row["task_id"], row["criterion"])
            if key not in expected or key in seen:
                raise ValueError(f"Unknown or duplicate task/criterion on line {line}: {key}")
            applicable = row["criterion"] in tasks[row["task_id"]]["criteria"]
            value = row["score"].strip().upper()
            if value not in (("0","1") if applicable else ("NA",)):
                raise ValueError(f"Line {line}: score must be 0/1 for applicable or NA for inapplicable: {key}")
            seen[key] = (value, row["reviewer_note"])
    if set(seen) != expected:
        raise ValueError(f"Scorecard incomplete: {len(expected - set(seen))} missing rows")
    totals = defaultdict(lambda: [0, 0])
    by_stratum = defaultdict(lambda: [0, 0])
    failures = []
    for task_id, criterion in sorted(expected):
        value, note = seen[(task_id, criterion)]
        if value == "NA":
            continue
        score = int(value)
        for label in ("overall", family(criterion)):
            totals[label][0] += score
            totals[label][1] += 1
        s = tasks[task_id]["stratum"]
        by_stratum[s][0] += score
        by_stratum[s][1] += 1
        if score == 0:
            failures.append({"task_id": task_id, "criterion": criterion, "reviewer_note": note})
    report = {
        "instrument": package["instrument"], "version": package["version"],
        "scope": "16 synthetic tasks; representation and evidence handling only",
        "human_adjudicated": True,
        "totals": {k: {"earned": v[0], "applicable": v[1]} for k,v in sorted(totals.items())},
        "by_stratum": {k: {"earned": v[0], "applicable": v[1]} for k,v in sorted(by_stratum.items())},
        "failures": failures,
    }
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 aggregate_scores.py filled_scorecard.csv")
    try:
        main(sys.argv[1])
    except (ValueError, OSError) as exc:
        raise SystemExit(str(exc))
