# Researcher 3: consumers, dependents, release and breaking-change impact of the built-in split (#73)

Read-only research. open-packs `main` @ `5c489d6`; charter @ lock pin `fb24052` (`charter.lock.yaml:68`); core source `/opt/spec-kitty` @ `2e9ca559` (4.0.0rc9).

## 0. Target shape, per the accepted charter records

- `built-in` becomes a **distribution pack**. It keeps `pack_id 01ARWG13C000000000000000FG` and `pack_level: built-in`, **holds no artifacts of its own**, aggregates its members through `depends_on`, and keeps the `default`/`minimal` presets (ADR-0048 d12, `docs/adr/0048-...md:168-170`). The phrase "minimal offering" in the issue title means the presets plus the descriptor fields (`fallback_profile`, `mutability_policy`). It does not mean leftover artifacts.
- Members are `foundation` and `writing` (ADR-0053 d3 `:91`, d9 `:115`). Each is a top-level pack (ADR-0048 d11 `:166`) and a root with `parent_pack: null` (d15 `:177`). Members version separately, release in lockstep, and `built-in` pins their exact versions (d17 `:182-184`).
- **Level rule:** a pack may depend only on packs at its own level or one nearer built-in (ADR-0048 d7 amended, `:145`; resolver `PackCompositionResolver.java:879-893`, `LEVEL_VIOLATION`). Because `built-in` depends on them, **`foundation` and `writing` must be `pack_level: built-in`**. Several findings below follow from this.
- Stack/topical packs are opt-in `org` packs (ADR-0048 d14; ADR-0053 d1). They are not part of #73.

## 1. How core consumes built-in today, and what it would see after the split

**Mechanism: fetched by commit pin. Core keeps no vendored copy in git.**
- Pin: `/opt/spec-kitty/packs/built-in.source.yaml:5-13` pins `repository`, `commit a79c36318b…`, `subtree: packs/built-in` and a `clean-tree-sha256` digest. The commit is open-packs tag `core-rc8-glossary-6562` (from `git ls-remote`), which predates `pre-charter-cutover`. Core uses its own digest algorithm. It does not read open-packs' `packs/built-in.source.yaml` (`spec-kitty-snapshot-sha256`, `packs/built-in.source.yaml:16-19`); the header comments on both sides describe the two opposite anchors.
- Fetch: `make sync-packs` runs `scripts/sync_packs.py --pack all` (`Makefile:15-16`). `PACK_NAMES = ("built-in", "internal")` (`scripts/sync_packs.py:31`). It fetches only the pinned `subtree` (`src/charter/offering/packs/pack_fetch.py:137-185`, `fetch_commit_subtree`) and checks the digest (`:112`, `:154`).
- Packaging: only `packs/built-in` is force-included in the wheel, after the hatch hook verifies it (`pyproject.toml:212-229`). `test_packaging_safety.py` guards this.
- Loading: one tree. `resolve_pack_root("built-in")` → `built_in_root()` → `built_in_dir(kind) = root / kind.plural` (`src/charter/offering/pack_paths.py:144-200`). Core has no `depends_on` resolution. `PackDescriptor` is `extra="forbid"` and has no `depends_on`, `fallback_profile`, `mutability_policy` or `schema_version` (`src/charter/offering/packs/pack_descriptor.py:88-125`). The digest step itself loads the descriptor (`pack_clean_digest.py:121`), and so does `charter pack vendor` (`pack_vendor.py:127`).
- Identity: `_BUILTIN_PACK_ID = "01ARWG13C000000000000000FG"` is hard-coded (`src/charter/offering/drg/org_pack_config.py:84`, used at `:1026`) and bound to `pack.yaml` by core's `test_pack_id_identity.py`. Keeping the id, as d12 requires, keeps this binding.
- Fallback: core hard-codes `GENERIC_AGENT_ID = "generic-agent"` for the empty-charter route (`src/specify_cli/invocation/empty_charter.py:55,112`). It does not read `fallback_profile`.
- Command templates and step contracts load from `packs/built-in/missions` (`pyproject.toml:175`).

