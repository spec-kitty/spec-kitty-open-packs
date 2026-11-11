# #194 gate mechanics (read from origin/main faa4770; local main is 7 commits behind but the gate files are identical)

Paths are relative to the repo root. Line numbers are from origin/main.

## 1. What is hashed

scripts/ci/built_in_digest.py
- :29-42 `snapshot_sha256(root)`. Algorithm is core's `spec-kitty-snapshot-sha256`, reimplemented (:4-8).
  - Walks `root.rglob("*")`, sorted by POSIX relative path (:31).
  - A symlink raises (:33-34). A directory is skipped (:35).
  - The top-level `pack-manifest.yaml` is excluded. The check is `relative == "pack-manifest.yaml"`, so it applies to the root manifest only (:26, :35).
  - Any non-regular, non-dir entry raises (:37-38).
  - Per file: `len(path_utf8)` as 8-byte big-endian, then the path, then `size` as 8-byte big-endian, then the raw bytes (:39-41). Bytes are raw, with no CRLF normalisation. Paths are root-relative POSIX, UTF-8.
  - Dotfiles and everything else are included. There is no other exclusion list.
- :23-25 constants. `BUILT_IN` and `SOURCE` are hardcoded; there is no pack parameter.
- :45-59 `main()`. With no flag it prints the digest. With `--check` it compares to `yaml.safe_load(SOURCE)["tree_digest"]["value"]` (:52). On mismatch it prints a `::error file=packs/built-in.source.yaml::` line and returns 1.
- The script needs pyyaml. There is no unit test for it: tests/ci has no test file touching `built_in_digest`.

scripts/ci/check-built-in.sh:14-16
- Only checks that `packs/built-in/pack.yaml` exists, then runs `built_in_digest.py --check`.
- The header (:2-6) says it checks "the built-in pack".

packs/built-in.source.yaml (22 lines)
- Schema:
  - `seeded_from{repository, path, commit, date}` (:10-14). This is history only (:7-8).
  - `tree_digest{algorithm: spec-kitty-snapshot-sha256, value: <hex>}` (:20-22).
