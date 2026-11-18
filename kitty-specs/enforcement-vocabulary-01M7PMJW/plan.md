# Implementation Plan: Directive enforcement vocabulary

**Branch**: `issue-233-enforcement-vocabulary` | **Date**: 2026-11-18 | **Spec**: [spec.md](spec.md)
**Input**: Mission specification from `kitty-specs/enforcement-vocabulary-01M7PMJW/spec.md`

Branch contract: the current branch, the planning/base branch and the merge target are all `issue-233-enforcement-vocabulary` (`branch_matches_target: true`). The pull request goes from that branch to `main`.

## Summary

Define the three enforcement levels once, as the `enforcement-level` term in the foundation `spec-kitty-core` glossary context, and point the authoring guidance at it. Remove self-binding prose (level, criticality, gate posture) from every directive body and from the content that cites directives. Keep `enforcement:` as the pack-supplied default, because the pin requires it, and record that in an ADR. Close the class with a vocabulary-guard rule. Then bump versions, write the changelog entry, restamp digests and regenerate the pack pages.

## Technical Context

**Language/Version**: YAML and Markdown pack content (`schema_version: "1.0"`); Python 3.12 stdlib for the vocabulary guard and its tests
**Primary Dependencies**: the pinned charter contract at `050d780` (`contracts/packs/schemas/directive.schema.json`, `glossary.schema.json`); `pyyaml==6.0.3` and `jsonschema==4.26.0` for `validate-packs.sh` (already in CI)
**Storage**: files under `packs/`, `docs/`, `scripts/ci/`, `tests/vocabulary/`
**Testing**: `python3 -m unittest discover -s tests/vocabulary` (new guard rule: a planted phrase is refused and the clean tree passes); `tests/ci/test_software_dev_ascii.py`; `validate-packs.sh` (also `--cross-pack`), `check-pack-digests.sh`, `gen_pack_reference.py --check`; the charter-service and drift jobs in CI
**Target Platform**: the charter service at the pin (pack composition and registration) and the docs site
**Project Type**: content repository (doctrine packs)
**Performance Goals**: N/A (content only; the guard adds one regex pass per tracked pack file)
**Constraints**: the `enforcement:` field is required at the pin (C-001); no level value changes (C-003); no id or file-name changes (C-004); software-dev content stays ASCII (NFR-002)
**Scale/Scope**: 59 directives across 11 packs read in full; about 10 directive bodies, 14 "in v1" posture lines, 8 cave-dev prompts, 5 graph reasons and about 10 other prose sites (research.md R5)

## Charter Check

- **Docs are a first-class deliverable**: the authoring guide and the artefact reference are updated (FR-003); the pack pages are regenerated, never hand-edited. PASS.
- **Decisions are recorded as ADRs**: the field decision is recorded as `docs/architecture/adr/2026-11-18-1-directive-enforcement-is-a-pack-supplied-default.md` (FR-008). PASS.
- **Gates fail closed**: pack validation errors=0, digests, the vocabulary guard and the pages drift gate all run locally before push, and in CI. PASS.
- **Tests only where they guard real behaviour (DIRECTIVE_041)**: the one new test guards the new guard rule; content edits get no tests. PASS.
- **Identity discipline**: no `pack_id`, artefact id or file name changes. PASS.
- **DIRECTIVE_018**: a minor bump for each pack whose content changes (nothing is removed or renamed, and no rule is tightened); `built-in` moves in lockstep. PASS.
- **DIRECTIVE_035 (bulk edit)**: `change_mode: bulk_edit` with `occurrence_map.yaml`. PASS.
- **DIRECTIVE_051 (supply chain)**: no dependency is added, upgraded or removed. N/A.

## Design decisions

