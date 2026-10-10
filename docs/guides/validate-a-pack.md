---
title: Validate a pack
description: Run the Spec Kitty 4.x Charter Pack validator, read errors vs advisories, and understand the CI gate this repository runs on every pull request.
doc_status: wip
updated: '2026-10-10'
related:
- docs/guides/author-a-doctrine-pack.md
- docs/guides/publish-a-pack.md
---
# Validate a pack

Before publishing, validate your pack against schema and DRG constraints. The validator is the
**single canonical surface** that lets authors check their work against the same rules Spec
Kitty applies at load time.

## Run the validator

```bash
spec-kitty charter pack validate ./my-pack
spec-kitty charter org validate ./my-pack     # when the pack has an org-charter.yaml
```

Exit codes:

- `0` — pack passes. Advisories may print but do not affect exit.
- `1` — at least one error. Fix and re-validate.

Machine-readable output for CI:

```bash
spec-kitty charter pack validate ./my-pack --json
# {"advisories": [], "errors": [], "ok": true}
```

`charter pack validate` checks one pack in isolation. To check how several packs combine
(collisions between sibling packs, edges into another pack), register them in a project and run
`spec-kitty doctor charter-packs`.

## Errors vs advisories

| Condition | Class |
| --- | --- |
| Artifact YAML fails schema validation (for example a lowercase directive `id`) | **Error** |
| Duplicate `id` within the pack | **Error** |
| DRG content under `drg/*.graph.yaml` (org packs use `drg/fragment.yaml` only) | **Error** |
| `org-charter.yaml` or `presets/*.yaml` schema violation | **Error** |
| A retired field such as `accompanies_doctrine_pack` or `doctrine_pack_id` (`RETIRED_PACK_FIELD`) | **Error** |
| DRG edge endpoint that is neither built-in nor in this pack (`drg_external_endpoint`) | Advisory |
| Artifact ID collides with a built-in ID (`same_id_collision`; declare `enhances:` or `overrides:` to say which you mean) | Advisory |
| `pack-manifest.yaml` exists and was author-edited | Advisory |

### Common errors

- **`schema_invalid`** — compare the file with the kind's schema. Every artifact needs
  `schema_version: "1.0"`; directives need an upper-case `id`, `title`, `intent` and
  `enforcement`. The validator names the failing field.
- **`drg_root_graph_missing`** — the pack has `drg/*.graph.yaml` shards. Move the nodes and
  edges into `drg/fragment.yaml`.
- **No artifact directories found** — the pack root is wrong (point at the pack directory
  itself, not a parent), or no canonical subdirectory has valid YAML.

## The CI gate in this repository

Every pull request runs [`scripts/ci/validate-packs.sh`](../../scripts/ci/validate-packs.sh)
against a pinned spec-kitty build (`.github/workflows/validate-packs.yml`). It:

1. runs `charter pack validate` (and `charter org validate`) on every directory under `packs/`
   and `tests/fixtures/valid/`;
2. registers all of those packs together in a scratch project and runs
   `doctor charter-packs`, so sibling packs that collide fail the build;
3. checks that every pack under `tests/fixtures/invalid/` **fails** with exit code 1, so a
   validator that passes everything — or a CLI that lacks the command — turns the job red.

Run it locally before opening a PR:

```bash
scripts/ci/validate-packs.sh
```

## Next

- [Publish a pack](publish-a-pack.md)