- The recorded value, ad841252..., equals the actual digest of `packs/built-in/` today.
- Readers:
  - `built_in_digest.py:52`, reading `tree_digest.value` only.
  - Core CLI reads it as its pin file. Core has its own `packs/built-in.source.yaml` which pins a commit of this repo (docs/architecture/overview.md:23, :90-96; the file's own header :3-5).
  - Prose references only: docs/guides/validate-a-pack.md:76-77, docs/architecture/overview.md, packs/README.md:47-48, each `packs/*/PROVENANCE.md:10` ("see packs/built-in.source.yaml"), ADR 2026-10-20-1 :74-76, ADR 2026-10-26-1 :55, CHANGELOG.
  - The docs generator does NOT read it. `scripts/docs/gen_pack_reference.py` has its own checksum (see below).
  - No test reads it. `tests/ci/test_workflows.py` does not mention built-in or digest.
- Staleness: the file's comment (:15-17) still says built-in "depends on foundation and writing". It now has six members. docs/architecture/overview.md:23 does list all six.

The digests that exist today, computed with the same recipe (none of them recorded anywhere except built-in):

| pack | tree digest |
|---|---|
| built-in | ad841252089ca5cdc5da33d7a027fb34386a80fe64249c1e368e61162dea38ca (recorded) |
| foundation | 2eb56e07337f3173ec6997700eebc784c14da4a83510a39efe64b6f3d50523ac |
| writing | 4a6c98a3e84865a135c8d7f8e12d215731d5fa0d881a6a9818ba6353e459223c |
| testing | 6c0f6937b512b705b5c0bb0e8aa96313679fee0b7a51cc895c017cf94300354d |
| refactoring | ccebe0fb1a29a0078557b36c6c1c28627b1a48a445148b22a2d0dba891d1f786 |
| architecture | f48f6fe54ffe797410e2dad5e4a8af05ad7be39681f9f74624fd2f8b04a268c5 |
| planning-analysis | 3cfd9d886fbd74a78f65bf8dbc90b077acd445d8ce6f292593d4caa76ce051b5 |

Two other hash recipes in the repo (all different, so they are not interchangeable):
- Docs generator `compute_checksum` (scripts/docs/gen_pack_reference.py:293-309, `_pack_files` :286-290):
  - sha256 over `relpath + NUL + bytes + LF`, for every regular file including `pack-manifest.yaml`.
  - Shown on each generated pack page (:522-524) as the "Content checksum".
  - ADR 2026-07-18-3 is "Proposed" and calls it interim. Issue #23 is OPEN.
- Release archive digest (scripts/release/release_assets.py:153-154): sha256 of the .tar.gz, written to `<pack>-vX.Y.Z.tar.gz.sha256`.

## 2. CI wiring and required checks

- .github/workflows/validate-packs.yml:
  - Job `validate`, named "Charter Pack validation" (:43-44). The step "Check the built-in pack digest" is at :62-64, with `if: !cancelled()`, running `scripts/ci/check-built-in.sh`.
  - Job `charter-service`, named "Charter service validation" (:96-98).
  - Job `gate`, named "Validate packs gate" (:139-141), with `needs: [validate, charter-service]` and `if: always()`. It fails unless both are `success` (:175-195).
  - Triggers (:14-22): PR, push to main, workflow_dispatch, workflow_call.
- Ruleset 26594729 ("main", active, target branch, include ~DEFAULT_BRANCH):
  - Rules: deletion, non_fast_forward, required_linear_history.
  - pull_request with 0 required approvals.
  - required_status_checks, `strict: false`, with exactly two contexts, "Validate packs gate" and "Charter service validation" (integration 15368).
  - Charter service validation is also a job that `gate` needs.
  - "Charter Pack validation" is not listed itself; it is required only transitively through the gate.
- Not required:
  - Docs site `build` (docs-site.yml:54), `drift-gate` (:105) and `deploy` (:127). It is path-filtered (:23-43), so it cannot be required (docs/guides/contributing.md:92-93).
  - The internal docs `drift-gate` job is not required either, but `gen_pack_reference.py --check` is duplicated in the required gate (validate-packs.yml:71-75).
- Evidence for the "#200 merged red" claim: `gh run list` for the Docs site workflow shows `failure` for the main push of 62e6b46 (run 43076058651) and for PR runs. The log failure is the step "Validate frontmatter and source links": "1 file(s) failed validation".
- The built-in digest check is inside the required gate. So the digest check is enforced; what slips through is the docs build.
- Release: .github/workflows/release.yml:33-40 calls validate-packs.yml (the same gates) before :42-90 builds archives for every pack under packs/. See section 4.

## 3. pack-manifest.yaml, stamping and the #182 guard

scripts/ci/validate_pack_schemas.py
- Manifest shape (checked in packs/foundation/pack-manifest.yaml): `schema_version`, `manifest_hash`, `constituents[{kind,id,path,content_hash}]`, optionally `presets` (:321 `MANIFEST_LISTS`).
- :325-327 `content_hash` = sha256 of the file bytes after CRLF/CR become LF.
- :330-346 `manifest_hash` = sha256 of the RFC 8785 canonical JSON of the `schema_version` + constituents + presets, with no `manifest_hash` field. It is the charter's recipe (PackManifests.canonicalJson).
- :363-375 `stale_manifest_fields`.
- :378-382 `unlisted_constituents` is the #182 completeness guard (:68-76 the schema set `MANIFEST_CONSTITUENT_SCHEMAS`). It is invoked at :824-835 and reports "stale manifest" and "incomplete manifest".
- :385-409 `regenerate_manifest` restamps every `content_hash` plus `manifest_hash`, and keeps membership. The CLI flag is at :1211. REGENERATE_COMMAND is at :77.
- Which packs have a manifest:
  - Present: architecture, built-in, foundation, planning-analysis, refactoring, testing, writing.
  - Absent: cave-kitty, drupal, event-driven, go, internal, java, javascript, pack-authoring, python, qa, rust, spdd.
  - built-in's manifest is empty (`constituents: []`, manifest_hash 287713e4...).

Overlap with the tree digest
- The manifest already carries per-file hashes (`content_hash`) plus an aggregate `manifest_hash`, and it is verified in the required gate.
- It is NOT the same coverage. It lists only doctrine constituents and presets. It does not list pack.yaml, pack.md, PROVENANCE.md, the graphs, the skills/templates/mission step prompts (exempt, :71-72), or the assets payloads unless they are listed. The hash is CRLF-normalised, and the tree digest is raw bytes. The tree digest also excludes the manifest itself.
- The manifest's own integrity is not in the tree digest, so a manifest edit alone does not change the tree digest. Only the archive digest covers it (ADR 2026-10-20-1 :86).
- The manifest cannot be a substitute for the tree digest: its coverage is partial and it is not generated for 12 packs.
- One mechanism for both purposes? Not as it is. The practical single mechanism is a tree-digest stamp that sits beside the manifest stamp (for example a `tree_digest` field written by the same `--regenerate-manifest` command). The stamp would be restamped by the same command and verified by the same gate. This is a design choice; the charter's manifest schema (spec-kitty-charter) may not admit extra fields. Not verified; the repo aligns to the charter. Check before adding a field.
- Alternatively keep a sidecar, so that there is no charter-schema dependency.

## 4. Release workflow and publication of digests

- release.yml:3-6: per-pack deterministic `<pack>-vX.Y.Z.tar.gz` plus `.sha256`. Core pins `{tag, commit, archive_sha256}`. The workflow runs the gates (calls validate-packs.yml, which includes the built-in digest step) first. Archive reproducibility is checked at :68-72.
- release.yml publishes NO `tree_digest` for any pack, and no per-pack source file. ADR 2026-10-20-1:31 says a consumer "wants to pin `{tag, commit, archive_sha256, tree_digest}`". :74-76 records `tree_digest` only for `built-in`, in `packs/built-in.source.yaml`. The ADR "Which digest proves what" (:66-80) is the existing doctrine on this. The ADR text is stale on built-in: since #73 the digest proves only the shell.
- ADR 2026-07-18-3 (build-time checksum, Proposed) is a docs-side display. It is not a published digest (the docs pages carry it but nothing in the release does). Issue #23 (OPEN) wanted `docs/packs/reference/checksums.json`, a published recipe and docs/security/pack-trust-model.md. Not delivered per the repo listing: `docs/packs/reference` does not exist at origin/main, and no pack-trust-model was found under docs/security.
- scripts/release/release_assets.py does not read the source file and has no digest-over-tree logic.

## 5. Design options for #194

The facts that matter:
- Seven packs have manifests: six built-in members and the shell. The org packs have no manifest and no digest.
- The built-in shell is `depends_on` the six members with `==` pins (packs/built-in/pack.yaml:19-34).
- Core pins `packs/built-in/` by digest and needs member digests when it aligns (#194 body). Core compatibility is explicitly not this repo's concern (AGENTS.md alignment).
- The recorded value is hand-edited. The only tooling is `--check`, with no regenerate step.

### A. Where digests are recorded
1. One source file listing all packs (extend `packs/built-in.source.yaml`, e.g. a `members:` map {pack: digest}).
   - Pro: one place to diff and bump. It matches core's single pin file. It is the smallest change.
   - Con: every member edit touches a file outside the pack, which gives merge conflicts across parallel PRs (the repo's pack work is already parallel, e.g. #191/#192 PRs). It is not self-describing per pack. The filename is wrong for a multi-pack list.
2. A per-pack digest file (`packs/<p>/pack.digest.yaml` or similar), for built-in-level packs only or for all packs.
   - Pro: the pack is self-contained. It is archived with the pack. The edit and its digest are in the same directory. A generic `--check` can iterate.
   - Con: the file lives inside the hashed tree, so it must be excluded (as `pack-manifest.yaml` is) or it is self-referential; this changes the recipe's exclusion list, and core's algorithm excludes only the manifest, so core's digest would differ unless the file is named like the manifest or lives outside the pack. Also 12-19 new files if applied to all packs.
3. Stamp the digest into `pack-manifest.yaml` (see section 3). Pro: no new file, and it is already excluded from the tree digest. Con: charter schema and core compatibility unknown; 12 packs have no manifest.
   - Alternative that avoids the self-reference: a sidecar at `packs/<p>.source.yaml` (the existing `built-in.source.yaml` pattern, generalised). The digest stays outside the tree, no recipe change, and it matches what core already knows. Cost: one extra file per pack beside the dir.

### B. Check logic
1. Generic `pack_digest.py --check` over every pack that has a recorded digest (or a manifest), with `--update` to restamp.
   - Pro: one code path, the recipe tested once, a regenerate command that removes the hand-copying (today's error message tells people to copy by hand). Easy to unit test (currently none).
   - Con: policy question of which packs participate. If every pack with a manifest, the 12 manifest-less packs are not covered. If every pack, every content edit needs a restamp (more friction, but `--update` is one command).
2. Keep built-in special-cased and add members to a list.
   - Pro: smallest diff, matches the issue's "built-in, foundation, writing" scope. Con: leaves the org packs and the next pack unprotected, and a hardcoded list drifts (the issue is itself the symptom: the list was written for one pack and the pack was split).
   - A middle way: generic mechanism, with the set of participating packs derived (pack_level in {built-in}, plus the closure of built-in's `depends_on`) rather than hardcoded.

### C. Should built-in's digest be a closure digest?
- Today built-in's digest is stable across member changes, so a pin by built-in's digest alone no longer proves any doctrine. That is the problem #194 describes.
- A closure digest over (built-in tree + each member's tree digest, in pinned-dependency order or sorted by pack id) would make one value identify the full distribution.
  - Pro: one pin value covers all content; a member edit forces a visible change to built-in's recorded value (so a version bump discussion happens).
  - Con: it is a new recipe that core does not know (core's `snapshot_sha256` is not this); every member edit changes built-in's value and so churns `built-in.source.yaml`; redundant if per-member digests are also recorded.
- Alternative: record per-member digests and leave built-in's own digest as the shell. Core resolves the closure through `depends_on` `==` pins. It needs no new recipe, and the members' versions are already exact-pinned.
- The two are compatible: record member digests (needed anyway) and optionally derive a closure value from them later.

### Recommendation
1. Generalise `built_in_digest.py` into a pack-parametrised `pack_digest.py` (keep the recipe verbatim: same exclusions and ordering, so core's algorithm still matches) with `--check` (all participating packs) and `--update` (restamp).
2. Record the digests in a sidecar per pack, in the existing `packs/<name>.source.yaml` pattern (or one map in `built-in.source.yaml`), outside the hashed tree, so the exclusion list is unchanged. The one-file option is simpler to ship now. The per-pack sidecar is better once the org packs join and when parallel PRs conflict. This is a close call; pick one-file if only the 7 built-in-level packs join, per-pack if all packs do.
3. Participation is derived: the shell plus the closure of its `depends_on` pins, with every other pack opt-in or covered once it has a sidecar. Do not add a closure-digest recipe now. Core's own request is "per-member digests".
4. Keep `scripts/ci/check-built-in.sh` as the CI entry point, renamed or reworded to say what it covers. It stays inside the required `validate` job, so no ruleset change is needed.
5. Add a unit test (none exists today) plus a test_workflows-style guard that the step is in `validate`.
6. Separately: the docs `build` job failure is not touched by this. Requiring it would need the path-filter problem solved (a required check that never starts blocks the PR), per validate-packs.yml:3-6 and contributing.md:92-93. That is a different issue.
