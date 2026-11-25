---
title: testing pack reference
description: "Generated reference for the testing Charter Pack: artifact inventory, per-kind counts, and content checksum."
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

# testing pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/testing`
- **Pack level:** `built-in`
- **Declared version:** `3.7.0`
- **Content checksum (sha256):** `299262294bd92252060adc2e35c72f83fa2593a22f9d020a38847d6974191a7d`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Test design and test-first practice beyond the foundation basics: BDD and specification by example, test minimisation and reconstruction, mutation testing, Gherkin, and the debugging profile.

**Depends on:** [`foundation`](foundation.md) `==3.7.0`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 1 |
| `tactics` | 10 |
| `styleguides` | 5 |
| `toolguides` | 2 |
| `paradigms` | 2 |
| `procedures` | 5 |
| `anti_patterns` | 32 |
| `agent_profiles` | 1 |
| `assets` | 4 |
| `drg` | 1 |
| **Total files** | **66** |

### Full listing

<details>
<summary><code>directives</code> (1)</summary>

- `use-mutation-testing-to-validate-test-quality.directive.yaml`

</details>

<details>
<summary><code>tactics</code> (10)</summary>

- `testing/atdd-adversarial-acceptance.tactic.yaml`
- `testing/bdd-scenario-formulation.tactic.yaml`
- `testing/formalized-constraint-testing.tactic.yaml`
- `testing/mutation-testing-workflow.tactic.yaml`
- `testing/no-parallel-duplicate-test-runs.tactic.yaml`
- `testing/shared-machine-test-measurement.tactic.yaml`
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
<summary><code>anti_patterns</code> (32)</summary>

- `delete-a-mega-file-wholesale.anti-pattern.yaml`
- `exception-only-assertion.anti-pattern.yaml`
- `fabricated-unrealistic-test-data.anti-pattern.yaml`
- `fixing-without-a-feedback-loop.anti-pattern.yaml`
- `forgetting-that-a-stub-is-a-second-copy-of-the-contract.anti-pattern.yaml`
- `full-application-restart.anti-pattern.yaml`
- `gold-plating-as-a-licence-to-double-owned-logic.anti-pattern.yaml`
- `identity-value-inputs.anti-pattern.yaml`
- `imperative-gherkin.anti-pattern.yaml`
- `infrastructure-as-untyped-shared-mutable-state.anti-pattern.yaml`
- `keep-the-wp-nfr-label-on-a-promoted-test.anti-pattern.yaml`
- `leaving-debug-artifacts-behind.anti-pattern.yaml`
- `logging-everything.anti-pattern.yaml`
- `merge-the-scaffolding-clean-it-up-later.anti-pattern.yaml`
- `missing-assumption-check.anti-pattern.yaml`
- `multiple-whens-in-one-scenario.anti-pattern.yaml`
- `orphaned-step-definitions.anti-pattern.yaml`
- `over-mocking-to-compensate-for-a-missing-boundary.anti-pattern.yaml`
- `refactoring-beyond-the-fix.anti-pattern.yaml`
- `retire-coverage-disguised-as-a-duplicate.anti-pattern.yaml`
- `rubber-stamp-scenarios.anti-pattern.yaml`
- `self-constructed-oracle-an-injection-proof-that-never-injects.anti-pattern.yaml`
- `shared-mutable-state-between-scenarios.anti-pattern.yaml`
- `side-script-investigation.anti-pattern.yaml`
- `single-branch-condition.anti-pattern.yaml`
- `single-hypothesis-anchoring.anti-pattern.yaml`
- `stubbing-a-new-gate-out-of-an-old-harness.anti-pattern.yaml`
- `substring-case-insensitive-message-assertion.anti-pattern.yaml`
- `sweep-the-whole-suite-in-the-landing-pr.anti-pattern.yaml`
- `test-passes-immediately.anti-pattern.yaml`
- `the-literal-scan-trap.anti-pattern.yaml`
- `wrong-failure-reproduction.anti-pattern.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (1)</summary>

- `debugger-debbie.agent.yaml`

</details>

<details>
<summary><code>assets</code> (4)</summary>

- `quad-a-test-structure.md`
- `quad-a-test-structure.md.asset.yaml`
- `test-desiderata-checklist.md`
- `test-desiderata-checklist.md.asset.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>
