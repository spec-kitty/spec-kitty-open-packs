---
title: planning-analysis pack reference
description: "Generated reference for the planning-analysis Charter Pack: artifact inventory, per-kind counts, and content checksum."
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

# planning-analysis pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/planning-analysis`
- **Pack level:** `built-in`
- **Declared version:** `3.7.0`
- **Content checksum (sha256):** `ae60ef2cf20a3244e5a268f64f936a063bcb3e14138c95740cd0cd69a4cfb1d4`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Planning, research and brownfield analysis: the planner and researcher profiles, the retrospective facilitator, situational assessment, legacy triage, spikes and the planning templates.

**Depends on:** [`architecture`](architecture.md) `==3.7.0`, [`foundation`](foundation.md) `==3.7.0`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `tactics` | 2 |
| `styleguides` | 1 |
| `paradigms` | 1 |
| `procedures` | 5 |
| `anti_patterns` | 19 |
| `agent_profiles` | 3 |
| `drg` | 1 |
| **Total files** | **35** |

### Full listing

<details>
<summary><code>tactics</code> (2)</summary>

- `analysis/analysis-extract-before-interpret.tactic.yaml`
- `analysis/vertical-skeleton-first.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (1)</summary>

- `planning-and-tracking.styleguide.yaml`

</details>

<details>
<summary><code>paradigms</code> (1)</summary>

- `brownfield-onboarding.paradigm.yaml`

</details>

<details>
<summary><code>procedures</code> (5)</summary>

- `domain-aware-decision-interview.procedure.yaml`
- `issue-triage-state-machine.procedure.yaml`
- `legacy-codebase-triage.procedure.yaml`
- `situational-assessment.procedure.yaml`
- `spike-timebox-policy.procedure.yaml`

</details>

<details>
<summary><code>anti_patterns</code> (19)</summary>

- `batch-questioning.anti-pattern.yaml`
- `blocking-on-the-optional-steps.anti-pattern.yaml`
- `budgetless-spike.anti-pattern.yaml`
- `child-ticket-checklist-in-the-epic-body.anti-pattern.yaml`
- `closing-a-community-duplicate-before-migrating-its-evidence.anti-pattern.yaml`
- `implementation-coupled-briefs.anti-pattern.yaml`
- `memory-only-rejection.anti-pattern.yaml`
- `meta-tracker-as-canonical-parent.anti-pattern.yaml`
- `multiple-active-state-labels.anti-pattern.yaml`
- `over-interviewing.anti-pattern.yaml`
- `over-reading-squash-merged-history.anti-pattern.yaml`
- `premature-decision-records.anti-pattern.yaml`
- `rationalised-outcome.anti-pattern.yaml`
- `skipping-the-exclusion-list.anti-pattern.yaml`
- `substituting-triage-for-deeper-investigation.anti-pattern.yaml`
- `terminology-policing.anti-pattern.yaml`
- `treating-triage-as-a-verdict.anti-pattern.yaml`
- `unwritten-finding.anti-pattern.yaml`
- `vague-needs-info-questions.anti-pattern.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (3)</summary>

- `planner-priti.agent.yaml`
- `researcher-robbie.agent.yaml`
- `retrospective-facilitator.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>
