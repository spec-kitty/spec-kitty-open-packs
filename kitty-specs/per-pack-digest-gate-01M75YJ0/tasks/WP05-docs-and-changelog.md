---
work_package_id: WP05
title: Guides, PR template, ADR, packs README, charter prose and changelog
dependencies:
- WP03
- WP04
- WP06
requirement_refs:
- FR-008
- FR-011
- FR-013
- FR-014
- C-004
- C-006
- SC-003
planning_base_branch: feat/194-pack-digests
merge_target_branch: feat/194-pack-digests
branch_strategy: Planning artifacts for this mission were generated on feat/194-pack-digests. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/194-pack-digests unless the human explicitly redirects the landing branch.
subtasks:
- T017
- T018
- T019
- T020
- T021
- T022
history: []
agent_profile: scribe-sally
authoritative_surface: docs/
create_intent:
- docs/architecture/adr/2026-11-11-2-record-a-tree-digest-for-every-pack.md
execution_mode: code_change
model: sonnet
owned_files:
- docs/guides/validate-a-pack.md
- docs/guides/contributing.md
- docs/guides/publish-a-pack.md
- docs/changelog/CHANGELOG.md
- docs/architecture/adr/2026-11-11-2-record-a-tree-digest-for-every-pack.md
- docs/architecture/adr/index.md
- packs/README.md
- .kittify/charter/interview/answers.yaml
- .github/PULL_REQUEST_TEMPLATE.md
role: documentarian
tags: []
tracker_refs: []
---

# WP05 — Guides, PR template, ADR, packs README, charter prose and changelog

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load the agent profile specified in the frontmatter, and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `scribe-sally`
- **Role**: `documentarian`
- **Agent/tool**: `claude`

If no profile is specified, run `spec-kitty agent profile list` and select the best match for this work package's `task_type` and `authoritative_surface`.

---

Implement with: `spec-kitty agent action implement WP05 --agent claude --mission per-pack-digest-gate-01M75YJ0`

## Objective

Make the authored docs say what the gate now covers: every pack has a recorded digest, one command
restamps it, releases ship each pack's sidecar, and manifests must list every non-exempt graph node.
Add the PR-template checklist line, the ADR (and its index row) and the `[Unreleased]` entry.

## Context

- Charter: docs are first-class; generated vs authored split (DIRECTIVE_044) — do **not** paste
  digest values or pack counts into prose (those are generated facts); explain purpose and how-to.
  Keep docs in sync with shipped behaviour (DIRECTIVE_037). Existing ADRs are never edited; the new
  ADR 2026-11-11-2 is authored here (operator answer 3).
- Release asset name comes from WP06 (`<pack>-vX.Y.Z.source.yaml`); WP05 depends on WP06.
- Final names (from WP01/WP03): `scripts/ci/pack_digest.py` (`--check`, `--update`),
  `scripts/ci/check-pack-digests.sh`, CI step "Check every pack's recorded digest", sidecars
  `packs/<name>.source.yaml`; compatibility entry point `scripts/ci/built_in_digest.py`.
  Node completeness: `MANIFEST_EXEMPT_NODE_KINDS` in `validate_pack_schemas.py` (WP04).
- Occurrence map exceptions: do not edit `docs/architecture/adr/**`, released CHANGELOG sections,
  `kitty-ops/**`, other missions.
- Out of scope to mention as delivered: docs build as required check, #23 shared recipe, clean-tree-sha256.

### Subtask T017: `docs/guides/validate-a-pack.md`

**Steps**:
1. Replace the paragraph at ~lines 76-77 (built-in-only digest) with a short section
   "Recorded pack digests": what is hashed (every file in the pack directory except the root
   `pack-manifest.yaml`), where it is recorded (`packs/<name>.source.yaml`, beside the directory),
   that a new pack without a sidecar fails, and the two commands:
   `python3 scripts/ci/pack_digest.py --update` after an edit, `scripts/ci/check-pack-digests.sh`
   to run what CI runs.
2. Where the guide describes the manifest checks, add one sentence: every graph node of a
   manifest-bearing pack must be a constituent, except actions, anti-patterns, templates, mission
   types and step contracts.
3. Relative links (`../../scripts/ci/...`) like the existing ones.

### Subtask T018: `docs/guides/contributing.md`

**Steps**:
1. In the section describing what to run before a pack PR / the required checks, add: edit a pack →
   run `python3 scripts/ci/pack_digest.py --update` and commit the changed sidecar(s); a rebase over
   another pack change may need the same.
2. If the guide lists the gate's steps by name, rename the digest step.

### Subtask T019: `packs/README.md` and charter answers prose

**Steps**:
1. `packs/README.md` ~lines 47-48: replace "`scripts/ci/check-built-in.sh` checks the built-in
   digest" with: every pack's tree digest is recorded in `packs/<name>.source.yaml` and checked by
   `scripts/ci/check-pack-digests.sh`; keep the pointer to `built-in.source.yaml` for built-in's
   provenance.
2. `.kittify/charter/interview/answers.yaml` line ~18 mentions `scripts/ci/check-built-in.sh` in a
   prose answer: update the script name/coverage only (manual_review per occurrence map).
   Run `spec-kitty charter status` before and after the edit. If the edit makes the charter
   report drift/out-of-sync (answers feed the compiled charter), revert the edit and record in
   implementation notes that the reference waits for the next charter regeneration; do not
   regenerate the charter in this mission.
3. `packs/*/PROVENANCE.md` "see packs/built-in.source.yaml" pointers are about seed provenance
   and stay correct. Verify with `grep -n "built-in.source" packs/*/PROVENANCE.md` that each
   points at seed provenance (not at "the digest of this pack"); record the result in the
   implementation notes so FR-008's "PROVENANCE pointers where wrong" is visibly covered. Edit
   none unless one claims built-in's file holds that pack's digest (then this is an out-of-map
   edit: record a one-line rationale).

