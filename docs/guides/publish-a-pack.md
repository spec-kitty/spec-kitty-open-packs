---
title: Publish a pack
description: Distribute a Spec Kitty Charter Pack via git, HTTPS bundle, or a custom API; version it for reproducibility; and account for the pack trust surface.
doc_status: wip
updated: '2026-10-10'
related:
- guides/validate-a-pack
- guides/use-a-charter-pack
---
# Publish a pack

Once a pack [validates](validate-a-pack.md) cleanly, distribute it so consumers can fetch it.
Spec Kitty's org layer fetches packs over git, HTTPS, Artifactory or a custom API (`source_type`).

## Option A — Git repository (recommended)

Push the pack to a git remote and tag releases. In this marketplace, most open packs live as
directories inside `spec-kitty-open-packs` and are pinned by tag or commit SHA.

```bash
git tag pack/<pack>/v0.1.0
git push origin pack/<pack>/v0.1.0
```

Consumers point at the remote and pin the ref (see [Use a Charter Pack](use-a-charter-pack.md)).

> **Subdirectory packs.** Consumers fetch one pack out of this repository with the `subdir`
> field of their `charter_packs.org.packs` entry (for example `subdir: packs/qa`),
> so a pack does not need its own repository.

## Option B — HTTPS bundle

Upload a tarball to an HTTPS location (object storage, releases page); consumers download and
extract.

```bash
tar czf <pack>-v0.1.0.tar.gz -C ./packs/<pack> .
```

## Option C — Custom HTTP API

For organisations with a governance API server, expose pack contents under a base URL. The
contract is defined in Spec Kitty core's org Charter Pack source-API contract.

## Assemble a compound distributable

To ship several packs as one artifact, assemble them:

```bash
spec-kitty charter pack assemble ./out ./packs/core-engineering ./packs/domain-driven-design
```

The first argument is the output directory; the rest are inputs. Conflicts fail by default;
use `--conflicts-out conflicts.json` to inspect or `--force` for last-pack-wins. The
assembled output is validated before exit.

## Versioning

**Pin versions** in consumer config. Use a git tag or commit SHA; branch names are accepted
but discouraged — a moving target on `main` silently changes behaviour for every consumer on
every fetch.

## Trust & integrity

Publishing a pack that others run is a supply-chain action. As the pack ecosystem matures:

- Packs that ship **executable gate assets** must declare their executable paths/requirements,
  and consumers are warned at activation
  ([core #2536](https://github.com/spec-kitty/spec-kitty/issues/2536),
  [#2542](https://github.com/spec-kitty/spec-kitty/issues/2542)).
- **Content-hash integrity / tamper-evidence** and a graduated trust signal
  (built-in / org-pack / third-party / verified) are on the roadmap
  ([core #2539](https://github.com/spec-kitty/spec-kitty/issues/2539)).

Read the [security position](../../SECURITY.md) before publishing a code-bearing pack.

## Next

- [Use a Charter Pack](use-a-charter-pack.md) — the consumer side of what you just published.
