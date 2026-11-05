---
affected_files: []
cycle_number: 1
mission_slug: strict-pack-composition-01M6M0W4
reproduction_command:
reviewed_at: '2026-11-04T21:11:38Z'
reviewer_agent: claude
wp_id: WP01
---

# WP01 review, cycle 1: changes requested

**Verdict: reject, for one defect.** The gate's idea of "held" is not the charter's, so it disagrees with the service in both directions on real `built-in` targets. Everything else is sound; see "What held up". Do not widen the fix.

Evidence came from running the charter's production `DomainRepositoryService` and `OfferingReadService` at `85c20fa1` (the research `RealComposeProbeTest`) on the same fixtures as the gate.

## BLOCKING: `composition_violations` judges "held" from `declared_nodes`

`scripts/ci/validate_pack_schemas.py:860` passes `declared_nodes(...)` as `held`, and lines 835 and 839 judge references against it. `declared_nodes` answers "what is declared", which includes every graph or fragment node. The charter answers differently (`DomainRepositoryService.compositionFacts`, `PackCompositionResolver.holds`): a pack holds its artifact files, of every kind that may appear in graphs, plus `anti_pattern` graph nodes. A node without a file is held by nobody.

`declared_nodes` also misses files the charter counts: agent profiles (their key is `profile-id`, not `id`), mission types (absent from `ARTIFACT_SCHEMAS`, line 697) and templates (payload files, identified by path).

Measured on real packs, charter against gate:
- 37 `built-in` ids are held for the gate only: 16 `template:*` nodes such as `template:agent-brief-template`, and 21 `mission_step_contract:*` nodes such as `documentation/accept`.
- 29 templates are held for the charter only: 19 in `built-in`, 10 in `qa`.

| Scenario (consumer pack, `depends_on` built-in) | Gate | Charter |
|---|---|---|
| edge `built-in::template:agent-brief-template` (real) | pass | `PACK_REFERENCE_ARTIFACT_MISSING` |
| edge `built-in::mission_step_contract:documentation/accept` (real) | pass | `PACK_REFERENCE_ARTIFACT_MISSING` |
| edge `template:agent-brief-template`, bare (real) | fail, "qualify it" | accepted |
| edge `built-in::template:writing/meeting-minutes.md` (real file) | fail | accepted |
| root `*.graph.yaml` edge `template:writing/meeting-minutes.md`, bare (real file) | pass | `PACK_REFERENCE_UNQUALIFIED` |
| typed or root-graph bare reference to a profile that has a file and no node | pass | `PACK_REFERENCE_UNQUALIFIED` |
| `directive_refs: [NODE_DIR]`, bare, node only | fail | accepted |

Why this matters:
- **FR-003**: a qualified target the named pack does not hold must fail. It passes for those 37 real ids.
- **FR-002**: a correct qualified reference must pass. `built-in::template:writing/meeting-minutes.md` fails.
- **Spec edge case and `data-model.md`**: a bare reference no pack holds is not refused. It is refused for node-only ids.
- **User Story 2**: rows 1 and 3 chain together. A bare reference the service accepts fails here, the message says to qualify it, the qualified form passes here, and the service then refuses it. `built-in` itself uses those 16 template ids bare (39 sites; corrected 2026-11-05 at close-out: 41, re-counted with `written_references`), so they look safe to copy.

Nothing in the 93 migration sites hits this today, so the migration is not at risk. The risk is every reference written after it.

**Fix.** Add one small helper for what a pack holds, and leave `declared_nodes` alone as T002 says:
1. artifact files of the existing schemas plus `mission-type`, with the id from `id` or `profile-id`;
2. templates by path: `templates/<p>` gives `<p>`, and `missions/<m>/templates/<p>` gives `<m>/<p>`;
3. `anti_pattern` nodes from both graph document shapes.

Pass that to `composition_violations`. Let the older edge check at line 894 also accept a held artifact, or a correct qualified reference to a file-only target still fails there.

I tried this in a scratch copy only, in about 24 lines, which keeps the validator's added lines near 144 of the 150 allowed. Results:
- all the table rows agree with the charter;
- `validate-packs.sh` stays green;
- as-is packs with the allowances off give exactly 93 bare-reference findings (internal 78, event-driven 12, qa 3) plus the 3 missing descriptors;
- research-migrated packs with the allowances off give 0 violations.

