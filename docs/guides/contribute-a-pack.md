---
title: Contribute a pack
description: The path for an outside author who wants to propose a new Charter Pack or change an existing one here, from the proposal issue through identity, gates and review to the release.
doc_status: wip
updated: '2026-11-19'
related:
- guides/contributing
- guides/author-a-charter-pack
- guides/validate-a-pack
- guides/publish-a-pack
- architecture/adr/2026-11-19-3-pin-charter-releases-and-charter-owns-pack-logic
---
# Contribute a pack

This guide is for an author outside the maintainer team who wants to add a Charter Pack to this
repository, or change one that is already here. It covers the intake: how to propose, what you
own, which gates your pull request must pass, and how it is reviewed. The mechanics of writing a
pack are in [Author a Charter Pack](author-a-charter-pack.md) and
[Validate a pack](validate-a-pack.md).

> **The pack contract still changes often.** The pack schemas, file rules and validation belong to
> [`spec-kitty-charter`](https://github.com/spec-kitty/spec-kitty-charter), and this repository
> follows its releases ([ADR 2026-11-19-3](../architecture/adr/2026-11-19-3-pin-charter-releases-and-charter-owns-pack-logic.md),
> epic [#287](https://github.com/spec-kitty/spec-kitty-open-packs/issues/287)). A pin move can
> require changes to every pack, sometimes weekly. Expect your pack to be migrated with the others
> after it lands, and expect a long-open pull request to need a rebase onto a new pin.

## 1. Propose before you author

Open an issue first, and wait until the scope is agreed before you write the pack:

| You want to… | Open |
| --- | --- |
| Add a new pack | a **Pack proposal** issue |
| Change an existing pack (add, fix or remove an artifact) | an **Enhancement / idea** issue |
| Change how packs are validated, resolved or composed | an issue in [`spec-kitty-charter`](https://github.com/spec-kitty/spec-kitty-charter/issues), not here |

Before you file, check the [pack catalog proposal](../packs/catalog-proposal.md) and the
[open issues](https://github.com/spec-kitty/spec-kitty-open-packs/issues): the pack may already be
proposed. A small fix to wording or a broken reference can go straight to a pull request.

## 2. Identity: `pack_id` and `name`

A pack's `pack.yaml` carries two identities. Both are hard to change once other packs or
projects use them.

- **`pack_id`** is a [ULID](https://github.com/ulid/spec). You mint it once, when you create the
  pack, and it never changes after that: not on a rename, not on a move to another repository.
  Never copy another pack's `pack_id`, and never invent one by hand-editing characters.
  Downstream consumers never mint a `pack_id` for a pack they did not create; they use the one the
  pack carries (the project charter's identity discipline).
- **`name`** is the qualifier other packs write in a cross-pack reference (`<name>::<id>`). It
  need not match the directory name.

This repository is the canonical home of the packs under `packs/`, including
`spec-kitty-internal`. A reviewer checks that your `pack_id` and `name` are new. Namespace your artifact ids too; see
[Author a Charter Pack](author-a-charter-pack.md).

## 3. Author and validate locally

Work in a fork. Lay out the pack as [Author a Charter Pack](author-a-charter-pack.md) describes,
then run the checks the required gate runs:

```bash
scripts/ci/validate-packs.sh                      # every pack against the pinned charter schemas
python3 scripts/ci/pack_digest.py --update        # restamp packs/<name>.source.yaml
python3 scripts/ci/check_vocabulary.py            # retired ids and names
python3 scripts/docs/gen_pack_reference.py        # regenerate the docs/packs/ pages
```

Commit what the last three change. The pack pages under `docs/packs/` are generated: never edit
them by hand. [Validate a pack](validate-a-pack.md) explains each check and its output.

When you change an existing pack, bump its `pack_version`. A removed or renamed artifact raises
the major version (DIRECTIVE_018). In this repository's changelog, an added artifact raises the
minor and a wording fix the patch. Some
packs are pinned exactly by others (the `built-in` members), so a bump there moves those pins as
well; the reviewer will tell you if your change does.

## 4. Open the pull request

- Open it from your fork against `main`, and allow edits from maintainers.
- Fill in the [pull request template](https://github.com/spec-kitty/spec-kitty-open-packs/blob/main/.github/PULL_REQUEST_TEMPLATE.md),
  including its **New pack** checklist when you add one, and link the agreed issue.
- Add an entry under `## [Unreleased]` in the [changelog](../changelog/CHANGELOG.md).
- If an AI coding agent wrote much of the change, say so in the description.

GitHub may hold the workflow runs of a first-time contributor until a maintainer approves them.

## 5. The gates

`main` requires one check, **`Validate packs gate`**. It covers pack validation, the charter
service check at the pinned charter release (every pack composed and registered, every invalid
fixture refused), the recorded pack digests, the vocabulary guard, the generated-page drift check
and the tooling tests. **`Docs site`** also runs when docs or packs change; it builds the docsite and
checks its links. See [Contributing: what runs where](contributing.md#what-runs-where).

The project charter treats these gates as fail-closed: a pull request merges only when they are
green.

## 6. Review and landing

A maintainer reviews the pull request against the agreed issue: content fidelity, identity, the
version bump, and whether the change belongs here or in the charter. Maintainers may push fixes
to your branch, and they may rebase it onto a new charter pin. `main` is linear, and pull requests
land by rebase.

The maintainers' landing flow is the `landing-contributor-prs` procedure of the
`spec-kitty-internal` pack. Its steps still name Spec Kitty core's repository and tooling, so
until [#270](https://github.com/spec-kitty/spec-kitty-open-packs/issues/270) makes it
repository-neutral, maintainers land pull requests here as [Contributing](contributing.md)
describes.

## 7. After it lands

Your pack ships in the next repository release: a `vX.Y.Z` tag publishes one reproducible archive
per pack ([Contributing: releases](contributing.md#releases)). Later charter migrations update it
together with the other packs.
