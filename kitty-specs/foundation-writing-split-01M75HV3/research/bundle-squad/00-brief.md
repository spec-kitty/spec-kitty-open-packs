# Shared brief: #73 bundle squad (READ-ONLY research)

Repo: /home/user/spec-kitty-open-packs, main @ 5c489d6. Read `packs/built-in/` there; it is unchanged.
Do NOT edit anything in the repo or in `.worktrees/`. Write only your own report into this folder.

Charter repo (read-only, at the lock pin fb24052): /home/user/spec-kitty/spec-kitty-charter
- docs/adr/0048-pack-composition-and-the-named-packs-split.md
- docs/adr/0052-*, docs/adr/0053-operator-rulings-on-the-pack-ecosystem-open-questions.md
- docs/plans/pack-ecosystem-work-breakdown.md (census, "Foundation membership"), docs/plans/pack-ecosystem-design-notes.md

Open-packs docs:
- docs/packs/catalog-proposal.md (catalog packs #1–#16)
- AGENTS.md (charter-only alignment)
- .kittify/charter/charter.md

## Precomputed data
In /tmp/claude-0/-home-user-spec-kitty-open-packs/e9f46af0-8323-5c9a-a991-c6e66101578d/scratchpad/research/:

| File | Contents |
|---|---|
| `edges.json` | `[source, relation, target, graph-file]` for all 1091 DRG edges of built-in. Relations: requires, scope, instantiates, suggests, rejects, specializes_from, refines, in_tension_with, reconciles_tension, vocabulary. |
| `delegates.json` | `[step_contract, "delegates_to", target]`: the candidates named inside mission step-contract bodies. |
| `profrefs.json` | Agent-profile body references. `directive-references` and `tactic-references` are checked references; `collab.*` entries are role words, not references. |
| `strict-membership.json` | The CURRENT approved split (see below). |
| `1-inventory.md` | Every node with inbound referrers, census divergences and contested clusters (its group rulings predate the operator's later rulings). |
| `2-architecture.md`, `3-consumers.md`, `4-gates.md` | Pack-level rules (d7 level rule, closures, qualification), consumers, gates. |

## Rules that bind any design
- A pack may `depends_on` only packs at its own level or nearer built-in (built-in < org < project).
- References must name a pack in the writer's transitive `depends_on` closure. There are no cycles.
- Sibling packs at one level may not hold the same id.
- built-in is a distribution pack (no artifacts) aggregating `foundation` and `writing`, both at built-in level.
- Opt-in specialist bundles are `pack_level: org`; they may depend on foundation, writing and other org bundles, acyclically.
- An edge whose source is in a lower pack can be declared in the higher pack's graph with a qualified source (`foundation::<urn>`). Body references (step-contract `delegates_to`, profile `*-references`) cannot be relocated: they must be in closure or removed.

## Operator rulings so far (the "choices" to corroborate or counterargue)
1. **Foundation = "only the very basis"**, strict one hop:
   - Seeds: generic-agent (display "Generic Giannis"), implementer-ivan, reviewer-renata, analyst-annie, and the software-dev, plan and research mission types (with actions, step contracts, templates).
   - Plus the directives and tactics the seeds reference directly, all cross-cutting directives, and the glossary.
   - Result: 115 nodes. No diagram/writer/architect profile, no language stacks.
2. **Documentation mission bundle goes to `writing`**, with the comms/docs profiles and docs styleguides (57 nodes).
3. **qa and internal take their topical items now**: 6 + 4.
4. **Org packs depend directly on foundation/writing** (not on built-in).
5. **The rest (217 nodes) is parked** in a temporary org pack `specialist-staging`, to be carved into specialist bundles one PR per bundle.
6. **Open question raised**:
   - Foundation's step contracts name execution-lanes (toolguide), trunk-based (paradigm), git-flow and example-mapping-workshop (procedures) in their bodies.
   - The kept directives each `require` their how-to procedure (about 37).
   - Under the strict rule these go to staging: the step-contract candidates get deleted, and the directive→procedure edges get relocated.
7. **java** (#5, 4 items) will be an org pack depending on foundation; rust/go likewise. Whether built-in should aggregate java is open and not to be decided here.

The operator is unsure about the planned opt-in org bundle split and wants the foreseen bundles documented from research.
