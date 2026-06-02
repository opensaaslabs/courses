# Quality Engine

The quality engine validates graph integrity and computes academy quality analytics.

## Checks

- Broken relation sources and targets
- Duplicate relation IDs
- Course outcome coverage
- Course module coverage
- Lab and assessment coverage
- Badge criteria completeness
- Certification requirement completeness
- Orphan detection

## Outputs

- `exports/analytics/graph-validation.json`
- `exports/analytics/quality.json`

## Principle

A learning artifact is not publishable merely because it exists. It must be complete, connected, governed, and reviewable.
