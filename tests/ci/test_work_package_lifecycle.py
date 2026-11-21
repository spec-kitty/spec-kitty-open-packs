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

#: (from, to) -> the guard refs that transition names. Unlisted edges of this table are unguarded.
EXPECTED_GUARDS: dict[tuple[str, str], set[str]] = {
    ("planned", "claimed"): {"dependency-ready"},
    ("claimed", "in_progress"): {"dependency-ready"},
    ("blocked", "in_progress"): set(),
    ("in_progress", "for_review"): {"implementation-ready", "spec-kitty-pre-review"},
    ("for_review", "in_review"): set(),
    ("in_progress", "approved"): {"review-approved"},
    ("in_review", "approved"): {"review-approved"},
    ("in_review", "done"): {"review-approved"},
    ("approved", "done"): {"review-approved"},
    ("in_review", "in_progress"): {"review-ref"},
    ("approved", "in_progress"): {"review-ref"},
    ("in_progress", "planned"): set(),
    ("in_review", "planned"): set(),
    ("approved", "planned"): {"review-ref"},
    **{(lane, "blocked"): set() for lane in NON_TERMINAL if lane != "blocked"},
    **{(lane, "canceled"): set() for lane in NON_TERMINAL},
}

#: Guard id -> (implementing built-in, on_indeterminate as the file states it; None means absent, so block).
EXPECTED_GUARD_FILES: dict[str, tuple[str, str | None]] = {
    "spec-kitty-pre-review": ("builtin:spec-kitty-pre-review", "pass"),
    "dependency-ready": ("builtin:dependency-ready", "pass"),
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
        self.edges = _edges(_load(LIFECYCLE))

    def test_each_edge_is_declared_once(self) -> None:
        dupes = [edge for edge, n in Counter(edge for edge, _ in self.edges).items() if n > 1]
        self.assertEqual(dupes, [], "an edge appears in more than one transition entry")

    def test_edges_are_core_lanes_edges(self) -> None:
        self.assertEqual({edge for edge, _ in self.edges}, set(EXPECTED_GUARDS))

    def test_each_edge_names_the_guards_core_enforces_on_it(self) -> None:
        actual = {edge: {g["ref"] for g in t.get("guard", [])} for edge, t in self.edges}
        mismatches = {edge: (actual.get(edge), want) for edge, want in EXPECTED_GUARDS.items() if actual.get(edge) != want}
        self.assertEqual(mismatches, {}, "edge -> (declared, expected) guard refs")

    def test_transition_context_complete_is_not_declared(self) -> None:
        refs = {g["ref"] for _, t in self.edges for g in t.get("guard", [])}
        self.assertNotIn("transition-context-complete", refs)
        self.assertFalse((GUARDS / "transition-context-complete.guard.yaml").exists())

    def test_split_entries_keep_their_event(self) -> None:
        events = {edge: t.get("event") for edge, t in self.edges}
        for edge in (("claimed", "in_progress"), ("blocked", "in_progress")):
            self.assertEqual(events[edge], "start", edge)
        for source in ("in_progress", "in_review", "approved"):
            self.assertEqual(events[(source, "planned")], "reset", source)

    def test_every_guard_file_is_the_builtin_it_is_named_for(self) -> None:
        files = {path.name.removesuffix(".guard.yaml"): _load(path) for path in GUARDS.glob("*.guard.yaml")}
        self.assertEqual(set(files), set(EXPECTED_GUARD_FILES))
        for guard_id, (implemented_by, on_indeterminate) in EXPECTED_GUARD_FILES.items():
            guard = files[guard_id]
            self.assertEqual(guard["id"], guard_id)
            self.assertEqual(guard["implemented_by"], implemented_by, guard_id)
            self.assertEqual(guard.get("on_indeterminate"), on_indeterminate, guard_id)
            self.assertNotIn("blocking", guard, "a guard carries no severity; the transition entry does")


if __name__ == "__main__":
    unittest.main()
