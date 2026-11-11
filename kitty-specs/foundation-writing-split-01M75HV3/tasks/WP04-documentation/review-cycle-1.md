---
affected_files: []
cycle_number: 1
mission_slug: foundation-writing-split-01M75HV3
reproduction_command:
reviewed_at: '2026-11-11T16:56:32Z'
reviewer_agent: claude-reviewer-subagent
wp_id: WP04
---

# Review: WP04 Documentation (foundation-writing-split-01M75HV3, #73)

Commit under review: `6f79870` "docs: record the built-in split, its bundles and the migration (#73)"
in `.worktrees/foundation-writing-split-01M75HV3-lane-d`, diffed against `65d7dae`.

## Verdict: REJECT

The ADR is accurate and the generated pages are clean. Two defects in the CHANGELOG block approval:
- The Breaking entry appears twice.
- The root `CHANGELOG.md` symlink was replaced by a regular file.

Several pages that research/4-gates.md listed for update also still say that every org pack depends on built-in, or that built-in is one pack.

## Findings

### HIGH-1: The 💥 Breaking entry is duplicated
`docs/changelog/CHANGELOG.md` lines 24-66 and 69-111 contain the same "`built-in` split into `foundation`, `writing` and ten opt-in bundles" entry, word for word, both added by this commit. `grep -c 'split into \`foundation\`'` returns 2. Delete one copy.

### HIGH-2: The root `CHANGELOG.md` symlink was replaced by a regular file
- `git diff HEAD^ HEAD --summary` reports `mode change 120000 => 100644 CHANGELOG.md`. The parent tree had `CHANGELOG.md -> docs/changelog/CHANGELOG.md`, and research/4-gates.md says "root and `.github/` are symlinks". `.github/CHANGELOG.md` is still a symlink.
- The two files are byte-identical today, but that is a copy, not the single source the repo had before. They will drift on the next edit, and `scripts/release/release_assets.py` reads the root `CHANGELOG.md` for release notes.
- As a regular file at the repo root, every `../architecture/...` and `../guides/...` link in it now points outside the repo. The new ADR link is one of them, and so are the older entries at lines 138 and 141.
- Fix: restore the symlink (`git checkout HEAD^ -- CHANGELOG.md` after fixing the docs copy). The link path `../architecture/adr/2026-11-11-1-...md` is correct for `docs/changelog/CHANGELOG.md` and follows the existing convention.

### MEDIUM-1: Stale claims that research flagged are still in docs
- `docs/glossary/index.md:23`: "Every org pack here depends on `built-in`". This is exactly the stale phrase. No org pack depends on built-in any more; each depends on foundation, writing or a bundle. research/4-gates.md:174 lists `docs/glossary/index.md`.
- `docs/architecture/overview.md:56`: "**Built-in** — `pack_level: built-in`. One pack, shipped with the CLI." There are now three built-in-level packs.
- `docs/architecture/overview.md:89-94`, "Where built-in content comes from": "`packs/built-in/` is authored here … core fetches the pack from it". It does not say that built-in now holds nothing and that the members must be fetched at the same pin. The ADR and CHANGELOG say this; the overview does not. The table row at :23 has the same problem. research/4-gates.md:173 lists all of these lines.
- `packs/README.md:3-7`: "It ships four packs so far, cave-kitty, event-driven, qa and spdd; the rest of the catalog is still a proposal, carved from the Spec Kitty built-in corpus incrementally". This is false now: 12 more packs ship (and `internal`). The commit rewrote the later paragraph (:31-38) but missed this one, which research flagged at `packs/README.md:3-6`.

### MEDIUM-2: The CHANGELOG does not tell consumers of the rewired org packs what they must now register
The entry says `internal`, `qa`, `event-driven`, `spdd` and `cave-kitty` "were rewired and bumped to 1.1.0". It does not say what a consumer of `qa` or `event-driven` must now place.
- `qa` 1.1.0 now `depends_on` foundation, planning-analysis and testing. Through planning-analysis it also pulls in architecture, adversarial-review, refactoring and writing.
- `event-driven` depends on architecture, and through it on refactoring, testing, adversarial-review, writing and foundation.

A consumer who registered only `qa` gets `pack_dependency_unknown`. That is a consumer-visible break (a new required dependency in a minor bump), so it belongs in the "It breaks for" list. Add a migration step: "register each pack in the `depends_on` closure of the org packs you use".

Smaller points on the migration steps:
- Step 3 says to depend on "the packs you actually reference, ranged `>=1.0,<2`" but does not say that `depends_on` takes the `pack_id` ULID, or where to find it (`packs/<name>/pack.yaml`).
- Step 5 says "re-add it through its bundle", but annie's DIRECTIVE_047 edge ships with `writing`, a built-in member, not a bundle (membership.json `body_reference_fixes`). It is harmless, because writing comes with built-in, but the step should say "bundle or member".

The other steps work: place the members at the same commit, rewrite `built-in::` (membership.json is the map), and register the bundles.

### MEDIUM-3: The ADR does not follow the template structure that every sibling ADR uses
`adr-template.md` and all five ADRs from 2026-10 and 2026-11 have the following. The new ADR has none of them:
- `**Chosen option:** "…", because …`
- `### Consequences` split into `#### Positive / #### Negative / #### Neutral`
- `### Confirmation`
- `## Pros and Cons of the Options`