**Today's state.** Current open-packs `main` already cannot be loaded by core. `packs/built-in/pack.yaml:10,17,18` carries `schema_version`, `fallback_profile` and `mutability_policy`, and core's closed model refuses them. Even the digest step that `sync-packs` runs refuses them. The org packs also carry `depends_on`, which core refuses (open-packs ADR 2026-11-04-1 `:131-134`).

**After the split, if core fetched only `packs/built-in` at a new pin.** Assuming core first learned to parse the descriptor, its tree would contain only `pack.yaml`, `pack.md`, `presets/`, `policy.yaml` (and possibly a graph shard). It would lose every `agent_profiles/*` (generic-agent, **implementer-ivan**, reviewer-renata, …), all four mission types with their step contracts and command templates, directives, tactics, glossary, templates and assets. `built_in_dir(kind)` would point at missing directories. The empty-charter route would pin a `generic-agent` that no longer exists. So yes, implementer-ivan and every other profile disappear for core. ADR-0048 Consequences (`:214-223`) list the core work this needs: sync every member at one pin with per-tree digests, widen the wheel include and amend core ADR 2026-08-16-3, and add an upgrade step with a doctor warning. Per AGENTS.md this is **not** this repository's concern and must not block #73; #73 item 3 was explicitly scoped out on 2026-11-09. Recommendation: say this in the 💥 entry and the ADR, as the SPDD and #118 entries did. No released core is affected unless core bumps its pin.

## 2. How the charter service consumes packs: before and after

**Mechanism.**
- Composition reads a configuration root `<root>/packs/<dir>/`, and each pack declares its level in `pack.yaml` (ADR-0038; `scripts/ci/charter_service_check.py:14-19`). The service ships no open-packs content (ADR-0070 Context `:45`). A deployer places the built-in pack.
- One compose is the `depends_on` closure rooted at every configured pack (ADR-0053 d6 `:99-101`). The resolver **does not fetch** anything. A `depends_on` target missing from the root is refused with `pack_dependency_unknown` (`PackCompositionResolver.java:129,829-839`; fixture `tests/fixtures/invalid/unknown-dependency/expected-code:4-5`).
- Registration (ADR-0065): a whole-pack `PUT` replaces the stored pack (D1 `:69-77`). **Only `org` and `project` packs are writable. A built-in-level pack is refused with `409 registration_conflict`** (D3 `:93-97`). Re-sending the same `pack_version` with different content gives `409 pack_version_conflict` (D2 `:86`, D9 `:233-238`).
- Qualified references: a `<pack>::` qualifier must name a pack in the referrer's **transitive** `depends_on` closure (`dependsOnClosure`, `PackCompositionResolver.java:519-534`), and that pack must hold the artifact (`:505-515`, `pack_reference_artifact_missing`). The local gate behaves the same way (`scripts/ci/validate_pack_schemas.py:976-984`, used `:1009,1060`).
- Fallback profile: resolved in the declaring pack's closure (ADR-0068 d2 `:57-59`) and locked along it (d3 `:60-62`). `built-in` can therefore keep `fallback_profile: generic-agent` and its `policy.yaml` lock (`packs/built-in/policy.yaml`) while foundation holds the profile.
- The "empty active charter = nothing" rule (ADR-0053 d10) is **already implemented** in the service (`ActivationDocument.java:31`). The split does not change activation semantics on the service.

| | Before (main) | After the split |
|---|---|---|
| What a deployer places in the root | `packs/built-in` | `packs/built-in` **and** `packs/foundation` **and** `packs/writing`, all `pack_level: built-in` |
| Only `built-in` placed | Composes | **Refused** `pack_dependency_unknown`. The aggregator does not pull members transitively. |
| Registering `built-in` / members | Not possible (D3) | Not possible (D3). Members are read-only too. |
| Org pack with `depends_on: built-in >=1.0,<2` and `built-in::X` refs | Composes | Refused `pack_reference_artifact_missing` (built-in holds nothing). If built-in goes to 2.0.0, the range is refused first. |
| Org pack re-qualified `foundation::X` / `writing::X`, depends_on built-in | n/a | Composes. foundation/writing are in its closure through built-in (transitive). |
| Effective artifact set for a project activating built-in's `default` preset | Built-in's artifacts | The same artifacts, now held by foundation and writing (preset ids are bare and resolve across the closure) |

