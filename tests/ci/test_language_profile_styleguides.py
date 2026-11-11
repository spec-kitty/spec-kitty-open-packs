"""Every language-specialist profile in any pack requires the conventions styleguide of its languages.

Cascades and effective reads walk outgoing edges (spec-kitty-charter ADR-0064), so the edge must run
from the profile to the styleguide. Operator ruling on spec-kitty-charter#405, tracked by #131.
"""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

# Since #73 the language profiles and their styleguides live in the opt-in stack packs (python,
# java, javascript, drupal), so the test reads every pack and compares unqualified URNs.
PACKS = Path(__file__).resolve().parents[2] / "packs"

# Explicit language -> conventions styleguide map; Drupal breaks a `<lang>-conventions` name rule.
CONVENTIONS = {
    "java": "java-conventions",
    "rust": "rust-conventions",
    "go": "go-conventions",
    "python": "python-conventions",
    "php": "drupal-conventions",
    "twig": "drupal-conventions",
    "typescript": "typescript-conventions",
    "html": "html-conventions",
    "css": "css-conventions",
}

# Languages with no conventions styleguide in any pack, by maintainer ruling on #131 (2026-11-07):
# javascript stays exempt; typescript-conventions is type-system centred and does not cover it.
EXEMPT = {"javascript"}


def _bare(urn: str) -> str:
    return urn.split("::", 1)[-1]


def _requires_edges() -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for graph in [*PACKS.glob("*/*.graph.yaml"), *PACKS.glob("*/drg/fragment.yaml")]:
        doc = yaml.safe_load(graph.read_text(encoding="utf-8")) or {}
        for edge in doc.get("edges") or []:
            if edge.get("relation") == "requires":
                edges.add((_bare(edge["source"]), _bare(edge["target"])))
    return edges


class LanguageProfileStyleguideTest(unittest.TestCase):
    def test_each_language_profile_requires_its_conventions_styleguide(self) -> None:
        edges = _requires_edges()
        checked = 0
        for path in sorted(PACKS.glob("*/agent_profiles/*.agent.yaml")):
            profile = yaml.safe_load(path.read_text(encoding="utf-8"))
            for language in profile.get("applies_to_languages") or []:
                if language in EXEMPT:
                    continue
                self.assertIn(language, CONVENTIONS, f"{path.name}: no conventions styleguide mapped for {language!r}")
                styleguide = CONVENTIONS[language]
                self.assertTrue(any(PACKS.glob(f"*/styleguides/**/{styleguide}.styleguide.yaml")), styleguide)
                self.assertIn((f"agent_profile:{profile["profile-id"]}", f"styleguide:{styleguide}"), edges,
                              f"agent_profile:{profile["profile-id"]} must `requires` styleguide:{styleguide}")
                checked += 1
        # 7 stack profiles carry 10 language pairs today; a lost profile or edge drops below this floor.
        self.assertGreaterEqual(checked, 10)


if __name__ == "__main__":
    unittest.main()
