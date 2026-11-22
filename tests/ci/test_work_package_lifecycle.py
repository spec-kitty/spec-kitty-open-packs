"""The foundation work-package lifecycle names the guards core enforces on each transition (#291).

Operator ruling (2026-11-21): declare ``dependency-ready``, ``implementation-ready``,
``review-approved`` and ``review-ref`` where core's status model checks them; leave
``transition-context-complete`` undeclared; split the ``start`` and ``reset`` entries per source
lane so each guard sits only on the edges core checks.
"""

from __future__ import annotations

import unittest
from collections import Counter
from pathlib import Path

import yaml

FOUNDATION = Path(__file__).resolve().parents[2] / "packs" / "foundation"
LIFECYCLE = FOUNDATION / "lifecycles" / "work-package.lifecycle.yaml"
GUARDS = FOUNDATION / "guards"

NON_TERMINAL = ("planned", "claimed", "in_progress", "for_review", "in_review", "approved", "blocked")

#: (from, to) -> (event, the guard refs in order); every entry blocks.
EXPECTED_EDGES: dict[tuple[str, str], tuple[str | None, list[str]]] = {
    ("planned", "claimed"): ("claim", ["dependency-ready"]),
    ("claimed", "in_progress"): ("start", ["dependency-ready"]),
    ("blocked", "in_progress"): ("start", []),
    ("in_progress", "for_review"): (None, ["implementation-ready", "spec-kitty-pre-review"]),
    ("for_review", "in_review"): ("start_review", []),
    ("in_progress", "approved"): ("approve", ["review-approved"]),
    ("in_review", "approved"): ("approve", ["review-approved"]),
    ("in_review", "done"): ("complete", ["review-approved"]),
    ("approved", "done"): ("complete", ["review-approved"]),
    ("in_review", "in_progress"): ("changes_requested", ["review-ref"]),
    ("approved", "in_progress"): ("changes_requested", ["review-ref"]),
    ("in_progress", "planned"): ("reset", []),
    ("in_review", "planned"): ("reset", []),
    ("approved", "planned"): ("reset", ["review-ref"]),
    **{(lane, "blocked"): ("block", []) for lane in NON_TERMINAL if lane != "blocked"},
    **{(lane, "canceled"): ("cancel", []) for lane in NON_TERMINAL},
}

#: Guard id -> (implementing built-in, on_indeterminate as the file states it; None means absent, so block).
EXPECTED_GUARD_FILES: dict[str, tuple[str, str | None]] = {
    "spec-kitty-pre-review": ("builtin:spec-kitty-pre-review", "pass"),
    "dependency-ready": ("builtin:dependency-ready", None),
    "implementation-ready": ("builtin:implementation-ready", None),
    "review-approved": ("builtin:review-approved", None),
    "review-ref": ("builtin:review-ref", None),
}


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _edges(lifecycle: dict) -> list[tuple[tuple[str, str], dict]]:
    edges = []
    for transition in lifecycle["transitions"]:
        sources = transition["from"]
        for source in [sources] if isinstance(sources, str) else sources:
            edges.append(((source, transition["to"]), transition))
    return edges


class WorkPackageLifecycleGuardsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.edges = _edges(_load(LIFECYCLE))

    def test_each_edge_is_declared_once(self) -> None:
        dupes = [edge for edge, n in Counter(edge for edge, _ in self.edges).items() if n > 1]
        self.assertEqual(dupes, [], "an edge appears in more than one transition entry")

    def test_each_edge_has_its_event_and_the_blocking_guards_core_enforces_on_it(self) -> None:
        # blocking absent means true; a report-only entry would make the guard advisory.
        actual = {edge: (t.get("event"), [(g["ref"], g.get("blocking", True)) for g in t.get("guard", [])]) for edge, t in self.edges}
        expected = {edge: (event, [(ref, True) for ref in refs]) for edge, (event, refs) in EXPECTED_EDGES.items()}
        self.assertEqual(actual, expected)

    def test_every_guard_file_is_the_builtin_it_is_named_for(self) -> None:
        files = {path.name.removesuffix(".guard.yaml"): _load(path) for path in GUARDS.glob("*.guard.yaml")}
        self.assertEqual(set(files), set(EXPECTED_GUARD_FILES))
        for guard_id, (implemented_by, on_indeterminate) in EXPECTED_GUARD_FILES.items():
            guard = files[guard_id]
            self.assertEqual(guard["implemented_by"], implemented_by, guard_id)
            self.assertEqual(guard.get("on_indeterminate"), on_indeterminate, guard_id)


if __name__ == "__main__":
    unittest.main()
