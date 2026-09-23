#!/usr/bin/env python3
"""Validate structure and evidence gates without reading private research data."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    root = parser.parse_args().project
    errors: list[str] = []
    if not root.is_dir():
        print(f"ERROR: project directory not found: {root}")
        return 2
    for required in ("docs", "data", "code"):
        if not (root / required).exists():
            errors.append(f"missing directory: {required}/")
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if text.count("```") % 2:
            errors.append(f"unbalanced code fence: {path.relative_to(root)}")
    evidence = root / "reports" / "evidence-map.csv"
    if evidence.exists():
        with evidence.open(newline="", encoding="utf-8") as f:
            for i, row in enumerate(csv.DictReader(f), 2):
                if not row.get("claim"):
                    errors.append(f"evidence map row {i}: missing claim")
                if row.get("verification_status") == "missing":
                    errors.append(f"evidence map row {i}: unresolved missing evidence")
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".env", ".key", ".pem"}:
            errors.append(f"credential-like file: {path.relative_to(root)}")
    if errors:
        print("FAIL")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print("PASS: structure, markdown fences, evidence map, and credential checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
