#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]


def read_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_records(pattern: str) -> list[dict[str, Any]]:
    return [read_yaml(path) for path in sorted(ROOT.glob(pattern))]


def load_ids() -> set[str]:
    ids: set[str] = set()
    patterns = [
        "courses/CRS-*/course.yaml",
        "learning-paths/LP-*/path.yaml",
        "badges/BADGE-*/badge.yaml",
        "certifications/CERT-*/certification.yaml",
        "competencies/COMP-*/competency.yaml",
        "evidence/EVD-*/evidence.yaml",
    ]
    for pattern in patterns:
        for record in load_records(pattern):
            if record.get("id"):
                ids.add(record["id"])

    skills_file = ROOT / "skills" / "skills.yaml"
    if skills_file.exists():
        for skill in read_yaml(skills_file).get("skills", []):
            if skill.get("id"):
                ids.add(skill["id"])

    for pattern in ["labs/LAB-*/lab.md", "assessments/ASM-*/assessment.md", "modules/MOD-*/module.md"]:
        for path in ROOT.glob(pattern):
            ids.add(path.parent.name.split("-", 1)[0] + "-" + path.parent.name.split("-", 2)[1])

    return ids


def load_relations() -> list[dict[str, Any]]:
    path = ROOT / "registry" / "relations" / "relations.yaml"
    if not path.exists():
        return []
    return read_yaml(path).get("relations", [])


def validate() -> tuple[list[str], dict[str, Any]]:
    ids = load_ids()
    relations = load_relations()
    errors: list[str] = []
    warnings: list[str] = []

    seen_relation_ids: set[str] = set()
    incoming = defaultdict(int)
    outgoing = defaultdict(int)

    for relation in relations:
        rid = relation.get("id")
        source = relation.get("source")
        target = relation.get("target")
        if rid in seen_relation_ids:
            errors.append(f"Duplicate relation id: {rid}")
        seen_relation_ids.add(rid)
        if source not in ids:
            errors.append(f"Broken relation source {source} in {rid}")
        if target not in ids:
            errors.append(f"Broken relation target {target} in {rid}")
        outgoing[source] += 1
        incoming[target] += 1

    for course in load_records("courses/CRS-*/course.yaml"):
        cid = course.get("id")
        if not course.get("outcomes"):
            errors.append(f"Course {cid} has no outcomes")
        if not course.get("modules"):
            errors.append(f"Course {cid} has no modules")
        if not course.get("labs"):
            warnings.append(f"Course {cid} has no labs")
        if not course.get("assessments"):
            warnings.append(f"Course {cid} has no assessments")

    for badge in load_records("badges/BADGE-*/badge.yaml"):
        bid = badge.get("id")
        criteria = badge.get("criteria", {})
        for key in ["courses", "skills", "assessments"]:
            if not criteria.get(key):
                errors.append(f"Badge {bid} missing criteria.{key}")

    for cert in load_records("certifications/CERT-*/certification.yaml"):
        cid = cert.get("id")
        for key in ["requiredCourses", "requiredSkills", "requiredAssessments"]:
            if not cert.get(key):
                errors.append(f"Certification {cid} missing {key}")

    orphans = sorted(identifier for identifier in ids if incoming[identifier] == 0 and outgoing[identifier] == 0)
    analytics = {
        "ids": len(ids),
        "relations": len(relations),
        "errors": errors,
        "warnings": warnings,
        "orphans": orphans,
        "brokenReferences": len([e for e in errors if e.startswith("Broken relation")]),
    }
    return errors, analytics


def main() -> None:
    errors, analytics = validate()
    output = ROOT / "exports" / "analytics" / "graph-validation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(analytics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if errors:
        print("Graph validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Graph validation passed")


if __name__ == "__main__":
    main()
