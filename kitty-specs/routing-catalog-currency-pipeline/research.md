# Research: routing catalog currency pipeline (#315)

Pre-spec research step for #315 (operator ruling, 2026-11-24): propose the sources and the run
frequency, for the operator to approve **before anything is built**. Nothing here builds the
pipeline. `/spec-kitty.specify` adopts this file when the mission is created.

- Governance: `spec-kitty charter context --action research` (software-dev-default template set).
- Read: #315 (with its two operator-ruling comments), #313 (closed), #287, #308, #310,
  PR #344 head `e56c0bb` (`.github/workflows/charter-track.yml`), the catalog, `packs/*/pack.yaml`.
- **Not read: charter ADR-0080.** spec-kitty-charter is private and outside this session's
  access, and the pinned `contracts/packs` (routing-catalog schema) could not be fetched either.
  ADR-0080 decisions 10 and 14 are taken from their restatement in #313 and #315.
- Source checks ran on 2026-11-24 from a cloud session whose network reaches GitHub only. Each
  source below is marked **verified** (fetched and inspected) or **unverified** (host blocked from
  this session: no claim is made beyond its public reputation). Evidence:
  [research/source-register.csv](research/source-register.csv).

## Operator rulings (2026-11-25, relayed by the dispatcher)

The operator approved the recommendations, with benchmarks dropped:

- **Sources.** Primary: models.dev at a pinned commit (A1). Authority: the provider docs (A2), cited
  and not scraped. Cross-check: LiteLLM (A3). A disagreement is flagged in the PR and is never
  auto-resolved.
- **Benchmarks.** Not in v1. Section 2b and recommendation 4 are recorded for a later version only.
- **Schedule.** Weekly on Monday, early UTC, plus `workflow_dispatch`.
- **Token.** Reuse `PR_CREATION_TOKEN`, held only by the final step, the one that opens the PR.
- **Pending.** The canonical decimal form for ADR-0080 decision 10 (R5, open question 5). The
  dispatcher is having it quoted from a charter session.
- **Sequencing.** The spec follows the open-packs pack-doctor alignment mission, which touches the
  same pin tooling. No PR until the dispatcher confirms the order.

## 1. What the catalog holds today

`packs/foundation/routing_catalogs/default.routing-catalog.yaml` (561 lines, `generated_at`
2026-07-04, description: "Task-fit scores are editorial judgment, not benchmarked"):

| Section | Content | Who keeps it current |
| --- | --- | --- |
| `task_types[]` (25) | id, title, description, `quality_sensitivity`, `cost_sensitivity` | Editorial. Not a pipeline field. |
| `models[]` (3 entries, one provider) | `id`, `provider`, `family`, `tools`, `strengths`, `weaknesses`, `task_fit[]` (25 × score/confidence/rationale), `cost{tier, input_per_1m_usd, output_per_1m_usd, currency}`, `latency_tier` | Split, see below. |
| `routing_policy` | objective, weights, `tier_constraints[]` | Editorial. Not a pipeline field. |
| `sources[]` (1) | `name`, `url`, `access_method: manual`, `snapshot_at`, `license_notes` | Pipeline, as provenance. |
| `generated_at` | catalog timestamp | Pipeline. |

Fields a pipeline can keep current **from facts**:

- **Availability:** whether each `models[].id` is still served, deprecated or retired, and which new
  entries the same providers ship. A new entry can only be *proposed*: its `task_fit`, `strengths`,
  `weaknesses`, `cost.tier` and `latency_tier` are editorial.
- **Pricing:** `cost.input_per_1m_usd`, `cost.output_per_1m_usd`, `cost.currency`.
- **Capabilities (optional):** `tools` (code execution, file edit, web search), when a source states them.
- **Provenance:** `sources[].snapshot_at`, `sources[].url`, `generated_at`.

Fields a pipeline must **not** write: `task_fit` scores, `confidence`, `rationale`, `cost.tier`,
`latency_tier`, `routing_policy`. The catalog says outright that task fit is editorial. Benchmarks
measure benchmarks, not this catalog's 25 task types, so a mechanical benchmark-to-score mapping
would invent precision. **Decision (proposed): benchmark data is advisory evidence in the PR body,
not catalog content.**

