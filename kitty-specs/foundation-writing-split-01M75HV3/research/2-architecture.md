# Research 2: architecture of the built-in → foundation + writing split (open-packs #73)

Read-only research. open-packs `main @ 5c489d6`; charter at the lock pin `fb24052d` (`charter.lock.yaml:19`).
Abbreviations: CR = charter repo `/home/user/spec-kitty/spec-kitty-charter`; OP = `/home/user/spec-kitty-open-packs`;
RES = `CR/service/packs/src/main/java/ai/speckitty/charter/packs/domain/PackCompositionResolver.java`.

## 0. Ruling baseline (what is already decided)

- `built-in` becomes a **distribution pack**: it keeps its `pack_id` and `pack_level: built-in`, holds **no artifacts of
  its own**, aggregates members **through `depends_on`**; presets `default`/`minimal` stay on it (ADR-0048 d12,
  `CR/docs/adr/0048-…md:168-170`).
- Members: `foundation` and `writing` (ADR-0053 d3, `0053:91-92`; name `foundation` d9, `0053:115`). Each a full
  top-level pack (d11, `0048:166-167`), each a root with `parent_pack: null` (d15, `0048:177-179`).
- Stack packs (java, python, drupal…) are **opt-in, not members** (d14, `0048:175-176`; ADR-0053 d3 "every other
  topical pack and every stack pack is opt-in", `0053:91-92`) and declare `pack_level: org` (ADR-0053 d1, `0053:86-87`).
- Members version separately, release in lockstep, and **`built-in` pins members' exact versions** (d17, `0048:182-184`).
- #73 body (re-scoped 2026-11-09) restates all of this; item 3 (core pin/fetch) is out of scope (charter-only
  alignment, OP `AGENTS.md`).

## 1. Pack levels, ordering, the d7 rule, and the level of foundation/writing

- Levels: `built-in`, `org`, `project` (schema enum, `CR/contracts/packs/schemas/pack-descriptor.schema.json:44-53`;
  `PackLevel.java` BUILT_IN/ORG/PROJECT).
- Ordering: RES `rank()` `RES:897-903`: built-in=0, org=1, project=2.
- d7 as amended 2026-11-03 (`0048:143-145`): "a pack may take a `parent_pack` only at its own level or one nearer
  built-in, and the rule extends to `depends_on`… refused `pack_level_violation`". Implemented in `requireLevel`
  `RES:882-895`: refuse iff `rank(target) > rank(own)`. Applied to every `depends_on` edge (`RES:858`… in
  `dependenciesOf` `RES:829-872`, call at the `requireLevel(pack, target, false)` line) and to `parent_pack`. Rule
  C10 in `CR/docs/architecture/composition-and-activation-rules.md:199-201`.
- So: **a built-in-level pack MAY depend on another built-in-level pack** (same rank → allowed). A built-in pack may
  NOT depend on an org/project pack. An org pack may depend on org or built-in packs.
