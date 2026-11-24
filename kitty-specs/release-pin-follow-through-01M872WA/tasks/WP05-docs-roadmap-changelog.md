---
work_package_id: WP05
title: Docs, roadmap and changelog
dependencies:
- WP01
- WP02
- WP03
- WP04
requirement_refs:
- FR-002
- FR-010
- FR-011
- NFR-001
planning_base_branch: ci/release-pin-follow-through
merge_target_branch: ci/release-pin-follow-through
branch_strategy: Planning artifacts for this mission were generated on ci/release-pin-follow-through. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into ci/release-pin-follow-through unless the human explicitly redirects the landing branch.
subtasks:
- T019
- T020
- T021
- T022
history:
- at: '2026-11-24T16:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: scribe-sally
authoritative_surface: docs/guides/validate-a-pack.md
create_intent: []
execution_mode: code_change
model: ''
owned_files:
- docs/guides/validate-a-pack.md
- docs/plans/roadmap.md
- CHANGELOG.md
- docs/changelog/CHANGELOG.md
role: implementer
tags: []
tracker_refs:
- '#331'
- '#310'
- '#287'
---
# Work Package Prompt: WP05 – Docs, roadmap and changelog

## ⚡ Do This First: Load Agent Profile

Load the assigned profile with `/spk-charter-profile-load scribe-sally` before reading anything else.

## Objective

Make the authored docs match what WP01–WP04 shipped (FR-002, FR-010, FR-011). Follow the charter's docs rules:
- DIRECTIVE_037: in sync with shipped behaviour;
- DIRECTIVE_044: generated facts are never restated;
- DIRECTIVE_047: write for the audience.

Use short sentences with the facts first. Generated pages (`docs/packs/`) are never hand-edited.

Read the merged diffs of WP01–WP04 before writing.

## Branch Strategy

The planning branch and merge target is `ci/release-pin-follow-through`. This WP depends on WP01–WP04, so its lane bases on their merged work. Implement with `spec-kitty agent action implement WP05 --agent <name> --mission release-pin-follow-through-01M872WA`.

## Subtasks

### T019 — Guide: stray files

`docs/guides/validate-a-pack.md`, the paragraph headed **Stray files (R34, #331)** (≈l.272–275). Replace "so it fails the gate until #331's decision lands" with the ruling:
- the operator accepted the gap (2026-11-21), and open-packs does not override pack-check's verdict;
- only ignored-kind files (Markdown notes) may stay in a pack;
- any other stray file fails through `round_trip_red` until spec-kitty-charter#631 makes the round trip skip unheld files.

Also check the table row at ≈l.92 for consistency.

### T020 — Guide: the release bump

In the same guide, the bump/`PR_CREATION_TOKEN` section (≈l.390–405):
- **Token split:** the job token pushes the branch from steps that run only `gh`; the step that re-derives the packs from the new release's contract runs with no token (#310).
- **Attestation:** a read-only job verifies the build attestation of the service jar and the pack-check jar. It warns only (operator ruling); the bump PR is opened anyway, and its body says, per jar, verified / not verified / not checked. A reviewer of a bump PR whose jars are not verified compares both digests with the release assets by hand.

### T021 — Roadmap

`docs/plans/roadmap.md`, Charter pin section, **Waits on** (≈l.74–77). `service-v0.1.0-rc.3` ships:
- the `tension` spelling;
- the `file_not_held` ruling (charter #554);
- the routing catalog (charter ADR-0080).

The packs are pinned to it. Rewrite **Waits on** to what is still outstanding: the charter fixes #629, #630 and #631, so that the remaining Python rules (#330) can retire and stray files can stay. Re-check the section's other sentences against the lock (`charter.lock.yaml`) and remove the stale claim that the nightly main check stays red until a release, if it is no longer true. Check the latest `charter:main-red` issue state with the GitHub tools if you can; otherwise say so in the hand-off.

### T022 — Changelog

Add one entry under `## [Unreleased]` in `CHANGELOG.md`, in the matching subsection (🔒 Security / ✨ Added / 🔧 Changed / 🐛 Fixed; follow the file's existing headings). Copy it byte-for-byte into `docs/changelog/CHANGELOG.md`; the two files are identical today. Cover:
- the accepted stray-file gap (#331);
- the manifest mirror no longer following linked directories (#262);
- the bump job's token split and the warn-only attestation check (#310);
- the precise self-binding lint (#304).

Bump the `updated:` front-matter date to the day of the change.

## Definition of Done

- `diff CHANGELOG.md docs/changelog/CHANGELOG.md` is empty.
- `python3 -m unittest discover -s tests/docs` passes, and the docs freshness and link checks the repo wires pass.
- No generated page was edited.

## Reviewer guidance

Check every claim against the merged code, especially the bump-step names and the attestation states.
