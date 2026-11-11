# Data Model: Per-pack digest gate

## Pack directory
- Identity: directory name `<name>` under `packs/`; participates iff `packs/<name>/pack.yaml` is a file.
- Hashed content: every regular file beneath it except the root `pack-manifest.yaml`.
- Invariant: no symlink or special file (digest refuses).

## Sidecar `packs/<name>.source.yaml`
| Field | Required | Notes |
|---|---|---|
| `tree_digest.algorithm` | yes | literal `spec-kitty-snapshot-sha256` |
| `tree_digest.value` | yes | 64 lowercase hex |
| `seeded_from{repository,path,commit,date}` | no | only where true (built-in) |
| leading comments | no | preserved verbatim by `--update` |

States: **fresh** (value == actual) · **stale** (differs) · **missing** (pack, no sidecar) · **orphan** (sidecar, no pack) · **malformed** (unparseable / missing keys / wrong algorithm).
Transitions: `--update`: stale → fresh (value line rewritten); missing → fresh (created from template); malformed → refused (manual fix); orphan → reported (manual delete).
`--check`: fresh → ok; any other state → `::error file=packs/<name>.source.yaml::…`, exit 1.

## Manifest node completeness
- Declared node: `(kind, id)` from `validate_pack_schemas.declared_nodes(pack_dir)`.
- Constituent: `(kind, id)` from `pack-manifest.yaml` `constituents[]`.
- `MANIFEST_EXEMPT_NODE_KINDS = {action, anti_pattern, template, mission_type, mission_step_contract}`.
- Invariant (packs with a manifest only): `declared − exempt ⊆ constituents`.

## Release asset
- `<pack>-vX.Y.Z.source.yaml`: byte copy of the sidecar at the tagged commit; one per released pack (see `contracts/pack-digest-cli.md`). Missing at the tag → release build fails.
