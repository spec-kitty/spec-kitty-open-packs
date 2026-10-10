---
title: Blockers & core dependencies
description: 'Missing Spec Kitty core functionality blocking a content-from-code, checksum-tagged docsite: capability-to-epic map, ranked blockers, cross-references.'
doc_status: active
updated: '2026-07-18'
type: Context
kind: Explanation
related:
- research
- research/docsite-feasibility-and-generator
- architecture/adr/2026-07-18-3-build-time-checksum-tagging
external_references:
- url: https://github.com/spec-kitty/spec-kitty-open-packs/blob/main/README.md
  title: README.md
---
# Blockers & core dependencies

> Research capture, 2026-07-18. Read-only investigation of `spec-kitty-open-packs` and the core
> tracker/codebase (`Priivacy-ai/spec-kitty`). Issue states verified at time of writing. Feeds
> [ADR-3 (build-time checksum tagging)](../architecture/adr/2026-07-18-3-build-time-checksum-tagging.md)
> and the open-packs docsite epic.

## Ground truth from the code (not just tickets)

- **`packs/` is empty.** It contains only `README.md`. Zero materialized packs; the 16 base + 4
  compound packs in [`catalog-proposal.md`](../packs/catalog-proposal.md) are proposed, not authored.
- **Built-in doctrine is still a monolith.** `src/doctrine/directives/built-in/` is one flat tree
  of `*.directive.yaml`; no named-pack split exists on disk.
- **The validator logic exists and works** (`src/specify_cli/doctrine/pack_validator.py`,
  reachable via `spec-kitty doctrine pack validate`), **but lives under the `specify_cli`
  namespace** — consuming it means depending on the whole CLI package, not a lightweight library.
- **The manifest has no version/dependency notion.** `OrgPackConfig`
  (`src/doctrine/drg/org_pack_config.py`) has `name, local_path, subdir, source_type, url, ref` —
  **no `pack_id`, no `version`, no `depends_on`**; `PackRegistry` is a flat unique-name list.
- **No pack-level checksum/integrity code exists.** The only sha256 usage
  (`src/doctrine/versioning.py`) hashes individual artifact content for *doctrine artifact
  versioning* — unrelated to pack distribution integrity.

## Capability → core dependency map

| Capability the docsite/checksum direction needs | Exists in core today? | Planned where | Verdict |
| --- | --- | --- | --- |
| **Stable pack manifest schema** (`pack_id`/`version`/`depends_on[]`, DAG) | No — `OrgPackConfig` has no version/DAG; built-in unsplit | **#2467** (KEYSTONE, open) under umbrella **#2466** | **Planned, not landed** |
| **Pack validator as a reusable surface** | Partly — logic exists, but coupled inside `specify_cli`; not standalone-installable | **#2471** (open, depends #2467) — extract to dependency-light package + `doctrine-validate` CI entry | **Logic exists; consumable surface is a gap** |
| **Checksum/integrity tagging + verified distribution** | No pack-level mechanism | **#2543** (open, P3) content-hash integrity; epic **#2539**; siblings **#2542** (SBOM), **#2544** (hosted "SK verified"), anchor **#2540** (executable-asset baseline) | **Genuine gap; narrowly scoped to executable assets** |
| **Charter authoring that selects packs** | Activate/deactivate + cascade exists; version-pinned selection needs #2467 | **#2519** (open epic) charter robustness; **#2536** exec-asset activation warning | **Partially exists; not a docsite blocker on its own** |
| **Docsite tooling / pipeline pattern** | Core runs DocFX+Pages for its *own* site | **#2314** (core docsite epic); doc-coverage **#2053**, **#2352** | **Reusable pattern; none targets an open-packs docsite** |

**Scope-mismatch caveat on checksums:** #2543 ties its integrity work to the *executable-gate-asset*
trust envelope (built on #2540). The open-packs goal is **checksum-tagging for verifiable
distribution of content-only packs** (most of the 16 proposed packs ship no executable code). That
need sits *between* #2467 (which would carry `pack_id`/`version`) and #2543 (executable-asset
tamper-evidence) and is **not cleanly owned by either** — the basis for candidate core ticket #2 below.

