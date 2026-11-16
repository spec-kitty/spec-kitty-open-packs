# Project Charter — Spec Kitty Open Packs

Curated companion to the authoritative `.kittify/charter/charter.yaml`. This file
holds the rationale; the YAML is what the runtime reads.

## What this repository is

`spec-kitty-open-packs` is the open, free **doctrine-pack marketplace** for Spec
Kitty. It holds **content and packaging** — doctrine artifacts, the `built-in`
distribution and its members, opt-in org packs, presets (compound stacks are
curated presets on `built-in`, not separate packs that `depends_on` a stack),
authoring/usage guides, and a published documentation site. The repo is public,
MIT, and work-in-progress.

**Ownership (operator ruling, 2026-11-16).** Packs and their schema, structure
and validation are no longer a concern of the core repository. Core
([`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty)) is the
deployable, assembler surface; the canonical owner of the logic (the pack
schemas, validation, resolution, the DRG, activation) is the charter repository
([`spec-kitty/spec-kitty-charter`](https://github.com/spec-kitty/spec-kitty-charter)).
Content ownership is in the packs repositories.

**Lockstep with charter `main`.** This repository aligns to the charter, not to
core: `charter.lock.yaml` pins a charter commit, every pack validates against
the schemas at that pin, and the pin follows the charter's `main`. A core
release is never a gate for pack work.

## Governing paradigm

**Author-and-publish, charter-aligned** — doctrine content is authored here
(including content once extracted from core) and published as opt-in packs and
presets; the charter owns the logic that reads it, and core assembles it.

## How we work (enforced policy — see `charter.yaml` for the catalog)

- **Docs are a first-class deliverable.** Follow Common Docs conventions
  (`DIRECTIVE_042`) and the generated-evidence / authored-explanation split
  (`DIRECTIVE_044`): facts derivable from code (pack inventories, counts,
  checksums, validation status) are *generated*; purpose and how-to are
  *authored*, and the two never restate the same datum. Write for the audience
  (`DIRECTIVE_047`); keep docs in sync with shipped behaviour (`DIRECTIVE_037`).
- **Decisions are recorded** as ADRs under `docs/architecture/adr`
  (`DIRECTIVE_003`); an ADR is superseded, never silently edited.
- **BDD is first-class** for pack behaviour: behaviour-driven-development and
  specification-by-example paradigms, `given-when-then-authoring`, and the
  `bdd-scenario-lifecycle` / `example-mapping-workshop` procedures.
- **Gates (fail-closed):** pack validation (errors=0) and built-in parity; the
  docsite builds clean; docs freshness / links / terminology green; generated
  pages are never hand-edited (a checksum drift gate catches it); a changelog
  entry for user-facing change. Tests exist only where they guard real behaviour
  (`DIRECTIVE_041`).
- **Identity discipline:** a pack's `pack_id` is minted once and never
  fabricated downstream. `spec-kitty-open-packs` is the canonical home of the
  `spec-kitty-internal` pack.

## Activation scope (curated, not everything)

Built-in doctrine is **narrowed** to what fits a docs + pack-catalog maintainer
repo. Dropped as irrelevant: the implementation-language profiles and guides
(`drupal-*`, `java-*`, `node-*`, `frontend-*`, `atomic-design`). Kept and relied
on: documentation, communication (`comms-cleo`, `scribe-sally`,
`professional-communications`), diagramming (`diagram-daisy`), doctrine curation
(`doctrine-daphne`, `curator-carla`), review/planning (`reviewer-renata`,
`paula-patterns`, `planner-priti`, `planning-and-tracking`), BDD, and PR/issue
maintenance (`issue-triage-state-machine`).

## Maintainer doctrine — the `spec-kitty-internal` org pack

This repository is the **canonical home** of the `spec-kitty-internal` pack
(`packs/internal`, registered under `charter_packs.org.packs`). Its governing
`base` preset puts maintainer doctrine in force as must-have items in the charter service
(core does not apply them yet; see "Pack skills" in `packs/internal/README.md`): the `kitty-*` skills (`land-pr`,
`issue-triage`, `mission-from-issue`, `report-debrief`, `semi-auto`) and the
`landing-contributor-prs`, `memory-curation-and-escalation`,
`executive-debrief-generation`, `cloud-session-dispatch`, `semi-auto-delivery`,
`project-evolution-postmortem`, and `test-suite-quality-assessment` procedures.

## Mission types

`documentation` (discover → audit → design → generate → validate → publish →
accept) is the blueprint for the docsite build. `software-dev`, `plan`, and
`research` are also available.

## Amending this charter

Change via `/spec-kitty.charter` (edit `interview/answers.yaml`, regenerate) or
by editing `charter.yaml`'s `governance`/`directives` sections directly, then
commit explicitly.
