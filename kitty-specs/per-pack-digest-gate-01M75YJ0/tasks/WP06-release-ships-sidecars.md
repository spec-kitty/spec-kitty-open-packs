---
work_package_id: WP06
title: Release archives ship each pack's sidecar
dependencies:
- WP02
requirement_refs:
- FR-012
- SC-006
- C-001
- C-002
planning_base_branch: feat/194-pack-digests
merge_target_branch: feat/194-pack-digests
branch_strategy: Planning artifacts for this mission were generated on feat/194-pack-digests. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/194-pack-digests unless the human explicitly redirects the landing branch.
subtasks:
- T023
- T024
- T025
- T026
history: []
agent_profile: python-pedro
authoritative_surface: scripts/release/
create_intent: []
execution_mode: code_change
model: sonnet
owned_files:
- scripts/release/release_assets.py
- tests/release/test_release_assets.py
- .github/workflows/release.yml
role: implementer
tags: []
tracker_refs: []
---

# WP06 — Release archives ship each pack's sidecar

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load the agent profile specified in the frontmatter, and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`
- **Agent/tool**: `claude`

If no profile is specified, run `spec-kitty agent profile list` and select the best match for this work package's `task_type` and `authoritative_surface`.

---

Implement with: `spec-kitty agent action implement WP06 --agent claude --mission per-pack-digest-gate-01M75YJ0`

## Objective

`scripts/release/release_assets.py build vX.Y.Z` also writes `<pack>-vX.Y.Z.source.yaml` for every
released pack: the exact bytes of `packs/<pack>.source.yaml` at the tagged commit. A released pack
with no sidecar at that commit fails the build. The release workflow publishes them with the
archives.

## Context

- Operator answer 2 (spec Decision 9, FR-012, SC-006; research D10). ADR 2026-10-20-1 says a
  consumer pins `{tag, commit, archive_sha256, tree_digest}`; today only the archive and its
  `.sha256` ship.
- WP02 creates a sidecar for every pack, so on a real tag every pack has one.
- Read `scripts/release/release_assets.py` fully first. Key facts:
  - Content comes from the **git tree of the tagged commit** via `_git`/`git cat-file --batch`
    (`_read_blobs`), never the working tree. Keep that for the sidecar.
  - `list_packs(repo, rev)` returns directories under `packs/`; non-tree entries that are blobs
    (the sidecars, `README.md`) are skipped, other kinds raise.
  - `write_assets(repo, rev, tag, out)` writes `<pack>-<tag>.tar.gz` and `.sha256` per pack and
    returns the written paths, which `main` prints.
- `.github/workflows/release.yml` job `release`: "Build archives" runs `build`; "Archives are
  reproducible" rebuilds into `dist-rebuild` and diffs `sha256sum *.tar.gz` and checks
  `*.sha256`; "Publish" uploads `dist/*` and compares the uploaded count with `ls dist | wc -l`, so
  new files in `dist/` are published and counted with no change to that step.
- Tests: `tests/release/test_release_assets.py` builds a temporary git repo in `setUp`
  (`packs/built-in`, `packs/qa`), commits and tags `v1.2.3`. CI runs
  `python3 -m unittest discover -s tests/release` ("Release tooling tests").
- Stdlib only (the module docstring says so). Do not import `pack_digest.py` and do not recompute
  digests here: the gate at the tagged commit already proved them (the release workflow runs
  `validate-packs.yml` first). This WP only ships the recorded file.

### Subtask T023: Read the sidecar from the tagged tree

**Steps**:
1. Add `SIDECAR_SUFFIX = ".source.yaml"`.
2. Add `sidecar_bytes(repo: Path, rev: str, pack: str) -> bytes`: resolve
   `git rev-parse --verify --quiet {rev}:packs/{pack}.source.yaml`. A missing object raises
   `ReleaseError(f"packs/{pack}.source.yaml is missing at {rev}; every released pack needs its recorded digest (run python3 scripts/ci/pack_digest.py --update)")`.
   If the entry is not a blob, raise too. Read it with `_read_blobs` (or `git cat-file blob`).
3. Do not parse or rewrite it: ship the bytes as committed.

**Validation**: unit test in T025.

### Subtask T024: Write the asset

**Steps**:
1. In `write_assets`, per pack, after the `.sha256`: write `out / f"{pack}-{tag}.source.yaml"` with
   `sidecar_bytes(...)` (binary write) and append it to `written`.
2. Asset names stay unique: `<pack>-vX.Y.Z.tar.gz`, `.tar.gz.sha256`, `.source.yaml`.
3. Update the module docstring and the `build` sub-command help: "write every pack's archive,
   .sha256 and recorded-digest sidecar".
4. Check the whole build before writing anything, or accept partial writes? Today an error in one
   pack leaves earlier files in `out`; keep that behaviour (the workflow fails the job), but check
   all sidecars **first** so a missing one fails fast before archives are built. Document this
   in the function's docstring.

**Validation**: `scripts/release/release_assets.py build v0.0.0 --rev HEAD --out /tmp/x` on the
real repo (after WP02) lists one `.source.yaml` per pack.

### Subtask T025: Tests

Add to `tests/release/test_release_assets.py`; extend the `setUp` fixture so both fixture packs
have a sidecar (`packs/built-in.source.yaml`, `packs/qa.source.yaml`, small YAML with a comment):
1. `test_every_pack_ships_its_sidecar`: `write_assets` returns, per pack, a `.source.yaml` whose
   bytes equal the committed sidecar bytes (compare with `git show v1.2.3:packs/qa.source.yaml`).
2. `test_sidecar_comes_from_the_tag_not_the_working_tree`: modify `packs/qa.source.yaml` in the
   working tree after tagging; the built asset still holds the tagged bytes.
3. `test_a_pack_without_a_sidecar_fails_the_release`: remove one sidecar, commit, tag `v1.2.4`;
   `write_assets` raises `ReleaseError` naming `packs/qa.source.yaml`; and the same fixture with
   the sidecar restored passes (positive control).
4. `test_sidecars_are_not_packs`: `list_packs` still returns only `["built-in", "qa"]` with
   sidecars present (the existing test asserts this; keep it green with the new fixture files).
5. Existing tests (reproducibility, archive equals subtree, `.sha256` matches) stay green: the
   sidecars live outside the pack directories, so the archives are unchanged.

**Validation**: `python3 -m unittest discover -s tests/release -v` green.

### Subtask T026: Release workflow reproducibility step

**Steps**:
1. In `.github/workflows/release.yml`, step "Archives are reproducible", also compare the sidecars:
   `diff <(cd dist && sha256sum *.tar.gz *.source.yaml) <(cd dist-rebuild && sha256sum *.tar.gz *.source.yaml)`.
   Rename the step to "Release assets are reproducible" only if no test or doc refers to the old
   name (grep `tests/` and `docs/`); otherwise keep the name.
2. Do not change the Publish step: it uploads `dist/*` and counts the files, which now include the
   sidecars. Add a one-line comment there saying the count includes each pack's `.source.yaml`.
3. Update the workflow header comment (lines ~3-6) to list the sidecar among the assets.

**Validation**: `python3 -m unittest discover -s tests/ci -p 'test_workflows.py'` still green
(it parses workflows; make sure YAML stays valid); `python3 -c "import yaml;yaml.safe_load(open('.github/workflows/release.yml'))"`.

## Definition of Done

- `build` writes one `<pack>-vX.Y.Z.source.yaml` per released pack, bytes from the tagged tree.
- A released pack without a sidecar at the tag fails the build with an actionable message.
- New tests green, each failure case with a same-fixture positive control; existing release tests green.
- Workflow reproducibility check covers the sidecars; Publish unchanged apart from a comment.
- No file outside `owned_files` touched (docs mention is WP05's).
- Subtasks recorded via `spec-kitty agent tasks mark-status`.

## Risks

- Reading the sidecar from the working tree instead of the tag would let an uncommitted edit leak
  into a release → T025 test 2.
- An asset name colliding with a pack named like `x.source` → names are `<pack>-<tag>.source.yaml`,
  and `<tag>` is `vX.Y.Z`, so no collision with `.tar.gz` files.
- Old tags (before WP02) have no sidecars: rebuilding an old release with this code fails. That is
  intended (fail closed); note it in the docstring. Releases are only cut from new tags.

## Reviewer Guidance

- Confirm the sidecar is read with git plumbing at `rev`, never `Path.read_bytes()`.
- Confirm the missing-sidecar error fires before any archive is written.
- Confirm the reproducibility diff includes `*.source.yaml`.
