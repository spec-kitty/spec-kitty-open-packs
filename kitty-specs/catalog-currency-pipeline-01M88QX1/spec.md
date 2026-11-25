# Mission Specification: Routing catalog currency pipeline

**Mission Branch**: `kitty/mission-catalog-currency-pipeline-01M88QX1` (targets `feat/catalog-currency-pipeline`)
**Created**: 2026-11-25
**Status**: Draft
**Input**: #315, grounded in [research.md](research.md) (operator rulings 2026-11-24 and 2026-11-25, relayed by the dispatcher)

## Intent Summary

- **Primary actor:** the pack maintainer who reviews catalog changes. The secondary actor is the
  scheduled run that proposes them.
- **Trigger:** a weekly schedule (Monday, early UTC), or a maintainer starting a run by hand.
- **Desired outcome:** when an approved public source shows that a price in the default routing
  catalog has changed, the maintainer receives **one** pull request. It holds the corrected prices,
  every derived file the change requires, citations to the provider's own documentation, and a list
  of anything a person must judge (source disagreements, deprecations, retirements, new entries).
  When nothing changed, nothing happens.
- **Invariant:** the run never merges, approves or auto-merges. A person reviews every catalog
  change. Editorial judgment (task fit, tiers, strengths, routing policy) is never written by the run.
- **Boundary:** this repository holds the run (charter ADR-0080 decision 14). The charter holds no
  pipeline. Benchmarks are out of scope for v1.
- **Sequencing:** the spec is committed now. Plan and implementation wait until the open-packs
  pack-doctor alignment mission has landed, because both touch the pin tooling.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A price change arrives as one reviewable pull request (Priority: P1)

A provider changes the price of an entry the catalog holds. In the next weekly run, the primary
source shows the new price. The maintainer finds one pull request that corrects the price and
carries every derived change: the foundation pack version and the pins on it, manifests, digests,
pack pages and a changelog entry. It cites the provider's documentation, and it passes every
open-packs gate. The maintainer checks the citation and merges by hand.

**Why this priority**: this is the whole point of #315: a catalog that stays current without
anyone polling providers by hand.

**Independent Test**: point the run at a source fixture whose price for one catalog entry differs
from the catalog. Exactly one pull request is proposed, the change is limited to that value and its
derived files, and every repository gate passes on it.

**Acceptance Scenarios**:

1. **Given** the catalog states an input price of 15 for an entry, **When** the primary source states 18 for the same entry, **Then** one pull request changes only that value (plus provenance and derived files) to `18`.
2. **Given** an open currency pull request, **When** a later run finds a further difference, **Then** that pull request is replaced, not joined by a second one.
3. **Given** a proposed pull request, **When** a maintainer inspects it, **Then** nothing in the run can merge it, approve it or turn on auto-merge.

---

### User Story 2 - No change, no noise (Priority: P1)

Most weeks nothing changes. The maintainer should not hear from the run at all.

**Why this priority**: a weekly job that produces noise gets ignored or switched off.

**Independent Test**: run against a source fixture that agrees with the catalog. No pull request,
issue, branch or commit is created, and the catalog file is byte-identical.

**Acceptance Scenarios**:

1. **Given** sources that agree with the catalog, **When** the run completes, **Then** nothing is created and the catalog is unchanged byte for byte.
2. **Given** the catalog writes a price as `15.0`, **When** the source states `15`, **Then** this counts as no change and `15.0` is left as written.

---

### User Story 3 - Judgment calls reach the reviewer, never get decided by the run (Priority: P2)

The primary source and the cross-check disagree, or a source shows a catalog entry deprecated or
retired, or the catalog's provider ships a new entry. The reviewer needs to see this, but the run
must not decide it.

**Why this priority**: these are the cases where an automated edit would be wrong. They must be
visible, not acted on.

**Independent Test**: fixtures with a disagreement, a deprecation and a new entry. The pull request
body lists each one, and the catalog's entries and editorial fields are untouched.

**Acceptance Scenarios**:

1. **Given** the primary source and the cross-check state different prices, **When** a pull request is proposed, **Then** its body names both values and their sources, and the run adopts neither the cross-check's value nor a compromise.
2. **Given** a source marks a catalog entry deprecated, **When** a pull request is proposed for any reason, **Then** the deprecation is listed in its body and the entry stays in the catalog.
3. **Given** only availability findings and no price difference, **When** the run completes, **Then** the findings are still surfaced to the maintainer (see FR-012) without editing the catalog.

---

### User Story 4 - A broken source fails loudly, once (Priority: P2)

A source moves, changes shape or cannot be reached.

**Independent Test**: a fixture that cannot be parsed. One red issue is opened (or the open one is
rewritten), and no pull request or branch is created.

**Acceptance Scenarios**:

1. **Given** the primary source cannot be parsed, **When** the run completes, **Then** one issue names the source and the error, and no partial pull request exists.
2. **Given** a red issue is open, **When** a later run reads every source cleanly, **Then** the issue is closed.

### Edge Cases

