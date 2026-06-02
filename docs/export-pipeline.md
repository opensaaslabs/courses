# Export Pipeline

The export pipeline converts source YAML artifacts into machine-readable academy outputs.

## Flow

```text
YAML source artifacts
  -> tools/export.py
  -> exports/catalog
  -> exports/graph
  -> exports/jsonld
  -> exports/search
```

## Outputs

- Catalog JSON for websites and APIs.
- Graph JSON for visualization and reasoning.
- JSON-LD for semantic discovery.
- Search index for static or hosted search.

## Principle

Humans author structured YAML. Systems consume generated exports.
