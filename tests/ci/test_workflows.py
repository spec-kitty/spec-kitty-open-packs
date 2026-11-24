"""The workflows behind the required checks are always reported and honour `pr:pause-ci`.

These are property tests over the parsed workflow files: each event a run can start from (a pull
request push, a label change, a push to main, a release's call) is simulated, and
the workflow's own expressions are evaluated against it with `gh_expr`. They assert what the required check
and the pause label need, not how the YAML spells it.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gh_expr  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"

# The check the operator requires on `main`, and the workflow that posts it. The operator
# documentation in docs/guides/contributing.md names the same check.
WORKFLOW = "validate-packs.yml"
GATE = "Validate packs gate"

PAUSE_LABEL = "pr:pause-ci"
DEFAULT_PR_TYPES = {"opened", "synchronize", "reopened"}


def load(name: str) -> dict[str, Any]:
    return yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))


def triggers(workflow: dict[str, Any]) -> dict[str, Any]:
    # YAML 1.1 reads the bare key `on` as the boolean true.
    return dict(workflow.get("on", workflow.get(True)))


def job_named(workflow: dict[str, Any], check: str) -> tuple[str, dict[str, Any]]:
    for job_id, job in workflow["jobs"].items():
        if job.get("name", job_id) == check:
            return job_id, job
    raise AssertionError(f"no job is named {check!r}")


# --- Simulated events -------------------------------------------------------------------------------

def pr_event(action: str = "synchronize", labels: tuple[str, ...] = (), label: str | None = None,
             number: int = 7, run_id: int = 1001) -> dict[str, Any]:
    event: dict[str, Any] = {
        "action": action,
        "number": number,
        "pull_request": {
            "number": number,
            "draft": False,
            "labels": [{"name": name} for name in labels],
            "head": {"sha": "a" * 40, "ref": "feature"},
            "base": {"sha": "b" * 40, "ref": "main"},
        },
    }
    if label is not None:
        event["label"] = {"name": label}
    return {"event_name": "pull_request", "event": event, "ref": f"refs/pull/{number}/merge",
            "run_id": run_id}


def push_event(ref: str = "refs/heads/main", run_id: int = 3001) -> dict[str, Any]:
    return {"event_name": "push", "event": {"ref": ref, "before": "b" * 40, "after": "c" * 40},
            "ref": ref, "run_id": run_id}


def dispatch_event(run_id: int = 4001) -> dict[str, Any]:
    return {"event_name": "workflow_dispatch", "event": {"ref": "refs/heads/main", "inputs": {}},
            "ref": "refs/heads/main", "run_id": run_id}


def contexts(github: dict[str, Any], needs: dict[str, str] | None = None) -> dict[str, Any]:
    github = {"repository": "spec-kitty/spec-kitty-open-packs", "workflow": "Validate packs",
              "sha": "c" * 40, "token": "x", **github}
    return {
        "github": github,
        "needs": {job: {"result": result, "outputs": {}} for job, result in (needs or {}).items()},
        "env": {}, "secrets": {"GITHUB_TOKEN": "x"}, "inputs": {}, "vars": {}, "runner": {},
        "steps": {}, "matrix": {}, "strategy": {}, "job": {},
    }


PAUSED_EVENTS = {
    "a push to a paused PR": pr_event(labels=(PAUSE_LABEL,)),
    "adding the pause label": pr_event("labeled", labels=(PAUSE_LABEL,), label=PAUSE_LABEL),
    "another label on a paused PR": pr_event("labeled", labels=("docs", PAUSE_LABEL), label="docs"),
}
RUNNING_EVENTS = {
    "a push to a PR": pr_event(),
    "opening a PR": pr_event("opened"),
    "removing the pause label": pr_event("unlabeled", labels=(), label=PAUSE_LABEL),
    "another label": pr_event("labeled", labels=("docs",), label="docs"),
    "a push to main": push_event(),
    "a release calling the workflow": push_event("refs/tags/v1.2.3"),
    "a manual dispatch": dispatch_event(),
}
NON_PR_EVENTS = {
    "a push to main": push_event(),
    "a release calling the workflow": push_event("refs/tags/v1.2.3"),
    "a manual dispatch": dispatch_event(),
}


def concurrency(workflow: dict[str, Any], github: dict[str, Any]) -> tuple[str, bool]:
    block = workflow["concurrency"]
    group = gh_expr.render(block["group"], contexts(github))
    return str(group), gh_expr._truthy(gh_expr.render(block["cancel-in-progress"], contexts(github)))


def reachable_expressions(workflow: dict[str, Any], github: dict[str, Any]) -> list[str]:
    """The expressions a run evaluates for one event: workflow-level ones, every `if`, and the rest of
    each job and step only when its `if` lets it run."""
    needs = contexts(github, {job: "success" for job in workflow["jobs"]})
    found = gh_expr.expressions_in({k: v for k, v in workflow.items() if k != "jobs"})
    for job in workflow["jobs"].values():
        found.extend(gh_expr.expressions_in({"if": job["if"]}) if "if" in job else [])
        if not gh_expr.evaluate_if(job.get("if"), needs, strict_event=True):
            continue
        found.extend(gh_expr.expressions_in({k: v for k, v in job.items() if k not in ("if", "steps")}))
        for step in job.get("steps", []):
            found.extend(gh_expr.expressions_in({"if": step["if"]}) if "if" in step else [])
            if gh_expr.evaluate_if(step.get("if"), needs, strict_event=True):
                found.extend(gh_expr.expressions_in({k: v for k, v in step.items() if k != "if"}))
    return found


GATE_STUBS = {
    # `gh api` prints the labels the PR has now, one per line, or fails like an API outage.
    "gh": """#!/usr/bin/env bash