**Is it breaking?** For a charter-service deployer, yes: they must add two pack directories. For any third-party pack that writes `built-in::<id>`, yes: every such reference must be re-qualified. For a project that only activates presets or artifact ids, no: ids are unchanged (ADR-0048 d10) and only the provenance moves.

**This repository's own service gate needs changes.** `scripts/ci/charter_service_check.py` hard-codes the single built-in:
- `:64` `BUILT_IN = "built-in"`. Registration stages only it (`:381` `stage(root, [built_in])`). `:382-388` raises **CannotRun** when a non-built-in pack is not `org`/`project`. foundation and writing are exactly that case, so the job would exit 2.
- The invalid fixtures stage only `[built_in]` (`:419`, `:430`). After the split, built-in's own unknown dependencies would be refused first and mask the expected `pack_unreadable` / `validation_failed` codes.
- Fix direction: stage **every `pack_level: built-in` pack** read from the descriptors. This matches D3, which makes every built-in-level pack read-only.

## 3. Packs that depend on built-in and reference its artifacts

Every org pack declares `depends_on: 01ARWG13C000000000000000FG ">=1.0,<2"`: `packs/internal/pack.yaml:21-23`, `qa:18-20`, `event-driven:17-19`, `cave-kitty:19-21`, `spdd:11-13`. Under d12 **every** `built-in::` reference must change, because built-in holds nothing. There are 102 occurrences on 72 distinct targets: internal 62, qa 27 (24 typed profile refs + 3 graph edges), event-driven 7, spdd 6, cave-kitty 0. Membership below follows the census (charter `docs/plans/pack-ecosystem-work-breakdown.md:75-115`, the starting cut per ADR-0053 d2). Rows marked † need an operator ruling or are later moves.

