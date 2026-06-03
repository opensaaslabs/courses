# Runner Contract

A conforming runner must:

- Accept an implementation identifier.
- Execute all required fixture groups.
- Treat valid fixtures as pass-only when accepted.
- Treat invalid fixtures as pass-only when rejected.
- Compare generated graph outputs with expected graph semantics.
- Generate a JSON report.
- Return a non-zero exit code when required conformance checks fail.