**Test to change.** `test_the_bare_id_lists_are_read_under_the_kind_their_field_means` (`tests/ci/test_validate_pack_schemas.py:466`) asserts that a bare `directive_refs: [D_1]`, where `D_1` is node-only in the `built_in()` fixture (line 374), is refused. The charter accepts that, so the test pins the disagreement, and it is the only test that goes red under the fix. It is new in this WP, so changing it is not an "existing assertion" change: make `D_1` a directive file. Add tests for a node-only target (qualified fails, bare passes) and for a file-only profile, mission type and template (qualified passes, bare fails), each with a positive control on the same fixture.

## Non-blocking: fix these in the same round if cheap

1. `tests/ci/test_validate_pack_schemas.py:527`: `test_a_pending_pack_may_keep_...` patches both allowance constants, so deleting `PENDING_DESCRIPTORS` (WP02 T008) raises `AttributeError` in it (confirmed), and deleting `PENDING_PACKS` (WP07 T024) will do the same. Neither prompt mentions this test and neither WP owns the file. Split it in two, so each later WP deletes one test whole with no change to any assertion, and note that in the hand-off.
2. Two surviving mutants. Removing the pack itself from `_depends_on_closure` is not caught, so add a self-qualified reference (`consumer::tactic:own`), which the charter accepts. Dropping `guard` and `lifecycle` from `UNHELD_KINDS` is not caught either; test them or cut the constant to what is tested.
3. `docs/packs/index.md:60` still says the generator does not fabricate a purpose "when a pack's `pack.yaml` omits one", which implies the field exists. That is what FR-012 removes. `docs/architecture/docsite-design.md:44,50` says the same. Reword them or hand them to WP07 by name.
4. `docs/guides/validate-a-pack.md:69` says a pack with no `pack.yaml` fails, but does not mention `PENDING_DESCRIPTORS`, which exempts qa, event-driven, cave-kitty and the example pack until WP02.
5. The allowances are keyed on directory base name, and nothing fails when an entry goes stale, so "only shrinks" rests on the WPs. A stale entry keeps skipping silently until WP02 and WP07 delete the constants. Accepted, because both deletions are planned.
6. `_depends_on_closure` (line 797) silently ignores a `depends_on` naming an unknown `pack_id`. The charter refuses it with `PACK_DEPENDENCY_UNKNOWN`. FR-003 does not list this, so it is a choice, but a typo there passes when the pack writes no qualified reference.
7. A self-loop written with a self-qualifier (`consumer::tactic:own` to `tactic:own`) passes here and is `PACK_UNREADABLE` at the charter. Also outside FR-003; recorded only.
8. `tests/docs` runs in no workflow, so the new generator tests do not run in CI. This gap predates the WP. Worth a line in the hand-off.
9. `read_pack_descriptor` now raises a raw `yaml` parser error on a malformed `pack.yaml`. Failing loud is right; the traceback is merely unfriendly.

## What held up

- Gates, re-run on the lane: `tests/ci` 50 OK, `tests/docs` OK, `tests/release` 8 OK, `tests/vocabulary` 12 OK, `validate-packs.sh` green (0 violations), `check-built-in.sh` green, generator `--check` no drift.
- Pin: `85c20fa1` is the tip of charter `main` and contains `88ed36e4`.
- Thin: 120 added validator lines, with no ordering, level, range or sibling logic.
- NFR-001: about 1.2 s added (5.57 s to 6.73 s).
- References read: all the charter's fields, both forms, steps, id lists and root graphs agreed with the charter, as did transitive `depends_on`, descriptors and duplicates.
- Tests: 18 of 20 mutants were killed. No existing assertion changed; only a descriptor was added to one fixture helper.
- Generator: `depends_on` publishes every entry, and pyyaml is installed before the generator runs in both workflows.
- Allowances: removing both over research-migrated packs gives 0 gate violations, and the charter composes all five.

## Anti-pattern checklist

1. Dead code: PASS.
2. Synthetic fixture: PASS.
3. Silent empty return: PASS (the non-dict `pack.yaml` case is left to the schema check).
4. FR coverage: **FAIL** for FR-002 and FR-003 as above; the behaviour is tested, but against the wrong definition of held.
5. Frozen surface: PASS (no pack content touched).
6. Locked decision: **FAIL**, "a bare reference no pack holds is not refused".
7. Shared-file ownership: PASS. Coordination note: `validate_pack_schemas.py` and `docs/packs/*` are also edited by later WPs, and WP02 and WP03 should rebase on the fix.
8. Production fragility: PASS (no new `raise`).
