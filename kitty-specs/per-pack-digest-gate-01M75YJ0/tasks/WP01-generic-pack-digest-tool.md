---
work_package_id: WP01
title: Generic pack digest tool, built-in shim and unit tests
dependencies: []
requirement_refs:
- FR-001
- FR-002
- FR-003
- FR-004
- FR-006
- FR-010
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-002
planning_base_branch: feat/194-pack-digests
merge_target_branch: feat/194-pack-digests
branch_strategy: Planning artifacts for this mission were generated on feat/194-pack-digests. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/194-pack-digests unless the human explicitly redirects the landing branch.
subtasks:
- T001
- T002
- T003
- T004
- T005
- T006
history: []
agent_profile: python-pedro
authoritative_surface: scripts/ci/
create_intent:
- scripts/ci/pack_digest.py
- tests/ci/test_pack_digest.py
execution_mode: code_change
model: sonnet
owned_files:
- scripts/ci/pack_digest.py
- scripts/ci/built_in_digest.py
- tests/ci/test_pack_digest.py
role: implementer
tags: []
tracker_refs: []
---

# WP01 — Generic pack digest tool, built-in shim and unit tests

## ⚡ Do This First: Load Agent Profile

Use the `/spk-charter-profile-load` skill to load the agent profile specified in the frontmatter, and behave according to its guidance before parsing the rest of this prompt.

- **Profile**: `python-pedro`
- **Role**: `implementer`
- **Agent/tool**: `claude`

If no profile is specified, run `spec-kitty agent profile list` and select the best match for this work package's `task_type` and `authoritative_surface`.

---

Implement with: `spec-kitty agent action implement WP01 --agent claude --mission per-pack-digest-gate-01M75YJ0`

## Objective

Create `scripts/ci/pack_digest.py`: the existing `snapshot_sha256` recipe, byte-for-byte, applied to
any pack directory, plus pack discovery, a fail-closed `--check` and a text-preserving `--update`.
Turn `scripts/ci/built_in_digest.py` into a thin compatibility shim. Add the first unit tests for
the recipe.

## Context

- Issue #194: after the #73 split, `packs/built-in/` is a five-file shell; the only recorded digest
  proves no doctrine. Operator decisions (spec.md "Decisions"): a sidecar per pack
  (`packs/<dirname>.source.yaml`), recipe unchanged (C-001), every `packs/*/pack.yaml` participates.
- Read first: `kitty-specs/per-pack-digest-gate-01M75YJ0/spec.md`, `plan.md`, `research.md` (D1–D7),
  `data-model.md` (sidecar states), `contracts/pack-digest-cli.md` (the CLI contract you implement),
  `contracts/sidecar.schema.yaml`.
- Current code: `scripts/ci/built_in_digest.py` (60 lines). Its `snapshot_sha256` is the reference.
- External callers to keep working: kitty-stack runs `python3 scripts/ci/built_in_digest.py` with no
  arguments and reads one hex line; `scripts/ci/check-built-in.sh` runs `built_in_digest.py --check`
  (WP03 rewires that; until then it must keep passing).
- WP02 runs your `--update` to generate 18 new sidecars; WP03 wires `--check` into CI. Get the
  contract right; they depend on it.
- Only stdlib + PyYAML (NFR-004). CI runs `python3 -m unittest discover -s tests/ci`.

### Subtask T001: Move the recipe into `pack_digest.py`

**Purpose**: one importable implementation of the recipe for any directory.

