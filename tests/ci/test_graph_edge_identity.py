"""Each pack holds at most one edge per unordered component pair.

spec-kitty-charter ADR-0027 (clarified by ADR-0036) allows one unidirectional relationship per
component pair. A source that breaks the rule is fixed in the source, not collapsed on read.
Graph documents are the only source of relationships (ADR-0064), so this test reads the
`drg/fragment.yaml` and `*.graph.yaml` documents of every pack. Tracked by #135.
"""

from __future__ import annotations

import unittest
from collections import defaultdict
from pathlib import Path

import yaml

PACKS = Path(__file__).resolve().parents[2] / "packs"

# Pairs with one edge in each direction (A->B and B->A), frozen when #135 was filed. Each needs a
# curation ruling on which direction keeps the meaning. This list may only shrink: a new pair
# fails, and an entry that has been collapsed must be removed from here.
REVERSE_PAIR_BASELINE = frozenset({
    ("built-in", "directive:DIRECTIVE_001", "tactic:paula-patterns-architecture-scout-review"),
    ("built-in", "directive:DIRECTIVE_003", "tactic:traceable-decisions"),
    ("built-in", "directive:DIRECTIVE_024", "directive:DIRECTIVE_025"),
    ("built-in", "directive:DIRECTIVE_024", "directive:RECONCILE_CHANGE_SCOPE_TENSIONS"),
    ("built-in", "directive:DIRECTIVE_025", "directive:RECONCILE_CHANGE_SCOPE_TENSIONS"),
    ("built-in", "directive:DIRECTIVE_030", "styleguide:test-desiderata-and-boundaries"),
    ("built-in", "directive:DIRECTIVE_030", "styleguide:testing-principles"),
    ("built-in", "directive:DIRECTIVE_030", "styleguide:tiered-standards"),
    ("built-in", "directive:DIRECTIVE_030", "tactic:work-package-completion-validation"),
    ("built-in", "directive:DIRECTIVE_034", "paradigm:specification-by-example"),
    ("built-in", "directive:DIRECTIVE_034", "tactic:formalized-constraint-testing"),
    ("built-in", "directive:DIRECTIVE_035", "tactic:occurrence-classification-workflow"),
    ("built-in", "directive:DIRECTIVE_038", "paradigm:structured-prompt-driven-development"),
    ("built-in", "directive:DIRECTIVE_040", "tactic:five-paradigm-parallel-debugging"),
    ("built-in", "directive:DIRECTIVE_041", "styleguide:testing-principles"),
    ("built-in", "directive:DIRECTIVE_042", "styleguide:common-docs"),
    ("built-in", "directive:DIRECTIVE_042", "tactic:common-docs-find"),
    ("built-in", "directive:DIRECTIVE_042", "tactic:common-docs-scaffold"),
    ("built-in", "directive:DIRECTIVE_042", "tactic:common-docs-write"),
    ("built-in", "directive:DIRECTIVE_043", "tactic:architectural-gate-non-vacuity"),
    ("built-in", "directive:DIRECTIVE_043", "tactic:frozen-baseline-shrink-only-ratchet"),
    ("built-in", "directive:DIRECTIVE_044", "tactic:canonical-source-unification"),
    ("built-in", "directive:DIRECTIVE_044", "tactic:model-task-routing"),
    ("built-in", "directive:DIRECTIVE_051", "tactic:dependency-hygiene"),
    ("built-in", "directive:DIRECTIVE_051", "tactic:supply-chain-install-safety"),
    ("built-in", "directive:RECONCILE_CHANGE_SCOPE_TENSIONS", "tactic:change-apply-smallest-viable-diff"),
    ("built-in", "paradigm:behaviour-driven-development", "tactic:bdd-scenario-formulation"),
    ("built-in", "paradigm:domain-driven-design", "styleguide:aggregate-design-rules"),
    ("built-in", "procedure:bdd-scenario-lifecycle", "tactic:bdd-scenario-formulation"),
    ("built-in", "procedure:disciplined-defect-diagnosis", "procedure:test-first-bug-fixing"),
    ("built-in", "procedure:legacy-codebase-triage", "tactic:forensic-repository-audit"),
    ("built-in", "styleguide:aggregate-design-rules", "tactic:aggregate-boundary-design"),
    ("built-in", "styleguide:common-docs", "tactic:common-docs-find"),
    ("built-in", "styleguide:common-docs", "tactic:common-docs-scaffold"),
    ("built-in", "styleguide:common-docs", "tactic:common-docs-write"),
    ("built-in", "styleguide:planning-and-tracking", "tactic:ownership-map-leeway"),
    ("built-in", "styleguide:planning-and-tracking", "tactic:reviewer-implementer-role-separation"),
    ("built-in", "styleguide:test-desiderata-and-boundaries", "styleguide:testing-principles"),
    ("internal", "procedure:tracker-organisation-workflow", "tactic:tracker-backlog-iterative-deepening"),
})


def _graph_documents(pack: Path) -> list[Path]:
    fragment = pack / "drg" / "fragment.yaml"
    return ([fragment] if fragment.is_file() else []) + sorted(pack.glob("*.graph.yaml"))


def _edges_by_pair() -> dict[tuple[str, str, str], list[tuple[str, str, str, str]]]:
    """Map (pack, lower urn, higher urn) to every edge on that unordered pair, as (file, source, target, relation)."""
    pairs: dict[tuple[str, str, str], list[tuple[str, str, str, str]]] = defaultdict(list)
    for pack in sorted(p for p in PACKS.iterdir() if p.is_dir()):
        for graph in _graph_documents(pack):
            doc = yaml.safe_load(graph.read_text(encoding="utf-8")) or {}
            for edge in doc.get("edges") or []:
                low, high = sorted((edge["source"], edge["target"]))
                pairs[(pack.name, low, high)].append(
                    (str(graph.relative_to(PACKS)), edge["source"], edge["target"], edge["relation"]))
    return pairs


class GraphEdgeIdentityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pairs = _edges_by_pair()
        self.assertTrue(self.pairs, "no graph edges found under packs/")

    def test_no_pair_carries_two_edges_in_one_direction(self) -> None:
        duplicates = [edges for _, edges in sorted(self.pairs.items())
                      if len(edges) != len({(source, target) for _, source, target, _ in edges})]
        self.assertFalse(duplicates, f"duplicate edges for one direction (keep one, ADR-0027): {duplicates}")

    def test_no_new_pair_has_edges_in_both_directions(self) -> None:
        reversed_pairs = {key for key, edges in self.pairs.items() if len({(s, t) for _, s, t, _ in edges}) > 1}
        new = sorted(reversed_pairs - REVERSE_PAIR_BASELINE)
        self.assertFalse(new, f"edges in both directions on one pair (keep one, ADR-0027): "
                              f"{[self.pairs[k] for k in new]}")

    def test_reverse_pair_baseline_only_shrinks(self) -> None:
        reversed_pairs = {key for key, edges in self.pairs.items() if len({(s, t) for _, s, t, _ in edges}) > 1}
        stale = sorted(REVERSE_PAIR_BASELINE - reversed_pairs)
        self.assertFalse(stale, f"collapsed pairs still listed in REVERSE_PAIR_BASELINE, remove them: {stale}")


if __name__ == "__main__":
    unittest.main()
