---
title: "Pack: example-pack"
description: "Generated reference for the example-pack Charter Pack: 1 directive, 1 tactic, 1 preset."
doc_status: active
updated: '2026-10-10'
type: API
kind: Reference
tags:
- pack-reference
- generated
generated:
  by: agent/generate_pack_reference.py
  at: '2026-10-10'
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
| Org charter | org `acme`; keys: `org_name`, `schema_version` ([`org-charter.yaml`](../../fixtures/valid/example-pack/org-charter.yaml)) |

## Provenance & integrity

- **Content checksum** (`open-packs-sha256-v1`, 5 file(s)): `sha256:915faabb7857b6df96bd2ff1907ea848526777b4639a1c4ce5ab9ff1bd8fef60`
- **File set:** the git-shipped files (tracked, plus untracked files that are not ignored). A clean checkout or release tarball of the pack contains exactly
  these files. Symlinks and file names containing a backslash or newline are rejected.
- **Verify** a fetched copy from inside the pack directory:

  ```sh
  # in a git checkout (matches what CI hashes):
  git ls-files -z --cached --others --exclude-standard -- . | tr '\0' '\n' | LC_ALL=C sort \
    | while IFS= read -r f; do sha256sum "./$f"; done | sha256sum
  # in a plain download of exactly those files:
  find . -type f ! -path '*/.*' | LC_ALL=C sort \
    | while IFS= read -r f; do sha256sum "$f"; done | sha256sum
  ```

  (`shasum -a 256` in place of `sha256sum` on macOS.) This is tamper-evidence for the published
  content, not a signature: it tells you the copy matches this repository, not who to trust
  (ADR 2026-07-18-3).

## Directives

| ID | Title | Summary | Enforcement | Source |
| --- | --- | --- | --- | --- |
| `ACME_001_SECRET_HANDLING` | Never commit credentials to the repository | Secrets come from the environment or a secret manager\, never from the repository\. | `required` | [`directives/acme-001-secret-handling.directive.yaml`](../../fixtures/valid/example-pack/directives/acme-001-secret-handling.directive.yaml) |

## Tactics

| ID | Title | Summary | Steps | Source |
| --- | --- | --- | --- | --- |
| `acme-tac-001-scan-staged` | Scan staged content for credentials | — | 1 step | [`tactics/acme-tac-001.tactic.yaml`](../../fixtures/valid/example-pack/tactics/acme-tac-001.tactic.yaml) |

## Presets

| ID | Title | Summary | Activates | Source |
| --- | --- | --- | --- | --- |
| `acme` | acme | Turn on the Acme rules\. | 1 directive | [`presets/acme.yaml`](../../fixtures/valid/example-pack/presets/acme.yaml) |
