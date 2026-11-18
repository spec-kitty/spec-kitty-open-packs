"""The shipped glossary contexts carry the docs/context terms (#221) and the Op term (#234).

spec-kitty-core is the consumer context: its definitions must not cite core's source tree, tests,
ADRs or issue numbers, and it names itself the authoring source. Both contexts keep term ids and
surface forms (names and aliases) unique, and every see_also resolves inside its own context.
"""

from __future__ import annotations

import re
import unittest
from collections import Counter
from pathlib import Path

import yaml

PACKS = Path(__file__).resolve().parents[2] / "packs"
CORE = PACKS / "foundation" / "glossaries" / "spec-kitty-core.glossary.yaml"
INTERNAL = PACKS / "internal" / "glossaries" / "spk-internal-glossary.glossary.yaml"

#: What a consumer definition must not cite: core's source and test trees, ADRs, issue numbers, docs pages, work
#: packages, requirement ids and code symbols.
CORE_CITATION = re.compile(r"\bsrc/|\btests/|\bADR[ -]?\d|#\d{3,}|docs/context/|\bWP\d+\b|\bFR-\d+|\w+\(\)|::\w+|\.py\b")


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _terms(path: Path) -> dict[str, dict]:
    return {term["id"]: term for term in _load(path)["terms"]}


class OpTermTest(unittest.TestCase):
    def test_op_is_defined_as_directive_053_describes_it(self) -> None:
        op = _terms(CORE).get("op")
        self.assertIsNotNone(op, "term:spec-kitty-core/op is missing (#234)")
        self.assertEqual(op["name"], "Op")
        self.assertEqual(op["status"], "active")
        self.assertIn("profile invocation", op.get("aliases", []))
        self.assertIn("term:spec-kitty-core/mission", op.get("see_also", []))
        for phrase in ("spec-kitty dispatch", "spec-kitty profile-invocation complete", "DIRECTIVE_053"):
            self.assertIn(phrase, op["definition"])

    def test_the_four_mission_types_are_terms(self) -> None:
        terms = _terms(CORE)
        for mission_type in ("software-dev", "research", "documentation", "plan"):
            term = terms.get(f"{mission_type}-mission")
            self.assertIsNotNone(term, f"{mission_type} mission type has no term")
            self.assertIn("term:spec-kitty-core/mission-type", term.get("see_also", []))


class ConsumerContextTest(unittest.TestCase):
    def test_definitions_do_not_cite_core_internals(self) -> None:
        hits = [(tid, m.group(0)) for tid, term in _terms(CORE).items() for m in CORE_CITATION.finditer(term["definition"])]
        self.assertEqual(hits, [], "consumer definitions cite core's code, tests, ADRs or issues")

    def test_citation_pattern_is_not_vacuous(self) -> None:
        # Same pattern, a definition shaped like core's docs/context source text.
        self.assertTrue(CORE_CITATION.search("Realized by the `MissionTopology` enum in `src/mission_runtime/context.py`."))
        self.assertTrue(CORE_CITATION.search("See ADR 2026-11-08-2 and #6611."))
        self.assertTrue(CORE_CITATION.search("Since WP07 (FR-012), read by resolve_planning_branch_from_meta()."))

    def test_the_context_names_itself_the_authoring_source(self) -> None:
        document = _load(CORE)
        self.assertNotIn("migrated from", document["description"])
        self.assertIn("authoring source", document["description"])
        self.assertIn("authoring source", CORE.read_text(encoding="utf-8").split("\nschema_version:", 1)[0])


class ContextIntegrityTest(unittest.TestCase):
    def _check(self, path: Path) -> None:
        document = _load(path)
        terms = document["terms"]
        ids = Counter(term["id"] for term in terms)
        self.assertEqual([i for i, n in ids.items() if n > 1], [], f"{path.name}: duplicate term ids")
        forms = Counter(form.lower() for term in terms for form in [term["name"], *term.get("aliases", [])])
        self.assertEqual([f for f, n in forms.items() if n > 1], [], f"{path.name}: a name or alias is used twice")
        prefix = f"term:{document['id']}/"
        broken = [(t["id"], ref) for t in terms for ref in t.get("see_also", []) if not ref.startswith(prefix) or ref[len(prefix):] not in ids]
        self.assertEqual(broken, [], f"{path.name}: see_also must resolve inside the context")

    def test_consumer_context(self) -> None:
        self._check(CORE)

    def test_internal_context(self) -> None:
        self._check(INTERNAL)

    def test_house_terms_stay_out_of_the_consumer_context(self) -> None:
        core, internal = set(_terms(CORE)), set(_terms(INTERNAL))
        self.assertEqual(core & internal, set(), "a term id is in both the consumer and the internal context")
        for house in ("ratchet-baseline", "priority-scheme", "tool-vs-agent-naming", "unit-test-marker"):
            self.assertIn(house, internal)


if __name__ == "__main__":
    unittest.main()
