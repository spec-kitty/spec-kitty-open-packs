# Tasks — Docsite & README overhaul

Single-branch mission; WPs run sequentially in the write checkout.

### WP01 — Toolkit bump + nav restructure
Depends on: none
- T001 Bump `@spec-kitty/doc-toolkit` to 0.3.0; apply loader/CLI migration.
- T002 Rewrite `docs/_meta/sections.yaml` to the new IA; delete `docs/toc.yml`.

### WP02 — Landing, README, architecture overview, glossary
Depends on: WP01
- T003 Rewrite `docs/index.md` as the overview.
- T004 Rewrite `README.md`.
- T005 Add `docs/architecture/overview.md`; refresh `architecture/index.md`.
- T006 Add `docs/glossary/index.md`.

### WP03 — Contracts, artefacts, organisations
Depends on: WP01
- T007 Add `docs/contracts/index.md`.
- T008 Add `docs/artefacts/index.md`.
- T009 Add `docs/organisations/index.md`.

### WP04 — Terminology sweep + generator + changelog
Depends on: WP02, WP03
- T010 Classify and rewrite governing-sense "doctrine" in live docs, site config, CONTRIBUTING/SECURITY/templates; rename the two guides and fix links.
- T011 Update generator wording; regenerate; `--check`; run generator tests.
- T012 Changelog entry.
