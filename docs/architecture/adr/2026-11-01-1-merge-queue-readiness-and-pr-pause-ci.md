---
title: 'ADR: main lands through a merge queue, and pr:pause-ci pauses a parked pull request'
description: Decision that the one required check runs on merge_group, docs-site.yml stays path-filtered and non-required, and pr:pause-ci keeps a paused pull request red.
doc_status: active
updated: '2026-11-01'
related:
- guides/contributing
- architecture/adr/2026-10-20-1-semver-releases-with-per-pack-archives
---
# main lands through a merge queue, and pr:pause-ci pauses a parked pull request

**Filename:** `2026-11-01-1-merge-queue-readiness-and-pr-pause-ci.md`

> **Superseded in part.** The operator ruled on 2026-11-02 that this repository has no merge queue.
> In core the queue duplicated CI runs rather than avoiding reruns. `validate-packs.yml` no longer runs
> on `merge_group`, and the queue settings are gone from the contributing guide. `Validate packs gate`
> stays the required check, and `pr:pause-ci` stays. The text below records the earlier decision; read
> every mention of the queue in it as retired.

**Status:** Accepted. The operator ruled on 2026-11-01, as recommended, and turns the queue on after the change lands. Superseded in part on 2026-11-02 (see above): no queue.

**Date:** 2026-11-01

**Deciders:** Stijn Dejongh (operator)

**Technical Story:** [open-packs #106](https://github.com/spec-kitty/spec-kitty-open-packs/issues/106) (multi-runner
landing). The same remedy is applied in spec-kitty-charter (ADR-0047), doc-kitty (ADR-0072),
spec-kitty-events (ADR-0005) and core (#6961).

---

## Context and Problem Statement

- Several sessions open pull requests here at once.
  - Each one is tested against the `main` it branched from.
  - When one merges, the others are re-seeded and re-run by hand: the `chore(landing): re-seed…`
    commits on `main` are that cost.
- The operator is turning on GitHub's merge queue for `main`. The queue tests each pull request
  on top of the ones ahead of it, and it waits for the required checks on a `merge_group` event.
- No workflow ran on `merge_group`, so every queued pull request would have waited for the check
  timeout and then been evicted.
- Nothing stopped CI on a parked pull request during a pile-up.

## Decision Drivers

* A required check must report on every pull request and on every queue entry. A check that never
  starts blocks the pull request.
* A queue run carries no pull-request payload. No expression may read one there without a guard.
* Queue runs and `main` runs must not cancel or hold back each other.
* A paused pull request must never read as green.

## Considered Options

* **Path filters.**
  * (a) Keep `docs-site.yml` path-filtered and non-required. Put its cheap drift check in the
    required job.
  * (b) Move `docs-site.yml`'s filter into the job, as a detect step, and add a gate job, so it can be
    required too.
* **Another label's event.**
  * (c) Re-run validation, in a concurrency group of its own.
  * (d) Repeat the last verdict on the commit by polling its check runs, as charter's `ci.yml` does.

## Decision Outcome

**Chosen options:** (a) and (c).

**(a) path filters.**
- Validation takes 1 to 3 minutes. The docsite build needs npm and a private-package token, which
  a queue run gains little from.
- The failure the queue exists to catch is two pack changes that each re-seed `docs/packs/` and then
  drift once combined. The drift check catches that, and it now runs in the required job.

**(c) other labels.** A full re-run costs 1 to 3 minutes here, which is less machinery than polling.

1. **One required check: `Validate packs gate`**, with GitHub Actions as its source.
   - `validate-packs.yml` runs on `merge_group` (`checks_requested`) and is not path-filtered.
   - The drift check `gen_pack_reference.py --check` is now a step of its validation job.
   - `docs-site.yml` and `release.yml` do not run on `merge_group`.
2. **Concurrency.**
   - Pull requests: one group per pull request number, and a new run cancels the old one.
   - Every other run has a group of its own (its run id):
     - a queue entry;
     - a push to `main`;
     - a release's call;
     - a dispatch.

     These runs are never cancelled, and none waits behind another.
3. **`pr:pause-ci`.**
   - `pull_request` also triggers on `labeled` and `unlabeled`.
   - On a pull request that carries the label, validation is skipped and the gate fails.
   - Adding or removing the label joins the pull request's group:
     - adding it cancels the running check;
     - removing it runs CI again.
   - Another label's event gets a `label-` group, so it never cancels a real run.
   - The gate decides "paused" from the pull request's labels as they are now, not from the run's
     payload. A run that started before the label was added therefore cannot post a green gate on a
     paused pull request, whether it is another label's run or a re-run of an old run.
   - The label is ignored on `merge_group`, `push` and `workflow_call`.
4. **Queue settings**, set by the operator: see
   [Contributing](../../guides/contributing.md#required-checks) (the queue settings were removed on 2026-11-02).

### Consequences

#### Positive

* A queued pull request is tested on the `main` it will land on, so combined drift fails in the
  queue, not on `main`.
* A paused pull request costs only its gate job, and it cannot merge or enter the queue.

#### Negative

* On a pull request, the drift check runs twice: once in the required job and once in
  `docs-site.yml`, when that workflow's paths match. It takes about 20 seconds.
* A change to any other label re-runs validation, which takes 1 to 3 minutes.
* The gate's live label read needs `pull-requests: read`. `release.yml` grants it to the workflow it
  calls.
* A pull request already in the queue is not paused by the label, because a queue run carries no
  labels. Take it out of the queue first.
* Known windows, all of which leave a pull request red rather than green, except the last:
  * A run that started while the label was on, and gets its runner only after the label is removed,
    skips validation and posts a red gate. A push, or a re-run of the newest run, gives a verdict.
  * A run superseded by a newer one still posts its gate (the gate runs `always()`), as a red
    "cancelled" result, until the newer run reports. Its `always()` is deliberate: a skipped
    required check counts as passing.
  * The gate's label read and the label being added can cross within seconds, so a paused pull
    request can briefly read green. The queue tests it again before it merges, and charter's
    verdict-repeat polling, which would close the window, is more machinery than it is worth here.

#### Neutral

* The docsite build stays a non-required, path-filtered check, as before.

### Confirmation

- `tests/ci/test_workflows.py` simulates each event against the parsed workflows and evaluates
  their expressions. The events are:
  - a push to a pull request;
  - a pause label added or removed;
  - another label;
  - a queue entry;
  - a push to `main`;
  - a release's call;
  - a dispatch.
- The tests assert the properties above.
- The first queue runs after the operator turns the queue on confirm it on GitHub.
