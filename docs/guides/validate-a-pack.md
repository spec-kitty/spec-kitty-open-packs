---
title: Validate a pack
description: Run the canonical Spec Kitty pack validator, read errors vs advisories, and wire validation into CI for open doctrine packs.
doc_status: wip
updated: '2026-07-12'
related:
- docs/guides/author-a-doctrine-pack.md
- docs/guides/publish-a-pack.md
---
# Validate a pack

Before publishing, validate your pack against schema and DRG constraints. Validation is the
**single canonical surface** that lets downstream authors check their work against the same
rules instead of maintaining a bespoke suite — that shared validator is tracked upstream as
[core #2471](https://github.com/Priivacy-ai/spec-kitty/issues/2471).

## Run the validator

```bash
spec-kitty doctrine pack validate ./my-pack
```

Exit codes:

- `0` — pack passes. Advisories may print but do not affect exit.
- `1` — at least one error. Fix and re-validate.

Machine-readable output for CI:

```bash
spec-kitty doctrine pack validate ./my-pack --json
```

## Errors vs advisories

| Condition | Class |
| --- | --- |
| Artifact YAML fails schema validation | **Error** |
| Duplicate `id` within the pack | **Error** |
| Dangling DRG edge (target URN not in merged artifact set) | **Error** |
| DRG extension modifies or removes a built-in node | **Error** |
| `org-charter.yaml` schema violation | **Error** |
| Artifact ID collides with a built-in ID | Advisory |
| `pack-manifest.yaml` exists and was author-edited | Advisory |
| `enforcement` value other than `"advisory"` | Advisory |

### Common errors

- **Dangling DRG edge** — the named URN doesn't resolve in your pack's artifact set. Add the
  missing artifact, fix the URN, or remove the edge. The validator prints the URN and the
  fragment file.
- **DRG extension attempts to modify a built-in node** — fragments are additive only.
  Refactor to *add* edges/nodes instead.
- **No artifact directories found** — the pack root is wrong (point at the pack directory
  itself, not a parent), or no canonical subdirectory has valid YAML.

## Wire it into CI

Because validation is a single command with a clean exit code, gating a pack repository is a
few lines. Example GitHub Actions step:

```yaml
- name: Validate doctrine packs
  run: |
    pipx install spec-kitty-cli
    for pack in packs/*/; do
      spec-kitty doctrine pack validate "$pack" --json
    done
```

> **🚧 WIP.** This repository does not yet ship a CI workflow that validates every pack on
> push; adding one is a bootstrap follow-up once the first packs are materialized. Until then,
> validate locally before opening a PR.

## Next

- [Publish a pack](publish-a-pack.md)