## Blockers, ranked hard → soft

1. **[HARDEST — prerequisite] No materialized packs.** A content-from-code docsite has no content
   to render until at least one pack is authored. **Can start now** — the current flat org-pack
   layout is already valid input to `validate_pack()`; authoring need not wait for #2467.
2. **[HARD — prerequisite for checksum] Manifest schema incomplete and explicitly unstable.** No
   `pack_id`/`version`/`depends_on` (#2467 not landed). A checksum can't be meaningfully *bound* to
   a stable identity/version, and compound `depends_on` can't be expressed. Upstream in core.
3. **[HARD — the checksum ask itself] No checksum/integrity mechanism exists.** #2543 is unstarted,
   P3, and framed around executable-asset trust. "Checksum-tagged packs" has no owning
   implementation today. Prerequisite for the integrity half of the goal.
4. **[MEDIUM — parallelizable] Validator not consumable standalone.** Works only inside
   `specify_cli` (#2471 not landed). **Interim path:** shell out to an installed
   `spec-kitty doctrine pack validate` in CI now; swap to `doctrine-validate` when #2471 lands.
5. **[SOFT — parallelizable] No open-packs docsite ticket / pipeline wiring.** Core's #2314
   DocFX+Pages pattern is reusable but not wired here, and no issue tracks it. Pure setup; not
   blocked by core code.

**Sequencing:** blocker #1 gates everything renderable. #2 (#2467) gates *stable* checksum tagging
(#3). #4 and #5 proceed in parallel with interim workarounds. The interim checksum decision
([ADR-3](../architecture/adr/2026-07-18-3-build-time-checksum-tagging.md)) deliberately sidesteps
#2/#3 by generating open-packs' own content hash now, pending core's canonical scheme.

## Cross-reference recommendations

**New open-packs docsite ticket(s) should cross-reference:**

- **#2314** — reuse the core DocFX + GitHub Pages deploy/freshness-gate pipeline pattern.
- **#2053 / #2352** — doctrine/charter doc coverage already planned/partly written in core; link,
  don't duplicate.
- **#2467** — the manifest schema the docsite renders "from code"; content must track it as it changes.
- **#2471** — the validator surface the docsite documents and the CI gate consumes.
- **#2539 / #2543** — the checksum/verified-distribution direction the checksum story depends on.

**A new open-packs checksum ticket should cross-reference:** **#2543**, **#2539**, **#2540**,
**#2542**, **#2544**.

## Candidate NEW core tickets — REQUIRES HiC APPROVAL, not filed

Per the governance boundary, **no new tickets are filed in `spec-kitty` core without HiC
approval.** These are drafted for HiC review only:

1. **REQUIRES HiC APPROVAL — do not file:** *"Publish the extracted pack validator (#2471) as a
   pip-installable, dependency-light package + `doctrine-validate` console script consumable by
   external repos (e.g. spec-kitty-open-packs CI)."* — Rationale: #2471 extracts the module, but
   open-packs needs a *distributable, version-pinnable* artifact; today `validate_pack` is only
   reachable inside `specify_cli`. Confirm #2471's deliverable includes a published surface, or
   this needs its own ticket.
2. **REQUIRES HiC APPROVAL — do not file:** *"Pack manifest records `pack_id` + `version` +
   aggregate content checksum for content-only packs, independent of the executable-asset trust
   envelope."* — Rationale: #2543's integrity work is scoped under executable-gate-asset trust
   (#2540); checksum-tagging for the majority content-only packs falls between #2467 and #2543 and
   has no clear owner.
3. **(open-packs repo, not core)** *"Stand up a content-from-code docsite for
   spec-kitty-open-packs, reusing core #2314's DocFX/Pages pipeline."* — This belongs in the
   open-packs tracker (created as part of this work), cross-referencing core #2314/#2053/#2352.
