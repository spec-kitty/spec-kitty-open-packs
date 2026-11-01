"""The workflows behind the required checks are merge-queue ready and honour `pr:pause-ci`.

These are property tests over the parsed workflow files: each event a run can start from (a pull
request push, a label change, a merge-queue entry, a push to main, a release's call) is simulated, and
the workflow's own expressions are evaluated against it with `gh_expr`. They assert what the merge queue
and the pause label need, not how the YAML spells it.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gh_expr  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"

# The checks the operator requires on `main`, by workflow file and check (job) name. The operator
# documentation in docs/guides/contributing.md names the same checks.
REQUIRED_CHECKS = {"validate-packs.yml": "Validate packs gate"}

PAUSE_LABEL = "pr:pause-ci"
DEFAULT_PR_TYPES = {"opened", "synchronize", "reopened"}


def load(name: str) -> dict[str, Any]:
    return yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))


def triggers(workflow: dict[str, Any]) -> dict[str, Any]:
    # YAML 1.1 reads the bare key `on` as the boolean true.
    on = workflow.get("on", workflow.get(True))
    if isinstance(on, str):
        return {on: None}
    if isinstance(on, list):
        return {name: None for name in on}
    return dict(on or {})


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


def merge_group_event(run_id: int = 2001, pr: int = 7) -> dict[str, Any]:
    head = "c" * 40
    return {
        "event_name": "merge_group",
        "event": {"action": "checks_requested",
                  "merge_group": {"base_sha": "b" * 40, "head_sha": head,
                                  "head_ref": f"refs/heads/gh-readonly-queue/main/pr-{pr}-{head}",
                                  "base_ref": "refs/heads/main"}},
        "ref": f"refs/heads/gh-readonly-queue/main/pr-{pr}-{head}",
        "run_id": run_id,
    }


def push_event(ref: str = "refs/heads/main", run_id: int = 3001) -> dict[str, Any]:
    return {"event_name": "push", "event": {"ref": ref, "before": "b" * 40, "after": "c" * 40},
            "ref": ref, "run_id": run_id}


def dispatch_event(run_id: int = 4001) -> dict[str, Any]:
    return {"event_name": "workflow_dispatch", "event": {"ref": "refs/heads/main", "inputs": {}},
            "ref": "refs/heads/main", "run_id": run_id}


def contexts(github: dict[str, Any], needs: dict[str, str] | None = None) -> dict[str, Any]:
    github = {"repository": "spec-kitty/spec-kitty-open-packs", "workflow": "Validate packs",
              "sha": "c" * 40, **github}
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
    "a merge-queue entry": merge_group_event(),
    "a push to main": push_event(),
    "a release calling the workflow": push_event("refs/tags/v1.2.3"),
    "a manual dispatch": dispatch_event(),
}
NON_PR_EVENTS = {
    "a merge-queue entry": merge_group_event(),
    "a push to main": push_event(),
    "a release calling the workflow": push_event("refs/tags/v1.2.3"),
    "a manual dispatch": dispatch_event(),
}


def concurrency(workflow: dict[str, Any], github: dict[str, Any]) -> tuple[str, bool] | None:
    block = workflow.get("concurrency")
    if block is None:
        return None
    if isinstance(block, str):
        return gh_expr.render(block, contexts(github)), False
    group = gh_expr.render(block["group"], contexts(github))
    cancel = gh_expr.render(block.get("cancel-in-progress", False), contexts(github))
    return str(group), gh_expr._truthy(cancel)


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


_NEEDS_RESULT = re.compile(r"needs\.[A-Za-z0-9_-]+\.result")
_SHELL_BRANCH = re.compile(r"^\s*(?:(?:if|elif|case|while|until|for|test)\b|\[)|\|\||&&")


def fails_unconditionally(run: str) -> bool:
    """A step script that ends in a non-zero `exit` (or `false`) with no branch before it always fails."""
    lines = [line.strip() for line in run.strip().splitlines() if line.strip() and not line.strip().startswith("#")]
    if not lines or any(_SHELL_BRANCH.search(line) for line in lines):
        return False
    return lines[-1] == "false" or bool(re.fullmatch(r"exit\s+([1-9][0-9]*)", lines[-1]))


def simulate(workflow: dict[str, Any], github: dict[str, Any]) -> dict[str, str]:
    """Each job's result for one event, assuming the real work succeeds.

    A job fails when a step that runs ends in an unconditional `exit 1`, or when a step that runs
    reads a `needs.<job>.result` that is not `success` (the gate's verdict). Everything else passes.
    """
    results: dict[str, str] = {}
    pending = dict(workflow["jobs"])
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
                continue
            results[job_id] = "success"
            for step in job.get("steps", []):
                failed = results[job_id] == "failure"
                step_status = {"success": not failed, "failure": failed, "cancelled": False}
                if not gh_expr.evaluate_if(step.get("if"), contexts(github, upstream), status=step_status):
                    continue
                if fails_unconditionally(str(step.get("run", ""))):
                    results[job_id] = "failure"
                for expression in gh_expr.expressions_in(step):
                    if _NEEDS_RESULT.search(expression):
                        if gh_expr.evaluate(expression, contexts(github, upstream)) != "success":
                            results[job_id] = "failure"
    return results


class RequiredChecksAreMergeQueueReady(unittest.TestCase):
    def test_required_check_workflows_run_on_every_merge_queue_entry(self) -> None:
        for name in REQUIRED_CHECKS:
            on = triggers(load(name))
            with self.subTest(workflow=name):
                self.assertIn("merge_group", on, "the queue would wait for a check that never starts")
                types = (on["merge_group"] or {}).get("types", ["checks_requested"])
                self.assertIn("checks_requested", types)

    def test_required_check_workflows_are_not_filtered_away(self) -> None:
        # A filtered trigger never posts its check on a change outside the filter, and a required
        # check that never reports blocks the PR (or evicts it from the queue at the timeout).
        for name in REQUIRED_CHECKS:
            on = triggers(load(name))
            for event in ("pull_request", "merge_group"):
                config = on.get(event) or {}
                for key in ("paths", "paths-ignore", "branches", "branches-ignore"):
                    with self.subTest(workflow=name, event=event, filter=key):
                        self.assertNotIn(key, config)

    def test_the_required_check_reports_on_every_event(self) -> None:
        for name, check in REQUIRED_CHECKS.items():
            workflow = load(name)
            job_id, _ = job_named(workflow, check)
            for label, github in {**RUNNING_EVENTS, **PAUSED_EVENTS}.items():
                with self.subTest(workflow=name, event=label):
                    self.assertNotEqual(simulate(workflow, github)[job_id], "skipped")

    def test_no_expression_reads_a_pull_request_field_on_a_queue_or_main_run(self) -> None:
        # Strict mode fails any read of a payload field the event does not carry, unless a guard
        # such as `github.event_name == 'pull_request' &&` short-circuits it first. A skipped job or
        # step is not evaluated past its `if`, as on GitHub.
        for name in REQUIRED_CHECKS:
            workflow = load(name)
            for label, github in NON_PR_EVENTS.items():
                for expression in reachable_expressions(workflow, github):
                    with self.subTest(workflow=name, event=label, expression=expression.strip()):
                        gh_expr.evaluate(expression, contexts(github, {j: "success" for j in workflow["jobs"]}),
                                         strict_event=True)

    def test_validation_passes_through_the_queue_when_it_passes(self) -> None:
        for name, check in REQUIRED_CHECKS.items():
            workflow = load(name)
            job_id, _ = job_named(workflow, check)
            for label, github in RUNNING_EVENTS.items():
                with self.subTest(workflow=name, event=label):
                    self.assertEqual(simulate(workflow, github)[job_id], "success")

    def test_the_required_check_covers_the_generated_pack_pages(self) -> None:
        # The queue tests PRs combined; two pack PRs that each re-seed docs/packs/ can drift together.
        # The drift check must run in a job the required check depends on, on every unpaused event.
        for name, check in REQUIRED_CHECKS.items():
            workflow = load(name)
            _, gate = job_named(workflow, check)
            needs = gate.get("needs", [])
            needs = [needs] if isinstance(needs, str) else needs
            for label, github in RUNNING_EVENTS.items():
                with self.subTest(workflow=name, event=label):
                    ran = [step for job_id in needs
                           if gh_expr.evaluate_if(workflow["jobs"][job_id].get("if"), contexts(github))
                           for step in workflow["jobs"][job_id].get("steps", [])
                           if "gen_pack_reference.py --check" in str(step.get("run", "")).split("#")[0]
                           and gh_expr.evaluate_if(step.get("if"), contexts(github))]
                    self.assertTrue(ran, "no drift check runs under the required check")


class ConcurrencyKeepsQueueAndMainRunsApart(unittest.TestCase):
    def setUp(self) -> None:
        self.workflows = {name: load(name) for name in REQUIRED_CHECKS}

    def test_queue_main_and_release_runs_never_cancel_or_displace_each_other(self) -> None:
        for name, workflow in self.workflows.items():
            runs = [merge_group_event(2001, 7), merge_group_event(2002, 8), push_event(run_id=3001),
                    push_event(run_id=3002), push_event("refs/tags/v1.2.3", 3003), dispatch_event(4001),
                    pr_event()]
            groups = [concurrency(workflow, github) for github in runs]
            if groups[0] is None:
                continue  # no concurrency block: nothing is cancelled or held back
            with self.subTest(workflow=name):
                non_pr = groups[:-1]
                self.assertEqual(len({group for group, _ in non_pr}), len(non_pr),
                                 "a pending run in a shared group is replaced by the next one")
                self.assertNotIn(groups[-1][0], {group for group, _ in non_pr})
                self.assertFalse(any(cancel for _, cancel in non_pr))

    def test_a_new_push_to_a_pr_supersedes_its_running_check(self) -> None:
        for name, workflow in self.workflows.items():
            first, second = concurrency(workflow, pr_event(run_id=1)), concurrency(workflow, pr_event(run_id=2))
            with self.subTest(workflow=name):
                self.assertIsNotNone(first, "without a concurrency group a paused PR's running check is never cancelled")
                self.assertEqual(first[0], second[0])
                self.assertTrue(second[1])
                self.assertNotEqual(first[0], concurrency(workflow, pr_event(number=8))[0])


class PauseLabelGuard(unittest.TestCase):
    def setUp(self) -> None:
        self.workflows = {name: load(name) for name in REQUIRED_CHECKS}

    def test_label_changes_re_run_ci(self) -> None:
        for name, workflow in self.workflows.items():
            types = set((triggers(workflow)["pull_request"] or {}).get("types", DEFAULT_PR_TYPES))
            with self.subTest(workflow=name):
                self.assertLessEqual(DEFAULT_PR_TYPES | {"labeled", "unlabeled"}, types)

    def test_a_paused_pr_skips_the_work_and_its_required_check_is_red(self) -> None:
        for name, check in REQUIRED_CHECKS.items():
            workflow = load(name)
            gate_id, _ = job_named(workflow, check)
            for label, github in PAUSED_EVENTS.items():
                results = simulate(workflow, github)
                with self.subTest(workflow=name, event=label):
                    self.assertEqual(results[gate_id], "failure", "a paused PR must never read as green")
                    for job_id, result in results.items():
                        if job_id != gate_id:
                            self.assertEqual(result, "skipped", f"{job_id} ran while paused")

    def test_the_label_is_ignored_off_pull_requests(self) -> None:
        # A queue entry, main and a release carry no labels; nothing there may read as paused.
        for name, check in REQUIRED_CHECKS.items():
            workflow = load(name)
            gate_id, _ = job_named(workflow, check)
            for label, github in NON_PR_EVENTS.items():
                results = simulate(workflow, github)
                with self.subTest(workflow=name, event=label):
                    self.assertTrue(all(result == "success" for result in results.values()), results)

    def test_the_pause_label_cancels_the_running_check_and_other_labels_do_not(self) -> None:
        for name, workflow in self.workflows.items():
            real = concurrency(workflow, pr_event())
            with self.subTest(workflow=name):
                self.assertIsNotNone(real, "adding the pause label must cancel the running check")
                for github in (pr_event("labeled", (PAUSE_LABEL,), PAUSE_LABEL),
                               pr_event("unlabeled", (), PAUSE_LABEL)):
                    self.assertEqual(concurrency(workflow, github), real)
                for github in (pr_event("labeled", ("docs",), "docs"), pr_event("unlabeled", (), "docs")):
                    other = concurrency(workflow, github)
                    self.assertNotEqual(other[0], real[0], "another label's run would cancel a real run")


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
        ctx = contexts(merge_group_event())
        self.assertEqual(gh_expr.evaluate("github.event_name == 'merge_group' && 'q' || 'p'", ctx), "q")
        self.assertEqual(gh_expr.evaluate("format('{0}-{1}', 'a', 2)", ctx), "a-2")
        self.assertTrue(gh_expr.evaluate("github.event_name == 'MERGE_GROUP'", ctx))
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
