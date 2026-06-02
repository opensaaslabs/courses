# ADR-0002: Programming-Language Neutral Core

## Status

Accepted

## Context

The academy repository needs validation, export, quality, and publishing tools. Early implementations used Python scripts directly under `tools/`, but that could incorrectly imply Python is the canonical runtime.

## Decision

OpenSaaSLabs Courses defines a programming-language-neutral, schema-first academy model.

The canonical layer consists of:

- Schemas
- Governance policies
- Registry records
- Relations
- Source artifacts
- Export contracts
- Validation contracts
- Quality contracts
- Publishing contracts

Tooling in Python, Go, Rust, JavaScript, Java, or any other language is replaceable as long as it conforms to the same contracts.

## Consequences

- Python scripts are treated as reference implementations only.
- Workflows may use Python initially, but must describe it as the reference implementation.
- Future Go, Rust, or JavaScript implementations can replace or complement Python without changing the academy model.
- The repository remains portable across runtimes, platforms, and deployment targets.