[[ "$1" == "api" && "$*" == *"repos/$STUB_REPO/issues/$STUB_NUMBER/labels"* ]] || exit 2
[[ "$STUB_API" == "ok" ]] || { echo "HTTP 502" >&2; exit 1; }
printf '%s' "$STUB_LABELS"
""",
    "sleep": "#!/usr/bin/env bash\nexit 0\n",  # the retry back-off, without the wait
}


def run_gate(workflow: dict[str, Any], github: dict[str, Any], validate: str, *,
             labels_now: tuple[str, ...] = (), api: str = "ok", service: str = "success") -> str:
    """Run the gate job's real step scripts under bash and return its result.

    `validate` and `service` are the `needs.validate.result` and `needs.charter-service.result` the gate
    sees. `labels_now` is what the API reports for
    the pull request when the gate asks, which can differ from the run's payload; `api="down"` makes
    the call fail. Steps are chosen by their own `if`, and a failed step skips the ones after it.
    """
    _, gate = job_named(workflow, GATE)
    ctx = contexts(github, {"validate": validate, "charter-service": service})
    with tempfile.TemporaryDirectory() as tmp:
        for name, body in GATE_STUBS.items():
            path = Path(tmp) / name
            path.write_text(body, encoding="utf-8")
            path.chmod(0o755)
        for step in gate["steps"]:
            if not gh_expr.evaluate_if(step.get("if"), ctx):
                continue
            env = {"PATH": f"{tmp}:{os.environ['PATH']}", "STUB_API": api, "STUB_LABELS": "\n".join(labels_now),
                   "STUB_REPO": ctx["github"]["repository"],
                   "STUB_NUMBER": str(github.get("event", {}).get("number", ""))}
            env.update({key: str(gh_expr.render(value, ctx)) for key, value in step.get("env", {}).items()})
            done = subprocess.run(["bash", "-e", "-c", gh_expr.render(step["run"], ctx)], env=env,
                                  capture_output=True, text=True, timeout=30, check=False)
            if done.returncode != 0:
                return "failure"
    return "success"


def simulate(workflow: dict[str, Any], github: dict[str, Any]) -> dict[str, str]:
    """Each job's result for one event, assuming the real work succeeds.

    A job whose `if` is false is skipped; the gate job runs its real scripts (`run_gate`), seeing the
    labels the payload carries; every other job that runs passes.
    """
    results: dict[str, str] = {}
    pending = dict(workflow["jobs"])
    payload_labels = tuple(label["name"] for label in github.get("event", {}).get("pull_request", {}).get("labels", []))
    while pending:
        for job_id, job in list(pending.items()):
            needs = job.get("needs", [])
            needs = [needs] if isinstance(needs, str) else needs
            if any(need in pending for need in needs):
                continue
            del pending[job_id]
            upstream = {need: results[need] for need in needs}
            ok = all(result == "success" for result in upstream.values())
            status = {"success": ok, "failure": not ok, "cancelled": False}
            if not gh_expr.evaluate_if(job.get("if"), contexts(github, upstream), status=status):
                results[job_id] = "skipped"
            elif job.get("name", job_id) == GATE:
                results[job_id] = run_gate(workflow, github, upstream["validate"], labels_now=payload_labels,
                                           service=upstream["charter-service"])
            else:
                results[job_id] = "success"
    return results


class RequiredCheckAlwaysReports(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = load(WORKFLOW)

    def test_the_workflow_is_not_filtered_away(self) -> None:
        # A filtered trigger never posts its check on a change outside the filter, and a required
        # check that never reports blocks the PR.
        on = triggers(self.workflow)
        for event in ("pull_request",):
            config = on.get(event) or {}
            for key in ("paths", "paths-ignore", "branches", "branches-ignore"):
                with self.subTest(event=event, filter=key):
                    self.assertNotIn(key, config)

    def test_no_expression_reads_a_pull_request_field_on_a_main_or_release_run(self) -> None:
        # Strict mode fails any read of a payload field the event does not carry, unless a guard
        # such as `github.event_name == 'pull_request' &&` short-circuits it first. A skipped job or
        # step is not evaluated past its `if`, as on GitHub.
        for label, github in NON_PR_EVENTS.items():
            for expression in reachable_expressions(self.workflow, github):
                with self.subTest(event=label, expression=expression.strip()):
                    gh_expr.evaluate(expression, contexts(github, {j: "success" for j in self.workflow["jobs"]}),
                                     strict_event=True)

    def test_every_job_passes_when_validation_passes_on_an_unpaused_event(self) -> None:
        # Includes the events that carry no labels (main, a release): none reads as paused.
        for label, github in RUNNING_EVENTS.items():
            with self.subTest(event=label):
                results = simulate(self.workflow, github)
                self.assertTrue(all(result == "success" for result in results.values()), results)

    def test_the_required_check_covers_the_generated_pack_pages(self) -> None:
        # Two pack PRs that each re-seed docs/packs/ can drift together.
        # The drift check must run in a job the required check depends on, on every unpaused event.
        _, gate = job_named(self.workflow, GATE)
        needs = gate.get("needs", [])
        needs = [needs] if isinstance(needs, str) else needs
        for label, github in RUNNING_EVENTS.items():
            with self.subTest(event=label):
                for command in ("gen_pack_reference.py --check", "discover -s tests/docs"):
                    ran = [step for job_id in needs
                           if gh_expr.evaluate_if(self.workflow["jobs"][job_id].get("if"), contexts(github))
                           for step in self.workflow["jobs"][job_id].get("steps", [])
                           if command in str(step.get("run", "")).split("#")[0]
                           and gh_expr.evaluate_if(step.get("if"), contexts(github))]
                    self.assertTrue(ran, f"{command!r} does not run under the required check")

    def test_the_required_check_covers_every_pack_digest(self) -> None:
        # A pack edit without its recorded digest must fail the required check on every unpaused event.
        script = "scripts/ci/check-pack-digests.sh"
        _, gate = job_named(self.workflow, GATE)
        needs = gate.get("needs", [])
        needs = [needs] if isinstance(needs, str) else needs
        for label, github in RUNNING_EVENTS.items():
            with self.subTest(event=label):
                ran = [step for job_id in needs
                       if gh_expr.evaluate_if(self.workflow["jobs"][job_id].get("if"), contexts(github))
                       for step in self.workflow["jobs"][job_id].get("steps", [])
                       if str(step.get("run", "")).strip() == script
                       and gh_expr.evaluate_if(step.get("if"), contexts(github))]
                self.assertTrue(ran, f"{script} does not run under the required check")
        path = Path(__file__).resolve().parents[2] / script
        self.assertTrue(path.is_file() and os.access(path, os.X_OK), f"{script} is missing or not executable")
        self.assertIn("pack_digest.py --check", path.read_text(encoding="utf-8"))


class CharterServiceJob(unittest.TestCase):
    """The job that asks the charter service (charter ADR-0070) is part of the required check."""

    def setUp(self) -> None:
        self.workflow = load(WORKFLOW)

    def test_the_gate_waits_for_it_and_a_paused_pull_request_skips_it_like_the_other_work(self) -> None:
        job_id, job = job_named(self.workflow, "Charter service validation")
        _, gate = job_named(self.workflow, GATE)
        self.assertIn(job_id, gate["needs"])
        self.assertEqual(job["if"], self.workflow["jobs"]["validate"]["if"])

    def test_it_reads_the_pin_and_runs_the_driver_script_on_the_jar_it_obtained(self) -> None:
        _, job = job_named(self.workflow, "Charter service validation")
        runs = "\n".join(str(step.get("run", "")) for step in job["steps"])
        for command in ("charter_lock.py commit", "charter_service_jar.sh", "charter_service_check.py --jar"):
            self.assertIn(command, runs)
        self.assertEqual(job["steps"][-1]["env"]["SERVICE_JAR"], "${{ steps.service.outputs.jar }}")
        java = [step for step in job["steps"] if str(step.get("uses", "")).startswith("actions/setup-java@")]
        self.assertEqual([step["with"]["java-version"] for step in java], ["25"])

    def test_it_gates_every_pack_on_pack_check_from_the_pin_and_keeps_the_report(self) -> None:
        # #252: the charter's whole-pack check, pack-check, from the pinned release (digest-checked), replaces driftTest.
        _, job = job_named(self.workflow, "Charter service validation")
        steps = job["steps"]
        runs = "\n".join(str(step.get("run", "")) for step in steps)
        check = next(step for step in steps if "charter_pack_check.py" in str(step.get("run", "")))
        self.assertEqual(check.get("id"), "pack_check")
        self.assertNotIn("continue-on-error", check)
        self.assertIn("!cancelled()", check["if"])  # it runs even when obtaining the service jar failed
        # Obtaining the jar and running it are one step under `set -e`: a jar that cannot be had fails the gate.
        self.assertIn("set -euo pipefail", check["run"])
        self.assertLess(check["run"].index("charter_pack_check_jar.sh"), check["run"].index("charter_pack_check.py --jar"))
        self.assertIn("tests.ci.test_charter_pack_check.RealPackCheck", check["run"])
        upload = next(step for step in steps if str(step.get("uses", "")).startswith("actions/upload-artifact@"))
        self.assertGreater(steps.index(upload), steps.index(check))
        self.assertIn("always()", upload["if"])
        self.assertEqual(upload["with"]["name"], "charter-pack-check-report")
        self.assertEqual(upload["with"]["path"], "${{ runner.temp }}/pack-check-report")
        self.assertEqual(check["env"]["REPORT_DIR"], upload["with"]["path"])
        # The service check still runs when pack-check is red, so one run reports both.
        self.assertIn("!cancelled()", steps[-1]["if"])

    def test_gradle_is_set_up_only_for_a_commit_pin(self) -> None:
        # A release pin downloads both jars; only a commit pin builds them from the pinned source.
        _, job = job_named(self.workflow, "Charter service validation")
        steps = job["steps"]
        gradle = next(step for step in steps if str(step.get("uses", "")).startswith("gradle/actions/setup-gradle@"))
        pin = next(i for i, step in enumerate(steps) if step.get("id") == "pin")
        self.assertGreater(steps.index(gradle), pin)
        for release_tag, expected in (("", True), ("service-v0.1.0-rc.3", False)):
            ctx = contexts(pr_event())
            ctx["steps"] = {"pin": {"outputs": {"release_tag": release_tag}}}
            with self.subTest(release_tag=release_tag):
                self.assertEqual(gh_expr.evaluate_if(gradle["if"], ctx), expected)

TRACK = "charter-track.yml"
TARGET = {"charter_commit": "d" * 40, "charter_release_tag": "service-v9.0.0", "charter_jar_sha256": "e" * 64,
          "charter_pack_check_sha256": "f" * 64}


RELEASE_CRON = "41 5 * * *"
NIGHTLY_CRON = "23 2 * * *"  # the nightly main track (#311)


def schedule_event(ref: str = "refs/heads/main", run_id: int = 5001, cron: str = RELEASE_CRON) -> dict[str, Any]:
    return {"event_name": "schedule", "event": {"schedule": cron}, "ref": ref, "run_id": run_id}


def nightly_event(ref: str = "refs/heads/main", run_id: int = 5002) -> dict[str, Any]:
    return schedule_event(ref, run_id, NIGHTLY_CRON)


def track_dispatch(track: str, ref: str = "refs/heads/main", run_id: int = 6001) -> dict[str, Any]:
    inputs = {"track": track, "charter_ref": "main", "release_tag": ""}
    return {"event_name": "workflow_dispatch", "event": {"ref": ref, "inputs": inputs}, "ref": ref,
            "run_id": run_id, "inputs": inputs}


def track_contexts(github: dict[str, Any], resolved: dict[str, str], checks: str = "success") -> dict[str, Any]:
    ctx = contexts({k: v for k, v in github.items() if k != "inputs"}, {"resolve": "success", "checks": checks})
    ctx["needs"]["resolve"]["outputs"] = resolved
    ctx["inputs"] = github.get("inputs", {})
    return ctx


class CharterTrack(unittest.TestCase):
    """charter-track.yml (#253): the release track acts only from main; the on-demand track never acts."""

    RELEASE = {"track": "release", "run": "true", "act": "true"}

    def setUp(self) -> None:
        self.workflow = load(TRACK)
        self.jobs = self.workflow["jobs"]

    def runs(self, job: str, github: dict[str, Any], resolved: dict[str, str], checks: str = "success",
             resolve: str = "success", provenance: str = "success", derive: str = "success") -> bool:
        needs = self.jobs[job].get("needs", [])
        results = {"resolve": resolve, "checks": checks, "provenance": provenance, "derive": derive}
        ok = all(results[need] == "success" for need in ([needs] if isinstance(needs, str) else needs))
        status = {"success": ok, "failure": not ok, "cancelled": False}
        ctx = track_contexts(github, resolved, checks)
        ctx["needs"]["resolve"]["result"] = resolve
        return gh_expr.evaluate_if(self.jobs[job].get("if"), ctx, status=status)

    def test_a_scheduled_run_that_cannot_resolve_the_release_says_so_on_main_only(self) -> None:
        self.assertTrue(self.runs("alert", schedule_event(), {}, checks="skipped", resolve="failure"))
        for event in (track_dispatch("release"), schedule_event("refs/heads/issue-253"),
                      {**schedule_event(), "repository": "someone/spec-kitty-open-packs"}):
            with self.subTest(event=event["event_name"], ref=event["ref"]):
                self.assertFalse(self.runs("alert", event, {}, checks="skipped", resolve="failure"))
        self.assertFalse(self.runs("bump", schedule_event(), {}, checks="skipped", resolve="failure"))

    def test_a_settled_red_issue_is_closed_by_release_runs_on_main_only(self) -> None:
        idle = {"track": "release", "run": "false", "act": "false"}
        self.assertTrue(self.runs("settle", schedule_event(), idle, checks="skipped"))
        self.assertTrue(self.runs("settle", schedule_event(), self.RELEASE))
        for name, event, resolved in (
            ("off main", schedule_event("refs/heads/issue-253"), idle),
            ("on demand", track_dispatch("ref"), {"track": "ref", "run": "true", "act": "false"}),
            ("a pull request", pr_event(labels=("charter:head",)), {"track": "ref", "run": "true", "act": "false"}),
        ):
            with self.subTest(case=name):
                self.assertFalse(self.runs("settle", event, resolved))
        self.assertFalse(self.runs("settle", schedule_event(), idle, resolve="failure"))

    def test_a_newer_release_on_main_opens_one_pull_request_when_green_and_one_issue_when_red(self) -> None:
        for event in (schedule_event(), track_dispatch("release")):
            with self.subTest(event=event["event_name"]):
                self.assertTrue(self.runs("bump", event, self.RELEASE))
                self.assertFalse(self.runs("alert", event, self.RELEASE))
                self.assertFalse(self.runs("bump", event, self.RELEASE, checks="failure"))
                # The provenance job fails only on an integrity event (a jar that is not the pinned file, #310): then
                # nothing is derived or published. A missing attestation is a warning and leaves it green.
                self.assertTrue(self.runs("provenance", event, self.RELEASE))
                self.assertTrue(self.runs("derive", event, self.RELEASE))
                for job in ("derive", "bump"):
                    self.assertFalse(self.runs(job, event, self.RELEASE, provenance="failure"))
                self.assertFalse(self.runs("bump", event, self.RELEASE, derive="failure"))
                self.assertTrue(self.runs("alert", event, self.RELEASE, checks="failure"))
                self.assertFalse(self.runs("alert", event, self.RELEASE, checks="cancelled"))
                self.assertTrue(self.runs("report", event, self.RELEASE, checks="failure"))

    def test_nothing_is_opened_off_main_in_a_fork_or_for_a_release_that_is_not_newer(self) -> None:
        cases = {
            "a dispatch on a branch": (track_dispatch("release", "refs/heads/issue-253"), self.RELEASE),
            "a fork's schedule": ({**schedule_event(), "repository": "someone/spec-kitty-open-packs"}, self.RELEASE),
            "an older release asked for": (track_dispatch("release"), {**self.RELEASE, "act": "false"}),
            "the on-demand track on main": (track_dispatch("ref"), {"track": "ref", "run": "true", "act": "false"}),
            "a labelled pull request": (pr_event(labels=("charter:head",)), {"track": "ref", "run": "true", "act": "false"}),
        }
        for name, (event, resolved) in cases.items():
            for checks in ("success", "failure"):
                with self.subTest(case=name, checks=checks):
                    self.assertFalse(self.runs("bump", event, resolved, checks))
                    self.assertFalse(self.runs("alert", event, resolved, checks))

    def test_nothing_runs_past_resolve_when_there_is_nothing_to_check(self) -> None:
        idle = {"track": "release", "run": "false", "act": "false"}
        for job in ("checks", "report", "provenance", "derive", "bump", "alert"):
            with self.subTest(job=job):
                self.assertFalse(self.runs(job, schedule_event(), idle, checks="skipped", provenance="skipped",
                                           derive="skipped"))

    def test_only_the_acting_jobs_hold_a_secret_or_a_write_permission(self) -> None:
        self.assertEqual(self.workflow["permissions"], {"contents": "read"})
        for job_id, job in self.jobs.items():
            text = yaml.safe_dump(job)
            writes = {scope for scope, level in (job.get("permissions") or {}).items() if level == "write"}
            with self.subTest(job=job_id):
                if job_id in ("bump", "alert", "settle", "main-red"):
                    self.assertTrue(writes)
                else:
                    self.assertEqual(writes, set())
                    self.assertNotIn("secrets.", text)
        self.assertNotIn("secrets.", yaml.safe_dump(self.jobs["alert"]))
        self.assertNotIn("secrets.", yaml.safe_dump(self.jobs["main-red"]))

    def test_a_pull_request_runs_it_only_with_the_charter_head_label_and_never_while_paused(self) -> None:
        expected = {
            "a push to a labelled PR": (pr_event(labels=("charter:head",)), True),
            "adding the label": (pr_event("labeled", labels=("charter:head",), label="charter:head"), True),
            "another label on a labelled PR": (pr_event("labeled", labels=("charter:head", "docs"), label="docs"), False),
            "a push to an unlabelled PR": (pr_event(), False),
            "a paused labelled PR": (pr_event(labels=("charter:head", PAUSE_LABEL)), False),
            "the schedule": (schedule_event(), True),
            "a dispatch": (track_dispatch("ref"), True),
        }
        for name, (event, runs) in expected.items():
            with self.subTest(event=name):
                ctx = track_contexts(event, {})
                self.assertEqual(gh_expr.evaluate_if(self.jobs["resolve"]["if"], ctx, strict_event=True), runs)

    def test_its_checks_are_the_required_checks_own_jobs_moved_to_the_target(self) -> None:
        checks = self.jobs["checks"]
        self.assertEqual(checks["uses"], f"./.github/workflows/{WORKFLOW}")
        self.assertEqual(set(checks["with"]), set(TARGET))
        for name, value in checks["with"].items():
            self.assertEqual(value, "${{ needs.resolve.outputs.%s }}" % name.removeprefix("charter_"))
        gate = load(WORKFLOW)
        self.assertEqual(set(triggers(gate)["workflow_call"]["inputs"]), set(TARGET))
        firsts = {"validate": "validate-packs.sh", "charter-service": "charter_lock.py"}
        for job_id, first_check in firsts.items():
            steps = gate["jobs"][job_id]["steps"]
            runs = [str(step.get("run", "")) for step in steps]
            move = next(i for i, run in enumerate(runs) if "charter_pin.py apply" in run)
            check = next(i for i, run in enumerate(runs) if first_check in run)
            with self.subTest(job=job_id):
                self.assertLess(move, check)
                self.assertEqual(steps[move]["if"], "${{ inputs.charter_commit }}")
                self.assertFalse(gh_expr.evaluate_if(steps[move]["if"], contexts(pr_event())))
                called = contexts(schedule_event())
                called["inputs"] = dict(TARGET)
                self.assertTrue(gh_expr.evaluate_if(steps[move]["if"], called))
                # Once the move failed, no later check judges the unmoved pin; when it did not run, all run.
                for outcome, expected in (("failure", False), ("skipped", True), ("success", True)):
                    called["steps"] = {"move": {"outcome": outcome}, "service": {"outcome": "success"}}
                    status = {"success": outcome != "failure", "failure": outcome == "failure", "cancelled": False}
                    for later in steps[move + 1:]:
                        if "if" not in later or "always()" in str(later["if"]):
                            continue
                        with self.subTest(job=job_id, step=later.get("name", later.get("uses")), move=outcome):
                            self.assertEqual(gh_expr.evaluate_if(later["if"], called, status=status), expected)

    def test_a_call_against_a_target_never_joins_or_cancels_a_pull_requests_own_check(self) -> None:
        gate = load(WORKFLOW)
        event = pr_event(labels=("charter:head",))
        own_group, own_cancel = concurrency(gate, event)
        ctx = contexts(event)
        ctx["inputs"] = dict(TARGET)
        group = str(gh_expr.render(gate["concurrency"]["group"], ctx))
        cancel = gh_expr._truthy(gh_expr.render(gate["concurrency"]["cancel-in-progress"], ctx))
        self.assertTrue(own_cancel)
        self.assertNotEqual(group, own_group)
        self.assertFalse(cancel)

    def test_release_runs_queue_and_on_demand_runs_stand_alone(self) -> None:
        def group(event: dict[str, Any]) -> tuple[str, bool]:
            ctx = track_contexts(event, {})
            block = self.workflow["concurrency"]
            return (str(gh_expr.render(block["group"], ctx)),
                    gh_expr._truthy(gh_expr.render(block["cancel-in-progress"], ctx)))
        scheduled, dispatched = group(schedule_event()), group(track_dispatch("release"))
        self.assertEqual(scheduled, dispatched)
        self.assertFalse(scheduled[1])
        self.assertNotEqual(group(track_dispatch("ref", run_id=1))[0], group(track_dispatch("ref", run_id=2))[0])
        self.assertTrue(group(pr_event(labels=("charter:head",)))[1])

    def test_another_label_never_cancels_a_charter_head_run(self) -> None:
        def group(event: dict[str, Any]) -> str:
            return str(gh_expr.render(self.workflow["concurrency"]["group"], track_contexts(event, {})))
        running = group(pr_event(labels=("charter:head",)))
        self.assertEqual(group(pr_event("labeled", labels=("charter:head",), label="charter:head")), running)
        self.assertNotEqual(group(pr_event("labeled", labels=("charter:head", "docs"), label="docs", run_id=7)), running)
        self.assertNotEqual(group(pr_event("labeled", labels=("charter:head", "docs"), label="docs", run_id=7)),
                            group(pr_event("labeled", labels=("charter:head", "x"), label="x", run_id=8)))


class CharterTrackBumpBoundary(unittest.TestCase):
    """#310 item 2, after review cycle 1: the token boundary is a job boundary. The derive job runs the pin tooling over
    the new release's contract and holds no token at all; the publish job (bump) holds the tokens, runs no repository
    code, and builds the commit request from fixed text, taking only validated file changes from the derive artifact.
    The PAT stays in the one step that opens and closes pull requests (operator ruling on #314)."""

    QUERY = "mutation($input: CreateCommitOnBranchInput!) { createCommitOnBranch(input: $input) { commit { oid } } }"

    def setUp(self) -> None:
        jobs = load(TRACK)["jobs"]
        self.derive_job, self.job = jobs["derive"], jobs["bump"]
        self.steps = self.job["steps"]
        self.lookup = next(step for step in self.steps if step.get("id") == "lookup")
        self.build = next(step for step in self.steps if step.get("id") == "build")
        self.push = next(step for step in self.steps if step.get("id") == "push")
        self.open = next(step for step in self.steps if step.get("name") == "Open the bump pull request")

    def test_derive_and_publish_are_separate_jobs_and_derive_holds_no_token(self) -> None:
        self.assertIn("derive", self.job["needs"])
        self.assertEqual(self.derive_job["permissions"], {"contents": "read"})
        text = yaml.safe_dump(self.derive_job)
        for credential in ("secrets.", "github.token", "GH_TOKEN", "GITHUB_TOKEN"):
            self.assertNotIn(credential, text)
        checkout = next(s for s in self.derive_job["steps"] if str(s.get("uses", "")).startswith("actions/checkout@"))
        self.assertIs(checkout["with"]["persist-credentials"], False)
        runs = "\n".join(str(step.get("run", "")) for step in self.derive_job["steps"])
        for command in ("charter_pin.py apply", "charter_pin.py changelog", "charter_pin.py commit-payload"):
            self.assertIn(command, runs)

    def test_publish_runs_no_repository_or_artifact_code(self) -> None:
        self.assertEqual(self.job["permissions"], {"contents": "write", "pull-requests": "read", "issues": "read"})
        uses = [str(step["uses"]) for step in self.steps if "uses" in step]
        self.assertEqual([u.split("@")[0] for u in uses], ["actions/download-artifact"])
        self.assertRegex(uses[0], r"@[0-9a-f]{40}$")  # pinned to a commit, like every action here
        for step in self.steps:
            run = str(step.get("run", ""))
            with self.subTest(step=step.get("name") or step.get("uses")):
                # No interpreter, no shell file, no sourcing, and no artifact file run as a command.
                self.assertIsNone(re.search(
                    r"python|\bpip3? |\.py\b|\.sh\b|\bchmod\b|\beval\b|\b(?:node|npx|java|perl|ruby|php|deno|bun)\b"
                    r"|\b(?:ba)?sh\s+[-\w$\"/]|(?:^|[;&|]\s*|\bthen\s+|\bdo\s+)(?:source\s|\.\s+\S|\"?\$ARTIFACT/)", run, re.M))
                # Every value reaches a script through env:, never by ${{ }} interpolation, and nothing reaches the
                # environment of a later step.
                self.assertNotIn("${{", run)
                self.assertNotRegex(run, r"GITHUB_(?:ENV|PATH)\b")

    def test_the_request_is_built_from_fixed_text(self) -> None:
        self.assertEqual(self.build["env"]["HEAD_SHA"], "${{ github.sha }}")
        self.assertNotRegex(yaml.safe_dump(self.build.get("env")), r"TOKEN|secrets\.|github\.token")
        self.assertEqual(self.push["env"]["HEAD_SHA"], "${{ github.sha }}")
        order = [self.steps.index(step) for step in (self.lookup, self.build, self.push, self.open)]
        self.assertEqual(order, sorted(order))

    def build_request(self, additions: list[str], deletions: list[str] = (), head: str = "a" * 40,
                      states: tuple[str, str] = ("verified", "verified"),
                      branch: str = "charter/service-release-service-v2.0.0",
                      raw: str | None = None, head_file: str | None = None) -> tuple[int, str, dict | None, str]:
        """Run the build step on a stand-in artifact; return its exit code, output, the request and the PR body."""
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            (work / "artifact").mkdir()
            changes = {"additions": [{"path": p, "contents": self.LOCK if p == "charter.lock.yaml" else "eA=="}
                                     for p in additions],
                       "deletions": [{"path": p} for p in deletions]}
            (work / "artifact" / "file-changes.json").write_text(json.dumps(changes) if raw is None else raw,
                                                                 encoding="utf-8")
            (work / "artifact" / "head").write_text(head + "\n" if head_file is None else head_file, encoding="utf-8")
            env = {**os.environ, "RUNNER_TEMP": tmp, "ARTIFACT": str(work / "artifact"), "HEAD_SHA": "a" * 40,
                   "REPO": "spec-kitty/spec-kitty-open-packs", "BRANCH": branch,
                   "RELEASE_TAG": "service-v2.0.0", "COMMIT": "c" * 40, "CURRENT": "service-v1.0.0",
                   "JAR_SHA256": "d" * 64, "PACK_CHECK_SHA256": "e" * 64, "RED": "12",
                   "RUN_URL": "https://example.invalid/run/1", "ATTEST_SERVICE": states[0],
                   "ATTEST_PACK_CHECK": states[1]}
            done = subprocess.run(["bash", "-c", self.build["run"]], env=env, capture_output=True, text=True, cwd=tmp)
            request = work / "request.json"
            body = work / "pr.md"
            return (done.returncode, done.stdout + done.stderr,
                    json.loads(request.read_text(encoding="utf-8")) if request.exists() else None,
                    body.read_text(encoding="utf-8") if body.exists() else "")

    #: The lock a real bump of service-v2.0.0 writes (the stand-in resolve outputs below), comments and all.
    LOCK_TEXT = ("# The charter this repository's packs are proven against.\n"
                 f"commit: {'c' * 40}\nrelease_tag: service-v2.0.0\njar_sha256: {'d' * 64}\n"
                 f"pack_check_sha256: {'e' * 64}\n")
    LOCK = base64.b64encode(LOCK_TEXT.encode()).decode()

    REAL = ["charter.lock.yaml", "docs/changelog/CHANGELOG.md", "packs/foundation.source.yaml",
            "packs/foundation/pack-manifest.yaml", "tests/fixtures/valid/example-pack/pack-manifest.yaml",
            "docs/packs/foundation.md"]

    def test_a_real_bumps_changes_become_a_request_with_the_fixed_query_branch_and_head(self) -> None:
        code, output, request, body = self.build_request(self.REAL, deletions=["docs/packs/retired.md"])
        self.assertEqual(code, 0, output)
        self.assertEqual(request["query"], self.QUERY)
        given = request["variables"]["input"]
        self.assertEqual(given["branch"], {"repositoryNameWithOwner": "spec-kitty/spec-kitty-open-packs",
                                           "branchName": "charter/service-release-service-v2.0.0"})
        self.assertEqual(given["expectedHeadOid"], "a" * 40)
        self.assertEqual([a["path"] for a in given["fileChanges"]["additions"]], self.REAL)
        self.assertEqual(given["fileChanges"]["deletions"], [{"path": "docs/packs/retired.md"}])
        self.assertIn("Closes #12.", body)

    def test_any_path_a_bump_does_not_write_fails_before_anything_is_pushed(self) -> None:
        for bad in ("../outside.md", "/etc/passwd", ".github/workflows/charter-track.yml", "scripts/ci/charter_pin.py",
                    "packs/../.github/x.yml", "docs/packs/sub/x.md", "packs/./foundation.source.yaml",
                    "packs/foundation/pack-manifest.yaml/x", "charter.lock.yaml\n.github/x", "",
                    "charter.lock.yaml\n", "docs/packs/foundation.md\u0007", "evil/charter.lock.yaml", ".github/packs/foundation.source.yaml",
                    "packs/foundation.source.yaml.bak"):
            for kind in ("addition", "deletion"):
                with self.subTest(path=bad, kind=kind):
                    args = ([*self.REAL, bad], []) if kind == "addition" else (self.REAL, [bad])
                    code, output, request, _ = self.build_request(*args)
                    self.assertNotEqual(code, 0)
                    self.assertIsNone(request)
                    self.assertIn("::error::", output)

    def test_the_lock_must_pin_exactly_what_was_checked(self) -> None:
        # Squad review: the derive artifact is untrusted, so the lock it carries could pin another jar, tag or commit
        # than the gate and the provenance job checked. Each wrong, missing or doubled pin value is refused.
        def lock_with(text: str) -> tuple[int, str, dict | None, str]:
            saved = self.LOCK
            self.LOCK = base64.b64encode(text.encode()).decode()
            try:
                return self.build_request(self.REAL)
            finally:
                self.LOCK = saved
        cases = {"another jar": self.LOCK_TEXT.replace("d" * 64, "f" * 64),
                 "another pack-check": self.LOCK_TEXT.replace("e" * 64, "f" * 64),
                 "another release": self.LOCK_TEXT.replace("service-v2.0.0", "service-v1.0.0"),
                 "another commit": self.LOCK_TEXT.replace("c" * 40, "b" * 40),
                 "a value missing": self.LOCK_TEXT.replace(f"jar_sha256: {'d' * 64}\n", ""),
                 "a value twice": self.LOCK_TEXT + f"jar_sha256: {'f' * 64}\n"}
        for name, text in cases.items():
            with self.subTest(case=name):
                code, output, request, _ = lock_with(text)
                self.assertNotEqual(code, 0)
                self.assertIsNone(request)
                self.assertIn("::error::", output)
        code, output, request, _ = self.build_request([p for p in self.REAL if p != "charter.lock.yaml"])
        self.assertNotEqual(code, 0, "a bump without the lock is no bump")
        self.assertIsNone(request)
        code, output, request, _ = self.build_request([*self.REAL, "charter.lock.yaml"])
        self.assertNotEqual(code, 0, "the lock is written once")
        self.assertIsNone(request)

    def changes_with_lock(self, text: str) -> str:
        return json.dumps({"additions": [{"path": p, "contents": base64.b64encode(text.encode()).decode()
                                          if p == "charter.lock.yaml" else "eA=="} for p in self.REAL],
                           "deletions": []})

    def test_a_second_json_document_cannot_smuggle_another_lock(self) -> None:
        # Tier R review, B1: jq judged the last value of the file while the request took the first one, so an evil
        # document followed by a good one passed the lock check and committed the evil lock. The file is now read
        # once, as exactly one object.
        good = self.changes_with_lock(self.LOCK_TEXT)
        evil = self.changes_with_lock(self.LOCK_TEXT.replace("d" * 64, "f" * 64))
        for name, raw in {"evil then good": f"{evil}\n{good}\n", "no separator": evil + good,
                          "good then evil": f"{good}\n{evil}\n", "good twice": f"{good}\n{good}\n",
                          "an array": f"[{good}]", "nothing": ""}.items():
            with self.subTest(artifact=name):
                code, output, request, _ = self.build_request(self.REAL, raw=raw)
                self.assertNotEqual(code, 0)
                self.assertIsNone(request)
                self.assertIn("::error::", output)
        self.assertEqual(self.build_request(self.REAL, raw=good)[0], 0)

    def test_the_lock_holds_only_comments_blank_lines_and_the_four_pins(self) -> None:
        # Tier R review, N1: anything else in the lock is refused before it is pushed, including what a YAML reader
        # could take for another line (a NUL, NEL or line separator) that jq's split does not see.
        cases = {"a quoted key": self.LOCK_TEXT + f'"jar_sha256": {"f" * 64}\n',
                 "another key": self.LOCK_TEXT + "extra: 1\n",
                 "a NUL": self.LOCK_TEXT.replace("\njar_sha256", "\x00jar_sha256"),
                 "a NEL in a comment": "#\u0085jar_sha256: " + "f" * 64 + "\n" + self.LOCK_TEXT,
                 "a line separator": "# x\u2028jar_sha256: " + "f" * 64 + "\n" + self.LOCK_TEXT,
                 "CRLF": self.LOCK_TEXT.replace("\n", "\r\n"),
                 "an indented pin": self.LOCK_TEXT + "  jar_sha256: " + "d" * 64 + "\n"}
        for name, text in cases.items():
            with self.subTest(lock=name):
                code, output, request, _ = self.build_request(self.REAL, raw=self.changes_with_lock(text))
                self.assertNotEqual(code, 0)
                self.assertIsNone(request)
        # Landing review: jq's @base64d stops at the first padding, so a good lock with an evil one appended after
        # it decoded as the good lock alone; only canonical base64 is taken.
        evil = self.LOCK_TEXT.replace("d" * 64, "f" * 64)
        padded = self.LOCK_TEXT + "#"
        while len(padded.encode()) % 3 == 0:
            padded += "#"
        smuggled = json.loads(self.changes_with_lock(padded))
        for addition in smuggled["additions"]:
            if addition["path"] == "charter.lock.yaml":
                addition["contents"] += base64.b64encode(("\n" + evil).encode()).decode()
        code, _, request, _ = self.build_request(self.REAL, raw=json.dumps(smuggled))
        self.assertNotEqual(code, 0)
        self.assertIsNone(request)
        blank_and_comments = "\n# a comment\n\n" + self.LOCK_TEXT + "\n"
        self.assertEqual(self.build_request(self.REAL, raw=self.changes_with_lock(blank_and_comments))[0], 0)

    def test_only_a_generated_pack_page_may_be_deleted_and_no_authored_page_is_touched(self) -> None:
        for path in ("packs/foundation.source.yaml", "packs/foundation/pack-manifest.yaml",
                     "tests/fixtures/valid/example-pack/pack-manifest.yaml", "docs/packs/index.md"):
            with self.subTest(deleted=path):
                self.assertIsNone(self.build_request(self.REAL, deletions=[path])[2])
        for page in ("docs/packs/index.md", "docs/packs/catalog-proposal.md"):
            with self.subTest(added=page):
                self.assertIsNone(self.build_request([*self.REAL, page])[2])

    def test_the_lock_and_the_changelog_are_rewritten_never_deleted(self) -> None:
        for kept in ("charter.lock.yaml", "docs/changelog/CHANGELOG.md"):
            with self.subTest(deleted=kept):
                code, output, request, _ = self.build_request(self.REAL, deletions=[kept])
                self.assertNotEqual(code, 0)
                self.assertIsNone(request)
                self.assertIn("::error::", output)

    def test_the_branch_is_the_releases_own_and_the_body_is_not_read_from_the_artifact(self) -> None:
        self.assertEqual(self.build["env"]["BRANCH"], "${{ steps.lookup.outputs.branch }}")
        self.assertEqual(self.push["env"]["BRANCH"], "${{ steps.lookup.outputs.branch }}")
        self.assertIn('branch="charter/service-release-$RELEASE_TAG"', self.lookup["run"])
        code, output, request, _ = self.build_request(self.REAL, branch="main")
        self.assertNotEqual(code, 0)
        self.assertIsNone(request)
        self.assertIn("::error::", output)
        # The body is written by the build step under RUNNER_TEMP, beside but never inside the artifact directory.
        self.assertIn('} > "$RUNNER_TEMP/pr.md"', self.build["run"])
        self.assertIn('--body-file "$RUNNER_TEMP/pr.md"', self.open["run"])
        download = next(step for step in self.steps if "uses" in step)
        self.assertEqual(download["with"]["path"], "${{ runner.temp }}/charter-bump")
        self.assertEqual(self.build["env"]["ARTIFACT"], "${{ runner.temp }}/charter-bump")

    def test_an_artifact_cut_from_another_commit_is_refused(self) -> None:
        # The head file holds this commit and nothing else: another commit, or this one plus a second line, is refused.
        cases = {"another commit": {"head": "b" * 40},
                 "a second line": {"head_file": "a" * 40 + "\n" + "b" * 40 + "\n"}}
        for name, kwargs in cases.items():
            with self.subTest(case=name):
                code, output, request, _ = self.build_request(self.REAL, **kwargs)
                self.assertNotEqual(code, 0)
                self.assertIsNone(request)
                self.assertIn("::error::", output)

    def test_the_body_states_each_jars_build_provenance(self) -> None:
        cases = {("verified", "verified"): (2, 0, False),
                 ("verified", "unverified"): (1, 1, True),
                 ("unverified", "unverified"): (0, 2, True)}
        for states, (verified, unverified, by_hand) in cases.items():
            with self.subTest(states=states):
                code, output, _, body = self.build_request(self.REAL, states=states)
                self.assertEqual(code, 0, output)
                self.assertEqual(body.count("verified against `spec-kitty/spec-kitty-charter`"), verified)
                self.assertEqual(body.count("**not verified**"), unverified)
                self.assertEqual("by hand" in body, by_hand)
        code, _, request, _ = self.build_request(self.REAL, states=("mismatch", "verified"))
        self.assertNotEqual(code, 0)  # never reached in a run (the bump needs a green provenance job), refused anyway
        self.assertIsNone(request)

    def test_only_contents_is_written_with_the_job_token_and_the_pat_lives_only_in_open(self) -> None:
        for step in (self.lookup, self.push, self.open):
            self.assertEqual(step["env"]["GH_TOKEN"], "${{ github.token }}")
        text = yaml.safe_dump(self.job)
        self.assertNotIn("CHARTER_BUMP_TOKEN", text)
        self.assertEqual(set(re.findall(r"secrets\.(\w+)", text)), {"PR_CREATION_TOKEN"})
        holders = [step.get("name") for step in self.steps if "PR_CREATION_TOKEN" in yaml.safe_dump(step.get("env", {}))]
        self.assertEqual(holders, ["Require PR_CREATION_TOKEN", "Open the bump pull request"])
        self.assertEqual(self.open["env"]["PR_TOKEN"], "${{ secrets.PR_CREATION_TOKEN }}")
        self.assertNotIn("uses", self.open)

    def test_the_pat_opens_and_closes_and_the_job_token_pushes_and_deletes(self) -> None:
        pat_lines = [line.strip() for line in self.open["run"].splitlines() if "$PR_TOKEN" in line]
        self.assertEqual(len(pat_lines), 3)
        self.assertTrue(any("gh pr create" in line for line in pat_lines))
        self.assertTrue(any('gh api -X PATCH "repos/$REPO/pulls/$number" -f state=closed' in line for line in pat_lines))
        self.assertTrue(any("gh pr comment" in line for line in pat_lines))
        self.assertNotIn("--delete-branch", self.open["run"])  # it needs Contents, which the PAT does not hold
        self.assertIn('if ! gh api -X DELETE "repos/$REPO/git/refs/heads/$old_branch"', self.open["run"])
        for step in (self.lookup, self.build, self.push, self.open):
            self.assertNotIn("gh workflow run", step["run"])
        # A bump pull request already open: the lookup exits before it writes go, so nothing is built, pushed or opened.
        skipped = {"steps": {"lookup": {"outputs": {}}, "push": {"outputs": {}}}}
        go = {"steps": {"lookup": {"outputs": {"go": "true"}}, "push": {"outputs": {"branch": "b"}}}}
        for step in (self.build, self.push, self.open):
            self.assertFalse(gh_expr.evaluate_if(step.get("if"), skipped))
            self.assertTrue(gh_expr.evaluate_if(step.get("if"), go))

    def test_a_superseded_pull_request_that_cannot_be_closed_or_cleaned_fails_the_job(self) -> None:
        def run(fail: str) -> tuple[int, list[str]]:
            with tempfile.TemporaryDirectory() as tmp:
                work = Path(tmp)
                (work / "bin").mkdir()
                gh = work / "bin" / "gh"
                gh.write_text(
                    "#!/usr/bin/env bash\n"
                    'echo "${GH_TOKEN}:$*" >> "$GH_LOG"\n'
                    'case "$*" in *"$FAIL"*) [[ -n "$FAIL" ]] && exit 1 ;; esac\n'
                    '[[ "$1 $2" == "pr create" ]] && echo https://example.invalid/pull/9\n'
                    "exit 0\n", encoding="utf-8")
                gh.chmod(0o755)
                (work / "open-prs.tsv").write_text("5\tcharter/service-release-service-v1.0.0\n"
                                                   "6\tcharter/service-release-service-v1.1.0\n", encoding="utf-8")
                (work / "pr.md").write_text("body\n", encoding="utf-8")
                log = work / "gh.log"
                log.touch()
                env = {**os.environ, "PATH": f"{work / 'bin'}:{os.environ['PATH']}", "GH_LOG": str(log), "FAIL": fail,
                       "GH_TOKEN": "job", "PR_TOKEN": "pat", "REPO": "spec-kitty/spec-kitty-open-packs",
                       "BRANCH": "charter/service-release-service-v2.0.0", "RELEASE_TAG": "service-v2.0.0",
                       "RUNNER_TEMP": tmp, "GITHUB_STEP_SUMMARY": str(work / "summary.md")}
                done = subprocess.run(["bash", "-c", self.open["run"]], env=env, capture_output=True, text=True)
                return done.returncode, log.read_text(encoding="utf-8").splitlines()
        code, calls = run("")
        self.assertEqual(code, 0)
        self.assertTrue(calls[0].startswith("pat:pr create"))
        self.assertIn("pat:api -X PATCH repos/spec-kitty/spec-kitty-open-packs/pulls/5 -f state=closed", calls)
        self.assertIn("job:api -X DELETE repos/spec-kitty/spec-kitty-open-packs/git/refs/heads/charter/service-release-service-v1.0.0", calls)
        self.assertIn("job:api -X DELETE repos/spec-kitty/spec-kitty-open-packs/git/refs/heads/charter/service-release-service-v1.1.0", calls)
        for fail in ("pulls/5", "refs/heads/charter/service-release-service-v1.0.0"):
            with self.subTest(failing=fail):
                code, calls = run(fail)
                self.assertEqual(code, 1)
                self.assertTrue(any("pulls/6" in call for call in calls))  # the others are still handled
        code, _ = run("pr comment")
        self.assertEqual(code, 0)  # a missing comment is only a warning
        code, calls = run("pr create")
        self.assertEqual(code, 1)
        self.assertEqual(len(calls), 1)

    def test_a_missing_secret_fails_loudly_before_anything_is_pushed(self) -> None:
        guard = self.steps[0]
        self.assertEqual(guard["name"], "Require PR_CREATION_TOKEN")
        self.assertEqual(guard["env"]["HAS_PR_TOKEN"], "${{ secrets.PR_CREATION_TOKEN != '' }}")
        for has, code in (("false", 1), ("true", 0)):
            with self.subTest(secret_set=has):
                done = subprocess.run(["bash", "-c", guard["run"]], env={**os.environ, "HAS_PR_TOKEN": has},
                                      capture_output=True, text=True)
                self.assertEqual(done.returncode, code)
                if code:
                    self.assertIn("::error::The repository secret PR_CREATION_TOKEN is not set", done.stdout)
        ctx = contexts(schedule_event())
        for secret, expected in (("", "false"), ("github_pat_x", "true")):
            ctx["secrets"] = {"PR_CREATION_TOKEN": secret}
            self.assertEqual(str(gh_expr.render(guard["env"]["HAS_PR_TOKEN"], ctx)).lower(), expected)


class CharterTrackProvenance(unittest.TestCase):
    """#310 item 1, after review cycle 1. Before a bump, a read-only job checks both release jars:
    - A jar that is not the pinned file (another SHA-256) is an integrity event: ::error::, and the job fails, so
      nothing is derived or published.
    - A build attestation that is missing or does not verify (signer workflow and tag pinned) is a warning only
      (operator ruling); the bump pull request says so."""

    SIGNER = "spec-kitty/spec-kitty-charter/.github/workflows/service-release.yml"

    def setUp(self) -> None:
        self.jobs = load(TRACK)["jobs"]
        self.job = self.jobs["provenance"]
        self.step = next(step for step in self.job["steps"] if step.get("id") == "verify")

    def test_it_reads_only_and_runs_no_repository_code(self) -> None:
        self.assertEqual(self.job["permissions"], {"contents": "read", "attestations": "read"})
        self.assertEqual(self.job["needs"], "resolve")
        text = yaml.safe_dump(self.job)
        self.assertNotIn("secrets.", text)
        self.assertNotIn("actions/checkout", text)
        self.assertNotIn("python", text)
        self.assertEqual(self.step["env"]["CHARTER"], "spec-kitty/spec-kitty-charter")
        # The states the bump body reports are the ones this step wrote, not a constant.
        build = next(s for s in self.jobs["bump"]["steps"] if s.get("id") == "build")
        for output, env in (("service", "ATTEST_SERVICE"), ("pack_check", "ATTEST_PACK_CHECK")):
            self.assertEqual(self.job["outputs"][output], f"${{{{ steps.verify.outputs.{output} }}}}")
            self.assertEqual(build["env"][env], f"${{{{ needs.provenance.outputs.{output} }}}}")

    def test_it_runs_exactly_when_the_bump_would_act_and_gates_derive_and_publish(self) -> None:
        for job_id in ("provenance", "derive", "bump"):
            condition = str(self.jobs[job_id]["if"])
            for part in ("needs.resolve.outputs.track == 'release'", "needs.resolve.outputs.act == 'true'",
                         "github.repository == 'spec-kitty/spec-kitty-open-packs'", "github.ref == 'refs/heads/main'"):
                with self.subTest(job=job_id, part=part):
                    self.assertIn(part, condition)
            self.assertNotIn("always()", condition)
            self.assertNotIn("cancelled()", condition)
        self.assertIn("provenance", self.jobs["derive"]["needs"])
        self.assertIn("provenance", self.jobs["bump"]["needs"])
        self.assertIn("needs.checks.result == 'success'", str(self.jobs["bump"]["if"]))

    def verify(self, *, download: str = "", attest: str = "", digest_ok: bool = True) -> tuple[int, str, str, str]:
        """Run the step with a stand-in gh: ``download`` / ``attest`` name the jar whose download / verification fails."""
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            (work / "bin").mkdir()
            log = work / "gh.log"
            gh = work / "bin" / "gh"
            gh.write_text(
                "#!/usr/bin/env bash\n"
                'echo "$*" >> "$GH_LOG"\n'
                'args="$*"\n'
                'if [[ "$1 $2" == "release download" ]]; then\n'
                '  jar="${args##*--pattern }"; jar="${jar%% *}"\n'
                '  [[ -n "$FAIL_DOWNLOAD" && "$jar" == *"$FAIL_DOWNLOAD"* ]] && exit 1\n'
                '  dir="${args##*--dir }"; dir="${dir%% *}"; mkdir -p "$dir"; printf "%s" "$jar" > "$dir/$jar"; exit 0\n'
                "fi\n"
                'if [[ "$1 $2" == "attestation verify" ]]; then\n'
                '  [[ -n "$FAIL_ATTEST" && "$3" == *"$FAIL_ATTEST"* ]] && { echo "no attestations found" >&2; exit 1; }\n'
                "  exit 0\n"
                "fi\n"
                "exit 3\n", encoding="utf-8")
            gh.chmod(0o755)
            digest = lambda name: hashlib.sha256(name.encode()).hexdigest()  # noqa: E731
            out, summary = work / "out", work / "summary"
            env = {**os.environ, "PATH": f"{work / 'bin'}:{os.environ['PATH']}", "RUNNER_TEMP": tmp,
                   "GITHUB_OUTPUT": str(out), "GITHUB_STEP_SUMMARY": str(summary), "GH_TOKEN": "job",
                   "GH_LOG": str(log), "CHARTER": "spec-kitty/spec-kitty-charter", "RELEASE_TAG": "service-v2.0.0",
                   "JAR_SHA256": digest("spec-kitty-charter-service-2.0.0.jar") if digest_ok else "0" * 64,
                   "PACK_CHECK_SHA256": digest("pack-check-2.0.0.jar"),
                   "FAIL_DOWNLOAD": download, "FAIL_ATTEST": attest}
            done = subprocess.run(["bash", "-c", self.step["run"]], env=env, capture_output=True, text=True, cwd=tmp)
            self.calls = log.read_text(encoding="utf-8").splitlines()
            return done.returncode, out.read_text(encoding="utf-8"), done.stdout, summary.read_text(encoding="utf-8")

    def test_both_verified_with_the_signer_workflow_and_tag(self) -> None:
        code, out, _, summary = self.verify()
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines(), ["service=verified", "pack_check=verified"])
        self.assertIn("pack-check-2.0.0.jar", summary)
        verifies = [call for call in self.calls if call.startswith("attestation verify")]
        self.assertEqual(len(verifies), 2)
        for call in verifies:
            self.assertIn(f"--signer-workflow {self.SIGNER}", call)
            self.assertIn("--source-ref refs/tags/service-v2.0.0", call)

    def test_a_missing_attestation_or_a_failed_download_warns_and_never_fails(self) -> None:
        cases = {"no attestation": ({"attest": "pack-check"}, ["service=verified", "pack_check=unverified"]),
                 "no download": ({"download": "service"}, ["service=unverified", "pack_check=verified"])}
        for name, (kwargs, expected) in cases.items():
            with self.subTest(case=name):
                code, out, stdout, _ = self.verify(**kwargs)
                self.assertEqual(code, 0)
                self.assertEqual(out.splitlines(), expected)
                self.assertIn("::warning::", stdout)
                self.assertNotIn("::error::", stdout)

    def test_a_jar_that_is_not_the_pinned_file_is_an_integrity_failure(self) -> None:
        code, out, stdout, summary = self.verify(digest_ok=False)
        self.assertEqual(code, 1)
        self.assertEqual(out.splitlines(), ["service=mismatch", "pack_check=verified"])
        self.assertIn("::error::", stdout)
        self.assertIn("mismatch", summary)
        self.assertFalse(any("attestation verify" in call and "service-2.0.0" in call for call in self.calls))


