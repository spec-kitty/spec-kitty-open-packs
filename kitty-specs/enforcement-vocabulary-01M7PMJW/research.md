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

### R5 inventory (spec scan plus the independent hunt, adjudicated under R3)

**Remove or reword (directive bodies, FR-004/FR-005)**

- foundation 051 scope "advisory at the transition-gate level in v1 ... must not silently hard-block": remove; keep "visibility and explicit evidence; silence is not compliance".
- foundation 051 integrity rule 5 ("no fail-closed handler in v1 ... keep it advisory"): remove. It is level-only; its one substantive clause, that omitting the check is not compliance, is integrity rule 1 (NFR-003).
- foundation 052 "The mandatory output is the diagnosis": reword to "What the fix must produce is the diagnosis".
- foundation 049 "This is advisory guidance, not a runtime gate: ...": remove.
- foundation reconcile-change-scope-tensions "acceptable lenient-adherence allowance": reword to "acceptable allowance".
- internal cloud-session-orchestration intent "Makes the integrity rules ... binding charter content": reword to "Sets the integrity rules ..."; scope "remain advisory in the cloud-session-dispatch procedure": reword to "stay with the cloud-session-dispatch procedure, outside this directive".
- qa QA_002 "This is not a recommendation — every one of the seven is mandatory": drop the level framing and keep "no partial credit".
- qa QA_001 title "QA Traceability Mandatory": retitle to "QA Requirement Traceability" (Q3); the id, file name and slug references stay.
- writing ACTION_ITEM_ATTRIBUTION "This rule is enforced as a hard validation gate:": drop the framing and keep the concrete refusal.
- writing 042 "This directive binds the conventions ... enforced by live checks": reword "binds" to "carries"; keep the live checks.

**Remove (content citing a directive, FR-006)**: the "advisory in v1" or "Advisory:" posture sentences in software-dev.mission-type.yaml (3 substeps), plan.mission-type.yaml (supply-chain-check), the plan, implement and review prompts and guidelines (6 files), and the supply-chain-install-safety tactic (3 places); the "; enforcement `required`" suffix in the 8 cave-dev step prompts.

**Reword (other content, FR-007)**

- Graph edge reasons: foundation directive.graph (2), tactic.graph (1), internal drg fragment (1), writing directive.graph (1).
- cave-kitty README (2) and the cave-sty-001 styleguide: "is advisory context" becomes "is context an agent applies".
- writing kitty-glossary-writing styleguide: drop "This is not optional."
- writing agents: minutes-mahad "hard constraints" and "hard gate" become "applies" and "is checked"; comms-cleo "mandatory before drafting" becomes "happen before drafting".
- writing meeting-minutes-format styleguide :83 "hard gate": becomes "is checked".
- writing common-docs-scaffold tactic "required by this directive but not (yet) lint-enforced": becomes "part of this directive's rule, though no lint checks it yet".
- foundation software-dev.mission-type `content`: "Your charter enforces ..." and "(non-negotiable)" are reworded to name the practices without claiming a level.
- foundation glossary adversarial-squad "Optional and advisory, never a gate": becomes "Optional, never a gate" (the level word clashes with the new term).

**Folded from the post-tasks review (2026-11-18)**

- supply-chain tactic :118-122, the example disposition `rationale="v1 remains advisory per C-003 ..."`: reword the example to a substantive rationale.
- pack-authoring doctrine-daphne :52 and the onboard-external-agent-to-pack procedure :72, "a non-negotiable rule becomes a directive": reword to "a rule ("always", "never", "must") becomes a directive". A directive is not non-negotiable by kind; its level is a default.
- The QA_001 title also appears in qa `drg/fragment.yaml` :9, three qa agent profiles (`directive-references` names) and `docs/guides/getting-started.md` :88: retitle all of them.
- `docs/glossary/index.md` (hand-maintained) gains an "Enforcement level" entry that links the term.
- Versions: see the version decision (operator question Q4).

**Keep (other sense, or substance)**: internal report-debrief skill "(non-negotiable)" heading (the skill's own step emphasis); software-dev analyze.prompt "charter is non-negotiable" (charter authority); 025 "not an optional nicety" (the rule is to fix by default); 046 and mission-wrap-up "recommended" or "optional" (procedure role, not a directive level); no-full-heavy-suites "supersedes" (precedence of guidance); retrospective-facilitator "mandatory; cannot be marked done" (a runtime fact); template "(mandatory)" section headers; runtime-gate descriptions ("analyze is not optional", "informational only"); npm and security advisories; QA "in v1" format versions; glossary enforcement tiers and modes; meeting-minutes-pipeline "hard gate" (the procedure's own check); "Owner is mandatory" (a report field); 032, 042 live checks, 043, 030, qa-007/008 and 053 (scope and substance).
