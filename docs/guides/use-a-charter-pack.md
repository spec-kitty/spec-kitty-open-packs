---
title: Use a Charter Pack
description: Configure a Spec Kitty 4.x consumer project to fetch an open Charter Pack, activate it, and confirm it participates in context resolution.
doc_status: wip
updated: '2026-10-20'
related:
- guides/compose-packs
- guides
---
# Use a Charter Pack

This guide shows how a Spec Kitty **consumer project** pulls in an open Charter Pack instead
of inheriting the entire built-in corpus. It assumes Spec Kitty 4.x with the Charter Pack
cutover (`spec-kitty charter pack validate --help` works) and an initialized project
(`spec-kitty init`).

> **Spec Kitty 3.x?** The `spec-kitty doctrine …` commands and the `doctrine.org` config key
> were removed in 4.x without aliases. Run `spec-kitty upgrade` once and follow the
> [Charter Pack cutover runbook](https://github.com/spec-kitty/spec-kitty/blob/main/docs/migrations/charter-pack-cutover.md).

## 1. Point your config at the pack

Register each pack under `charter_packs.org.packs` in `.kittify/config.yaml`. Packs in this
repository live in subdirectories of one git repository, so name the pack's directory with
`subdir` and pin a ref:

```yaml
# .kittify/config.yaml
charter_packs:
  org:
    packs:
      - name: qa
        local_path: "${SPEC_KITTY_PACK_HOME}/qa"
        source_type: git
        url: "https://github.com/spec-kitty/spec-kitty-open-packs.git"
        ref: "<vX.Y.Z release tag or commit SHA>"   # never a branch
        subdir: packs/qa
```

`SPEC_KITTY_PACK_HOME` is any directory you choose for fetched packs (for example
`export SPEC_KITTY_PACK_HOME=~/.cache/spec-kitty-packs`); an unset variable fails the fetch.

| Field | Required | Purpose |
| --- | --- | --- |
| `name` | yes | Unique pack name (used by `--pack`, shown in `doctor charter-packs`). |
| `local_path` | yes | Where the snapshot lives. Supports `~` and `${VAR}` / `$VAR` indirection. |
| `source_type` | no | One of `git`, `https`, `artifactory`, `api`. Omit if the pack is already on disk. |
| `url` | if `source_type` set | Remote URL. |
| `ref` | no | Version pin (git tag or SHA recommended). |
| `subdir` | no | The pack's directory inside the fetched source, for multi-pack repositories. |

Only this named-list form is read. A single-pack `charter_packs.org.local_path` is ignored.

## 2. Fetch the pack

```bash
spec-kitty charter fetch                              # fetch all configured packs
spec-kitty charter fetch --pack qa                    # one pack
spec-kitty charter fetch --dry-run                    # preview without contacting any remote
```

## 3. Verify the install

```bash
spec-kitty doctor charter-packs
```

This lists each configured pack with its artifact counts and `org-charter.yaml` status, and
reports collisions between layers and dangling DRG endpoints. Add `--json` for scripting.

## 4. Activate what you want

A pack contributes artifacts to the charter offering; your project decides what is active.
If the pack ships activation presets, list and apply them:

```bash
spec-kitty charter pack list                                  # packs and their presets
spec-kitty charter activate --pack <pack> --preset <preset>
```

A preset writes ordinary `activated_<kind>` keys into `.kittify/config.yaml`; edit them
afterwards as you like. A pack's `org-charter.yaml` can also put artifacts in force through
its `required_*` lists.

## 5. Confirm it participates in resolution

```bash
spec-kitty charter context --action implement --json
spec-kitty charter context --include directive:<ID>
```

Resolved artifacts carry a `source` of `builtin`, `org`, or `project`. Artifacts your pack
contributes appear with `source: org`.

## Why pin, and why opt in

- **Pin versions** so a moving `main` doesn't silently change behaviour for every consumer on
  every fetch. Each `vX.Y.Z` release also publishes every pack as a reproducible
  `<pack>-vX.Y.Z.tar.gz` with a `.sha256`, so you can pin and verify the archive digest
  instead of fetching the repository. Release tags are never moved.
- **Opt in deliberately.** The point of packs is to *avoid* loading charter artefacts you don't need.
  Add only the packs whose domain matches your project, and activate only what you use, so
  context stays lean.

## Next

- [Compose packs](compose-packs.md) — combine several packs, and see how collisions resolve.
