# Tasks: Java conventions rules and one language vocabulary

**Mission**: `java-rules-and-language-vocabulary-01M77YQA` · **Planning/merge branch**: `feat/java-rules-and-language-vocabulary` (PR → `main`)
**Inputs**: [spec.md](spec.md), [plan.md](plan.md)

## Subtask Index

| ID | Description | WP | Parallel |
| --- | --- | --- | --- |
| T001 | Retag the two Java toolguides (`java, kotlin` / `java`) | WP01 | |
| T002 | Refuse runtime-family language names in `check_vocabulary.py`, with tests | WP01 | |
| T003 | Document the language vocabulary rule in the authoring guide | WP01 | [P] |
| T004 | Add the three rules to `java-conventions` | WP02 | |
| T005 | Bump `java` to 2.1.0, restamp the digest, regenerate `docs/packs/java.md` | WP02 | |
| T006 | CHANGELOG "Changed" (#204) and "Fixed" (#202) entries | WP02 | |

## WP01 – Language vocabulary (#202)

Subtasks T001-T003. Requirements FR-001, FR-002, FR-003. No dependencies.

## WP02 – java-conventions rules and release (#204)

Subtasks T004-T006. Requirements FR-004, FR-005, FR-006. Depends on WP01 (shared version bump and digest).
