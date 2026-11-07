"""Every language-specialist profile in built-in requires the conventions styleguide of its languages.

Cascades and effective reads walk outgoing edges (spec-kitty-charter ADR-0064), so the edge must run
from the profile to the styleguide. Operator ruling on spec-kitty-charter#405, tracked by #131.
"""

from __future__ import annotations

import unittest
from pathlib import Path

import yaml

BUILT_IN = Path(__file__).resolve().parents[2] / "packs" / "built-in"

# Explicit language -> conventions styleguide map; Drupal breaks a `<lang>-conventions` name rule.
CONVENTIONS = {
    "java": "java-conventions",
    "python": "python-conventions",
    "php": "drupal-conventions",
    "twig": "drupal-conventions",
}

# Languages with no conventions styleguide in built-in yet (open question on #131).
EXEMPT = {"javascript", "typescript", "html", "css"}


def _requires_edges() -> set[tuple[str, str]]:
    edges: set[tuple[str, str]] = set()
    for graph in BUILT_IN.glob("*.graph.yaml"):
        doc = yaml.safe_load(graph.read_text(encoding="utf-8")) or {}
        for edge in doc.get("edges") or []:
            if edge.get("relation") == "requires":
                edges.add((edge["source"], edge["target"]))
    return edges


class LanguageProfileStyleguideTest(unittest.TestCase):
    def test_each_language_profile_requires_its_conventions_styleguide(self) -> None:
        edges = _requires_edges()
        checked = 0
        for path in sorted((BUILT_IN / "agent_profiles").glob("*.agent.yaml")):
            profile = yaml.safe_load(path.read_text(encoding="utf-8"))
            for language in profile.get("applies_to_languages") or []:
                if language in EXEMPT:
                    continue
                self.assertIn(language, CONVENTIONS, f"{path.name}: no conventions styleguide mapped for {language!r}")
                styleguide = CONVENTIONS[language]
                self.assertTrue((BUILT_IN / "styleguides" / f"{styleguide}.styleguide.yaml").is_file(), styleguide)
                self.assertIn((f"agent_profile:{profile["profile-id"]}", f"styleguide:{styleguide}"), edges,
                              f"agent_profile:{profile["profile-id"]} must `requires` styleguide:{styleguide}")
                checked += 1
        self.assertGreater(checked, 0)


if __name__ == "__main__":
    unittest.main()
