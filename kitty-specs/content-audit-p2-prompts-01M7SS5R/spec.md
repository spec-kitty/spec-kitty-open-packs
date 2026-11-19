# Mission Specification: Content audit P2 (prompts, docs family, documentation and qa missions, internal flows)

**Mission Branch**: `fix/content-audit-p2-266-270`
**Created**: 2026-11-19
**Status**: Draft
**Input**: Issues #266, #267, #268, #269 and #270 (children of epic #263, the 2026-11-14 content audit), with #277 (`spec-kitty implement` naming) decided alongside #266. Dispatched by the orchestrator as one Mission and one PR.

## Intent Summary

The 2026-11-14 audit found pack guidance that contradicts itself, asserts things the consumer does not have, or describes CLI behaviour that changed. An agent following that guidance either picks one side at random, runs a gate that does nothing in its project, or concludes a check passed when it never ran.

- **Primary actor**: an agent loading a pack's step prompts, tactics, styleguides or procedures at runtime, in a consumer repository that is not spec-kitty core.
- **Outcome**: each slice gives one consistent instruction, names only what the consumer has (or says "if the project has one"), and matches `spec-kitty-cli 4.0.0rc9`.
- **Invariant**: built-in content stays consumer-neutral; internal-tier content names the repository's own mechanisms generically, resolved from that repository's charter or docs (operator ruling R1, #270).
- **Boundary**: no new pack schema, no core-only preset, no change to charter logic. Glossary-pack lines for #277 stay with #221/#234.

## User Scenarios & Testing

### User Story 1 - software-dev gives one instruction per step (#266, #277) (Priority: P1)

An agent running the software-dev mission in a web-app repository reads a mission persona with no charter principles it did not choose, one rule on `charter context`, one occurrence-map vocabulary, history rewrites only before the PR is presented, and "planning branch" throughout tasks-finalize. Instructional lines name `spec-kitty agent action implement`, the canonical rc9 entry.

**Acceptance Scenarios**:

1. **Given** `software-dev.mission-type.yaml`, **When** its `content:` is read, **Then** it names no charter principles and lists the mission's real steps.
2. **Given** the implement and review substeps and prompts, **When** read together, **Then** they agree: the bootstrap substep loads charter context for the action once, and the prompt does not ask for it again.
3. **Given** the implement prompt, **When** it describes the occurrence map, **Then** it uses only the `occurrence_map.yaml` schema vocabulary and points at the tactic and `spk-practice-bulk-edit`.
4. **Given** any tactic or directive, **When** it describes linear history, **Then** it says "before the PR is presented", never after merge.
5. **Given** the lines #277 lists outside the glossary pack, **When** they instruct the agent, **Then** they name `spec-kitty agent action implement`.

### User Story 2 - the common-docs family names only what the consumer has (#267) (Priority: P1)

An agent writing docs in a consumer repository is never told to run `regenerate-graph`, a page-inventory lockfile, a `related:` validator or an SEO step as a gate; where those are mentioned they read "if the project has one". A toolguide tells it how to resolve and run the shipped `docs_structural_lint.py`.

**Acceptance Scenarios**:

1. **Given** the common-docs directive, styleguides and tactics, **When** they name a check, **Then** each rule maps to the shipped lint or to "review".
2. **Given** the `common-docs-structural-lint` toolguide, **When** an agent follows it, **Then** it resolves the script and config through `spec-kitty charter pack asset path` / `charter pack path`, and knows `--extended` and the exit codes.
3. **Given** the styleguide, **When** read, **Then** the DIRECTIVE_042 self-test claim is gone.

### User Story 3 - the documentation mission agrees with common-docs (#268) (Priority: P1)

An agent running the documentation mission scaffolds pages into common-docs sections with common-docs frontmatter, so they pass `docs_structural_lint.py --extended`; the plan template and expected outputs describe the documentation flow; validate runs the checks the styleguides attribute to it; one placeholder convention is used.

**Acceptance Scenarios**:

1. **Given** a page scaffolded from each Divio template into the section generate names, **When** the lint runs with `--extended`, **Then** it passes.
2. **Given** the plan template and mission-type, **When** read, **Then** there are no WP, tasks, `research.md` or `data-model.md` references.
3. **Given** publish, **When** it outputs `release.md`, **Then** it is bound to `release-template.md`; the two software-dev template copies are gone.
4. **Given** validate, **When** it runs, **Then** it checks the Divio `type:`, the `updated:` tier and the structural lint, or the styleguides stop claiming it.
5. **Given** prompts, guidelines and templates, **When** grepped, **Then** one placeholder token is used, and guidelines hold only the quality-gate list.

### User Story 4 - the qa mission matches the current CLI (#269) (Priority: P1)

An agent running the qa mission gets no hand-install narrative, no authoring-mission ids, no core internals, the carrier schema inline, `--since` from the status event log, an accept step that names `qa-coverage.json`, and actionable step prompts.

**Acceptance Scenarios**:

1. **Given** `packs/qa`, **When** grepped for `overrides/templates` or `No installer`, **Then** nothing is found, and `EVIDENCE.md` is gone.
2. **Given** prompts, directives and toolguides, **When** grepped, **Then** no FR-, PMG-, source-mission ids or core issue numbers remain.
3. **Given** each qa step prompt, **When** read, **Then** it has what-to-do steps and success criteria built on its bound template.
4. **Given** the README and review prompt, **When** read, **Then** one dated statement covers what `blocking` enforces.

### User Story 5 - internal must-have flows are repo-neutral (#270) (Priority: P2)

A maintainer agent following `kitty-land-pr` in this repository gets correct steps: the repository's own changelog mechanism (`## [Unreleased]` here), its own PR template, and its own vocabulary check (`check_vocabulary.py` here), all resolved from the repository's charter or docs.

**Acceptance Scenarios**:

1. **Given** each must-have artifact in `base`, **When** grepped, **Then** no `spec-kitty/spec-kitty` literal and no core path remains.
2. **Given** `SPEC_KITTY_DOCS_CONVENTIONS` and its two procedures, **When** read, **Then** ADR and audience layout defer to the repository's charter.
3. **Given** `terminology-guard`, **When** read, **Then** it names "the repository's vocabulary check".
4. **Given** the internal README, **When** read, **Then** it says core carries its specifics as a project-tier override; no core-only preset exists.

## Requirements

- **FR-001**: Each instance listed in #266, #267, #268, #269 and #270 is fixed at its current location (the issues' line refs predate the step-contract merge into mission-type substeps).
- **FR-002**: Prompt claims about CLI behaviour are checked against `spec-kitty-cli 4.0.0rc9`.
- **FR-003**: Built-in content stays consumer-neutral; internal content is repo-neutral.
- **NFR-001**: Gates green: `validate-packs.sh`, the charter service check, `check_vocabulary.py`, `gen_pack_reference.py --check`, digests restamped, `tests/ci/test_software_dev_ascii.py`, the tooling tests.
- **NFR-002**: A changelog entry under `## [Unreleased]`.

## Success Criteria

- **SC-001**: Every "Done when" box in #266-#270 is satisfied (with #270's core-issue box dropped by the 2026-11-14 ruling).
- **SC-002**: The PR closes #266, #267, #268, #269 and #270 (and #277 if the orchestrator confirms folding it in).
