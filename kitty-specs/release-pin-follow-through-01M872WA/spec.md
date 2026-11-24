# Mission Specification: Release-pin follow-through

**Mission Branch**: `kitty/mission-release-pin-follow-through-01M872WA` (lands on `ci/release-pin-follow-through`, then a PR to `main`)
**Created**: 2026-11-24
**Status**: Draft
**Input**: Dispatcher brief "Mission A: release-pin follow-through", a child of epic #287. Its gate is clear: #329 and #336 have merged.

## Intent Summary (confirmed: operator rulings, no re-interview)

The brief gives the operator's rulings and tells the runner not to re-interview, so discovery was skipped on that instruction. Each fact below comes from the brief or was re-checked on `main` at `a7243e2`.

- **Primary actor:** a pack maintainer whose pull request runs the open-packs gate, and the charter release track that proposes each new charter release as a bump pull request. The operator reviews and merges that bump PR.
- **Trigger:** a PR to `main`, and the daily release track.
- **Outcome:** the release-pin work of epic #287 is finished:
  - the stray-file gap is pinned and documented as the operator accepted it;
  - the derived-manifest mirror matches the charter's walk and wording;
  - the bump job no longer holds a write token beside the content re-derivation;
  - the bump PR says whether the release's jars carry a verified build attestation.
- **Rule that always holds:** open-packs never overrides the charter's own verdict (no option 2 on #331), and a missing or unverified attestation never blocks the bump (warn only).
- **Re-checked state:** the lock already pins the release `service-v0.1.0-rc.3`, so the manual first release pin is done. From rc.4 on, the track proposes each release.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A stray file's fate is pinned and stated (Priority: P1)

A maintainer keeps a note in a pack. A Markdown note (`notes.md`) passes with a warning. Any other stray file (`notes.txt`, a log) still fails through pack-check's round trip, as the operator accepted. The guide and changelog say so and name the charter fix (spec-kitty-charter#631).

**Why this priority**: #331 is the head of the brief's order, and its docs still say "until #331's decision lands".

**Independent Test**: a gate test feeds the pack-check report of an unmodelled stray file and asserts the gate fails it, with no downgrade.

**Acceptance Scenarios**:

1. **Given** a pack-check report in which the same file is both `file_not_held` and `round_trip_red`, **When** the gate judges it, **Then** the gate fails and names the round-trip failure.
2. **Given** a stray `notes.md`, **When** the gate runs, **Then** it passes with a `file_not_held` warning. This is already landed in #336 and is kept.

### User Story 2 - The manifest mirror matches the charter (Priority: P1)

A maintainer derives or checks a pack manifest. The Python mirror lists exactly the files the charter's walk lists. A file reached through a linked directory is never listed. The mismatch reasons read as the charter writes them.

**Independent Test**: a fixture pack with a symlinked directory holding an artifact file; a derive-then-check run whose manifest bytes must change.

**Acceptance Scenarios**:

1. **Given** a pack holding a symlinked directory that contains a tactic file, **When** the manifest is derived, **Then** that tactic is not listed.
2. **Given** a manifest that lists the same unheld entry twice, **When** membership is judged, **Then** two reasons are given, "does not hold" and "twice", in the charter's order.
3. **Given** a pack whose manifest is stale, **When** `--derive-manifest` runs, **Then** the manifest's bytes change and the following check passes.

### User Story 3 - The release bump is hardened (Priority: P2)

The release track proposes a new charter release. The step that re-derives the packs from the release's contract content holds no token. Before the PR is opened, the service jar and the pack-check jar are each checked for a build attestation. When either has none, or it does not verify, the bump PR is still opened and its body says so.

**Independent Test**: workflow-structure tests in `tests/ci/test_workflows.py` assert that no step running `charter_pin.py apply` or `changelog` has a token in its environment, and that the attestation outcome reaches the PR body. A unit test covers the PR-body wording for each outcome.

**Acceptance Scenarios**:

1. **Given** the bump job, **When** its steps are inspected, **Then** the step that runs `charter_pin.py apply` and `changelog` has no `GH_TOKEN`, `GITHUB_TOKEN` or secret in its environment.
2. **Given** a release whose jars have no attestation, **When** the bump runs, **Then** a warning is annotated, the PR is opened, and the body names each jar that was not verified.
3. **Given** a release whose jars both verify, **When** the bump runs, **Then** the body states that both attestations verified.

### User Story 4 - Self-binding vocabulary is precise (Priority: P3)

A doctrine author writes ordinary prose ("The rule is mandatory reading for reviewers", "advisory context menu"). The vocabulary check does not flag it, but it still catches the simple variants #304 lists.

**Independent Test**: one test case per false positive and per false negative listed in #304.

### Edge Cases

