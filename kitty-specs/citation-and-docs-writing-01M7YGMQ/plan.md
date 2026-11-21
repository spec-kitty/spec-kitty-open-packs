# Implementation Plan: Citation and docs writing doctrine

**Branch**: `feat/citation-and-docs-writing` | **Date**: 2026-11-21 | **Spec**: [spec.md](spec.md)
**Input**: Mission specification from `kitty-specs/citation-and-docs-writing-01M7YGMQ/spec.md`

Branch contract: the planning/base branch and the merge target are `feat/citation-and-docs-writing` (`branch_matches_target: true`). The pull request goes from that branch to `main`.

## Summary

State the stable-identifier rule (#219) and the content-anchored citation rule (#150 rule 1) once each in the writing pack's `research-citation-discipline` styleguide, cross-referencing each other, and point the software-dev specify and plan prompts and the ADR drafting tactic at it. Add reproduce-before-resolved, reachability-before-ruling (#150 rules 2-3) and the no-prototyping delegate rule (#176) to the foundation squad procedure, and neutralise its `StatusGateError` example (#274). Record overturned rulings with their measurement in the internal procedure that already owns posting rulings (#150 rule 4). Extract the seven AI-prose tells from internal `report-writing` into a new writing styleguide `ai-writing-tells` that `report-writing` references and the documentation mission and `comms-cleo` reach (#238). Rewrite the common-docs guidance around doc-kitty's frontmatter and neutral examples, with every sibling surface agreeing (#240, #274). Then version, restamp and document.

## Technical Context

**Language/Version**: YAML and Markdown pack content (`schema_version: "1.0"`), validated against the charter contract at the pin in `charter.lock.yaml` (charter `33f3ad4`)
**Primary Dependencies**: `pyyaml`, `jsonschema`, `pytest` (already used by CI; nothing added)
**Storage**: files under `packs/`, `docs/packs/`, `docs/changelog/`, `tests/ci/test_pack_digest.py` (built-in digest constant)
**Testing**: no new tests. The deliverable is guidance text; the evidence is the existing gates (`validate-packs.sh`, `pytest tests` including `test_software_dev_ascii.py` and `test_graph_edge_identity.py`, `check_vocabulary.py`, `gen_pack_reference.py --check`, the digest check, `check_docs_freshness.py`) and the greps in NFR-004 and NFR-005, recorded per work package
**Target Platform**: the charter service at the pin, and the docs site
**Project Type**: content repository (doctrine packs)
**Performance Goals**: N/A (content only)
**Constraints**: principle descriptions within 255 characters (C-003); one edge per unordered pair per pack (C-004); no graph edge from foundation into writing (C-005); software-dev content ASCII-only (NFR-002); one home per rule (NFR-003)
**Scale/Scope**: 1 new styleguide (writing); about 16 edited artefacts across writing, foundation and internal; 4 graph files; the lockstep version set, built-in and internal

## Charter Check

- **Docs are a first-class deliverable**: pack pages regenerated, never hand-edited; changelog entry. PASS.
- **Decisions are recorded**: the four fixed inputs are decision moments in the mission; no ADR, because no repository-level decision changes. PASS.
- **Gates fail closed**: all gates run locally before push and in CI. PASS.
- **Tests only where they guard real behaviour (DIRECTIVE_041)**: no new tests; existing gates and recorded greps are the evidence. PASS.
- **Identity discipline**: one new artefact id (`ai-writing-tells`), no id or file renames. PASS.
- **DIRECTIVE_018**: minor bumps (research.md R5). PASS.
- **DIRECTIVE_051 (supply chain)**: no dependency change. N/A.
- **Alignment**: charter, not core (AGENTS.md); core's pin bump and its CLI halves (core #2897, #5095) are out of scope. PASS.

## Design decisions

1. **Two principles, one family.** `research-citation-discipline` gains "Cite changes by a stable identifier" and "Anchor code citations to content", placed after "Cite the specific locus". Each principle description is short (under 255 characters) and names the other; the full text and the bad/good examples go in same-named patterns and anti-patterns (C-003). The existing "Record retrieval context" principle lists "commit" as retrieval context; it gets a pointer that a commit recorded as retrieval context is ephemeral too.
2. **Reminders in foundation, rule in writing.** The specify and plan prompts and `adr-drafting-workflow` get one sentence each: history is rewritten at close-out, so cite a PR, issue, ADR id or tag; the rule is in the writing pack's `research-citation-discipline` styleguide. Prose only (C-005). The graph wiring goes the other way: writing's `action.graph.yaml` adds scope edges from `foundation::action:software-dev/specify` and `/plan` to the styleguide, the same pattern writing already uses for the retrospect actions.
3. **Squad procedure.** One new step "Check claims first-hand before a ruling" after "Synthesize", carrying both reproduce-before-resolved and reachability-before-ruling; one sentence in the dispatch step for no-prototyping; two short anti-patterns ("Resolved on paper", "Ruling on an unreachable test"). The gate anti-pattern example becomes "a status transition that refuses to run until a squad report is attached".
4. **Overturned rulings.** `cloud-session-dispatch` already says "Post every operator ruling on the governing issue". One sentence follows it: when a measurement overturns a ruling, post the overturn on the same issue with the command and result and link the earlier ruling; do not edit the earlier one.
5. **Shared tells.** New `packs/writing/styleguides/ai-writing-tells.styleguide.yaml` (scope docs) with the seven tells as patterns plus anti-patterns, neutral examples, and no voice or brand rule. `report-writing` keeps its report rules and Spec Kitty voice, replaces its tell patterns with one principle pointing at `writing::styleguide:ai-writing-tells`, and the internal fragment adds `styleguide:report-writing refines writing::styleguide:ai-writing-tells`. `executive-debrief` refines `report-writing` and is unaffected.
6. **Docs wiring.** writing graphs: node `styleguide:ai-writing-tells`; scope edges from `mission_type:documentation`, `action:documentation/generate` and `action:documentation/validate`; `agent_profile:comms-cleo suggests` it; `styleguide:ai-writing-tells suggests styleguide:plain-language`. Manifests derived.
7. **doc-kitty shape.** common-docs principles "Cross-references use related" and "Audience is named in an audience" and their patterns are rewritten: `related` holds page slugs (path under the docs root without `.md`, or `{ref, note}`), an unresolved slug fails a doc-kitty build; `external_references` holds `{url, title, note?}` or `{type, id}`; `audience` is a list of `{profile, guidance_text}`, where `profile` names a persona page (doc-kitty resolves it under `context/audience/`) and `guidance_text` says what that reader gets. A project with no persona pages still names the profile and records the gap. The path form is mentioned once, as legacy for projects whose own validator still reads paths. Tooling notes and the quality test follow. DIRECTIVE_042's two integrity rules and validation lines, the three common-docs tactics and the two audience procedures follow the same wording.
8. **Neutral examples (#274).** ADR rule: "filed under `adr/`, or `adr/<era>/` if the project versions its ADRs"; examples use `adr/` without an era. Examples use a neutral page ("Payment Retries") instead of "Charter Activation"; the "6 of 565 rows" comment becomes a plain "rarely populated" note.

## Project Structure

### Documentation (this mission)

```
kitty-specs/citation-and-docs-writing-01M7YGMQ/
├── spec.md
├── plan.md               # this file
├── research.md           # surface inventory, owner map, edge map, versioning
├── quickstart.md         # gate commands
├── checklists/requirements.md
├── decisions/            # fixed-input decision moments
└── tasks.md              # /spec-kitty.tasks output
```

### Source (repository root)

```
packs/writing/styleguides/ai-writing-tells.styleguide.yaml                (new)
packs/writing/styleguides/{research-citation-discipline,common-docs}.styleguide.yaml
packs/writing/tactics/common-docs-{write,scaffold,find}.tactic.yaml
packs/writing/directives/042-common-docs.directive.yaml
packs/writing/procedures/declare-page-audience.procedure.yaml
packs/writing/{styleguide,mission_type,action,agent_profile}.graph.yaml
packs/foundation/procedures/adversarial-squad-deployment.procedure.yaml
packs/foundation/tactics/communication/adr-drafting-workflow.tactic.yaml
packs/foundation/missions/software-dev/steps/{specify,plan}.prompt.md
packs/internal/styleguides/report-writing.styleguide.yaml
packs/internal/procedures/{cloud-session-dispatch,spec-kitty-page-audience}.procedure.yaml
packs/internal/drg/fragment.yaml, packs/internal/pack.yaml (writing range)
packs/*/pack.yaml, packs/*.source.yaml, packs/*/pack-manifest.yaml, docs/packs/*.md, tests/ci/test_pack_digest.py, docs/changelog/CHANGELOG.md
```

## Implementation Concern Map

### IC-01 — Citation rules (FR-001 to FR-004)
Two principles in `research-citation-discipline` with patterns and examples; reminders in the specify and plan prompts and the ADR tactic; writing scope edges onto the software-dev specify and plan actions.

### IC-02 — First-hand checks (FR-005 to FR-007, FR-013 squad part)
Squad procedure step, dispatch sentence, anti-patterns and the neutral gate example; the overturned-ruling sentence in internal `cloud-session-dispatch`.

### IC-03 — Shared AI-writing tells (FR-008 to FR-010)
New writing styleguide; `report-writing` points at it; internal refines edge; writing graph wiring for the documentation mission, two actions and `comms-cleo`.

### IC-04 — doc-kitty frontmatter and neutral docs examples (FR-011 to FR-013 docs part)
common-docs styleguide rewrite; DIRECTIVE_042, three tactics, two procedures aligned; ADR era optional; neutral page examples.

### IC-05 — Release surface (FR-014)
Versions, manifests, digests, built-in digest constant, pack pages, changelog.

## Complexity Tracking

No charter violations to justify.