Instead it uses `Chosen option: **2**` and Good/Bad/Neutral bullets. The rejected options 1 and 3 get no pros and cons beyond the squad bullets. Restructure the ADR to the template.

Two smaller points:
- The file name differs from WP04 `create_intent` (`…-split-built-in-into-foundation-and-writing.md`). This is acceptable, because the index links the actual name.
- It is indexed correctly in `docs/architecture/adr/index.md`.

### LOW-1: The ADR's pack table shows a transitive reduction under a `depends_on` heading
The table header says `depends_on`, but several rows omit `foundation`, which every one of these `pack.yaml` files lists explicitly:
- refactoring is shown as "testing", but the file has foundation and testing.
- architecture is shown as "refactoring, adversarial-review, writing", with foundation omitted.
- planning-analysis and adversarial-review omit foundation in the same way.

Either list the real entries, or rename the column to "builds on (direct, reduced)". Every other row matches `packs/*/pack.yaml` and membership.json `depends_on`.

### LOW-2: Leftover singular "built-in pack" wording in contracts
- `docs/contracts/index.md:125`: "the built-in pack's `<kind>.graph.yaml` shards". Built-in now ships none; line 31, which this commit fixed, says "built-in-level packs".
- `:64`: the `--regenerate-manifest packs/built-in` example now restamps an empty manifest. Consider `packs/foundation`.

### LOW-3: Org pack READMEs (probably WP03-owned, outside WP04 `owned_files`)
`packs/event-driven/README.md:30-33` says "The DRG fragment links to the built-in `domain-event-capture` and `anti-corruption-layer` tactics … `domain-driven-design` …". These now live in `architecture`, and the fragment references `architecture::`. Fix it here or note it for WP03.

## Checks that passed

- **ADR facts against the tree:**
  - Levels: foundation and writing are built-in; the ten bundles are org.
  - `built-in` 2.0.0 depends on foundation and writing at `==1.0.0` and keeps `fallback_profile: generic-agent`.
  - The rewired packs are at 1.1.0. The manifests are on built-in, foundation and writing only.
- **ADR counts:**
  - 398 nodes: membership has 399 entries minus one non-node file.
  - 110 relocated edges, matching spec.md:102 and E-synthesis:124.
  - 33 hollow how-tos and about 9 repoints, matching research.md:102-103.
  - internal gets four artifacts, and qa gets `sonar`.
- **The four body-reference drops** (annie→DIRECTIVE_047, daisy→USE_C4_MODEL_TECHNIQUES, ivan→test-first-bug-fixing, renata→adversarial-squad-deployment) match `body_reference_fixes`.
- **Service folds:** five dropped edges and `template:glossary-template` moved writing→architecture, matching `service_check_folds` exactly.
- **The java question** is presented as open, needing a charter ADR (C-004 satisfied).
- **Core's fetch-alone consequence** is recorded as out of scope, per AGENTS.md.
- **#182 manifest guard:** `unlisted_constituents` exists in `validate_pack_schemas.py`, and git-flow and execution-lanes are listed in the foundation manifest.
- **Generated pages:**
  - `CHARTER_CONTRACT_DIR=… gen_pack_reference.py --check` reports "No drift: 18 pack page(s) up to date".
  - Every `packs/*` directory has a `docs/packs/<name>.md` page, and each is linked from `docs/packs/index.md`.
  - `check_vocabulary.py` reports 0 findings.
- **Frontmatter:**
  - All 28 changed or new pages under `docs/` have title, description, doc_status and updated.
  - Every `related:` slug resolves to an existing page.
  - The new pack pages match their generated siblings exactly (kind: Reference, the same related set, generated by/at).
  - The ADR frontmatter matches the 2026-11-04-1 sibling.
  - No sibling uses `audience:`, so its absence is consistent.
- **Remaining "built-in" uses that are acceptable** (they mean the distribution or the level):
  - "built-in corpus" in packs/index.md:38, use-a-charter-pack.md:13, getting-started.md:115, author-a-charter-pack.md:207, event-driven README:72 and the historical catalog-proposal.
  - compose-packs.md:110, "built-in graph state".
  - glossary :22/:25/:26.
  - The internal README and pack.md mentions of the public built-in, including "moved from built-in by #73".
  - organisations :71-74 (preset paths that are still real).
  - The `built-in::` examples in ADR 2026-11-04-1, which is a historical ADR.
- **New pack READMEs** exist for all twelve new packs (FR-014).

## Required to approve

1. Remove the duplicate Breaking entry (HIGH-1).
2. Restore `CHANGELOG.md` as a symlink to `docs/changelog/CHANGELOG.md` (HIGH-2).
3. Fix the stale lines in docs/glossary/index.md:23, docs/architecture/overview.md (:23, :56, :89-94) and packs/README.md:3-7 (MEDIUM-1).
4. Add the dependency-closure break for qa, event-driven, spdd, cave-kitty and internal consumers, with a matching migration step (MEDIUM-2).
5. Restructure the ADR to the template (MEDIUM-3).

The LOW items can be fixed in passing or deferred.