1. **The field stays, as a default** (C-001). At the pin, `enforcement` is in the directive schema's `required` list with the enum `required | lenient-adherence | advisory`, and `additionalProperties: false`. Retiring it would fail validation, and so would adding a `default_enforcement` alias. Reading: the value a pack ships is the default; the adopting charter (core #5207, activation config) decides the level that applies.
2. **One term, not three** (FR-001, FR-002). `term:spec-kitty-core/enforcement-level` defines all three values in one definition. Three terms would invite three drifting definitions. `see_also` points at `directive`, `charter` and `activation-preset`, and the definition says it is distinct from preset `must_have` and `policy.yaml` levels.
3. **Classification rule** (Q1, recommendation A). Remove what claims how strictly the directive (or the directive it cites) binds; keep what describes a concrete check a procedure or tool runs, and keep other senses of the words. Each occurrence is classified in `occurrence_map.yaml`.
4. **Rewording, not deletion, of rules that only carried posture.** DIRECTIVE_051's last integrity rule ("does not introduce a fail-closed handler in v1 ... keep it advisory at the gate level") carries one piece of substance, that omitting the check is not compliance; that already lives in its first rule. The rule is removed and listed in the map as level-only (NFR-003). The scope sentence about "advisory at the transition-gate level in v1" is removed.
5. **Guard rule** (FR-009). `scripts/ci/check_vocabulary.py` gets a repo-own rule, `SELF_BINDING`: a short list of case-insensitive phrase patterns, checked line by line on every tracked pack file. It covers "advisory in vN", "advisory at the ... level", "(this|the) (directive|rule|guidance) is (advisory|required|mandatory|binding|lenient...)", "this is advisory", "not a runtime gate", "makes ... binding charter content", "advisory posture", and a prose "enforcement `required`" (a step restating its directive's level). It uses phrases, not single words, so the other senses of "advisory" and "mandatory" stay legal. Tests: one per pattern is refused, the other-sense controls pass, and the clean tree passes.
6. **Authoring guidance in two places** (FR-003). `docs/guides/author-a-charter-pack.md` (the example's comment and a short paragraph that links the term) and `docs/artefacts/index.md` (the directive row says "a rule, with a default enforcement level"). In the pack itself, the `doctrine-instruction-voice` styleguide gains one principle: state the rule, not its strictness.

## Project Structure

### Documentation (this mission)

```
kitty-specs/enforcement-vocabulary-01M7PMJW/
├── spec.md
├── plan.md               # this file
├── research.md           # pin evidence, classification, inventory
├── occurrence_map.yaml   # bulk-edit classification (DIRECTIVE_035)
├── checklists/requirements.md
├── decisions/            # Q1-Q3 Decision Moments
└── tasks.md              # /spec-kitty.tasks output
```

### Source (repository root)

```
packs/foundation/glossaries/spec-kitty-core.glossary.yaml   # + enforcement-level term
packs/foundation/directives/{051,052,028,049,...}.directive.yaml
packs/foundation/missions/software-dev/software-dev.mission-type.yaml   # 3 substeps
packs/foundation/missions/software-dev/steps/{plan,implement,review}.{prompt,guidelines}.md
packs/foundation/tactics/security/supply-chain-install-safety.tactic.yaml
packs/foundation/{directive,tactic}.graph.yaml               # edge reasons
packs/{internal,qa,writing}/directives/*.directive.yaml
packs/pack-authoring/styleguides/doctrine-instruction-voice.styleguide.yaml
packs/cave-kitty/README.md
packs/*/pack.yaml, pack-manifest.yaml, digests              # versions and restamp
scripts/ci/check_vocabulary.py, tests/vocabulary/test_check_vocabulary.py
docs/guides/author-a-charter-pack.md, docs/artefacts/index.md
docs/architecture/adr/2026-11-18-1-directive-enforcement-is-a-pack-supplied-default.md
CHANGELOG.md, generated pack pages
```

## Implementation Concern Map

| IC | Concern | Requirements |
|----|---------|--------------|
| IC-01 | Level vocabulary: glossary term, authoring docs, styleguide principle, ADR | FR-001, FR-002, FR-003, FR-008 |
| IC-02 | Directive-body sweep, all packs | FR-004, FR-005, NFR-003, C-003, C-004 |
| IC-03 | Steps, prompts, tactic, graph reasons and README sweep | FR-006, FR-007, NFR-002 |
| IC-04 | Guard rule and its tests | FR-009 |
| IC-05 | Versions, changelog, manifests, digests and pages | FR-010, NFR-001 |

Order: IC-04 is written red-first against the current tree (it must fail on main's 14 lines), IC-02 and IC-03 turn it green, IC-01 is independent, and IC-05 runs last.

## Risks

- **Over-reach**: removing a rule's substance along with its posture. Mitigation: NFR-003, and every removal is listed in the map.
- **Guard false positives** on other senses. Mitigation: phrase patterns only, with other-sense controls in the tests.
- **Collisions**: #266 (software-dev prompts) and #273 (directive bodies) have no open PR today. If either lands first, rebase with a signed rebase and restamp the changelog and digests.
