# Foundation wiring (WP05)

**Source of the dependency.** `foundation` pack_id `01M75HSYR9S9KPA372PHGT0EX3`, read from
`packs/foundation/pack.yaml` on `feat/73-foundation-writing-split` at `fb64afd` (draft PR #198). It
was not typed from memory. This branch is stacked on that branch.

**Template.** `packs/java` on the same branch. Its `java-jenny` edges were mirrored for `rust-ruben`
and `go-gwen`.

## Edges added, per pack (each target was grep-checked in `packs/foundation` at `fb64afd`)

| Source | Target | Relation |
| --- | --- | --- |
| profile | `foundation::agent_profile:implementer-ivan` | specializes_from |
| profile | `foundation::directive:DIRECTIVE_010`, `_024`, `_025`, `_030`, `_034`, `_051` | requires |
| profile | `foundation::directive:DIRECTIVE_041`, `DISCIPLINED_REFACTORING` | suggests |
| profile | `foundation::tactic:acceptance-test-first`, `tdd-red-green-refactor`, `dependency-hygiene`, `supply-chain-install-safety` | requires |
| styleguide | `foundation::directive:DIRECTIVE_030`, `_034`, `foundation::tactic:tdd-red-green-refactor` | suggests |
| `foundation::tactic:supply-chain-install-safety` | toolguide | suggests |

**Dropped.** None. Every planned target is held by `foundation`.

**Testing (separate, droppable commit).** It adds `depends_on: testing` (`01M75PCTC6HS38NX8HJGT26VTP`), the requires edge to `testing::procedure:test-first-bug-fixing` and the suggests edge to `testing::directive:USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY`.

**Before that commit.** java-jenny's edges into `testing`, the `test-first-bug-fixing`
procedure and the `USE_MUTATION_TESTING_TO_VALIDATE_TEST_QUALITY` directive, would need
`depends_on: testing`. The operator ruled on 2026-11-11 that rust and go carry them, for parity with java.
They come in a separate commit, so that commit can be dropped. `bdd-scenario-formulation` is not
mirrored: java ties it to Cucumber-JVM, and neither stack pack teaches a BDD runner.

**Verification.** On the stacked branch with `CHARTER_CONTRACT_DIR` set:

- `validate-packs.sh`: 20 packs, 0 violations, and the cross-pack check passes;
- `check-built-in.sh`: green;
- `check_vocabulary.py`: 0 findings;
- `gen_pack_reference.py --check`: 19 pages, no drift, and the pages show the dependency.

The charter service check, which resolves qualified edges, runs in CI only.
