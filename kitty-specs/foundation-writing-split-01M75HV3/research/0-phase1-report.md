# #73 phase 1 — foundation/writing split: research report (for operator approval)

Read-only. open-packs main @ 5c489d6, charter pin fb24052. Detail files next to this one:
1-inventory.md (per-artifact table, all 398 graph nodes + non-node files, crossing edges),
2-architecture.md, 3-consumers.md, 4-gates.md.

## 1. Membership (baseline: charter census, pack-ecosystem work breakdown, ADR-0053 d2)

| Group | Nodes | Proposed ruling |
|---|---|---|
| A uncontested → foundation | 230 | 12 base profiles (implementer-ivan, reviewer-renata, architect-alphonso, planner-priti, analyst-annie, curator-carla, debugger-debbie, designer-dagmar, human-in-charge, paula-patterns, researcher-robbie, retrospective-facilitator), 29 cross-cutting directives, paradigms, glossary pack, base templates, anti-patterns, the software-dev, plan and research mission types + step contracts + actions, 61 tactics, 49 procedures |
| B uncontested → writing | 38 | comms-cleo, diagram-daisy, lexical-larry, minutes-mahad, scribe-sally, synthesizer-sam; DIRECTIVE_042, DIRECTIVE_047, ACTION_ITEM_ATTRIBUTION, MINUTES_STAND_ALONE; 9 docs styleguides; mermaid/plantuml; common-docs tactics + lint asset; audience assets; minutes/audience procedures; meeting templates |
| C stays in built-in | 0 artifacts | pack.yaml (depends_on members), pack.md, regenerated manifest, presets default + minimal (ADR-0048 d12) |
| D stack / topical opt-in | 68 | refactoring 26, javascript 12, pack-authoring 7, qa 5, python 5, **java 4** (java-jenny, java-conventions, java-supply-chain, maven-review-checks), drupal 4, internal 4, architecture 1 |
| E contested | 62 | see below; recommendation for all = foundation except mutation-testing-workflow (→ qa) |

Contested clusters (recommendation first):
- **E-DOC, documentation mission type (18 nodes)**: foundation (d13: shipped mission types live in foundation). Its 19 scope edges into writing move to writing's graph with a `foundation::` source. Alternative: move the whole mission type to writing.
- **E-DDD (11)** and **E-C4 (5)**: foundation. The census sends them to `architecture`, but foundation's profiles, plan mission and paradigms require them.
- **8 architecture tactics, 7 communication tactics, 4 census omissions (037 + living-docs-sync, planning-and-tracking, github-tracker), 036 + BBIT, given-when-then, drill-down-documentation**: foundation (foundation artifacts require them).
- **Cut candidates (039, brownfield-onboarding, small-explicit-code-shaping)**: park in foundation and cut in the curation pass (deep-module-design requires 039).
- **generic-agent + policy.yaml**: the profile goes to foundation; foundation's policy locks it and declares its own fallback_profile; built-in keeps `fallback_profile: generic-agent` (it resolves in the closure). Whether built-in's policy may lock a member's artifact is a charter question.

