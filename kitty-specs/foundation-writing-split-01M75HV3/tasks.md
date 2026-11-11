# Tasks: Split built-in into foundation, writing and opt-in bundles

**Branch**: `feat/73-foundation-writing-split` | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

All work runs sequentially on one lane:
- WP01 produces the tree the other packages edit.
- WP02 and WP03 both need WP01.
- WP03's charter service run needs WP02's org-pack rewiring.
- WP04 documents the final state.

**Next required step**: `/spec-kitty.analyze`, then implementation.

## Subtask Index

| ID | Description | WP | Parallel |
|----|-------------|----|----------|
| T001 | Write foundation, writing and the ten bundle descriptors, pack.md, README, PROVENANCE, org-charter | WP01 | |
| T002 | Write the migration tool: node→file map, non-node file map, fail on unmapped files | WP01 | |
| T003 | `git mv` every file to its pack (including the 10 qa/internal items) | WP01 | |
| T004 | Split the 14 graph fragments by owner; relocate upward edges with qualified sources | WP01 | |
| T005 | Strip out-of-closure body references (profiles, step contracts); qualify cross-pack in-closure ones as needed | WP01 | |
| T006 | Rewrite built-in as the distribution pack (2.0.0, depends_on, presets, policy, fallback); Generic Giannis | WP01 | |
| T007 | Write member lists for the built-in, foundation and writing manifests and restamp them; validate-packs green for the three packs | WP01 | |
| T008 | Rewrite every `built-in::` reference in internal, qa, event-driven, spdd (and any in cave-kitty) | WP02 | |
| T009 | Set each org pack's `depends_on` to the packs it references; bump pack_version | WP02 | |
| T010 | Integrate the received qa/internal items into their packs (fragment nodes, README lists, PROVENANCE) | WP02 | |
| T011 | Validate the org packs (validate-packs, profile reference check) | WP02 | |
| T012 | charter_service_check.py: stage every built-in-level pack; compose and register all packs | WP03 | |
| T013 | #182 manifest-completeness guard in validate_pack_schemas.py with unit tests | WP03 | |
| T014 | Re-record the built-in digest; fix check_vocabulary.py and the tests that hard-code built-in paths | WP03 | |
| T015 | Run every gate on the head; the charter service check green with Java 25 | WP03 | |
| T016 | ADR 2026-11-11-1 and a 💥 Breaking CHANGELOG entry with migration notes | WP04 | |
| T017 | README, packs/README, docs/packs index/catalog, guides naming built-in paths | WP04 | |
| T018 | Generate pack reference pages for the new packs; regenerate built-in's page; nav | WP04 | |

## WP01 — Pack migration (Priority P1)

**Goal**: three new packs and an empty distribution `built-in`, built from [membership.json](membership.json) by a deterministic tool.
**Independent test**: `validate-packs.sh` passes for built-in, foundation, writing and the ten bundles. `packs/built-in` holds only pack.yaml, pack.md, policy.yaml, presets/ and pack-manifest.yaml.
**Prompt**: [tasks/WP01-pack-migration.md](tasks/WP01-pack-migration.md)

T001 Write the new descriptors, pack.md, README, PROVENANCE and org-charter (WP01)
T002 Write the migration tool (WP01)
T003 git mv every file (WP01)
T004 Split the graphs and relocate edges (WP01)
T005 Body-reference surgery (WP01)
T006 Rewrite built-in as the distribution pack; Generic Giannis (WP01)
T007 Manifests; validate (WP01)

Dependencies: none. Risk: unmapped files. The tool must refuse rather than guess.

## WP02 — Rewire the org packs (Priority P1)

**Goal**: internal, qa, event-driven, cave-kitty and spdd compose against the new packs.
**Independent test**: no `built-in::` remains in `packs/`; validate-packs is green.
**Prompt**: [tasks/WP02-rewire-org-packs.md](tasks/WP02-rewire-org-packs.md)

T008 Rewrite the references (WP02)
T009 depends_on and versions (WP02)
T010 Integrate the received items (WP02)
T011 Validate (WP02)

Dependencies: WP01.

## WP03 — Gates and the #182 guard (Priority P1)

**Goal**: every gate understands three built-in-level packs; the manifest guard lands.
**Independent test**: all gates are green on the head, including the charter service check.
**Prompt**: [tasks/WP03-gates-and-guard.md](tasks/WP03-gates-and-guard.md)

T012 Charter service check: stage every built-in-level pack (WP03)
T013 #182 guard with tests (WP03)
T014 Digest, vocabulary and test fixes (WP03)
T015 Run every gate (WP03)

Dependencies: WP01, WP02.

## WP04 — Documentation (Priority P2)

**Goal**: readers and consumers learn what moved and how to migrate.
**Independent test**: `gen_pack_reference.py --check` is green; the CHANGELOG has the 💥 entry; the ADR is indexed.
**Prompt**: [tasks/WP04-documentation.md](tasks/WP04-documentation.md)

T016 ADR and CHANGELOG (WP04)
T017 READMEs, catalog and guides (WP04)
T018 Generated pages and nav (WP04)

Dependencies: WP01, WP02, WP03.
