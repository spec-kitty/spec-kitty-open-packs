# Researcher 4: gates, tooling and hard-coded pack lists for #73 (built-in -> built-in + foundation + writing)

Repo `/home/user/spec-kitty-open-packs` at main `5c489d6`; charter `/home/user/spec-kitty/spec-kitty-charter` at the lock pin
`fb24052d411a00ee6ed301af344c3720cd0fe725` (`charter.lock.yaml:16`). Nothing in the repo was modified. All experiments ran in
the scratch dir `/tmp/claude-0/-home-user-spec-kitty-open-packs/e9f46af0-8323-5c9a-a991-c6e66101578d/scratchpad/research/`
(logs in `logs/`, experimental repo copy in `exp/`, built jar in `charter-build/`).

## 0. Headline findings (things that WILL break or need deciding)

1. **`charter_service_check.py` cannot run once a second built-in-level pack exists.** `foundation` and `writing` must be
   `pack_level: built-in`, because `built-in` (level built-in) depends on them and the level rule only lets a pack depend on
   its own level or one nearer built-in (charter ADR-0048 d7 amendment, `docs/adr/0048-...md:145`). The script hard-codes one
   built-in pack: `BUILT_IN = "built-in"` (`scripts/ci/charter_service_check.py:64`), `built_in = repo / "packs" / BUILT_IN`
   (`:457`), registration root stages only it (`:381`), and it refuses unless every non-built-in pack is org/project
   (`:382-388`). The invalid-fixture roots stage only it too (`:419`, `:431`). **Reproduced:** in a scratch copy with a
   `packs/foundation` (`pack_level: built-in`) and `built-in` `depends_on` it, the check exits 2:
   `cannot run the charter service check: 6 of 7 non-built-in packs declare pack_level org or project`. Composition itself
   passed (built-in "1 dependencies resolved", foundation at level built-in).
   **Fix, verified:** treat every pack whose `pack_level` is `built-in` as the read-only base: stage them all in the registration
   and invalid-fixture roots, and exclude them from `others`. With that 8-line change (diff at
   `scratchpad/research/exp-charter_service_check.diff`) the full check is green: composition, 6 org registrations, and
   all 4 non-vacuity refusals. The unit tests in `tests/ci/test_charter_service_check.py` should get a case for "two
   built-in-level packs".
2. **`built-in::` qualifiers in org packs go stale.** 102 `built-in::` references exist: `packs/internal/drg/fragment.yaml` (62),
   `packs/event-driven/drg/fragment.yaml` (7), `packs/spdd/drg/fragment.yaml` (6), `packs/qa/drg/fragment.yaml` (3) and the
   five `packs/qa/agent_profiles/*.agent.yaml` (24). Every one that names a moved artifact must become `foundation::` or
   `writing::`. **Verified with the jar:** a stale `built-in::directive:X` (X moved to foundation) is refused by the service,
   at composition (`GET /offering` 500 `pack_reference_artifact_missing`) and at registration. The schema precheck
   (`validate-packs.sh`) does not catch it for graph edges; it does for agent-profile references
   (`profile_reference_violations`, `validate_pack_schemas.py:992`). **Also verified:** `foundation::directive:X` written in
   `spdd` (which depends only on built-in) is ACCEPTED by both the precheck and the service: the `depends_on` closure is
   transitive (spdd -> built-in -> foundation), so the org packs do not need `foundation`/`writing` added to their own
   `depends_on`. Also `docs/guides/compose-packs.md:91` shows `built-in::tactic:bdd-scenario-formulation` as an example.
