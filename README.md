<div align="center">
    <img src="https://github.com/spec-kitty/spec-kitty/raw/main/docs/assets/logo_small.webp" alt="Spec Kitty logo"/>
    <h1>Spec Kitty Open Packs</h1>
    <p><strong>Open, free doctrine packs for Spec Kitty — domain- and purpose-specific behavioural configuration you compose into your own codebase.</strong></p>
</div>

> [!WARNING]
> **🚧 Work in progress — this is a product-direction shift, not a finished repository.**
>
> `spec-kitty-open-packs` is the seed of a **doctrine-packs-as-a-marketplace** direction for
> Spec Kitty. It is being stood up in the open, deliberately early, so the design can be
> shaped in public. Expect churn: pack names, boundaries, the manifest schema, and the
> composition mechanics **will change**. Nothing here is stable or versioned for production
> use yet. Track the direction through the [open epics](#where-this-is-going) and the
> [pack catalog proposal](docs/packs/catalog-proposal.md).

[![License: MIT](https://img.shields.io/badge/license-MIT-yellow?style=flat-square)](LICENSE)
[![Status: WIP](https://img.shields.io/badge/status-work_in_progress-orange?style=flat-square)](#-work-in-progress--this-is-a-product-direction-shift-not-a-finished-repository)
[![Doctrine logic: upstream](https://img.shields.io/badge/doctrine_logic-spec--kitty%2Fspec--kitty-blue?style=flat-square)](https://github.com/spec-kitty/spec-kitty)

## Why this repository exists

[Spec Kitty](https://github.com/spec-kitty/spec-kitty) ships a large, multi-domain set of
**built-in doctrine** — the directives, tactics, styleguides, paradigms, procedures,
toolguides, and agent profiles that shape how AI coding agents behave under governance.

That built-in set is a single monolithic bundle. Spec Kitty's default charter behaviour is
**"activate everything when not explicitly constrained"**, and while every project is guided
to author a charter, doing so is *not enforced* (by design). The consequence: a consumer
project that skips the charter step inherits the whole multi-domain corpus and **floods every
LLM session's context** with doctrine it does not need.

This repository is the answer to that problem. Instead of one monolith, doctrine becomes a
set of **coherent, composable, opt-in packs** that consumers pull in deliberately:

- **Domain / purpose packs** — e.g. a Domain-Driven Design pack, a Java development pack, a
  web/frontend pack, a testing & BDD pack — each a self-consistent slice you can adopt on its
  own.
- **Vertical *and* horizontal composition** — Spec Kitty core today composes doctrine
  *vertically* (built-in → org → project layers). Packs add *horizontal* composition:
  independent packs, and **compound packs** that declare `depends_on` other packs, resolved
  as a DAG.
- **Shared validation** — a single canonical place to validate a pack, so downstream authors
  can lint their work against the same rules instead of each maintaining a bespoke suite.

## Division of responsibility

This repository holds **content and packaging**. The **logic** that makes doctrine work stays
in Spec Kitty core.

| Concern | Lives in |
| --- | --- |
| Doctrine artifacts, packs, compound packs | **this repo** (`spec-kitty-open-packs`) |
| Pack authoring & usage guides | **this repo** (`docs/guides/`) |
| Doctrine mechanics, resolution, DRG, activation engine | [`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty) |
| Pack manifest schema, validator, assembler | [`spec-kitty/spec-kitty`](https://github.com/spec-kitty/spec-kitty) (consumed here) |

Cross-referencing between the two repositories is expected and encouraged. Issues here track
**pack creation**; issues in core track **doctrine functionality and logic**.

## Where this is going

The direction is grounded in these open epics in Spec Kitty core (this repository is the
downstream home for the *content* they enable):

| Epic | What it establishes |
| --- | --- |
| [#2466 — Doctrine/Charter extensibility & pack ecosystem](https://github.com/spec-kitty/spec-kitty/issues/2466) | The umbrella: turn the scattered doctrine substrate into an author-able pack ecosystem. |
| [#2467 — Split built-in doctrine into packs + compound packs (KEYSTONE)](https://github.com/spec-kitty/spec-kitty/issues/2467) | Split the monolith into named packs; give packs a `depends_on` DAG. |
| [#2471 — Standalone pack validator as a lightweight CI entry point](https://github.com/spec-kitty/spec-kitty/issues/2471) | The canonical validation surface authors reuse. |
| [#2539 — Pack trust, verifiability & verified distribution](https://github.com/spec-kitty/spec-kitty/issues/2539) | Provenance, integrity, and a graduated trust signal for packs. |
| [#2519 — Charter authoring & lifecycle robustness](https://github.com/spec-kitty/spec-kitty/issues/2519) | Making the charter that *selects* packs easy and robust to author. |

See the [pack catalog proposal](docs/packs/catalog-proposal.md) for the concrete set of packs
we intend to carve out of the current built-in corpus, and the
[open-packs issue tracker](https://github.com/spec-kitty/spec-kitty-open-packs/issues) for
per-pack progress.

## What a pack looks like

A pack is a directory with one subdirectory per artifact kind — the same canonical layout
Spec Kitty 4.x resolves for org Charter Packs:

```
my-pack/
├── directives/                 # *.directive.yaml
├── tactics/                    # *.tactic.yaml
├── styleguides/                # *.styleguide.yaml
├── toolguides/                 # *.toolguide.yaml
├── paradigms/                  # *.paradigm.yaml
├── procedures/                 # *.procedure.yaml
├── agent_profiles/             # *.agent.yaml
├── presets/                    # <name>.yaml — activation presets
├── drg/fragment.yaml           # additive DRG fragment
└── org-charter.yaml            # optional: policy / required artifacts
```

Artifact directories are optional; every pack ships `drg/fragment.yaml` (empty is fine). Consumers register a pack
under `charter_packs.org.packs` in `.kittify/config.yaml` (git ref plus `subdir`, HTTPS
bundle, or API), pin a version, and validate with `spec-kitty charter pack validate`.

New to packs? Start with the guides. They are also published as the docsite at
**<https://spec-kitty.github.io/spec-kitty-open-packs/>**, built from [`docs/`](docs/index.md) with
[DocKitty](https://github.com/spec-kitty/doc-kitty) (see [ADR-5](docs/architecture/adr/2026-10-10-5-dockitty-docsite.md)).
That site also carries a generated [pack reference](docs/packs/reference/index.md):

- **Usage:** [Use a Charter Pack](docs/guides/use-a-doctrine-pack.md) · [Compose packs](docs/guides/compose-packs.md)
- **Authoring:** [Author a Charter Pack](docs/guides/author-a-doctrine-pack.md) · [Validate a pack](docs/guides/validate-a-pack.md) · [Publish a pack](docs/guides/publish-a-pack.md)

## Status & stability

| Aspect | State |
| --- | --- |
| Repository | Bootstrapping — structure and conventions being established. |
| Pack catalog | **Proposed**, not yet materialized. See the [catalog proposal](docs/packs/catalog-proposal.md). |
| Manifest schema / composition | Defined upstream in core (`#2467`), tracked, subject to change. |
| Validation tooling | Consumed from core (`#2471`); every pack is validated in CI (`scripts/ci/validate-packs.sh`). |
| Docsite | DocKitty site built from `docs/` (`pnpm install && pnpm build`); pack reference generated from `packs/`. |
| Trust / verified distribution | Roadmap only (`#2539`). |

## Contributing

This is an open, community-facing repository. Pack proposals, corrections, and authoring
feedback are welcome — see [CONTRIBUTING](CONTRIBUTING.md) and the
[Code of Conduct](CODE_OF_CONDUCT.md). Because packs can eventually ship executable gate
assets, please read the [security position](SECURITY.md) before proposing code-bearing
artifacts.

## License

[MIT](LICENSE). Doctrine content is free to use, adapt, and redistribute.