class CharterTrackNightlyMain(unittest.TestCase):
    """charter-track.yml's nightly main track (#311): charter main every night, report only, one charter:main-red issue."""

    MAIN = {"track": "main", "run": "true", "act": "false"}

    def setUp(self) -> None:
        self.workflow = load(TRACK)
        self.jobs = self.workflow["jobs"]
        self.runs = CharterTrack.runs.__get__(self)

    def resolve_env(self, event: dict[str, Any], name: str) -> str:
        step = next(step for step in self.jobs["resolve"]["steps"] if step.get("id") == "target")
        return str(gh_expr.render(step["env"][name], track_contexts(event, {}))).strip()

    def test_both_schedules_run_at_different_hours_and_the_jobs_name_the_nightly_one(self) -> None:
        crons = [entry["cron"] for entry in triggers(self.workflow)["schedule"]]
        self.assertEqual(crons, [RELEASE_CRON, NIGHTLY_CRON])
        self.assertNotEqual(RELEASE_CRON.split()[1], NIGHTLY_CRON.split()[1])
        text = (WORKFLOWS / TRACK).read_text(encoding="utf-8")
        named = set(gh_expr_crons(text))
        self.assertEqual(named, {NIGHTLY_CRON})  # no expression names a cron the schedule does not list
        self.assertIn("main", triggers(self.workflow)["workflow_dispatch"]["inputs"]["track"]["options"])

    def test_the_nightly_schedule_checks_charter_main_and_the_release_schedule_the_release_track(self) -> None:
        self.assertEqual(self.resolve_env(nightly_event(), "TRACK"), "main")
        self.assertEqual(self.resolve_env(nightly_event(), "CHARTER_REF"), "main")
        self.assertEqual(self.resolve_env(schedule_event(), "TRACK"), "release")
        dispatch = track_dispatch("main")
        dispatch["inputs"] = {**dispatch["inputs"], "charter_ref": "feature"}
        self.assertEqual(self.resolve_env(dispatch, "TRACK"), "main")
        self.assertEqual(self.resolve_env(dispatch, "CHARTER_REF"), "main")
        ref = track_dispatch("ref")
        ref["inputs"] = {**ref["inputs"], "charter_ref": "feature"}
        self.assertEqual(self.resolve_env(ref, "CHARTER_REF"), "feature")

    def test_it_runs_the_shared_checks_and_never_bumps_or_touches_the_release_issue(self) -> None:
        for event in (nightly_event(), track_dispatch("main")):
            for checks in ("success", "failure"):
                with self.subTest(event=event["event_name"], checks=checks):
                    self.assertTrue(self.runs("checks", event, self.MAIN))
                    self.assertTrue(self.runs("report", event, self.MAIN, checks))
                    for job in ("bump", "alert", "settle"):
                        self.assertFalse(self.runs(job, event, self.MAIN, checks), job)

    def test_on_main_a_red_run_keeps_one_issue_and_a_green_run_closes_it(self) -> None:
        for event in (nightly_event(), track_dispatch("main")):
            with self.subTest(event=event["event_name"]):
                self.assertTrue(self.runs("main-red", event, self.MAIN, checks="failure"))
                self.assertTrue(self.runs("main-red", event, self.MAIN, checks="success"))
                self.assertFalse(self.runs("main-red", event, self.MAIN, checks="cancelled"))

    def upkeep(self, open_issue: str, resolved: str, result: str, old_title: str = "") -> list[str]:
        """Run the main-red step under bash with a stub gh; return the gh calls it made."""
        script = self.jobs["main-red"]["steps"][-1]["run"]
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            (work / "bin").mkdir()
            (work / "scripts" / "ci").mkdir(parents=True)
            report = work / "scripts" / "ci" / "charter_track_report.sh"
            report.write_text("#!/usr/bin/env bash\necho '| Job | Conclusion |'\n", encoding="utf-8")
            report.chmod(0o755)
            gh = work / "bin" / "gh"
            gh.write_text(
                "#!/usr/bin/env bash\n"
                'echo "$*" >> "$GH_LOG"\n'
                'case "$1 $2" in\n'
                '  "issue list") printf %s "$OPEN_ISSUE" ;;\n'
                '  "issue view") printf %s "$OLD_TITLE" ;;\n'
                "esac\n", encoding="utf-8")
            gh.chmod(0o755)
            log = work / "gh.log"
            log.touch()
            env = {**os.environ, "PATH": f"{work / 'bin'}:{os.environ['PATH']}", "GH_LOG": str(log),
                   "OPEN_ISSUE": open_issue, "OLD_TITLE": old_title, "REPO": "spec-kitty/spec-kitty-open-packs",
                   "RUN_URL": "https://example.invalid/run/1", "RESOLVED": resolved, "RESULT": result,
                   "COMMIT": "d" * 40, "CURRENT": "service-v1.0.0", "GITHUB_SHA": "c" * 40,
                   "GITHUB_RUN_ID": "1", "RUNNER_TEMP": tmp}
            subprocess.run(["bash", "-c", script], cwd=work, env=env, check=True, capture_output=True)
            return log.read_text(encoding="utf-8").splitlines()

    def test_the_upkeep_keeps_exactly_one_charter_main_red_issue(self) -> None:
        def verbs(calls: list[str]) -> list[str]:
            return [" ".join(call.split()[:2]) for call in calls]
        # Red with none open: label it and open one.
        calls = self.upkeep("", "success", "failure")
        self.assertEqual(verbs(calls), ["issue list", "label create", "issue create"])
        self.assertIn("--label charter:main-red", calls[0])
        self.assertIn("--label charter:main-red", calls[2])
        self.assertIn("--title Charter main fails the packs", calls[2])
        # Red with one open: rewrite it, no second issue; a comment only when the title changes.
        calls = self.upkeep("12", "success", "failure", old_title="Charter main fails the packs")
        self.assertEqual(verbs(calls), ["issue list", "label create", "issue view", "issue edit"])
        calls = self.upkeep("12", "failure", "skipped", old_title="Charter main fails the packs")
        self.assertEqual(verbs(calls), ["issue list", "label create", "issue view", "issue edit", "issue comment"])
        self.assertIn("--title Charter track cannot resolve charter main", calls[3])
        # Green: close the open one, or do nothing.
        calls = self.upkeep("12", "success", "success")
        self.assertEqual(verbs(calls), ["issue list", "issue close"])
        self.assertTrue(calls[1].startswith("issue close 12 "))
        self.assertEqual(verbs(self.upkeep("", "success", "success")), ["issue list"])
        for calls in (self.upkeep("", "success", "failure"), self.upkeep("12", "success", "success")):
            self.assertFalse(any("release-red" in call.split("--body")[0] for call in calls))

    def test_nothing_is_opened_or_closed_off_main_in_a_fork_or_by_another_track(self) -> None:
        cases = {
            "a dispatch on a branch": (track_dispatch("main", "refs/heads/issue-311"), self.MAIN),
            "a fork's nightly": ({**nightly_event(), "repository": "someone/spec-kitty-open-packs"}, self.MAIN),
            "the release track": (schedule_event(), CharterTrack.RELEASE),
            "the on-demand track": (track_dispatch("ref"), {"track": "ref", "run": "true", "act": "false"}),
            "a labelled pull request": (pr_event(labels=("charter:head",)), {"track": "ref", "run": "true", "act": "false"}),
        }
        for name, (event, resolved) in cases.items():
            for checks in ("success", "failure"):
                with self.subTest(case=name, checks=checks):
                    self.assertFalse(self.runs("main-red", event, resolved, checks))

    def test_a_nightly_run_that_cannot_resolve_charter_main_says_so_on_its_own_issue(self) -> None:
        for event in (nightly_event(), track_dispatch("main")):
            with self.subTest(event=event["event_name"]):
                self.assertTrue(self.runs("main-red", event, {}, checks="skipped", resolve="failure"))
                self.assertFalse(self.runs("alert", event, {}, checks="skipped", resolve="failure"))
        self.assertTrue(self.runs("alert", schedule_event(), {}, checks="skipped", resolve="failure"))
        for event in (schedule_event(), track_dispatch("ref"), track_dispatch("release")):
            with self.subTest(event=event["event_name"], track=event.get("inputs", {}).get("track")):
                self.assertFalse(self.runs("main-red", event, {}, checks="skipped", resolve="failure"))

    def test_nightly_runs_queue_on_their_own_and_never_with_the_release_track(self) -> None:
        def group(event: dict[str, Any]) -> tuple[str, bool]:
            ctx = track_contexts(event, {})
            block = self.workflow["concurrency"]
            return (str(gh_expr.render(block["group"], ctx)),
                    gh_expr._truthy(gh_expr.render(block["cancel-in-progress"], ctx)))
        nightly, dispatched = group(nightly_event()), group(track_dispatch("main"))
        self.assertEqual(nightly, dispatched)
        self.assertFalse(nightly[1])
        self.assertNotEqual(nightly[0], group(schedule_event())[0])
        self.assertNotEqual(nightly[0], group(track_dispatch("ref"))[0])