Today's prices are written `15.0`, `75.0`, `0.8`, `4.0`: plain YAML floats. Whether these already
satisfy ADR-0080 decision 10 ("exact decimals, round-trip byte for byte") depends on the schema and
the charter's round trip, which this session could not read. See risk R5.

## 2. Candidate sources

### 2a. Model availability and pricing

| # | Source | URL / format | Licence, terms | Auth | Stability | Maps to | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | **models.dev** (open community catalog, TOML in git, generated JSON API) | `https://models.dev/api.json` (JSON). Source of truth: TOML per provider and entry in the `sst/models.dev` repository (now `anomalyco/models.dev`), readable at a pinned commit via `raw.githubusercontent.com`. | MIT (LICENSE verified). No separate data terms found. | None | Documented v1 API fields; an experimental v2 exists, so the v1 shape may move. The git TOML can be pinned by commit. | `cost.input` / `cost.output` are **USD per 1M tokens**, the catalog's own unit → `input_per_1m_usd` / `output_per_1m_usd`. `status: deprecated` → availability. `limit.context`, `tool_call`, `release_date`. | README and licence verified. `api.json` host blocked here. |
| A2 | **Provider's own docs**: the models overview (the catalog's current source), pricing and deprecations pages on `docs.anthropic.com` | HTML or markdown. No public machine API. | Provider site terms. These are the authoritative statement. | None for the pages. The provider's `/v1/models` API needs a key → **excluded** (no credentials). | Authoritative, but scrape-fragile: page layout changes without notice. | Pricing, retirement dates, API ids. | Unverified (host blocked). |
| A3 | **LiteLLM price map**: `model_prices_and_context_window.json` in `BerriAI/litellm` | `https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json` (JSON, 5.2 MB, 7,158 entries) | MIT outside `enterprise/` (verified) | None | Very actively maintained; key set drifts. | `input_cost_per_token` / `output_cost_per_token` (**USD per token, JSON float literals** such as `3e-06`) → ×10⁶ for the catalog. `deprecation_date` (sparse: 4 of 24 entries for the catalog's provider). `max_input_tokens`. | **Verified.** |
| A4 | **OpenRouter models API** | `https://openrouter.ai/api/v1/models` (JSON) | Commercial reseller ToS: data reuse not confirmed | None for listing (by reputation) | Stable public API. Prices are the **reseller's**, which can differ from first-party. Strings per token (by reputation). | Pricing (per token), context length | Unverified (host blocked) |

### 2b. Benchmarks

| # | Source | URL / format | Licence, terms | Auth | Stability, freshness | Maps to | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B1 | **SWE-bench leaderboards** (agentic issue resolution) | `https://raw.githubusercontent.com/SWE-bench/swe-bench.github.io/master/data/leaderboards.json` (JSON, 4 MB). Boards: Verified (180 rows), Lite, Test, Multilingual, Multimodal. `resolved` is a percentage. | **CC BY-NC 4.0** (site repo, verified). Non-commercial: vendoring or redistributing the data in this MIT repo of a company is a legal question. Linking and citing in a PR body is lower risk. | None | Newest row: Verified 2026-02-26, Multilingual 2026-02-20, Lite 2025-09-11. **About nine months stale.** | Advisory for `code-review`, `implementation`, `code-*` | **Verified** |
| B2 | **Aider polyglot leaderboard** (code editing across languages) | `https://raw.githubusercontent.com/Aider-AI/aider/main/aider/website/_data/polyglot_leaderboard.yml` (YAML, 69 rows). `pass_rate_2` (%), `total_cost`, `edit_format`. | Apache-2.0 (verified) | None | Newest row 2025-10-03: **over a year stale.** | Advisory for `implementation`, `mechanical-edit` | **Verified** |
| B3 | **Epoch AI Benchmarking Hub** (aggregates many benchmarks, CSV downloads) | `https://epoch.ai/data/ai-benchmarking-dashboard` (CSV / zip) | CC BY by reputation: **to confirm** | None (by reputation) | Research-org maintained, updated continuously (by reputation) | Advisory across reasoning and coding task types | Unverified (host blocked) |
| B4 | **LiveBench** (contamination-limited reasoning, math, coding, data analysis, instruction following) | `https://livebench.ai`. Data as Hugging Face datasets under `livebench/` (JSONL), leaderboard via repo script. | Code: mixed Apache-2.0 / MIT, no own licence named (verified). Data licence not stated. | None (by README) | README names release 2025-04-25: possibly stale | Advisory for `analysis`, `investigation`, `code-*` | Partly verified (GitHub only) |
| B5 | **LMArena** (human-preference Elo) / **Artificial Analysis** (composite index) | `lmarena.ai` (HF datasets); `artificialanalysis.ai` (API) | LMArena: unverified. Artificial Analysis: the **API needs a key**, so it is **excluded** (no sign-up). | LMArena none; AA key | Both fresh, by reputation | Human preference and composite indices fit no catalog task type closely | Unverified (host blocked) |

**Finding:** every benchmark source this session could verify is 9–14 months stale, and the freshest
is non-commercial. The only fresh, permissively licensed benchmark candidates (B3, B4) are
unverified. That supports keeping benchmarks advisory.

## 3. Recommendation

**Source set (proposed):**

1. **A1 models.dev as the primary availability and pricing feed**, read as the TOML at a pinned
   commit of its git repository rather than the generated JSON. Reasons: MIT; the catalog's own unit
   (USD per 1M); explicit `deprecated` status; literal decimal text available (see R5); and a commit
   can be named in `sources[]` the way `charter.lock.yaml` names a charter commit.
2. **A2 the provider's docs pages as the authority.** The pipeline does not scrape them. Every PR
   cites them in `sources[]` and the body, and the reviewer confirms each change against them.
   That keeps the catalog's current `access_method: manual` source honest.
3. **A3 LiteLLM as a cross-check only.** When A1 and A3 disagree on a price, the PR says so and
   does not pick one.
4. **Benchmarks: advisory, in the PR body only.** Use B3 (Epoch AI) once its licence is confirmed as
   CC BY, falling back to B1 (SWE-bench Verified) as a *link and cite* only, never vendored. No
   benchmark number is written into the catalog. If the operator prefers, drop benchmarks from v1
   altogether: availability and pricing alone meet #315's "Done when".
5. **Not used:** OpenRouter (reseller prices), provider model APIs and Artificial Analysis (both
   need credentials), LMArena (no task-type fit; licence unverified).

**Frequency (proposed): weekly**, Monday early UTC, plus `workflow_dispatch`.

- Prices and deprecations move a few times a quarter. Daily (like the charter track) would mostly
  produce no-change runs. Monthly risks a retirement passing before the catalog notices.
- There is no upstream release event to hook, so "on release" applies only to this repo's own
  releases. It can be added as a second trigger: a run before each open-packs release.
- No-change runs are silent (#315). A change opens or updates **one** PR, so a weekly cadence
  cannot pile up PRs.

## 4. Reuse of the #308/#310 machinery (as hardened in PR #344)

Proposed shape: a **separate workflow** (`catalog-track.yml`), not a fourth track inside
`charter-track.yml`. It gets its own concurrency group and its own label (`catalog:currency`), and
it never touches `charter.lock.yaml`. Job split, mirroring PR #344:

| Job | Permissions, tokens | Does |
| --- | --- | --- |
| `resolve` | `contents: read` | Fetch sources at named revisions. Compute a canonical diff against the catalog. Output `act=false` on no change (silent). |
| `derive` | `contents: read`, **no token in any step**, `persist-credentials: false` | Parses untrusted external data (TOML/JSON), so it holds nothing. Edits the catalog. Bumps foundation `pack_version` (patch for a price or availability fix, minor for a new entry). Rewrites the **6 exact pins** (`range: "==3.7.0"` in built-in members' `pack.yaml`). Re-derives manifests, `*.source.yaml` digests and `docs/packs/*.md`. Adds a changelog entry. Hands over `file-changes.json` only. |
| `checks` | as `validate-packs.yml` | The same gates at the charter pin (ADR-0070 decision 3): `validate-packs.sh` (+ `--cross-pack`), charter-service and pack-check, vocabulary, `gen_pack_reference.py --check`, digests. |
| `bump` | job token `contents: write`. No checkout, no Python. | Checks every path against a **catalog allowlist**. Builds the commit from fixed text. Commits with GraphQL `createCommitOnBranch` (signed). Branch `catalog/currency-<diff-hash>`. |
| Open step (inside `bump`) | **the only holder of `PR_CREATION_TOKEN`**, runs nothing but `gh` | Opens the PR (its own `pull_request` checks run), or updates the open one, and closes a superseded one. |

**Allowlist** (narrower than the charter track's, and not a copy). The charter track's `rewritten`
regex does not cover `pack.yaml` or the catalog, and it does cover `charter.lock.yaml`:

```text
^packs/foundation/routing_catalogs/default\.routing-catalog\.yaml$
^packs/[A-Za-z0-9_-][A-Za-z0-9._-]*/pack\.yaml$          # foundation version + exact pins only (content-checked)
^packs/[A-Za-z0-9_-][A-Za-z0-9._-]*/pack-manifest\.yaml$
^packs/[A-Za-z0-9_-][A-Za-z0-9._-]*\.source\.yaml$
^docs/packs/[A-Za-z0-9_-][A-Za-z0-9._-]*\.md$            # not index / catalog-proposal
^docs/changelog/CHANGELOG\.md$
```

`pack.yaml` edits should also be checked by content, in the way PR #344 checks the lock: only the
foundation `pack_version` line and `==<old>` → `==<new>` ranges may change. Additions only; no
deletions.

**Never merges itself:** no `gh pr merge`, no `--auto`, no approve, and no `pull-requests: write`
on the job token. Workflow property tests (as in `tests/ci/test_workflows.py`) assert all of this,
along with "acts only from `main` in this repository" and "only `bump` holds a write scope or a
secret".

## 5. Risks

- **R1 Source drift.** models.dev's v1 API has a v2 successor; LiteLLM keys churn; provider pages
  change layout. *Mitigation:* read A1 at a pinned commit. A parse failure fails closed and opens
  one `catalog:currency-red` issue, like `charter:release-red`. It never produces a partial PR.
- **R2 Rate limits.** Raw GitHub is generous for one weekly fetch. The models.dev host and
  provider pages state no limits that this session could see. *Mitigation:* one fetch per source
  per run, cached as an artifact.
- **R3 ToS and licence.** SWE-bench data is CC BY-NC 4.0 and must not be vendored. OpenRouter terms
  are unknown. The Epoch licence is to be confirmed. *Mitigation:* each source gets a
  `license_notes` line in `sources[]`, and benchmark numbers stay out of the catalog.
- **R4 Catalog churn.** Every change cascades: the foundation version, 6 exact pins, about 7
  manifests and digests, and docs pages. *Mitigation:* one PR at a time, superseded and not stacked;
  ignore sub-cent rounding noise and fields the catalog does not hold; weekly cadence.
- **R5 Exact decimals (ADR-0080 decision 10).** LiteLLM is per token in float notation (`3e-06`), so
  ×10⁶ in binary floating point is lossy. *Mitigation:* never touch a float. Parse with
  `Decimal(text)` (`json.loads(parse_float=Decimal)`, `tomllib.loads(parse_float=Decimal)`), scale
  with `Decimal.scaleb(6)`, and render in the catalog's canonical form. Edit the YAML with targeted
  line replacement, not a `yaml.dump` round trip, so untouched bytes stay identical. Test that a
  no-change run reproduces the file byte for byte. **Open:** the canonical decimal form the charter
  expects (`15.0` vs `15` vs a quoted string) is in ADR-0080 and the schema, which this session could
  not read.
- **R6 Supply chain.** The derive job parses third-party data. Hence no token and no write scope
  there, and a path and content allowlist in `bump` (PR #344's model).
- **R7 Verification gap.** Seven candidate hosts were unreachable from this session. Before build,
  re-check them from a runner that can reach them (GitHub Actions has open egress).

## Open questions for the operator

1. Approve **models.dev (pinned commit) as primary**, **provider docs as authority**, **LiteLLM as
   cross-check**?
2. Benchmarks: **advisory in PR body (Epoch AI, SWE-bench link only)**, or **drop from v1**?
3. Frequency: **weekly** (+ dispatch, + optional pre-release run)?
4. A separate `catalog-track.yml` with its own allowlist, reusing `PR_CREATION_TOKEN`: or a
   different PAT?
5. Who supplies ADR-0080 decision 10's canonical decimal form (R5)?