**→ `writing::` (census writing members)**
- `directive:DIRECTIVE_042`: `internal/drg/fragment.yaml:658`
- `directive:DIRECTIVE_047`: `internal/drg/fragment.yaml:661`
- `styleguide:common-docs`: `internal/drg/fragment.yaml:326`
- `traceable-decisions` (tactics/communication/*): `qa/agent_profiles/qa-reporter-rhea.agent.yaml:72`
- † `procedure:declare-page-audience`: `internal/drg/fragment.yaml:672`
- † `procedure:common-docs-page-authoring`: `internal/drg/fragment.yaml:675`. The census does not name these two procedures. They fit "the audience assets" and the common-docs cluster.
- Prose only, unchecked: `comms-cleo`, `synthesizer-sam` in `internal/procedures/executive-debrief-generation.procedure.yaml`, and `synthesizer-sam` in `project-evolution-postmortem.procedure.yaml`

**→ `foundation::` (everything else, interim home within #73's scope)**
- **spdd** (`packs/spdd/drg/fragment.yaml`): `agent_profile:architect-alphonso` `:59`; `action:software-dev/{specify,plan,tasks,implement,review}` `:67,70,73,76,79`. The step enhancements target foundation's mission type. The ADR-0048 d16 rename (`missions/`→`mission_types/`) changes paths, not the `action:` URNs.
- **event-driven** (`packs/event-driven/drg/fragment.yaml`): `tactic:domain-event-capture` `:101,130`; `procedure:event-storming-discovery` `:104`; `paradigm:domain-driven-design` `:107`; `paradigm:deep-module-design` `:110`; † `tactic:anti-corruption-layer` `:154`; † `tactic:reference-architectural-patterns` `:167`. The two † items are `tactics/architecture/*`, which the census sends to a later `architecture` pack.
- **qa graph** (`packs/qa/drg/fragment.yaml`): `tactic:bdd-scenario-formulation` `:187`; † `styleguide:given-when-then-authoring` `:190`; † `toolguide:gherkin` `:193`. The two † items are census "testing extras fold into qa". They would become bare in-pack refs when they move, which is later work.
- **qa profiles** (typed `built-in::<id>` → `foundation::<id>`):
  - tessa `qa-test-designer-tessa.agent.yaml:37,66,74,80,87,96†,102†`
  - dmitri `qa-defect-triager-dmitri.agent.yaml:29,30,55`
  - elena `qa-test-executor-elena.agent.yaml:44,51,57,67,71†,80`
  - quinn `qa-strategist-quinn.agent.yaml:45,51,58,66,70`
  - rhea `qa-reporter-rhea.agent.yaml:64,82`. Rhea `:72` goes to writing (above).
  - The service may not artifact-check a kind-less typed id. The local gate does (`validate_pack_schemas.py --cross-pack`, "id the named pack does not hold").
- **internal** (`packs/internal/drg/fragment.yaml`):
  - directives: 025 `:409`, 041 `:384,506,522`, 044 `:317`, 045 `:525,570`, `RECONCILE_CHANGE_SCOPE_TENSIONS` `:413`, `RED_MAIN_RELEASE_DISCIPLINE` `:249,262,307`
  - profiles: planner-priti `:486,515,579,588`, reviewer-renata `:540`
  - procedures: adversarial-squad-deployment ×5, test-first-bug-fixing ×3, development-assist-test-cleanup ×2, post-merge-arch-gate-adjudication ×2, issue-triage-state-machine `:354`, † refactoring `:417` (census: `refactoring` pack)
  - styleguides: planning-and-tracking `:313,358,640`, test-desiderata-and-boundaries `:376,559`, testing-principles `:380`
  - toolguide: github-tracker `:362`
  - tactics: model-task-routing, clean-linear-commit-history, moscow-scoping-lens, pr-agent-worktree-isolation, occurrence-classification-workflow, frozen-baseline-shrink-only-ratchet, canonical-source-unification, architectural-gate-non-vacuity, no-parallel-duplicate-test-runs (lines in the index)
  - † census "moves to internal": `styleguide:tiered-standards` `:310`, `procedure:mission-tracer-files` `:500`, `procedure:mission-wrap-up-sequence` `:448,472,491,585`. If #73 moves them into `internal`, these refs become **bare**. Otherwise they become `foundation::`.
- **cave-kitty**: no checked refs. Its prompts name built-in profiles in prose (`cave-kitty/missions/cave-dev/steps/*.prompt.md:5-23`: "a built-in … profile such as `implementer-ivan`"). The same applies to `qa/missions/qa/steps/discovery.prompt.md:5,11` and the `internal/procedures/*` prose. These still read correctly, since built-in still *ships* the profiles via its members. "built-in" there means the distribution, so no change is required, though the wording could be refreshed.

**depends_on choice (operator ruling needed).** Option A, which matches the epic #190 constraint "every pack declares depends_on on built-in": keep `depends_on: built-in` and write `foundation::`/`writing::`. These resolve through the transitive closure. Option B, which matches the ADR-0048 d8 diamond: depend directly on the member(s) a pack references (internal on foundation and writing; qa on foundation and writing; event-driven and spdd on foundation). B is more precise and survives a later recomposition of built-in. A changes fewer lines. Either way the **range must move if built-in goes to 2.0.0** (§4). cave-kitty is touched only by that range change.

**Downstream PRs and branches.** `git ls-remote origin` shows **no `feat/rust-go-packs` branch and no Java branch or PR**. The recent PR list has none either. Their issue texts are written against the pre-split shape and need updating:
- #5 (java): "directives 010/024/025/030/034/051 and the tactics dependency-hygiene, supply-chain-install-safety, TDD/ATDD/BDD, which all stay in built-in … qualified as `built-in::<kind>:<id>`" and `depends_on built-in >=1.0,<2`. After the split these are `foundation::`, and the range follows the built-in major. If java lands **before** the split, its git-mv sources and `built-in::` refs are re-qualified by the split PR. If it lands **after**, it extracts from `foundation`.
- #191/#192 (rust/go) state `depends_on built-in >=1.0,<2` and `built-in::<kind>:<id>` (shape sections). The same update applies. They also say `implementer-ivan` and `reviewer-renata` keyword "rust". Those profiles move to foundation.
- **Open PR #193** (paradigm principles) edits 9 `packs/built-in/paradigms/*`, `pack-manifest.yaml` and `built-in.source.yaml`. It will conflict with the file moves. Land it first, or rebase it onto the split.
- Private/external: the charter repo's `syncPacks` copies `packs/internal` and `packs/qa` for its own CLI governance (ADR-0070 d5; `gradle.properties:10` `openPacksRef=a2a9379`). Its tests no longer read open-packs (ADR-0070 d1). No charter CI breaks. Its governance copy picks up re-qualified refs at its next pin bump. This repository's own `.kittify/charter/charter.yaml` has CLI-generated `source_path: ${SPEC_KITTY_PACKS_ROOT}/built-in/...` entries (`:414-462, 528, 1464, 1488`). These go stale; regenerate them or accept the drift (CLI preflight is off, ADR 2026-11-04-1 `:203-209`).

## 4. Release and versioning

- Release unit: repository-wide `vX.Y.Z` tags. Each tag ships `<pack>-vX.Y.Z.tar.gz` and `.sha256` for **every directory under `packs/`** (ADR 2026-10-20-1 `:50-56`). `list_packs` enumerates `git ls-tree packs/` (`scripts/release/release_assets.py:55-68`), so **foundation and writing get archives with no tooling change**. `tests/release/test_release_assets.py` uses a synthetic repo (`:44,60,94-96`) and needs no change. Tag `v0.1.0` exists, but `CHANGELOG.md` has only `[Unreleased]` (`:20`). The next repo tag is a 0.x minor.
- **Pack versions** (`pack_version`, separate from the repo tag):
  - `built-in` **1.0.0 → 2.0.0**. It loses all its artifacts, and every `built-in::<id>` reference by any dependent breaks. That is what a major bump is for. Org packs' `<2` ranges then fail closed with a clear range refusal rather than a puzzling `pack_reference_artifact_missing`.
  - `foundation` 1.0.0 and `writing` 1.0.0, new tool-minted ULID `pack_id`s (charter.md identity rule `:110-112`), `pack_level: built-in`, `parent_pack: null`.
  - `built-in` `depends_on`: foundation `==1.0.0`, writing `==1.0.0` (ADR-0048 d17 exact pins; PEP 440 per ADR-0053 d4).
  - Org packs: range `>=2.0,<3` on built-in (option A), or on the members (option B).
  - Bump the `pack_version` of every org pack whose files change: internal, qa, event-driven, spdd, and cave-kitty for the range. A re-registration of an unchanged `1.0.0` with new content is `409 pack_version_conflict` on any service that already stored 1.0.0 (ADR-0065 D2/D9). CI's fresh root does not catch this. No org pack has bumped yet despite past changes, which is an existing gap.
- **Release and gate tooling that hard-codes built-in:**
  - `scripts/ci/built_in_digest.py:24-25` and `check-built-in.sh:14-16` digest only `packs/built-in`. Record digests for foundation and writing too, for example a member block in `built-in.source.yaml` or `<member>.source.yaml` files. ADR-0048 `:214-216` expects core to verify every member tree's digest.
  - `scripts/ci/charter_service_check.py:64,381-388,419,430` (§2).
  - `scripts/ci/check_vocabulary.py:75` names the path `packs/built-in/procedures/test-first-bug-fixing.procedure.yaml`. Moving that file makes the row stale, and the script reports stale rows. `:5` is a comment. Tests `tests/vocabulary/test_check_vocabulary.py:57,98,99` use synthetic paths and are fine.
  - `scripts/docs/gen_pack_reference.py:153-167` puts built-in first and sorts the rest. `docs/packs/foundation.md` and `writing.md` must be generated and committed for `--check`.
  - `packs/README.md:31-33` says "validate-packs.sh skips [built-in]". That is already stale (`validate-packs.sh:28,57` includes it). Update it with the new members.
  - README pack table `README.md:56-62` and status `:110`; `.kittify/charter/charter.md:79-81`; ADR 2026-11-04-1's name table `:167-173` (superseded in part by the new ADR).

## 5. Breaking-change assessment and recommended wording

**Who breaks:**
1. Charter-service deployers: they must place two more built-in-level packs.
2. Any pack qualifying `built-in::<id>`: in this repository the four org packs are fixed in the same PR, but third parties are affected.
3. Org packs ranging on `built-in <2`.
4. Core at any future pin (out of scope; already broken at main).

**Who does not break:** projects that activate presets or artifact ids, because ids are unchanged.

**Precedent:** the #175 SPDD and #118 entries (`CHANGELOG.md:35-62`). Add an ADR (epic #190 constraint).

Suggested entry under `### 💥 Breaking`:

> - **`built-in` is now a distribution pack over two new packs, `foundation` and `writing`** (#73, #190;
>   charter ADR-0048 d11–d17, ADR-0053 d2/d3/d9; ADR 2026-11-1x-1). `built-in` keeps its `pack_id`,
>   `pack_level: built-in`, its `default` and `minimal` presets, `fallback_profile` and `policy.yaml`, but holds no
>   artifacts: it `depends_on` `foundation` and `writing` at exact versions. `foundation` holds the cross-cutting
>   directives, paradigms, tactics, the base agent profiles (`generic-agent`, `implementer-ivan`, …), the four mission
>   types with their step contracts, the glossary, templates and assets; `writing` holds the documentation styleguides,
>   the writing and communication profiles, directives 042 and 047 and `tactics/communication/*`. No artifact id
>   changes. `built-in` is now `2.0.0`; `foundation` and `writing` start at `1.0.0`. What a consumer must now do:
>   - On the charter service, place `packs/foundation` and `packs/writing` beside `packs/built-in` in the
>     configuration root. All three are built-in level and read-only to registration; `built-in` alone is refused
>     `pack_dependency_unknown`.
>   - In your own pack, re-qualify every `built-in::<kind>:<id>` (graph edge) and `built-in::<id>` (typed reference)
>     as `foundation::…` or `writing::…`, and raise your `depends_on` range on `built-in` to `>=2.0,<3`. The
>     `internal`, `quality-assurance`, `event-driven`, `spdd` and `cave-kitty` packs here are migrated.
>   - Presets and activations need no change: ids are unchanged and resolve across the closure.
>   - Core fetches only `packs/built-in` at its pin, so a core that bumps its pin past this commit loses every
>     profile and mission type until it fetches and ships the members (ADR-0048 Consequences); core compatibility is
>     not this repository's concern (AGENTS.md).

Migration note for consumers (guide `docs/guides/use-a-charter-pack.md`, next to the #65 migration anchor):
1. Pin a release that contains the split and fetch all three `<pack>-vX.Y.Z.tar.gz` archives (built-in, foundation, writing). Verify each `.sha256`.
2. Configuration root: `packs/built-in`, `packs/foundation`, `packs/writing`.
3. Rewrite qualifiers. Mechanical lookup: the artifact's file now lives under `packs/foundation/` or `packs/writing/`, and that directory names the qualifier.
4. Bump `depends_on` ranges and your own `pack_version`, then re-register (whole-pack replace, ADR-0065 D1).
5. Activation and preset files are unchanged.
6. Staying on the old layout: pin the last pre-split commit or tag. Recommend tagging one, e.g. `pre-built-in-split`, as #118 did with `pre-charter-cutover`.

## Risks and open items for the orchestrator
- **Operator rulings needed:**
  - depends_on target (built-in vs members, §3)
  - the † memberships: the two writing procedures, the three census moves to internal, and the architecture/refactoring/qa interim homes
  - whether `foundation` also declares `fallback_profile` and its own lock so it is usable on its own (members "can be reused and registered on their own", ADR-0048 `:291-292`)
- Sibling-conflict rule: foundation and writing are siblings at one level, so no id may be held by both (`PackCompositionResolver.java:575-640`). The split must partition artifacts exactly, graph-shard node declarations included.
- Graph shards: built-in's `*.graph.yaml` edges that cross the foundation↔writing boundary must be qualified, and writing must `depends_on` foundation (same level, so allowed) if writing's edges point into foundation. Cycles between members are refused.
- Sequencing: land PR #193 and the #182 manifest guard first. Java (#5), rust/go (#191/#192) issue texts need the post-split qualifiers and ranges.