- The level the rule reads is the **configured** level (`pack.configured().level()`, `RES:883-884`; ADR-0053 d8).
  In a config root the configured level is the one the pack's own `pack.yaml` declares
  (`CR/service/packs/src/main/java/.../infra/storage/StorageRootLocations.java:32-35`: "Its level is the one its own
  pack.yaml declares… built-in, org and project packs live side by side"). Several built-in-level packs in one root
  are fine (built-in ones are sorted first, `StorageRootLocations.java:146-147`).
- **Answer: `foundation` and `writing` must be `pack_level: built-in`.**
  - `built-in` (level built-in) depends on them → they must be at rank ≤ 0 → built-in. Making them `org` would make
    built-in's own `depends_on` a `pack_level_violation`.
  - Org stack packs (`java`/`rust`/`go`, ADR-0053 d1 org) may then depend on `foundation` (org → built-in is
    "nearer built-in", allowed). Org packs `internal`/`qa`/`cave-kitty`/`event-driven`/`spdd` likewise.
  - Consequence: no org pack can ever be a member of `built-in` without itself being re-levelled to built-in (see §5).
- Note (schema): `pack_level` is required whenever `depends_on` is non-empty
  (`pack-descriptor.schema.json:171-189`); built-in will now have `depends_on`, so its existing `pack_level: built-in`
  (OP `packs/built-in/pack.yaml:16`) is mandatory. foundation and writing need it whenever they declare a dependency.

## 2. How aggregation is expressed; is it supported at the pin?

- **There is no aggregation field** (`includes`/`aggregates`/`members`) in the descriptor at the pin. The schema is
  closed (`additionalProperties: false`, `pack-descriptor.schema.json:4`) with properties schema_version, pack_id,
  pack_version, parent_pack, name, pack_level, depends_on, overrides, requires_core, active_charter, pack_drg,
  mutability_policy, fallback_profile (`:6-164`). An `includes:` key would make `pack.yaml` unreadable.
- **Aggregation = `depends_on`** (ADR-0048 d12 "aggregates its members through `depends_on`"; d8 diamond with a
  "distribution pack Z depends on the specialists", `0048:149-153`). `parent_pack` is not the aggregation edge
  (d15: the distribution pack "depends on it and does not derive it").
- Supported at the pin: yes. `resolve()` (`RES:253-276`) builds ordering from `depends_on`+`parent_pack`
  (`dependenciesOf` `RES:829-872`), checks unknown dependency, PEP 440 range (`admits`, `RES:874-876`), level,
  self-cycle; `topologicalOrder` (`RES:905-958`) is Kahn with cycle refusal; disjoint-range refusal across dependents
  (`refuseDisjointRanges`, `RES:544`); shared dependency deduped by pack_id; composition closure walks depends_on +
  parent_pack (`compositionClosure`, `RES:327-341`). A pack with zero artifacts is a legal `PackUnderResolution`
  (`definedArtifacts` empty, `RES:100-107`).
- Proposed built-in descriptor shape (d17 exact pins; PEP 440 grammar per ADR-0053 d4):
  ```yaml
  schema_version: "1.0"
  pack_id: 01ARWG13C000000000000000FG
  pack_version: 2.0.0            # artifacts leave built-in: a breaking major (see §3 range note)
  parent_pack: null
  name: built-in
  pack_level: built-in
  fallback_profile: generic-agent   # resolved along built-in's closure (see below)
  mutability_policy: policy.yaml    # optional to keep here, see below
  depends_on:
    - pack_id: <foundation ULID>
      range: "==1.0.0"
    - pack_id: <writing ULID>
      range: "==1.0.0"
  ```
- Things that keep working on an artifact-less built-in at the pin:
  - `fallback_profile`: judged over the **declaring pack's closure** — "a pack of the closure holds it… locked by any
    pack of its closure" (`FallbackProfileRule.java:59-75`; schema text `pack-descriptor.schema.json:157-163`). So
    `generic-agent` may move to foundation while built-in keeps declaring `fallback_profile`.
  - `policy.yaml` locks are judged "along the closure, highest level wins" (ADR-0063 D3, `0063:81-92`); keys are bare
    URNs, never qualified (`0063:76-77`). built-in's `agent_profile:generic-agent: locked` (OP
    `packs/built-in/policy.yaml`) keeps locking it if it lives in foundation. A mention of an id no pack holds is "left
    alone" (`RES:718-725`); only a case-only mismatch is refused. Cleaner alternative: move the policy (and possibly
    `fallback_profile`) to foundation, since foundation is the pack org stack packs depend on directly.
  - Presets resolve closure-wide, by bare id (`ClosureView` held presets; preset schema forbids qualified ids,
    `preset.schema.json:10`), so `default`/`minimal` on built-in can name foundation/writing artifacts. Preset contests
    are per-level unless on a parent line (`refusePresetContests`, `RES:686-715`) — presets must exist ONLY on built-in,
    not copied into foundation/writing (they would be built-in-level siblings holding the same preset id).
- **The gate script needs changing (blocker for the PR, not for the design).** `OP/scripts/ci/charter_service_check.py`:
  - Registration phase stages **only `packs/built-in`** into the scratch root (`:381`, ADR-0065 D3: built-in is
    read-only to registration, `0065:93-97`; service `PackRegistrationService.java:302-305`) and raises `CannotRun`
    unless every non-built-in pack is `org`/`project` (`:382-388`). With foundation/writing at `pack_level: built-in`
    the script exits 2, and even if not, built-in's `depends_on` would be unknown in the scratch root
    (`pack_dependency_unknown`). Fix: stage every pack whose `pack_level` is `built-in` (built-in + foundation +
    writing), and compare `others` against non-built-in-level packs.
  - Same in `check_invalid` (`:419`, `:430`): invalid fixtures are composed/registered beside `[built_in]` only;
    stage all built-in-level packs there too.
  - `BUILT_IN = "built-in"` (`:64`) and `built_in = repo/packs/BUILT_IN` (`:457`) stay valid as "the distribution".
  - Composition phase (`:350-376`) already handles any number of packs/levels.
  - Other built-in-only tooling: `scripts/ci/check-built-in.sh:14`, `built_in_digest.py:24` (tree digest of
    `packs/built-in` only — `built-in.source.yaml` is a core-fetch concern, out of scope, but the digest will change),
    `gen_pack_reference.py:155-163` (built-in first), `check_vocabulary.py:75` (hard-codes a
    `packs/built-in/procedures/…` path).

