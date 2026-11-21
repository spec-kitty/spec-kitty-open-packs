# Mission Specification: Citation and docs writing doctrine

**Mission Branch**: `feat/citation-and-docs-writing`
**Created**: 2026-11-21
**Status**: Draft
**Input**: Issues #219, #150, #238 and #240 under epic #288, with #274 (the common-docs and adversarial-squad examples only) and #176 (the squad procedure's delegate rule only) folded in. Dispatched with operator defaults accepted on 2026-11-21 (recorded as decision moments). #210 is not folded in (see C-006).

## Intent Summary

Four writing failures recur in missions that consume these packs:

1. **Citations that do not survive change.** Specs, plans, ADRs and briefs cite bare commit SHAs and bare line ranges. The mission lifecycle itself rewrites history (close-out compaction, rebase onto a moving upstream), so a SHA written during a mission is expected to dangle, and line numbers drift within a round. A rewritten SHA can still sit in the object store, so a lookup says "commit" while the object is unreachable.
2. **Rulings issued without first-hand checks.** Briefs and rulings declare a blocker resolved without reproducing it, and lean on a named acceptance test that does not exist or cannot run.
3. **AI-prose rules reach only internal reports.** The em-dash, "not just X but Y", intensifier, buzzword, rule-of-three and puffery rules live in the internal `report-writing` styleguide. No consumer styleguide applies them to documentation pages.
4. **The common-docs styleguide teaches shapes doc-kitty rejects.** It recommends `audience:` as a repository path and `related:` as repo-relative `.md` paths. doc-kitty reads `audience` as a list of `{profile, guidance_text}`, `related` as page slugs, and other links as `external_references`. Its examples also use Spec Kitty's own ADR eras and pages.

- **Primary actors**: an agent writing a spec, plan, ADR, research note or squad brief; an agent or writer producing documentation pages (including `comms-cleo`); an orchestrator running an adversarial squad.
- **Trigger**: a durable artifact cites a change or a code location; a squad brief or ruling calls a blocker resolved or relies on an acceptance test; a documentation page is written or its frontmatter is touched.
- **Outcome**: one styleguide states, once, how durable artifacts cite changes (stable identifier) and code (content anchor, counts carry their command); the squad procedure requires reproduction and reachability before a ruling; one shared writing styleguide lists the AI-prose tells and is reached from the documentation mission and `comms-cleo`; the common-docs guidance teaches doc-kitty frontmatter with neutral examples.
- **Invariants**: (a) each rule has exactly one home; other surfaces point to it; (b) no writing-pack surface still recommends a path-string `audience` or a repository-path `related`; (c) consumer packs carry no Spec Kitty core symbols, ADR eras or page names as examples; (d) software-dev mission content stays ASCII.
- **Boundary**: "stable identifier" means a PR number, issue number, ADR id, release tag, or a symbolic description of the change. It does not forbid SHAs outright: a SHA is allowed when necessary and annotated as ephemeral.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Citations that survive a rebase (Priority: P1)

A planner writing `plan.md` wants to say which earlier change introduced a rename. Instead of a bare SHA, they cite the PR number and describe the rename. When they cite a function, they write `path::qualname` or a path with a quoted anchor, not `file.py:120-140`. When they cite a count, they put the command that produced it next to it.

**Why this priority**: #219 and #150 rule 1 are the same family; the dangling-SHA failure has been seen repeatedly in core missions.

**Independent Test**: the `research-citation-discipline` styleguide carries both rules, each once, cross-referencing each other, and the software-dev specify and plan prompts and the ADR drafting tactic carry a one-line reminder that points to it.

**Acceptance Scenarios**:

1. **Given** the writing pack, **When** an agent loads `research-citation-discipline`, **Then** it reads a stable-identifier principle (PR, issue, ADR id, release tag or symbolic description; a SHA only when necessary and annotated as ephemeral, because the lifecycle rewrites history) and a content-anchored citation principle (`path::qualname` or path plus quoted anchor, not a bare line range; a cited count carries its command).
2. **Given** the software-dev specify or plan step, **When** an agent authors the artifact, **Then** the prompt reminds it that a SHA written now will not resolve after close-out and names the styleguide.
3. **Given** the software-dev specify or plan action, **When** the charter context resolves its doctrine, **Then** the citation styleguide is in scope.

### User Story 2 - Check before you rule (Priority: P1)

