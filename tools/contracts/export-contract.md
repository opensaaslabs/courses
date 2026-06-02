# Export Contract

The export contract defines how source artifacts become machine-readable outputs.

## Inputs

- Courses
- Learning paths
- Badges
- Certifications
- Competencies
- Evidence
- Relations

## Required Outputs

```text
exports/catalog/catalog.json
exports/graph/graph.json
exports/search/search-index.json
exports/jsonld/courses.jsonld
```

## Rules

- Source YAML remains canonical.
- Exported JSON is generated and replaceable.
- Implementations must preserve stable artifact IDs.
- Relations must be represented as graph edges.