class CharterTrackReport(unittest.TestCase):
    """scripts/ci/charter_track_report.sh reads each failed job's log, as the runner's gh allows (#323)."""

    REPORT = ROOT / "scripts" / "ci" / "charter_track_report.sh"
    # A job log as the API serves it: ANSI colour codes around the step echo and inside an error annotation.
    LOG = ("2026-11-20T02:28:06.1Z \x1b[36;1mpython3 scripts/validate.py\x1b[0m\n"
           "2026-11-20T02:28:06.2Z ##[error]foundation/directive.graph.yaml: \x1b[31m'in_tension_with'\x1b[0m is `bad`\n"
           # An OSC hyperlink, closed once by BEL and once by ESC \: the payload goes, the text stays.
           "2026-11-20T02:28:06.3Z ##[error]see \x1b]8;;https://osc.invalid/a\x07the run\x1b]8;;\x1b\\ for more\n"
           "2026-11-20T02:28:06.4Z ##[error]Process completed with exit code 1.\n")
    JOBS = ("11\tfailure\tCharter checks / Charter Pack validation\n"
            "12\tsuccess\tCharter checks / Charter service validation\n"
            "13\tfailure\tReport\n")

    def report(self, gh_mode: str) -> subprocess.CompletedProcess[str]:
        """Run the report against a stub gh. gh_mode: "strict" refuses escape sequences unless
        --allow-escape-sequences is passed (the runner's gh); "old" has no such flag and prints them;
        "denied" fails every log read."""
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            (work / "bin").mkdir()
            (work / "log.txt").write_text(self.LOG, encoding="utf-8")
            (work / "jobs.tsv").write_text(self.JOBS, encoding="utf-8")
            gh = work / "bin" / "gh"
            gh.write_text(
                "#!/usr/bin/env bash\n"
                'if [[ "$*" == "api --help" ]]; then\n'
                '  [[ "$GH_MODE" == old ]] && echo "  --jq string" || echo "  --allow-escape-sequences   Output escape sequences"\n'
                "  exit 0\n"
                "fi\n"
                'case "$*" in\n'
                '  *"/runs/"*"/jobs"*) cat "$WORK/jobs.tsv" ;;\n'
                '  *"/logs")\n'
                '    if [[ "$GH_MODE" == denied ]]; then echo "gh: Resource not accessible by integration (HTTP 403)" >&2; exit 1; fi\n'
                '    if [[ "$GH_MODE" == strict && "$*" != *--allow-escape-sequences* ]]; then\n'
                '      echo "the response contains terminal escape sequences; pass --allow-escape-sequences to output it anyway" >&2\n'
                "      exit 1\n"
                "    fi\n"
                '    if [[ "$GH_MODE" == old && "$*" == *--allow-escape-sequences* ]]; then echo "unknown flag: --allow-escape-sequences" >&2; exit 1; fi\n'
                '    printf "%b" "$(cat "$WORK/log.txt")" ;;\n'
                "  *) echo \"unexpected: $*\" >&2; exit 1 ;;\n"
                "esac\n", encoding="utf-8")
            gh.chmod(0o755)
            env = {**os.environ, "PATH": f"{work / 'bin'}:{os.environ['PATH']}", "WORK": str(work), "GH_MODE": gh_mode,
                   "GITHUB_REPOSITORY": "spec-kitty/spec-kitty-open-packs"}
            return subprocess.run(["bash", str(self.REPORT), "1"], env=env, capture_output=True, text=True, check=True)

    def test_the_errors_of_a_failed_job_are_quoted_whichever_gh_reads_the_log(self) -> None:
        for mode in ("strict", "old"):
            with self.subTest(gh=mode):
                out = self.report(mode).stdout
                self.assertIn("| Charter Pack validation | failure |", out)
                self.assertIn("| Charter service validation | success |", out)
                self.assertNotIn("Report", out)  # only the called gate's jobs
                self.assertIn("#### Charter Pack validation: errors", out)
                self.assertIn("foundation/directive.graph.yaml: 'in_tension_with' is 'bad'", out)
                self.assertIn("Process completed with exit code 1.", out)
                self.assertNotIn("could not be read", out)
                self.assertIn("see the run for more", out)
                self.assertNotIn("osc.invalid", out)  # an OSC sequence goes with its payload
                self.assertNotIn("\x1b", out)  # no escape sequence reaches the issue
                self.assertNotIn("\x07", out)
                self.assertEqual(out.count("```"), 2)  # one fence, opened and closed

    def test_a_log_that_cannot_be_read_says_why(self) -> None:
        done = self.report("denied")
        self.assertIn("(the job log could not be read; see the run)", done.stdout)
        self.assertIn("Resource not accessible by integration (HTTP 403)", done.stdout)
        self.assertIn("job 11 log: gh: Resource not accessible by integration (HTTP 403)", done.stderr)
        self.assertEqual(done.stdout.count("```"), 2)


