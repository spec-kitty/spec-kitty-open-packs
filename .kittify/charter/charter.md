# Project Charter — Spec Kitty Open Packs

Curated companion to the authoritative `.kittify/charter/charter.yaml`. This file
holds the rationale; the YAML is what the runtime reads.

## What this repository is

`spec-kitty-open-packs` is the open, free **doctrine-pack marketplace** for Spec
Kitty. It holds **content and packaging** — doctrine artifacts, individual and
compound packs (`built-in`, `cave-kitty`, `event-driven`, `qa`), authoring/usage
guides, and a published documentation site. The doctrine **logic** (resolution,
the DRG, activation, the manifest schema, the validator) stays upstream in
[`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty) and is
consumed here. The repo is public, MIT, and work-in-progress.

## Governing paradigm

**Extract-then-publish separation** — content is extracted from core and
published here as opt-in packs; the two repositories keep a clean division of
responsibility.

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
(`packs/internal`, registered under `charter_packs.org.packs`). Its org-charter
puts maintainer doctrine in force automatically: the `kitty-*` skills (`land-pr`,
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
