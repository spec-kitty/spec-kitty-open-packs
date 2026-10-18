---
title: "Getting started: adopt your first pack"
description: "Adopt your first Spec Kitty Charter Pack end to end: register it, fetch it, activate one rule through the charter, and confirm it is in force. For first-time pack users."
doc_status: wip
updated: '2026-10-17'
related:
- guides
- guides/use-a-charter-pack
- guides/compose-packs
---
# Getting started: adopt your first pack

This tutorial takes you from nothing to a working, activated Charter Pack in under fifteen
minutes. You need no prior knowledge of Spec Kitty packs — follow the five steps in order and
you will have fetched a real pack from this repository, activated one of its rules, and
confirmed the charter is putting it in force.

We use the **`qa`** pack as the example. It is deliberately *inert*: it ships quality-assurance
charter artefacts but activates nothing on its own, so you can adopt it beside your team's existing
charter and turn on exactly the one rule this tutorial activates.

## Before you start

You need:

- **Spec Kitty 4.x** on your PATH. Check with `spec-kitty --version`. If you are on 3.x, run
  `spec-kitty upgrade` first — the `doctrine` commands and config keys were removed in 4.x.
- **An initialized project** — a directory where you have run `spec-kitty init`, so it has a
  `.kittify/` folder.

Everything below runs from the root of that project.

## Step 1 — Tell your project about the pack

Open `.kittify/config.yaml` and register the `qa` pack under `charter_packs.org.packs`. Packs
in this repository are subdirectories of one git repository, so you name the pack's `subdir`
and pin a ref:

```yaml
# .kittify/config.yaml
charter_packs:
  org:
    packs:
      - name: qa
        local_path: "${SPEC_KITTY_PACK_HOME}/qa"
        source_type: git
        url: "https://github.com/spec-kitty/spec-kitty-open-packs.git"
        ref: "<commit SHA or pack/qa/vX.Y.Z tag>"   # pin a tag or SHA, never a branch
        subdir: packs/qa
```

`SPEC_KITTY_PACK_HOME` is any directory you choose to hold fetched packs. Set it once in your
shell:

```bash
export SPEC_KITTY_PACK_HOME=~/.cache/spec-kitty-packs
```

An unset variable fails the fetch in the next step. For the full field reference, see
[Use a Charter Pack](use-a-charter-pack.md).

## Step 2 — Fetch the pack

Pull the pack onto disk at the ref you pinned:

```bash
spec-kitty charter fetch --pack qa
```

Preview first with `--dry-run` if you want to see what would be fetched without contacting the
remote. Omit `--pack` to fetch every pack you have configured.

## Step 3 — Verify the install

```bash
spec-kitty doctor charter-packs
```

This lists the `qa` pack with its on-disk version and per-artifact counts, and reports any
collisions or unsanctioned overrides. A healthy report exits `0`; an unhealthy one exits `1`
and prints the finding. Add `--json` if you want to script the check.

At this point the pack's artefacts are *offered* to your project — but, because `qa` is inert,
nothing is active yet.

## Step 4 — Activate one rule

Turn on a single directive — `QA_001`, "QA Traceability Mandatory":

```bash
spec-kitty charter activate directive QA_001
```

`charter activate KIND ARTIFACT_ID` writes an `activated_<kind>` key into
`.kittify/config.yaml`. (Packs that ship **presets** can instead be activated in bulk with
`spec-kitty charter activate --pack qa --preset <name>`; the `qa` pack ships none, so we
activate the one rule directly.)

## Step 5 — Confirm it is in force

List what your charter now has active:

```bash
spec-kitty charter list
```

`QA_001` appears under the activated directives. To see it resolved in a real action context,
fetch it directly:

```bash
spec-kitty charter context --include directive:QA_001
```

The directive renders with a `source` of `org` — proof that it came from the pack you adopted
rather than from the built-in corpus. That is the whole loop: **registered → fetched →
activated → in force.**

## What you just did

| Step | Command | Result |
| --- | --- | --- |
| Register | edit `.kittify/config.yaml` | The project knows where the pack lives. |
| Fetch | `spec-kitty charter fetch --pack qa` | The pack is on disk at a pinned ref. |
| Verify | `spec-kitty doctor charter-packs` | The pack is offered and healthy. |
| Activate | `spec-kitty charter activate directive QA_001` | One rule is switched on. |
| Confirm | `spec-kitty charter context --include directive:QA_001` | The rule resolves with `source: org`. |

## Next

- [Use a Charter Pack](use-a-charter-pack.md) — the full consumer reference: every config
  field, preset activation, and resolution detail.
- [Compose packs](compose-packs.md) — add several packs at once and see how conflicts resolve.
