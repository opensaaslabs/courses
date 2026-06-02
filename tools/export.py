#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "exports"


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_records(pattern: str) -> list[dict[str, Any]]:
    return [read_yaml(path) for path in sorted(ROOT.glob(pattern))]


def collect_catalog() -> dict[str, list[dict[str, Any]]]:
    return {
        "courses": load_records("courses/CRS-*/course.yaml"),
        "learningPaths": load_records("learning-paths/LP-*/path.yaml"),
        "badges": load_records("badges/BADGE-*/badge.yaml"),
        "certifications": load_records("certifications/CERT-*/certification.yaml"),
        "competencies": load_records("competencies/COMP-*/competency.yaml"),
        "evidence": load_records("evidence/EVD-*/evidence.yaml"),
    }


def collect_relations() -> list[dict[str, Any]]:
    relation_file = ROOT / "registry" / "relations" / "relations.yaml"
    if not relation_file.exists():
        return []
    return read_yaml(relation_file).get("relations", [])


def node_type_from_id(identifier: str) -> str:
    prefix = identifier.split("-", 1)[0]
    return {
        "CRS": "Course",
        "LP": "LearningPath",
        "BADGE": "Badge",
        "CERT": "Certification",
        "COMP": "Competency",
        "ASM": "Assessment",
        "LAB": "Lab",
        "EVD": "Evidence",
        "CRD": "Credential",
    }.get(prefix, "Concept")


def build_graph(catalog: dict[str, list[dict[str, Any]]], relations: list[dict[str, Any]]) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    for records in catalog.values():
        for record in records:
            identifier = record.get("id")
            if identifier:
                nodes[identifier] = {
                    "id": identifier,
                    "type": node_type_from_id(identifier),
                    "name": record.get("name") or record.get("claim") or identifier,
                    "status": record.get("status"),
                }

    for relation in relations:
        for identifier in [relation.get("source"), relation.get("target")]:
            if identifier and identifier not in nodes:
                nodes[identifier] = {
                    "id": identifier,
                    "type": node_type_from_id(identifier),
                    "name": identifier,
                    "status": "referenced",
                }

    edges = [
        {
            "id": relation.get("id"),
            "source": relation.get("source"),
            "target": relation.get("target"),
            "type": relation.get("type"),
            "status": relation.get("status"),
        }
        for relation in relations
    ]
    return {"nodes": list(nodes.values()), "edges": edges}


def build_search_index(catalog: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    index: list[dict[str, Any]] = []
    for collection_name, records in catalog.items():
        for record in records:
            identifier = record.get("id")
            if not identifier:
                continue
            index.append(
                {
                    "id": identifier,
                    "type": node_type_from_id(identifier),
                    "collection": collection_name,
                    "name": record.get("name") or identifier,
                    "description": record.get("description") or record.get("claim") or "",
                    "status": record.get("status"),
                    "tags": record.get("tags", []),
                }
            )
    return index


def build_jsonld_courses(courses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for course in courses:
        output.append(
            {
                "@context": "https://schema.org",
                "@type": "Course",
                "identifier": course.get("id"),
                "name": course.get("name"),
                "description": course.get("description"),
                "provider": {
                    "@type": "Organization",
                    "name": course.get("provider", "OpenSaaSLabs"),
                },
                "educationalLevel": course.get("level"),
                "timeRequired": f"PT{course.get('durationHours', 0)}H",
            }
        )
    return output


def main() -> None:
    catalog = collect_catalog()
    relations = collect_relations()
    graph = build_graph(catalog, relations)
    search_index = build_search_index(catalog)

    write_json(EXPORTS / "catalog" / "catalog.json", catalog)
    for key, value in catalog.items():
        write_json(EXPORTS / "catalog" / f"{key}.json", value)

    write_json(EXPORTS / "graph" / "nodes.json", graph["nodes"])
    write_json(EXPORTS / "graph" / "edges.json", graph["edges"])
    write_json(EXPORTS / "graph" / "graph.json", graph)

    write_json(EXPORTS / "search" / "search-index.json", search_index)
    write_json(EXPORTS / "jsonld" / "courses.jsonld", build_jsonld_courses(catalog["courses"]))

    print("Export complete")


if __name__ == "__main__":
    main()
