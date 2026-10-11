---
title: Contributing to Spec Kitty Open Packs
description: How to propose, author, and submit doctrine packs and documentation to the Spec Kitty Open Packs repository, including the WIP status and where doctrine logic lives.
doc_status: active
updated: '2026-10-11'
type: Guide
kind: How-To
related:
- guides/author-a-doctrine-pack
- guides/validate-a-pack
external_references:
- url: https://github.com/spec-kitty/spec-kitty-open-packs/blob/main/README.md
  title: README.md
---
# Contributing to Spec Kitty Open Packs

Thanks for your interest. This repository distributes **open, free doctrine packs** for
[Spec Kitty](https://github.com/spec-kitty/spec-kitty). It is deliberately **early and
in-the-open** — a product-direction shift toward doctrine-packs-as-a-marketplace. Conventions
here will change; contributions that help shape them are welcome.

## What belongs here vs. in core

| You want to… | Contribute to |
| --- | --- |
| Propose or author a doctrine pack | **this repository** |
| Improve a usage or authoring guide | **this repository** |
| Change how doctrine is resolved, validated, or composed | [`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty) |
| Change the pack manifest schema or the validator | [`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty) |

If you are unsure, open an issue here first and we will help route it. Cross-referencing
between the two repositories is expected.

## Proposing a pack

1. Check the [pack catalog proposal](../packs/catalog-proposal.md) and the
   [issue tracker](https://github.com/spec-kitty/spec-kitty-open-packs/issues) — the pack you
   have in mind may already be proposed or in progress.
2. Open an issue using the **Pack proposal** template. Describe the pack's purpose, the
   artifacts it would contain (ideally referencing existing built-in artifacts), any
   `depends_on` packs, and the intended consumer.
3. Once the scope is agreed, author the pack following
   [Author a Charter Pack](author-a-doctrine-pack.md).

## Authoring standards

- **Namespace your IDs.** Use an organisation/pack prefix so IDs don't collide silently with
  built-in or project doctrine. See the authoring guide for the recommended patterns.
- **One rule per file.** Resist dumping a whole policy page into a single artifact — split so
  each rule can be cited individually.
- **Validate before you push.** Run the canonical validator (see
  [Validate a pack](validate-a-pack.md)). Packs must pass with exit code `0`.
- **Keep it inert where possible.** Prefer data-only artifacts. If a pack must ship an
  executable gate asset, read the [security position](../../SECURITY.md) first and declare
  the executable surface explicitly.

## Documentation conventions

Docs follow the [DocKitty convention](https://github.com/spec-kitty/doc-kitty/blob/main/docs/context/convention.md)
and are published with `@spec-kitty/doc-toolkit` (see [ADR-5](../architecture/adr/2026-10-10-5-dockitty-docsite.md)):
Markdown with YAML frontmatter (`title`, `description` of at most 180 characters, `doc_status` —
`draft` | `active` | `deprecated` | `superseded` | `durable` — `updated`, `type`, `kind`, optional
`related` as docs-root-relative slugs such as `guides/validate-a-pack`), an `index.md` per section,
nav order and section labels in [`docs/_meta/charter.yaml`](../_meta/charter.yaml), and a canonical
changelog under `docs/changelog/` symlinked from the repository root. Pages under
`docs/packs/reference/` are generated — never edit them; run
`python3 scripts/docs/generate_pack_reference.py` instead. Build the site locally with
`pnpm install && pnpm build`, and run `pnpm docs:validate` and `pnpm docs:links` before you push.
The toolkit installs from GitHub Packages, which needs a classic personal access token with
`read:packages` in your user-level `~/.npmrc` (`//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}`);
the repository's `.npmrc` already maps the `@spec-kitty` scope.

## Code of Conduct

All participation is governed by the [Code of Conduct](../../CODE_OF_CONDUCT.md).

## AI-assisted contributions

Contributions authored with AI coding agents are welcome — this is a Spec Kitty repository.
Please review generated content for correctness and disclose substantial AI assistance in
your PR description.
