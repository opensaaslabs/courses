# Conformance Program

The conformance program proves that an implementation correctly follows the OpenSaaSLabs Academy Specification.

## Components

- Fixtures: canonical test inputs.
- Golden outputs: canonical expected outputs.
- Runner: executes fixtures and compares behavior.
- Reports: machine-readable results.
- Certification: recognition that an implementation passes conformance for a specific spec version.

## Initial Implementation

The Python reference runner is the first implementation and is used to bootstrap the conformance suite. It does not own the specification.
