# Conformance Runner

The conformance runner executes canonical fixtures against an implementation and produces a machine-readable report.

## Responsibilities

1. Load fixture inputs.
2. Run an implementation under test.
3. Compare generated outputs against expected behavior or golden outputs.
4. Produce pass/fail results.
5. Emit a conformance report.

## Required Report Fields

```json
{
  "implementation": "python-reference",
  "specVersion": "v0.1.0-alpha",
  "fixtures": 0,
  "passed": 0,
  "failed": 0,
  "status": "PASS"
}
```

## Principle

Conformance tests define expected behavior. Implementations are replaceable.
