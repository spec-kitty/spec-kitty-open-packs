# Implementation Plan: Charter slice B migration

**Branch**: `feat/slice1-readme-retire-org-charter` | **Date**: 2026-11-12 | **Spec**: [spec.md](spec.md)
**Input**: Mission specification from `kitty-specs/charter-slice-b-migration-01M78K20/spec.md`

## Summary

Content and tooling migration to the charter's slice B. Pin charter `17ce3f9`. Make each pack's root `README.md`
its only document (#241): merge `pack.md`, fold `PROVENANCE.md`, delete both. Retire `org-charter.yaml` and
`active_charter` (#242): `internal`'s 18 required ids become must-have items of `presets/base.yaml`, and the 11
inert files go. Follow-on edits: the four CI/doc scripts and their tests, the live docs, the fixture, the
glossary sentence, regenerated pack pages, restamped digests and a CHANGELOG entry. Prove the result with the
charter service check at the pin.

## Technical Context

**Language/Version**: Python 3.12 (stdlib + PyYAML) for scripts and tests; Markdown and YAML pack content; Java 25
for the charter service jar built from the pinned commit.
**Primary Dependencies**: the charter service at `17ce3f9` (built by `scripts/ci/charter_service_jar.sh`); the pinned
charter's pack schemas and `file-kinds.yaml` (fetched by `validate_pack_schemas.py`). No dependency is added.
**Storage**: files in git.
**Testing**: `pytest tests/`; gates `scripts/ci/check-pack-digests.sh`, `scripts/ci/validate_pack_schemas.py`,
`scripts/ci/check_vocabulary.py`, `scripts/docs/gen_pack_reference.py --check`,
`scripts/ci/charter_service_check.py --jar <jar>`.
**Target Platform**: GitHub Actions (`validate-packs.yml`, `docs-site.yml`) and a developer machine.
**Project Type**: content repository with CI tooling.
**Performance Goals**: n/a.
**Constraints**: README must stay readable by the charter's `pack-document` Markdown model (one H1, ATX, no closing
`#` on H1/H2, no CR/BOM, no open fence). Generated pages and digests are never hand-edited.
**Scale/Scope**: 19 packs, 19 `pack.md`, 16 `PROVENANCE.md`, 12 `org-charter.yaml`, one fixture, about 20 docs.

## Charter Check

- DIRECTIVE_003: no new decision. The ADR-0042 amendment and the #431 ruling are recorded on the charter side; this
  repo implements them. Existing ADRs keep their history.
- DIRECTIVE_044 (generated vs authored): the Purpose on each generated page now comes from the authored README
  preamble; Level, `pack_id` and Depends-on stay generated-only (dropped from READMEs).
- DIRECTIVE_037 (docs in sync): every live mention named in #241 and #242 is corrected in the same PR.
- DIRECTIVE_041: tests change only where they pin behaviour that changed (the excluded-file list, the companion
  check, the Purpose source, the vocabulary row).
- Changelog entry for user-facing change: yes.
- Supply chain (DIRECTIVE_051): no dependency added or upgraded. The charter pin moves; it is a commit SHA, and the
  jar is built from source at that SHA.
- Alignment rule (AGENTS.md): core still reads `org-charter.yaml`; that gap is recorded in the PR, not a blocker.

## Design decisions

1. **One PR, one pin** (operator ruling, 2026-11-12): pin, #241 and #242 together, because only all three register
   19/19.
2. **Service check first**: run `charter_service_check.py` at `17ce3f9` on the unchanged packs to confirm the
   refusals are exactly the expected ones (`retired`, `pack_unreadable`) before editing content.
3. **README merges by script plus review**: the mechanical steps (fold `PROVENANCE.md` under `## Provenance`,
   demote its headings, drop its H1, delete descriptor bullets, add `pack.md` H2s other than "Contents") are the
   same for the nine carved packs, so they are applied uniformly, then each README is read. The long READMEs
   (internal, qa, cave-kitty, event-driven, go, rust, built-in, foundation, writing, spdd) are edited by hand per
   #241's per-pack fixes.
4. **README shape check**: a small check of the Markdown-model rules (single H1, ATX only, no closing `#`, no
   CR/BOM, closed fences) is run over every root README locally. It is not added as a new CI gate: the service
   check already refuses an unreadable README.
5. **Generator**: `read_pack_document` reads `README.md` and keeps the same preamble rule (text between the H1
   and the first H2). The "no preamble" fallback text names the README.
6. **internal**: `presets/base.yaml` is replaced by #242's listing, with a new header comment. No `policy.yaml`
   (C-005). `skill_namespace` is dropped; the README says the `kitty-` prefix is core's rendering.
7. **Glossary**: the "Charter Pack" definition takes the operator's governing-preset wording. The core mirror is
   handed to the operator as a follow-up (this session cannot write to core).

## Work packages

- **WP01 – Tooling (scripts and tests)**: `charter_service_check.py` `NOT_REGISTERED`; `validate_pack_schemas.py`
  companion pre-check and allowance; `check_vocabulary.py` qa row; `gen_pack_reference.py` README reader; tests.
- **WP02 – README merges (#241)**: the 19 packs, `built-in.source.yaml` and `internal/pack.yaml` comments.
- **WP03 – Org charters retired (#242)**: 12 packs, fixture, `internal` preset, preset/README text in go, rust,
  event-driven, qa; `pack.yaml` header comments.
- **WP04 – Docs, generated pages, digests, CHANGELOG, proof**: live docs from both issues, glossary sentence,
  `.kittify` comments and charter.md, regenerate `docs/packs/*.md`, restamp digests, CHANGELOG, run every gate and
  the service check.

## Risks

- **The pin jumps 182 charter commits** (`fb24052..ddfd954`, plus 36 after): new refusals beyond the two issues may
  appear. Mitigation: decision 2. Anything outside #241/#242 is reported, and fixed here only if small.
- **Merge loses text**: NFR-003. Mitigation: a word-level diff of each old `pack.md` H2 and `PROVENANCE.md` body
  against the new README.
- **PR #243 (java 2.1.0)** may touch `packs/java/`. Rebase and restamp if it lands first.
