---
title: Pack Catalog Proposal
description: Proposed set of domain and purpose doctrine packs carved from the Spec Kitty built-in corpus, with source-artifact mappings, dependencies, and compound stacks.
doc_status: wip
updated: '2026-10-14'
related:
- docs/guides/author-a-doctrine-pack.md
- docs/guides/compose-packs.md
- README.md
---
# Pack Catalog Proposal

> **🚧 Proposal, not a materialized catalog.** This document proposes how the current Spec
> Kitty **built-in** doctrine corpus could be carved into coherent, composable **packs**. It
> is the grounding for the per-pack tracking issues in this repository. Names, boundaries,
> and membership are **subject to change** and will be refined issue-by-issue. Doctrine
> *logic* stays in [`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty); this
> repository owns the *content* and *packaging*.

## Why carve the monolith

Spec Kitty ships built-in doctrine as one bundle, and its default is "activate everything
when not explicitly constrained." A consumer that skips the (unenforced) charter step
inherits the whole multi-domain corpus and floods every session's context. Packs replace the
monolith with opt-in slices. This proposal is the downstream content plan for the core
pack-ecosystem epics:

- [#2466 — Doctrine/Charter extensibility & pack ecosystem](https://github.com/spec-kitty/spec-kitty/issues/2466) (umbrella)
- [#2467 — Split built-in doctrine into packs + compound packs (KEYSTONE)](https://github.com/spec-kitty/spec-kitty/issues/2467)
- [#2471 — Standalone pack validator](https://github.com/spec-kitty/spec-kitty/issues/2471)
- [#2539 — Pack trust, verifiability & verified distribution](https://github.com/spec-kitty/spec-kitty/issues/2539)

## Design principles

1. **One small foundation, many focused domains.** `core-engineering` is the lean,
   language-agnostic default. Every other pack `depends_on` it so consumers get a coherent
   base without the full corpus.
2. **Coherence over completeness.** A pack is a slice a team would adopt *as a unit* — not an
   alphabetical bucket. If two artifacts are always used together, they belong in the same
   pack.
3. **Reuse built-in artifacts.** Most packs are *curated subsets* of existing built-in
   artifacts, referenced by their current IDs — not rewrites.
4. **Compound packs demonstrate horizontal composition.** Ready-made stacks (`java-ddd-stack`,
   …) bundle base packs via `depends_on` so a consumer configures one name.

## Base packs

| # | Pack | Purpose | `depends_on` |
| --- | --- | --- | --- |
| 1 | `core-engineering` | Language-agnostic engineering backbone — the lean default. | — |
| 2 | `domain-driven-design` | Strategic + tactical DDD: bounded contexts, aggregates, ubiquitous language. | core-engineering |
| 3 | `test-and-bdd` | Test-first, BDD, specification-by-example, defect diagnosis. | core-engineering |
| 4 | `python-development` | Python conventions, review checks, mutation tooling. | core-engineering |
| 5 | `java-development` | Java conventions, Maven review checks. | core-engineering |
| 6 | `frontend-webdesign` | Atomic design, component state, TS mutation tooling. | core-engineering |
| 7 | `architecture-and-modeling` | C4 modeling, diagramming, architectural review. | core-engineering |
| 8 | `documentation-and-glossary` | Living docs, ADRs, common-docs, glossary curation. | core-engineering |
| 9 | `git-delivery-workflow` | Branching models, PR discipline, commit signing, trackers. | core-engineering |
| 10 | `refactoring-and-simplification` | Semantic compression + the refactoring catalog. | core-engineering |
| 11 | `adversarial-review` | Adversarial squads, review cadence, defect-class closure. | core-engineering |
| 12 | `brownfield-onboarding` | Legacy triage, forensic audit, reverse-speccing, migration. | core-engineering |
| 13 | `planning-and-analysis` | Scoping, risk, prioritisation, requirements validation, tracing. | core-engineering |
| 14 | `structured-prompt-driven-development` | SPDD paradigm + REASONS canvas. | core-engineering |
| 15 | `doctrine-authoring` | Meta-pack for pack/skill authors and doctrine maintainers. | core-engineering |
| 16 | `spec-kitty-internal` | Spec Kitty's own dogfooded doctrine + charter: contributor/maintainer workflow, review process, tracker processing. | core-engineering, doctrine-authoring, git-delivery-workflow, adversarial-review |
| 17 | `event-driven` | Event-sourced design: versioned events, one canonical writer, projections, upcasting, idempotent consumers. | core-engineering, domain-driven-design |

### 1. `core-engineering`

The lean default every project can adopt without domain flooding.

- **Directives:** `001-architectural-integrity-standard`, `024-locality-of-change`,
  `025-boy-scout-rule`, `030-test-and-typecheck-quality-gate`, `031-context-aware-design`,
  `032-conceptual-alignment`, `044-canonical-sources-and-unification`.
- **Tactics:** `easy-to-change`, `avoid-gold-plating`, `input-validation-fail-fast`,
  `focused-function-complexity-check`, `locality-of-change`,
  `change-apply-smallest-viable-diff`, `canonical-source-unification`.
- **Agent profiles:** `generic-agent`, `implementer-ivan`, `human-in-charge`.

### 2. `domain-driven-design`

- **Paradigms:** `domain-driven-design`, `deep-module-design`.
- **Styleguides:** `aggregate-design-rules`.
- **Tactics (analysis):** `bounded-context-identification`, `bounded-context-canvas-fill`,
  `context-boundary-inference`, `context-mapping-classification`,
  `entity-value-object-classification`, `strategic-domain-classification`,
  `terminology-extraction-mapping`.
- **Tactics (architecture):** `aggregate-boundary-design`, `anti-corruption-layer`,
  `domain-event-capture`, `language-driven-design`, `reference-architectural-patterns`,
  `problem-decomposition`.
- **Procedures:** `event-storming-discovery`, `domain-aware-decision-interview`.
- **Agent profiles:** `architect-alphonso`, `paula-patterns`.

### 3. `test-and-bdd`

- **Paradigms:** `behaviour-driven-development`, `specification-by-example`.
- **Directives:** `034-test-first-development`, `036-black-box-integration-testing`,
  `041-tests-as-scaffold-not-friction`.
- **Styleguides:** `testing-principles`, `test-desiderata-and-boundaries`,
  `mutation-aware-test-design`.
- **Tactics:** `behavior-driven-development`, `development-bdd`,
  `five-paradigm-parallel-debugging`.
- **Procedures:** `bdd-scenario-lifecycle`, `example-mapping-workshop`,
  `test-first-bug-fixing`, `disciplined-defect-diagnosis`,
  `development-assist-test-cleanup`.
- **Agent profiles:** `debugger-debbie`.

### 4. `python-development`

- **Styleguides:** `python-conventions`.
- **Toolguides:** `python-review-checks`, `python-mutation-tools`.
- **Agent profiles:** `python-pedro`.

### 5. `java-development`

- **Styleguides:** `java-conventions`.
- **Toolguides:** `maven-review-checks`.
- **Agent profiles:** `java-jenny`.

### 6. `frontend-webdesign`

- **Paradigms:** `atomic-design`.
- **Tactics (architecture):** `atomic-design-review-checklist`, `atomic-state-ownership`,
  `cross-cutting-state-via-store`, `compositional-stream-boundaries`,
  `interface-variation-design`.
- **Toolguides:** `typescript-mutation-tools`.
- **Agent profiles:** `frontend-freddy`, `designer-dagmar`, `node-norris`.

### 7. `architecture-and-modeling`

- **Paradigms:** `c4-incremental-detail-modeling`.
- **Toolguides:** `mermaid-diagramming`, `plantuml-diagramming`.
- **Tactics (architecture):** `c4-zoom-in-architecture-documentation`,
  `architecture-diagram-review-checklist`, `dependency-hygiene`,
  `deepening-opportunity-assessment`, `paula-patterns-architecture-scout-review`.

### 8. `documentation-and-glossary`

- **Directives:** `003-decision-documentation-requirement`, `037-living-documentation-sync`,
  `042-common-docs`.
- **Styleguides:** `common-docs`, `kitty-glossary-writing`.
- **Toolguides:** `contextive`.
- **Tactics:** `common-docs-curation`, `common-docs-find`, `common-docs-scaffold`,
  `common-docs-write`, `adr-drafting-workflow`, `documentation-curation-audit`,
  `usage-examples-sync`, `glossary-curation-interview`, `traceable-decisions`,
  `decision-marker-capture`, `stakeholder-alignment`, `code-documentation-analysis`.
- **Procedures:** `drill-down-documentation`, `documentation-gap-prioritization`.
- **Agent profiles:** `curator-carla`.

### 9. `git-delivery-workflow`

- **Paradigms:** `git-flow`, `trunk-based`, `shared-branch-ci`, `execution-lanes`.
- **Directives:** `029-agent-commit-signing-policy`, `033-targeted-staging-policy`,
  `045-prs-only-and-read-intent`, `046-readable-consistent-prs`.
- **Toolguides:** `git-agent-commit-signing`, `github-tracker`.
- **Tactics:** `clean-linear-commit-history`, `pr-agent-worktree-isolation`.
- **Procedures:** `tracker-organisation-workflow`, `issue-triage-state-machine`.

### 10. `refactoring-and-simplification`

- **Paradigms:** `semantic-compression`.
- **Tactics:** the `refactoring/*` catalog (`change-function-declaration`,
  `combine-functions-into-transform`, `conditional-to-strategy`,
  `consolidate-conditional-expression`, `encapsulate-record`, `encapsulate-variable`,
  `extract-class-by-responsibility-split`, …), `boring-code-review`,
  `generated-code-stewardship`.
- **Procedures:** `refactoring`.
- **Agent profiles:** `randy-reducer`.

### 11. `adversarial-review`

- **Styleguides:** `adversarial-squad-cadence`.
- **Directives:** `040-recurring-bug-structural-intervention`,
  `043-close-defect-class-by-construction`.
- **Tactics:** `adversarial-qa-handoff`, `iterative-deepening-review`,
  `code-review-incremental`, `architectural-gate-non-vacuity`.
- **Procedures:** `adversarial-squad-deployment`, `post-merge-arch-gate-adjudication`.
- **Agent profiles:** `reviewer-renata`.

### 12. `brownfield-onboarding`

- **Paradigms:** `brownfield-onboarding`.
- **Tactics (analysis):** `forensic-repository-audit`, `reverse-speccing`,
  `split-brain-authority-detection`, `connascence-analysis`.
- **Procedures:** `legacy-codebase-triage`, `situational-assessment`,
  `migrate-project-guidance-to-spec-kitty-charter`.
- **Agent profiles:** `researcher-robbie`.

### 13. `planning-and-analysis`

- **Directives:** `010-specification-fidelity-requirement`.
- **Styleguides:** `planning-and-tracking`, `tiered-standards`.
- **Tactics:** `ammerse-impact-analysis`, `premortem-risk-identification`,
  `moscow-scoping-lens`, `eisenhower-prioritisation`, `requirements-validation-workflow`,
  `safe-to-fail-experiment`, `dialectic-research`, `analysis-extract-before-interpret`.
- **Procedures:** `mission-tracer-files`, `mission-wrap-up-sequence`.
- **Agent profiles:** `planner-priti`.

### 14. `structured-prompt-driven-development`

- **Paradigms:** `structured-prompt-driven-development`.
- **Directives:** `038-structured-prompt-boundary`.
- **Styleguides:** `reasons-canvas-writing`.
- **Tactics:** `reasons-canvas-fill`, `reasons-canvas-review`.

### 15. `doctrine-authoring`

Meta-pack for people who *build* packs, skills, and doctrine.

- **Directives:** `018-doctrine-versioning-requirement`, `028-search-tool-discipline`.
- **Styleguides:** `deployable-skill-authoring`.
- **Toolguides:** `terminology-guard`, `efficient-local-tooling`, `rtk-search-tooling`.
- **Procedures:** `onboard-external-agent-to-pack`.
- **Agent profiles:** `doctrine-daphne`.

### 16. `spec-kitty-internal`

Spec Kitty's **own** doctrine, dogfooded as an open pack — the encoded version of how the
Spec Kitty project itself is run, so contributors and downstream teams can adopt (or study)
its way of working. Partly a curation of built-in artifacts that describe the project's
process, partly **net-new artifacts** derived from the repository's own maintainer/contributor
material (`HOW_TO_MAINTAIN.md`, `CONTRIBUTING.md`, `RELEASE_CHECKLIST.md`, tracker
conventions). Ships the project's own `org-charter.yaml`. Grounded in the catfooding epic
[core #2196](https://github.com/spec-kitty/spec-kitty/issues/2196).

- **Directives:** `039-lynn-cole-engineering-culture`, `025-boy-scout-rule` (curated),
  `044-canonical-sources-and-unification` (curated); net-new: contributor-workflow and
  maintainer-workflow directives encoding PR-landing, review gates, and release discipline.
- **Styleguides:** `planning-and-tracking`, `adversarial-squad-cadence`, `tiered-standards`;
  net-new: review-process and issue-tracker-processing styleguides.
- **Tactics:** `autonomous-operation-protocol`, `clean-linear-commit-history`,
  `pr-agent-worktree-isolation`, `frozen-baseline-shrink-only-ratchet`, `ownership-map-leeway`.
- **Procedures:** `tracker-organisation-workflow`, `issue-triage-state-machine`,
  `mission-wrap-up-sequence`, `post-merge-arch-gate-adjudication`,
  `adversarial-squad-deployment`, `development-assist-test-cleanup`.
- **Agent profiles:** `human-in-charge`, `reviewer-renata`, `doctrine-daphne`,
  `retrospective-facilitator`.
- **Charter:** ships `org-charter.yaml` — the compiled Spec Kitty charter (catfooding).

This pack doubles as the reference example for "how do I encode my team's whole way of
working as a pack," and as the eventual self-governance pack for this very repository.

### 17. `event-driven`

**Materialized** in [`packs/event-driven/`](../../packs/event-driven/README.md). Mostly
**net-new** content: the built-in corpus has the event *capture* tactic but no rules for
versioning, writing, projecting and consuming events. It encodes the event-native direction of
Spec Kitty core (one canonical writer behind an event-bridge port, versioned events, side effects
in consumers) for any team that builds that way.

- **Paradigms:** net-new `evd-event-sourced-design`; built-in `domain-driven-design`,
  `deep-module-design` (referenced by DRG edge).
- **Directives:** net-new `EVD_001`–`EVD_006` (schema version on every event, one canonical
  writer, immutable past-tense facts, latest-version producers and declared-version consumers,
  side effects in consumers, shared contracts only).
- **Styleguides:** net-new `evd-event-naming-and-payload`.
- **Tactics:** net-new `evd-event-versioning-and-upcasting`, `evd-event-bridge-port`,
  `evd-projection-replay`, `evd-idempotent-consumer`; built-in `domain-event-capture`,
  `anti-corruption-layer`, `reference-architectural-patterns` (referenced by DRG edge).
- **Procedures:** built-in `event-storming-discovery` (referenced by DRG edge).
- **Glossary:** net-new `evd-glossary`.
- **Assets:** a worked example after Fowler's *Event Sourcing* article, set on a Spec Kitty
  lane board.

## Compound packs (horizontal composition)

The four compound packs below are tracked together under a **single epic** rather than one
issue each — they are demonstrations of horizontal composition over the base packs and move
as a group once their constituents exist.

These declare `depends_on` over base packs; a consumer configures **one** name.

| Compound pack | Bundles |
| --- | --- |
| `java-ddd-stack` | core-engineering + domain-driven-design + java-development + test-and-bdd + architecture-and-modeling |
| `python-service-stack` | core-engineering + python-development + test-and-bdd + git-delivery-workflow |
| `web-frontend-stack` | core-engineering + frontend-webdesign + test-and-bdd + refactoring-and-simplification |
| `quality-and-review-stack` | core-engineering + adversarial-review + refactoring-and-simplification + test-and-bdd |

## Intentionally staying in core (not packaged here)

Some built-in artifacts are foundational runtime mechanics rather than domain doctrine, and
are expected to remain built-in (or move only when core decides). Examples:
`035-bulk-edit-occurrence-classification` and its `occurrence-classification-workflow`,
`model-task-routing`, mission-type/step-contract machinery, and the retrospective mechanics.
This proposal does **not** claim them.

## From proposal to issues

Each of the **17 base packs** above maps to its own tracking issue in this repository,
labelled `pack` + `doctrine` and cross-referencing the relevant core epic. The **four
compound packs** are tracked under a single `epic` + `compound-pack` umbrella issue rather
than one issue each. See the
[issue tracker](https://github.com/spec-kitty/spec-kitty-open-packs/issues). Membership lists
here are a **starting point** — each issue refines its own pack's contents during authoring.
