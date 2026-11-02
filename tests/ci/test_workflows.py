"""The workflows behind the required checks are always reported and honour `pr:pause-ci`.

These are property tests over the parsed workflow files: each event a run can start from (a pull
request push, a label change, a push to main, a release's call) is simulated, and
the workflow's own expressions are evaluated against it with `gh_expr`. They assert what the required check
and the pause label need, not how the YAML spells it.
"""

from __future__ import annotations

import os
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
             labels_now: tuple[str, ...] = (), api: str = "ok") -> str:
    """Run the gate job's real step scripts under bash and return its result.

    `validate` is the `needs.validate.result` the gate sees. `labels_now` is what the API reports for
    the pull request when the gate asks, which can differ from the run's payload; `api="down"` makes
    the call fail. Steps are chosen by their own `if`, and a failed step skips the ones after it.
    """
    _, gate = job_named(workflow, GATE)
    ctx = contexts(github, {"validate": validate})
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
                results[job_id] = run_gate(workflow, github, upstream["validate"], labels_now=payload_labels)
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
                ran = [step for job_id in needs
                       if gh_expr.evaluate_if(self.workflow["jobs"][job_id].get("if"), contexts(github))
                       for step in self.workflow["jobs"][job_id].get("steps", [])
                       if "gen_pack_reference.py --check" in str(step.get("run", "")).split("#")[0]
                       and gh_expr.evaluate_if(step.get("if"), contexts(github))]
                self.assertTrue(ran, "no drift check runs under the required check")


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
