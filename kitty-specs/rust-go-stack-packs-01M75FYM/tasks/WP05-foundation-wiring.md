---
work_package_id: WP05
title: Wire the foundation dependency
dependencies:
- WP04
requirement_refs:
- FR-009
- C-003
- NFR-003
planning_base_branch: feat/rust-go-packs
merge_target_branch: feat/rust-go-packs
branch_strategy: Planning artifacts for this mission were generated on feat/rust-go-packs. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/rust-go-packs unless the human explicitly redirects the landing branch.
subtasks:
- T020
- T021
- T022
history:
- at: '2026-11-11T15:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: kitty-specs/rust-go-stack-packs-01M75FYM/research/
create_intent:
- kitty-specs/rust-go-stack-packs-01M75FYM/research/foundation-wiring.md
execution_mode: planning_artifact
owned_files:
- kitty-specs/rust-go-stack-packs-01M75FYM/research/foundation-wiring.md
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP05 – Wire the `foundation` dependency

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill:
`implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Declare each pack's dependency on #73's `foundation` pack and add the qualified cross-pack edges
(FR-009). **Blocked** until `foundation` exists with a pack_id: on `main`, or on
`feat/73-foundation-writing-split`, relayed by the orchestrator.

The deliverable files are edits to files WP03 and WP04 created: both `pack.yaml`, both
`drg/fragment.yaml` and both generated pages. WP05 runs strictly after them, so these are sequenced
out-of-map edits with this rationale: the dependency is external, and splitting ownership of one
descriptor across two WPs would be worse. `research/foundation-wiring.md` records the evidence.

## Subtasks

### T020 — `depends_on`

```yaml
depends_on:
  - pack_id: <foundation pack_id, copied from foundation's pack.yaml — never typed from memory>
    range: ">=1.0,<2"
```

### T021 — Qualified edges

Only to artifacts the **landed** `foundation` holds. Grep its `pack.yaml`, graph and files first.
Proposed set (research R-06, data-model.md):

- profile → `foundation::agent_profile:implementer-ivan` : `specializes_from`;
- profile → `foundation::directive:DIRECTIVE_010`, `_024`, `_025`, `_030`, `_034` : `requires`
  (`_041` : `suggests`);
- profile → `foundation::tactic:tdd-red-green-refactor`, `foundation::tactic:dependency-hygiene`,
  `foundation::tactic:supply-chain-install-safety` : `requires`;
- styleguide → `foundation::directive:DIRECTIVE_030`, `_034` : `suggests`.

Each edge carries a `reason`. Drop or re-target any edge whose target `foundation` does not hold,
and record that in `research/foundation-wiring.md`.

### T022 — Regenerate and gate

Regenerate `docs/packs/{rust,go}.md`, then run every gate in `quickstart.md`. The cross-pack check
must accept the qualified edges inside the `depends_on` closure. `foundation` must be present under
`packs/` for the local run: rebase onto it once it is on `main`, or check it out read-only from its
branch for the local check only.

## Definition of Done

- [ ] Both packs `depends_on` foundation; every `foundation::` edge resolves.
- [ ] All gates are green; the generated pages show the dependency.
- [ ] `research/foundation-wiring.md` lists the pack_id source commit, each edge, and any dropped edge.