**Steps**:
1. Create `scripts/ci/pack_digest.py` with a module docstring describing the recipe (copy the
   wording from `built_in_digest.py`'s docstring, generalised: "a pack directory") and the CLI usage
   from `contracts/pack-digest-cli.md`.
2. Constants: `REPO_ROOT = Path(__file__).resolve().parents[2]`, `PACKS = REPO_ROOT / "packs"`,
   `MANIFEST = "pack-manifest.yaml"`, `ALGORITHM = "spec-kitty-snapshot-sha256"`,
   `SIDECAR_SUFFIX = ".source.yaml"`.
3. Copy `snapshot_sha256(root: Path) -> str` **verbatim** (same sort key, same symlink/special-file
   refusals, same root-only manifest exclusion, same length prefixes). Do not "improve" it: no CRLF
   normalisation, no new exclusions, no streaming changes that alter bytes hashed. Reading files
   in chunks is fine only if the bytes fed to the hash are identical; simplest is to keep it as is.

**Files**: `scripts/ci/pack_digest.py` (new, ~200 lines when the WP is done).

**Validation**: `python3 -c "import sys; sys.path.insert(0,'scripts/ci'); import pack_digest as p; print(p.snapshot_sha256(p.PACKS/'built-in'))"`
prints `ad841252089ca5cdc5da33d7a027fb34386a80fe64249c1e368e61162dea38ca`.

### Subtask T002: Discovery and sidecar reading

**Purpose**: find every participating pack and every sidecar, and classify each pack's state.

**Steps**:
1. `discover_packs(packs_root: Path) -> list[Path]`: sorted directories `d` in `packs_root` where
   `(d / "pack.yaml").is_file()`. Do not hardcode names. Ignore files (`README.md`, sidecars).
2. `sidecar_path(pack_dir: Path) -> Path`: `pack_dir.parent / f"{pack_dir.name}{SIDECAR_SUFFIX}"`
   (directory name, not `pack_id` — research D5).
3. `orphan_sidecars(packs_root) -> list[Path]`: every `*.source.yaml` in `packs_root` whose stem
   (strip `.source.yaml`) is not a discovered pack directory.
4. `recorded_digest(sidecar: Path) -> str`: `yaml.safe_load`; raise a `SidecarError(ValueError)`
   with a precise message when the file is not a mapping, `tree_digest` is missing, `algorithm`
   is not `ALGORITHM`, or `value` is not 64 lowercase hex. Also catch `yaml.YAMLError` and
   `UnicodeDecodeError` and re-raise as `SidecarError` (state `malformed`), so a broken sidecar
   yields an `::error` line, never a traceback (NFR-003).
5. A small result type (dataclass or tuple) `PackStatus(name, state, actual, recorded, message)`
   with `state` in `{"fresh", "stale", "missing", "malformed"}`; orphans are reported separately.

**Validation**: unit tests in T005 cover each state.

### Subtask T003: `--check`

**Purpose**: the fail-closed verification CI runs.

**Steps**:
1. `check(packs_root, names: list[str] | None) -> int`. With no names, check every discovered pack
   **and** report orphans. With names, check only those (unknown name → usage error exit 2).
2. Report every failing pack in one run (do not stop at the first).
3. Failure line format (NFR-003), one per problem:
   `::error file=packs/<name>.source.yaml::<reason>; run \`python3 scripts/ci/pack_digest.py --update <name>\``
   - stale: `packs/<name>/ digest <actual> != recorded <recorded>`
   - missing: `packs/<name>/ has no recorded digest`
   - malformed: the `SidecarError` message (remedy: fix the file by hand; `--update` refuses it)
   - orphan: `no pack directory packs/<stem>/ for this sidecar; delete it` (no update remedy)
4. Success line per fresh pack: `ok: packs/<name>/ digest matches <value>`.
5. Exit 0 when all fresh and no orphan; 1 otherwise.
5a. **Non-vacuity**: if discovery finds no pack at all, print `::error::no pack found under packs/`
   and exit 1 (both `--check` and `--update`). This replaces the built-in-only `pack.yaml` guard
   that WP03 removes from the entry script.
6. Paths in messages are repo-relative POSIX (`packs/...`), computed relative to `packs_root.parent`
   so temp-dir tests produce the same shape.

**Validation**: on the current tree (before WP02) `--check` fails for 18 packs (missing) and passes
built-in. That is expected.

### Subtask T004: `--update`

**Purpose**: nobody hand-copies digests (operator decision 5).

**Steps**:
1. `update(packs_root, names) -> int`. For each selected pack:
   - **fresh**: no write (idempotent, NFR-002).
   - **stale**: rewrite only the value. Use a targeted text substitution on the line matching
     `^(\s+value:\s*)([0-9a-f]{64})\s*$` that sits under the `tree_digest:` block (find the
     `tree_digest:` line, then the first following indented `value:` line). Do **not** round-trip
     YAML: comments and `seeded_from` must survive byte-for-byte. If the substitution does not
     match **exactly once** (e.g. a quoted `value: '…'`), treat the sidecar as malformed: write
     nothing, print the `::error` line, exit 1.
   - **missing**: create the sidecar from a fixed template:
     ```yaml
     # Recorded tree digest of packs/<name>/ (spec-kitty-open-packs#194).
     # Generated by `python3 scripts/ci/pack_digest.py --update`; scripts/ci/check-pack-digests.sh
     # verifies it. The algorithm is spec-kitty-snapshot-sha256 (see scripts/ci/pack_digest.py).
     tree_digest:
       algorithm: spec-kitty-snapshot-sha256
       value: <hex>
     ```
     Keep the header free of retired vocabulary (the vocabulary guard scans `packs/`).
   - **malformed**: do not write; print the `::error` line; exit 1 at the end.
2. Orphans are reported (warning line) but never deleted automatically.
3. Print one line per written file: `updated: packs/<name>.source.yaml` / `created: ...`.
4. Write with `newline="\n"`, UTF-8, trailing newline.
5. `--check` and `--update` are mutually exclusive (argparse group). No flag: print
   `<digest>  packs/<name>` for each selected pack.

**Validation**: after `--update` on a stale fixture, `--check` passes and `git diff` shows one
changed line per stale sidecar; a second `--update` prints nothing and changes no bytes.

### Subtask T005: Unit tests `tests/ci/test_pack_digest.py`

**Purpose**: the recipe has no tests today (FR-010). Each behaviour test pairs a failing and a
passing case on the same fixture (non-vacuity).

**Steps** (unittest, `tempfile.TemporaryDirectory`, import via `sys.path.insert(0, scripts/ci)`
the same way `tests/ci/test_validate_pack_schemas.py` imports the validator):
1. **Recipe vector**: a fixture tree `{"a.txt": b"x", "sub/b.txt": b"yz", "pack-manifest.yaml": b"m"}`;
   assert a hard-coded expected hex (compute it once with the verbatim recipe and paste it), and
   assert changing `pack-manifest.yaml` does not change it while changing `sub/pack-manifest.yaml`
   does.
2. **Real-tree parity**: `snapshot_sha256(PACKS / "built-in")` equals the value recorded in
   `packs/built-in.source.yaml` (ties the recipe to core's pin).
3. Symlink refuses (`OSError`); skip on platforms without symlink support.
4. Discovery: a `packs/` fixture with `p1/pack.yaml`, `p2/` (no pack.yaml), `README.md`,
   `p1.source.yaml`, `ghost.source.yaml` → packs `[p1]`, orphans `[ghost.source.yaml]`.
5. Check states: fresh → exit 0 + ok line; flip one byte → exit 1 + stale line naming the sidecar
   and the `--update p1` command; delete sidecar → missing; bad algorithm / non-hex → malformed;
   orphan → exit 1; invalid YAML and non-UTF-8 bytes → malformed line, no traceback; empty
   `packs/` (no pack.yaml anywhere) → exit 1 "no pack found".
6. Update: stale → only the value line changes (compare all other lines, including a comment and
   a `seeded_from` block); missing → created with template; second run → no write (mtime/bytes
   unchanged); malformed → untouched, exit 1; quoted `value: '<hex>'` that is stale → refused,
   file untouched, exit 1.
7. Real-tree discovery (NFR-001): `discover_packs(PACKS)` names equal exactly the set of
   directories under `packs/` that hold a `pack.yaml` (computed independently in the test with
   `glob("*/pack.yaml")`), so discovery cannot silently drop a pack; and a full real-tree
   `snapshot_sha256` over every discovered pack completes without error.

**Files**: `tests/ci/test_pack_digest.py` (new, ~200 lines).

**Validation**: `python3 -m unittest discover -s tests/ci -p 'test_pack_digest.py' -v` green.

### Subtask T006: Compatibility shim `built_in_digest.py`

**Purpose**: FR-006 — kitty-stack and the current `check-built-in.sh` keep working.

**Steps**:
1. Replace the body of `scripts/ci/built_in_digest.py` with: a docstring saying it is a
   compatibility entry point for `packs/built-in` kept for external callers (kitty-stack
   `open-packs digest`), pointing to `pack_digest.py`; import `snapshot_sha256`, `check` from
   `pack_digest` (same directory: `sys.path.insert(0, str(Path(__file__).resolve().parent))`).
2. Keep the CLI: no args → print **only** the hex digest of `packs/built-in` (one line, nothing
   else); `--check` → `pack_digest.check(PACKS, ["built-in"])` exit code.
3. Keep `snapshot_sha256` importable from `built_in_digest` (re-export) in case anything imports it.
4. Add a test in `test_pack_digest.py`: run the shim via `subprocess` with no args; stdout is
   exactly the built-in digest + newline; `--check` exits 0 on the real tree.

**Validation**: `python3 scripts/ci/built_in_digest.py` prints `ad8412…38ca`;
`scripts/ci/check-built-in.sh` still exits 0.

## Definition of Done

- `pack_digest.py` implements `contracts/pack-digest-cli.md` exactly (print / `--check` / `--update`, exit codes, message shapes).
- Recipe unchanged: built-in digest equals the recorded `ad8412…38ca`.
- Shim prints the same single line as before; `--check` works; `check-built-in.sh` still green.
- `tests/ci/test_pack_digest.py` green; every behaviour has a paired fail/pass case.
- No new dependency. No file outside `owned_files` touched (sidecars are WP02's).
- Each subtask recorded with `spec-kitty agent tasks mark-status T00x --status done`.

## Risks

- **Silent recipe change** (e.g. sorting by `str(path)` instead of the relative POSIX path, or
  reading text instead of bytes) → caught by the real-tree parity test; keep the code verbatim.
- **Update rewrites YAML** and drops comments → forbidden; targeted line substitution only.
- **Regex hits the wrong `value:`** (e.g. a future `snapshot_sha256:` block) → anchor on the line
  after `tree_digest:`; test with a sidecar containing another `value:` key elsewhere.

## Reviewer Guidance

- Diff `snapshot_sha256` against the original in `git show HEAD~:scripts/ci/built_in_digest.py`: must be identical logic.
- Run `--update` twice on a temp copy; second run must be a no-op.
- Check every failure line names a sidecar path and a remedy command (NFR-003).
- Confirm the shim's no-arg stdout is a bare hex line (kitty-stack parses it).
