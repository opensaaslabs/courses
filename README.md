# OpenSaaSLabs Courses

OpenSaaSLabs Courses is the canonical, vendor-neutral learning repository for cloud-native, AI-native, SaaS, platform engineering, data, security, governance, and agentic engineering education.

This repository is designed as a governed learning platform, not a loose tutorial collection. Every course, module, lab, assessment, skill, badge, and certification is treated as a versioned artifact with ownership, schema, lifecycle state, evidence, and review controls.

## North Star

Enable institutions and individuals to learn, validate, and apply production-grade SaaS, AI, cloud, and agent engineering capabilities through open, structured, auditable, and continuously improving curriculum assets.

## Repository Structure

```text
courses/
├── courses/              # Canonical course definitions and content
├── learning-paths/       # Ordered multi-course pathways
├── modules/              # Reusable learning modules
├── lessons/              # Atomic lessons
├── labs/                 # Hands-on labs and exercises
├── projects/             # Real-world capstone and portfolio projects
├── assessments/          # Exams, rubrics, and validation tasks
├── skills/               # Skill taxonomy and mappings
├── certifications/       # Credential definitions
├── badges/               # Micro-credential definitions
├── taxonomy/             # Controlled vocabularies
├── schemas/              # JSON Schemas and JSON-LD contexts
├── governance/           # Policies, quality gates, lifecycle, review rules
├── templates/            # Authoring templates
├── tools/                # Validation and automation scripts
└── docs/                 # Platform documentation
```

## Artifact Model

Every learning asset should include:

- Stable ID
- Human-readable name
- Version
- Status
- Owner
- Reviewers
- License
- Source references
- Learning outcomes
- Prerequisites
- Skill mappings
- Governance metadata
- Quality and trust score fields
- Schema.org compatible JSON-LD metadata

## Initial Learning Paths

- Cloud Native SaaS Engineering
- Agentic Engineering
- Platform Engineering
- Data and AI Engineering
- Security and Governance
- Product and Enterprise Architecture

## Quality Gates

A course is publishable only when it has:

1. Valid metadata
2. Clear prerequisites
3. Measurable outcomes
4. At least one hands-on lab or project
5. Assessment or rubric
6. Skill mappings
7. Governance metadata
8. License and source attribution

## Current Status

Status: `bootstrap`

This repository contains the first production baseline for the OpenSaaSLabs learning graph. Course content will evolve through pull requests, review, and versioned releases.

## License

Content license and source policy are defined in `governance/licensing-policy.md`.
