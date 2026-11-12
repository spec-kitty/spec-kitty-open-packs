---
title: refactoring pack reference
description: "Generated reference for the refactoring Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# refactoring pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/refactoring`
- **Declared version:** `2.0.0`
- **Content checksum (sha256):** `ec8da4a7a7c68df8d83379607ed523500e93e0330dd7064eb81b4dcc99eb8af4`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

The refactoring catalogue (Fowler-style moves, strangler fig, state and strategy patterns), semantic compression, the code-smell anti-patterns and the Randy Reducer profile.

- **Contents:** 25 tactics, 7 anti patterns, 1 agent profile, 1 paradigm, 1 procedure.
- **Agent profiles:** `randy-reducer`.

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 ==1.0.0`, `01M75PCTC6HS38NX8HJGT26VTP ==2.0.0`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `tactics` | 25 |
| `paradigms` | 1 |
| `procedures` | 1 |
| `agent_profiles` | 1 |
| `drg` | 1 |
| **Total files** | **32** |

### Full listing

<details>
<summary><code>tactics</code> (25)</summary>

- `code-patterns/chain-of-responsibility-rule-pipeline.tactic.yaml`
- `refactoring/refactoring-change-function-declaration.tactic.yaml`
- `refactoring/refactoring-combine-functions-into-transform.tactic.yaml`
- `refactoring/refactoring-conditional-to-strategy.tactic.yaml`
- `refactoring/refactoring-consolidate-conditional-expression.tactic.yaml`
- `refactoring/refactoring-encapsulate-record.tactic.yaml`
- `refactoring/refactoring-encapsulate-variable.tactic.yaml`
- `refactoring/refactoring-extract-class-by-responsibility-split.tactic.yaml`
- `refactoring/refactoring-extract-first-order-concept.tactic.yaml`
- `refactoring/refactoring-guard-clauses-before-polymorphism.tactic.yaml`
- `refactoring/refactoring-inline-temp.tactic.yaml`
- `refactoring/refactoring-introduce-null-object.tactic.yaml`
- `refactoring/refactoring-move-field.tactic.yaml`
- `refactoring/refactoring-move-method.tactic.yaml`
- `refactoring/refactoring-replace-magic-number-with-symbolic-constant.tactic.yaml`
- `refactoring/refactoring-replace-temp-with-query.tactic.yaml`
- `refactoring/refactoring-retry-pattern.tactic.yaml`
- `refactoring/refactoring-state-pattern-for-behavior.tactic.yaml`
- `refactoring/refactoring-strangler-fig.tactic.yaml`
- `semantic-compression/semantic-compression-abstraction-extraction.tactic.yaml`
- `semantic-compression/semantic-compression-behavioral-boundary-mapping.tactic.yaml`
- `semantic-compression/semantic-compression-dead-weight-elimination.tactic.yaml`
- `semantic-compression/semantic-compression-equivalence-verification.tactic.yaml`
- `semantic-compression/semantic-compression-redundancy-discovery.tactic.yaml`
- `semantic-compression/semantic-compression-semantic-consolidation.tactic.yaml`

</details>

<details>
<summary><code>paradigms</code> (1)</summary>

- `semantic-compression.paradigm.yaml`

</details>

<details>
<summary><code>procedures</code> (1)</summary>

- `refactoring.procedure.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (1)</summary>

- `randy-reducer.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