### Subtask T020: Changelog `[Unreleased]`

**Steps**:
1. In `docs/changelog/CHANGELOG.md` under `## [Unreleased]`, in the fitting subsection (Added /
   Changed — follow the file's existing headings and emoji style), add an entry:
   **Every pack has a recorded tree digest** (#194; epic #190): each `packs/<name>/` now has a
   sidecar `packs/<name>.source.yaml`; the required gate checks all of them
   (`scripts/ci/check-pack-digests.sh`, formerly `check-built-in.sh`); `pack_digest.py --update`
   restamps; `built_in_digest.py` stays as a compatibility entry point; `packs/built-in.source.yaml`
   keeps its path and keys. Plus: manifests must list every non-exempt graph node (residual of #182).
2. Mention related #23/#19 only as "see also", not as delivered.
3. Add to the same entry: release archives now ship each pack's sidecar as
   `<pack>-vX.Y.Z.source.yaml` (WP06), and link the new ADR 2026-11-11-2.
4. In `docs/guides/publish-a-pack.md` (~line 39, where the `.tar.gz` and `.sha256` assets are
   described), add one sentence: each release also carries `<pack>-vX.Y.Z.source.yaml`, the pack's
   recorded tree digest at the tagged commit. Use WP06's actual asset name.

### Subtask T021: PR template checklist line

**Purpose**: FR-014 / operator answer 1.

**Steps**:
1. In `.github/PULL_REQUEST_TEMPLATE.md`, section `## Pack changes (if applicable)`, add after the
   `validate-packs.sh` line:
   `- [ ] Pack digests restamped: \`python3 scripts/ci/pack_digest.py --update\` and the changed \`packs/<pack>.source.yaml\` committed (\`scripts/ci/check-pack-digests.sh\` passes)`
2. Keep the existing lines and order untouched.

**Validation**: the command in the line runs verbatim from the repo root.

### Subtask T022: ADR 2026-11-11-2 and index row

**Purpose**: FR-013 / operator answer 3.

**Steps**:
1. Create `docs/architecture/adr/2026-11-11-2-record-a-tree-digest-for-every-pack.md` from
   `docs/architecture/adr/adr-template.md`. Front matter like the sibling
   `2026-11-11-1-…md` (title `'ADR: Record a tree digest for every pack'`, `doc_status: active`,
   `updated: '2026-11-11'`, `related:` packs + `architecture/adr/2026-10-20-1-semver-releases-with-per-pack-archives`).
   **`description` must be at most 180 characters** (docs validator; see commit faa4770). Example
   (≈150 chars): "Every pack records a snapshot_sha256 tree digest in its own sidecar, checked fail-closed in the
   required gate and shipped with each release."
   Verify: `python3 -c "import yaml,sys;d=next(yaml.safe_load_all(open(sys.argv[1])));print(len(d['description']))" <file>` ≤ 180.
2. Status `Accepted`. Context: ADR 2026-10-20-1 records `tree_digest` only for built-in, which
   since #73 is a shell. Decision: every `packs/<name>/` with `pack.yaml` has
   `packs/<name>.source.yaml` (outside the hashed tree) with `tree_digest {algorithm:
   spec-kitty-snapshot-sha256, value}`; recipe unchanged (core's `snapshot_sha256`); missing,
   stale or orphan sidecars fail the required `Validate packs gate`; `pack_digest.py --update`
   restamps; releases ship `<pack>-vX.Y.Z.source.yaml`. Options considered: one map in
   `built-in.source.yaml`; stamp in `pack-manifest.yaml`; per-pack sidecar (chosen) — take the
   pros/cons from `kitty-specs/per-pack-digest-gate-01M75YJ0/research.md` D1/D10.
   Consequences: every pack edit restamps one line; `built-in.source.yaml` path/keys unchanged for
   core; clean-tree-sha256 and the #23 docs checksum stay separate. State that it extends (does
   not supersede) ADR 2026-10-20-1, which is not edited.
3. Add a row to the `## Index` table in `docs/architecture/adr/index.md` after the 2026-11-11 / 1
   row: `| 2026-11-11 | 2 | [Record a tree digest for every pack](2026-11-11-2-record-a-tree-digest-for-every-pack.md) | Accepted |`;
   bump the index's `updated:` only if it is not already `'2026-11-11'`.
4. Keep the ADR short (≤ ~80 lines). No digest values or pack counts in prose (DIRECTIVE_044).

**Validation**: the docs validator passes if available (`npm run validate` in the docs site);
otherwise check the description length and that every link resolves.

## Definition of Done

- The guides, packs README, PR template, ADR and changelog describe the shipped commands, names and
  release asset exactly; no digest values or counts in prose.
- ADR file exists, `description` ≤ 180 characters, index row present; ADR 2026-10-20-1 unchanged.
- `grep -rn "check-built-in" docs/guides packs/README.md` returns nothing.
- Docs checks pass locally where available (`npm run validate` in the docsite if set up; at minimum
  `python3 scripts/docs/gen_pack_reference.py --check` and the vocabulary guard).
- Subtasks recorded via `spec-kitty agent tasks mark-status`.

## Risks

- Restating generated facts in prose (DIRECTIVE_044) → describe, don't enumerate.
- Editing history (existing ADRs, released changelog) → forbidden by occurrence map.
- ADR `description` over 180 characters fails the docs validator (it bit faa4770) → measure it.

## Reviewer Guidance

- Follow the guide's commands on a scratch edit; they must work verbatim.
- Check the changelog entry sits under `[Unreleased]` only.
