---
title: internal pack reference
description: "Generated reference for the internal Charter Pack: artifact inventory, per-kind counts, and content checksum."
doc_status: active
updated: '2026-11-12'
kind: Reference
related:
- packs
- architecture/docsite-design
- packs/catalog-proposal
generated:
  by: scripts/docs/gen_pack_reference.py
  at: '2026-11-12'
---

# internal pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/internal`
- **Pack level:** `org`
- **Declared version:** `4.5.0`
- **Content checksum (sha256):** `d3af7a610c5739eb8559fea9ef6163281dd0b785eca88a5431652c6637c1471d`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

This is Spec Kitty's own **internal** Charter Pack: the doctrine that governs
*contributors, maintainers, and the core team* of the Spec Kitty project itself.
It is loaded as an **org-tier** pack (registered in `.kittify/config.yaml` under
`charter_packs.org.packs`), overlaying the public `packs/built-in/` product doctrine. It is never shipped to consumers:
maintainer-only doctrine must not be force-shipped on the wheel.

**Depends on:** [`foundation`](foundation.md) `>=3.7,<4`, [`planning-analysis`](planning-analysis.md) `>=2.0,<4`, [`refactoring`](refactoring.md) `>=2.0,<4`, [`testing`](testing.md) `>=3.6,<4`, [`writing`](writing.md) `>=3.4,<4`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 6 |
| `tactics` | 6 |
| `styleguides` | 7 |
| `toolguides` | 6 |
| `procedures` | 19 |
| `anti_patterns` | 57 |
| `assets` | 22 |
| `glossaries` | 1 |
| `drg` | 1 |
| `presets` | 1 |
| `skills` | 10 |
| **Total files** | **139** |

### Full listing

<details>
<summary><code>directives</code> (6)</summary>

- `cloud-session-orchestration.directive.yaml`
- `no-full-heavy-suites-in-mission.directive.yaml`
- `operator-signal-contract.directive.yaml`
- `spec-kitty-build-identity.directive.yaml`
- `spec-kitty-docs-conventions.directive.yaml`
- `spec-kitty-red-main-policy.directive.yaml`

</details>

<details>
<summary><code>tactics</code> (6)</summary>

- `branded-deliverable.tactic.yaml`
- `spec-kitty-ci-workflow-evidence-exemplar.tactic.yaml`
- `spec-kitty-gate-non-vacuity-exemplar.tactic.yaml`
- `spec-kitty-mock-boundary-exemplar.tactic.yaml`
- `spec-kitty-ratchet-cost.tactic.yaml`
- `tracker-backlog-iterative-deepening.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (7)</summary>

- `executive-debrief.styleguide.yaml`
- `feature-and-scenario-authoring.styleguide.yaml`
- `report-writing.styleguide.yaml`
- `spec-kitty-docs-lint-config.styleguide.yaml`
- `spec-kitty-package-tiers.styleguide.yaml`
- `spec-kitty-tracker-labels.styleguide.yaml`
- `tiered-standards.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (6)</summary>

- `branded-document-generation.guide.md`
- `branded-document-generation.toolguide.yaml`
- `terminology-guard.guide.md`
- `terminology-guard.toolguide.yaml`
- `test-quality-triage.guide.md`
- `test-quality-triage.toolguide.yaml`

</details>

<details>
<summary><code>procedures</code> (19)</summary>

- `charter-offering-scenario-extraction.procedure.yaml`
- `cloud-session-dispatch.procedure.yaml`
- `executive-debrief-generation.procedure.yaml`
- `issue-to-mission-delivery.procedure.yaml`
- `issue-triage-pass.procedure.yaml`
- `landing-contributor-prs.procedure.yaml`
- `memory-curation-and-escalation.procedure.yaml`
- `mission-tracer-files.procedure.yaml`
- `mission-wrap-up-sequence.procedure.yaml`
- `operator-signal-emission.procedure.yaml`
- `project-evolution-postmortem.procedure.yaml`
- `semi-auto-delivery.procedure.yaml`
- `spec-kitty-arch-gate-adjudication.procedure.yaml`
- `spec-kitty-common-docs-layout.procedure.yaml`
- `spec-kitty-page-audience.procedure.yaml`
- `spec-kitty-red-main-triage.procedure.yaml`
- `targeted-mission-test-run.procedure.yaml`
- `test-suite-quality-assessment.procedure.yaml`
- `tracker-organisation-workflow.procedure.yaml`

</details>

<details>
<summary><code>anti_patterns</code> (57)</summary>