An orchestrator's squad synthesis says "the blocker from round 1 is resolved". Before writing that, the orchestrator reproduces the blocker against the current head. Before a ruling relies on "test X proves it", it checks test X exists and runs. A delegate validating instructions reads code and runs existing tests; it does not prototype the change.

**Why this priority**: #150 rules 2-3 and #176 change the same procedure; one edit avoids churn.

**Independent Test**: the `adversarial-squad-deployment` procedure carries the reproduce, reachability and no-prototyping rules, each once.

**Acceptance Scenarios**:

1. **Given** the procedure, **When** a brief or ruling calls a blocker resolved, **Then** a step requires reproducing it first and recording how.
2. **Given** a ruling that names an acceptance test, **When** the ruling is written, **Then** a step requires checking the test exists and can run.
3. **Given** the dispatch step, **When** a delegate validates instructions, **Then** it reads code and runs existing tests only, and does not prototype, simulate or dry-run the change.
4. **Given** the "hard-wiring the squad as a gate" anti-pattern, **When** a consumer reads it, **Then** its example uses no Spec Kitty core symbol.

### User Story 3 - Overturned rulings carry their measurement (Priority: P3)

A Spec Kitty maintainer finds that a measurement contradicts an earlier operator ruling. They post the overturn on the governing issue with the command and result that overturned it, linking the earlier ruling.

**Independent Test**: the rule sits in the internal pack, in the procedure that already owns "post every operator ruling on the governing issue".

### User Story 4 - One list of AI-prose tells for every page (Priority: P2)

A writer producing a docs page, or `comms-cleo` validating a draft, runs one checklist of machine-prose tells. The internal report styleguide uses the same list by reference, so the rules never drift apart.

**Independent Test**: a new writing styleguide holds the rules; `report-writing` references it and no longer restates them; the documentation mission, its generate and validate actions, and `comms-cleo` reach it.

**Acceptance Scenarios**:

1. **Given** the writing pack, **When** an agent loads the new styleguide, **Then** it reads the seven tells (em-dash rationing, "not just X but Y", empty intensifiers and throat-clearing, LLM buzzwords, rule of three and uniform bullet openers, puffery, gathered versus synthesised figures) with neutral examples and no Spec Kitty voice or brand rules.
2. **Given** the internal `report-writing` styleguide, **When** it is read, **Then** it points to the shared styleguide for the tells and keeps only its report-specific and Spec Kitty voice rules.
3. **Given** the documentation mission or `comms-cleo`, **When** charter context resolves, **Then** the shared styleguide is reachable.

### User Story 5 - doc-kitty frontmatter as the default (Priority: P2)

A consumer agent writes a new docs page following the common-docs guidance. It writes `audience` as a list of `{profile, guidance_text}`, `related` as page slugs, and puts external links under `external_references`. The examples it copies are neutral (no Spec Kitty ADR eras or pages).

**Independent Test**: the common-docs styleguide, the three common-docs tactics, DIRECTIVE_042, the `declare-page-audience` procedure and the internal page-audience procedure agree on the doc-kitty shape; the path form appears only as legacy.

**Acceptance Scenarios**:

1. **Given** the common-docs styleguide, **When** an agent reads its principles, patterns and tooling notes, **Then** `audience`, `related` and `external_references` use the doc-kitty shape, and the path form is named only as a legacy form.
2. **Given** any writing-pack surface, **When** it describes `related:` or `audience:`, **Then** it does not contradict the styleguide.
3. **Given** the ADR layout rule, **When** a consumer reads it, **Then** an era subdirectory is optional ("if the project versions its ADRs; otherwise `adr/`") and the examples name no Spec Kitty era.

### Edge Cases

