---
title: testing pack reference
description: "Generated reference for the testing Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
doc_status: active
updated: '2026-11-09'
kind: Reference
related:
- packs
- architecture/docsite-design
- packs/catalog-proposal
generated:
  by: scripts/docs/gen_pack_reference.py
  at: '2026-11-09'
---

# testing pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/testing`
- **Declared version:** `2.0.0`
- **Content checksum (sha256):** `0d7932d66a25cb3321351384fdcb6f2a38ba65903a5ee9739d0912840a955e80`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Test design and test-first practice beyond the foundation basics: BDD and specification by example, test minimisation and reconstruction, mutation testing, Gherkin, and the debugging profile.

A built-in-level core bundle, carved out of `built-in` by #73 and aggregated by it since 3.0.0 (ADR 2026-11-11-1, amendment 2026-11-11). It builds on `foundation`.

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 ==1.0.0`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 1 |
| `tactics` | 9 |
| `styleguides` | 5 |
| `toolguides` | 2 |
| `paradigms` | 2 |
| `procedures` | 5 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| **Total files** | **31** |

### Full listing

<details>
<summary><code>directives</code> (1)</summary>

- `use-mutation-testing-to-validate-test-quality.directive.yaml`

</details>

<details>
<summary><code>tactics</code> (9)</summary>

- `testing/atdd-adversarial-acceptance.tactic.yaml`
- `testing/bdd-scenario-formulation.tactic.yaml`
- `testing/formalized-constraint-testing.tactic.yaml`
- `testing/mutation-testing-workflow.tactic.yaml`
- `testing/no-parallel-duplicate-test-runs.tactic.yaml`
- `testing/test-minimisation.tactic.yaml`
- `testing/test-pyramid-progression.tactic.yaml`
- `testing/test-to-system-reconstruction.tactic.yaml`
- `testing/zombies-tdd.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (5)</summary>

- `given-when-then-authoring.styleguide.yaml`
- `mutation-aware-test-design.styleguide.yaml`
- `quadruple-a-test-format.styleguide.yaml`
- `test-desiderata-and-boundaries.styleguide.yaml`
- `testing-principles.styleguide.yaml`

</details>

<details>
<summary><code>toolguides</code> (2)</summary>

- `gherkin.guide.md`
- `gherkin.toolguide.yaml`

</details>

<details>
<summary><code>paradigms</code> (2)</summary>

- `behaviour-driven-development.paradigm.yaml`
- `specification-by-example.paradigm.yaml`

</details>

<details>
<summary><code>procedures</code> (5)</summary>

- `bdd-scenario-lifecycle.procedure.yaml`
- `development-assist-test-cleanup.procedure.yaml`
- `disciplined-defect-diagnosis.procedure.yaml`
- `mutation-testing-review.procedure.yaml`
- `test-first-bug-fixing.procedure.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (1)</summary>

- `debugger-debbie.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
