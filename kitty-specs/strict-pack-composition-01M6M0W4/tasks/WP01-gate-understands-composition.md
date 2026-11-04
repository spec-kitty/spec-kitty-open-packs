---
work_package_id: WP01
title: Gate understands composition
dependencies: []
requirement_refs:
- FR-001
- FR-002
- FR-003
- FR-012
- NFR-001
- NFR-002
- C-003
- C-004
planning_base_branch: feat/strict-pack-composition
merge_target_branch: feat/strict-pack-composition
branch_strategy: Planning artifacts for this mission were generated on feat/strict-pack-composition. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/strict-pack-composition unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
history:
- at: '2026-11-04T20:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: python-pedro
authoritative_surface: scripts/ci/
create_intent: []
execution_mode: code_change
owned_files:
- scripts/ci/validate_pack_schemas.py
- scripts/ci/validate-packs.sh
- scripts/docs/gen_pack_reference.py
- tests/ci/test_validate_pack_schemas.py
- tests/docs/test_gen_pack_reference.py
- tests/fixtures/invalid/**
- docs/guides/validate-a-pack.md
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP01 – Gate understands composition

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill: `python-pedro`. If the skill is not available, run `spec-kitty agent profile show python-pedro`.

## Objective

Teach the gate the strict composition rules, so correct qualified references pass and incorrect ones fail, while nothing has been migrated yet. Today it does the opposite: `validate_pack_schemas.py:782-783` reads `built-in::tactic:x` as kind `built-in`, so 67 correct edges would fail, and it passes everything the service refuses.

## Branch Strategy

- Planning/base branch: `feat/strict-pack-composition`. Final merge target: `feat/strict-pack-composition`, which reaches `main` by pull request after the mission.
- The workspace is resolved by `spec-kitty agent action implement`; trust the path it prints.

## Context

Read first: `kitty-specs/strict-pack-composition-01M6M0W4/spec.md`, `plan.md`, `data-model.md`, `research.md`. The full site list is `reference-inventory.txt` in the same folder.

Local tools. `python3 -m venv` fails on this machine; use the spec-kitty venv:

```bash
export PATH=~/Documents/code/kitty/spec-kitty/.venv/bin:$PATH
```

Git identity is not configured here. Pass it per command, do not edit config:
`GIT_AUTHOR_NAME="Stijn Dejongh" GIT_AUTHOR_EMAIL="stijn.dejongh@sddevelopment.be" GIT_COMMITTER_NAME="Stijn Dejongh" GIT_COMMITTER_EMAIL="stijn.dejongh@sddevelopment.be"`.

Pause and report, rather than deciding, on: changing an existing test's asserted expectation, any contract change, widening scope past this WP, or a mission runtime failure (C-005).

Implement with:

```bash
spec-kitty agent action implement WP01 --agent claude --mission strict-pack-composition-01M6M0W4
```

## Subtasks

### T001 Bump the contract pin

Set `CHARTER_COMMIT` in `scripts/ci/validate_pack_schemas.py` to a full SHA of spec-kitty-charter `main`. Fetch first (`git -C ~/Documents/code/kitty/spec-kitty-charter fetch origin`) and use the tip; it was `85c20fa1` at research time. Confirm `contracts/packs` has not changed in a way that adds violations by running the gate. Research measured 0 violations on as-is content, fixtures included. Correct `docs/guides/validate-a-pack.md:74-75`, which says the pin is on an open branch.

Never float this to a branch (C-003).

### T002 Parse qualifiers, by writing the tests first

Add failing tests in `tests/ci/test_validate_pack_schemas.py`, following that file's style (`write_contract`, `write_pack`, `run_validator`). A real contract is not needed; extend the test contract if a rule requires it.

In `cross_pack_violations`, split an edge end on `::` before the existing kind split. A qualifier maps to a pack through its descriptor `name`, never its directory: `packs/qa` answers to `quality-assurance`. Add one small helper; do not change `declared_nodes` at line 730, which reads declared nodes, not references.

Cases: `built-in::tactic:x` with `built-in` holding it passes; `built-in::tactic:gone` fails naming the reference. Assert the existing "declared by more than one pack" and "resolves to no node" checks still fire (positive control on the same fixture).

### T003 Add the composition checks

Under `--cross-pack`, all of these fail with the file and the reference named:

1. a bare reference held only by another pack;
2. a qualifier naming a pack outside the referrer's `depends_on` closure (`depends_on` is by `pack_id`);
3. a qualified target the named pack does not hold;
4. a pack directory with no `pack.yaml`;
5. duplicate `pack_id` or `name`.

Which references: both edge ends in `drg/fragment.yaml`, plus typed references in artifact files. The charter's list is `service/packs/.../domain/ArtifactEdges.java` and `infra/storage/DomainRepositoryService.java:314-345` in spec-kitty-charter; read them and check the same fields. Add the two forms from `data-model.md`. A bare reference no pack holds is **not** refused, and neither are `action:` targets. Do **not** reimplement ordering, level rules, version-range overlap or sibling logic (NFR-002: under 150 added production lines, and say the count in your report).

Add `PENDING_PACKS`, a module constant holding directory names `internal`, `qa`, `event-driven`, with a comment saying it only shrinks and is deleted by the end of the mission. Checks 1 to 3 skip a pack listed there. Check 4 also needs an allowance until WP02 adds the files: use a second constant, or include `cave-kitty` and the example fixture only for that check, whichever is shorter.

Every check gets a fixture that fails and a same-fixture positive control. Add `tests/fixtures/invalid/` entries only if a schema-level failure is needed; the composition checks are better as unit tests, because `--expect-invalid` does not run the cross-pack checks.

Existing tests whose fixtures run `--cross-pack` without a `pack.yaml` will fail check 4. Add a descriptor to the **fixture**; do not change what they assert. If an assertion must change, pause.

### T004 Fix the docs generator

`scripts/docs/gen_pack_reference.py:165-226` reads `pack.yaml` by hand and mangles the required `depends_on` shape into `('pack_id: 01ARWG13C000000000000000FG',)`, losing later entries. Replace the reader with `yaml.safe_load` (the job already installs pyyaml, but check `.github/workflows/docs-site.yml` and say if not), update its docstring, and test a `depends_on` of two entries in `tests/docs/test_gen_pack_reference.py`.

Lines 495-498 say `purpose` is a `pack.yaml` field, but the closed schema has no such property, and authoring one would make the file unreadable. Reword the placeholder so it does not suggest adding it. A generator change will drift `docs/packs/`; run the generator and include the regenerated pages in this WP's commit (out-of-map, recorded). Confirm `--check` passes.

### T005 Validate

Run the gates below over as-is content: all pass. Time the gate before and after (NFR-001: under 5 seconds added). Prove the fix half by half (tactic `acceptance-criteria-non-vacuity`): revert qualifier parsing alone and confirm tests go red; revert each composition check and confirm its test goes red. Report the results.

## Definition of Done

All gates pass on as-is content. Each FR-003 defect has a test that fails without its check. `PENDING_PACKS` exists and is documented. Added production lines reported, under 150.

Record subtask completion with `spec-kitty agent tasks mark-status <ids> --status done`.

## Reviewer guidance

Check that the local checks did not grow into a second resolver. Check that the bare-reference check really sees typed references, not only edges. Try a correct `built-in::<id>` typed reference and an incorrect `built-in::tactic:x` one in a fixture. Test names should state behaviour.