def gh_expr_crons(text: str) -> list[str]:
    """Every cron string a workflow expression compares github.event.schedule with."""
    return re.findall(r"github\.event\.schedule [!=]= '([^']+)'", text)


class GateVerdict(unittest.TestCase):
    """The gate's own scripts, run under bash against each verdict of the validation job."""

    def setUp(self) -> None:
        self.workflow = load("validate-packs.yml")

    def test_only_a_successful_validation_passes_the_gate(self) -> None:
        for label, github in (("a pull request", pr_event()), ("a push to main", push_event())):
            for validate in ("skipped", "failure", "cancelled", "success"):
                with self.subTest(event=label, validate=validate):
                    expected = "success" if validate == "success" else "failure"
                    self.assertEqual(run_gate(self.workflow, github, validate), expected)

    def test_only_a_successful_service_validation_passes_the_gate(self) -> None:
        # The charter service job is as required as the validation job: either one red, skipped or
        # cancelled fails the gate, on a pull request and on main.
        for label, github in (("a pull request", pr_event()), ("a push to main", push_event())):
            for service in ("skipped", "failure", "cancelled", "success"):
                with self.subTest(event=label, service=service):
                    expected = "success" if service == "success" else "failure"
                    self.assertEqual(run_gate(self.workflow, github, "success", service=service), expected)

    def test_a_pause_label_on_the_pull_request_now_fails_the_gate_even_when_validation_passed(self) -> None:
        # The run's payload predates the label (a re-run, or another label's run): only the API knows.
        for labels in ((PAUSE_LABEL,), ("docs", PAUSE_LABEL), ("PR:Pause-CI",)):
            with self.subTest(labels=labels):
                self.assertEqual(run_gate(self.workflow, pr_event(), "success", labels_now=labels), "failure")

    def test_other_labels_do_not_pause(self) -> None:
        for labels in ((), ("docs",), (f"x{PAUSE_LABEL}", f"{PAUSE_LABEL}-not")):
            with self.subTest(labels=labels):
                self.assertEqual(run_gate(self.workflow, pr_event(), "success", labels_now=labels), "success")

    def test_an_unreadable_label_list_fails_the_gate_closed(self) -> None:
        self.assertEqual(run_gate(self.workflow, pr_event(), "success", api="down"), "failure")

    def test_main_and_dispatch_runs_never_read_the_labels(self) -> None:
        for github in (push_event(), dispatch_event()):
            self.assertEqual(run_gate(self.workflow, github, "success", api="down"), "success")


