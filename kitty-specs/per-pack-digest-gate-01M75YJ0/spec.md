# Mission Specification: Per-pack digest gate

**Mission Branch**: `feat/194-pack-digests`
**Created**: 2026-11-11
**Status**: Draft
**Input**: Issue #194 ("Extend the built-in digest gate to foundation and writing"), widened by operator decision to every pack under `packs/`, plus the residual #182 manifest-completeness gap. Epic #190; related #23, #19.

## Intent Summary (confirmed by operator decisions)

- **Primary actor**: a pack maintainer or contributor who edits any pack under `packs/`; secondary actors are the CI gate and downstream pinners (spec-kitty core, kitty-stack).
- **Trigger**: a change to any file inside a pack directory.
- **Outcome**: the change is only mergeable when the pack's recorded tree digest has been restamped in its sidecar, with one command; CI proves every pack's digest, not just the built-in shell's.
- **Invariant**: every directory `packs/<name>/` that holds a `pack.yaml` has a sidecar `packs/<name>.source.yaml` whose recorded tree digest equals the digest of the directory's current content. Absence or staleness fails closed.
- **Second invariant (#182 residual)**: in every pack that ships a `pack-manifest.yaml`, every declared graph node of a file-backed kind is a manifest constituent.

Discovery was replaced by the operator's decision record (see `research.md` and the Decisions section); no interview questions were left open.

## Domain Language

| Term | Meaning | Avoid |
|------|---------|-------|
| tree digest | The `spec-kitty-snapshot-sha256` value over a pack directory, as `scripts/ci/built_in_digest.py` computes it today (every regular file except the root `pack-manifest.yaml`; length-prefixed path + size + raw bytes; sorted by POSIX path; symlinks refused). | "checksum" (that is the docs-page recipe of #23), "clean-tree digest" (core's other recipe, out of scope) |
| sidecar | `packs/<name>.source.yaml`, beside (outside) the pack directory, recording `tree_digest {algorithm, value}` and optional provenance. | "pin file" (core's term for its own file) |
| participating pack | Any directory `packs/<name>/` holding a `pack.yaml`. | "built-in-level pack" (participation is no longer limited by level) |
| digest gate | The check, run inside the required `Validate packs gate`, that every participating pack has a fresh sidecar. | "built-in check" |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Any pack edit is caught by the digest gate (Priority: P1)

A contributor edits a tactic in `packs/foundation/`. Today nothing records foundation's digest, so the change is invisible to anyone pinning by digest. After this mission the gate fails until the contributor restamps the sidecar.

**Why this priority**: it is the defect #194 reports; after the #73 split the only recorded digest covers a five-file shell.

**Independent Test**: change one byte in any pack, run the digest gate: it fails naming that pack and the restamp command; restamp; it passes.

**Acceptance Scenarios**:

1. **Given** all sidecars are fresh, **When** the gate runs, **Then** it passes and reports one ok line per participating pack (19 today).
2. **Given** a byte changed in `packs/writing/`, **When** the gate runs, **Then** it fails, names `packs/writing.source.yaml`, the actual and recorded digests, and the restamp command.
3. **Given** a new directory `packs/new-pack/` with a `pack.yaml` and no sidecar, **When** the gate runs, **Then** it fails closed naming the missing sidecar.
4. **Given** a sidecar `packs/ghost.source.yaml` with no `packs/ghost/pack.yaml`, **When** the gate runs, **Then** it fails naming the orphan sidecar.

### User Story 2 - Restamp with one command (Priority: P1)

A maintainer runs one update command after editing packs; it rewrites only the `tree_digest.value` of stale sidecars, creates missing ones, and leaves comments and provenance untouched.

**Why this priority**: today the error message tells people to hand-copy a hex string; with 19 participating packs that is untenable.

**Independent Test**: make two packs stale, run update, observe exactly those two sidecars change (value only) and the gate passes.

**Acceptance Scenarios**:

1. **Given** two stale sidecars, **When** update runs, **Then** exactly those two files change, only on the `value` line, and a subsequent check passes.
2. **Given** a pack with no sidecar, **When** update runs, **Then** a sidecar is created with the standard header comment and `tree_digest`.
3. **Given** all sidecars fresh, **When** update runs, **Then** no file changes (idempotent).

### User Story 3 - Downstream pinners are not broken (Priority: P1)

spec-kitty core reads `packs/built-in.source.yaml`; kitty-stack runs `scripts/ci/built_in_digest.py` with no arguments to print built-in's digest.

**Independent Test**: `python3 scripts/ci/built_in_digest.py` prints the same value as before for an unchanged `packs/built-in/`; `packs/built-in.source.yaml` keeps its path, `seeded_from` and `tree_digest {algorithm, value}` keys.

**Acceptance Scenarios**:

1. **Given** the unchanged built-in tree, **When** `built_in_digest.py` runs without arguments, **Then** it prints `ad841252089ca5cdc5da33d7a027fb34386a80fe64249c1e368e61162dea38ca`.
2. **Given** the old invocation `built_in_digest.py --check`, **When** it runs, **Then** it still checks built-in and exits 0/1 as before.

### User Story 4 - Manifest lists every file-backed graph node (Priority: P2)

A maintainer adds a graph node for a tactic to `packs/testing/drg/fragment.yaml` but forgets the manifest entry. The pack validator now refuses it.

**Independent Test**: on a fixture pack whose graph declares a `tactic` node that no constituent lists (and no artifact file backs, so the existing file-based #182 guard is silent), the validator reports the node; adding the constituent clears it.

**Acceptance Scenarios**:

1. **Given** the seven manifest-bearing packs as they are today, **When** the validator runs, **Then** no node is reported (all pass, measured at planning time).
2. **Given** a declared `tactic` node with no constituent, **When** the validator runs, **Then** it reports `incomplete manifest: graph node tactic:<id> is not a constituent`.
3. **Given** a declared node of an exempt kind (`action`, `anti_pattern`, `template`, `mission_type`, `mission_step_contract`), **When** the validator runs, **Then** it is not reported.

### User Story 5 - Names and docs say what is covered (Priority: P3)

The CI step, the entry script, comments and the guides say "pack digests", not "built-in digest", and the changelog records the change.

**Independent Test**: grep for the old step name and stale "built-in only" wording in the touched files returns nothing; the guides describe the update command.

### Edge Cases

- A pack directory containing a symlink or special file: the digest refuses (existing behaviour, kept).
- The root `pack-manifest.yaml` is excluded from a pack's digest; a nested file of the same name is not (existing behaviour, kept).
- `packs/README.md` and other non-directory entries under `packs/` are not packs.
- A directory under `packs/` without `pack.yaml` is not a participating pack (and is not given a sidecar).
- `pack_id` differs from directory name (`packs/internal` is `spec-kitty-internal`): the sidecar is keyed by directory name, matching `built-in.source.yaml`.
- CRLF content: digest is over raw bytes; `.gitattributes` governs checkout; no normalisation is added.
- A sidecar whose YAML is malformed or lacks `tree_digest.value`: check fails naming the file; update refuses to overwrite it rather than silently replacing it.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status | Delivery | No-op passable? |
|----|-------|------------|----------|--------|----------|-----------------|
| FR-001 | Pack-parametrised digest | As a maintainer, I want the existing snapshot_sha256 recipe computed for any pack directory, byte-for-byte unchanged, so that core's recipe still matches. | High | Open | [build] | no — built-in's value must equal the recorded ad8412… on the same tree while another pack yields its own value |
| FR-002 | Discover participating packs | As the gate, I want every `packs/*/pack.yaml` directory discovered, not a hardcoded list, so that a new pack cannot slip past. | High | Open | [build] | no — fixture with a new pack and no sidecar must fail |
| FR-003 | Check all sidecars, fail closed | As the gate, I want a check mode that fails on a missing, stale, malformed or orphan sidecar and reports every failing pack in one run. | High | Open | [build] | no — paired stale and fresh fixtures |
| FR-004 | Update mode | As a maintainer, I want an update mode that restamps stale values and creates missing sidecars, preserving comments and provenance, idempotently. | High | Open | [build] | no — must change exactly the stale files |
| FR-005 | Sidecar per pack | As a pinner, I want `packs/<name>.source.yaml` committed for all 19 current packs with fresh digests and the built-in schema (`tree_digest {algorithm: spec-kitty-snapshot-sha256, value}`, optional `seeded_from`). | High | Open | [build] | no — gate fails before the files exist |
| FR-006 | Backward compatibility | As core and kitty-stack, I want `packs/built-in.source.yaml` path and keys unchanged and `scripts/ci/built_in_digest.py` (no args → print built-in digest; `--check` → check built-in) still working. | High | Open | [ratchet] | yes — paired with FR-001's value assertion on the shim's output |
| FR-007 | Gate in required job | As the maintainer, I want the digest check as a step in the `validate` job feeding `Validate packs gate`, so no ruleset change is needed. | High | Open | [build] | no — workflow test asserts the step and its command in `validate` |
| FR-008 | Rename to cover all packs | As a reader, I want the entry script, CI step name and stale comments (built-in.source.yaml header, PROVENANCE pointers where wrong, packs/README.md) to say they cover every pack. | Medium | Open | [build] | no — grep for the old step name returns nothing |
| FR-009 | Manifest node completeness (#182 residual) | As the validator, I want every declared graph node of a non-exempt kind in a manifest-bearing pack to be a manifest constituent, with the exempt kinds named explicitly in code. | High | Open | [build] | no — negative fixture reported, positive repo passes |
| FR-010 | Unit tests | As a maintainer, I want unit tests for the digest tool (recipe vectors, discovery, check, update, shim) and for the node-completeness check, run by the existing `tests/ci` step. | High | Open | [build] | no — each test pairs a failing and passing fixture |
| FR-011 | Docs and changelog | As a contributor, I want validate-a-pack and contributing guides describing the gate and update command, and a `[Unreleased]` changelog entry. | Medium | Open | [build] | no — guide text names the update command |
| FR-012 | Release ships sidecars | As a pinner of a release, I want each pack's sidecar published next to its archive as `<pack>-vX.Y.Z.source.yaml` (bytes of `packs/<pack>.source.yaml` at the tagged commit), and the release build to fail when a released pack has no sidecar at that commit. | High | Open | [build] | no — build on a fixture tag with a sidecar emits it; without one it fails |
| FR-013 | ADR for per-pack digests | As a maintainer, I want an ADR under `docs/architecture/adr/` that extends ADR 2026-10-20-1's `tree_digest` record from built-in to every pack (fail-closed, one sidecar per pack, snapshot_sha256 recipe, shipped with releases), listed in the ADR index, with a front-matter `description` of at most 180 characters. | Medium | Open | [build] | no — index row and file must exist; description length checked |
| FR-014 | PR template reminder | As a contributor, I want the PR template's pack-change section to include a checklist line to run `python3 scripts/ci/pack_digest.py --update` and commit the sidecar(s). | Low | Open | [build] | no — template line names the command |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Speed | Check over all 19 packs completes in under 10 seconds on a CI runner. | Performance | Medium | Open |
| NFR-002 | Determinism | Two runs on the same tree yield identical digests and identical sidecar bytes after update (zero diff). | Reliability | High | Open |
| NFR-003 | Actionable errors | 100% of failure lines name the sidecar path and the exact command that fixes it, in `::error file=…::` form. | Usability | High | Open |
| NFR-004 | Dependencies | No new third-party dependency beyond python3 + pyyaml already required by CI. | Maintainability | Medium | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Recipe frozen | The snapshot_sha256 recipe is not changed (no new exclusions, no normalisation); clean-tree-sha256 is not added. | Technical | High | Open |
| C-002 | Sidecar outside tree | Sidecars live at `packs/<name>.source.yaml`, never inside the hashed directory. | Technical | High | Open |
| C-003 | No ruleset change | Enforcement stays inside the already-required `Validate packs gate`. | Business | High | Open |
| C-004 | Out of scope | Requiring the docs build; sharing the recipe with the #23 docsite; clean-tree-sha256; #124; #37; #195. | Business | High | Open |
| C-005 | Charter alignment | Repository aligns to spec-kitty-charter; core loading compatibility does not block pack work, but the built-in sidecar stays readable by core (FR-006). | Technical | Medium | Open |
| C-006 | Generated docs untouched by hand | Any change to `docs/packs/` comes from the generator only. | Technical | Medium | Open |

### Key Entities

- **Pack directory**: `packs/<name>/` with `pack.yaml`; the unit hashed.
- **Sidecar**: `packs/<name>.source.yaml`; holds `tree_digest {algorithm, value}` and optional `seeded_from {repository, path, commit, date}`.
- **Manifest**: `packs/<name>/pack-manifest.yaml`; constituents `{kind, id, path, content_hash}`.
- **Declared graph node**: a `(kind, id)` from root `*.graph.yaml` or `drg/fragment.yaml`.

## Decisions (operator, recorded — not open)

1. Per-pack sidecar `packs/<name>.source.yaml`, built-in schema, outside the hashed tree.
2. snapshot_sha256 recipe kept exactly; generalised to any path. No clean-tree-sha256.
3. Every pack participates (19 today), discovered from `packs/*/pack.yaml`; missing or stale fails closed.
4. #182 residual folded in: node-to-constituent completeness for manifest-bearing packs; exempt kinds explicit. Derived from `validate_pack_schemas.py`'s existing `MANIFEST_CONSTITUENT_SCHEMAS` comment: `action` and `anti_pattern` are graph-only (no file); `mission_type`, `mission_step_contract` and `template` are deliberately not listed in this repository's manifests. Measured at planning time, all seven manifest-bearing packs pass with this set.
5. In scope: renames, unit tests, update mode, gate inside `Validate packs gate`, docs + changelog, built-in compatibility shim.
6. Out of scope: see C-004.
7. WPs sized for Sonnet implementation and Opus review; sequential where files overlap.
8. Author UX (operator answer, 2026-11-11): the error line names the exact `--update` command; the contributing guide and changelog say so; the PR template's pack-change section gets a checklist line (FR-014).
9. Release (operator answer): release archives ship each pack's sidecar next to the archive (FR-012). This narrows C-004's "out of scope" list only for release shipping; clean-tree-sha256 and the #23 docsite recipe remain out.
10. ADR (operator answer): a short ADR extends ADR 2026-10-20-1's `tree_digest` record to every pack and mentions release shipping; the ADR index is updated (FR-013). The earlier ADR is not edited.

## Assumptions

- Sidecar key is the pack's **directory name**, consistent with `built-in.source.yaml` (`packs/internal.source.yaml`, not `spec-kitty-internal.source.yaml`).
- `seeded_from` is optional: kept on built-in; new sidecars carry only `tree_digest` plus a generated header comment. No provenance is fabricated for packs that were not seeded.
- kitty-stack's `open-packs digest` invocation (no args) is the only external caller of `built_in_digest.py`.

## Issue Matrix

| Issue | Verdict | Note |
|-------|---------|------|
| #194 | in scope | Anchor. |
| #182 | closed; residual folded | Node-completeness check (FR-009). |
| #190 | parent | Epic. |
| #23 | related, not in scope | Docs checksum recipe stays separate. |
| #19 | related, not in scope | Docsite epic. |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 19 of 19 current packs have a fresh recorded digest and the gate passes on the branch — [build] · no-op passable: no
- **SC-002**: A one-byte change in any one pack makes the required gate fail, naming that pack — [build] · no-op passable: no
- **SC-003**: Restamping after an edit takes one command and changes only the stale sidecars — [build] · no-op passable: no
- **SC-004**: Built-in's recorded digest value is unchanged (ad8412…) and the legacy entry point prints it — [ratchet] · no-op passable: yes (paired with SC-002 on the same tree)
- **SC-005**: Removing a non-exempt node's manifest entry is reported by the validator; the current repository reports zero — [build] · no-op passable: no
- **SC-006**: A release of N packs publishes N sidecars alongside N archives; a pack without a sidecar at the tag stops the release — [build] · no-op passable: no
