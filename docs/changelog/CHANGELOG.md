---
title: Changelog
description: Canonical changelog for the Spec Kitty Open Packs repository, following Keep a Changelog and Semantic Versioning.
doc_status: wip
updated: '2026-11-11'
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

- **Every pack has a recorded tree digest** (#194, epic #190; see also #23 and #19;
  [ADR 2026-11-11-2](../architecture/adr/2026-11-11-2-record-a-tree-digest-for-every-pack.md)).
  Each `packs/<name>/` now has a sidecar `packs/<name>.source.yaml`, and the required gate checks
  all of them with `scripts/ci/check-pack-digests.sh` (formerly `check-built-in.sh`), failing on a
  stale, missing or orphan sidecar. `python3 scripts/ci/pack_digest.py --update` restamps them.
  `scripts/ci/built_in_digest.py` stays as a compatibility entry point, and
  `packs/built-in.source.yaml` keeps its path and keys.
  - Release archives now ship each pack's sidecar as `<pack>-vX.Y.Z.source.yaml`.
  - A pack manifest must list every graph node its pack declares, except actions, anti-patterns,
    templates, mission types and step contracts (residual of #182).
  - Manifest node guard: `scripts/ci/validate_pack_schemas.py` now fails a `pack-manifest.yaml`
    that omits a file-backed graph node (#182, #194).
  - For consumers: nothing changes for core. The `.source.yaml` release assets are informational
    and are not core pins. A release now has 3 assets per pack, so check any tooling that counts or
    globs assets. Tags cut before #194 cannot be rebuilt by the current `release_assets.py`; their
    published `.sha256` stays authoritative.
  - For contributors: every pack edit needs `python3 scripts/ci/pack_digest.py --update` in the
    same commit, and the script needs pyyaml. `check-built-in.sh` was removed with no shim.
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
### 🔄 Changed

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
- **The shared JVM toolguides now apply to Kotlin projects** (spec-kitty/spec-kitty#6444).
  **Before:** `java-supply-chain` and `maven-review-checks` were tagged `java`, so a Kotlin
  project, or one that declares only Gradle or Maven, never received them. **After:** both are
  tagged `jvm`. Core expands `java` and `kotlin` to the `jvm` family when it matches doctrine,
  so Java and Kotlin projects both get them; `java-jenny` and `java-conventions` stay
  Java-only. Needs a core that knows the `jvm` family (spec-kitty/spec-kitty#6444).

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