## 3. Proposed depends_on graph; acyclicity and level proof

Nodes (level): built-in (B), foundation (B), writing (B); internal, quality-assurance, cave-kitty, event-driven, spdd,
future java, rust, go (all org).

Edges (proposal):
```
built-in   -> foundation  (==1.0.0)
built-in   -> writing     (==1.0.0)
writing    -> foundation  (>=1.0,<2)      # only if writing's graph references foundation artifacts (expected)
foundation -> (nothing)
java/rust/go -> foundation (>=1.0,<2)     # option (b), §5
internal, quality-assurance, event-driven, spdd, cave-kitty -> built-in (>=2.0,<3) and/or -> foundation/writing
```

- **Acyclic**: assign a topological rank: foundation=0, writing=1, built-in=2, every org pack=3. Every edge above goes
  from a higher number to a strictly lower one, so no cycle exists (`topologicalOrder` would place all; no
  `pack_dependency_cycle`). No pack names itself; all `parent_pack: null`, so parent edges add nothing.
- **No level violation**: built-in→foundation/writing and writing→foundation are built-in→built-in (rank 0→0); every
  org→built-in-level edge is 1→0. None has `rank(target) > rank(own)` (`RES:885`).
- **Does foundation depend on anything?** No. It must not depend on `built-in` (cycle B→F→B) and should not depend on
  `writing` (that forces writing not to depend on foundation, see §4). It is the root.
- **Does writing depend on foundation?** Recommended yes, if any writing artifact references a foundation artifact
  (e.g. writing profiles referencing cross-cutting directives, the generic profile, or the documentation mission's
  steps). It is legal (same level) and keeps foundation a pure root. If writing references nothing in foundation, the
  edge is optional — but declaring it is cheap and future-proofs qualified references.
- Diamond (d8): built-in→writing→foundation and built-in→foundation share foundation, loaded once; ranges must
  overlap (`refuseDisjointRanges`). built-in pins `==1.0.0`; any other dependent's range on foundation must admit
  1.0.0 or the compose with built-in is refused. This is a real constraint on java/rust/go ranges (e.g. java
  `>=1.1` with built-in pinning `==1.0.0` would be refused in any compose holding both).
- **Range note for existing org packs**: they declare `built-in` at `>=1.0,<2` (OP `packs/*/pack.yaml`). Removing
  artifacts from built-in is breaking; if built-in goes to 2.0.0 every dependent's range must move, or built-in stays
  1.x (a policy choice; the service treats version as a label for registration, ADR-0065 D2, but `depends_on` ranges
  are checked, `RES:874-876`).
- **Sibling rule at the built-in level**: foundation, writing and built-in are siblings at level built-in, so the
  split must be a strict **partition** — any artifact id held by two of them is `pack_sibling_conflict`
  (`refuseContests`, `RES:614-676`; C14/C16 `composition-and-activation-rules.md:218-236`). Steps don't contest on
  their own; their mission type does (`RES:606-612`). No stray copies (e.g. glossary, generic-agent, templates) in two
  members.
- Existing org packs: may keep `depends_on: built-in` only. The qualified-reference check uses the transitive
  `depends_on` closure (`dependsOnClosure`, `RES:523-536`; local gate mirrors it, OP
  `scripts/ci/validate_pack_schemas.py:976-985`), so an org pack that depends only on built-in may write
  `foundation::…` and `writing::…`. Depending directly on foundation/writing is more precise and decouples them from
  built-in's exact pins (a choice for the lead).

## 4. Qualified cross-pack references

- Form: `<pack-name>::<urn>` (ADR-0053 d7, `0053:104-112`; ADR-0048 d10 amendment `0048:162`). `<pack-name>` is the
  descriptor `name` (grammar `^[a-z0-9][a-z0-9_-]*$`, `pack-descriptor.schema.json:37-43`), not the directory
  (OP ADR 2026-11-04-1 lines 64-77: `quality-assurance` ≠ `packs/qa`). Parser: `PackQualifiedReference.parse` (one
  `::` max). Two spellings in open-packs: graph-edge end `<pack>::<kind>:<id>`; typed-reference `id` field
  `<pack>::<id>` (OP ADR 2026-11-04-1:79-88). Graph-shard and org-fragment schemas allow the qualifier on **both**
  `source` and `target` (`graph-shard.schema.json:8-18`).
