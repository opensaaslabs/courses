# Versioning

The academy specification uses explicit versioning for schemas, contracts, and APIs.

## Versions

```text
academy/v1alpha1
academy/v1beta1
academy/v1
```

## Compatibility Rules

- Breaking changes require a new version.
- Stable versions must preserve backwards compatibility.
- Deprecated fields must include migration guidance.
- Generated exports must declare their source specification version.
