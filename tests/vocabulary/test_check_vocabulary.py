"""Controls for the pack vocabulary guard (spec-kitty/spec-kitty#6553).

Proves ``scripts/ci/check_vocabulary.py`` is neither vacuous nor over-eager.
Stdlib ``unittest`` only. Run it with::

    python3 -m unittest discover -s tests/vocabulary
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "ci" / "check_vocabulary.py"
_spec = importlib.util.spec_from_file_location("check_vocabulary", _SCRIPT)
vocab = importlib.util.module_from_spec(_spec)
sys.modules["check_vocabulary"] = vocab
_spec.loader.exec_module(vocab)

_SURFACE = vocab._RETIRED_SURFACE_TOKEN


def _git(repo: Path, *args: str) -> None:
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
           "GIT_COMMITTER_EMAIL": "t@t", "GIT_CONFIG_GLOBAL": os.devnull}
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, env=env)


class RetiredIdTest(unittest.TestCase):
    def test_flags_every_shape(self) -> None:
        snippet = (
            "activated_tactics:\n  - bug-fixing-checklist\n"
            "edge: tactic:locality-of-change\n"
            "path: tactics/boring-code-review.tactic.yaml\n"
            "- type: styleguide\n  id: adversarial-squad-cadence\n"
            "see contracts/adversarial-evidence-contract.md\n"
        )
        self.assertEqual(
            set(vocab.retired_ids_in(snippet, "packs/qa/x.yaml")),
            {"bug-fixing-checklist", "locality-of-change", "boring-code-review", "adversarial-squad-cadence", "adversarial-evidence-contract"},
        )

    def test_spares_live_twins(self) -> None:
        snippet = (
            "activated_directives:\n  - 024-locality-of-change\n"
            "see DIRECTIVE_024 locality-of-change discipline\n"
            "- type: styleguide\n  id: boring-code-review\n"
            "styleguide:boring-code-review\n"
        )
        self.assertEqual(vocab.retired_ids_in(snippet, "packs/built-in/x.yaml"), [])

    def test_internal_allowlist_covers_only_the_moved_ids(self) -> None:
        snippet = "- tracker-organisation-workflow\n- iterative-deepening-review\n- bug-fixing-checklist\n"
        self.assertEqual(vocab.retired_ids_in(snippet, "packs/internal/drg/fragment.yaml"), ["bug-fixing-checklist"])
        self.assertEqual(
            set(vocab.retired_ids_in(snippet, "packs/qa/x.yaml")),
            {"tracker-organisation-workflow", "iterative-deepening-review", "bug-fixing-checklist"},
        )

    def test_provenance_strips_only_its_phrase(self) -> None:
        rel, stem, phrase = next(row for row in vocab.PROVENANCE_PHRASES if row[0] == "packs/qa/README.md")
        self.assertEqual(vocab.retired_ids_in(f"| {phrase} in 4.0.0rc5. |\n", rel), [])
        self.assertEqual(vocab.retired_ids_in(f"| {phrase}. |\n- tactic: {stem}\n", rel), [stem])
        # The finding points at the real mention, not at the provenance line before it.
        self.assertEqual([line for line, _ in vocab.findings_in(f"| {phrase}. |\n- tactic: {stem}\n", rel)], [2])
        self.assertEqual(vocab.retired_ids_in(phrase, "packs/qa/other.md"), [stem])

    def test_stale_provenance_is_reported(self) -> None:
        texts = {rel: phrase for rel, _stem, phrase in vocab.PROVENANCE_PHRASES}
        self.assertEqual(vocab.stale_provenance(texts), [])
        rel = vocab.PROVENANCE_PHRASES[0][0]
        texts[rel] = "rewritten"
        self.assertEqual(len(vocab.stale_provenance(texts)), 1)
        self.assertIn(rel, vocab.stale_provenance(texts)[0])


class CommandAndSurfaceTest(unittest.TestCase):
    def test_flags_the_renamed_command_with_its_line(self) -> None:
        text = "intro\nthen run Spec-Kitty merge --dry-run\n"
        self.assertEqual([line for line, _ in vocab.findings_in(text, "packs/qa/prompt.md")], [2])

    def test_spares_merge_compounds_and_consolidate(self) -> None:
        text = (
            "spec-kitty merge-driver-event-log %O %A %B\nspec-kitty merge-mission\nspec-kitty consolidate\ngit merge --no-ff\n"
            "spec-kitty merges the approved lanes\nonce spec-kitty merged them\n"
        )
        self.assertEqual(vocab.findings_in(text, "packs/qa/prompt.md"), [])

    def test_flags_the_retired_surface_only_in_a_glossary(self) -> None:
        text = f"terms:\n  - name: {_SURFACE}\n  - name: {_SURFACE} pack\n  - name: \"{_SURFACE}\"\n  - name: '{_SURFACE}'  # old\n"
        self.assertEqual([line for line, _ in vocab.findings_in(text, "packs/foundation/glossaries/x.glossary.yaml")], [2, 4, 5])
        self.assertEqual(vocab.findings_in(text, "packs/built-in/notes.yaml"), [])


class RuntimeFamilyLanguageTest(unittest.TestCase):
    """#202: a runtime family such as ``jvm`` is not a language name."""

    def test_flags_block_and_flow_entries(self) -> None:
        block = "id: x\napplies_to_languages:\n- java\n- jvm\nlast_updated: '2026-01-01'\n"
        flow = "applies_to_languages: [java, 'dotnet']\n"
        self.assertEqual(vocab.family_languages_in(block), [(4, "jvm")])
        self.assertEqual(vocab.family_languages_in(flow), [(1, "dotnet")])
        self.assertTrue(any("runtime family 'jvm'" in message for _, message in vocab.findings_in(block, "packs/java/x.yaml")))

    def test_spares_languages_prose_and_later_lists(self) -> None:
        snippet = (
            "applies_to_languages:\n  - java\n  - kotlin\n"
            "summary: runs on the jvm\n"
            "commands:\n- jvm --version\n"
            "applies_to_languages: []\n"
        )
        self.assertEqual(vocab.family_languages_in(snippet), [])

    def test_only_yaml_files_are_checked(self) -> None:
        self.assertEqual(vocab.findings_in("applies_to_languages:\n- jvm\n", "packs/java/README.md"), [])