- Rules (C12/C13, `composition-and-activation-rules.md:208-217`; `checkReferences` `RES:442-478`,
  `checkQualifiedReference` `RES:483-519`):
  - A reference to the writer's own artifact stays bare.
  - A bare reference held only by another pack → `pack_reference_unqualified`.
  - A qualified reference must name a pack in the **writer's own `depends_on` closure** (transitive, depends_on only,
    not parent_pack) → else `pack_reference_pack_missing`; and that pack must hold the artifact →
    else `pack_reference_artifact_missing`.
  - Both ends of every edge are checked (`EdgeIndex.java:394-404` flattens `fromReference`, `toReference`).
- **Which side qualifies**: the edge is authored in one pack's graph documents (ADR-0064); in that pack, whichever end
  is not held by the authoring pack is qualified. An edge with a **qualified source** is legal and is homed at the
  source's pack (`EdgeIndex.add`, `EdgeIndex.java:410-425`), so a dependent pack can attach guidance to a
  dependency's node. Hence the edge always lives in the **dependent** pack: e.g. writing can author
  `foundation::action:documentation/<step> -> styleguide:<writing-id>` without foundation depending on writing. This
  matters because ADR-0048 OQ3 notes the documentation mission type relies on writing styleguides/profiles
  (`0048:254-257`): if the documentation mission type stays in foundation, its edges to writing guidance must move into
  writing's graph documents (source qualified `foundation::`), or the documentation mission type goes to writing.
- **An edge from foundation to an artifact left in built-in is illegal.** built-in is not in foundation's closure
  (`pack_reference_pack_missing`), and adding it would close the cycle foundation→built-in→foundation
  (`pack_dependency_cycle`). Moreover built-in holds no artifacts by d12, so `built-in::X` anywhere after the split is
  `pack_reference_artifact_missing`. Likewise foundation→writing edges are illegal unless foundation depends on writing
  (which would forbid writing→foundation).
- **Rewrite load from the split**: today org packs carry `built-in::` references (count by file: internal
  fragment 62, event-driven 7, spdd 6, qa fragment 3, qa agent profiles 24 — the last are the #119 typed
  references). Every one must become `foundation::` or `writing::`. Built-in's own internal edges that end up crossing
  foundation/writing must gain the prefix too (ADR-0053 Negative consequences, `0053:220-222`). #5 (java) currently
  plans `built-in::` qualifiers on java-jenny's edges; if #5 lands before #73 those become a rewrite too.
- Local early gate: `validate_pack_schemas.py:998-1032` (qualifier outside closure) and `cross_pack_violations`
  (`:1109-1175`; forbids the same id at two levels, checks preset ids across all packs).

## 5. java-in-built-in trade-off (not decided)

**(a) built-in aggregates java.**
- Level: built-in → java requires java at `pack_level: built-in` (built-in→org is `pack_level_violation`,
  `RES:882-895`; d7). That contradicts ADR-0053 d1 (java is org, `0053:86-87`).
- Membership: contradicts ADR-0048 d14 ("`java`… are not members of `built-in`", `0048:175-176`) and ADR-0053 d3
  ("every other topical pack and every stack pack is opt-in", `0053:91-92`).