- A SHA is the only identifier (an unpushed local commit, a forensic note about an orphaned object): allowed, marked ephemeral or pre-rewrite, with a symbolic description beside it.
- A count whose command is expensive or non-deterministic: record the command and the date, and label the count a measurement at that point.
- A project that does not use doc-kitty and still keeps path-form `related:`: the styleguide names the path form as legacy; it does not ban the project's own validator.
- A page with no persona pages: doc-kitty soft-misses an unresolved `profile`; the guidance says to name the profile in plain words in `guidance_text` and record the gap.
- `report-writing` keeps "Keep the Spec Kitty voice": it is house voice, not an AI-prose tell, so it stays internal.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status | Delivery | No-op passable? |
|----|-------|------------|----------|--------|----------|-----------------|
| FR-001 | Stable-identifier citation principle | As an author of a durable artifact, I want `research-citation-discipline` to state that changes are cited by a stable identifier (PR, issue, ADR id, release tag, or a symbolic description), and that a SHA is allowed only when necessary and annotated as ephemeral or pre-rewrite because the lifecycle rewrites history, with a bad and good example, so that citations survive close-out. | High | Open | [build] | no |
| FR-002 | Content-anchored citation principle | As an author, I want the same styleguide to state that durable artifacts cite code as `path::qualname` or a path plus a quoted anchor, not a bare line range, and that a cited count carries the command that produced it, cross-referenced with FR-001 and with the existing "cite the specific locus" principle, so that citations survive edits. | High | Open | [build] | no |
| FR-003 | Authoring-step reminder | As a spec or plan author, I want the software-dev specify and plan step prompts and the foundation `adr-drafting-workflow` tactic to carry a one-sentence reminder that a SHA written now will not resolve after close-out, naming the `research-citation-discipline` styleguide, so that the rule is in front of the author. | High | Open | [build] | no |
| FR-004 | Citation styleguide in scope for specify and plan | As an agent, I want the writing pack's graph to scope `research-citation-discipline` to the software-dev specify and plan actions, so that charter context delivers it where specs and plans are written. | Medium | Open | [build] | no |
| FR-005 | Reproduce before resolved; reachability before ruling | As an orchestrator, I want `adversarial-squad-deployment` to require that a brief or ruling calling a blocker resolved reproduces it first, and that a ruling relying on a named acceptance test checks the test exists and can run, so that rulings rest on first-hand checks. | High | Open | [build] | no |
| FR-006 | No prototyping by delegates | As an orchestrator, I want the procedure's dispatch step to say delegates validate by reading code and running existing tests, never by prototyping, simulating or dry-running the change, so that work is not done twice. | Medium | Open | [build] | no |
| FR-007 | Overturned rulings recorded with the measurement | As a Spec Kitty maintainer, I want the internal procedure that owns "post every operator ruling on the governing issue" to require that an overturned ruling is posted there with the measurement that overturned it and a link to the earlier ruling, so that the reversal is auditable. | Medium | Open | [build] | no |
| FR-008 | Shared AI-writing-tells styleguide | As a writer, I want a writing-pack styleguide holding the seven AI-prose tells, generalised with neutral examples and no house voice, so that docs and reports apply one list. | High | Open | [build] | no |
| FR-009 | report-writing references the shared list | As a maintainer, I want `report-writing` to point to the shared styleguide instead of restating the tells, keeping only its report-specific and Spec Kitty voice rules, and the internal graph to link the two, so that there is one authority. | High | Open | [build] | no |
| FR-010 | Shared styleguide wired for docs | As `comms-cleo` or a docs action, I want the shared styleguide scoped to the documentation mission and its generate and validate actions and suggested by `comms-cleo`, so that it reaches docs work beside `plain-language` and `professional-communications`. | High | Open | [build] | no |
| FR-011 | common-docs teaches doc-kitty frontmatter | As a docs author, I want the common-docs styleguide's principles, patterns, examples, tooling notes and quality test to teach `audience` as `{profile, guidance_text}` entries, `related` as page slugs (optionally `{ref, note}`), and other links under `external_references`, naming the path form only as legacy, so that I write the shape doc-kitty reads. | High | Open | [build] | no |
| FR-012 | Sibling docs surfaces agree | As an agent, I want DIRECTIVE_042, the `common-docs-write`, `common-docs-scaffold` and `common-docs-find` tactics, the `declare-page-audience` procedure, and the internal `spec-kitty-page-audience` procedure to agree with FR-011, so that no surface recommends the path form. | High | Open | [build] | no |
| FR-013 | Neutral common-docs and squad examples | As a consumer, I want the common-docs styleguide and tactics to make the ADR era optional with no Spec Kitty era in examples, to drop the "Charter Activation" and "6 of 565 rows" examples, and the squad procedure's gate anti-pattern to drop `StatusGateError`, so that examples are not opaque Spec Kitty internals. | Medium | Open | [build] | no |
| FR-014 | Release surface | As a consumer, I want the changed packs versioned per DIRECTIVE_018, digests and manifests restamped, pack reference pages regenerated, docs freshness kept and a changelog entry, so that the release surface reflects the change. | High | Open | [evidenced-by-run] | n/a -- evidence: the digest, manifest, pack-reference and freshness gates |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Gates green | `validate-packs.sh`, `pytest tests`, `check_vocabulary.py`, `gen_pack_reference.py --check` and `check_docs_freshness.py --base origin/main` exit 0 and the per-pack digests match; the charter-service check passes in CI. | Reliability | High | Open |
| NFR-002 | Software-dev content stays ASCII | 0 non-ASCII characters in software-dev mission files (`tests/ci/test_software_dev_ascii.py` passes). | Compatibility | High | Open |
| NFR-003 | One home per rule | Each new rule (stable identifier, content anchor, reproduce-before-resolved, reachability-before-ruling, no prototyping, overturned-ruling record, each AI-prose tell) is defined in exactly 1 artefact; other surfaces state it in at most one sentence and name the owner. | Maintainability | High | Open |
| NFR-004 | No path-form recommendation | `grep` over `packs/writing` and `packs/internal` for `repo-relative .md path` and `audience: ../` returns 0 recommended uses (legacy mentions labelled as legacy only). | Correctness | High | Open |
| NFR-005 | No Spec Kitty examples in the touched consumer surfaces | `grep -rn "adr/4.x\|adr/3.x\|Charter Activation\|StatusGateError\|6 of 565" packs --include=*.yaml` hits only `packs/internal`. | Portability | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Charter alignment | Validate against the charter pin in `charter.lock.yaml`; core compatibility does not block or reshape the work (AGENTS.md). | Technical | High | Open |
| C-002 | Fixed homes | #219 is a principle in `research-citation-discipline`, not a directive; #238 is a shared `writing` styleguide that `report-writing` references; #240 makes doc-kitty's shape the consumer default; #150 rule 4 is in `internal` (operator rulings and defaults, recorded as decision moments). | Business | High | Open |
| C-003 | Principle length cap | Styleguide principle descriptions stay within the 255-character cap (ADR-0067); longer text goes in a same-named pattern. | Technical | High | Open |
| C-004 | Graph edge identity | At most one edge per unordered pair in a pack (the edge-identity test). | Technical | Medium | Open |
| C-005 | Foundation does not depend on writing | Foundation surfaces (the step prompts, the ADR tactic, the squad procedure) name writing artefacts in prose only; they carry no graph edge into writing. Edges from writing onto foundation actions are allowed. | Technical | High | Open |
| C-006 | Out of scope | #210 (needs #207's owner's agreement, not on record); the #176 step-prompt edits (left with #207, which orders prompt work after #266); the rest of #274 outside the common-docs surfaces and the squad procedure; the core CLI halves of #219 (core #2897) and #150 (core #5095); core's pin bump. | Business | Medium | Open |

