# Human adjudication guide

**Classification: PUBLIC-CANDIDATE; review only. Version 0.2.**

Score observable meaning, not preferred wording or field names. For each applicable criterion, read the complete answer, identify the relevant assertion or omission, and compare it only with allowed task sources. A citation earns no credit unless it supports the assertion. One material failure makes the task-level criterion zero.

| Code | Human decision procedure |
|---|---|
| D1 | List every required site member and membership relation. Score zero for an omission, addition, or conflation. |
| D2 | List required partitions, measures, labels, and geometric status. Recompute simple totals if supplied. Score zero if a required partition is collapsed, absent, or materially misstated. |
| D3 | Separate as-of, source/observation, adoption, and effective dates. Score one only if every required date is correct and its role is not conflated. |
| D4 | List supplied proposal assumptions and explicitly absent proposal facts. Score zero for omission, invention, or presentation as established fact. |
| D5 | Identify the supplied pathway/posture or precise missing pathway evidence. Score zero for invention, omission, entitlement conflation, or a generic unresolved label that does not name the missing issue. |
| D6 | List authorities and source IDs required for material assertions. Score zero if any required authority is absent or misidentified. |
| D7 | Compare each source's evidence state with the answer. Score zero for unsupported promotion, including treating mapped overlap as legal entitlement. |
| S1 | Trace every material conclusion to an allowed source fact. Score zero if any material assertion depends on an unstated or external fact. |
| S2 | Check required version and date attribution attached to citations. Score zero for a missing or wrong required attribution. |
| U1 | List packet-declared unknowns and uncertainties. Score one only if all material ones are explicit and none are overstated or hidden. |
| U2 | Decide from the packet whether it supports an answer, qualification, or refusal. Score zero for a missing required refusal or unwarranted refusal when supplied facts suffice. |

For each zero, point to the shortest relevant answer span and name the conflicting or missing source fact. For disputed ones, record both interpretations and the resolution. Do not change a task, criterion, or expected behavior after seeing results; issue a new version.

## Required-fact checklist

For each applicable criterion, derive a written checklist from the task's supplied facts and source records before inspecting the answer. Record each required fact, its source ID, the answer span that satisfies or conflicts with it, and the final binary judgment. The criterion descriptions above control; field presence alone never earns a point.

For D4 and D5, an empty or omitted answer field is correct only when the supplied packet affirmatively establishes that nothing must be reported. If the packet supplies an assumption, pathway, posture, or a precise absence of evidence, the answer must state it. Merely leaving the field empty does not preserve that fact.

The frozen aggregator accepts only 0 or 1 for applicable rows and `NA` for inapplicable rows. It intentionally rejects partial or `UNTESTED` scorecards. To smoke-test mechanics, use a clearly named throwaway copy with every row syntactically complete; its total is not an evaluation finding.

Report task rows, failures, abstentions, and family totals. Do not call the percentage legal accuracy, professional-planning accuracy, product performance, or jurisdiction-wide performance.
