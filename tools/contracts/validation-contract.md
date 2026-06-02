# Validation Contract

The validation contract defines the behavior any implementation must satisfy.

## Inputs

- Source artifact directories
- JSON Schemas
- Governance policies

## Required Outputs

- Pass/fail result
- List of validation errors
- List of warnings where applicable

## Required Checks

- Course metadata validates against course schema
- Required fields exist
- Governance metadata exists
- Status values are valid
- IDs follow expected conventions

## Implementation Neutrality

This contract may be implemented in Python, Go, Rust, JavaScript, Java, or any other language.
