---
title: Changelog
description: Canonical changelog for the Spec Kitty Open Packs repository, following Keep a Changelog and Semantic Versioning.
doc_status: wip
updated: '2026-11-20'
---
# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to the Spec Kitty Open Packs repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **🚧 Pre-release.** This repository has no released version yet. It is bootstrapping the
> doctrine-pack marketplace direction in the open. Entries below record the scaffolding as it
> lands; pack boundaries and the manifest schema are still subject to change.

## [Unreleased]

### 💥 Breaking

- **The packs follow charter `main` at `33f3ad4`** (epic #287; #316, #309, #313). `charter.lock.yaml`
  moves from the `service-v0.1.0-rc.1` release to `33f3ad46e9e33e895d4cd3a077d928d91b4f025f`, charter
  `main` HEAD on 2026-11-20, pinned on demand because no service release carries charter #602, #554 and
  #600 yet. The round trip, the service registration and the schema gate are green at this pin.
  - **Tensions use charter's `tension` spelling** (#316; charter #602, ADR-0045). The six
    `in_tension_with` edges in the foundation pack are now `relation: tension`, each with the
    pack-owned, lexicographically smaller side as `source`. **Upgrade:** rename
    `in_tension_with` to `tension` in your graph shards and fragments.
  - **A file no rule models is a `file_not_held` warning, not a violation** (#309; charter #554,
    ruling Q1). `validate_pack_schemas.py` and `charter_service_check.py` warn it as the charter
    does: it is not held and not judged further. This includes a shard below the pack root
    (`drg/<kind>.graph.yaml`) and a `charter.yaml`. The charter's whole-pack round trip still names
    such files, so the packs here stay free of them.
  - **Foundation ships the default routing catalog** (#313; charter #600, ADR-0080).
    `foundation/routing_catalogs/default.routing-catalog.yaml` carries the model-to-task routing
    catalog in the charter's shape, and the built-in `default` preset selects it with a bare
    `activated_routing_catalogs: - id: default`. The schema mirror knows the `routing-catalog`
    kind.
- **The packs follow charter `main` at `050d780`** (epic #287). `charter.lock.yaml` moves from
  `eacbc3c` to `050d780876c6e9bd4265c7ec3335abe1b95cda61`, charter `main` HEAD on 2026-11-16. It
  holds glossary contexts (#106), slice F's kind taxonomy (#537, ADR-0077), the round trip in
  `pack-validation` (#555), slice G's profile selection (#538, ADR-0078) and identifiers on the
  shared slug grammar (#552). The pin refuses the old content, so the migrations below land
  with it in one pull request.
  - **Glossary packs become glossary contexts** (#283; charter ADR-0049, ADR-0076). Each
    `glossary_packs/<id>.glossary-pack.yaml` is now `glossaries/<id>.glossary.yaml`, with
    `schema_version: "1.0"`, a `name`, and terms carrying a minted `id`, `name` (was `surface`)
    and `avoid` (was `synonyms_to_avoid`); `confidence`, `introduced_in_mission` and `provenance`
    are gone. The four ids are kept (`spec-kitty-core`, `qa-glossary`, `evd-glossary`,
    `spk-internal-glossary`), and a term's address is `term:<context-id>/<term-id>`. The graph
    node is `glossary_context:<id>`, a fragment lists `glossaries`, and a preset activates them
    with `activated_glossaries`. `see_also` entries that named no term are dropped (three), and
    so is the `step contract` term. **Upgrade:** rename `activated_glossary_packs` to
    `activated_glossaries` in your presets, and address terms as `term:<context>/<term-id>`.
  - **Step contracts are folded into their steps' `substeps`** (#285 items 1 and 5; charter
    ADR-0077). The 28 `*.step-contract.yaml` files and the two `mission_step_contract.graph.yaml`
    fragments are gone; 149 substeps sit on 28 steps of the software-dev, plan, research,
    documentation and qa mission types. 115 substep ids now use `-` instead of `_`
    (`quality_gate` is `quality-gate`), and writing's 34 delegation candidates are written
    `foundation::<id>`. **Upgrade:** a pack that overrode or enhanced a step contract writes its
    change against the step's substeps.
  - **`human-in-charge` is human-performed, with the role `operator`** (#139; charter ADR-0078
    decision 4). `sentinel: true` becomes `performer: human`, and `role: human-in-charge` becomes
    `role: operator`; the five collaboration entries that named the role say `operator`. The
    profile id is unchanged. **Upgrade:** a profile or step that names the role
    `human-in-charge` names `operator`.
  - **Versions** (DIRECTIVE_018: a removed or renamed artifact raises the major). Major:
    `foundation` 2.0.0, `writing` 2.0.0, `built-in` 4.0.0, `qa` 4.0.0, `event-driven` 4.0.0,
    `internal` 4.0.0. Minor: `architecture`, `planning-analysis`, `refactoring` and `testing`
    2.1.0 (role references only); `cave-kitty` 2.2.0, `drupal` 2.1.0, `go` 1.1.0, `java` 2.2.0,
    `javascript` 2.1.0, `pack-authoring` 1.2.0, `python` 2.1.0, `rust` 1.1.0 and `spdd` 3.1.0
    (their `foundation`/`writing` range moves to `>=2.0,<3`). The built-in members stay pinned
    exactly and in lockstep (`==2.0.0`, `==2.1.0`; charter ADR-0048 decision 17). This carries
    the `foundation`/`writing` bump #285's slice A deferred.

- **Every pack registers against the charter's slice B: one `README.md` per pack, and no
  `org-charter.yaml`** (#241, #242; charter #451, #431, PR #501). `charter.lock.yaml` now pins
  charter `17ce3f9` (a commit pin; the charter has no release yet), which refuses `pack.md`,
  `PROVENANCE.md` and `org-charter.yaml` by name (`retired`) and cannot read a `pack.yaml` that
  declares `active_charter`.
  - Each pack's root `README.md` is its only document, held and served by the charter.
    `pack.md` is merged into it, and `PROVENANCE.md` is folded in as a `## Provenance` section;
    both files are gone from all 19 packs. The Level, `pack_id` and Depends-on bullets that
    restated `pack.yaml` are dropped. The generated pack pages take their Purpose from
    the README preamble, so the preamble holds only the description (contents and adoption
    move under H2 sections).
  - `org-charter.yaml` and `active_charter` are gone from the 12 packs that had them and from the
    valid example fixture. `internal`'s required lists (18 ids) are now `must_have: true` items
    of its governing `presets/base.yaml`, and its `skill_namespace` is dropped (the `kitty-`
    skill names are core's rendering). Org enforcement is a governing preset plus `policy.yaml`
    levels; the guides, contracts and Organisations pages say so and point at the charter's
    "Enforce presets on an organization's projects" guide.
  - Spec Kitty core still reads `org-charter.yaml`: until core aligns with the charter, a project
    that runs `internal` through core no longer sees its required lists or skill namespace, and core
    applies no `must_have`. Core then reports the committed `kitty-*` skill directories as orphaned,
    and `spec-kitty upgrade` would retire them: do not run it in a repository that relies on them
    until core aligns.
  - A new invalid fixture, `tests/fixtures/invalid/retired-pack-document`, proves the service
    refuses a pack that still ships `pack.md` or `PROVENANCE.md`.
  - `charter_service_check.py` uploads the README and no longer leaves out the retired files;
    `validate_pack_schemas.py` keys its descriptor pre-check on `README.md` and no longer allows
    `PROVENANCE.md`; `check_vocabulary.py` reads the qa provenance phrase from the README.
  - The core-seeded glossary's "Charter Pack" entry now says an org pack enforces activations
    through a governing preset.

- **`built-in` split into `foundation`, `writing` and nine opt-in bundles** (#73, epic #190;
  charter ADR-0048 decisions 12-14, ADR-0053 decisions 3 and 9; [ADR 2026-11-11-1](../architecture/adr/2026-11-11-1-split-built-in-into-foundation-writing-and-opt-in-bundles.md)).
  `built-in` 2.0.0 is now a distribution pack that holds no artifacts of its own. It depends on its
  members `foundation` and `writing` (exact `==1.0.0` pins) and keeps the `default` and `minimal`
  presets.
  - `foundation` holds:
    - the profiles: Generic Giannis (`generic-agent`, display name only), `implementer-ivan`,
      `reviewer-renata`, `analyst-annie` and `human-in-charge`;
    - the `software-dev`, `plan` and `research` missions;
    - every cross-cutting directive, with its procedures, tactics and toolguides, including the
      adversarial-review squad practice;
    - the fallback lock.
  - `writing` holds the documentation mission and the comms, docs and glossary doctrine.
  - Everything else ships as opt-in org packs: `testing`, `refactoring`, `architecture`,
    `planning-analysis`, `pack-authoring`, `python`, `javascript`, `drupal` and `java`.

  Artifact ids are unchanged. It breaks for:
  - a deployer who places `packs/built-in` alone. Composition is refused with
    `pack_dependency_unknown`; place `foundation` and `writing` beside it.
  - every `built-in::<urn>` reference. It no longer resolves (`pack_reference_artifact_missing`),
    because built-in holds nothing.
  - every `depends_on` range on built-in below 2.0.
  - anyone relying on specialist doctrine: the architect, planner, researcher, retrospective,
    debugger and stack profiles, DDD, C4, refactoring and BDD extras. It is opt-in now.
    - Activating such an id, or naming it in a preset, needs its bundle registered.
    - Projects on the `default` preset keep every mission running, but some steps change silently.
      Documentation `design` (role `architect`) and every `retrospect` step (role `facilitator`)
      fall back to Generic Giannis. Research steps (role `researcher`) go to a `writing` profile
      that lists it as an alt-role (`comms-cleo` or `synthesizer-sam`). Register `architecture`
      and `planning-analysis` to restore the specialists.
  - consumers of this repository's org packs. `internal`, `qa`, `event-driven`, `spdd` and
    `cave-kitty` are all bumped to 2.0.0 and depend directly on the packs they reference instead
    of on `built-in`, so their whole closure must be placed with them.
    - For example, `qa` needs `foundation`, `testing` and `planning-analysis`, and through those
      `architecture`, `refactoring` and `writing`. Placing `qa` alone is refused with
      `pack_dependency_unknown`.
    - `qa` also received the `sonar` toolguide, and `internal` four maintainer artifacts.
  - guidance that is gone even with every pack registered:
    - three profile-body references outside their pack's closure: `analyst-annie` →
      DIRECTIVE_047, `diagram-daisy` → USE_C4_MODEL_TECHNIQUES, and `implementer-ivan`'s operating
      procedure test-first-bug-fixing. Their graph edges survive, the body text does not.
    - five graph edges the charter service refuses across packs: `generic-agent` →
      USE_MUTATION_TESTING (the fallback is locked), and four edges from `planning-analysis` to
      file-less templates and anti-patterns in `architecture` and `writing`.
  - a third-party pack that overrides or enhances an id that moved into a bundle. It must now
    depend on that bundle, or it no longer reaches the artifact.

  spec-kitty core is out of scope here (AGENTS.md). If it bumps its pin as it is today, it breaks:
  - it fetches `packs/built-in/` alone, so it must fetch the members at the same pin;
  - it also hard-codes `researcher-robbie` and `architect-alphonso` as step defaults, which are
    now opt-in, and its fallback never chooses `generic-agent`, so software-dev `plan` and `tasks`
    would find no profile;
  - its pinned `packs/internal` now needs a larger closure.

  To stay on the old layout, pin the commit before this change or tag `v0.1.0`.

  **Migrate:**
  1. Place or fetch `foundation` and `writing` with `built-in`, at the same commit.
  2. Rewrite each `built-in::<urn>` to the pack that now holds it. The pack pages list each pack's
     artifacts, and `kitty-specs/foundation-writing-split-01M75HV3/membership.json` maps every one.
     Its keys are pack names, which differ from directory names for `quality-assurance` (`qa/`)
     and `spec-kitty-internal` (`internal/`).
  3. Replace a `depends_on` on built-in with the packs you actually reference. Each entry names the
     pack's `pack_id` (the ULID in its `pack.yaml`, also listed in `membership.json` `pack_ids`),
     with a range of `>=1.0,<2`.
  4. Place the closure of every pack you register: follow each `pack.yaml` `depends_on`.
  5. Register `architecture`, `planning-analysis`, `testing` and the stacks if you relied on their
     profiles or doctrine. The relocated graph edges come back with them; the three dropped
     profile-body references do not.

- **`built-in` now aggregates the core bundles** (#73; amendment of 2026-11-11 to
  [ADR 2026-11-11-1](../architecture/adr/2026-11-11-1-split-built-in-into-foundation-writing-and-opt-in-bundles.md)).
  Operator decision: built-in is the aggregate of the general-purpose open-packs.
  - `testing`, `refactoring`, `architecture` and `planning-analysis` move from `pack_level: org`
    to `pack_level: built-in` and are now members of `built-in`. Their ids and artifacts are
    unchanged.
  - Versions: those four go 1.0.0 → 2.0.0; `built-in` goes 2.0.0 → 3.0.0 and pins all six members
    exactly (`foundation` and `writing` `==1.0.0`, the four `==2.0.0`).
  - Org packs that depend on the four (`python`, `javascript`, `drupal`, `java`, `qa`, `internal`,
    `event-driven`, `spdd`) now require `>=2.0,<3` of them, and each takes its next major
    version because its `depends_on` changed: `python`, `javascript`, `drupal` and `java` go
    1.0.0 → 2.0.0; `qa`, `internal`, `event-driven` and `spdd` go 2.0.0 → 3.0.0.
  - The four bundles now declare `schema_version: "1.0"`, carry a generated `pack-manifest.yaml`,
    and no longer ship an `org-charter.yaml` (nor its `active_charter` pointer); like `foundation`
    and `writing`, they are not registered.
  - Everything else stays opt-in at org level: `pack-authoring`, `python`, `javascript`, `drupal`,
    `java`, `internal`, `qa`, `event-driven`, `spdd` and `cave-kitty`.

  **Migrate:**
  1. If you registered any of the four at org level, drop that opt-in: built-in-level packs are
     read-only and are not registered.
  2. Place `testing`, `refactoring`, `architecture` and `planning-analysis` beside `built-in`,
     `foundation` and `writing`, at the same commit.
  3. Change any `depends_on` range on the four from `>=1.0,<2` to `>=2.0,<3`, and any on built-in
     to `>=3.0,<4`.
  4. The `default` preset again reaches the architect, planner, researcher and retrospective
     profiles; the fallbacks listed in the entry above no longer apply once the four are placed.
  5. This supersedes step 5 of the migration in the entry above: do not register `architecture`,
     `planning-analysis` or `testing` at org level; place them with `built-in` as in step 2. Only
     the stacks (and `pack-authoring`) are still registered.

- **Packs migrated to charter ADR-0067/0068/0069** (charter #474; #69, #70). Every agent
  profile now declares one primary `role` plus optional `alt-roles` in place of `roles:`
  (`randy-reducer` is primarily a `refactorer`). Styleguide `principles` are named
  `{name, description}` items; descriptions over 255 characters were condensed and their full
  text kept as a same-named entry in `patterns`. The built-in pack declares
  `fallback_profile: generic-agent`, now role-neutral (`role: generic`) and locked by a new
  `policy.yaml`. The stale `.github/agents/*.agent.md` bootstrap copies are removed.
  `charter.lock.yaml` moves to #474's merge commit `fb24052`.

- **SPDD/REASONS moved from `built-in` to the opt-in `spdd` pack** (#73, charter
  ADR-0066). The paradigm, directive, two canvas tactics and canvas-writing
  styleguide moved with five new step enhancements. The `software-dev` specify,
  plan, tasks, implement and review prompts now declare only an empty
  `spdd:reasons-block` slot; their former guidance lives in Markdown fragment
  companions in `packs/spdd`. Existing consumers must configure `spdd` and
  activate its `spdd` preset to restore the doctrine and prompt guidance. The
  renderer must support ADR-0066 fragments; older core versions render the base
  prompts without the SPDD blocks.

- **Four built-in paradigms have been reclassified or retired** (#65). Consumers that select these paradigms must migrate their selections and graph URNs:
  - `paradigm:git-flow` is now `procedure:git-flow`.
  - `paradigm:shared-branch-ci` is retired; use `paradigm:trunk-based`, which now includes its shared-branch CI and staging guidance.
  - `paradigm:execution-lanes` is now `toolguide:execution-lanes`.
  - `paradigm:extract-then-publish-separation` is retired; use `procedure:meeting-minutes-pipeline`, which carries the separation as an invariant.
  `semantic-compression` remains a paradigm. Core needs a coordinated open-packs pin bump with updates to cached charters, generated snapshots, and tests that reference the old ids. See [Use a Charter Pack](../guides/use-a-charter-pack.md#migrate-reclassified-built-in-paradigms).

- **The packs follow strict composition, and the as-is CLI is no longer supported** (#118,
  [ADR 2026-11-04-1](../architecture/adr/2026-11-04-1-strict-pack-composition-and-the-end-of-cli-compatibility.md)).
  Every pack now has a `pack.yaml`, the org packs declare `depends_on` on `built-in` at `>=1.0,<2`,
  and their references to `built-in` are qualified. The CLI rejects `depends_on`, so a project that
  registers `internal` or `qa` loses its whole org DRG layer, and only `charter status`'s
  `org_layer.errors`, `charter org validate` and `doctor charter-packs` say so.
  What a consumer must now do:
  - On the as-is CLI, pin the tag `pre-charter-cutover`, the last semi-compatible commit.
  - On the charter service, configure `built-in` with any pack that depends on it. `quality-assurance`
    is the name and qualifier of the pack in `packs/qa`.
  - In your own pack, qualify references to another pack's artifact: `<pack>::<kind>:<id>` on a graph
    edge and `<pack>::<id>` in a typed reference's `id`. A pack with no `pack.yaml` is refused.
  - If you read the six `built-in` asset sidecars, their `path` is now relative to `assets/` (#75).

- **Packs no longer target the old core** (charter service swap-over). Pack validation now
  follows `contracts/packs` on `spec-kitty-charter` `main`, rather than a pre-merge branch,
  and the built-in record drops its `requires_core` version range. Compatibility with core
  4.0.0rc8 and earlier is not supported.

- **Procedures and toolguide guides in `built-in`, `internal` and `qa` now use the charter's
  sanitized shapes** (#91, spec-kitty/spec-kitty-charter#194). Procedures changed `name` to
  `title`, `purpose` to `description` and `actor` to `role`; toolguide guides were renamed to
  `<id>.guide.md` with fixed sections. Core up to 4.0.0rc8 still requires the old fields and
  rejects the 39 migrated procedures as `schema_invalid`. A consumer on a released core who pins
  a commit after this one loses those procedures. CI no longer depends on core, so it stays green
  (see Changed).

### ✨ Added

- **`/spec-kitty.analyze` reviews the whole planning corpus and product coherence** (#213, #214,
  #247; epic #244). Before, the software-dev `analyze` step read only the spec, the plan, the tasks
  and the WP prompts. Now it also does the following.
  - It reads every artifact the `check-prerequisites` inventory lists (the feature directory itself
    excluded), the `meta.json` creation intent, `occurrence_map.yaml` and the recorded decisions,
    headings first. Pass H (`X` findings, tactic `planning-corpus-consistency`) reports decisions in
    `research.md`, `plan.md` and the recorded decisions that no task implements, gaps between the
    data model, the contracts and the quickstart, and work no artifact grounds. These findings keep
    their normal severity.
  - Pass J (`M` findings, tactic `product-coherence-review`) judges intent drift, the MVP slice, the
    vertical slice, overbuild, lost scenarios, sequencing and grouping. Its findings are capped at
    MEDIUM, so they never block the verdict. The step ends in one `Recommendation:` line (`revise
    spec`, `revise plan`, `revise tasks` or `proceed`); a fixed owner rule picks the artifact to revise.
  - **Findings stay deterministic and single-owner.** Scenario rows that are only context
    (accepted, rejected) no longer become findings; the `Inferred:` label sits in the carrier
    summary and the table cell. Table rows sort by step then id number, and an overflow past 50 rows
    keeps every HIGH and CRITICAL row. A task mapped to nothing stays pass E's `C` finding. A missing
    inventory is reported, never read as "no planning artifacts".
  - **The recommendation follows a fixed owner rule.** Coverage, validation and WP findings go to
    tasks, other findings to the artifact they cite, and every planning artifact other than the spec
    and `meta.json` goes to plan. A ready mission says `proceed` unless a MEDIUM `M` finding exists.
    The report carries exactly one `Recommendation:` line.
  - **The MVP is read, not forced.** `/spec-kitty.tasks` records it in tasks.md's MVP Scope note;
    the split tasks flow generates tasks.md, so a missing note is a LOW finding that cannot force a
    revise. Setup work packages the MVP slice needs are not scaffolding. Editing a planning
    artifact the staleness check does not track still means re-running analyze.

  cave-kitty's `cave-dev` analyze step names the same checks. The analyze step still changes nothing
  but `analysis-report.md`, and the only `finalize-tasks` form it names is `--validate-only`.
  The change is additive (DIRECTIVE_018).
  **Versions:** `foundation`, `writing`, `testing`, `refactoring`, `architecture` and
  `planning-analysis` 3.2.0 → 3.3.0 with the exact pins following, `built-in` 5.2.0 → 5.3.0 and
  `cave-kitty` 2.3.0 → 2.4.0. The `foundation` range in `cave-kitty` tightened from `>=2.0,<4` to
  `>=3.3,<4`, because its fragment now scopes tactics that exist only from foundation 3.3.0.
  **What to do:** nothing in your packs. A consumer that pins `cave-kitty` 2.4.0 needs `foundation`
  3.3.0 or later.
- **Tests may mock only at the responsibility boundary** (#216). A new `foundation` `DIRECTIVE_054`
  holds the allow-list of seams a test may substitute; collaborators the code owns run for real. The
  new `unfake-an-over-mocked-test` procedure turns an over-mocked test into one that does. Both load
  at the implement and review actions and for the implementer, reviewer, generic and qa test-designer
  profiles. Before, the seam lists in the testing tactics and styleguides differed; now they agree
  with the directive. The remaining #216 items (the tests-as-scaffold paradigm and the DIRECTIVE_041
  mindset split, the anti-pattern nodes and reference assets, checklist de-duplication, the curator
  profile) stay open.
- **A red that proves the right thing** (#151). `red-first-bug-reproduction` records the failure text,
  inverts a test that pins the defect, and splits a reproduction from its fix with a strict expected
  failure. Before, a red could pass for the wrong reason. `acceptance-test-first` now has each new acceptance test run on the base with its failure text recorded, so an anchor that is red for a missing symbol or an unstaged version bump is caught.
- **Review now fails doubles of owned logic and new change-detector tests** (#216, #209). The
  software-dev review step fails a test double on code the system under test owns, and fails a new
  test that only restates configuration; a touched existing one may be retired once its evidence is
  recorded. It also checks that the cited run or gate exists and exercises the changed configuration. Configuration that encodes security or permission policy is
  exempt from the change-detector check; it takes red-first or a repository-wide policy check.
- **The spec template and the specify prompt carry the evidence labels** (#209). Requirement rows gain
  the `[evidenced-by-run]` delivery label and the `n-a` no-op mark, defined in the
  `acceptance-criteria-non-vacuity` tactic.
- **Two new glossary terms** (#216, #209): "responsibility boundary" and "change-detector test".
- **`internal` carries two worked examples**: a CI workflow for the evidence rule above, and the core
  release-step incident for the mock-boundary rule, which no longer ships in `foundation`. Its `foundation`
  range narrows to `>=3.2,<4`, since its content cites the 3.2 rules.
- **Packs that use the new rules need `foundation` 3.2** (#216, #209, #151). `DIRECTIVE_054` and the narrowed `DIRECTIVE_036` rule say so
  themselves: they bind the tests a change adds or modifies. An existing test that does not conform is
  fixed when a change touches it, or recorded as a follow-up, so existing tests stay conforming and the
  change is additive (DIRECTIVE_018). The bumps are minor and lockstep:
  `foundation`, `writing`, `testing`, `refactoring`, `architecture` and `planning-analysis`
  3.1.0 → 3.2.0, `built-in` 5.1.0 → 5.2.0, `qa` 5.0.0 → 5.1.0 (its `foundation` range narrows to
  `>=3.2,<4`, since it cites `DIRECTIVE_054`), and `internal` 4.1.0 → 4.2.0 (its `foundation` range
  narrows to `>=3.2,<4`). `python` and `drupal` take a minor bump, 2.1.1 → 2.2.0: their `foundation`
  range also narrows to `>=3.2,<4`, since `python-pedro` cites `DIRECTIVE_054` and `drupal-dries`
  cites the carve-out. Narrowing the lower bound within the same major (`qa`, `internal`, `python`,
  `drupal`) is a minor, not a major: the 3.1 combination is superseded, not broken, because the new
  content only adds rules. A `depends_on` that moved to a new major, as in the earlier major-version
  entries, breaks the old combination and is a major. **What to do:** a consumer that pins `foundation` 3.1 must move to 3.2 to take `qa` 5.1, `internal` 4.2, `python` 2.2 or `drupal` 2.2.

- **`/spec-kitty.analyze` checks implementation readiness** (#246, #237, #247; epic #244). The
  software-dev `analyze` step now does three more things before it gives a verdict:
  - It runs `spec-kitty agent mission finalize-tasks --validate-only` and reports what it finds.
    A refusal (unmapped or unknown requirements, `tasks.md` and WP files that don't pair, dependency
    cycles, overlapping ownership between parallel WPs, invalid WP metadata) is CRITICAL. Stale
    finalization is HIGH. The step never runs a writing `finalize-tasks`.
  - It reviews every `tasks/WP*.md` prompt against the WP prompt template the Mission resolves, and
    reports per WP what blocks implementation and what would only improve it.
  - It judges the requirements: testable, solution-free, unambiguous, consistent and complete. It
    reads behavioural requirements against the EARS patterns, audits the scenarios of each user story,
    and writes clarification questions with concrete answer choices. Findings reached by judgement
    are labelled `Inferred:`.

  The report has a fixed section order and fixed finding-id prefixes, so a rerun on unchanged
  artifacts gives the same ids. Two new `foundation` tactics hold the checklists:
  `requirement-quality-ears`, which the specify step also cites when requirements are written, and
  `wp-prompt-readiness-review`. cave-kitty's `cave-dev` analyze step names the same checks. The
  change is additive (DIRECTIVE_018), so the bumps are minor and lockstep, and the exact pins follow:
  `foundation`, `writing`, `testing`, `refactoring`, `architecture` and `planning-analysis`
  3.0.0 → 3.1.0, `built-in` 5.0.0 → 5.1.0, and `cave-kitty` 2.2.2 → 2.3.0.
  **What to do:** nothing in your packs. An agent running analyze needs spec-kitty CLI >= 3.1.0a5,
  where `--validate-only` writes nothing. On an older CLI, or with no CLI, analyze does not run the
  check: it records a HIGH finding, and the verdict is blocked.
- **Three ADRs record decisions that lived only in pull requests and issues** (#295, epic #287).
  ADR 2026-11-19-1 records charter slice B (#241, #242, PR #248): `README.md` is the pack
  document, and `pack.md`, `PROVENANCE.md`, `org-charter.yaml` and `active_charter` are retired.
  ADR 2026-11-19-2 records charter slice F (#285, PRs #289 and #293; charter ADR-0077): step
  contracts fold into steps, steps are linked from mission types, and delegations are scoped.
  ADR 2026-11-19-3 records the pin policy (operator ruling, 2026-11-18): `charter.lock.yaml` pins a
  charter release by default and charter `main` only on demand, superseding the 2026-11-16
  lockstep with `main`. It also records the 2026-11-16 ownership ruling: the charter owns the pack
  logic, core assembles, and pack repositories own the content. No earlier ADR is superseded.
  ADR 2026-11-11-1's existing slice F amendment now points to ADR 2026-11-19-2.
  The vision and the roadmap's Charter pin theme, last changed on 2026-11-18 without their
  `updated:` moving, were verified against the pin policy: the pin moves with charter releases, the
  scheduled job bumps on a release, and both link ADR 2026-11-19-3.
- **A contributor path for outside pack authors** (#296). The new guide
  `docs/guides/contribute-a-pack.md` covers the proposal issue, `pack_id` and `name` identity,
  the local checks and gates, review and landing, and warns that the pack contract still changes
  often. `README.md`, the contributing guide and the guides index link it. The Pack proposal issue
  template asks for the `name` qualifier and the canonical home, and the pull request template
  gains a "New pack" checklist.

- **The packs are checked against charter `main` every night** (#311). `charter-track.yml` gains a
  nightly main track: at 02:23 UTC, apart from the release track's 05:41, it runs the on-demand
  track's checks, the round trip included, against charter `main` built from source. It reports only:
  it never bumps the lock and is not a required check. From `main`, a red run opens or rewrites one
  `charter:main-red` issue naming the charter commit and the failing jobs' errors, and a green run
  closes it; the release track's `charter:release-red` issue is untouched. A dispatch with
  `track: main` runs it on demand. This restores charter ADR-0070's "nightly, non-blocking
  open-packs run against charter `main`", which charter's retired `open-packs-drift.yml` used to run.

- **The bump pull request is opened with `PR_CREATION_TOKEN`** (#314, operator ruling). The
  organization does not let GitHub Actions create pull requests, so the release track's bump job no
  longer depends on that setting. The job's own token, with `contents: write` on that job only, pushes
  the bump branch and its signed commit. The repository secret `PR_CREATION_TOKEN`, a fine-grained PAT
  with Actions and Pull requests read and write and no Contents access, opens the pull request and
  closes a superseded one. Opened that way, the bump pull request runs its own required check, so the
  `validate-packs.yml` dispatch that stood in for it is gone, and so is the optional
  `CHARTER_BUMP_TOKEN`. Without the secret, the bump job fails before it pushes anything, naming it.

- **The charter pin follows charter releases on its own** (#253, epic #287). A daily
  `charter-track.yml` lists the charter's releases and checks the newest `service-v*` release or
  pre-release that is newer than `charter.lock.yaml`. It runs the required check's own jobs with that
  release's jar, checked against its `.sha256` asset, and with `commit` set to the tag's commit. From
  `main` only, a green run opens one bump pull request with the re-derived manifests, digests and pack
  pages; a red run opens one `charter:release-red` issue that names the failing jobs' errors. On
  demand (a dispatch with `track: ref` and `charter_ref`, default `main`, or the `charter:head` label
  on a pull request), the same checks, the round trip included, run against charter source and only
  report. `validate-packs.yml` takes the charter target as `workflow_call` inputs, and
  `scripts/ci/charter_pin.py` resolves and applies one. While a bump pull request is open, the track
  does not check its release again, and it closes a red issue once the lock passes that release. This
  replaces charter's `open-packs-drift.yml`, which spec-kitty/spec-kitty-charter#604 is to retire once this lands.

- **The glossary contexts carry core's docs/context terminology, and "Op" is defined** (#221, #234;
  epic #288). Core's `docs/context/` pages (at core `01e577d`) defined about 290 terms that no
  shipped glossary held. Each of the 297 source terms now has a recorded verdict and reason in
  `kitty-specs/glossary-docs-context-terms-01M7PN2S/research/ledger.yaml`.
  - **foundation** (`spec-kitty-core`, 139 → 295 terms) gains 156 consumer-facing terms: the
    charter, activation and DRG-relation vocabulary, Mission topology, branches, lanes and gates,
    the dossier, decisions and events, the four mission types, and the foundational technology
    terms (API, CLI, UI, Markdown, YAML, JSON, SHA256) that the writing pack's glossary styleguide
    requires. Definitions cite no core source path, test, ADR or issue; where core describes a
    surface the charter retired (the org charter, `required_<kind>`, `activated_glossary_packs`,
    step contracts, `mission-runtime.yaml`), the definition follows the charter.
  - **`op`** (#234) is the dispatched, governed ad-hoc unit of work of DIRECTIVE_053: alias
    `profile invocation`, see also `mission`.
  - **internal** (`spk-internal-glossary`, 12 → 91 terms) gains 79 house terms: core's code
    symbols, architectural test gates and pytest markers (ids ending `-test-marker`), tracker
    labels, product lines, retired hosted vocabulary and the tool-vs-agent naming record.

- **A roadmap in the docs: a new Plans section** (ADR 2026-11-16-1). `docs/plans/roadmap.md` is
  one living page with a section per theme (charter lockstep, pack content quality, doctrine from
  core, catalog shape and publication, docsite and trust). Each section gives the goal it serves,
  quoted from the vision or charter, its horizon (Now, Next or Later), its exit criteria and an
  `Epics:` line; every open epic is named on exactly one. Progress stays in the tracker
  (`DIRECTIVE_044`); rendering it on the docsite is planned in doc-kitty#350.
- **The validator refuses a `specializes_from` cycle among agent profiles** (#286; charter
  ADR-0078 decision 2). `--cross-pack` names each cycle in order (`a -> b -> a`) across all
  packs; the charter refuses one only within the closure it registers. A profile may have
  several parents. Open-packs has no cycle.
- **`implementer-ivan` routes CI work** (#301; companion to core spec-kitty#7697, PR
  spec-kitty#7707). The profile's `domain-keywords` add `ci`, `ci matrix`, `ci pipeline`,
  `github actions`, `github workflow` and `continuous integration`, so core's dispatch router
  sends CI and workflow requests to it. No other profile declares these keywords, and none of
  their tokens is a router stop-word. The change is additive (DIRECTIVE_018), so the bumps are
  minor and lockstep, and the exact pins follow: `foundation` 2.0.0 → 2.1.0, `writing`
  2.0.0 → 2.1.0, `testing`, `refactoring`, `architecture` and `planning-analysis` 2.1.0 → 2.2.0,
  and `built-in` 4.0.0 → 4.1.0.

- **Every mission step is linked from its mission type, every delegation candidate is scoped,
  and foundation has a work-package lifecycle with the pre-review guard** (#285 items 2 to 4;
  charter slice F, ADR-0077). These are additive and valid at the current pin. They prepare the
  pin move, which refuses an unlinked step (`mission_step_unlinked`) and an unscoped candidate
  (`substep_delegation_unscoped`).
  - 26 `mission_type:<t> -requires-> action:<t>/<s>` edges, so each of the six mission types
    links every step and on-demand step: cave-dev 8, qa 7, software-dev 8, research 2,
    documentation 1 (plan was already complete). 23 of their targets get a new `action` node:
    cave-dev 8, qa 7, software-dev 7, research 1.
  - 79 `scope` edges from a step's action to each step-contract delegation candidate that had
    none (80 uses: foundation 47, qa 18, writing 14; writing's targets are `foundation::`).
    `scope` puts the candidate in force for that step's context. The delegation already named
    it, so this is intended.
  - foundation: guard `spec-kitty-pre-review` (`builtin:spec-kitty-pre-review`,
    `on_indeterminate: pass`) and lifecycle `work-package` with core's nine lanes. The guard runs
    on `in_progress -> for_review` (charter ADR-0054 decision 12). The software-dev `review` step
    contract keeps its `gates[]` entry until the fold (#285 item 1) retires the contract.
  - `qa` moves to 3.1.0 and `cave-kitty` to 2.1.0 (additive, DIRECTIVE_018). `foundation` and
    `writing` stay at 1.0.0 for now: six packs pin them exactly, released in lockstep, so their
    bump is left to the operator's call on #285.

- **`pack-authoring` styleguide `doctrine-instruction-voice`** (#275): canonical glossary terms in
  instructions, no unauthorized high-risk operation in an example, and roles instead of one
  project's local values. `pack-authoring` moves to 1.1.0.

- **Every pack has a recorded tree digest** (#194, epic #190; see also #23 and #19;
  [ADR 2026-11-11-2](../architecture/adr/2026-11-11-2-record-a-tree-digest-for-every-pack.md)).
  Each `packs/<name>/` now has a sidecar `packs/<name>.source.yaml`, and the required gate checks
  all of them with `scripts/ci/check-pack-digests.sh` (formerly `check-built-in.sh`), failing on a
  stale, missing or orphan sidecar. `python3 scripts/ci/pack_digest.py --update` restamps them.
  `scripts/ci/built_in_digest.py` stays as a compatibility entry point, and
  `packs/built-in.source.yaml` keeps its path and keys.
  - Release archives now ship each pack's sidecar as `<pack>-vX.Y.Z.source.yaml`.
  - Manifest node guard (residual of #182): `scripts/ci/validate_pack_schemas.py` fails a
    `pack-manifest.yaml` that omits any graph node its pack declares, except actions,
    anti-patterns, templates, mission types and step contracts. An unknown node kind fails closed.
  - For consumers: nothing changes for core. The `.source.yaml` release assets are informational
    and are not core pins. A release now has 3 assets per pack, so check any tooling that counts or
    globs assets. Tags cut before #194 cannot be rebuilt by the current `release_assets.py`; their
    published `.sha256` stays authoritative.
  - For contributors: every pack edit needs `python3 scripts/ci/pack_digest.py --update` in the
    same commit, and the script needs pyyaml. The `check-built-in.sh` wrapper was removed; `built_in_digest.py --check` remains.
    Only git-tracked files are hashed, so `git add` a new file before restamping.
- **`rust` Charter Pack** (`packs/rust/`, #191, epic #190). This is an opt-in org pack with Spec Kitty-authored MIT
  doctrine for any Rust codebase:
  - the `rust-conventions` styleguide: validated newtypes, parsing at the boundary, `thiserror` in
    libraries and `anyhow` at binary edges, money as a decimal or a currency-carrying minor-units
    type and never a float, exhaustive matches, and documented `unsafe`;
  - the `rust-review-checks` toolguide: `cargo fmt`, `clippy -D warnings`, tests, `cargo doc` and
    `cargo deny` / `cargo audit`, cheapest first;
  - the `rust-ruben` implementer profile, which requires the conventions;
  - a `rust` preset.

  It depends on `foundation` and `testing`, and `built-in` does not aggregate it (#73).
  `PROVENANCE.md` records the seed idioms it was re-authored from and how their contradictions
  were resolved.

- **`go` Charter Pack** (`packs/go/`, #192, epic #190). This is an opt-in org pack with Spec Kitty-authored MIT
  doctrine for any Go codebase:
  - the `go-conventions` styleguide: typed constants with a validated parse, errors wrapped with
    `%w` and matched with `errors.Is`/`errors.As`, `context.Context` first, explicit dependencies
    instead of package globals, money never `float64`, `defer` for cleanup, and owned goroutines;
  - the `go-review-checks` toolguide: `gofmt`, `go vet`, staticcheck or golangci-lint,
    `go test -race`, fuzzing and `govulncheck`, cheapest first;
  - the `go-gwen` implementer profile, which requires the conventions;
  - a `go` preset.

  It depends on `foundation` and `testing`, and `built-in` does not aggregate it (#73).
  `PROVENANCE.md` records the seed idioms it was re-authored from and how their contradictions
  were resolved.

- **Manifest-completeness guard** (#182). In a pack that ships a `pack-manifest.yaml`, the pack gate
  now fails when a file-backed doctrine artifact is not a constituent, and names the file. The kinds
  checked are profiles, directives, tactics, procedures, paradigms, styleguides, toolguides, assets,
  glossary packs, skills, guards and lifecycles. The `git-flow` procedure and the
  `execution-lanes` toolguide had shipped unlisted; they are listed now, in `foundation`.
  `scripts/ci/charter_service_check.py` now stages every built-in-level pack and registers org
  packs dependencies first (#73). The nine opt-in bundles carry no manifest, so the guard
  does not cover them, as before for org packs.

- **Every paradigm now states its principles** (#66, charter ADR-0067). All eleven paradigms carry an
  ordered `principles` list of `{name, description}` items in the style of Kent Beck's Test Desiderata,
  explaining why the practices each paradigm brings in belong together. `brownfield-onboarding` is
  ratified: its draft marker is gone and the open question on escalating "document and transfer first,
  then refactor" to a directive is kept. The authoring guide and artefact index now say paradigms should
  state principles.
- **Every pack is validated through the charter service in CI** (charter ADR-0070, #188). A new
  `Charter service validation` job in `validate-packs.yml`, required by `Validate packs gate`, builds
  the charter service at the commit pinned in the new `charter.lock.yaml` (or downloads its release
  jar, checked against `jar_sha256`, once the charter publishes one) and drives it with
  `scripts/ci/charter_service_check.py`: `GET /offering` must compose every pack, every org and
  project pack must register whole, and every pack under `tests/fixtures/invalid/` must be refused
  with the code its new `expected-code` file names. `charter.lock.yaml` is now the one charter pin;
  `validate_pack_schemas.py` reads its schema commit from it and fails closed unless it is a full
  commit. Two fixtures carry `expected-code`: `legacy-shapes` (now with a `pack.yaml`, so it is
  refused for its files, not for a missing descriptor) and the new `unknown-dependency`. The pin is
  charter `main` at `f4acac9`: the packs validate there unchanged, and at the previous schema pin
  (`55c7d82`) the service refuses the registration of `spdd`, whose step enhancements it did not yet model.

- **Every pack now authors a `pack.md` — the charter's pack description — and the generated
  reference pages render it** (#21). The charter contract maps `*/pack.md` to the
  `pack-document` schema and calls it "A pack's description" (charter #260, ADR-0042 decision 8);
  the closed `pack.yaml` descriptor schema declares identity and lineage only, so `pack.md` is
  the description carrier. `scripts/docs/gen_pack_reference.py` now publishes each pack's
  `pack.md` preamble under the page's Purpose heading instead of the "no such field" note
  (a pack without a `pack.md` still falls back to it). `cave-kitty`, `event-driven`, `internal`,
  `qa` and `spdd` gain an authored `pack.md`; `built-in`'s moves its authored/generated note
  under an H2 so its preamble is purely descriptive (its tree digest is re-recorded). The
  authoring guide now documents the `pack.yaml` / `pack.md` / `pack-manifest.yaml` split.

- **Every `plan` mission action now scopes the tactics named by its prompt** (#143, #141). The specify, research, plan and review effective action contexts no longer resolve empty; each receives doctrine through direct `scope` edges in `packs/built-in/action.graph.yaml`, rather than relying on mission-type scope or template edges that are absent from the charter's effective graph. The same orphan adjudication connects deployable-skill authoring to external-agent onboarding and gives the lexical profile a `vocabulary` edge to the Spec Kitty glossary.

- **Agent-profile references to another pack are qualified and guarded** (#119, charter
  ADR-0053 decision 7). The 24 references in `packs/qa/agent_profiles/*` that resolve only in
  `built-in` — 13 `tactic-references`, 6 `styleguide-references`, 1 `toolguide-references` and
  4 `operating-procedures` — are now written `built-in::<id>`; references inside one pack stay
  bare. `validate_pack_schemas.py --cross-pack` now refuses an agent-profile reference that is
  bare but held only by another pack or by no pack, qualified with the profile's own pack
  (references inside one pack stay bare), with a pack outside the referrer's `depends_on`
  closure, or with an id the named pack does not hold — edge ends and profile selection
  fields judged alike, `directive-references` codes included (a directive's code is its id or,
  as built-in cites its own, the number after `DIRECTIVE_` in it).

- **The internal test-quality scanner supports Java/JUnit suites** (#115). One
  asset now discovers and ranks Python/pytest and Java/JUnit 4 or 5 tests,
  including Java weak-oracle and test-smell mappings, git window scans and
  package-based ledgers. Java parsing uses exact, lazily imported tree-sitter
  pins declared in PEP 723 metadata; Python-only scans remain standard-library
  only. The sidecar title, toolguide, assessment procedure and generated pack
  reference state the supported languages.
- **The Java test-quality scanner rejects non-ArchUnit checks, empty AssertJ chains and redundant exception null checks as value assertions** (#172).

- **Cloud-session orchestration rules are binding** (#76). The internal
  `CLOUD_SESSION_ORCHESTRATION` directive makes sibling read-only boundaries,
  orchestrator-mediated writes, blocked-session replacement and just-in-time shared
  numbering required charter content for cloud dispatch and semi-auto delivery.

- **Cloud dispatch now bounds multi-runner fleets** (#106, #76). The internal
  `cloud-session-dispatch` procedure and cloud mode of the `semi-auto` skill set WIP limits,
  staggering and collision rules, environment probes and pin checks, settled dispatch conventions,
  batched decisions, and an orchestrator status record. Runners check tooling before the single
  documented install fallback, keep sibling clones read-only, route `<repo>#TBD-<slug>` drafts back
  through the orchestrator, replace blocked sessions, and reproduce a missing squad as parallel
  profile-loaded lens subagents.

- **Built-in `typescript-conventions` styleguide** (#131). Conventions for TypeScript code: a strict
  type-check gate, naming, named exports, `unknown` over `any`, no unchecked assertions,
  discriminated unions, promise ownership and RxJS stream discipline, with patterns,
  anti-patterns and tooling. Paraphrased from, and checked against, the Google TypeScript Style
  Guide, ts.dev, the TypeScript docs, typescript-eslint, Codewalkers' tooling page and the RxJS
  guide; rules with no source are marked as house rules. Shaped after the penguin-pragmatic-patterns
  primers.

- **Built-in `css-conventions` styleguide** (#131). Conventions for CSS, with the emphasis on media
  types and media queries: intrinsic layout first, mobile-first `min-width` queries, content-driven
  breakpoints in `em`, only the `all`, `screen` and `print` media types, print styles, user-preference
  and input-capability media features, plus naming, specificity and formatting rules. Paraphrased
  from, and checked against, the Google HTML/CSS Style Guide and MDN (media queries, @media,
  printing, user-preference features, container queries, @layer and !important); rules with no
  source are marked as house rules.

- **Built-in `html-conventions` styleguide** (#131). Conventions for HTML: the document skeleton
  and viewport, elements used for their purpose, landmarks, validity, separation of structure,
  presentation and behaviour, alt text, labelled controls, native semantics before ARIA, and
  formatting. Paraphrased from, and checked against, the Google HTML/CSS Style Guide, MDN, W3C
  ARIA in HTML and Using ARIA, the WAI tutorials and the ARIA Authoring Practices; keeping
  optional tags is a stated deviation from Google. It suggests `css-conventions` as its companion.

- **`frontend-freddy` and `node-norris` require their new conventions styleguides** (#131).
  `frontend-freddy` now `requires` `typescript-conventions`, `html-conventions` and
  `css-conventions`; `node-norris` `requires` `typescript-conventions`. The language-profile test
  maps the three languages and exempts only `javascript`, which the #131 ruling left open.

- **`pr:pause-ci` pauses a parked pull request, and `Validate packs gate` is the one required check**
  (#106, ADR 2026-11-01-1). There is no merge queue: in core it duplicated CI runs rather than
  avoiding reruns.
  - `validate-packs.yml`, behind the one required check `Validate packs gate`, also runs the
    generated-pack-page drift check, so two pack changes that drift once combined fail on the push
    to `main`.
  - `main` runs and release runs never cancel each other.
  - On a pull request labelled `pr:pause-ci`, validation is skipped and the gate fails. Adding the
    label cancels the running check, and removing it runs CI again. The gate reads the labels as
    they are now, so a run that started before the label was added cannot pass a paused pull
    request. `release.yml` grants the workflow it calls `pull-requests: read` for that read.
  - `tests/ci/test_workflows.py` checks these properties against the parsed workflows, and that
    every action is pinned to a full commit SHA.
  - The required-check setup is in the contributing guide.

- **Cross-pack checks run over all packs together in `validate-packs.sh`** (follow-up to #102).
  The retired `doctor charter-packs` also judged packs against one another; the schema
  validator only judged each pack alone. `validate_pack_schemas.py --cross-pack` now fails on a
  preset that names an id no pack declares (for example `DIRECTIVE_999`), on a DRG fragment edge
  endpoint that resolves to no node of any pack, and on one `(kind, id)` declared by two packs.
  Core flags a higher layer shadowing a lower one; here each pack is its own layer, so any shared
  id is a collision and there is no sanction list. The check fails closed when no pack declares a
  node. All packs pass; the only violation found was the `example-pack` fixture, whose fragment
  declared no nodes for the directive and tactic its preset and edge name, which now has them.

- **Cross-pack checks run over all packs together in `validate-packs.sh`** (follow-up to #102).
  The retired `doctor charter-packs` also judged packs against one another; the schema
  validator only judged each pack alone. `validate_pack_schemas.py --cross-pack` now fails on a
  preset that names an id no pack declares (for example `DIRECTIVE_999`), on a DRG fragment edge
  endpoint that resolves to no node of any pack, and on one `(kind, id)` declared by two packs.
  Core flags a higher layer shadowing a lower one; here each pack is its own layer, so any shared
  id is a collision and there is no sanction list. The check fails closed when no pack declares a
  node. All packs pass; the only violation found was the `example-pack` fixture, whose fragment
  declared no nodes for the directive and tactic its preset and edge name, which now has them.

- **A `qa` preset activates the qa mission type and its five agent profiles** (#97). A mission
  type names roles, not profiles (charter ADR-0032), so `packs/qa/presets/qa.yaml` is how a
  project puts the QA profiles in force. It is the first preset in the charter's sanitized
  preset shape (ADR-0042: `schema_version`, `id`, item objects). On core up to 4.0.0rc8, which
  reads only the old shape, `spec-kitty charter pack list` and
  `spec-kitty charter activate --pack qa` fail with `PRESET_INVALID` for any project that
  registers the qa pack. Those projects need a core that reads the sanitized shape, or must not
  register qa.
- **Mission steps declare their preconditions** (#99). Where a step needs an earlier step's
  artifact, it lists it under `expected_input_artifacts`, reusing the producer's key: for
  example `plan` needs `spec.md` and `tasks` needs `spec.md` and `plan.md`. An input blocks only
  when its producer marks the output blocking, so qa `review`'s `defect-log.md` does not.
- **Retrospect and research accept prompts, and a software-dev `retrospect` step** (#98). The
  documentation, research and software-dev `retrospect` on-demand steps get a prompt that drives
  `spec-kitty retrospect create`, and research `accept` gets its prompt. The software-dev step
  carries the guidance of the retired `actions/retrospect/index.yaml`.
- **The built-in glossary defines the activation ledger and the current active
  charter** (spec-kitty/spec-kitty#6562). `.kittify/charter/activation.yaml`
  became the single activation authority in core #6496, but the glossary still
  described the old `config.yaml` / `charter.yaml` home and had no term for the
  ledger. Both entries now name the ledger, the `deactivated_<kind>` exclusions
  and the legacy-location caveat for a project not yet on 4.0.0rc8, and the new
  term keeps the Migration Ledger distinction.

- **A vocabulary guard keeps retired names out of every pack** (spec-kitty/spec-kitty#6553).
  Core checks pack content for retired doctrine ids, the renamed `merge` command and the retired
  governing glossary surface, but only over the synced built-in and internal trees and only
  after a pin bump, and this repository had no such check. `scripts/ci/check_vocabulary.py`
  now runs the same rules over every pack in `validate-packs.yml`, with `::error` annotations
  per file and line, and fails when a provenance exemption no longer matches its file. Prose
  where the old command name runs on ("merges", "merged") is not flagged, the same as in core
  (#62). All packs are clean today.

- **Semver releases with a reproducible archive per pack** (#53). Until now this repository
  could only be pinned by a raw commit, with no release notes and a fragile sparse checkout to
  fetch one pack. Pushing a `vX.Y.Z` tag now re-validates the packs and publishes a GitHub
  release with a reproducible `<pack>-vX.Y.Z.tar.gz` and `.sha256` for every pack: `built-in`,
  `internal`, `qa`, `event-driven` and `cave-kitty`. The notes come from the matching changelog
  section, and a release without one fails. The release stays a draft until every archive has
  uploaded. Release tags are never moved or deleted; prereleases are not released.

- **Docsite and README overhaul for the Brain Kitty line.** The README and the docsite now
  describe open packs as the content half of **Brain Kitty**, and show how a pack reaches the
  Spec Kitty CLI: vendored or registered, merged into the **Charter Offering**, activated into
  the **Active Charter**, and served through the charter's entry seams. The landing page is that
  overview. New sections: **Charter artefacts** (the structure of every artefact kind),
  **Organisations** (built-in → org → project tiers, `required_<kind>`, skill namespaces and the
  standard provisionings that ship), **Contracts** (pack, org-charter, preset, manifest and DRG
  files, consumer registration, commands, charter seams), an **architectural overview** and a
  **Glossary**. The nav is reordered with the changelog last, and the site wears an olive Brain
  Kitty colourway over the Spec Kitty theme. Live docs use canonical Charter terminology
  ("doctrine pack" is now "Charter Pack"; the guides moved to `use-a-charter-pack` and
  `author-a-charter-pack`), and links to the retired `Priivacy-ai` organisation now point at
  `spec-kitty`. The site builds on doc-kitty **0.3.0**; the stale `docs/toc.yml` is removed.
- **Published documentation site for the open packs** (#40). `spec-kitty-open-packs` now has a
  browsable, Brain Kitty-branded docs site built with **doc-kitty/Astro** (the same stack as the
  charter site), so anyone adopting a pack has a real home for the material instead of reading
  raw files. It surfaces the existing guides, adds a **packs hub**, and ships
  **generated-from-source per-pack reference** pages — inventory, per-kind counts, validation
  status, and a content checksum derived straight from each pack, kept honest by a CI
  drift gate so the pages can never silently diverge from the packs. A getting-started tutorial
  walks a newcomer through adopting a pack with the `spec-kitty` CLI and a charter. This
  supersedes the earlier MkDocs direction (new ADR
  `2026-10-17-1-doc-kitty-astro-as-docsite-generator`, superseding ADR-1). The site publishes to
  GitHub Pages from `main` once a repo admin turns Pages on (Settings → Pages → Source: GitHub
  Actions).
- **`cave-kitty` Charter Pack** (`packs/cave-kitty/`, #35). A "caveman" communication voice as
  opt-in doctrine: an agent answers outcome-first with filler cut, while every payload (code,
  paths, numbers), every negation, and the user's own words stay exact, and it restores full
  sentences at a cliff edge (destructive or irreversible actions, a confused reader). Ships a
  styleguide (`cave-sty-001-communication`), a directive (`CAVE_001`) that governs the agent's
  output prose only, and a `cave-dev` mission type that re-voices the eight-step `software-dev`
  lifecycle without touching its engineering rigour. Activate the voice on `--type software-dev`
  for a clean token-impact comparison, or run `--type cave-dev` for the re-voiced lifecycle —
  note `--type cave-dev` does not inherit software-dev's `next`-loop WP iteration or guards (a
  CLI-level coupling), so the voice-activation path is the instrument for a token A/B.
- **Stable `Validate packs gate` CI check** (#34). The pack-validation workflow now ends in a
  fixed-name gate job, so branch protection on `main` can require one status check that does not
  rename itself when the pinned `spec-kitty` commit is bumped (the old matrix-leg name carried the
  pin). Require `Validate packs gate` as the protected check.
- **`event-driven` Charter Pack** (`packs/event-driven/`). Event-sourced design as opt-in
  doctrine: an `evd-event-sourced-design` paradigm, six directives (`EVD_001`–`EVD_006`: schema
  version on every event, one canonical writer per stream, immutable past-tense facts,
  producers emit the latest version while consumers declare what they accept, side effects in
  consumers, shared contracts only), four tactics (versioning and upcasting, ports-and-adapters
  event bridge, projection replay, idempotent consumers), an event naming and payload
  styleguide, a glossary, an `event-driven` activation preset, and a worked example after
  Martin Fowler's *Event Sourcing* article set on a Spec Kitty lane board. Links to built-in
  `domain-event-capture`, `event-storming-discovery` and related doctrine rather than restating it.
- **Seeded `built-in/`** (#31). The Spec Kitty consumer built-in pack, byte-identical to core
  `packs/built-in/` at `82fee752`, so core can vendor it from a pinned commit here
  (spec-kitty/spec-kitty#3504). It sits outside `packs/` because CI registers every `packs/*`
  directory as an org pack. `built-in.source.yaml` records the source commit, the tree digest
  and the supported core range, and `scripts/ci/check-built-in.sh` validates the pack and checks
  the digest. Core is still where built-in content is edited until the authoring flip.
- **`qa` Charter Pack** (`packs/qa/`). A `qa` mission type that redefines the seven canonical
  steps in QA terms, eight QA directives (`QA_001`–`QA_008`), test-design tactics, procedures, five
  QA agent profiles, an ISTQB-grounded glossary, and three evidence tools (`qa-result-ingest`,
  `qa-traceability-lint`, `qa-promise-trace-lint`), plus a promise-page → scenario → acceptance CI
  loop. Ported from `spec-kitty/spec-kitty-qa-pack` at `e9ed31c` via `spec-kitty/private-packs`
  PR #1; the ingester now reads the template-mandated body-fenced test cases
  (spec-kitty-qa-pack#5). See `packs/qa/PROVENANCE.md`.
- **Pack validation CI** (#27). `.github/workflows/validate-packs.yml` runs
  `scripts/ci/validate-packs.sh` on every pull request against a pinned spec-kitty commit: it
  validates each pack under `packs/`, loads all packs together in a scratch project with
  `doctor charter-packs`, and requires the fixtures under `tests/fixtures/invalid/` to fail, so the
  gate cannot pass vacuously. It also fails when two packs declare the same id (which
  `doctor charter-packs` only reports), runs every spec-kitty call under a throwaway `HOME`, and
  pins its actions by commit SHA.
- **Repository bootstrap.** Initialized `spec-kitty-open-packs` with `spec-kitty init`
  (Claude Code, Codex, Gemini, Copilot surfaces), MIT license, Code of Conduct, security
  position, and the documentation convention mirrored from Spec Kitty core (`toc.yml` nav skeleton,
  frontmatter, root `CHANGELOG.md` / `CONTRIBUTING.md` symlinks, `.github` artifacts).
- **Documentation scaffold.** Added `docs/guides/` with usage guides (use a pack, compose
  packs) and authoring guides (author, validate, publish a pack).
- **Pack catalog proposal.** Added `docs/packs/catalog-proposal.md` — 16 base packs (incl. a
  `spec-kitty-internal` dogfooding pack) + 4 compound stacks, carved from the current built-in
  doctrine corpus and cross-referenced to the core pack-ecosystem epics
  ([#2466](https://github.com/spec-kitty/spec-kitty/issues/2466),
  [#2467](https://github.com/spec-kitty/spec-kitty/issues/2467)).
- **Tracker seed.** Filed one tracking issue per base pack (open-packs #1–#16) plus a single
  compound-pack epic (#17), with `pack` / `doctrine` / `epic` / `compound-pack` labels.
- **Docsite research & architecture.** Investigated a content-from-code, checksum-tagged docsite
  via a three-lens research squad (feasibility & generator, blockers & core dependencies,
  information architecture) and recorded the outcome under Common Docs structure:
  `docs/research/` (three findings docs), `docs/architecture/` (vision, docsite design), and
  `docs/architecture/adr/` (ADR-1 docsite generator, ADR-2 generated-from-source pack reference,
  ADR-3 build-time checksum tagging, ADR-4 information architecture). Extended `docs/toc.yml`
  with Architecture + Research sections. Decision: **MkDocs Material** — single Python toolchain,
  purpose-built content-from-code plugins, largest OSS ecosystem — with DocFX (consistency-with-core)
  recorded as considered-but-deferred and Hugo rejected; one hand-authored `pack.yaml` is the
  content-from-code prerequisite; generate an interim sha256 content hash pending core verified
  distribution. (ADR-1 revised from an initial DocFX draft following maintainer review.)
- **Docsite tracker tickets.** Opened epic #19 (content-from-code docsite) with scoping children
  #20–#25, cross-referencing core epics
  ([#2314](https://github.com/spec-kitty/spec-kitty/issues/2314) pipeline,
  [#2467](https://github.com/spec-kitty/spec-kitty/issues/2467) manifest,
  [#2471](https://github.com/spec-kitty/spec-kitty/issues/2471) validator,
  [#2539](https://github.com/spec-kitty/spec-kitty/issues/2539) trust). Candidate new **core**
  tickets are drafted for HiC approval only and were **not** filed.
- **A docs freshness gate** (#297; the project charter's "docs freshness" gate). The `Docs site`
  workflow gains a `Docs freshness` job on pull requests. `scripts/docs/check_docs_freshness.py`
  fails an authored page under `docs/` that the pull request adds or changes when its `updated:` is
  missing, older than the author date of the last commit to it, or more than a day later. The
  author date survives a rebase, and paths are read NUL-separated, so non-ASCII names are judged.
  Per the operator's ruling on #297, a pure rename (similarity 100%) and `docs/changelog/` are not
  judged, and a commit trailer `Docs-Freshness-Unchanged: <path>` opts that page out for that
  commit, visibly in history, so a typo fix need not move a date nobody re-verified. Only changed pages are judged, so there is no baseline. Pages carrying `generated:`
  frontmatter are left to the drift gate. An advisory step lists pages past the staleness tiers of
  writing's `docs-freshness-sla` styleguide (guides 90 days, ADRs 365) and this repository's
  choice for other pages (180), and pages dated in the future, skipping `durable`, `superseded` and
  `deprecated` pages. `tests/docs` covers the checker, so it runs under
  the required gate.

### 🔄 Changed

- **Red-first where it earns lasting value** (#209). `DIRECTIVE_034` now requires red-first for product
  logic, gate and classifier scripts, invariants, and security or permission policy. For configuration
  and glue work, a recorded real run or an existing gate is the evidence, labelled
  `[evidenced-by-run]`, and delivery asks the long-term-value question. The evidence must exist and
  run the changed configuration itself (the new or edited job, step or setting executes in it, visible
  in the run's log); a run of other jobs on the same change does not count. Red-first work with no failing-first test does not conform, whatever evidence
  it names, and a doubtful change counts as carrying lasting regression risk. A justified skip still
  exists: skipping red-first for behavior with that risk needs an explicit justification in the
  commit or PR, and the carve-out for configuration and glue work is not a skip. Security or permission configuration
  that takes a policy check instead of a test needs a recorded red: the check must fail on a
  configuration that violates the policy. Review flags new tests that only restate configuration as
  waste and checks that the cited evidence exists.
  `DIRECTIVE_041` lets a change detector retire once its evidence is recorded. Before, the doctrine
  asked for a failing test ahead of every production change.
- **`DIRECTIVE_036` defers to `DIRECTIVE_054` for where substitutes sit** (#216). Before, the two
  directives could read as giving different answers on which seams a test may substitute. `DIRECTIVE_054` also judges a seam by what sits behind it, not by the transport: a test cannot stub an HTTP call to a sibling service of its own bounded context.
- **Missions here use `packs/` as their workspace** (found by the mission for #246).
  `.kittify/config.yaml` maps `project.path_conventions.workspace` to `packs/`. Software-dev
  missions change pack content and there is no `src/`, so without the remap `spec-kitty agent
  mission accept` refused every one of them with "expects workspace path: src/ (not found)". The
  remap is project-wide: it applies to every mission type that declares `workspace`. Research
  missions now look for `packs/` instead of `research/` (accept then checks
  `<deliverables>/packs/`, so a research mission here will likely need its own fix); documentation
  missions check `packs/` instead of `docs/` for their workspace, while their `documentation: docs/`
  key still checks `docs/`; plan missions check `packs/` instead of `docs/`, which is harmless. This
  is an operator trade-off until the CLI offers per-mission-type overrides (spec-kitty/spec-kitty#7748).
  Repository tooling only; no pack changes.
- **The schema mirror follows charter #554's root-only graph shards** (#253, epic #287). Charter
  `main` reads a `<name>.graph.yaml` shard at the pack root only: a `drg/*.graph.yaml` is no longer
  modelled, and an unmodelled file is warned as `file_not_held` instead of refused.
  `validate_pack_schemas.py` now fails closed on a known kind only when the contract maps that kind
  nowhere, so it judges a nested shard as `unmodelled` instead of stopping. The same applies to any kind
  whose rule is scoped to a path: a misplaced `foo.step-enhancement.yaml` is an `unmodelled` violation,
  where it used to stop the gate. It still fails every file the charter does not hold, and the service
  check names such a file as unmodelled, not as a drifted mirror. The `legacy-shapes` fixture's shard moves to the pack root, so the schema pass
  is green against both the pinned `service-v0.1.0-rc.1` and charter `main`. Every shipped pack
  already keeps its shards at the root.

- **The packs are pinned to charter release `service-v0.1.0-rc.1`** (epic #287; operator ruling,
  2026-11-18). `charter.lock.yaml` moves from `main` at `050d780` to the pre-release tag
  `service-v0.1.0-rc.1`, its commit `ebce9083cc132c4cc7f7602f8b8681b933dac98a` and the jar digest
  `596a7861…941714` its `.sha256` asset states. The `Charter service validation` job now downloads
  `spec-kitty-charter-service-0.1.0-rc.1.jar` and refuses any other digest instead of building the
  service with Gradle; the round trip still runs from the source at the tagged commit. Between the
  two commits the charter changed release tooling, CI and identifier tests only: the packs
  contract's `file-kinds.yaml` and schemas are unchanged, so no manifest, digest or pack content
  changes. The pin policy changes with it, superseding the 2026-11-16 lockstep with `main`: pin a
  charter release or pre-release tag by default, and charter `main` HEAD only on demand. The lock
  comments, the project charter and its interview answers, the README, the vision, the roadmap and
  the validate-a-pack guide say so.
- **The accountable human is "the operator" in pack prose and both glossaries** (#139). "HiC",
  "Human-in-Charge" and "human-in-command" no longer name a role: the glossary term is
  `operator` (avoid: "human in charge", "human in command"), the kitty-glossary-writing
  styleguide drops its rule requiring "HiC" in every definition (now 7 principles) and its
  "Passive Authority" anti-pattern, glossary-curation-interview drops its "Apply HiC
  terminology" step, and procedures, tactics, the contextive toolguide, the writing tactic
  graph and the software-dev charter prompt say "the operator". The `human-in-charge` agent
  profile keeps its id. **Upgrade:** retrospective-facilitator's mode `hic` is now `operator`.
- **`spec-kitty-core.glossary.yaml` is the authoring source** (#234). Its description no longer
  says it was migrated from `spec_kitty_core.yaml`, and its header names the curation workflow.
  29 pre-existing definitions drop core source paths, ADRs, issue numbers, `docs/context` pointers, core
  work-package history and HiC wording (ids and names unchanged); `review-py-package`, a core
  layout detail, is deprecated.
- **Versions:** none of its own. Per the operator's ruling of 2026-11-18, #300, #302 and #303
  share one bump: this content lands inside foundation and writing 2.1.0, the core bundles 2.2.0
  and built-in 4.1.0 from #302, and internal 4.0.1 from #303.
- **A directive states its rule, never how strictly it binds** (#233, epic #245; core
  spec-kitty#5207). How strictly a directive binds is the adopting charter's call; the packs said
  it twice and disagreed (DIRECTIVE_051 was `required` but called itself "advisory in v1").
  - The levels are defined once: `term:spec-kitty-core/enforcement-level` in foundation's
    glossary context, and an entry in the docs glossary. The meanings follow the pinned directive
    schema (the rank `required` > `lenient-adherence` > `advisory`; a `lenient-adherence` directive
    lists at least one `explicit_allowances` entry). The directive's `enforcement:` field is read as
    the pack-supplied default, and the level that applies is the adopting charter's decision (core
    spec-kitty#5207). The term is kept apart from presets' `must_have` and `policy.yaml` levels. The
    authoring guide, the artefact reference and pack-authoring's `doctrine-instruction-voice`
    styleguide ("State the rule, not its strictness") point to it.
  - The field stays: at charter `050d780` the directive schema requires it. No default value
    changes (ADR 2026-11-18-1, Accepted).
  - Level prose is removed from directive bodies: DIRECTIVE_051 (its scope sentence and its
    level-only fifth integrity rule; the evidence rules stay), 052, 049,
    `RECONCILE_CHANGE_SCOPE_TENSIONS`, `CLOUD_SESSION_ORCHESTRATION`, QA_002,
    `ACTION_ITEM_ATTRIBUTION` and 042. QA_001 is retitled "QA Requirement Traceability" (its id and
    file name are unchanged).
  - Level prose is also removed from the content that cites directives: the software-dev plan,
    implement and review substeps, prompts and guidelines, and the plan mission type's
    supply-chain substep (all drop "advisory in v1"); the `supply-chain-install-safety` tactic;
    graph edge reasons in foundation, internal and writing; the cave-dev step prompts; and
    wording in the cave-kitty README and styleguide, writing's minutes, glossary-writing, comms and
    scaffold artefacts, pack-authoring's onboarding profile and procedure, internal's
    `cloud-session-dispatch` procedure, and the QA_001 title in qa's graph fragment and three
    profiles. The adversarial-squad term and procedure stop calling the squad "advisory" (a
    procedure, not a directive, but the word now names a level).
  - `check_vocabulary.py` gains a rule that refuses self-binding phrasings ("advisory in v1",
    "this is advisory guidance", "binding charter content", ...) in every pack file, including a
    phrase wrapped across two lines. A claim made with a single bare word is left to review.
  - Versions (DIRECTIVE_018): `pack-authoring` 1.3.0 (the styleguide principle); `qa` 4.0.1,
    `internal` 4.0.1 and `cave-kitty` 2.2.1 (wording; a registered pack re-sent at the same
    version answers `409`). The built-in members `foundation` and `writing` are never registered;
    their changes ride the batch's shared bump to 2.1.0 (with `built-in` 4.1.0), so the exact
    `==2.1.0` pins on them (in `built-in` and five other packs) do not move again.
  - **Upgrade:** none. A project that relied on a directive's prose for its level reads its
    charter, or the field.
- **The direction docs state who owns what** (operator ruling, 2026-11-16). Packs and their
  schema, structure and validation are no longer a core repository concern: core is the
  deployable, assembler surface, the charter repository owns the logic, and content is owned in
  the packs repositories. The vision and the project charter (`charter.md` and the interview
  answers) say so, and add that packs move in lockstep with the charter's `main` and that
  compound stacks are presets on `built-in` (#17), not `depends_on` stack packs. The
  architecture overview and index, the docsite design, the home page, the README, the
  contributing guide and the catalog proposal are aligned; the July blockers research is
  annotated as a dated record.
- **The round trip runs `:pack-validation:driftTest`** (#284; charter #555, ADR-0075 decision 8).
  The `Charter service validation` job uploads the report from
  `service/pack-validation/build/reports/tests/driftTest`. The judgement is unchanged.
- **The validator follows the new pin's file rules** (#285 item 5): a `retired` rule beats a
  `files` rule that also matches, unless an exclusion matches too, so a leftover
  `mission_step_contract.graph.yaml` is one `retired layout` violation; the step-contract kind is
  no longer known, and a glossary declares the node `glossary_context:<id>`.

- **The implementer flips a green PR to ready for review, and each internal delivery rule has
  one owner** (#271, #260). Before: `mission-wrap-up-sequence` told the agent never to mark the
  PR ready, while `issue-to-mission-delivery` and `semi-auto-delivery` told it to flip, so one run
  got opposite orders; the changelog, docs-index, PR-body, deferral, tree-check and base-ref rules
  were restated up to eight times and had drifted. After:
  - `mission-wrap-up-sequence` owns the shared delivery rules, one step each. Its closeout step
    runs: consolidation closeout, draft PR, CI to green, then the implementer flips the PR to ready
    for review. Merging stays with the operator.
  - The changelog fragment is `<id>.<section>.md` with the spelling check; the PR body is
    validated through `spec-kitty charter pack asset path validate-pr-body`. The deferral bar
    refines DIRECTIVE_046, and the tree check allows only deliberate, listed removals.
  - `issue-to-mission-delivery`, `semi-auto-delivery`, `cloud-session-dispatch`,
    `landing-contributor-prs`, `memory-curation-and-escalation` and the skills point at those
    steps. Delegate profile loading points at `adversarial-squad-deployment`, and the cloud
    integrity rules at `CLOUD_SESSION_ORCHESTRATION`.
  - The closeout step also owns commit attribution (the operator's convention, no AI model
    identifier), now for every internal procedure that opens a PR. `semi-auto-delivery`,
    `cloud-session-dispatch` and `landing-contributor-prs` now `require` `mission-wrap-up-sequence`.
  - Delegates load their profiles by `adversarial-squad-deployment`'s routes, which include its
    degraded on-disk fallback; the old "never a raw profile file" wording is gone.
  - `semi-auto.skill.md` keeps only the order and the mode fork. The long landing and triage
    steps are split.

- **The pack gates follow the charter's slice B file model** (#249). Both gates now
  classify files as the charter at `17ce3f9` does, and they fail on the same files.
  - `validate_pack_schemas.py` refuses a root case variant of a ruled file (`Readme.md`,
    `PROVENANCE.MD`) as `retired` under the rule it shadows. A file no rule models (`notes.txt`,
    `x.tactic.yml`) fails as `unmodelled`, in built-in-level packs too.
  - The validator also applies the charter's `ignored` rule last. Markdown only that rule takes now
    fails as `not_held`, unless it is a `README.md` note. It used to fail as `unclassified`. A
    skill body that a skill's `body_path` names is held as its companion.
  - A preset's `must_have` id must be held, as a file, within the preset pack's `depends_on` closure.
  - `charter_service_check.py` uploads each pack's real tree. It prints every registration
    diagnostic and classifies each `file_not_held` file with the validator's mirror, so one
    allowlist fails in both gates.
  - The generated `docs/packs/` pages show the pack level and name each dependency. They no
    longer record a validation verdict.

- **`java` 2.1.0: three business-code rules in `java-conventions`** (#204, epic #190). New
  principles, each with a bad and a good example:
  - money is a `BigDecimal` with an explicit `MathContext` or scale and `RoundingMode`, never
    `double` or `float`, and is compared with `compareTo`;
  - a stored or wire code becomes an enum through a `fromCode`/`fromByte` factory that throws a
    named exception on an unknown value, never `values()[ordinal]` or a silent default;
  - a positional or wire-format layout has its own codec and an explicit mapper; JPA `@Entity` is
    never put straight over it.

  Additive: no artifact id changes and no pack depends on `java`.

- **The spdd step enhancements are proven against the charter's current schemas, and the
  pinned charter commit moves to `55c7d824`** (#177, charter ADR-0066). The five
  `missions/software-dev/enhancements/*.step-enhancement.yaml` files and their
  `*.prompt-fragment.md` companions were already classified by the pinned `file-kinds.yaml`
  and laid out per ADR-0066 (id equals the file stem, one `enhances` edge per enhancement to
  `built-in::action:software-dev/*`, empty `spdd:reasons-block` slots in the base prompts,
  `schema_version: "1.0"`); what was missing is proof against the schemas themselves.
  `tests/ci/test_prompt_fragments.py` now asserts every spdd enhancement and fragment is
  classified and validated by the pinned contract with zero violations, and that an id that
  is not its file stem, a missing `schema_version`, an empty `prompt_fragments` list, a
  fragment with frontmatter and a 65-character id are refused. The last case needs the id
  `maxLength` of 64 that charter commit `55c7d824` added (the only schema change since
  `465e3de2`, with 136- and 255-character caps beside it), which is what the pin bump
  delivers; an audit confirmed every pack passes at the new pin. The `spdd` README's
  activation wording follows charter rule E6 and ADR-0059 A4: an enhancement is in force
  only while the `software-dev` mission type is, in addition to its own activation via the
  preset, and activation cascades forward only.

- **All 39 reverse-direction duplicate edges are collapsed under the operator's curation
  rule** (#135). ADR-0027 allows at most one unidirectional edge per unordered component pair;
  the ruling (2026-11-08) keeps the edge whose source is the more authoritative kind
  (paradigm > directive > procedure > tactic > styleguide), lets the `in_tension_with` /
  `reconciles_tension` edge win its pair, and moves a dropped back-pointer's `when`/`reason`
  onto the kept edge only where it adds meaning. No pair involving git-flow, shared-branch-ci,
  execution-lanes or extract-then-publish-separation was in the baseline, so nothing was
  deferred to #65. The operator ruled the two same-kind pairs: `disciplined-defect-diagnosis`
  keeps its `requires` to `test-first-bug-fixing`, and `testing-principles` governs
  `test-desiderata-and-boundaries`. `REVERSE_PAIR_BASELINE` in
  `tests/ci/test_graph_edge_identity.py` is now empty.
- **39 over-strong `requires` edges become `suggests`** (#127). The curator pass on the 142 pairs
  whose removed field and graph edge disagreed found edges that were generated by a per-kind rule,
  not authored: their own text calls the target optional, conditional or a "see also". Most targets
  stay reachable through `suggests` hops. `DIRECTIVE_040` leaves `software-dev/tasks`, and its
  five-paradigm procedure and tactic leave tasks, implement and review, by operator ruling.
- **Graph documents are the only source of relationships, part B** (#127, charter #240, charter
  ADR-0064). `CHARTER_COMMIT` moves to the merged charter commit `fb87f51`. 30 org-fragment edges in
  event-driven, internal and qa gain the `when` text the new contract allows. The composition gate
  reads references from graph documents only, so `TYPED_REFERENCE_SCHEMAS`, `BARE_ID_LISTS` and
  `written_references` are gone, and the guides and the missions README no longer describe the
  dropped fields or a typed-reference form. The `legacy-shapes` fixture now carries the removed fields.
- **Packs align with the charter contracts, not core releases** (operator ruling, 2026-11-06).
  `CONTRIBUTING.md` records it: packs are validated against the spec-kitty-charter contracts;
  core becomes compatible through the charter service's generated client; adhering to the
  contracts is the consumer's decision, not the responsibility of packs or charter.
- **Lane and worktree doctrine follows the hardened lane model** (spec-kitty/spec-kitty#7285,
  epic spec-kitty/spec-kitty#7276). Status is read only through the CLI from the resolved
  status surface, never from a checkout's files; the three task-prompt templates, the implement
  and review prompts and a new `resolved status surface` glossary term say so, and `status commit`
  no longer claims status commits target lane branches. One worktree vocabulary (lane worktree,
  coordination worktree, write checkout, write branch, harness isolation worktree; the
  maintainer-only PR-landing worktree is in the internal glossary) and
  `wp state` / `execution lane` terms separate a WP's lifecycle state from an execution lane.
  Consolidation wording replaces "merge" (glossary, accept, review, tasks, specify); `merge state`
  is deprecated for `consolidation state`. Accept and the wrap-up procedure teach lane cleanup as
  consolidation's final step, not waiting for the PR merge; tasks, specify and finalize-tasks
  teach the size-based default topology with lane worktrees created after `finalize-tasks`. A new
  built-in tactic `lane-recovery` covers `DESTROYED_LANE` and `LANE_WORK_TIP_UNKNOWN`. The behaviour it
  describes lands in core with epic #7276. Packs follow the charter contracts, not core releases:
  when to bump the pin is core's decision.
- **Landing worktrees are pruned with a proof, not by hand** (spec-kitty/spec-kitty#7173). The
  `landing-contributor-prs` procedure and the `land-pr` skill create landing worktrees under
  `.worktrees/`, start each pass with `spec-kitty doctor workspaces`, and remove a merged
  landing worktree and its branch with `spec-kitty doctor workspaces --prune`, which removes
  only worktrees whose content is on `origin/main` and prints a command to recreate each
  branch. This needs the core release that ships `--prune`.

- **The docs say a preset is self-contained, not incremental.** A preset is the whole activation
  selection for the kinds it names, and which agent profiles it holds is an operator's choice.
  Stated in the contracts page and the author guide; the comment of `packs/qa/presets/qa.yaml`
  no longer reads as if the researcher profile were activated elsewhere. Its list is unchanged.

- **The docs say a preset is self-contained, not incremental.** A preset is the whole activation
  selection for the kinds it names, and which agent profiles it holds is an operator's choice.
  Stated in the contracts page and the author guide; the comment of `packs/qa/presets/qa.yaml`
  no longer reads as if the researcher profile were activated elsewhere. Its list is unchanged.

- **Packs are validated against the charter's schemas, not the core CLI** (ruling on #102). CI
  now checks every pack file, `packs/built-in` included, against the JSON Schemas in
  `spec-kitty-charter` (`contracts/packs/`), pinned by commit in
  `scripts/ci/validate_pack_schemas.py`. It no longer installs core or runs
  `charter pack validate`, `charter org validate` or `doctor charter-packs`, so compatibility
  with core's own validator is not a requirement. The pin is a commit of the open charter
  mission-type branch (PR #275); it moves to a `main` commit once that merges. The built-in and
  event-driven presets and the built-in pack manifest moved to the sanitized shapes to pass. The
  schemas cannot see duplicate ids across packs or an edge to a missing node, so those two
  checks are gone with core's `doctor`.

- **Step descriptions and titles reviewed after the mission-type consolidation** (#96). The
  software-dev `charter`, `tasks-outline`, `tasks-packages` and `tasks-finalize` steps get a
  one-line description of their own; the prompt frontmatter keeps its original description. Three titles
  return to their former display names: plan `Specification` and `Planning`, software-dev
  `Task Breakdown`. software-dev `implement` and `review` now name their roles.
- **Step prompts no longer name the retired mission files** (refs #100). The research,
  software-dev, cave-dev and qa prompts pointed at `mission.yaml`, `mission-runtime.yaml`,
  `expected-artifacts.yaml` or `mission-steps/`. The READMEs, templates and step contracts that
  still name them are left to #100.
- **Docs and guidance describe the mission-type layout** (#100). Several docs still named
  mission files that #95 retired (`mission.yaml`, `mission-runtime.yaml`, action indices,
  `mission-steps/`, `command-templates/`, `governance-profile.yaml`, `expected-artifacts.yaml`).
  They now name `missions/<type>/<type>.mission-type.yaml` and its `steps/` prompts and
  guidelines. The `reviewer-implementer-role-separation` tactic now says a step names a role and
  a preset activates profiles (charter ADR-0032). Its id and intent are unchanged.

- **Red-main discipline is a directive, not a procedure** (#74,
  [spec-kitty-charter#199](https://github.com/spec-kitty/spec-kitty-charter/pull/199)). The
  red-main content is a standing rule (no green-washing, no release on red, no expensive QA on a
  red base), not a playbook. The built-in `red-main-release-discipline` procedure is now the
  `RED_MAIN_RELEASE_DISCIPLINE` directive, and the internal pack's `spec-kitty-red-main-policy`
  procedure is now the `SPEC_KITTY_RED_MAIN_POLICY` directive that refines it. The substance is
  unchanged. A consumer that activated the procedure by id activates the directive instead. The
  internal pack now needs a core that vendors `RED_MAIN_RELEASE_DISCIPLINE`: on the current core
  release its three red-main edges dangle. CI now warns about this instead of failing.

- **The internal pack's README names the spec-conformant command-skill folders**
  ([spec-kitty#6475](https://github.com/spec-kitty/spec-kitty/issues/6475),
  [spec-kitty#6470](https://github.com/spec-kitty/spec-kitty/issues/6470)). Spec Kitty now
  generates its command skills as `.agents/skills/spec-kitty-<command>` instead of the dotted
  `spec-kitty.<command>`, which several harnesses silently dropped. The recovery note for the
  untracked command-skill ledger now names both forms and warns not to remove the shipped
  `spec-kitty-*` charter skills. Mission-step prompts keep their `/spec-kitty.<command>`
  invocations: they are correct for the slash-command agents, and core rewrites them to the
  skill name when it renders a command skill.

- **The internal pack's tracker-label doctrine matches the 2026-10-19 label clean-up on
  `spec-kitty/spec-kitty`** ([spec-kitty#6503](https://github.com/spec-kitty/spec-kitty/pull/6503)).
  The `spec-kitty-tracker-labels` styleguide no longer offers `bug` or `enhancement` as kind
  labels (kind is the native issue type; `bug`, `enhancement` and `type:*` were deleted), names
  `deferred` instead of the non-existent `future`, adds `triage:needs-decision` (formerly
  `type:decision`), and gains a "Renamed and retired labels" pattern (`domain:merge` →
  `domain:consolidation`, `domain:dashboard` → `domain:status-api`, `domain:hosted` →
  `legacy:hosted`, `documentation` merged into `domain:docs`, and the deleted `squad:*`,
  `needs:*`, `ci:green`/`ci:red`, fleet `from:*` labels outside the provenance set, `launch-window`, `question`, `help wanted`,
  `invalid` and `wontfix`). The `issue-triage-pass` procedure and the `kitty-issue-triage` skill
  no longer call `status:*` fleet-owned: the SkyKitty fleet is switched off, `status:*`,
  `taken-by-human` and `ready-for-squad` are human workflow state, and a triage pass removes
  `status:triage` once an issue is decided. `issue-to-mission-delivery` and
  `landing-contributor-prs` drop their fleet-dispatcher and `squad:*` wording to match.
- **Built-in doctrine no longer sends agents to the closed `docs/adr/3.x/` folder**
  ([spec-kitty#5428](https://github.com/spec-kitty/spec-kitty/issues/5428)). The software-dev
  review prompt pointed reviewers at `docs/adr/3.x/` for architectural intent, and the
  `common-docs-scaffold` tactic used `adr/3.x/` as the home of a new ADR, though that era takes
  no new records. The prompt now names `docs/adr/`, filed by era, and the tactic's examples use
  `adr/4.x/`. `packs/built-in.source.yaml` records the new tree digest.
- **Org DRG fragments now match the charter's pack schema**
  ([spec-kitty-charter#114](https://github.com/spec-kitty/spec-kitty-charter/issues/114)), so the
  charter service can load every pack here. Before, `packs/internal/drg/fragment.yaml` had 84
  bare-id edge endpoints and the org fragments carried provenance header fields, which that
  schema refuses. Endpoints are now the URNs core already resolved them to
  (`landing-contributor-prs` → `procedure:landing-contributor-prs`), and the fragments drop the
  header fields they carried; core overwrites those from the consumer's registration. Core's
  merged graph is unchanged (461 nodes, 1235 edges). `validate-packs.sh` now fails on a bare-id
  endpoint or a header field, because core still accepts both.
- **The charter step says up front that activation is additive (core `#6408`).** The
  `software-dev` charter prompt never said that interview selections only add to what is
  already active, or that the first activation list is frozen, so later built-ins seemed to go
  missing. It now says so, and names the narrow paths: `charter interview --narrow-activation`,
  `charter activate <kind> <id> --only` and `charter activate --preset minimal`.
- **The `internal` pack declares `pack_level: org`, `active_charter` and `pack_drg` again.**
  Core's loader needs these fields to fetch the pack from this repository
  (spec-kitty/spec-kitty#6451). CI now validates against core `f166339`, which accepts them.
- **The built-in pack now lives at `packs/built-in/`, next to the other packs.** It used to sit at
  the repository root as `built-in/`, with its pin at `built-in.source.yaml`. Both are now under
  `packs/`: `packs/built-in/` and `packs/built-in.source.yaml`. The content and digest are
  unchanged. `validate-packs.sh` skips it, because it is the built-in tier and not an org pack.
  Core's vendoring has to read the new path; spec-kitty/spec-kitty#6451 tracks sourcing it from
  here directly.
- **Guides follow the Spec Kitty 4.x Charter Pack cutover.** `spec-kitty doctrine …` became
  `spec-kitty charter …`, `doctrine.org.packs` became `charter_packs.org.packs` (with `subdir`
  for packs in this repository), `doctor doctrine` became `doctor charter-packs`, the DRG lives
  in `drg/fragment.yaml`, the directive example matches the schema, and presets replace
  activation defaults. Core links point at `spec-kitty/spec-kitty`. Built-in overrides are declared
  as DRG edges and sanctioned in `replaceable-builtins.yaml` (the schemas reject `enhances:` /
  `overrides:` fields), `drg/fragment.yaml` is documented as required, examples use the real `qa`
  pack, and the multi-pack `--include` gap (spec-kitty#5779) is called out.

### 🐛 Fixed

- **The charter-track issues quote the failing jobs' errors again** (#323). The runner's `gh`
  refuses to print a response containing terminal escape sequences, and every job log carries
  ANSI colour codes, so each `charter:main-red` and `charter:release-red` issue said "(the job log
  could not be read; see the run)". `scripts/ci/charter_track_report.sh` passes
  `--allow-escape-sequences` when the installed `gh` knows it and strips escape sequences and
  control characters before quoting. A log that still cannot be read is quoted with `gh`'s own
  error, which the job log also shows.
- **Pack guidance gives one instruction per step, names only what the consumer has, and matches
  `spec-kitty-cli 4.0.0rc9`** (#266, #267, #268, #269, #270, #277, epic #263).
  - **software-dev** (foundation): the mission persona names no charter principles and lists the
    real steps. implement and review load charter context once, through the bootstrap substep. The
    occurrence map uses the rc9 schema vocabulary. History is cleaned before the PR is presented,
    never after merge. tasks-finalize says "planning branch". Agent-facing text names
    `spec-kitty agent action implement`, since rc9 labels `spec-kitty implement` internal.
  - **common-docs** (writing): no consumer gate requires `regenerate-graph`, a page-inventory
    lockfile, a `related:` validator or an SEO step; each check-table row maps to the shipped lint
    or to review. A new `common-docs-structural-lint` toolguide, plus a config asset sidecar, says
    how to resolve and run `docs_structural_lint.py`.
  - **documentation mission** (writing): Divio pages go to common-docs sections (`guides/`,
    `api/`, `architecture/`) with common-docs frontmatter, and pass the lint with `--extended`.
    The plan template and expected outputs describe the documentation flow; the two software-dev
    template copies are gone and `release.md` is bound to its template. validate runs the lint,
    the Divio `type:`, freshness and placeholder checks. Templates keep `{...}` slots; generate
    fills each slot or writes `[TODO: ...]`. Guidelines hold only the quality gates.
  - **qa mission**: no hand-install narrative, `EVIDENCE.md` or authoring-mission ids. review takes
    `--since` from the status event log, accept names `qa-coverage.json`, the `qa-traceability/v1`
    schema is inlined, and one dated note says what `blocking` enforces on rc9. Every step
    prompt has steps and success criteria.
  - **internal** `base`: the must-have landing, issue, semi-auto, triage, cloud-dispatch and
    wrap-up flows name the repository's own changelog mechanism, PR template, docs scripts, make
    targets and vocabulary check, from its charter or docs. No core-only preset; core keeps its
    specifics as a project-tier override.
  - **Versions** (DIRECTIVE_018, operator ruling at landing): `qa` 5.0.0 and `writing` 3.0.0 are
    major, because each removes artifacts (`EVIDENCE.md`; the documentation mission's
    `task-prompt-template.md` and `tasks-template.md`). `foundation` and the core bundles
    (`testing`, `refactoring`, `architecture`, `planning-analysis`) move to 3.0.0 in lockstep,
    `built-in` to 5.0.0, and every exact pin to `==3.0.0`. `internal` goes to 4.1.0 and `cave-kitty`
    to 2.2.2. Org packs' `>=2.0,<3` ranges on the lockstep packs widen to `>=2.0,<4`, with a patch
    bump each: `drupal`, `event-driven`, `go`, `java`, `javascript`, `pack-authoring`, `python`,
    `rust` and `spdd`.
  - **Upgrade:** a project that pins `foundation`, `writing` or a core bundle with `<3` widens the
    range. A project that used the removed documentation templates or qa's `EVIDENCE.md` keeps a
    project-tier copy.

- **Consumer packs no longer point agents at this repository's tree, internal-only artifacts or
  paths a consumer does not have** (#258, #259, #265, epic #263).
  - `packs/built-in/...` paths in writing and planning-analysis styleguides, the lint config and
    graph comments now name the artifact (and its pack) instead.
  - Spec Kitty core `src/` paths become neutral `src/myproject/...` examples in `testing-principles`
    and `python-review-checks`. The Mermaid and PlantUML guides no longer promise theme and template
    files that ship in no pack.
  - The software-dev `implement` prompt no longer sends agents into a `packs/` tree or into Spec
    Kitty's generated agent commands: the bulk-edit sweep searches project-authored templates and
    agent files. It no longer cites the internal `mission-wrap-up-sequence`, and neither do the qa
    go/no-go review or testing's `development-assist-test-cleanup`, which now triggers "after
    acceptance, before merge". The internal pack keeps the sequencing edge.
  - Project profiles point at `.kittify/charter-packs/agent_profiles/` (with a new id that
    specializes a shipped profile), not the unread `.kittify/charter/agents/`. The squad
    procedure casts by role and its on-disk fallback reads the installed pack; tactics cite the
    software-dev mission type instead of file paths.
  - The six mutation-guide links, the qa Sonar guide's two links and the contextive guide's two
    links that broke across packs now cite artifacts by `<pack>::<kind>:<id>`.
  - writing ships four writing-audience personas and now says so; the fifth is internal. The
    file-less `stakeholder-persona-template` and `system-context-canvas-template` nodes and their
    two edges are removed (#196 tracks authoring them).
  - Prose that names an artifact outside the pack's `depends_on` closure names the pack and says
    "when installed" (supply-chain toolguides, `python-pedro`, `researcher-robbie`,
    `research-citation-discipline`, `kitty-glossary-writing`, `test-first-bug-fixing`, `zombies-tdd`,
    `use-c4-model-techniques`, the jqwik warning's `java-conventions`). `canonical-source-unification`
    no longer names a `packs/` path (#274 keeps its other core examples), and spdd's README names
    its real dependencies.
- **pack-authoring tells one authoring story, and foundation no longer ships house authoring rules**
  (#275, epic #263).
  - `doctrine-daphne` and `onboard-external-agent-to-pack` now agree with each other and with this
    repository: a pack keeps plural kind directories at its root (`charter new` places each file), an
    org pack's edges live in its hand-authored `drg/fragment.yaml` with nothing to regenerate, the
    project tier gets its edges from a profile's typed `*-references` fields on `charter activate
    --cascade all`, and built-in-level graph shards are not an authoring surface. Neither authors an
    `applies` edge, and neither grows a legacy inline `references:` list. The core-only gates and the
    frozen profile measurement are gone from the profile.
  - `migrate-project-guidance-to-spec-kitty-charter` names the project and org tiers and the real
    commands (`charter new`, `validate`, `org validate`, `org add`, `activate`, `interview`,
    `generate`, `synthesize`, `context`, `consistency-check`, `lint`, `glossary validate`) instead of
    "promote into the shipped set". Both procedures and the profile state the project tier's limit:
    only directives, tactics, styleguides, procedures and agent profiles become nodes there, and edges
    come only from a project agent profile.
  - New `pack-authoring` styleguide `doctrine-instruction-voice` holds the two doctrine-voice rules that
    `DIRECTIVE_045` carried (quote a deprecated term; no unauthorized high-risk operation in an
    example). `DIRECTIVE_045` now names the protected default branch, not `main`, and the duplicate
    terminology note leaves `pr-agent-worktree-isolation`.
  - `DIRECTIVE_018` and `doctrine-version-change` stay in foundation, rewritten for the doctrine a
    project or organization authors: classify the change, bump `pack_version`, record rationale and
    migration notes, keep `schema_version`, validate with named commands. Its scope narrows: it no longer
    covers schema changes or a repository-wide validation pass over shipped doctrine.
  - `moscow-scoping-lens` names the project's priority scheme (if any) instead of `priority:P0`..`P3`,
    and `github-tracker` drops the keyring-token advice and the unreachable styleguide citation.
- **Commands, flags and skills that agents were told to run now exist and behave as described**
  (#264). Each instance gave an agent an error, a dead end, or quietly did the wrong thing.
  - `foundation` PowerShell toolguide: it told agents to chain with `;`, so a work package
    could move to review after its tests failed. It now separates Windows PowerShell 5.1 from
    `pwsh` 7: use `&&` on 7, and check `$LASTEXITCODE` or `$?` on 5.1. It no longer tells agents
    to write spec-kitty flags as `-Json`; that advice now covers cmdlets only. The `NNN-` worktree
    and branch names, the `tasks\planned` folder, the core-only `SPEC_KITTY_TEMPLATE_ROOT`
    example and the backslash-only rule are gone. Start-up failures point at
    `spec-kitty verify-setup --diagnostics`, not `pip show`.
  - `python` toolguides: `python-review-checks` uses the mutmut 3 form (`[tool.mutmut]` and
    `uv run mutmut run "<module>*"`), not mutmut 2's `--paths-to-mutate`. `python-mutation-tools`
    drops `--rerun-all=false`, `runner` and `show all`, which mutmut 3 does not have, and names
    `source_paths` and mutant names.
  - `cave-kitty` README: `--type` becomes `--mission-type`, the only spelling the CLI accepts.
  - `internal` `landing-contributor-prs`: the retired `scripts.docs.description_length_check`
    becomes `tests/docs/test_docs_seo.py`.
  - `foundation` tactics: `five-paradigm-parallel-debugging` names the `failing-test-triage` and
    `durable-fix-investigation` procedures instead of an `/investigate` skill no pack ships.
    `model-task-routing` no longer sends agents to a catalog they cannot open: it names the
    advisory panel `spec-kitty dispatch` prints, and says what to do when none is shown.

- **Every pack carries the manifest the charter derives, and CI round-trips every pack through the
  charter** (#255, #250, #252; charter #542, #545, #547). `charter.lock.yaml` moves from `17ce3f9` to
  `eacbc3c`, which also holds charter #547: the round trip now fails loudly on a file kind it does not
  model. From charter #542 on, the charter derives a manifest's lists from the pack and refuses
  any other lists as `manifest_membership`. At that pin it refused the hand-written manifests of
  `built-in` (it left out the presets `default` and `minimal`), `foundation` (it left out 31
  constituents) and `writing` (21).
  - All 19 packs and the valid example fixture now carry a `pack-manifest.yaml` generated from the
    derived lists: every artifact file, mission types, step contracts and templates included, and
    every preset, in path order. The twelve org packs had none. The four bundles that already
    matched are rewritten in path order.
  - `validate_pack_schemas.py --derive-manifest PACK` writes the manifest, mirroring the charter's
    `ManifestMembership`. `validate-packs.sh` passes `--derived-manifests`, which fails a pack whose
    manifest is missing or whose lists differ, worded as the charter words it.
  - The `Charter service validation` job runs the charter's `:packs:driftTest` over every pack from
    the pinned source (`scripts/ci/charter_drift_test.sh`) and uploads its report. It is a gate, and
    the only check the charter makes on a built-in-level pack, which is never registered.
  - The twelve org packs get a patch release, because a registered pack re-sent at the same version
    with new content answers `409`: `cave-kitty` 2.0.1, `drupal` 2.0.1, `event-driven` 3.0.1, `go`
    1.0.1, `internal` 3.0.1, `java` 2.1.1, `javascript` 2.0.1, `pack-authoring` 1.0.1, `python`
    2.0.1, `qa` 3.0.1, `rust` 1.0.1, `spdd` 3.0.1. Built-in-level packs cannot be registered, so their
    versions and the exact pins between them do not change.
- **Shipped prompts, procedures and tactics no longer point at paths the pack split removed**
  (#195, #227, #159). The #198 split moved files byte-for-byte, so they still named
  `packs/built-in/...` paths that no longer exist.
  - **Stale paths.** Step prompts, a plan template, a research guideline and four tactics now point
    at `packs/foundation/...`, or at the per-pack `packs/<pack>/...` pattern where any pack may hold
    the file.
  - **Core `src/` paths.** The `glossary-curation-interview` tactic drops spec-kitty's own
    `src/specify_cli/` paths for a neutral `src/myproject/`.
  - **Collaboration lists.** `analyst-annie`, `diagram-daisy` and `lexical-larry` name roles
    (`architect`, `semantic-analyst`, `implementer`), not profiles their pack's dependency closure
    does not hold.
  - **"Built-in" prose.** The `cave-kitty` and `qa` step prompts name the pack that ships a profile,
    not "built-in".
  - **Adversarial-squad dispatch.** The `adversarial-squad-deployment` dispatch step is
    harness-aware. Read-only can mean no process at all, so the orchestrator injects each resolved
    profile first, and self-loading and the per-pack on-disk fallback follow. Where a delegate
    cannot run `git`, the orchestrator puts the review target's diff, not the working tree, in the
    delegate prompt.

- **A Java project no longer loses its JVM toolguides** (#202, `java` 2.1.0). `java-supply-chain`
  and `maven-review-checks` declared `applies_to_languages: [jvm]`, so an activation filtered to
  `languages: [java]` dropped them (`languageFiltered`): the charter matches the field as a plain
  string and has no language-family alias. They now declare `[java, kotlin]` and `[java]`, so a
  Kotlin project on Maven or Gradle gets the supply-chain guide and not the Java review checks.
  This replaces the `jvm` tagging of spec-kitty/spec-kitty#6444, which relied on core expanding
  `java` and `kotlin` to a `jvm` family. `check_vocabulary.py` refuses a runtime family (`jvm` and
  its like) as a language name, and the authoring guide states the rule.

- **Work-package profile loading names the CLI command for hosts without skills** (#184). The
  "Do This First: Load Agent Profile" block in the `software-dev`, `documentation` and `research`
  task prompt templates, and the copy the `software-dev` tasks-packages step requires, still sends
  the agent to the `/spk-charter-profile-load` skill first. It now adds that a host which cannot
  run skills should run `spec-kitty agent profile show <profile-id>`, the command the skill itself
  uses. The `software-dev` implement and review steps' own profile-load instructions get the same
  fallback. An agent driven from the CLI could not follow the old wording.

- **The analyze prompt no longer asks the agent to count its own findings** (#183). The
  `software-dev` analyze step's `analysis-findings/v1` carrier example and rules leave `counts`
  out and say the recorder tallies `findings[]` itself, which core already does when the field is
  absent. A declared `counts` block is still accepted and still fails recording when it disagrees
  with the tally. Reports were being rejected for a count the prompt had asked the agent to type.

- **Internal procedure prose uses ASCII punctuation and puts regeneration exceptions first.** The
  `memory-curation-and-escalation` procedure replaces em dashes with sentence-appropriate ASCII
  punctuation. The `landing-contributor-prs` rebase step now names the docs retrieval index, page
  inventory and ADR era tables as exceptions in the regeneration instruction itself, before the
  general freshness-gate rationale; its commands and conflict-resolution guidance are unchanged.

- **Pack reference checksum recipes include the per-file trailing newline** (#120). The generator's
  docstring and every published page now describe `relative-path + NUL + bytes + LF`, matching the
  unchanged checksum algorithm so consumers can reproduce the published values.

- **Pack composition refuses dependencies and edges the charter rejects** (#123). A `depends_on`
  whose `pack_id` no configured pack declares now fails validation. So does an edge that joins a
  node of the pack to itself, whether its ends are bare or qualified with the pack's own name. An
  edge to the same urn in another pack joins two artifacts and stays allowed, as in the charter.

- **Pack composition refuses dependency cycles, as the charter does** (#123). A pack whose
  `depends_on` names its own `pack_id`, or that sits in any `depends_on` cycle, now fails
  validation with the cycle's path reported (charter C6, `pack_dependency_cycle`); a diamond of
  dependencies still passes. WP01's third accepted gate/charter disagreement was never recorded,
  and a dependency cycle was its likeliest candidate, so the operator ruled that the gate judge C6.

- **PR-body validation accepts GitHub's colon issue-link form** (#92). `Closes: #12`,
  `Fixes: #12` and the equivalent resolve forms now satisfy the advisory issue-link check. The
  internal delivery procedure clarifies that the Issue section and its closing link are needed only
  when a PR closes an issue, and the asset inventory names that advisory check.

- **Software-dev mission authoring content is ASCII-only** (#112). Its templates, prompts,
  guidelines and README no longer tell authors to emit non-ASCII dashes, arrows, box-drawing
  characters or symbols into mission artifacts. Core pins some of the old text (the
  success-criterion suffix, the "Do This First" heading and the "REASONS Guidance" headings), so a
  paired core change lands with the pin bump. A regression test rejects any non-ASCII character anywhere
  in the software-dev mission directory. The built-in tree digest is restamped.

- **One edge per component pair in the built-in graph** (#135). Seventeen pairs carried both a
  `requires` and a `suggests` edge, against charter ADR-0027: 14 profile-to-directive pairs for
  `DIRECTIVE_030`, `034` and `041`, plus `bdd-scenario-lifecycle` and `bdd-scenario-formulation` to
  `given-when-then-authoring`, and `testing-principles` to `quadruple-a-test-format`. Each keeps its
  `requires` edge, which already dominated the walk, and takes over the twin's `when` and `reason`.
  A new gate test refuses a duplicate in one direction and any new pair with an edge each way. The
  39 existing two-way pairs stay in a shrink-only baseline until they get curation rulings.

- **`qa` step prompts name the role a step asks for, not a bound profile** (#67). The seven
  `missions/qa/steps/*.prompt.md` files had a "Bound agent-profile" section naming one profile.
  It is now "Requested role": the role from `qa.mission-type.yaml`, and which profile the pack's
  `qa` preset activates for it (none for discovery's `researcher`).

- **`cave-kitty` step prompts name the role a step asks for, not a bound profile** (#67). The
  eight `missions/cave-dev/steps/*.prompt.md` files had a "Bound agent-profile" section naming one
  built-in profile. It is now "Requested role": the role from `cave-dev.mission-type.yaml`, with a
  note that cave-kitty ships no preset, so a built-in profile for that role fills it when the
  operator activates one.

- **Built-in `research` step prompts name the requested role, not a profile** (#67). The header
  line of `scoping`, `methodology`, `gathering`, `synthesis` and `output` said
  `**Agent profile**: researcher-robbie` (or `reviewer-renata`). It now says `**Requested role**`
  with the role from `research.mission-type.yaml` and names that profile only as an example.
  The built-in tree digest is restamped.

- **Work packages name the role they ask for, not a profile** (#67). In the built-in
  `software-dev` flow (`tasks-packages`, `tasks`, `implement` and `review` prompts), the three
  task-prompt templates and the `reviewer-implementer-role-separation` tactic, the WP frontmatter's
  `role` now drives profile selection: the active preset's profile for that role, or a profile whose
  roles and specialization context match. `agent_profile` stays in the frontmatter as an optional
  override, normally empty, so current core keeps working. The review handoff and the rejection
  handoff switch `role` instead of pinning `reviewer-renata` or `implementer-ivan`. Retiring the
  field itself follows in core after the charter service integration.

- **Internal procedures no longer regenerate the docs index in a PR** (#105). The
  `issue-to-mission-delivery`, `landing-contributor-prs` and `memory-curation-and-escalation`
  procedures told agents to run `docs_index --write` and `freshen_adr_inventory` (or register pages
  in the page inventory and retrieval index). Since spec-kitty/spec-kitty#6993 a CI guard refuses
  those edits and the `ci/regen-docs-index` bot PR regenerates them on main, so the procedures now
  say to leave them alone and to take main's copy on a rebase conflict.

- **`packs/internal/PROVENANCE.md` no longer calls `spec-kitty-charter` a vendored mirror** (#114).
  Since spec-kitty/spec-kitty-charter#364 the charter keeps gitignored copies that
  `./gradlew syncPacks` syncs at `openPacksRef`, with tree digests in `packs/open-packs.lock.yaml`.
  The page now describes that sync and drops the re-vendoring step: a downstream repository takes
  the pack at a pinned commit, never edits or re-mints it, and gets a change through a pin bump.
  Prose only; no pack content or `pack_id` changes.

- **`built-in` no longer holds two empty `__init__.py` files** (#94). The Python package markers in
  `missions/built_in_step_contracts/` and `toolguides/system_tools/` were leftovers of the pack's
  time inside core's package; no file-kind rule classifies them, and nothing imports them.

- **Each `quality-assurance` toolguide's id is now its file stem** (#93). `qa-promise-trace-lint-guide`
  and `qa-result-ingest-guide` are renamed to `qa-promise-trace-lint` and `qa-result-ingest`, their
  guides to `<id>.guide.md`, and the pack's graph nodes, edges and README follow. A consumer that
  names `toolguide:qa-promise-trace-lint-guide` or `toolguide:qa-result-ingest-guide` must use the
  new ids. The script assets keep their ids, which the toolguides now share.

- **Java doctrine advises against jqwik** (#46). Since 1.10.0 the jqwik test engine prints a line
  to stdout that tells AI agents to disregard previous instructions and ignore all jqwik results,
  and agents read that output to judge test evidence. The `java-conventions` styleguide now has an
  anti-pattern against adding `net.jqwik:*` (1.10.0 and later), linking upstream's "Anti-AI Usage
  Clause", and names JUnit `@ParameterizedTest` with generated inputs instead.
  `formalized-constraint-testing` records the same exclusion and alternative, and now `suggests`
  `java-conventions` for JVM constraint tests.

- **The internal pack tells agents to write a changelog fragment, not to edit `CHANGELOG.md`**
  (#105, spec-kitty/spec-kitty#6988). The landing, issue-to-mission and semi-auto procedures and
  their skills told agents to add an entry to `docs/changelog/CHANGELOG.md` and to keep both sides
  when it conflicted, which produced duplicate entries. They now name the fragment
  `docs/changelog/unreleased/<pr>.<section>.md`, a changelog conflict on rebase moves the entry
  into a fragment, and the "keep both sides" advice is gone. The docs lint config excludes
  `changelog/unreleased/**` from the frontmatter contract, since fragments are entries, not pages.

- **Language-specialist profiles `requires` their conventions styleguide** (#131,
  spec-kitty/spec-kitty-charter#405). `java-jenny`, `python-pedro` and `drupal-dries` now carry a
  `requires` edge to `java-conventions`, `python-conventions` and `drupal-conventions`, so a
  profile cascade selects the styleguide. The inverted styleguide-to-profile `suggests` edges are
  replaced, not kept beside the new ones; `drupal-dries` `suggests` `drupal-security-performance`.
  A new test fails when a profile does not `requires` the styleguide mapped to each of its
  `applies_to_languages`. JavaScript, TypeScript, HTML and CSS have no conventions styleguide yet
  and are listed as exempt until #131 settles them.

- **`--regenerate-manifest` no longer passes when the manifest lists a missing file.** Run on
  its own, it printed a warning, rewrote the manifest and exited 0, so the documented restamp
  command reported green on a pack the gate rejects. It now refuses like the charter's manifest
  write (`pack_unreadable`): it prints an error naming the file, leaves the manifest untouched and
  exits 1. The gate's advice for a `missing:` entry now says to restore the file or remove its
  entry, since a restamp cannot fix it.

- **`cave-dev` `tasks` declares the `tasks/WP*.md` work packages it writes.** The step wrote
  only `tasks.md`, so `implement` and `review` could not depend on the packages. `tasks` now
  emits `output.tasks.per_wp` (`tasks/WP*.md`, blocking), the key and pattern software-dev uses,
  and `implement` and `review` take it as blocking input instead of `tasks.md`. `accept` already
  matches software-dev (`tasks.md`) and is unchanged.

- **`cave-dev` `tasks` declares the `tasks/WP*.md` work packages it writes.** The step wrote
  only `tasks.md`, so `implement` and `review` could not depend on the packages. `tasks` now
  emits `output.tasks.per_wp` (`tasks/WP*.md`, blocking), the key and pattern software-dev uses,
  and `implement` and `review` take it as blocking input instead of `tasks.md`. `accept` already
  matches software-dev (`tasks.md`) and is unchanged.

- **The licence names the right copyright holder (#64).** `LICENSE` named `Spec Kitty LLC and
  the Spec Kitty contributors`, but no `Spec Kitty LLC` exists. It now names the legal entity,
  `Spec Kitty, Inc.`. The MIT grant is unchanged, and contributors keep their copyright as before.
- **A PR body without a `closes #<n>` line is a warning, not a failure** (`internal`, #59). The
  `validate-pr-body` asset refused any body without an issue link, which blocked
  decision-recording PRs that legitimately close no issue. A missing link now prints
  `warning: ...` and exits 0, and the match covers GitHub's full keyword set (`close`, `fix`,
  `resolve` and their forms). A real structural violation still fails. The fragment title and the
  `semi-auto-delivery` procedure say the link is advisory. Upstreams the copy vendored in
  spec-kitty-charter (commit `19cc37f`).
- **`plan` missions advance past `specify`.** The `plan` mission's artifact manifest named the
  old phases (`goals`/`structure`/`draft`) and asked for `goals.md`, so `spec-kitty next` blocked
  a committed `spec.md` with `Required artifact missing: spec.md`. The manifest now keys on the
  runtime steps (`specify` → `spec.md`, `research` → `research.md`, `plan` → `plan.md`), and the
  plan `mission.yaml` and README match. Re-seeded from core (spec-kitty/spec-kitty#6395), which
  also absorbs the interim plan step-contract patch below: `built-in/` is byte-identical to core
  again.
- **`plan` missions now compose and run (`#42`).** The built-in pack shipped the `plan` mission
  type but none of its four step contracts, so every `plan` action failed at runtime with
  `No step contract found for mission/action plan/<action>` and plan missions were unusable for
  consumers. The pack now carries `plan-specify`, `plan-research`, `plan-plan`, and `plan-review`
  contracts keyed `mission: plan`, mirroring the `research-*` shape; `plan-review` deliberately
  omits the work-package `move-task` transition and pre-review gate, which a plan mission (no work
  packages) has no use for. Shipped as a deliberate interim override of the byte-identical core
  seed — the gap originates upstream, and the durable fix re-vendors from core via
  spec-kitty/spec-kitty#3504.