class SelfBindingTest(unittest.TestCase):
    """#233: pack prose never states how strictly a directive binds; the charter does."""

    REFUSED = (
        "This directive is advisory at the transition-gate level in v1: it adds no handler.",
        "Advisory in v1: evidence is required, but this step does not gate the transition.",
        "This is advisory guidance, not a runtime gate.",
        "Makes the integrity rules for parallel cloud sessions binding charter content.",
        "- **Advisory posture**: an unexamined default is a gap.",
        "- `CAVE_001` (Caveman Terse Output) governs this step's output prose; enforcement `required`.",
        "Remember that the rule is advisory here.",
        "the worktree-isolation rules that DIRECTIVE_045 makes binding",
        "This tactic operationalizes the directive's binding rules.",
        "A Spec Kitty styleguide/directive is advisory context an agent applies.",
        "The missing-skill fallback and the PyPI fallback remain advisory in the procedure.",
        "This rule is enforced as a hard validation gate: ownerless actions are refused.",
        "    description: 'Surface the risk. Advisory: evidence is required, but this step does not gate the transition.'",
        "A report missing one is incomplete. This is not a recommendation: all seven count.",
        "classify each by kind: a non-negotiable rule becomes a directive.",
        "The attribution directive is a hard gate for every minute.",
        "applying its own resolution order is an acceptable lenient-adherence allowance here.",
        "CLOUD_SESSION_ORCHESTRATION makes the read-only sibling, orchestrator-mediated write and shared-number rules binding.",
    )

    #: (text, line the phrase starts on): phrases a ~80-column wrap splits across two lines.
    WRAPPED = (
        ("scope: >\n  It adds no gate. Advisory in\n  v1: evidence is required.\n", 2),
        ("intent: >\n  Read the evidence first. This directive is\n  advisory for teams adopting it.\n", 2),
        ("- \"A report missing one is incomplete. This is not a\n  recommendation: all seven count.\"\n", 1),
        ("notes:\n  # A styleguide is advisory\n  # context an agent applies.\n", 2),
    )

    ALLOWED = (
        "npm audit reports an advisory for this version; check it before the upgrade.",
        "Owner is mandatory on every action item.",
        "Assign each term an enforcement tier (advisory, acknowledgment-required, hard-failure).",
        "The file is written in the exact qa-traceability/v1 schema.",
        'reason: "CTRF not implemented in v1"',
        "enforcement: required",
        "  enforcement: advisory  # the pack-supplied default",
        "This directive applies when a dependency changes; it is a rule, not a gate.",
        "Spring makes property binding type-safe; Angular makes two-way binding easy.",
        "The service locator makes the service binding explicit.",
        "advisory: GHSA-xxxx-yyyy-zzzz",
        "Check the lockfile. Advisory: npm reports a moderate issue for this version.",
        "The rule is required reading for every reviewer.",
        "`/spec-kitty.analyze` must run first. This is not optional: it is the readiness gate.",
        "This directive binds only work handled under Spec Kitty.",
        "`lenient-adherence` means conform except where explicit_allowances permit.",
        "The attribution check is a hard gate whenever any action exists.",
    )

    def test_refuses_every_self_binding_phrase(self) -> None:
        for line in self.REFUSED:
            with self.subTest(line=line):
                found = vocab.self_binding_in(f"intro\n{line}\n")
                self.assertEqual([number for number, _ in found], [2])

    def test_refuses_a_phrase_split_by_a_line_wrap(self) -> None:
        for text, line in self.WRAPPED:
            with self.subTest(text=text):
                self.assertEqual([number for number, _ in vocab.self_binding_in(text)], [line])

    def test_a_phrase_on_one_line_is_reported_once(self) -> None:
        self.assertEqual([n for n, _ in vocab.self_binding_in("Advisory in v1: x.\nAdvisory in v1: y.\n")], [1, 2])

    def test_the_enforcement_field_never_joins(self) -> None:
        self.assertEqual(vocab.self_binding_in("intent: The rule is\nenforcement: advisory\n"), [])

    def test_spares_other_senses_and_the_field(self) -> None:
        for line in self.ALLOWED:
            with self.subTest(line=line):
                self.assertEqual(vocab.self_binding_in(f"{line}\n"), [])

    def test_findings_name_the_glossary_term(self) -> None:
        found = vocab.findings_in("x\nThis is advisory guidance.\n", "packs/foundation/directives/049.directive.yaml")
        self.assertEqual([line for line, _ in found], [2])
        self.assertIn("enforcement-level", found[0][1])


class MainTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        _git(self.repo, "init", "-q")
        for rel, _stem, phrase in vocab.PROVENANCE_PHRASES:
            self._write(rel, f"{phrase}\n")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _write(self, rel: str, text: str) -> None:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        _git(self.repo, "add", rel)

    def _main(self) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = vocab.main(self.repo)
        return code, out.getvalue()

    def test_clean_tree_passes(self) -> None:
        code, out = self._main()
        self.assertEqual(code, 0, out)

    def test_planted_finding_fails_with_an_annotation(self) -> None:
        self._write("packs/qa/missions/prompt.md", "ok\nrun spec-kitty merge now\n")
        code, out = self._main()
        self.assertEqual(code, 1)
        self.assertIn("::error file=packs/qa/missions/prompt.md,line=2::", out)

    def test_planted_self_binding_phrase_fails(self) -> None:
        self._write("packs/qa/directives/x.directive.yaml", "id: X\nenforcement: required\nscope: >\n  Advisory in v1.\n")
        code, out = self._main()
        self.assertEqual(code, 1)
        self.assertIn("::error file=packs/qa/directives/x.directive.yaml,line=4::", out)

    def test_untracked_files_are_not_scanned(self) -> None:
        (self.repo / "packs" / "qa" / "scratch.md").write_text("tactic:bug-fixing-checklist\n", encoding="utf-8")
        self.assertEqual(self._main()[0], 0)

    def test_empty_packs_refuses_instead_of_passing(self) -> None:
        _git(self.repo, "rm", "-q", "-r", "--cached", "packs")
        with self.assertRaises(SystemExit):
            vocab.main(self.repo)


if __name__ == "__main__":
    unittest.main()
