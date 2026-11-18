# Research: Directive enforcement vocabulary

## R1. What the pinned charter contract allows for `enforcement:`

- **Evidence**: `charter.lock.yaml` pins `spec-kitty-charter@050d780876c6e9bd4265c7ec3335abe1b95cda61`. At that commit, `contracts/packs/schemas/directive.schema.json` has `required: [id, schema_version, title, intent, enforcement]` and `additionalProperties: false`. Its properties are `id, schema_version, title, intent, enforcement, scope, integrity_rules, validation_criteria, explicit_allowances`. `$defs.Enforcement` is a string enum `required | lenient-adherence | advisory`, rank-ordered in the charter model.
- **Decision**: keep the field on every directive, unchanged in value, and read it as the pack-supplied default level.
- **Rationale**: removing it fails schema validation at the pin, and so does any alias such as `default_enforcement`, because `additionalProperties` is false. Per #5207 (core), the effective level belongs to the adopting charter's activation config, so the pack value is what that config overrides.
- **Alternatives considered**: retire the field (refused by the pin); add a parallel `default_enforcement` field (refused by the pin, and a second source of truth); leave the field's meaning implicit (that is the reported defect).

## R2. Where the level vocabulary is defined today

- No glossary context in any pack defines `required`, `lenient-adherence` or `advisory` as levels (verified with grep over `packs/*/glossaries/`). The only definitions are the enum comment in `docs/guides/author-a-charter-pack.md` and the "binding rule, with an enforcement level" row in `docs/artefacts/index.md`.
- The glossary term schema at the pin admits `id, name, definition, examples, aliases, avoid, status, see_also`; `id, name, definition, status` are required. `see_also` entries are written `term:<context>/<term-id>`.
- **Decision**: one term, `enforcement-level`, in `spec-kitty-core`, with `see_also` pointing at `directive`, `charter` and `activation-preset`.

## R3. Classification rule (operator Q1, recommendation A)

- **Remove**: any claim about how strictly a directive binds: its level ("advisory", "required"), criticality ("mandatory", "binding", "non-negotiable"), gate posture ("advisory at the transition-gate level in v1", "not a runtime gate", "does not gate the transition"), whether in the directive itself or in content that cites it.
- **Keep**: the rule's substance phrased with must/never; descriptions of a concrete check that a procedure or tool runs; other senses of the words (npm advisories, mandatory report fields, glossary enforcement tiers and modes, format versions such as `qa-traceability/v1`).

## R4. Collisions (2026-11-18)

- No open pull request on the repository. #266 (software-dev prompts) and #273 (directive bodies) are not in flight, so there is nothing to land after. If either opens first, rebase onto it with a signed rebase.

## R5. Inventory

See `occurrence_map.yaml` (classification per category and per file). The independent occurrence hunt (reviewer lens) is folded into the map.
