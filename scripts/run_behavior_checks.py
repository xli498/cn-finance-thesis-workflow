#!/usr/bin/env python3
"""Offline contract checks for the Darwin evaluation assets.

This runner checks the reproducibility contract, fixture integrity, prompt
coverage, and structured blocking fields. It does not invoke an LLM and does
not claim that a real thesis feasibility study was executed.
"""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    prompts = json.loads((ROOT / ".darwin/test-prompts.json").read_text())
    fixture = json.loads((ROOT / ".darwin/fixture-esg.json").read_text())
    evaluation = (ROOT / ".darwin/EVALUATION.md").read_text()
    skill = (ROOT / "SKILL.md").read_text()

    expected_ids = {
        "s0-empty", "s0-feasibility", "s1-unverified", "s2-paid",
        "s2-excel", "s2-file-ready", "s2-min-gap", "s3-empty",
        "s4-missing", "s5-realistic",
    }
    ids = {item.get("id") for item in prompts}
    if ids != expected_ids or len(prompts) != 10:
        fail(f"expected 10 unique prompts, got {len(prompts)}")
    if not all(item.get("prompt") and item.get("expected") for item in prompts):
        fail("every prompt must have prompt and expected fields")

    if fixture.get("is_test_fixture") is not True:
        fail("fixture must be explicitly marked is_test_fixture=true")
    if len(fixture.get("columns", [])) != 6 or len(fixture.get("rows", [])) != 5:
        fail("fixture shape must remain 5 rows x 6 columns")
    rows = fixture["rows"]
    keys = [(row[0], row[1]) for row in rows]
    if keys.count(("000002", 2018)) != 2:
        fail("fixture duplicate key contract changed")
    if sum(row[2] is None for row in rows) != 1 or sum(row[5] is None for row in rows) != 1:
        fail("fixture missing-value contract changed")
    if {row[1] for row in rows} != {2018, 2019, 2023}:
        fail("fixture year coverage contract changed")

    required_phrases = [
        "executed", "planned", "blocked", "pass", "needs_evidence",
        "S0", "S1", "误阻塞", "is_test_fixture", "20260924",
    ]
    for phrase in required_phrases:
        if phrase not in evaluation and phrase not in skill:
            fail(f"missing evaluation contract phrase: {phrase}")

    with (ROOT / "templates/evidence_map.csv").open(newline="") as handle:
        fields = next(csv.reader(handle))
    for field in ("blocking", "gate_scope", "evidence_required"):
        if field not in fields:
            fail(f"evidence map missing structured field: {field}")

    print("PASS: 10 prompts, fixture integrity, evaluation contract, and structured blocking fields")


if __name__ == "__main__":
    main()