- A source states a price per token instead of per 1M tokens: the conversion is exact (no binary floating point).
- A source states a price with more digits than the catalog uses: the catalog value is written exactly as the source states it, after scaling, in the convention of C-007.
- The source's currency differs from the catalog's `currency`: reported for review, never converted.
- A catalog entry is missing from the primary source: reported for review. It is never treated as a retirement and never removed.
- A pull request for the same difference was closed unmerged: the same difference is not proposed again until the sources change further.
- The run is started from a fork, a pull request or a branch other than `main`: it reports only and creates nothing.

## Domain Language

| Canonical term | Meaning | Avoid |
| --- | --- | --- |
| catalog | `packs/foundation/routing_catalogs/default.routing-catalog.yaml` | "routing table", "model list" |
| entry | one item of the catalog's `models[]` | (no model names in this mission's artifacts) |
| primary source | models.dev, read at a pinned commit | "the API" |
| cross-check | LiteLLM's price map | "secondary source of truth" |
| authority | the provider's own documentation, cited and never scraped | "docs scraper" |
| currency pull request | the one pull request a run proposes | "bump PR" (that is the charter track's) |
| editorial field | `task_fit`, `confidence`, `rationale`, `strengths`, `weaknesses`, `cost.tier`, `latency_tier`, `routing_policy`, `task_types` | — |

## Requirements *(mandatory)*

### Functional Requirements

| ID | Title | User Story | Priority | Status | Delivery | No-op passable? |
|----|-------|------------|----------|--------|----------|-----------------|
| FR-001 | Weekly and on-demand runs | As a maintainer, I want the run to start every Monday early UTC and on manual dispatch, and to act only on `main` of this repository, so that the catalog is checked weekly without forks or pull requests creating anything. | High | Open | [build] | no |
| FR-002 | Approved sources only | As a maintainer, I want the run to read models.dev at a pinned commit as the primary source and LiteLLM's price map as the cross-check, and no other source, so that only operator-approved feeds shape the catalog. | High | Open | [build] | no |
| FR-003 | Price comparison | As a maintainer, I want the input price, output price (per 1M tokens) and currency of every catalog entry compared with the primary source, so that a price change is detected. | High | Open | [build] | no — paired with the no-change fixture of FR-004 |
| FR-004 | Silent no-change run | As a maintainer, I want a run whose sources agree with the catalog to create no pull request, issue, branch or commit, so that I hear from it only when something changed. | High | Open | [build] | yes — paired with FR-003's price-change fixture on the same catalog |
| FR-005 | One complete currency pull request | As a maintainer, I want a difference to produce one pull request that edits the changed prices, updates the source provenance (`sources[]` snapshot and revision, `generated_at`), bumps foundation's `pack_version` (patch), moves the exact pins on it, re-derives manifests, digests and pack pages, and adds a changelog entry; its branch name is derived from the difference (e.g. `catalog/currency-<diff-hash>`) so a superseding run replaces it. | High | Open | [build] | no |
| FR-006 | Citations and disagreements | As a reviewer, I want the pull request body to cite the provider's documentation for each changed value and to list every disagreement between models.dev and LiteLLM with both values, so that I can verify each change. Disagreements between models.dev and LiteLLM are never auto-resolved. | High | Open | [build] | no |
| FR-007 | Supersede, never stack | As a maintainer, I want a newer difference to replace an open currency pull request, and a difference whose pull request was closed unmerged not to be re-proposed until the sources change again, so that at most one currency pull request is open. | Medium | Open | [build] | no |
| FR-008 | Fail closed on a bad source | As a maintainer, I want a source that cannot be fetched or parsed to open (or rewrite) one red issue naming the source and the error, with no partial pull request, and a later clean run to close that issue. | High | Open | [build] | no |
| FR-009 | Gates pass | As a maintainer, I want every currency pull request to pass every open-packs gate at the charter pin (pack validation and cross-pack, charter service and pack-check, vocabulary, pack reference, digests), so that review is about content only. | High | Open | [build] | no |
| FR-010 | Never merges itself | As a maintainer, I want the run unable to merge, approve or enable auto-merge on any pull request, so that a person reviews every catalog change. | High | Open | [build] | yes — proven by a property test over the workflow, not by a run |
| FR-011 | Availability is report-only | As a reviewer, I want deprecations, retirements, entries missing from the source, and new entries from a provider the catalog holds listed in the pull request body, and never added to or removed from the catalog, so that editorial judgment stays with people. (Decision DM-01M88QXFN26B71FTDHQP954KDN: option A.) | High | Open | [build] | no |
| FR-012 | Availability findings without a price change | As a maintainer, I want availability findings that arrive with no price difference reported in the run's summary and on one standing issue (not a pull request), so that they are seen without an empty catalog change. | Medium | Open | [build] | no |
| FR-013 | Plain decimal convention | As a maintainer, I want every price the run writes to be an unquoted number in plain notation with trailing zeros stripped (`15`, `0.6`, never `"15"`, `1.5e1` or `15.00`), so that the catalog matches the charter's wire form. | High | Open | [build] | no |

### Non-Functional Requirements

| ID | Title | Requirement | Category | Priority | Status |
|----|-------|-------------|----------|----------|--------|
| NFR-001 | Byte stability | A no-change run leaves the catalog byte-identical (0 changed bytes). A change run alters only the lines of changed values plus the provenance lines, so an existing `15.0` is never rewritten to `15`. No value passes through binary floating point at any step; a test over a per-token source value such as `3e-06` yields exactly `3`. | Reliability | High | Open |
| NFR-002 | Source load | At most 1 fetch per source per run. | Reliability | Medium | Open |
| NFR-003 | Run time | The run, excluding the repository gates, completes in under 15 minutes. | Performance | Medium | Open |
| NFR-004 | Token exposure | 0 steps that parse source data can read a token or hold a write scope. Exactly 1 step holds `PR_CREATION_TOKEN`. Asserted by workflow property tests. | Security | High | Open |

### Constraints

| ID | Title | Constraint | Category | Priority | Status |
|----|-------|------------|----------|----------|--------|
| C-001 | Reuse the release-track split | Follow the derive/bump split of PR #344: source parsing and re-derivation run with read-only scope and no token; the commit is built from fixed text and made through the signed GraphQL commit; the committing job runs no repository code. | Technical | High | Open |
| C-002 | Token placement | `PR_CREATION_TOKEN` (operator ruling 2026-11-25) is held only by the final step that opens or supersedes the pull request, and that step runs only the GitHub CLI. | Security | High | Open |
| C-003 | Path allowlist | The committed changes are limited to the catalog, `packs/*/pack.yaml` (only foundation's `pack_version` line and `==` pins on it, checked by content), `packs/*/pack-manifest.yaml`, `packs/*.source.yaml`, generated `docs/packs/*.md` (not `index` or `catalog-proposal`), and the changelog. `charter.lock.yaml` and `.github/` are never written. | Security | High | Open |
| C-004 | No editorial writes, no benchmarks | The run never writes an editorial field (see Domain Language) and reads no benchmark source in v1 (operator ruling 2026-11-25). | Business | High | Open |
| C-005 | No credentials to sources; no scraping | No source needs or receives credentials. The provider documentation is cited, not fetched or parsed. | Regulatory | High | Open |
| C-006 | Sequencing | Plan and implementation start only after the open-packs pack-doctor alignment mission has landed (dispatcher, 2026-11-25). No pull request until the dispatcher confirms the order. | Business | High | Open |
| C-007 | Schema validity | Prices remain JSON-schema numbers ≥ 0 and `currency` a non-empty string (`routing-catalog.schema.json` `$defs.Cost`, charter pin `cb9b154`). A quoted price is invalid. | Technical | High | Open |
| C-008 | Separate track | The run lives in its own workflow with its own concurrency group and labels; it shares no state with the charter track. | Technical | Medium | Open |

### Key Entities

- **Catalog entry**: an id, a provider, and a cost (input price per 1M, output price per 1M,
  currency). Only the cost's three factual values and the catalog's provenance are run-writable.
- **Source snapshot**: a source's name, its URL, the revision read (a commit for the primary source),
  the time read, and licence notes. It becomes the catalog's `sources[]` provenance.
- **Difference**: the set of (entry, field, catalog value, source value) tuples, plus findings
  (disagreements, availability). It is canonicalised and hashed, and the hash names the pull
  request branch.
- **Currency pull request**: one per difference. It is superseded by a newer one, never merged by
  the run.
- **Red issue**: one standing issue for a source failure, closed by the next clean run.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Within one scheduled run of a price change in the primary source, exactly 1 currency pull request exists for it, and it passes 100% of the repository gates. — [build] · no-op passable: no
- **SC-002**: Across runs where the sources agree with the catalog, 0 pull requests, issues, branches or commits are created. — [build] · no-op passable: yes — paired with SC-001 on the same catalog
- **SC-003**: 100% of catalog changes reach `main` only through a person's merge; the run performs 0 merges, approvals or auto-merge enablements. — [build] · no-op passable: yes — proven by property test, not by absence
- **SC-004**: 100% of source disagreements and availability findings in a run appear in that run's pull request body or standing issue, and 0 of them change an entry or an editorial field. — [build] · no-op passable: no

## Assumptions

- The primary source's per-entry price is the first-party list price; reseller prices are not used.
- The provider whose entries the catalog holds remains the only provider watched in v1. Adding a provider is an editorial change made by a person.
- `PR_CREATION_TOKEN` exists with the scopes documented for the charter track (operator ruling on #314).
- The pack-doctor alignment mission may change the pin tooling this run reuses. The plan re-reads that tooling after it lands.
- The decimal convention of FR-013 is this repository's convention, not a charter rule. The charter compares prices by value and keeps the written form (dispatcher, quoting charter `main` 4b95b9151).

## Out of Scope

- Benchmarks of any kind (v1).
- Writing task fit, tiers, strengths, weaknesses or routing policy.
- Adding or removing catalog entries.
- Other catalogs, or catalogs in other packs.
- Any change to the charter or to charter-track behaviour.