- Needs: a charter operator ruling + ADR amending ADR-0048 d14 and ADR-0053 d1/d3 (and d7 cannot bend — it is the
  rule; only java's level changes). Consequences: java becomes read-only to registration (ADR-0065 D3), is shipped to
  every consumer (the "too exhaustive" problem the split exists to fix, `0048:107-109`), and joins the built-in sibling
  partition (no id shared with foundation/writing). Mechanically: one more `depends_on` entry on built-in, java at
  built-in depending on foundation; still acyclic.
**(b) java stays opt-in.**
- java at `pack_level: org`, `depends_on` foundation (and writing if it references it), edges qualified
  `foundation::…`. Matches d1/d3/d14 as ruled; no ADR change. Registered by a project/org like qa. Range on
  foundation must overlap built-in's exact pin when both are in one compose.
**Neither is foreclosed by the split**: foundation is a separate built-in-level root pack that both a built-in-level
java (a) and an org java (b) may depend on (same level / nearer built-in). Switching from (b) to (a) later = re-level
java to built-in + add one `depends_on` entry on built-in + charter ADR amendment; no change to foundation or writing.
The split only forecloses java depending on `built-in`'s own artifacts (there are none), which both options avoid.

## 6. pack_id minting and the built-in id

- "Tool-minted": constraint C-002 of the strict-composition mission — "`pack_id` values are generated once by a tool,
  never typed by hand, and never reused from a scratch run" (OP `kitty-specs/strict-pack-composition-01M6M0W4/spec.md:103`;
  plan `:31`; data model `:9`). The "tool" was an inline Python ULID generator in the WP prompt (OP
  `kitty-specs/strict-pack-composition-01M6M0W4/tasks/WP02-pack-identity.md:80-92`: 48-bit ms timestamp + 80 random
  bits, Crockford base32). The three org ids sharing `01M6MF4FV4…` were minted in that batch; spdd's
  `01M6Y9ACNAAD96XPNQS0XWP2FF` later (commit 170dbc3). Any ULID library works (core uses `python-ulid` `str(ULID())`,
  e.g. `/opt/spec-kitty/src/specify_cli/upgrade/migrations/m_4_0_0rc7_pack_level_backfill.py:108`).
- No repo script and no CLI command mints an org/built-in pack id: `scripts/` has none (grep "ulid|mint" finds
  nothing); `spec-kitty charter org init` writes no `pack.yaml` (`/opt/spec-kitty/src/specify_cli/cli/commands/charter/org.py:225-242`);
  the charter repo has no minting script. Mint two fresh ULIDs (foundation, writing) once, with a tool, record them,
  never edit them (schema: Crockford pattern `^[0-9A-HJKMNP-TV-Z]{26}$`, `pack-descriptor.schema.json:193-197`).
- `01ARWG13C000000000000000FG` is the ULID spec's doc example, a deliberate fixed constant bound to the name
  `built-in` in core (`/opt/spec-kitty/src/charter/offering/drg/org_pack_config.py:64-84`, `ensure_pack_identity`
  `:1000-1036`; core test `tests/charter_offering/test_pack_id_identity.py`). ADR-0048 d12: built-in "keeps its
  `pack_id`" (`0048:168`). Every org pack's `depends_on` names it. **It must stay on `built-in`**; foundation and
  writing get new ids. (Note: it is a valid ULID with a 2016 timestamp, so it sorts first.)

## 7. Lead's extra questions

- **Is the `missions/` → `mission_types/` rename (d16 / ADR-0050 d4-5) forced by moving missions to foundation?** No —
  and at the pin it would be **refused**. The pin's file table puts mission types at
  `missions/<id>/<id>.mission-type.yaml` (`CR/contracts/packs/file-kinds.yaml:175-178`), companions under
  `*/missions/*/steps/` (`:181-186`), enhancements under `*/missions/*/enhancements/` (`:194-197`), templates under
  `*/missions/*/templates/**` (`:296-299`), and lists `*/mission_types/*.yaml` as **retired**, refused by name
  (`:261-265`). The service binds `"missions/" + id` (`MissionTypeBinding.java:79`, `DomainRepositoryService.java:414`,
  `TemplateBinding.java:67`). The layout is not built-in-specific: org packs qa/cave-kitty/spdd already hold
  `missions/` at the pin. Step contracts match `**/*.step-contract.yaml` anywhere (`file-kinds.yaml:143-144`), so
  `missions/built_in_step_contracts/` can move as is. ADR-0050 d4 (`0050:219-227`) is accepted but not built at the pin;
  the rename lands with a future charter pin bump, not with #73. #73's body line "The split renames `missions/` to
  `mission_types/`" should be read as deferred until the charter builds it.
- **Can a built-in-level pack depend on another pack?** Yes, on another built-in-level pack (`RES:882-895`).
- **Level for foundation/writing**: `built-in` (see §1).

## Risks / open points for the lead
1. charter_service_check.py must stage all built-in-level packs (§2) — the PR cannot be green otherwise.
2. The documentation mission type's dependency on writing guidance (§4): either edges are authored in writing with a
   `foundation::` source, or the mission type moves to writing.
3. Ranges: built-in's exact pins vs dependents' ranges (diamond overlap), and whether built-in bumps to 2.0.0 (org
   ranges `>=1.0,<2` then break).
4. Sequencing with #5: if java lands first with `built-in::` qualifiers, #73 rewrites them.
5. ADR-0053 d5 "Unclear" (settlement by `overrides` in pack.yaml from any pack) is irrelevant if the partition is
   strict.
