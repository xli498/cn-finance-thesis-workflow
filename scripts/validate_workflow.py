#!/usr/bin/env python3
"""Validate structure and evidence gates without reading private research data."""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


EVIDENCE_COLUMNS = {
    "claim",
    "claim_strength",
    "evidence_type",
    "source_or_result_ref",
    "verification_status",
    "action_if_missing",
}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),
    re.compile(r"(?:sk|ghp|github_pat)-[A-Za-z0-9_-]{16,}"),
    re.compile(r"(?:api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{20,}", re.I),
)


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
            reader = csv.DictReader(f)
            headers = set(reader.fieldnames or [])
            missing_headers = EVIDENCE_COLUMNS - headers
            if missing_headers:
                errors.append(
                    "evidence map missing columns: " + ", ".join(sorted(missing_headers))
                )
            for i, row in enumerate(reader, 2):
                if not row.get("claim"):
                    errors.append(f"evidence map row {i}: missing claim")
                if row.get("verification_status") == "missing":
                    errors.append(f"evidence map row {i}: unresolved missing evidence")
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"symlink is not allowed: {path.relative_to(root)}")
        if path.is_file() and (
            path.name.startswith(".env")
            or path.suffix.lower() in {".key", ".pem"}
            or path.name.lower() in {"credentials", "credentials.json", "secrets.json"}
        ):
            errors.append(f"credential-like file: {path.relative_to(root)}")
        if path.is_file() and path.stat().st_size <= 2_000_000:
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    errors.append(f"credential-like content: {path.relative_to(root)}")
                    break
    if errors:
        print("FAIL")
        print("\n".join(f"- {e}" for e in errors))
        return 1
    print("PASS: structure, markdown fences, evidence map, and credential checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
