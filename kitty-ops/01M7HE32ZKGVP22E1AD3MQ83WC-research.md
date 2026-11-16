# Grounding: the pin move to charter `main` (epic #287)

Op `01M7HE32ZKGVP22E1AD3MQ83WC` (planner-priti). Base: open-packs `beca19c` (#289, slice A of #285, stacked;
`main` is `c0ec640`). Old pin `eacbc3c`; new pin **`050d780876c6e9bd4265c7ec3335abe1b95cda61`**, charter `main`
HEAD on 2026-11-16 (214 commits, linear history).

## What the new pin holds

| Charter change | Charter ref | What it asks of open-packs | Here |
|---|---|---|---|
| Glossary contexts replace `glossary_pack` | #106 (PR #577), ADR-0049, ADR-0053 d11-14, ADR-0076 | migrate four glossaries | #283 |
| Kind taxonomy, step contracts folded into substeps, endpoint table | #537 (PR #567), ADR-0077 | fold 28 contracts; validator, docs | #285 items 1, 5 (items 2-4 are #289) |
| Round trip moves into `pack-validation` | #555 (PR #578), ADR-0075 d8 | `:pack-validation:driftTest` | #284 |
| `performer` replaces `sentinel`; profile selection; role pins | #538 (PR #573), ADR-0078 | `human-in-charge` reshaped | #139 |
| `specializes_from` is acyclic | ADR-0078 d2 | validator check | #286 |
| Every identifier on the shared slug grammar; tactic id letter-first | #552 | none found (below) | n/a |

`#580` is not on charter `main` at `050d780`.

## What the new pin refuses in the old content

`scripts/ci/validate-packs.sh` at `050d780` (contract from the charter checkout via `CHARTER_CONTRACT_DIR`) on
`beca19c`: 5 packs fail with 114 violations plus 1 cross-pack violation:

- `foundation` 61: `sentinel` on `human-in-charge`; the `glossary_pack` shard and file; the 14 step-contract files
  (`retired layout`); 28 schema errors on the `mission_step_contract.graph.yaml` nodes; 15 manifest constituents
  of retired kinds.
- `writing` 29: 7 step-contract files, 14 shard errors, 7 manifest constituents, the
  `foundation::glossary_pack:spec-kitty-core` edge target.
- `qa` 17, `internal` 4 (incl. `activated_glossary_packs`), `event-driven` 3: glossary-pack files, fragment kinds,
  manifest constituents; qa's 7 step contracts.
- cross-pack: `internal`'s must-have glossary is held by no pack once the file is refused.

The charter round trip at `050d780` over the base tree: BASE_DRIFT_RESULT

`:packs:driftTest` does not exist at `050d780` (Gradle: "task 'driftTest' not found in project ':packs'"), so the
current CI script cannot run at the new pin without #284.

#552 (slug grammar): with the four migrations applied, the schema pass and the round trip report nothing for
it; no open-packs id breaks the new grammar.

## Decisions taken here

- **Glossary ids kept** (`spec-kitty-core`, `qa-glossary`, `evd-glossary`, `spk-internal-glossary`), each equal to
  its new file stem: renaming would change every `term:` address and the preset entry for no gain. P7 (#47) is
  settled by keeping `spk-internal-glossary` for both.
- **Term ids:** all minted by the rule (lower-case, runs of `[^a-z0-9]` to `-`, trim); 0 hand-picked, 0 collisions
  (138 + 19 + 13 + 12). The `step contract` term goes with its kind, as charter #537 removed it.
- **`see_also`:** 7 references kept (internal), 3 dropped: the tactic and requirement entries on `catastrophic
  backtracking` (as the charter's example dropped them) and `release readiness` on `red main` (no such term in any
  pack).
- **Fold:** the charter's `apply-drafts.py --drafts 1` on a scratch copy; counts equal the draft (149 substeps,
  144 candidates, 34 qualified, 115 renames, 30 files). Drafts 2 and 3 report 0 to add (#289 holds them).
- **Versions** (DIRECTIVE_018, ADR-0048 d17): see the changelog. Major where an artifact is removed or renamed;
  minor where only role references, ranges or prose change.
- **Not changed:** `.kittify/charter/charter.yaml` (`selected_glossary_packs`, `selected_mission_step_contracts`)
  is core's generated project file and follows core (ADR-0077, Risks). Historical ADR lines and kitty-specs keep
  their wording; ADR 2026-11-11-1 gets a dated amendment.

## Similar surfaces

- Retired-file precedence: the validator classified `files` before `retired`, so a leftover
  `mission_step_contract.graph.yaml` read as a graph shard (14-28 schema errors) where the charter refuses it by
  name. Fixed with the classifier-cases rule 1 and a test.
- Node kind vs artifact kind: `glossary` (artifact, manifest, preset) vs `glossary_context` (node, URN). The
  validator's `_singular` and schema-to-kind mapping assumed one token; both now go through one table.
- Prose naming the retired shapes: 14 pack/doc sites reworded (draft TBD-validator-and-docs list), plus the
  software-dev ASCII guard caught an em dash the fold carried in.

## Tracked issues

- In this PR: #283, #284, #285 (items 1, 5; 2-4 via #289), #286, #139 (the 2026-11-15 scope).
- #139 stays open for the 2026-11-14 comment's prose ("HiC", "Human-in-Charge", `mode: hic`, the
  glossary-curation-interview step that writes the term into a consumer's glossary): prose, not refused by the pin,
  and partly #274's.
- #221, #234 ask for glossary content "as glossary-pack content": their target shape is now the glossary context.
- #262 (manifest mirror vs the charter walk), #124 (preflight), #252 (Python port retirement), #253 (nightly
  against charter `main`) are untouched; #253 is next.
