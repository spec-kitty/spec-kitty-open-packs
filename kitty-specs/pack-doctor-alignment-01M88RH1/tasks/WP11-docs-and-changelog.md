---
work_package_id: WP11
title: Docs and changelog
dependencies: []
requirement_refs:
- FR-019
- FR-020
- SC-004
subtasks:
- T057
- T058
- T059
- T060
- T061
phase: Phase 4 - Retirement and polish
assignee: ''
agent: claude
shell_pid: ''
history:
- at: '2026-11-25T07:30:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: scribe-sally
authoritative_surface: docs/
execution_mode: planning_artifact
model: ''
owned_files:
- docs/guides/validate-a-pack.md
- docs/artefacts/index.md
- docs/plans/roadmap.md
- docs/changelog/CHANGELOG.md
role: documentarian
task_type: implement
---

# Work Package Prompt: WP11 - Docs and changelog

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load an agent profile for the role below, and behave according to its guidance before parsing the rest of this prompt. If your host cannot run skills, run `spec-kitty agent profile show <profile-id>` and apply the profile it prints.

- **Role**: `documentarian`
- **Profile override**: `scribe-sally`
- **Agent/tool**: `claude`

---

## IMPORTANT: Review Feedback

Check `review_ref` with `spec-kitty agent tasks status --mission pack-doctor-alignment-01M88RH1`. Address every item.

---

## Objectives & Success Criteria

- The validate-a-pack guide describes the gate as it now runs (FR-019):
  - pack-doctor at a charter-`main` pin;
  - `validate … --round-trip --full`;
  - the `PackDoctorReport`;
  - the anti-pattern file model;
  - `remediate` as the manifest fix;
  - the split between pack-doctor and the house rules.
- `docs/artefacts/index.md` lists anti-patterns as a file kind.
- No live doc surface names pack-check. History stays as written (occurrence map).
- One changelog entry (FR-020).
- The docs gates pass.

## Context & Constraints

- **Depends on**: WP10, so the docs describe the final split.
- **Charter docs rules**:
  - Common Docs (`DIRECTIVE_042`).
  - The generated/authored split (`DIRECTIVE_044`): never restate counts the generated pages hold.
  - Write for the audience (`DIRECTIVE_047`).
- **Read**: issues #345 item 9, #346 "What changes", #348 "Done when" and #350 "Also changes"; charter `docs/guides/check-packs.md`; `plan.md` IC-06.

## Branch Strategy

- **Planning base / merge target**: `feat/pack-doctor-alignment`
- `spec-kitty agent action implement WP11 --agent <name> --mission pack-doctor-alignment-01M88RH1`

## Subtasks & Detailed Guidance

### Subtask T057 - `docs/guides/validate-a-pack.md`

- Rename every live mention to pack-doctor, and point readers to charter `docs/guides/check-packs.md` for the CLI, the report and the exit codes.
- Rewrite these sections:
  - the gate section: the main pin on demand (operator ruling, 2026-11-25), the jar script, and `validate … --round-trip --full`;
  - "What pack-check covers": now "What pack-doctor covers". The preset rows read "refused" (`preset_item_not_held`, `preset_item_undeclared`); add the `REFERENCES` row and `manifest_stale`;
  - the house-rule list, with rulings;
  - the lock example (`pack_doctor_sha256`);
  - "Actions and anti-patterns have no file": now anti-patterns are files (`anti_patterns/<id>.anti-pattern.yaml`), each with a `severity` and a `bad_example`, rejected by guidance through `rejects` edges;
  - the manifest fix: `pack-doctor remediate <pack>` replaces `--regenerate-manifest`/`--derive-manifest`.

### Subtask T058 - `docs/artefacts/index.md`

- In the anti-pattern row: "its own file, `anti_patterns/<id>.anti-pattern.yaml`; declared by a graph node, rejected by `rejects` edges".
- Remove `anti_patterns` from the styleguide and procedure field lists.

### Subtask T059 - Roadmap and the live-surface grep

- `docs/plans/roadmap.md`: update "Waits on" for #345-#350. The release pin waits on the first `service-v*` after pack-doctor.
- Run this grep, which must return only occurrence-map exceptions:

  ```bash
  grep -rn "pack-check\|pack_check\|packCheck" --exclude-dir=.git --exclude-dir=site --exclude-dir=kitty-specs --exclude-dir=kitty-ops . \
    | grep -v "docs/changelog\|docs/architecture/adr"
  ```

  Paste the result into the history.

### Subtask T060 - Changelog

Add one entry under the unreleased heading of `docs/changelog/CHANGELOG.md`:

- the gate runs the charter's pack-doctor, at a charter-`main` pin by operator ruling, with `--round-trip --full`;
- anti-patterns are files, with a severity and a bad example: N files from 273 inline entries and 15 file-less nodes, with N taken from the tree;
- manifests are stamped by `pack-doctor remediate`;
- the Python rules the charter judges are retired, and the house rules are kept.

Name the issues it closes (#343, #345-#350) and any deferral, for example the release pin.

### Subtask T061 - Docs gates

- Run `python3 scripts/docs/check_docs_freshness.py`, `python3 scripts/docs/gen_pack_reference.py --check`, `python3 scripts/ci/check_vocabulary.py`, `pytest tests/docs tests/vocabulary -q`, and the link check the docs workflow runs (`.github/workflows/docs-site.yml`).
- Paste the results into the history.

## Risks & Mitigations

- **Restating a generated datum** (a count) in authored prose. Link to the generated page instead.

## Review Guidance

- Read the guide's coverage table against #348's table.
- Confirm the grep result and that the docs gates are green.

## Progress & Status

Use the CLI only (`add-history`, `move-task`).
