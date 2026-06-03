#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
import jsonschema

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent
SCHEMA = json.loads((REPO / "schemas" / "course.schema.json").read_text(encoding="utf-8"))


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def run() -> dict[str, Any]:
    results = []

    valid_course = REPO / "conformance" / "fixtures" / "valid" / "course-minimal" / "course.yaml"
    try:
        jsonschema.validate(read_yaml(valid_course), SCHEMA)
        results.append({"fixture": "valid/course-minimal", "status": "PASS"})
    except Exception as exc:
        results.append({"fixture": "valid/course-minimal", "status": "FAIL", "error": str(exc)})

    invalid_course = REPO / "conformance" / "fixtures" / "invalid" / "course-missing-id" / "course.yaml"
    try:
        jsonschema.validate(read_yaml(invalid_course), SCHEMA)
        results.append({"fixture": "invalid/course-missing-id", "status": "FAIL", "error": "Invalid fixture was accepted"})
    except Exception:
        results.append({"fixture": "invalid/course-missing-id", "status": "PASS"})

    expected = json.loads((REPO / "conformance" / "fixtures" / "graph" / "simple-learning-path" / "expected.json").read_text(encoding="utf-8"))
    relations = read_yaml(REPO / "conformance" / "fixtures" / "graph" / "simple-learning-path" / "relations.yaml").get("relations", [])
    observed_edges = {f"{r['source']}->{r['target']}:{r['type']}" for r in relations}
    required_edges = set(expected.get("requiredEdges", []))
    missing = sorted(required_edges - observed_edges)
    if missing:
        results.append({"fixture": "graph/simple-learning-path", "status": "FAIL", "missingEdges": missing})
    else:
        results.append({"fixture": "graph/simple-learning-path", "status": "PASS"})

    passed = sum(1 for result in results if result["status"] == "PASS")
    failed = len(results) - passed
    return {
        "implementation": "python-reference",
        "specVersion": "v0.1.0-alpha",
        "fixtures": len(results),
        "passed": passed,
        "failed": failed,
        "status": "PASS" if failed == 0 else "FAIL",
        "results": results,
    }


def main() -> None:
    report = run()
    output = REPO / "conformance" / "reports" / "python-reference.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