3. **"Rename `missions/` to `mission_types/`" (from the #73 2026-11-08 body) conflicts with the pinned contract.**
   `contracts/packs/file-kinds.yaml:261-264` puts `*/mission_types/*.yaml` and `*/missions/mission_types/*.yaml` under
   `retired:` ("the mission-type file moved to missions/<id>/<id>.mission-type.yaml (ADR-0044)"); the precheck reports a
   retired-layout file as a violation (`validate_pack_schemas.py:745-747`). Keep `missions/<id>/<id>.mission-type.yaml` at
   this pin. The 2026-11-09 re-scope of #73 does not repeat the rename.
4. **Sibling rule.** Two packs of the same level that declare the same id get the service's `pack_sibling_conflict`.
   The precheck's "declared by packs of different levels" check (`validate_pack_schemas.py:1130-1141`) does not fire across
   built-in/foundation/writing (same level), so an artifact left in both is caught only by the service job. Move, never copy.
5. **The docs site cannot be built here**: `npm ci` needs a GitHub Packages token for `@spec-kitty/doc-toolkit`
   (`E401 ... npm.pkg.github.com`; the session's `GH_TOKEN` is invalid). It must be left to CI (`Docs site` workflow), which
   is path-filtered and not required.

## 1. Gate list, exact commands, and results on main

CI: `.github/workflows/validate-packs.yml`. Job `validate` (`:43-90`) + job `charter-service` (`:96-135`), summarised by the
one required check `Validate packs gate` (`:139-195`). `release.yml:28-35` calls the same workflow. `docs-site.yml` is separate
and path-filtered (`:8-28`).

Environment setup I needed locally:
- The precheck fetches the contract from `raw.githubusercontent.com/spec-kitty/spec-kitty-charter/<pin>/contracts/packs`
  (`validate_pack_schemas.py:171-198`); from this container it answers **404** (private repo / no token), so every
  schema-using step fails closed (exit 2), and `gen_pack_reference.py --check` reports drift on all six pages (validation
  status renders as unavailable). Fix: `export CHARTER_CONTRACT_DIR=/home/user/spec-kitty/spec-kitty-charter/contracts/packs`
  (the charter checkout is at the pin). `GITHUB_TOKEN` is also honoured (`:174-176`).
- The asset scanner tests need `tree-sitter==0.25.2 tree-sitter-java==0.23.5` (CI installs them, `validate-packs.yml:54`); absent,
  14 of 21 tests skip. I installed them into a scratch venv.

| Gate (CI step) | Command (repo root) | Result on main | Time |
|---|---|---|---|
| Validate packs (`:60-61`) | `CHARTER_CONTRACT_DIR=... scripts/ci/validate-packs.sh` | pass (7 packs + cross-pack 0 violations; both invalid fixtures behave) | 12.8 s |
| Built-in digest (`:62-64`) | `scripts/ci/check-built-in.sh` | pass (`3b7c06d4...45d5`) | 0.1 s |
| Vocabulary guard (`:65-70`) | `python3 scripts/ci/check_vocabulary.py` | pass, 676 files, 0 findings | 0.8 s |
| Generated pages (`:71-75`; also `docs-site.yml:390-410`) | `CHARTER_CONTRACT_DIR=... python3 scripts/docs/gen_pack_reference.py --check` | pass, 6 pages | 4.2 s |
| Release tooling tests (`:76-78`) | `python3 -m unittest discover -s tests/release` | 8 OK | 0.3 s |
| Vocabulary tests (`:79-81`) | `python3 -m unittest discover -s tests/vocabulary` | 12 OK | 0.1 s |
| Pack validator tests (`:82-84`) | `CHARTER_CONTRACT_DIR=... python3 -m unittest discover -s tests/ci` | 91 OK | 3.3 s |
| Page generator tests (`:85-87`) | `python3 -m unittest discover -s tests/docs` | 12 OK | 0.6 s |
| Test-quality scanner tests (`:88-90`) | `python3 -m unittest discover -s tests/assets` (with tree-sitter) | 21 OK | 0.1 s |
| Charter service (`:96-135`) | `jar="$(scripts/ci/charter_service_jar.sh <work>)"; JAVA_HOME=<jdk25> python3 scripts/ci/charter_service_check.py --jar "$jar"` | **pass**: composition 7 packs, 6 registrations, 4 refusals | 36 s (+5 min 21 s jar build) |
| Docs site build (`docs-site.yml:339-388`) | `cd site && npm ci && npm run validate && DK_PUBLISH_DRAFTS=on DK_DIAGRAM_BUILD_RENDER=client npm run build` (Node 22) | **blocked**: E401 from npm.pkg.github.com | n/a |

Note there is no single `python3 -m unittest discover` over `tests/`: CI runs each of the five suite directories separately.

### charter_service_check.py details

- **How it picks packs:** `pack_dirs(repo/"packs", repo/"tests/fixtures/valid")` (`:455`): every directory under `packs/`
  and the valid fixture; invalid fixtures from `tests/fixtures/invalid` (`:456`). New packs are picked up **automatically**
  for composition. Registration and fixture roots use the single hard-coded `packs/built-in` (see finding 1).
- The offering is keyed by **directory name** (`offered.get(pack.name)`, `:362`), `depends_on` is checked by
  `descriptorPackId` (`:368-371`), and `pack_level` in `pack.yaml` must equal the offering's level (`:366-367`).
- `read_descriptor` is a line reader (`:94-121`), not YAML: `depends_on` entries must be written `- pack_id: <ULID>` on
  their own line (as all packs do today) or the registration order (`:330-347`) will not see them.
- `NOT_REGISTERED` (`:78-84`) leaves `README.md`, `PROVENANCE.md`, `org-charter.yaml`, mission template notes out of the
  upload; any other unmodelled file in an org pack fails registration. Built-in-level packs are never uploaded (only staged).
- **Needs:** Java **25** (CI `setup-java` 25, `validate-packs.yml:116-119`; the charter build uses a Java 25 toolchain,
  `build-logic/.../charter.java-base.gradle.kts:10`, `gradle.properties: org.gradle.java.installations.auto-download=false`).
  The container's default `java` is 21, but `/usr/lib/jvm/temurin-25` exists: use `JAVA_HOME=/usr/lib/jvm/temurin-25`.
  `release_tag` is empty in the lock, so the jar must be built from the pinned commit with
  `./gradlew :deployable:bootJar` (`charter_service_jar.sh:21-49`), which needs network to github.com (fetch) plus
  services.gradle.org / plugins.gradle.org / Maven Central. Here: I skipped the fetch by copying the local charter checkout
  (already at the pin) to scratch and building there. First attempt failed in 33 s with HTTP **429** from
  repo.maven.apache.org (rate limit, via the proxy); the retry succeeded in 5 min 21 s. Jar:
  `scratchpad/research/charter-build/spec-kitty-charter/service/deployable/build/libs/deployable-0.1.0-SNAPSHOT.jar`
  (reusable by the implementer: `JAVA_HOME=/usr/lib/jvm/temurin-25 python3 scripts/ci/charter_service_check.py --jar <that>`).

## 2. Pack-manifest regeneration and the built-in digest

- **Manifest tool:** `python3 scripts/ci/validate_pack_schemas.py --regenerate-manifest packs/built-in`
  (`validate_pack_schemas.py:369-400`, CLI `:1187-1190`, `:1203-1214`; documented in `docs/contracts/index.md:65`). It is
  **not** a spec-kitty CLI command. It restamps `content_hash` and `manifest_hash` only, **membership is kept**: a listed path
  that no longer exists refuses the write (exit 1, nothing written). The validator flags a stale hash or missing file as a
  violation (`:802-808`). So when built-in loses ~all its artifacts, its `constituents` entries must be removed (and the
  new packs' entries created) by hand or by a new tool. No tool derives membership today; this is exactly the #182 gap.
  The spec-kitty CLI (4.0.0rc9) has `charter pack validate|assemble|regenerate-graph|vendor`, none of which writes this
  manifest; `pack.yaml:4-6` / `pack.md:12-16` cite core's `tests/architectural/test_pack_manifest_no_author_edit.py`, a core
  rule.
- Current manifest: 310 constituents (tactic 120, procedure 65, directive 38, styleguide 27, agent_profile 26, toolguide 18,
  paradigm 9, asset 6, glossary_pack 1) + presets `default`, `minimal`.
- **Is a manifest required?** No. The charter makes it optional (ADR-0042: "A pack ... with no presets and no manifest keeps
  its exact digest list", `docs/adr/0042-...md:373`, `:387`; the internal pack holds none, `:490`), and every org pack here
  has none. The precheck only verifies one when present. Whether `foundation`/`writing` carry one is a choice; if `built-in`
  keeps only presets, its manifest becomes `constituents: []` + presets (schema allows; `constituents` is required, see the
  `manifest_hash` recipe `:321-337`). Recommendation: if #182's guard lands, give `foundation`/`writing` manifests too so the
  guard covers the content that left built-in.
- **Digest:** `scripts/ci/built_in_digest.py` reimplements core's `snapshot_sha256`: SHA-256 over every regular file of
  `packs/built-in/` except top-level `pack-manifest.yaml`, sorted by POSIX path, each as 8-byte BE path length + UTF-8 path +
  8-byte BE size + bytes; symlinks/special files refuse (`:25-41`). Print: `python3 scripts/ci/built_in_digest.py`; record as
  `tree_digest.value` in `packs/built-in.source.yaml:19-21`; verified by `scripts/ci/check-built-in.sh` ->
  `built_in_digest.py --check` (`:43-56`). Paths `BUILT_IN`/`SOURCE` are hard-coded (`:22-24`). It covers only
  `packs/built-in`; nothing digests `foundation`/`writing`. Extending to a `<pack>.source.yaml` per built-in-level pack is
  optional here (core's pin is out of scope per AGENTS.md); at minimum the built-in digest must be re-recorded after the split.

## 3. Issue #182 (the guard to land)

- **Defect (still present at 5c489d6):** `procedures/git-flow.procedure.yaml` and `toolguides/execution-lanes.toolguide.yaml`
  are not in `packs/built-in/pack-manifest.yaml` (lost in `a6e11d9`, `7174cc9`). No comments on the issue.
- **Asked for:** (a) regenerate the manifest to add `{kind: procedure, id: git-flow}` and `{kind: toolguide, id: execution-lanes}`;
  (b) **a CI guard: every authored constituent file of a doctrine kind in a pack is listed in that pack's manifest, and every
  graph node has a manifest constituent.** Out of scope: step contracts, mission types, presets, `assets/docs_structural_lint.config.yaml`
  are intentionally not listed ("please confirm").
- **Prototype result over built-in today:** files not listed = the 2 above + 21 step contracts + 4 mission types +
  `assets/docs_structural_lint.config.yaml`. Graph nodes (398) with no constituent: template 24, action 24,
  mission_step_contract 21, anti_pattern 13, mission_type 4, plus the 2 above. Templates and anti-patterns have no doctrine
  file of their own, so "every graph node" must be scoped to the file-backed doctrine kinds (directive, tactic, styleguide,
  toolguide, paradigm, procedure, agent_profile, glossary_pack, skill, asset) or the guard is red on day one.
- **Where:** inside `validate_pack()` in `scripts/ci/validate_pack_schemas.py`, next to the stale-manifest check (`:802-808`),
  applied to any pack that has a `pack-manifest.yaml` (so it runs from `validate-packs.sh` for built-in and, after the split,
  for foundation/writing if they get manifests). Node ids come from the built-in `*.graph.yaml` shards / `drg/fragment.yaml`
  (`declared_nodes`, `:843`). Better still, extend `--regenerate-manifest` to derive membership from the files with the same
  kind mapping, so the fix and the guard share one rule and the split can regenerate manifests instead of hand-editing them.
- **How to test:** unit tests in `tests/ci/test_validate_pack_schemas.py`, reusing `write_pack`/`manifest_pack` (around
  `:110-215`): an unlisted `tactics/x.tactic.yaml` is a violation; a graph node of a doctrine kind without a constituent is a
  violation; step contracts / mission types / templates are not. An invalid fixture under `tests/fixtures/invalid/` is NOT
  suitable: each needs an `expected-code` the charter service refuses with (`charter_service_check.py:133-155`), and the
  service does not refuse an incomplete manifest. Then run `validate-packs.sh` to show it red on main (the 2 files) and green after.
- The guard belongs in the same PR as, or before, the split, since the split rewrites every manifest.

## 4. Hard-coded pack list / built-in path: what to update

Picked up automatically (no change): `validate-packs.sh:41` (`find packs ... -maxdepth 1`), `charter_service_check.py:455`
composition, `gen_pack_reference.py` `discover_packs` (built-in first, rest sorted), `release_assets.py:55-68` `list_packs`
(every dir under `packs/` gets an archive), `tests/ci/test_graph_edge_identity.py:17-34` (iterates `packs/*`),
`check_vocabulary.py:148-151` (all `git ls-files packs` text files: **new files must be git-added** to be scanned; it crashes
outside a git checkout), `docs-site.yml` paths (`packs/**`).

Must change:
| Place | What |
|---|---|
| `scripts/ci/charter_service_check.py:64, :379-388, :419, :431, :457-459` | single-built-in assumption (finding 1) |
| `scripts/ci/check_vocabulary.py:75` | provenance row hard-codes `packs/built-in/procedures/test-first-bug-fixing.procedure.yaml`; if it moves the row goes stale and the guard fails (`stale_provenance`, `:143-145`) |
| `scripts/ci/check_vocabulary.py:5, :67-68` | docstring + `INTERNAL_PACK` (unaffected unless content moves to internal) |
| `scripts/ci/built_in_digest.py:22-24`, `check-built-in.sh:13`, `packs/built-in.source.yaml` | re-record digest; decide on digests for new packs |
| `tests/ci/test_language_profile_styleguides.py:14` | `BUILT_IN = packs/built-in`; reads `agent_profiles/`, `styleguides/`, `*.graph.yaml` there and `assertGreater(checked, 0)` -> **fails** if language profiles leave built-in. Point it at the packs that hold them (edges may then be cross-pack `requires`) |
| `tests/ci/test_software_dev_ascii.py:8-14` | `packs/built-in/missions/software-dev`: if missions move to foundation it **passes vacuously** (rglob of a missing dir); repoint and add a non-empty assertion |
| `tests/ci/test_prompt_fragments.py:133-170` | real `packs/spdd` must stay valid; its fragment targets `built-in::action:software-dev/specify` (`packs/spdd/drg/fragment.yaml`) -> `foundation::` if the software-dev mission moves |
| 102 `built-in::` references (finding 2) | internal, event-driven, spdd, qa fragments + 5 qa agent profiles |
| `packs/README.md:3-6, :29-33` | pack list, "the exception is built-in/" text |
| `README.md:44-47, :58-64, :111` | packs table and Status row ("built-in, qa, ... exist") |
| `docs/packs/index.md:8-15 (related), :63-70 (table)` | hand-authored hub: add foundation and writing rows and `related` entries; rewrite the built-in row |
| `docs/architecture/overview.md:21-23, :41-42, :56, :89-94` | "One pack, shipped with the CLI" |
| `docs/index.md:43-57`, `docs/organisations/index.md:21, :71-72`, `docs/contracts/index.md:31, :48-65`, `docs/guides/compose-packs.md:25-33, :72, :80, :91`, `docs/guides/validate-a-pack.md:66, :76-78, :95`, `docs/glossary/index.md` | built-in descriptions; validate-a-pack:95 describes "a scratch root holding only built-in" |
| `.kittify/charter/charter.md:9-12` | lists packs (`built-in, cave-kitty, event-driven, qa`) |
| `docs/changelog/CHANGELOG.md` (root and `.github/` are symlinks) | Unreleased entry (Breaking) |
| `.github/workflows/validate-packs.yml:62-64` | step name "Check the built-in pack digest" (only if digest is extended) |

Not to change here: `.kittify/charter/charter.yaml:414+` `source_path: ${SPEC_KITTY_PACKS_ROOT}/built-in/...` is generated by
the core CLI for this repo's own governance (core compatibility is out of scope). Downstream: charter's nightly `driftTest`
round-trips every open-packs pack, and its `openPacksRef` pin (`gradle.properties`) controls when charter sees the split; the
`wholePackRoundTrip` gate reads "the pinned built-in pack" (`service/packs/build.gradle.kts:113-130`); not a gate here.

## 5. Generated docs pages

- `gen_pack_reference.py` writes `docs/packs/<dir-name>.md` for every directory under `packs/` (`discover_packs`), so
  `foundation.md` and `writing.md` appear automatically. Verified in the scratch copy: a page was produced with validation
  "passing". Run `CHARTER_CONTRACT_DIR=... python3 scripts/docs/gen_pack_reference.py` (write) and then `--check`.
- For a full page a new pack needs: `pack.yaml` (version + `depends_on`; the page prints `depends_on` as the **pack_id ULID**
  plus range, not the name), and a `pack.md` whose preamble becomes "Purpose" (otherwise the page says no purpose is declared).
  Slugs `index` and `catalog-proposal` are reserved (`RESERVED_SLUGS`).
- The `built-in.md` page and every org-pack page (`depends_on` unchanged, but checksum changes when their `built-in::` refs
  change) are rewritten; commit all regenerated pages in the same change or the drift step fails. Orphaned pages are detected.
- Nav: `docs/_meta/sections.yaml` is folder-level (section `packs`, `:9-13`), so no nav entry per page is needed. Update the
  hand-authored hub `docs/packs/index.md` (related list + table). `docs/packs/catalog-proposal.md` is the forward-looking
  catalog, worth a note that foundation/writing are now materialized. `site/astro.config.mjs` needs no change.

## 6. Minting pack_ids

- There is no spec-kitty CLI command that mints a `pack_id` (`charter org init` scaffolds org-charter/drg/presets/README, no
  `pack.yaml`). The "tool-minted" ids in this repo come from the snippet in
  `kitty-specs/strict-pack-composition-01M6M0W4/tasks/WP02-pack-identity.md:81-93` (T006): a ULID from `time.time()*1000`
  ms << 80 | 10 random bytes, encoded in Crockford base32 (`0123456789ABCDEFGHJKMNPQRSTVWXYZ`), 26 chars, "never typed by
  hand, never reused from a research scratch copy". Check after: valid, unique, `git grep` finds each only in its own descriptor
  (`:140`). The descriptor schema requires a ULID (`contracts/packs/schemas/pack-descriptor.schema.json` `$defs/Ulid`) and a
  `name` matching `^[a-z0-9][a-z0-9_-]*$` (the `<name>::` qualifier, so `foundation` and `writing`, ADR-0053 d9).
- `built-in` keeps `01ARWG13C000000000000000FG` (ADR-0048 d12). The experimental id I minted in scratch
  (`01M75GKVBCWZSWZCZR1WCY3E37`) must NOT be reused.
- New descriptors: `schema_version: "1.0"`, `pack_version: 1.0.0`, `parent_pack: null` (roots, ADR-0048 d15),
  `pack_level: built-in`, `name`, and `pack_drg: drg/fragment.yaml` if they use a fragment rather than `<kind>.graph.yaml` shards
  (both forms are mapped by `file-kinds.yaml:123-126`; the scratch foundation pack used a fragment and composed). `pack_level`
  is required whenever `depends_on` is non-empty (ADR-0053 d8).