- `a-report-with-no-ask.anti-pattern.yaml`
- `agent-merges-the-mainline.anti-pattern.yaml`
- `arming-auto-merge-before-the-fix-is-complete.anti-pattern.yaml`
- `catch-all-root.anti-pattern.yaml`
- `claiming-unread-progress.anti-pattern.yaml`
- `command-named-steps.anti-pattern.yaml`
- `crud-affordance-echo.anti-pattern.yaml`
- `dark-chrome-or-a-white-print-margin.anti-pattern.yaml`
- `deciding-silently.anti-pattern.yaml`
- `decision-drip.anti-pattern.yaml`
- `defect-framing.anti-pattern.yaml`
- `deferring-instead-of-finishing.anti-pattern.yaml`
- `dispatching-from-a-title.anti-pattern.yaml`
- `environment-improvisation.anti-pattern.yaml`
- `flipping-a-red-or-still-changing-pr-to-ready-for-review.anti-pattern.yaml`
- `forking-a-near-duplicate-epic.anti-pattern.yaml`
- `full-auto-drift.anti-pattern.yaml`
- `gating-instead-of-discipline.anti-pattern.yaml`
- `greening-by-erasure.anti-pattern.yaml`
- `grounding-prompt-without-discovery.anti-pattern.yaml`
- `hand-built-chrome.anti-pattern.yaml`
- `hand-counted-or-invented-figures.anti-pattern.yaml`
- `hiding-pre-existing-debt-in-new-work.anti-pattern.yaml`
- `importing-core-logic-from-scripting-packages.anti-pattern.yaml`
- `judging-liveness-against-a-stale-origin.anti-pattern.yaml`
- `keyword-only-triage.anti-pattern.yaml`
- `landing-a-draft-pr-without-asking.anti-pattern.yaml`
- `merge-commits-instead-of-a-linear-history.anti-pattern.yaml`
- `one-pr-for-unrelated-domains.anti-pattern.yaml`
- `over-broad-uncheckable-scenarios.anti-pattern.yaml`
- `over-length-entries.anti-pattern.yaml`
- `per-wp-green-treated-as-the-final-gate.anti-pattern.yaml`
- `placeholder-prompts.anti-pattern.yaml`
- `pointfix-without-discovery.anti-pattern.yaml`
- `reading-the-corpus-in-commit-order.anti-pattern.yaml`
- `recapturing-a-ci-owned-file-during-a-landing.anti-pattern.yaml`
- `restating-report-writing-here.anti-pattern.yaml`
- `retroactive-fill-in.anti-pattern.yaml`
- `rewriting-history-to-make-every-commit-green.anti-pattern.yaml`
- `running-the-heavy-suites-in-mission.anti-pattern.yaml`
- `running-the-suite-to-find-weak-tests.anti-pattern.yaml`
- `scope-creep-into-activation.anti-pattern.yaml`
- `setting-priority-p0-silently.anti-pattern.yaml`
- `skipping-the-assess-step.anti-pattern.yaml`
- `specifying-before-grounding.anti-pattern.yaml`
- `specifying-before-the-claim.anti-pattern.yaml`
- `starting-from-a-stale-or-wrong-remote.anti-pattern.yaml`
- `technical-first-burial.anti-pattern.yaml`
- `tests-for-the-sake-of-tests.anti-pattern.yaml`
- `touching-workflow-state-leases.anti-pattern.yaml`
- `transcribing-the-e2e-mechanism.anti-pattern.yaml`
- `treating-a-static-flag-as-a-verdict.anti-pattern.yaml`
- `unbounded-or-colliding-dispatch.anti-pattern.yaml`
- `uniform-standards-across-all-packages.anti-pattern.yaml`
- `unresolved-issue-verdicts-at-close.anti-pattern.yaml`
- `work-stranded-under-a-closed-epic.anti-pattern.yaml`
- `writing-to-an-issue-that-closed-mid-pass.anti-pattern.yaml`

</details>

<details>
<summary><code>assets</code> (22)</summary>

- `audiences/agentic-framework-core-team.md`
- `audiences/agentic-framework-core-team.md.asset.yaml`
- `debrief/collect-debrief.py`
- `debrief/collect-debrief.py.asset.yaml`
- `debrief/debrief-template.html`
- `debrief/debrief-template.html.asset.yaml`
- `debrief/fonts/FallingSky-Bold.otf`
- `debrief/fonts/FallingSky-Bold.otf.asset.yaml`
- `debrief/fonts/FallingSky-Extrabold.otf`
- `debrief/fonts/FallingSky-Extrabold.otf.asset.yaml`
- `debrief/fonts/FallingSky-Regular.otf`
- `debrief/fonts/FallingSky-Regular.otf.asset.yaml`
- `debrief/logo.png`
- `debrief/logo.png.asset.yaml`
- `debrief/render-debrief.py`
- `debrief/render-debrief.py.asset.yaml`
- `spec-kitty-branded-pdf.py`
- `spec-kitty-branded-pdf.py.asset.yaml`
- `test-quality-scan.py`
- `test-quality-scan.py.asset.yaml`
- `validate-pr-body.py`
- `validate-pr-body.py.asset.yaml`

</details>

<details>
<summary><code>glossaries</code> (1)</summary>

- `spk-internal-glossary.glossary.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

<details>
<summary><code>presets</code> (1)</summary>

- `base.yaml`

</details>

<details>
<summary><code>skills</code> (10)</summary>

- `issue-triage.skill.md`
- `issue-triage.skill.yaml`
- `land-pr.skill.md`
- `land-pr.skill.yaml`
- `mission-from-issue.skill.md`
- `mission-from-issue.skill.yaml`
- `report-debrief.skill.md`
- `report-debrief.skill.yaml`
- `semi-auto.skill.md`
- `semi-auto.skill.yaml`

</details>
