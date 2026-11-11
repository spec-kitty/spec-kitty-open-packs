# Research: Per-pack digest gate

Research was completed before specify and is not redone here. The three source notes are kept
verbatim under `research/`:

- [`research/A-gate-mechanics.md`](research/A-gate-mechanics.md) — what is hashed, CI wiring and
  required checks, manifest stamping and the #182 guard, release digests, design options.
- [`research/B-consumers.md`](research/B-consumers.md) — who reads digests: spec-kitty core (pin
  file, `clean-tree-sha256` + `snapshot_sha256`), spec-kitty-charter (manifest hashes only),
  kitty-stack (`open-packs digest` runs `built_in_digest.py`).
- [`research/C-related-issues.md`](research/C-related-issues.md) — issue triage around #194.

## Key findings (summary)

1. `scripts/ci/built_in_digest.py` hardcodes `packs/built-in`; after #73 that is a shell, so no
   recorded digest covers any doctrine. No unit test exists for it.
2. The recipe (`spec-kitty-snapshot-sha256`) is core's `snapshot_sha256`: sorted POSIX paths, every
   regular file except the root `pack-manifest.yaml`, 8-byte BE length-prefixed path, 8-byte BE size,
   raw bytes; symlinks and special files refuse. It differs from the docs checksum (#23), the release
   archive `.sha256`, and the manifest `manifest_hash`.
3. The check runs in the `validate` job, which feeds the required `Validate packs gate`; ruleset
   26594729 requires only `Validate packs gate` and `Charter service validation`.
4. Seven packs carry `pack-manifest.yaml`. The file-based #182 guard (`unlisted_constituents`) is in
   place (53df95d); the node-to-constituent check is not.
5. kitty-stack calls `built_in_digest.py` with no arguments; core reads
   `packs/built-in.source.yaml`'s path and keys. Both must keep working.

## Planning-time verification (this mission)

- **Pack count**: `packs/*/pack.yaml` matches **19** directories (every directory under `packs/`),
  not ~21 as the brief estimated.
- **Sidecars are invisible to other tooling**: the docs generator, validator, charter-service check
  and release tooling enumerate pack *directories* (`iterdir()` + `is_dir()`, or `rglob` inside a
  pack), so a file at `packs/<name>.source.yaml` is not a pack and is not inside any hashed tree.
  `packs/built-in.source.yaml` already proves this.
- **Vocabulary guard** scans `git ls-files packs`, so sidecar header comments are scanned; they
  must avoid retired vocabulary (header text is fixed and short).
- **Node completeness**: `validate_pack_schemas.declared_nodes(pack_dir)` (no contract argument)
  returns `(kind, id)` from `drg/fragment.yaml` and root `*.graph.yaml`. Measured over the seven
  manifest-bearing packs with exempt kinds `{action, anti_pattern, template, mission_type,
  mission_step_contract}`: **0 missing** in every pack. Kinds seen in graphs: agent_profile,
  anti_pattern, action, asset, directive, glossary_pack, mission_step_contract, mission_type,
  paradigm, procedure, styleguide, tactic, template, toolguide.

## Decisions

### D1 — Sidecar per pack
- **Decision**: `packs/<dirname>.source.yaml`, schema of `built-in.source.yaml`
  (`tree_digest {algorithm: spec-kitty-snapshot-sha256, value}`, optional `seeded_from`).
- **Rationale**: outside the hashed tree, so the recipe's exclusion list is unchanged; core already
  knows the shape; no merge hotspot across parallel pack PRs.
- **Alternatives**: one map in `built-in.source.yaml` (conflict hotspot, wrong name); stamp in
  `pack-manifest.yaml` (12 packs have none; charter schema owns it).

### D2 — Recipe unchanged, generalised
- **Decision**: move `snapshot_sha256(root)` verbatim into `scripts/ci/pack_digest.py`;
  `built_in_digest.py` becomes a shim that imports it. No `clean-tree-sha256`.

### D3 — Every pack participates
- **Decision**: discover `packs/*/pack.yaml`; missing, stale, malformed or orphan sidecar fails.

### D4 — #182 residual: node completeness with explicit exemptions
- **Decision**: new check in `validate_pack_schemas.py`, beside `unlisted_constituents`, over
  `declared_nodes(pack_dir)` minus `MANIFEST_EXEMPT_NODE_KINDS = {action, anti_pattern, template,
  mission_type, mission_step_contract}`.
- **Rationale**: mirrors the existing `MANIFEST_CONSTITUENT_SCHEMAS` comment — `action` and
  `anti_pattern` are graph-only kinds with no file; mission types, step contracts and templates are
  deliberately not listed in this repository's manifests.
- **Alternative rejected**: deriving exemptions as "kinds without a schema in
  `MANIFEST_CONSTITUENT_SCHEMAS`" — implicit, and a new kind would be silently exempt. The explicit
  set makes an unknown kind fail closed.

### D5 — Sidecar key is the directory name
- **Decision**: `packs/internal.source.yaml`, not `spec-kitty-internal.source.yaml`.
- **Rationale**: the digest is of a directory; `built-in.source.yaml` is already keyed that way.

### D6 — Provenance for unseeded packs
- **Decision**: `seeded_from` is optional and only kept where it is true (built-in). New sidecars
  carry a short generated header comment and `tree_digest` only. Nothing is fabricated
  (charter identity discipline).

### D7 — Update preserves text
- **Decision**: `--update` rewrites only the `value:` line under `tree_digest:` by a targeted text
  substitution (no YAML round-trip), so comments and `seeded_from` survive; it creates a sidecar
  from a fixed template when missing; it refuses a malformed sidecar instead of overwriting it.

### D8 — Entry point and CI step renamed
- **Decision**: `scripts/ci/check-built-in.sh` → `scripts/ci/check-pack-digests.sh`; step
  "Check the built-in pack digest" → "Check every pack's recorded digest". Same `validate` job, so
  no ruleset change. Occurrence classification in `occurrence_map.yaml`.

### D9 — Author UX (operator answer)
- **Decision**: keep the `::error` line naming `pack_digest.py --update <name>`, the contributing guide and the changelog; add a checklist line to the pack-change section of `.github/PULL_REQUEST_TEMPLATE.md` (WP05).

### D10 — Releases ship sidecars (operator answer)
- **Decision**: `scripts/release/release_assets.py build` writes `<pack>-vX.Y.Z.source.yaml` for every released pack: the bytes of `packs/<pack>.source.yaml` read from the tagged git tree (like the archives, never the working tree). A released pack without a sidecar at the tag fails the build (fail closed, consistent with D3). The release workflow's publish step uploads `dist/*` and counts the assets, so it needs no change; the reproducibility step also compares the sidecars. Owned by the new WP06.
- **Rationale**: ADR 2026-10-20-1 says a consumer wants to pin `{tag, commit, archive_sha256, tree_digest}`; shipping the sidecar puts the tree digest in the release.
- **Alternative rejected**: embedding the digest in the `.sha256` file — it would change an existing asset's format that core reads.

### D11 — ADR (operator answer)
- **Decision**: new ADR `docs/architecture/adr/2026-11-11-2-record-a-tree-digest-for-every-pack.md` extends ADR 2026-10-20-1's `tree_digest` record from built-in to every pack (fail closed, one sidecar per pack, snapshot_sha256 recipe, shipped with releases). The ADR index gets a row. The earlier ADR is not edited (DIRECTIVE_003). Front-matter `description` stays at 180 characters or fewer (docs validator rule).

## Issue matrix

| Issue | Verdict |
|-------|---------|
| #194 | in scope (anchor) |
| #182 | closed; residual (node completeness) folded in |
| #190 | parent epic |
| #23, #19 | related; recipe not shared with the docsite |

## Supply chain

No dependency is added, upgraded or removed (python3 + pyyaml already required). DIRECTIVE_051
controls are not triggered.

## Adversarial review dispositions

**Post-spec self-check (planner).**
- Pack count: 19, not ~21. Fixed in the spec.
- Sidecars must not disturb other tooling. Verified and recorded under "Planning-time verification".
- `--update` must keep the comments. Recorded as D7.
- Vocabulary guard scans the sidecar headers. Recorded as a risk on IC-02.

**Post-tasks squad (one Opus reviewer, reviewer-renata).** All findings were folded or decided; none was dropped.

| # | Finding | Disposition |
|---|---------|-------------|
| 1 | An empty `packs/` passes once WP03 drops the built-in guard | Folded. WP01 T003 5a fails "no pack found", with a test. |
| 2 | Invalid YAML or non-UTF-8 sidecar raises a traceback | Folded. WP01 T002.4 wraps both as malformed, with tests. |
| 3 | `--update` regex misses a quoted value | Folded. Substitution must match exactly once or the sidecar is refused. Test added. |
| 4 | WP04 positive control would trip the stale-manifest check | Folded. Regenerate the hashes and assert `EXIT_OK`. |
| 5 | Whole `tests/ci` suite must stay green | Folded into WP04 DoD. |
| 6 | Real-tree test assertion too weak | Folded. Discovery must equal `glob("*/pack.yaml")`. |
| 7 | `answers.yaml` edit may need charter regeneration | Decided. Check `charter status` before and after; revert if it drifts. No regeneration. |
| 8 | FR-008 says fix PROVENANCE pointers, WP05 says never | Folded. WP05 verifies by grep and records the result. |
| 9a | Open pack PRs fail until they restamp | Operator decided (D9): error line + contributing guide + changelog, plus a PR-template checklist line (WP05). |
| 9b | Release archives do not ship sidecars | Operator decided (D10): releases ship `<pack>-vX.Y.Z.source.yaml` per pack (new WP06). |
| 9c | A directory without `pack.yaml`: should the digest gate fail it? | Decided. No. `validate-packs.sh` already refuses a pack dir with pack-level files but no descriptor. The digest gate's unit is "has `pack.yaml`". |
