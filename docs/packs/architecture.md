---
title: architecture pack reference
description: "Generated reference for the architecture Charter Pack: artifact inventory, per-kind counts, and content checksum."
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

# architecture pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/architecture`
- **Pack level:** `built-in`
- **Declared version:** `2.0.0`
- **Content checksum (sha256):** `ce181ab96b26c620508e6d354ded09f3416ec2ca678bd98aef5b03cd9bac9a84`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

Domain-driven design and C4 architecture modelling: the DDD and C4 paradigms, bounded-context and aggregate tactics, architecture templates and anti-patterns, and the Architect Alphonso and Paula Patterns profiles.

**Depends on:** [`foundation`](foundation.md) `==1.0.0`, [`refactoring`](refactoring.md) `==2.0.0`, [`writing`](writing.md) `==1.0.0`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 1 |
| `tactics` | 14 |
| `styleguides` | 1 |
| `paradigms` | 3 |
| `procedures` | 3 |
| `agent_profiles` | 2 |
| `drg` | 1 |
| **Total files** | **28** |

### Full listing

<details>
<summary><code>directives</code> (1)</summary>

- `use-c4-model-techniques.directive.yaml`

</details>

<details>
<summary><code>tactics</code> (14)</summary>

- `analysis/ammerse-impact-analysis.tactic.yaml`
- `analysis/bounded-context-canvas-fill.tactic.yaml`
- `analysis/connascence-analysis.tactic.yaml`
- `analysis/context-mapping-classification.tactic.yaml`
- `analysis/entity-value-object-classification.tactic.yaml`
- `analysis/strategic-domain-classification.tactic.yaml`
- `architecture/aggregate-boundary-design.tactic.yaml`
- `architecture/anti-corruption-layer.tactic.yaml`
- `architecture/architecture-diagram-review-checklist.tactic.yaml`
- `architecture/c4-zoom-in-architecture-documentation.tactic.yaml`
- `architecture/development-bdd.tactic.yaml`
- `architecture/domain-event-capture.tactic.yaml`
- `architecture/paula-patterns-architecture-scout-review.tactic.yaml`
- `architecture/reference-architectural-patterns.tactic.yaml`

</details>

<details>
<summary><code>styleguides</code> (1)</summary>

- `aggregate-design-rules.styleguide.yaml`

</details>

<details>
<summary><code>paradigms</code> (3)</summary>

- `c4-incremental-detail-modeling.paradigm.yaml`
- `deep-module-design.paradigm.yaml`
- `domain-driven-design.paradigm.yaml`

</details>

<details>
<summary><code>procedures</code> (3)</summary>

- `c4-diagram-authoring.procedure.yaml`
- `drill-down-documentation.procedure.yaml`
- `event-storming-discovery.procedure.yaml`

</details>

<details>
<summary><code>agent_profiles</code> (2)</summary>

- `architect-alphonso.agent.yaml`
- `paula-patterns.agent.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>