- A pack directory that is itself reached through a link is still walked, as the charter enters a root configured through a link (#174).
- The attestation tool fails for a reason other than a missing attestation, such as the network or the API. That is treated as "not verified" (a warning), never as a failure of the bump.
- A pack's symlinked file is already skipped today, and that is kept.

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status | Delivery | No-op passable? |
|----|-------|------------|----------|--------|----------|-----------------|
| FR-001 | Unmodelled stray file still fails | As a maintainer, I want the gate to keep failing a stray `notes.txt` via pack-check's round trip, with no open-packs override, so that the accepted gap (#331 ruling, option 3) is pinned until spec-kitty-charter#631. | High | Open | [ratchet] | yes — paired with the `notes.md` warning case on the same judge fixture |
| FR-002 | Docs state the accepted gap | As a reader, I want the guide, the changelog and `charter_pack_check.py` to state the ruling and cite spec-kitty-charter#631 instead of "until #331's decision lands", so that the docs match shipped behaviour. | High | Open | [build] | no |
| FR-003 | Linked directories are not walked | As a maintainer, I want `derived_manifest` to skip every file under a symlinked directory, on every supported Python, so that the mirror matches the charter's walk. | High | Open | [build] | no |
| FR-004 | Duplicate-and-unheld wording pinned | As a maintainer, I want a test pinning that a listed-twice, unheld entry yields both charter reasons in charter order, so that the port cannot drift from `ManifestRules.mismatch`. | Medium | Open | [ratchet] | yes — a mutation dropping either reason must fail it |
| FR-005 | Derive test proves a write | As a maintainer, I want the derive-then-check test to assert that the manifest bytes changed, so that a no-op derive cannot pass. | Medium | Open | [build] | no |
| FR-006 | No token beside the re-derivation | As the operator, I want the bump job split so that the step running `charter_pin.py apply`, `changelog` and `commit-payload` has no token, and only the push and PR steps hold one, so that the release's contract content is parsed with no credential in reach (#310 item 2). | High | Open | [build] | no |
| FR-007 | Attestation check, warn only | As the operator, I want the bump job to verify the build attestation of the service jar and the pack-check jar, to warn on a missing or failed verification, and to open the PR anyway, so that provenance is visible without blocking (#310 item 1). | High | Open | [build] | no |
| FR-008 | PR body states attestation outcome | As the reviewer of a bump PR, I want its body to say, for each jar, whether its attestation verified, so that I know what stands behind the digests. | High | Open | [build] | no |
| FR-009 | Self-binding patterns anchored | As a doctrine author, I want the #304 false positives to pass and its false negatives to be flagged, with one test case each, so that the lint is precise. | Medium | Open | [build] | no |
| FR-010 | Roadmap and epic state current | As a reader, I want the roadmap's "Charter pin" **Waits on** to reflect that rc.3 ships the tension spelling, the #554 ruling and ADR-0080, so that the plan matches reality. | Low | Open | [build] | no |
| FR-011 | Changelog entry | As a consumer, I want one changelog entry covering this mission's user-facing changes. | Medium | Open | [build] | no |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Gates stay green | `tests/ci` passes in full, along with `validate-packs.sh` (+ `--cross-pack`), `check_vocabulary.py` and `gen_pack_reference.py --check`: 0 failures. | Reliability | High | Open |
| NFR-002 | Token exposure | 0 steps in `charter-track.yml` run repository Python with a token or secret in their `env`, other than the read-only resolve step's public-release lookup, which is unchanged. | Security | High | Open |
| NFR-003 | Bump cost | The attestation check adds at most 2 jar downloads and 2 verification calls per bump run. | Performance | Low | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | No override | Open-packs never downgrades pack-check's `round_trip_red` (operator ruling on #331). | Business | High | Open |
| C-002 | Charter is the reference | The mirror follows the charter at the pinned commit `cb9b154` (`ManifestRules.mismatch`, the `PackFileSet` walk). Core compatibility is not a concern. | Technical | High | Open |
| C-003 | Warn only | A missing or unverified attestation never fails the bump job (operator ruling on #310). | Business | High | Open |
| C-004 | No #315 build | #315 is out of scope here. Its sources and cadence are open questions to the dispatcher. | Business | Medium | Open |
| C-005 | Hygiene | Topic branches only, signed commits, no model names in artifacts. | Business | High | Open |

### Key Entities

- **Lock** (`charter.lock.yaml`): commit, `release_tag` and the two jar digests.
- **Bump job**: the `charter-track.yml` job that turns a green release into one PR.
- **Derived manifest**: the constituent and preset lists the charter derives for a pack.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 4 #304 false positives yield 0 findings, and all 5 false negatives yield 1 finding each. — [build] · no-op passable: no
- **SC-002**: A fixture with a symlinked directory derives 0 constituents from inside it, on Python 3.12 and 3.13. — [build] · no-op passable: no
- **SC-003**: The bump job has 0 steps that both hold a token and run `charter_pin.py apply`. — [build] · no-op passable: no
- **SC-004**: Every bump PR body carries an attestation line for each of the 2 jars. — [build] · no-op passable: no

## Assumptions

- The charter does not yet publish build attestations for its release jars. The warn-only path is therefore the expected outcome for rc.4 until it does.
- `gh attestation verify` is available on GitHub-hosted runners.
- Closing #252, rewriting #287's "State and order" and the #315 follow-on are tracker actions done at hand-off, not part of the code change.
