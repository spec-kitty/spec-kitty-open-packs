---
title: "Pack: example-pack"
description: "Generated reference for the example-pack Charter Pack: 1 directive, 1 tactic, 1 preset."
doc_status: active
updated: '2026-10-11'
type: API
kind: Reference
tags:
- pack-reference
- generated
generated:
  by: scripts/docs/generate_pack_reference.py
  at: '2026-10-11'
related:
- packs/reference
---

# Pack: example\-pack

> **Generated — do not edit.** This page is rendered from `tests/fixtures/valid/` by `scripts/docs/generate_pack_reference.py`; CI fails on drift. Change the pack, then re-run the generator.

## Summary

| Field | Value |
| --- | --- |
| Source | [`tests/fixtures/valid/example-pack/`](../../fixtures/valid/example-pack/) |
| Purpose | — (no `pack.yaml`) |
| Depends on | — |
| Artifacts | 1 directive, 1 tactic, 1 preset |
| DRG fragment | 0 node(s), 1 edge(s) ([`drg/fragment.yaml`](../../fixtures/valid/example-pack/drg/fragment.yaml)) |
| Org charter | org `example`; keys: `org_name`, `schema_version` ([`org-charter.yaml`](../../fixtures/valid/example-pack/org-charter.yaml)) |

## Provenance & integrity

- **Content checksum** (`open-packs-sha256-v1`, 5 file(s)): `sha256:7c6cebf4a375ef4301f60c1f9438cd5c4ae5aa8264fb4515200695c2d96232af`
- **File set:** the git-shipped files (tracked, plus untracked files that are not ignored). A clean checkout or release tarball of the pack contains exactly
  these files. Symlinks and file names containing a backslash or newline are rejected.
- **Verify** a fetched copy from inside the pack directory:

  ```sh
  # in a git checkout (matches what CI hashes):
  git ls-files -z --cached --others --exclude-standard -- . | tr '\0' '\n' | LC_ALL=C sort \
    | while IFS= read -r f; do sha256sum "./$f"; done | sha256sum
  # in a plain download of exactly those files:
  find . -type f ! -path './.git/*' | LC_ALL=C sort \
    | while IFS= read -r f; do sha256sum "$f"; done | sha256sum
  ```

  (`shasum -a 256` in place of `sha256sum` on macOS.) This is tamper-evidence for the published
  content, not a signature: it tells you the copy matches this repository, not who to trust
  (ADR 2026-07-18-3).

## Directives

| ID | Title | Summary | Enforcement | Source |
| --- | --- | --- | --- | --- |
| `EXAMPLE_001_SECRET_HANDLING` | Never commit credentials to the repository | Secrets come from the environment or a secret manager\, never from the repository\. | `required` | [`directives/example-001-secret-handling.directive.yaml`](../../fixtures/valid/example-pack/directives/example-001-secret-handling.directive.yaml) |

## Tactics

| ID | Title | Summary | Steps | Source |
| --- | --- | --- | --- | --- |
| `example-tac-001-scan-staged` | Scan staged content for credentials | — | 1 step | [`tactics/example-tac-001.tactic.yaml`](../../fixtures/valid/example-pack/tactics/example-tac-001.tactic.yaml) |

## Presets

| ID | Title | Summary | Activates | Source |
| --- | --- | --- | --- | --- |
| `example` | example | Turn on the example rules\. | 1 directive | [`presets/example.yaml`](../../fixtures/valid/example-pack/presets/example.yaml) |
