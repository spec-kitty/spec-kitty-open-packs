# Research: Glossary: docs/context terms and the Op term

## Source

- Core `spec-kitty/spec-kitty` `docs/context/` at `01e577d` (main, 2026-11-18): 28 pages, 287 term tables
  (a `###`/`####` heading followed by a `| Definition |` row), plus vocabulary on pages without tables
  (`mission-types.md`, `ops-vs-missions.md`, `naming-decision-tool-vs-agent.md`, `team-kitty.md`).
- Target contexts at open-packs `d4f4472`: `spec-kitty-core` (foundation, 138 terms) and `spk-internal-glossary`
  (internal, 12 terms). Schema: charter `contracts/packs/schemas/glossary.schema.json` at the lock pin `050d780`.
- `historical-terms.md`, named by #221, no longer exists in core; its content was folded into the pages above.

## Ledger

`research/ledger.yaml` holds one row per source term, built by `tools/build_ledger.py` against the two contexts as they stand on `main` at `d4f4472`: 297 rows. Every foundation row carries its page's reason (`FOUNDATION_REASON`); every override carries its own.

| Verdict | Rows | Meaning |
|---|---|---|
| foundation | 156 | added to `spec-kitty-core` |
| internal | 79 | added to `spk-internal-glossary` |
| exists | 49 | already a term of one of the two contexts; kept unchanged |
| excluded | 8 | not added; reason on the row |
| folded | 3 | same concept as another row (Op, Team Kitty, Drain) |
| alias | 2 | an alias row, added as an alias of its canonical term |

## Classification policy

- **foundation** (consumer): a concept a project meets in its own Missions, charter, packs, CLI output or event logs:
  the charter and activation vocabulary, the DRG relations a pack author writes, Mission topology, branches and lanes,
  the dossier, decisions, events and the glossary runtime's user-visible behaviour.
- **internal** (house): core's code symbols and modules, its architectural test gates and pytest taxonomy, its issue
  tracker labels, product lines, retired hosted vocabulary (Zeitgeist, moment, drain), the tool-vs-agent naming record,
  the docs audience personas, consolidation-gate internals, core's `mission-runtime.yaml` step DAG (a charter mission
  type is `<id>.mission-type.yaml`, its steps ordered by list), and the engagement/egress-consent rationale. Core's
  pytest markers get ids ending `-test-marker` so they do not claim bare words such as `unit` or `contract`.
- **excluded**: generic technology terms (decision `01M7PN8GR51G0YAS30CRRJ0NWP`), things the source says do not exist
  (`glossary/`, the bootstrap proposal, the charter library), a cross-reference, an out-of-scope term, and the seed file
  that retires in core (#5269), and `step contract`, which the charter retired (folded into steps' substeps, #285;
  the term was dropped in #283).
- Status: canonical → `active`, candidate → `draft`, deprecated → `deprecated`.

## Definitions

Foundation definitions are the source text with Markdown links unwrapped and parentheticals citing core code, tests,
ADRs or issues removed (`tools/render_terms.py`). Where the remainder still leaned on core internals, or described a
surface the charter retired (the org charter, `required_<kind>`, `activated_glossary_packs`), `research/rewrites.yaml`
carries a rewritten definition aligned with the charter (AGENTS.md: this repository follows the charter). Internal
definitions keep the source text with links unwrapped. `see_also` is kept only for links that resolve to a term of the
same context.

## Review rework (WP01, 2026-11-18)

The first review (reviewer-renata) moved `guideline` to excluded (core's doctrine precedence layer, no charter kind),
`import-candidate`, `artifactref`, `baseline-key` and the four glossary-runtime design principles to internal, marked
`clarification-burst-policy` as a draft "not shipped", reworded `schema` and `execution-mode-stamp`, and called an
Op sweep "a lapse, not a completion". The status deviations from the map are recorded in `rewrites.yaml` and in spec
decision 5.

## Operator wording (#139)

The identity page's "Human-in-Charge (HiC)" is the term `operator` (avoid: "human in charge", "human in command").
`tools/render_terms.py` rewrites "HiC", "Human-in-Charge" and "human-in-command" to "operator" in every rendered
definition, and `tools/clean_existing.py` does the same for pre-existing foundation definitions; the
`human-in-charge` agent profile id is never rewritten.

## Pre-existing foundation definitions (FR-005)

`tools/clean_existing.py` rewrites 29 pre-existing definitions (the `WorkPackage` alias is a separate edit): the ones
that cited core's `src/` tree, ADRs or `docs/context` pages or said HiC, plus `target-branch`, `current-branch`, `merge-target-branch`, `planning-base-branch`, `structural-debt` and
`charter-content-migration` (core's work-package history, function names and the retired merge command; review
cycle 2) and `review-py-package`, now `deprecated` as a core layout detail (moving it would remove a
shipped id). Term ids and names are unchanged. The whole pipeline is
reproducible from `main`, with core cloned beside this repository at `01e577d` (`../spec-kitty`): restore the two
contexts, run `build_ledger.py`, `render_terms.py --write`, the header and alias edits of WP01, then
`clean_existing.py`. The tools take no paths on the command line.

## Decision 3 reversed (2026-11-18)

The generic technology terms (API, CLI, UI, Markdown, YAML, JSON, SHA256) join foundation as drafts. The writing pack's
kitty-glossary-writing styleguide ("Foundational terms must be defined") and foundation's glossary-curation-interview
tactic ("Identify missing foundational terms") require them, so excluding them contradicted shipped guidance.

## Rebase onto the version batch (2026-11-18)

Rebased onto `main` after #302 and #303. The pipeline's base is now `main`'s two contexts, so #303's
`enforcement-level` term is kept; its citation of a core issue is dropped by `clean_existing.py` (29 rewritten
definitions). No version of this mission's own: it lands inside the batch versions.
