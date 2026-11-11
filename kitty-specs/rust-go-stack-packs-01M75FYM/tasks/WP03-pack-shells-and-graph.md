---
work_package_id: WP03
title: Pack shells, provenance and local graph
dependencies:
- WP01
- WP02
requirement_refs:
- FR-001
- FR-005
- FR-010
- FR-013
- NFR-003
- C-002
- C-004
planning_base_branch: feat/rust-go-packs
merge_target_branch: feat/rust-go-packs
branch_strategy: Planning artifacts for this mission were generated on feat/rust-go-packs. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/rust-go-packs unless the human explicitly redirects the landing branch.
subtasks:
- T011
- T012
- T013
- T014
- T015
history:
- at: '2026-11-11T15:00:00Z'
  actor: system
  action: Prompt generated via /spec-kitty.tasks
agent_profile: implementer-ivan
authoritative_surface: packs/
create_intent:
- packs/rust/pack.yaml
- packs/rust/pack.md
- packs/rust/README.md
- packs/rust/PROVENANCE.md
- packs/rust/org-charter.yaml
- packs/rust/drg/fragment.yaml
- packs/go/pack.yaml
- packs/go/pack.md
- packs/go/README.md
- packs/go/PROVENANCE.md
- packs/go/org-charter.yaml
- packs/go/drg/fragment.yaml
execution_mode: code_change
owned_files:
- packs/rust/pack.yaml
- packs/rust/pack.md
- packs/rust/README.md
- packs/rust/PROVENANCE.md
- packs/rust/org-charter.yaml
- packs/rust/drg/fragment.yaml
- packs/go/pack.yaml
- packs/go/pack.md
- packs/go/README.md
- packs/go/PROVENANCE.md
- packs/go/org-charter.yaml
- packs/go/drg/fragment.yaml
role: implementer
tags: []
tracker_refs: []
---

# Work Package Prompt: WP03 – Pack shells, provenance and local graph

## ⚡ Do This First: Load Agent Profile

Before reading anything else, load the assigned profile with the `/spk-charter-profile-load` skill:
`implementer-ivan`. If the skill is not available, run `spec-kitty agent profile show implementer-ivan`.

## Objective

Turn `packs/rust` and `packs/go` into valid, composable org packs: descriptor, documents, provenance
and a DRG fragment of local nodes and edges. `built-in` stays untouched (FR-010, C-002).

## Branch Strategy

Planning/base and merge target `feat/rust-go-packs`. Implement with
`spec-kitty agent action implement WP03 --agent claude --mission rust-go-stack-packs-01M75FYM`.

## Subtasks

### T011 — Mint pack_ids and write `pack.yaml`

Mint each id **once**, with the ULID library shipped in the spec-kitty install:

```bash
/root/.local/share/uv/tools/spec-kitty-cli/bin/python -c 'from ulid import ULID; print(ULID())'
```

Record the command and output in the commit message body. Never hand-type an id.

```yaml
# Authored pack descriptor for the opt-in Rust (org-tier) Charter Pack.
schema_version: "1.0"
pack_id: <minted>
pack_version: 1.0.0
parent_pack: null
name: rust
pack_level: org
active_charter: org-charter.yaml
pack_drg: drg/fragment.yaml
```

No `depends_on` yet. WP05 adds `foundation`. Is `pack_level` with no `depends_on` valid? The `spdd`
pack and the pack-descriptor schema show that it is. The same applies to `go`.

### T012 — `pack.md`, `README.md`, `org-charter.yaml`

- `pack.md`: an H1 and a preamble only. The preamble is the pack's description, and the generator
  shows it under "Purpose". Follow `packs/spdd/pack.md`.
- `README.md`: what the pack holds; **Adopt** (register it under `charter_packs.org.packs` with its
  `foundation` dependency, then activate the preset); what it deliberately does not cover (framework
  specifics such as tokio / axum or gin / echo); a pointer to `PROVENANCE.md`.
- `org-charter.yaml`: `schema_version: 2`, `org_name: spec-kitty-rust` / `spec-kitty-go`, and a
  comment saying it activates nothing on its own.

### T013 — `PROVENANCE.md` (FR-013)

Follow `packs/cave-kitty/PROVENANCE.md` (an authored-fresh pack). State:

- the seed: spec-kitty/charter-cobol-migrations at `2c4ce2a`, `charter-packs/<lang>/README.md`;
- that this pack is new authoring under MIT and that no seed text was copied;
- what was taken: target-language idioms only;
- what was not: migration doctrine, characterization and parity tactics, and anything COBOL;
- a table of **seed contradictions and resolutions** (research R-02, the rows for this language);
- the other sources consulted (the Rust API Guidelines, Clippy docs, Effective Go, Go Code Review
  Comments), cited as references, not copied.

### T014 — `drg/fragment.yaml`

Follow `packs/spdd/drg/fragment.yaml`. Nodes (`id`, `kind` plural, `title`, `body_path`):

- the styleguide (`kind: styleguides`);
- the toolguide (`kind: toolguides`);
- the profile (`kind: agent_profiles`).

Local edges, with singular URN kinds:

```yaml
- source: agent_profile:rust-ruben
  target: styleguide:rust-conventions
  relation: requires
  reason: A language-specialist profile requires the conventions styleguide of each of its applies_to_languages (#131; charter #405 ruling).
- source: agent_profile:rust-ruben
  target: toolguide:rust-review-checks
  relation: suggests
  reason: ...
- source: styleguide:rust-conventions
  target: toolguide:rust-review-checks
  relation: suggests
```

Add `when` where it helps routing. The same applies to `go`.

### T015 — Gates

```bash
export CHARTER_CONTRACT_DIR=/home/user/spec-kitty/spec-kitty-charter/contracts/packs
scripts/ci/validate-packs.sh          # must list packs/rust and packs/go ok, cross-pack 0 violations
scripts/ci/check-built-in.sh          # unchanged
python3 scripts/ci/check_vocabulary.py
git diff --stat origin/main -- packs/built-in packs/built-in.source.yaml   # must be empty
```

## Definition of Done

- [ ] Both packs validate with 0 violations, and the cross-pack check is clean.
- [ ] The pack_ids were minted by the tool, with the output recorded in the commit body.
- [ ] `built-in` is byte-identical to `origin/main`.
