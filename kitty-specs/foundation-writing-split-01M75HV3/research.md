# Research: Split built-in into foundation and writing

Inputs: the phase-1 squad reports in [research/](research/):
- `1-inventory.md`: per-node table. Its group rulings are superseded by the operator rulings below.
- `2-architecture.md`: levels, aggregation, qualification, java.
- `3-consumers.md`: core, service, org packs, versioning.
- `4-gates.md`: gates, manifest, digest, #182.

## D1 — Pack levels and graph

- **Decision**: foundation and writing are `pack_level: built-in`; the ten bundles are `org`.
  - Edges: built-in → foundation, writing; writing → foundation; bundles per the DAG in membership.json.
  - Org packs depend directly on the member packs they use (operator ruling).
- **Rationale**: ADR-0048 d7 (amended) lets a pack depend only on its own level or one nearer built-in (`PackCompositionResolver.java:882-903`).
  - built-in can therefore only aggregate built-in-level packs.
  - Ordering foundation < writing < built-in < org proves acyclicity.
- **Alternatives**: foundation and writing at org level. Rejected, because built-in → org is a level violation.

## D2 — Aggregation mechanism

- **Decision**: aggregation is plain `depends_on` with exact `==1.0.0` pins (ADR-0048 d12/d17).
- **Rationale**: the descriptor schema at the pin is closed and has no aggregation field.
- **Alternatives**: none at the pin.

## D3 — Foundation strictness (operator, DM 01M75HW2TNWHTYH1HX68AJJ32B) — SUPERSEDED by D11

- **Decision**: foundation contains:
  - the seeds: generic-agent ("Generic Giannis"), implementer-ivan, reviewer-renata, analyst-annie, and the software-dev, plan and research mission bundles;
  - the directives and tactics those seeds reference directly (one hop: `requires`/`scope`/`instantiates` graph edges, step-contract `delegates_to`, profile `directive-references`/`tactic-references`);
  - all cross-cutting directives (DM 01M75HWGJ5987VY15YJEWJFBH8);
  - the spec-kitty-core glossary.

  Everything else that is not writing/qa/internal goes to specialist-staging.
- **Rationale**: the operator asked for "only the very basis".
- **Alternatives**: the seeds plus their whole strong closure (~160 nodes). Rejected by the operator.
- **Consequence**: without staging installed, plan/software-dev lose their paradigm, procedure and architect guidance. Accepted.

## D4 — Edge relocation rule

- **Decision**: an edge is homed in the graph of its source's pack when the target is in that pack's closure.
  - Otherwise it is declared in the target's pack, with the source qualified `<source-pack>::<urn>`, provided the source's pack is in the target pack's closure.
  - Targets outside the source's own pack are qualified `<pack>::<urn>`.
  - An edge whose two ends sit in packs that are mutually outside each other's closure is impossible here: the bundle DAG in membership.json was checked by `research/bundle-squad/final.py` (0 edges without a legal home).
- **Rationale**: ADR-0048 d9 and ADR-0064 (graph documents are the relationship source). `EdgeIndex.java:410-425` homes a qualified source at its pack.
- **Alternatives**: deleting cross-boundary edges. Rejected, because it loses guidance that the bundle restores when installed.

## D5 — Body references

- **Decision**: a reference inside an artifact body that leaves its pack's closure is removed from the body, and its edge is relocated per D4. Examples: a profile `directive-references` or `tactic-references` entry, a step-contract `delegates_to` candidate.
  - Known case: analyst-annie → DIRECTIVE_047 (writing).
  - In-closure body references to another pack stay as they are written (bare). If the service refuses them, they are qualified.
- **Rationale**: `profile_reference_violations` (`validate_pack_schemas.py:992`) checks profile references against the pack closure.
- **Alternatives**: qualifying the body reference. Not possible, because the target is outside the closure.

## D6 — `missions/` layout kept

- **Decision**: mission bundles move unchanged under `missions/<type>/`.
- **Rationale**: `*/mission_types/*.yaml` is retired at the pin (`file-kinds.yaml:261-265`).

## D7 — Versions

- **Decision**:
  - built-in goes to 2.0.0.
  - foundation, writing and every bundle start at 1.0.0.
  - Each org pack bumps its minor version, and its range to the new packs is `>=1.0,<2`.
- **Rationale**: changed content re-registered under an unchanged version is refused (ADR-0065 D2/D9). The built-in major version marks the breaking change.

## D8 — Java in built-in (left open)

- (a) built-in aggregates java: java is re-levelled to built-in, which needs a charter ADR amending ADR-0053 d1/d3 and ADR-0048 d14.
- (b) java stays opt-in on foundation.
- This split forecloses neither: (a) later means one extra `depends_on` entry on built-in plus the re-level. Not decided here (C-004).

## D9 — Manifests and digest

- **Decision**:
  - The built-in-level packs (built-in, foundation, writing) each carry a `pack-manifest.yaml`. The member list is written by the migration tool from the moved files; hashes are restamped by `validate_pack_schemas.py --regenerate-manifest`.
  - The digest in `packs/built-in.source.yaml` keeps covering `packs/built-in` only. Extending parity to the members is follow-up work, since core fetch is out of scope.
- **Rationale**: keeps C-006. The digest exists for core's fetch of built-in.

## D10 — #182 guard scope

- **Decision**: the guard compares manifest constituents with the file-backed doctrine kinds found on disk: profiles, directives, tactics, procedures, paradigms, styleguides, toolguides, assets, glossary packs, and templates that have files.
  - Graph-only kinds (action, anti_pattern, mission_type, step contract) are exempt.
  - It applies only to packs that have a manifest.
- **Rationale**: `4-gates.md` §3. Otherwise the guard is red on day one.

## Security / supply chain

No dependency is added, upgraded or removed. DIRECTIVE_051 has no applicable control, and no adversarial pass is needed for dependencies.

## D11 — Bundle squad and re-scope (operator, DMs 01M75PEBPTKXHKAFXT4P6FY977 … 01M75PF7Q7V98Z2PGV7NRT8QM5)

**Supersedes** D3 and the specialist-staging pack.

**Decision**:
- Foundation is the basis plus its how-to layer, the four step-contract delegates, human-in-charge, git workflow and DISCIPLINED_REFACTORING (178 nodes).
- Writing adds the glossary group (68).
- Ten opt-in bundles are carved now; testing is the hub bundle.

**Rationale**: four independent lenses ([research/bundle-squad/](research/bundle-squad/)).
- The strict cut was invalid. annie → 047 is a cycle; writing → staging is a level violation; roles went unfilled; step hooks emptied; 33 directive how-tos had no other consumer.
- One staging pack would cost about 9 breaking repoints.
- Stacks need `testing`.

**Alternatives**:
- strict + fixes (~120);
- an opt-in core-engineering bundle;
- staging with later carving.

All were rejected by the operator.
