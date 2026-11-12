---
title: cave-kitty pack reference
description: "Generated reference for the cave-kitty Charter Pack: artifact inventory, per-kind counts, content checksum, and validation status."
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

# cave-kitty pack reference

> **Generated page — do not edit by hand.** This file is produced by `scripts/docs/gen_pack_reference.py` from the pack source. Hand edits are overwritten on regeneration, and the CI drift gate fails on any difference.

## Provenance & integrity

- **Pack directory:** `packs/cave-kitty`
- **Declared version:** `2.0.0`
- **Content checksum (sha256):** `bb3e60efd1e4470181c7c3d13cf21bdc353fc1537ba94cf30d7148a15ada2993`
- **Checksum recipe:** sha256 over the sorted `(relative-path + NUL + bytes + LF)` of every file in the pack directory. Re-hash a downloaded pack with the same recipe to verify integrity.

## Purpose

An open Spec Kitty Charter Pack that makes an agent answer in a **compressed, token-saving
"caveman" voice** — outcome-first, filler cut — while keeping every payload and every negation
exact and restoring full sentences at a cliff edge.

> **Scope note.** The styleguide and directive are complete and usable today, and are the clean
> instrument for the pack's purpose (see "Which path for a token A/B?" below). The `cave-dev`
> mission type **re-states the built-in `software-dev` step contract as prose** and overrides one
> thing only — the agent's output prose, which it compresses to the caveman voice. Its eight
> step prompts follow the same structured shape the canonical `qa` open pack uses (role +
> software-dev mapping, bound built-in profile, directive & styleguide citation, artifact/template
> binding, and the per-step voice specialization). cave-dev deliberately ships no templates and no
> personas of its own: the voice applies to prose, not to document structure, and not to the
> engineering rigour, which is `software-dev`'s.
>
> **Runtime caveat.** "Re-states the contract" is a documentation relationship, not a runtime one.
> Under `spec-kitty next`, the per-WP iteration and the step guards the loop runs for
> `implement`/`review`, and the analysis-currency gate ahead of `implement`, are keyed to the
> built-in `software-dev` family in the CLI and do **not** fire for a `cave-dev`-typed mission —
> its `implement`/`review` steps advance as generic single-shot DAG steps. The lane/worktree
> execution path (`spec-kitty implement WP##`) is unaffected. For a WP-iterating, guarded run in
> the caveman voice, use the voice-activation path (`--type software-dev` + activate the voice).

**Depends on:** `01M75HSYR9S9KPA372PHGT0EX3 >=1.0,<2`

## Artifact inventory

| Kind | Count |
| --- | --- |
| `directives` | 1 |
| `styleguides` | 1 |
| `drg` | 1 |
| `missions` | 9 |
| **Total files** | **14** |

### Full listing

<details>
<summary><code>directives</code> (1)</summary>

- `cave-001-terse-output.directive.yaml`

</details>

<details>
<summary><code>styleguides</code> (1)</summary>

- `cave-sty-001-communication.styleguide.yaml`

</details>

<details>
<summary><code>drg</code> (1)</summary>

- `fragment.yaml`

</details>

<details>
<summary><code>missions</code> (9)</summary>

- `cave-dev/cave-dev.mission-type.yaml`
- `cave-dev/steps/accept.prompt.md`
- `cave-dev/steps/analyze.prompt.md`
- `cave-dev/steps/discovery.prompt.md`
- `cave-dev/steps/implement.prompt.md`
- `cave-dev/steps/plan.prompt.md`
- `cave-dev/steps/review.prompt.md`
- `cave-dev/steps/specify.prompt.md`
- `cave-dev/steps/tasks.prompt.md`

</details>

## Validation

Reported by the charter pack schemas (`scripts/ci/validate_pack_schemas.py`): **passing**.

- Errors: 0
