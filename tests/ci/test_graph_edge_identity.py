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

# Pairs with one edge in each direction (A->B and B->A). The #135 baseline was collapsed under
# the operator's curation rule (2026-11-08): the governing side keeps the edge, tension edges
# win their pairs, and the two same-kind pairs were ruled by the operator. No reverse pair may
# be added again.
REVERSE_PAIR_BASELINE: frozenset[tuple[str, str, str]] = frozenset()


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
