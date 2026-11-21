# Research: Citation and docs writing doctrine

All facts below were read at `origin/main` on 2026-11-21 (the PR-#214 landing head). Paths name artefacts; quoted anchors stand in for line numbers.

## R1 - Surface inventory

| Rule | Owner (single home) | Pointers (one sentence each) |
|------|---------------------|------------------------------|
| Stable identifier for changes (#219) | `packs/writing/styleguides/research-citation-discipline.styleguide.yaml`, new principle "Cite changes by a stable identifier" | software-dev `specify.prompt.md`, `plan.prompt.md`; foundation `adr-drafting-workflow` "Cross-link and commit" step |
| Content-anchored citations, counts carry their command (#150 rule 1) | same styleguide, new principle "Anchor code citations to content" | cross-reference with the stable-identifier principle and "Cite the specific locus" |
| Reproduce before declaring resolved (#150 rule 2) | `packs/foundation/procedures/adversarial-squad-deployment.procedure.yaml`, new step | anti-pattern "Resolved on paper" |
| Reachability before ruling (#150 rule 3) | same new step | anti-pattern "Ruling on an unreachable test" |
| No prototyping by delegates (#176, procedure part) | same procedure, dispatch step | none |
| Overturned ruling carries its measurement (#150 rule 4) | `packs/internal/procedures/cloud-session-dispatch.procedure.yaml`, after "Post every operator ruling on the governing issue" | none |
| Seven AI-prose tells (#238) | new `packs/writing/styleguides/ai-writing-tells.styleguide.yaml` | internal `report-writing` (one principle pointing to it) |
| doc-kitty frontmatter shape (#240) | `packs/writing/styleguides/common-docs.styleguide.yaml` | DIRECTIVE_042; `common-docs-write`, `common-docs-scaffold`, `common-docs-find`; `declare-page-audience`; internal `spec-kitty-page-audience` |

Surfaces found that teach the old frontmatter shape (grep `related:` and `audience` over `packs/writing` and `packs/internal`): common-docs styleguide ("Cross-references use related", "Audience is named in an audience" principles and patterns, `related cross-reference` and `audience-resolvable` patterns, `related-resolvable-paths` and `audience-resolvable` tooling rows, quality test); DIRECTIVE_042 (integrity rules "Every `related:` entry must resolve to an existing repo-relative `.md` path" and the `audience:` rule, and two validation criteria); `common-docs-write` ("Express cross-references as related: resolvable paths" step and its examples and failure modes); `common-docs-scaffold` (frontmatter step, "a related: list of resolvable repo-relative"); `common-docs-find` (mentions `related:` neutrally; check only); `declare-page-audience` ("persona pages linked by repo-relative path"); internal `spec-kitty-page-audience` ("one or more resolvable repo-relative `.md` paths").

Spec Kitty examples in scope (#274 slice): common-docs styleguide (ADR eras in the principle and pattern, "Charter Activation" in three examples, "populated in only 6 of 565 rows", the `docs/adr/<era>/` anti-pattern example); `common-docs-scaffold` (`adr/4.x/` examples and "adr/1.x through adr/4.x"); `common-docs-write` (`../adr/3.x/...doctrine-layer-merge-semantics.md`, `charter-activation.md`); squad procedure ("raising a StatusGateError"). Found but out of scope: software-dev `review.prompt.md` ("filed by era (for example `docs/adr/4.x/`)") and `pack-authoring` `deployable-skill-authoring` (a core ADR path as source) - not on #274's list; reported on #274 for a later slice.

## R2 - doc-kitty frontmatter facts

Source: `@spec-kitty/doc-toolkit` 0.3.0 (the version `site/package.json` pins), `lib/schema.ts::docKittyFields`, `lib/metadata.ts::resolveProfile`, `components/slots/Audience.astro`.

- `related`: array of a bare slug string or `{ ref, note? }`. The build and `check-links` enforce ref integrity; a miss fails the build. Slugs are paths under the docs root without `.md` (this repository's own pages use `guides/validate-a-pack`).
- `external_references`: array of `{ url, title, note? }` or `{ type, id }`.
- `audience`: array of `{ profile, guidance_text }`. `profile` resolves to the page at `context/audience/<profile>`; a miss renders the humanised profile name and warns on the build log (soft miss).

Decision: teach these shapes as the default; mention the path form once as legacy. Rationale: operator ruling on #240. Alternative (both shapes side by side) rejected by the ruling.

## R3 - Graph edge map

Writing (`packs/writing/*.graph.yaml`, hand-edited, manifests derived):
- node `styleguide:ai-writing-tells` (styleguide.graph.yaml);
- `styleguide:ai-writing-tells suggests styleguide:plain-language` (styleguide.graph.yaml);
- `mission_type:documentation scope styleguide:ai-writing-tells` (mission_type.graph.yaml);
- `action:documentation/generate scope styleguide:ai-writing-tells`, `action:documentation/validate scope styleguide:ai-writing-tells` (action.graph.yaml);
- `foundation::action:software-dev/specify scope styleguide:research-citation-discipline`, `foundation::action:software-dev/plan scope styleguide:research-citation-discipline` (action.graph.yaml; precedent: the existing `foundation::action:software-dev/retrospect scope styleguide:kitty-glossary-writing` edge);
- `agent_profile:comms-cleo suggests styleguide:ai-writing-tells` (agent_profile.graph.yaml).

Internal (`packs/internal/drg/fragment.yaml`): `styleguide:report-writing refines writing::styleguide:ai-writing-tells`. No pair above has an existing edge (checked with grep), so the edge-identity test holds.

Foundation: no edge (C-005). Its prompts and tactic name the writing styleguide in prose.

## R4 - Placement of the #219 prompt note

The issue asks for the note in the spec/plan (and ADR, where a pack ships one) authoring step prompts. No pack ships an ADR step prompt; the ADR authoring surface is foundation's `adr-drafting-workflow` tactic, which the documentation mission's design action scopes. Decision: specify and plan prompts plus the tactic's "Cross-link and commit" step. The prompts are ASCII (NFR-002).

## R5 - Versioning (DIRECTIVE_018)

Minor. The change adds guidance and one styleguide; the frontmatter change alters a recommendation in a styleguide, not a schema these packs validate, so a page that conformed before still validates in this repository's gates. Precedent: the additive analyze release (foundation lockstep 3.3.0, built-in 5.3.0).

- Lockstep set (foundation, writing, testing, refactoring, architecture, planning-analysis): 3.3.0 to 3.4.0, with the exact `==` pins between them and in built-in moved.
- built-in: 5.3.0 to 5.4.0.
- internal: 4.2.0 to 4.3.0; its writing range tightens to `>=3.4,<4` because the refines edge needs `ai-writing-tells`.
- Mission C (`test-doctrine-2`) bumps the same set in parallel. Whichever merges second rebases and restamps.

## R6 - Not folded

- #210: the dispatcher allowed it only with #207's owner's agreement. #207 orders its prompt children after #266 and no agreement is on record, so it is skipped (decision moment `measure_dont_estimate`).
- #176 step-prompt edits: left with #207 for the same ordering reason; only the squad procedure part is here.
