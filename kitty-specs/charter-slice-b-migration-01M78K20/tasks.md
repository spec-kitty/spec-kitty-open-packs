# Tasks: Charter slice B migration

**Mission**: `charter-slice-b-migration-01M78K20` · **Planning/merge branch**: `feat/slice1-readme-retire-org-charter` (PR → `main`)
**Inputs**: [spec.md](spec.md), [plan.md](plan.md), issues #241 and #242

## Subtask Index

| ID | Description | WP | Parallel |
| --- | --- | --- | --- |
| T001 | Run the service check at the new pin on the unchanged packs and record the refusals | WP01 | |
| T002 | `charter_service_check.py`: drop `README.md`, `PROVENANCE.md`, `org-charter.yaml` and the two charter-excluded entries from `NOT_REGISTERED`; tests | WP01 | |
| T003 | `validate_pack_schemas.py`: README companion pre-check, drop the `*/PROVENANCE.md` allowance; tests | WP01 | [P] |
| T004 | `check_vocabulary.py`: the qa provenance row reads `packs/qa/README.md`; tests | WP01 | [P] |
| T005 | `gen_pack_reference.py`: Purpose from the README preamble; tests | WP01 | [P] |
| T006 | Merge `pack.md` into the README of the nine carved packs (architecture, drupal, java, javascript, pack-authoring, planning-analysis, python, refactoring, testing) | WP02 | |
| T007 | built-in (rename), foundation and writing READMEs | WP02 | [P] |
| T008 | cave-kitty, event-driven, spdd, go and rust READMEs, including the go/rust org-charter sentence | WP02 | [P] |
| T009 | internal and qa READMEs, including their org-charter text | WP02 | [P] |
| T010 | Delete every `pack.md` and `PROVENANCE.md`; run the Markdown-model shape check over every README | WP02 | |
| T011 | `internal`: `presets/base.yaml` with the 18 must-have items and a new header; `pack.yaml` drops `active_charter`, comments rewritten | WP03 | |
| T012 | The 11 inert packs: delete `org-charter.yaml` and `active_charter`; rewrite the `pack.yaml` header comments | WP03 | [P] |
| T013 | go and rust preset descriptions | WP03 | [P] |
| T014 | Fixture `tests/fixtures/valid/example-pack/`: drop `org-charter.yaml` and `active_charter`, rewrite its header | WP03 | [P] |
| T015 | Live docs named by #241 and #242, root and `packs/` READMEs, `.kittify` comments and charter.md | WP04 | |
| T016 | Glossary "Charter Pack" sentence (operator wording) | WP04 | [P] |
| T017 | Regenerate `docs/packs/*.md`, restamp digests (and the `built-in.source.yaml` comment), CHANGELOG entry | WP04 | |
| T018 | Run every gate and the service check at the pin; record counts | WP04 | |

## WP01 – Tooling follows the slice B file rules

Subtasks T001-T005. Requirements FR-001, FR-008, FR-012. No dependencies.

## WP02 – One README per pack (#241)

Subtasks T006-T010. Requirements FR-002, FR-003, FR-004, FR-005. Depends on WP01 (the generator reads the README).

## WP03 – Org charters retired (#242)

Subtasks T011-T014. Requirements FR-006, FR-007. Depends on WP02 (shared pack trees, one digest restamp).

## WP04 – Docs, generated pages, digests and proof

Subtasks T015-T018. Requirements FR-009, FR-010, FR-011, FR-013. Depends on WP01, WP02 and WP03.