class ConcurrencyKeepsMainRunsApart(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = load(WORKFLOW)

    def test_main_and_release_runs_never_cancel_or_displace_each_other(self) -> None:
        non_pr = [concurrency(self.workflow, github) for github in (
            push_event(run_id=3001),
            push_event(run_id=3002), push_event("refs/tags/v1.2.3", 3003), dispatch_event(4001))]
        self.assertEqual(len({group for group, _ in non_pr}), len(non_pr),
                         "a pending run in a shared group is replaced by the next one")
        self.assertNotIn(concurrency(self.workflow, pr_event())[0], {group for group, _ in non_pr})
        self.assertFalse(any(cancel for _, cancel in non_pr))

    def test_a_new_push_to_a_pr_supersedes_its_running_check(self) -> None:
        first, second = concurrency(self.workflow, pr_event(run_id=1)), concurrency(self.workflow, pr_event(run_id=2))
        self.assertEqual(first[0], second[0])
        self.assertTrue(second[1])
        self.assertNotEqual(first[0], concurrency(self.workflow, pr_event(number=8))[0])


class PauseLabelGuard(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = load(WORKFLOW)

    def test_label_changes_re_run_ci(self) -> None:
        types = set((triggers(self.workflow)["pull_request"] or {}).get("types", DEFAULT_PR_TYPES))
        self.assertLessEqual(DEFAULT_PR_TYPES | {"labeled", "unlabeled"}, types)

    def test_a_paused_pr_skips_the_work_and_its_required_check_is_red(self) -> None:
        gate_id, _ = job_named(self.workflow, GATE)
        for label, github in PAUSED_EVENTS.items():
            results = simulate(self.workflow, github)
            with self.subTest(event=label):
                self.assertEqual(results[gate_id], "failure", "a paused PR must never read as green")
                for job_id, result in results.items():
                    if job_id != gate_id:
                        self.assertEqual(result, "skipped", f"{job_id} ran while paused")

    def test_the_pause_label_cancels_the_running_check_and_other_labels_do_not(self) -> None:
        real = concurrency(self.workflow, pr_event())
        for github in (pr_event("labeled", (PAUSE_LABEL,), PAUSE_LABEL), pr_event("unlabeled", (), PAUSE_LABEL)):
            self.assertEqual(concurrency(self.workflow, github), real)
        for github in (pr_event("labeled", ("docs",), "docs"), pr_event("unlabeled", (), "docs")):
            self.assertNotEqual(concurrency(self.workflow, github)[0], real[0],
                                "another label's run would cancel a real run")


LEVELS = {"none": 0, "read": 1, "write": 2}


def granted(permissions: Any, scope: str) -> int:
    if permissions is None:
        return LEVELS["write"]  # unset: the repository default, which a test cannot see; assume enough
    if isinstance(permissions, str):
        return {"read-all": 1, "write-all": 2}.get(permissions, 0)
    return LEVELS.get(permissions.get(scope, "none"), 0)


class ReusableWorkflowCallsStart(unittest.TestCase):
    def test_a_caller_grants_every_permission_its_called_workflow_asks_for(self) -> None:
        # A called job cannot hold more than the calling job grants: GitHub refuses to start the
        # run, so a release would fail before it validates anything.
        for path in sorted(WORKFLOWS.glob("*.yml")):
            caller = yaml.safe_load(path.read_text(encoding="utf-8"))
            for job_id, job in caller["jobs"].items():
                uses = job.get("uses", "")
                if not uses.startswith("./.github/workflows/"):
                    continue
                allowed = job.get("permissions", caller.get("permissions"))
                called = load(Path(uses).name)
                for called_id, called_job in called["jobs"].items():
                    asked = called_job.get("permissions", called.get("permissions")) or {}
                    for scope in asked if isinstance(asked, dict) else ():
                        with self.subTest(caller=f"{path.name}:{job_id}", called=f"{uses}:{called_id}",
                                          scope=scope):
                            self.assertGreaterEqual(granted(allowed, scope), LEVELS[asked[scope]])


class ReleaseChecksDigestsBeforeBuilding(unittest.TestCase):
    def test_the_digest_check_runs_before_any_asset_is_built(self) -> None:
        steps = load("release.yml")["jobs"]["release"]["steps"]
        runs = [step.get("run", "") for step in steps]
        check = next(i for i, run in enumerate(runs) if "scripts/ci/pack_digest.py --check" in run)
        build = next(i for i, run in enumerate(runs) if "release_assets.py build" in run)
        self.assertLess(check, build)


class ActionsArePinned(unittest.TestCase):
    def test_every_external_action_is_pinned_to_a_full_commit_sha(self) -> None:
        # A tag can be moved to other code; a full commit SHA cannot.
        for path in sorted(WORKFLOWS.glob("*.yml")):
            workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
            for job_id, job in workflow["jobs"].items():
                for step in job.get("steps", []):
                    uses = step.get("uses")
                    if not uses or uses.startswith(("./", "docker://")):
                        continue
                    with self.subTest(workflow=path.name, job=job_id, uses=uses):
                        self.assertRegex(uses, r"@[0-9a-f]{40}$")


class WorkflowExpressionsEvaluate(unittest.TestCase):
    """Every workflow's expressions parse, so the evaluator above covers what the workflows use."""

    def test_every_expression_parses(self) -> None:
        for path in sorted(WORKFLOWS.glob("*.yml")):
            workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
            for expression in gh_expr.expressions_in(workflow):
                with self.subTest(workflow=path.name, expression=expression.strip()):
                    gh_expr.evaluate(expression, contexts(pr_event(), {j: "success" for j in workflow["jobs"]}))


class EvaluatorSemantics(unittest.TestCase):
    def test_operators_return_operands_and_short_circuit(self) -> None:
        ctx = contexts(push_event())
        self.assertEqual(gh_expr.evaluate("github.event_name == 'push' && 'q' || 'p'", ctx), "q")
        self.assertEqual(gh_expr.evaluate("format('{0}-{1}', 'a', 2)", ctx), "a-2")
        self.assertTrue(gh_expr.evaluate("github.event_name == 'PUSH'", ctx))
        # Guarded: the right side is never read.
        self.assertFalse(gh_expr.evaluate(
            "github.event_name == 'pull_request' && github.event.pull_request.number", ctx, strict_event=True))
        with self.assertRaises(gh_expr.ExpressionError):
            gh_expr.evaluate("github.event.pull_request.number", ctx, strict_event=True)

    def test_object_filter_and_contains(self) -> None:
        ctx = contexts(pr_event(labels=("a", PAUSE_LABEL)))
        self.assertTrue(gh_expr.evaluate(
            "contains(github.event.pull_request.labels.*.name, 'pr:pause-ci')", ctx))
        self.assertFalse(gh_expr.evaluate("contains(github.event.pull_request.labels.*.name, 'b')", ctx))

    def test_mixed_types_compare_as_numbers_and_format_escapes(self) -> None:
        ctx = contexts(pr_event())
        self.assertTrue(gh_expr.evaluate("null == 0", ctx))
        self.assertTrue(gh_expr.evaluate("github.event.pull_request.number == '7'", ctx))
        self.assertEqual(gh_expr.evaluate("format('{{{0}}}', 'x')", ctx), "{x}")
        self.assertTrue(gh_expr.evaluate("GitHub.Event_Name == 'pull_request'", ctx))

    def test_if_without_a_status_function_implies_success(self) -> None:
        ctx = contexts(pr_event())
        self.assertFalse(gh_expr.evaluate_if(True, ctx, status={"success": False, "failure": True,
                                                                "cancelled": False}))
        self.assertFalse(gh_expr.evaluate_if("true", ctx, status={"success": False, "failure": True,
                                                                  "cancelled": False}))
        self.assertTrue(gh_expr.evaluate_if("always()", ctx, status={"success": False, "failure": True,
                                                                     "cancelled": False}))


if __name__ == "__main__":
    unittest.main()