### Key Entities

- **Stable identifier**: a reference to a change that survives history rewrites: PR or issue number, ADR id, release tag, or a symbolic description.
- **Content anchor**: a reference to code by `path::qualname` or by path plus a quoted string, rather than by line number.
- **AI-prose tell**: a recurring surface pattern of machine-generated prose that readers discount.
- **doc-kitty frontmatter shape**: `audience: [{profile, guidance_text}]`, `related: [<page-slug> | {ref, note}]`, `external_references: [{url, title, note?} | {type, id}]`.

## Assumptions

- `profile` in doc-kitty's `audience` resolves to the persona page at `context/audience/<profile>`; a miss renders the humanised name and warns, while a `related` miss fails the build (doc-toolkit 0.3.0, `lib/metadata.ts::resolveProfile` and `components/slots/Audience.astro`).
- Versioning: minor (additive guidance, one new styleguide; the frontmatter shape changes recommendations, not a schema the packs enforce). The foundation lockstep set and built-in move together; `internal` gets its own minor bump and tightens its writing range to the release that ships the new styleguide.
- The new styleguide id is `ai-writing-tells`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `research-citation-discipline` holds 2 new principles (FR-001, FR-002), and 3 authoring surfaces (specify prompt, plan prompt, ADR tactic) point to it. — [build] · no-op passable: no
- **SC-002**: `adversarial-squad-deployment` holds the 3 new rules (FR-005 x2, FR-006), each once. — [build] · no-op passable: no
- **SC-003**: 1 shared styleguide holds the 7 tells; `report-writing` restates 0 of them and references it; it is reachable from 1 mission type, 2 actions and 1 agent profile. — [build] · no-op passable: no
- **SC-004**: 0 writing or internal surfaces recommend the path form (NFR-004). — [build] · no-op passable: no
- **SC-005**: All gates in NFR-001 green at the PR head. — [evidenced-by-run] · no-op passable: n/a -- evidence: the CI run on the PR head
