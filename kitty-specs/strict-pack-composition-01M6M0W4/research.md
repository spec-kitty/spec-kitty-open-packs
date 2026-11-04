# Research: strict pack composition (epic #118, 2026-11-04)

Pre-spec research and grounding squad (procedure `adversarial-squad-deployment`), measured at
open-packs `f85cf23` (tag `pre-charter-cutover`) and charter `origin/main` `85c20fa1`.
Cast (profile-loaded): researcher-robbie, architect-alphonso, planner-priti.

## Verdict
One mission, plus a companion charter PR. Issues in: #47, #75, #113, #116, #117. Slice: A (all five
blocking issues) sequenced with C's proving case inside it (`qa` is the tracer).

## What was executed, not inferred
Robbie compiled charter `origin/main` with `/usr/lib/jvm/temurin-25` (it exists, it is just not on
PATH) and ran the production `DomainRepositoryService` and `OfferingReadService` over real pack
directories (a throwaway probe, `RealComposeProbeTest.java`, kept with the operator's gitignored debrief under `.kittify/derived/debriefs/epic-118/evidence/`). With only #75, `pack.yaml` for 3 packs, 93
qualified references and `depends_on` on 3 packs:
`OFFERING OK: built-in(337) cave-kitty(3) event-driven(14) internal(44) qa(52)`.
13 mutants refused as expected (`probe-out2.txt`, same place). Limits: no HTTP controller, a stubbed
digest for `ConsistentRead`, levels set by the harness, scratch copies with fake ULIDs.

## Measured
| Pack | Epic sites/targets | Measured | Where | `pack.yaml` |
|---|---|---|---|---|
| internal | 73/29 | **78/31** | 57 edges, 19 procedure refs, 2 tactic refs | present |
| event-driven | 12/6 | 12/6 | 7 edges, 2 directive, 2 paradigm, 1 tactic | missing |
| qa | 3/3 | 3/3 | 3 edges | missing |
| cave-kitty | 0/0 | 0/0 | none | missing |

Total 93 sites, 67 graph edges. The dependency graph is a star: every org pack points at `built-in`.
No org-to-org edges, no sibling conflicts, no bare self-references.

## Divergences, adjudicated
- **internal count.** priti 73, robbie and alphonso 78. Adjudicated 78: the gap is 5
  `agent_profile:` edges (`planner-priti` x4, `reviewer-renata` x1), and leaving them bare is refused
  `pack_reference_unqualified` in an executed mutant (m1).
- **Pack names.** priti `spec-kitty-qa`, alphonso `qa`. Operator ruling: `quality-assurance`,
  `event-driven`, `cave-kitty`; the `packs/qa` directory is not renamed.
- **JDK.** alphonso and the brief said no JDK; robbie found one and used it. Corrected.

## Findings and disposition
| # | Sev | Finding | Disposition |
|---|---|---|---|
| R1 | BLOCKER | `validate_pack_schemas.py:782-783` splits on the first `:`, so 67 correct qualified edges fail. No issue tracks it | accepted: foundation WP |
| R2 | BLOCKER | #113, #116 and charter `docs/guides/compose-packs.md` prescribe `built-in::<kind>:<id>` for typed refs; the schema refuses it. Edges use that form, typed refs use `built-in::<id>` | accepted: spec states both; charter docs fix goes in the companion PR |
| R3 | HIGH | Pin `3c9f640a` predates #365 and rejects `::` and `depends_on`. Bump is safe on as-is content | accepted: foundation WP, before any qualifier |
| R4 | HIGH | No gate here catches a missing `pack.yaml`, bare cross-pack refs, reachability or sidecar payloads | accepted: thin qualifier-aware check; the charter stays authoritative |
| R5 | HIGH | Charter bump is atomic: `openPacksRef`, lock, `OpenPacksCorpus.DIAGNOSTICS`, inspector test, `known-failures.yaml`, compose test | accepted: companion PR |
| R6 | HIGH | #363 scope is `internal + built-in` and reads "synced" packs; `SUBTREES` holds only `internal` and `qa` | accepted: test reads the corpus checkout, all packs |
| R7 | HIGH | After merge, core's `load_org_pack` rejects `depends_on`, and `.kittify/config.yaml` registers `packs/internal` and `packs/qa` by local path. This repo's own governance stops merging them, quietly: `charter context` and `status` still report success | accepted by the operator: breakage accepted; land `internal` late, try `dispatch` and `next` early, pause if the mission's own runtime breaks |
| R8 | MAJOR | `gen_pack_reference.py:186` mis-parses `depends_on` and publishes wrong text with no gate failure | accepted: foundation WP |
| R9 | MED | #75 omits manifest restamp, `tree_digest`, generated page; core's `_anchor_for` breaks at its next pin bump | accepted (one atomic WP); core issue filed as follow-up |
| R10 | MED | `qa` agent profiles hold 24 built-in refs the service does not check | operator ruling: check and corroborate during the mission, log an issue if too much scope |
| R11 | MED | #72's target layout matches a retired, refused path | deferred_with_rationale: rewrite #72 outside this mission; note on the issue |
| R12 | MED | Stale issue text: #47 (internal `pack_level`), #113 (13 refs), #363 (13), #365 body (qa complies) | accepted: correct at close-out |
| R13 | LOW | `check-built-in.sh`, `built_in_digest.py` "re-seed" wording | accepted: reword with #75 |
| R14 | LOW | `validate-a-pack.md:74` says the pin is on an open branch; `compose-packs.md` says no pack carries `depends_on` | accepted: docs at close-out |
| R15 | LOW | cave-kitty prompts bind built-in profiles in prose | accepted: declare `depends_on` even with 0 refs |
| O1 | - | #93, #114, #72, #73 cause no refusal (executed) | deferred_with_rationale: out of scope; #73 redo is mechanical and fails loudly |
| O2 | - | #92, #94 go to the runner; overlap on built-in digest and `semi-auto-delivery` | second to land regenerates |

## Order and atomicity
Foundation (pin bump, qualifier parsing, generator fix) -> #47 and #75 -> `qa` tracer with a real
compose -> `event-driven` and `internal` -> guard refuses bare cross-pack refs, docs, changelog ->
charter PR re-pointed at the final open-packs `main` SHA.

Must land together: pin bump with qualifier parsing; #75's sidecars, manifest, digest and page; one
pack's `depends_on`, qualifiers and page; everything in the charter bump.

## Rerun the compose probe
Copy that `RealComposeProbeTest.java` into `service/packs/src/test/java/ai/speckitty/charter/packs/infra/storage/`
in a charter worktree, set `PROBE_SCENARIOS` and `PROBE_OUT`, then:
```
JAVA_HOME=/usr/lib/jvm/temurin-25 GRADLE_USER_HOME=<scratch> GRADLE_RO_DEP_CACHE=~/.gradle/caches \
  ~/.gradle/wrapper/dists/gradle-9.8.1-bin/*/gradle-9.8.1/bin/gradle --offline --no-daemon \
  -Dorg.gradle.java.installations.paths=/usr/lib/jvm/temurin-25 \
  :packs:test --tests '*RealComposeProbeTest' -x spotlessCheck
```
