# Data Model: Rust and Go stack packs

The "entities" are pack artifacts. Each is validated by its charter schema (charter `fb24052`).

## Per pack (`<lang>` ∈ {rust, go})

| Artifact | File | Id | Key invariants |
| --- | --- | --- | --- |
| Pack descriptor | `pack.yaml` | `pack_id` (ULID, minted once) | `name: <lang>`, `pack_level: org`, `parent_pack: null`, `pack_version: 1.0.0`, `active_charter`, `pack_drg`. Once foundation exists: `depends_on: [{pack_id: <foundation>, range: ">=1.0,<2"}]`. |
| Pack document | `pack.md` | — | H1 plus a preamble only (the generator uses it as "Purpose"). |
| Org charter | `org-charter.yaml` | — | `schema_version: 2`, `org_name: spec-kitty-<lang>`, activates nothing. |
| Preset | `presets/<lang>.yaml` | `<lang>` | Activates the styleguide, toolguide and profile. |
| Styleguide | `styleguides/<lang>-conventions.styleguide.yaml` | `<lang>-conventions` | `scope: code`, `applies_to_languages: [<lang>]`, every principle description ≤ 255 characters, each pattern and anti-pattern with a bad and a good example. |
| Toolguide | `toolguides/<lang>-review-checks.toolguide.yaml` | `<lang>-review-checks` | `guide_path` points at the companion guide; `commands` lists the tools. |
| Guide | `toolguides/<lang>-review-checks.guide.md` | — | H1 equals the toolguide title, no preamble, `## Overview` first, fixed blocks in order (Overview, When to use, Setup, Usage, then freeform sections, then Cautions, Known limitations, References). |
| Profile | `agent_profiles/<name>.agent.yaml` | `rust-ruben` / `go-gwen` | `role: implementer`, `applies_to_languages: [<lang>]`, `styleguide-references` and `toolguide-references` to its own pack. |
| DRG fragment | `drg/fragment.yaml` | — | One node per artifact. Edges, as below. |

## Edges

Now (local to the pack):

- `agent_profile:<name>` → `styleguide:<lang>-conventions` : **requires** (#131)
- `agent_profile:<name>` → `toolguide:<lang>-review-checks` : suggests
- `styleguide:<lang>-conventions` → `toolguide:<lang>-review-checks` : suggests

Once foundation exists (qualified, per the orchestrator's #73 design; each one is checked against
the landed pack):

- `agent_profile:<name>` → `foundation::agent_profile:implementer-ivan` : specializes_from
- `agent_profile:<name>` → `foundation::directive:DIRECTIVE_010 / _024 / _025 / _030 / _034` : requires
- `agent_profile:<name>` → `foundation::tactic:dependency-hygiene`, `foundation::tactic:supply-chain-install-safety`, `foundation::tactic:tdd-red-green-refactor` : requires
- `styleguide:<lang>-conventions` → `foundation::directive:DIRECTIVE_030`, `foundation::directive:DIRECTIVE_034` : suggests

## State

None. Activation is the consumer's: the preset puts the artifacts in force, and the org charter puts
nothing in force.