Group D process (recommended): **hold every D item in foundation for this PR**; each target pack carves its items out in its own issue (as #5 does for java). This keeps #73 a two-pack split and avoids strong edges from foundation to opt-in packs, e.g. software-dev/review → mission-wrap-up-sequence (internal).

## 2. Pack graph

| Pack | pack_id | level | depends_on |
|---|---|---|---|
| foundation | new ULID (minted at phase 2) | built-in | — |
| writing | new ULID | built-in | foundation ==1.0.0 |
| built-in | 01ARWG13C000000000000000FG (kept) | built-in | foundation ==1.0.0, writing ==1.0.0 (d12/d17) |
| internal, qa, cave-kitty, event-driven, spdd | unchanged | org | built-in >=2.0,<3 (or directly foundation/writing, see Q4) |
| rust, go (PR B), java (PR A, option b) | — | org | foundation |

- **No cycle**: order the packs foundation(0) < writing(1) < built-in(2) < org(3); every edge goes strictly down.
- **No level violation**: every edge is built-in→built-in or org→built-in-level (d7: same level or nearer built-in; `PackCompositionResolver.java:882-903`).
- foundation and writing must be `pack_level: built-in`. As org packs, built-in could not depend on them.
- Siblings at one level must partition exactly; a shared id is refused as `pack_sibling_conflict`.
- Qualified refs are `<pack-name>::<urn>` and must name a pack in the writer's transitive closure. Hence:
  - all 25 foundation→writing edges are relocated into writing's graph;
  - no edge targets built-in;
  - all 102 existing `built-in::` refs in the org packs are rewritten to `foundation::`/`writing::` (internal 62, qa 27, event-driven 7, spdd 6).
- The descriptor schema has no aggregation field; aggregation is `depends_on` only.

## 3. java-in-built-in trade-off (not decided)

- **(a) built-in aggregates java**
  - java is re-levelled to `pack_level: built-in` and becomes read-only to registration (ADR-0065).
  - Needs a charter ADR amending ADR-0053 d1/d3 and ADR-0048 d14 (stack packs are opt-in) and accepting d7's consequence.
  - Every built-in consumer then receives Java doctrine.
- **(b) java stays opt-in**
  - java is org-level and depends on foundation; no ADR change.
  - Consistent with the operator's rust/go ruling.
- **The split forecloses neither.** Moving to (a) later means one extra `depends_on` entry on built-in plus re-levelling java. Under the recommended "hold D in foundation", PR A takes the 4 java items out of foundation in either option.

## 4. Consumer impact / breaking

- **Core spec-kitty** fetches only `packs/built-in` at a pin and never follows `depends_on`. After the split it would see no profiles, mission types or templates. Core is already incompatible with main today (it refuses unknown descriptor fields).
  - Out of scope per AGENTS.md; recorded in the CHANGELOG/ADR as a known consequence.
- **Charter service deployers**: placing only built-in fails with `pack_dependency_unknown`; all three packs must be placed.
- **Third-party `built-in::X` qualifiers** fail with `pack_reference_artifact_missing`.
- **Ranges**: `<2` ranges fail once built-in becomes 2.0.0.
- **Not affected**: projects that use presets or bare ids (ids do not change).
- **Verdict:** breaking. built-in → 2.0.0 with a 💥 Breaking CHANGELOG entry and a migration note.
  - New packs start at 1.0.0.
  - Org packs move to `>=2.0,<3` and bump their own pack_version (ADR-0065 D2/D9).

## 5. Order of operations

1. Open PR #193 (edits built-in paradigms, manifest, digest) lands first, or the split rebases onto it.
2. Mint the ids; create the foundation and writing skeletons. Send the pack_id and branch to the orchestrator for PR B.
3. `git mv` the artifacts per the approved table. `missions/` keeps its name: renaming it to `mission_types/` is refused at the pin (`file-kinds.yaml:261`), so it is a follow-up.
4. Split the 14 graph files by source node; relocate the reverse edges into writing with qualified sources.
5. Rewrite built-in to an aggregator; move the policy and fallback settings.
6. Rewrite the 102 `built-in::` refs; bump the org packs' ranges and versions.
7. Tooling:
   - `charter_service_check.py`: stage every built-in-level pack (8-line diff, already proven passing in scratch).
   - Manifests: hand or tool member lists, restamped with `--regenerate-manifest`.
   - Digest covers the new layout.
   - `check_vocabulary.py:75`.
   - `test_language_profile_styleguides.py`, `test_software_dev_ascii.py`.
   - Land the #182 guard: a manifest-completeness check in `validate_pack()` for file-backed doctrine kinds, with unit tests. Fixes the git-flow and execution-lanes drift.
8. Docs: ADR, CHANGELOG 💥, README, packs/README, catalog/index, generated pack pages (each new pack needs a pack.md).

## 6. Gates (all green on main today)

| Gate | Status |
|---|---|
| `validate-packs.sh` | runs here; needs `CHARTER_CONTRACT_DIR` set locally |
| `check-built-in.sh` | runs here |
| `charter_service_check.py` | runs here: Java 25 at /usr/lib/jvm/temurin-25, jar built from the pin in about 5 min |
| `check_vocabulary.py` | runs here |
| `gen_pack_reference.py --check` | runs here |
| unittest per tests/ dir | runs here |
| docs-site build | **cannot run here** (npm 401 on @spec-kitty/doc-toolkit); rely on CI |

## 7. Proposed mission (WPs)

- **WP01** Pack skeletons: mint ids, foundation/writing pack.yaml/pack.md/README/PROVENANCE; built-in pack.yaml → aggregator. Early hand-off to the orchestrator.
- **WP02** Move artifacts (`git mv`) per the approved table, including the non-node files.
- **WP03** DRG split: per-pack graph files, edge relocation and qualification, policy/fallback; no dangling refs.
- **WP04** Org packs: rewrite the 102 `built-in::` refs, ranges, version bumps.
- **WP05** Tooling and guard: charter_service_check staging, manifests, digest, vocabulary/test fixes, #182 guard with tests.
- **WP06** Docs: ADR, CHANGELOG 💥 Breaking + migration note, READMEs, catalog/nav, generated pages.

Dependencies: WP01 → WP02 → WP03 → (WP04 ∥ WP05) → WP06.
