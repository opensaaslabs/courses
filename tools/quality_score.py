#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def score_course(course: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "metadata": bool(course.get("id") and course.get("name") and course.get("version")),
        "governance": bool(course.get("governance", {}).get("owner") and course.get("governance", {}).get("license")),
        "outcomes": bool(course.get("outcomes")),
        "modules": bool(course.get("modules")),
        "labs": bool(course.get("labs")),
        "assessments": bool(course.get("assessments")),
        "skills": bool(course.get("skills")),
        "jsonld": bool(course.get("jsonld")),
    }
    score = round(sum(1 for value in checks.values() if value) / len(checks) * 100)
    return {"id": course.get("id"), "name": course.get("name"), "qualityScore": score, "checks": checks}


def main() -> None:
    results = []
    for path in sorted((ROOT / "courses").glob("CRS-*/course.yaml")):
        results.append(score_course(read_yaml(path)))
    academy_score = round(sum(item["qualityScore"] for item in results) / len(results)) if results else 0
    payload = {"academyQualityScore": academy_score, "courses": results}
    output = ROOT / "exports" / "analytics" / "quality.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Academy quality score: {academy_score}")


if __name__ == "__main__":
    main()
