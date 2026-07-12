---
title: Use a doctrine pack
description: Configure a Spec Kitty consumer project to fetch and activate an open doctrine pack, then confirm it participates in context resolution.
doc_status: wip
updated: '2026-07-12'
related:
- docs/guides/compose-packs.md
- docs/guides/index.md
---
# Use a doctrine pack

This guide shows how a Spec Kitty **consumer project** pulls in an open doctrine pack instead
of inheriting the entire built-in corpus. It assumes you already have Spec Kitty installed
(`spec-kitty --version`) and a project initialized (`spec-kitty init`).

> **🚧 WIP.** The open-packs catalog is still being materialized. Until packs are published
> here, use the [org doctrine pack workflow](https://github.com/Priivacy-ai/spec-kitty/blob/main/docs/guides/create-an-org-doctrine-pack.md)
> upstream — the consumer configuration below is the same surface.

## 1. Point your config at the pack

A consumer enables the org layer by adding a `doctrine.org` block to
`.kittify/config.yaml`, listing each pack and pinning a version:

```yaml
# .kittify/config.yaml
doctrine:
  org:
    packs:
      - name: domain-driven-design
        local_path: "${SPEC_KITTY_PACK_HOME}/domain-driven-design"
        source_type: git
        url: "git@github.com:spec-kitty/spec-kitty-open-packs.git"
        ref: "v0.1.0"          # pin a tag or commit SHA — never a moving branch
```

| Field | Required | Purpose |
| --- | --- | --- |
| `name` | yes | Unique pack name (used by `--pack`, shown in `doctor doctrine`). |
| `local_path` | yes | Where the snapshot lives. Supports `~` and `${VAR}` / `$VAR` indirection. |
| `source_type` | no | One of `git`, `https`, `api`. Omit if pre-provisioned. |
| `url` | if `source_type` set | Remote URL. |
| `ref` | no | Version pin (git tag/SHA recommended). |

## 2. Fetch the pack

```bash
spec-kitty doctrine fetch                 # fetch all configured packs
spec-kitty doctrine fetch --pack domain-driven-design   # one pack
spec-kitty doctrine fetch --dry-run       # preview without contacting any remote
```

## 3. Verify the install

```bash
spec-kitty doctor doctrine
```

This enumerates each configured pack, its on-disk version, per-artifact counts, and
`org-charter.yaml` status. Add `--json` for scripting.

## 4. Confirm it participates in resolution

```bash
spec-kitty charter context --action implement --json
```

Resolved artifacts carry a `source` field of `builtin`, `org`, or `project`. Artifacts your
pack contributes appear with `source: org`.

## Why pin, and why opt in

- **Pin versions** so a moving `main` doesn't silently change behaviour for every consumer on
  every fetch.
- **Opt in deliberately.** The entire point of packs is to *avoid* loading doctrine you don't
  need. Add only the packs whose domain matches your project, and constrain further with a
  [charter](https://github.com/Priivacy-ai/spec-kitty/blob/main/docs/guides/charter-governed-workflow.md)
  so context stays lean.

## Next

- [Compose packs](compose-packs.md) — combine several packs, and use compound packs that
  declare `depends_on`.
