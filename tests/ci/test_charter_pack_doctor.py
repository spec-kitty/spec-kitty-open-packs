"""The pack-doctor gate (#252, #345): charter's whole-pack check, run from the pinned jar, judged fail-closed.

Most tests drive ``scripts/ci/charter_pack_doctor.py`` with a stand-in ``java`` that answers as pack-doctor would, so
they run anywhere. ``RealPackDoctor`` runs the real jar when ``PACK_DOCTOR_JAR`` names one; the ``Charter service
validation`` job sets it to the jar of the pin, so the invalid fixtures and this checkout's packs are proven against
the real tool there.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "ci"))

import charter_pack_doctor as gate  # noqa: E402

SCRIPT = ROOT / "scripts" / "ci" / "charter_pack_doctor.py"
ALL_CHECKS = ["PACK", "CLOSURE", "REFERENCES", "ROUND_TRIP"]


def report(names: list[str], *, problems: list | None = None, checks: list[str] | None = None,
           skipped: list | None = None, exit_code: int | None = None) -> dict:
    """A ``PackDoctorReport`` of the measured shape (research.md R2): its summary states the exit code it implies."""
    problems = problems or []
    document = {"tool": {"name": "pack-doctor", "version": "0.1.0-SNAPSHOT"},
                "inputs": {"packs": [f"./packs/{name}" for name in names],
                           "options": {"full": True, "round_trip": True}},
                "checks": checks or ALL_CHECKS,
                "packs": [{"name": name, "level": "org", "path": f"./packs/{name}"} for name in names],
                "problems": problems,
                "summary": {"packs": len(names), "violations": len(problems), "warnings": 0, "notices": 0,
                            "exit_code": (1 if problems else 0) if exit_code is None else exit_code}}
    if skipped is not None:
        document["skipped"] = skipped
    return document


def problem(code: str, *violations: str) -> dict:
    return {"title": "Validation failed", "status": 422, "detail": f"{code} here", "code": code,
            "violations": [{"pointer": "pack.yaml", "code": v, "detail": f"{v} detail"} for v in violations]}


class JudgeTheSet(unittest.TestCase):
    """The run over every pack and valid fixture must be a clean, complete verdict."""

    def judge(self, exit_code: int, document: dict | None, stderr: str = "", names=("a", "b")) -> list[str]:
        result = gate.Result(exit_code=exit_code, report=document, stderr=stderr)
        return gate.judge_set(result, list(names))

    def test_a_clean_complete_verdict_passes(self) -> None:
        stderr = "Picked up JAVA_TOOL_OPTIONS: x\nwarning: a: file_not_held docs/README.md: not held (notes)\n"
        self.assertEqual(self.judge(0, report(["a", "b"]), stderr), [])

    def test_exit_2_fails_closed_as_no_verdict(self) -> None:
        # Exit 2 is a usage fault or a failure outside a pack read: nothing was judged, so the gate fails closed.
        failures = self.judge(2, None, "pack-doctor: no command: give validate or remediate before the options\n")
        self.assertTrue(failures)
        self.assertIn("exited 2", failures[0])
        self.assertTrue(any("no command" in line for line in failures))

    def test_an_unknown_top_level_key_fails(self) -> None:
        failures = self.judge(0, {**report(["a", "b"]), "repairs": []})
        self.assertTrue(any("'repairs'" in line for line in failures), failures)

    def test_a_missing_or_skipped_references_check_fails(self) -> None:
        self.assertTrue(any("did not run REFERENCES" in line
                            for line in self.judge(0, report(["a", "b"], checks=["PACK", "CLOSURE", "ROUND_TRIP"]))))
        skipped = report(["a", "b"], checks=["PACK", "CLOSURE", "ROUND_TRIP"],
                         skipped=[{"check": "REFERENCES", "reason": "a closure failed to compose"}])
        failures = self.judge(0, skipped)
        self.assertIn("skipped REFERENCES", failures[0])

    def test_a_summary_exit_code_that_disagrees_with_the_run_fails(self) -> None:
        failures = self.judge(0, report(["a", "b"], exit_code=1))
        self.assertTrue(any("summary.exit_code is 1, but pack-doctor exited 0" in line for line in failures), failures)
        document = report(["a", "b"])
        del document["summary"]
        self.assertTrue(any("summary.exit_code is None" in line for line in self.judge(0, document)))

    def test_another_tool_name_fails(self) -> None:
        for tool in ({"name": "pack-check", "version": "0.1.0-rc.3"}, None):
            with self.subTest(tool=tool):
                failures = self.judge(0, {**report(["a", "b"]), "tool": tool})
                self.assertTrue(any("tool.name" in line for line in failures), failures)

    def test_a_run_without_full_or_round_trip_fails(self) -> None:
        for options in ({"full": False, "round_trip": True}, {"full": True, "round_trip": False}, {}):
            with self.subTest(options=options):
                document = report(["a", "b"])
                document["inputs"]["options"] = options
                self.assertTrue(any("inputs.options" in line for line in self.judge(0, document)))

    def test_checks_must_be_an_ordered_list_of_known_checks(self) -> None:
        for checks in ("PACK CLOSURE REFERENCES ROUND_TRIP", ["CLOSURE", "PACK", "REFERENCES", "ROUND_TRIP"],
                       [*ALL_CHECKS, "NEW_CHECK"]):
            with self.subTest(checks=checks):
                document = report(["a", "b"])
                document["checks"] = checks
                self.assertTrue(any("the report's checks" in line for line in self.judge(0, document)))

    def test_a_boolean_exit_code_in_the_summary_fails(self) -> None:
        document = report(["a", "b"])
        document["summary"]["exit_code"] = False  # False == 0, but it is not an exit code
        self.assertTrue(any("summary.exit_code is False" in line for line in self.judge(0, document)))

    def test_a_pack_reported_twice_is_named(self) -> None:
        document = report(["a", "b"])
        document["packs"].append(dict(document["packs"][0]))
        self.assertTrue(any("reported twice: ['a']" in line for line in self.judge(0, document)))

    def test_exit_1_fails_and_names_every_problem_and_violation(self) -> None:
        failures = self.judge(1, report(["a", "b"], problems=[problem("validation_failed", "round_trip_red")]))
        self.assertTrue(any("round_trip_red" in line for line in failures))

    def test_any_other_exit_code_fails(self) -> None:
        for code in (3, 137, -9):
            with self.subTest(code=code):
                self.assertTrue(self.judge(code, report(["a", "b"])))

    def test_exit_0_with_a_problem_still_fails(self) -> None:
        self.assertTrue(self.judge(0, report(["a", "b"], problems=[problem("validation_failed")])))

    def test_exit_0_without_a_parseable_report_fails(self) -> None:
        self.assertTrue(self.judge(0, None))

    def test_the_cause_of_a_skipped_check_comes_first(self) -> None:
        # Review of #332: on a pack that cannot be read (a missing companion), the generic "refused" and "did not run
        # CLOSURE" lines buried the cause, which only the skipped check's reason names. It now leads.
        reason = "CLOSURE needs the composition facts; cave-kitty cannot be read: steps/implement.prompt.md: missing"
        document = report(["a", "b"], checks=["PACK", "ROUND_TRIP"], skipped=[{"check": "CLOSURE", "reason": reason},
                                                                               {"check": "REFERENCES", "reason": reason}],
                          problems=[problem("validation_failed")])
        failures = self.judge(1, document)
        self.assertIn("steps/implement.prompt.md: missing", failures[0])

    def test_a_skipped_or_missing_check_fails(self) -> None:
        self.assertTrue(self.judge(0, report(["a", "b"], checks=["PACK", "REFERENCES", "ROUND_TRIP"])))
        skipped = [{"check": "CLOSURE", "reason": "no facts"}]
        self.assertTrue(self.judge(0, report(["a", "b"], skipped=skipped)))

    def test_a_pack_left_out_or_added_fails(self) -> None:
        self.assertTrue(self.judge(0, report(["a"])))
        self.assertTrue(self.judge(0, report(["a", "b", "c"])))

    def test_a_warning_other_than_file_not_held_fails(self) -> None:
        # driftTest, which this replaces, failed on every load warning; file_not_held stays a notice here because a
        # stray file warns, never fails (operator ruling R34, #331).
        stderr = "warning: b: prompt_slot_not_empty missions/x/prompt.md: legacy text in a slot\n"
        failures = self.judge(0, report(["a", "b"]), stderr)
        self.assertTrue(any("prompt_slot_not_empty" in line for line in failures))

    def test_a_warning_in_a_format_the_gate_cannot_read_fails(self) -> None:
        # A later pin that changes the warning format must not let every warning pass unread.
        for line in ("WARNING: b: prompt_slot_not_empty x", "warning[b]: prompt_slot_not_empty x", "warning: no code"):
            with self.subTest(line=line):
                self.assertTrue(self.judge(0, report(["a", "b"]), line + "\n"))
        # The same, if a later pin moved warnings into the JSON report.
        with self.subTest(report_key="warnings"):
            failures = self.judge(0, {**report(["a", "b"]), "warnings": [{"code": "prompt_slot_not_empty"}]})
            self.assertTrue(any("'warnings'" in line for line in failures))

    def test_file_not_held_warnings_are_returned_as_notices(self) -> None:
        stderr = "warning: a: file_not_held x/README.md: x/README.md: not held (notes)\n"
        self.assertEqual(gate.warnings(stderr), [("a", "file_not_held", "x/README.md: x/README.md: not held (notes)")])


class JudgeAnInvalidFixture(unittest.TestCase):
    """Non-vacuity: every invalid fixture is refused with the code its expected-code names."""

    def judge(self, exit_code: int, document: dict | None, expected: str) -> list[str]:
        return gate.judge_invalid(gate.Result(exit_code=exit_code, report=document, stderr=""), expected)

    def test_a_refusal_naming_the_expected_code_passes(self) -> None:
        self.assertEqual(self.judge(1, report(["x"], problems=[problem("validation_failed", "retired")]), "retired"), [])
        self.assertEqual(self.judge(1, report(["x"], problems=[problem("pack_dependency_unknown")]),
                                    "pack_dependency_unknown"), [])

    def test_an_accepted_fixture_fails(self) -> None:
        self.assertTrue(self.judge(0, report(["x"]), "retired"))

    def test_a_refusal_with_another_code_fails(self) -> None:
        self.assertTrue(self.judge(1, report(["x"], problems=[problem("validation_failed", "retired")]),
                                   "pack_dependency_unknown"))

    def test_the_report_of_an_invalid_fixture_is_read_as_strictly_as_the_sets(self) -> None:
        # FR-005, #349: a refusal read from a report the gate cannot read proves nothing.
        refused = report(["x"], problems=[problem("validation_failed", "retired")])
        cases = {"tool.name": {**refused, "tool": {"name": "pack-check", "version": "x"}},
                 "summary.exit_code": {**refused, "summary": {**refused["summary"], "exit_code": 0}},
                 "a key this gate cannot read": {**refused, "repairs": []},
                 "inputs.options": {**refused, "inputs": {"packs": ["x"], "options": {}}}}
        for needle, document in cases.items():
            with self.subTest(fault=needle):
                failures = self.judge(1, document, "retired")
                self.assertTrue(any(needle in line for line in failures), failures)

    def test_a_malformed_pack_version_is_a_problem_not_a_crash(self) -> None:
        # #343: rc.3 crashed on it (exit 2, charter#624); pack-doctor refuses it as pack_version_invalid (exit 1).
        refused = report(["x"], problems=[problem("validation_failed", "pack_version_invalid")])
        self.assertEqual(self.judge(1, refused, "pack_version_invalid"), [])

    def test_exit_2_is_never_taken_for_an_expected_code(self) -> None:
        # The retired `failed` expectation: exit 2 judged nothing, so no expectation matches it.
        for expected in ("retired", "failed", "pack_version_invalid"):
            with self.subTest(expected=expected):
                self.assertTrue(self.judge(2, None, expected))


class CommandFor(unittest.TestCase):
    """The run's argument vector is built from checked values only (SonarCloud S8701/S8705)."""

    def test_only_existing_files_and_resolved_pack_directories_reach_the_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            java, jar, pack = root / "java", root / "pack-doctor.jar", root / "packs" / "a"
            java.write_text("#!/bin/sh\n")
            java.chmod(0o755)
            jar.write_bytes(b"jar")
            pack.mkdir(parents=True)
            relative = Path(os.path.relpath(pack))
            report_file = root / "report" / "packs.yaml"
            command = gate.command_for(str(java), jar, [relative], report_file)
            self.assertEqual(command, [str(java.resolve()), "-jar", str(jar.resolve()), "validate",
                                       "--pack", str(pack.resolve()), "--round-trip", "--full",
                                       "--report", str(report_file.resolve())])
            for bad_java, bad_jar, bad_pack in ((str(root / "nope"), jar, pack), (str(jar), jar, pack),
                                                (str(java), root / "x.zip", pack), (str(java), jar, root / "missing"),
                                                (str(java), jar, Path("--config-root"))):
                with self.subTest(java=bad_java, jar=bad_jar, pack=bad_pack), self.assertRaises(gate.GateError):
                    gate.command_for(bad_java, bad_jar, [bad_pack], report_file)

    def test_a_report_inside_a_pack_is_refused_by_its_real_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            java, jar, pack = root / "java", root / "pack-doctor.jar", root / "packs" / "a"
            java.write_text("#!/bin/sh\n")
            java.chmod(0o755)
            jar.write_bytes(b"jar")
            (pack / "sub").mkdir(parents=True)
            (root / "into-pack").symlink_to(pack, target_is_directory=True)
            (root / "dangling").symlink_to(pack / "nope.yaml")
            (root / "pack-link").symlink_to(pack, target_is_directory=True)
            cases = {"a directory symlink into the pack": ([pack], root / "into-pack" / "r.yaml"),
                     "a file symlink into the pack": ([pack], root / "dangling"),
                     "a pack given by a symlink": ([root / "pack-link"], pack / "r.yaml"),
                     "a .. path": ([pack], root / "packs" / "x" / ".." / "a" / "r.yaml"),
                     "the pack directory itself": ([pack], pack)}
            for name, (packs, target) in cases.items():
                with self.subTest(case=name), self.assertRaises(gate.GateError):
                    gate.command_for(str(java), jar, packs, target)

    def test_a_report_file_inside_a_pack_is_refused(self) -> None:
        # pack-doctor refuses a report inside a pack it checks; the gate never asks for one.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            java, jar, pack = root / "java", root / "pack-doctor.jar", root / "packs" / "a"
            java.write_text("#!/bin/sh\n")
            java.chmod(0o755)
            jar.write_bytes(b"jar")
            pack.mkdir(parents=True)
            for inside in (pack / "report.yaml", pack / "sub" / "report.yaml"):
                with self.subTest(report=inside), self.assertRaises(gate.GateError):
                    gate.command_for(str(java), jar, [pack], inside)


class ExpectedCode(unittest.TestCase):
    def test_two_pack_doctor_lines_are_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "expected-code").write_text("pack-doctor: retired\npack-doctor: case_variant\n")
            with self.assertRaises(gate.GateError):
                gate.expected_pack_doctor(Path(tmp))

    def test_the_pack_doctor_line_is_read_and_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp)
            (fixture / "expected-code").write_text("# note\ncomposition: x  # c\npack-doctor: retired  # why\n")
            self.assertEqual(gate.expected_pack_doctor(fixture), "retired")
            for text in ("composition: x\n", "pack-doctor: Not A Code\n",
                         "pack-check: retired\n"):  # the old key is read no more (#345): no line, so refused
                (fixture / "expected-code").write_text(text)
                with self.subTest(text=text), self.assertRaises(gate.GateError):
                    gate.expected_pack_doctor(fixture)

    def test_every_invalid_fixture_names_its_pack_doctor_code(self) -> None:
        fixtures = sorted(path for path in (ROOT / "tests" / "fixtures" / "invalid").iterdir() if path.is_dir())
        self.assertEqual(len(fixtures), 5)
        expected = {fixture.name: gate.expected_pack_doctor(fixture) for fixture in fixtures}
        # #343: the two expectations that lagged charter main now name what pack-doctor answers.
        self.assertEqual(expected["case-variant-readme"], "case_variant")
        self.assertEqual(expected["malformed-pack-version"], "pack_version_invalid")


STUB = textwrap.dedent("""\
    #!/usr/bin/env python3
    # A stand-in for `java -jar pack-doctor.jar validate ...`: answers from the JSON plan in $STUB_PLAN, keyed by
    # whether the run is the set run (more than one --pack) or names a fixture directory. With "names": "auto" it
    # writes a PackDoctorReport over the packs it was given, refusing them with the plan's "codes" when there are any,
    # to standard output and, as pack-doctor does, to the --report file.
    import json, os, sys
    plan = json.load(open(os.environ["STUB_PLAN"]))
    packs = [sys.argv[i + 1] for i, arg in enumerate(sys.argv) if arg == "--pack"]
    target = next((sys.argv[i + 1] for i, arg in enumerate(sys.argv) if arg == "--report"), None)
    key = "set" if len(packs) > 1 else os.path.basename(packs[0].rstrip("/"))
    answer = plan.get(key, plan.get("default"))
    if answer.get("names") == "auto":
        codes = answer.get("codes", [])
        problems = [{"title": "Validation failed", "status": 422, "code": "validation_failed",
                     "violations": [{"pointer": "pack.yaml", "code": c, "detail": c} for c in codes]}] if codes else []
        answer["stdout"] = json.dumps({"tool": {"name": "pack-doctor", "version": "stub"},
            "inputs": {"packs": packs, "options": {"full": "--full" in sys.argv, "round_trip": "--round-trip" in sys.argv}},
            "checks": ["PACK", "CLOSURE", "REFERENCES", "ROUND_TRIP"], "problems": problems,
            "packs": [{"name": os.path.basename(p.rstrip("/")), "level": "org", "path": p} for p in packs],
            "summary": {"packs": len(packs), "violations": len(codes), "warnings": 0, "notices": 0,
                        "exit_code": answer["exit"]}})
        if target:
            open(target, "w").write(answer["stdout"])
    sys.stdout.write(answer.get("stdout", ""))
    sys.stderr.write(answer.get("stderr", ""))
    sys.exit(answer["exit"])
    """)
#: How the stand-in refuses the invalid fixture of the scratch repository, as pack-doctor does (#343).
REFUSED = {"exit": 1, "names": "auto", "codes": ["pack_version_invalid"]}


class EndToEnd(unittest.TestCase):
    """The script over a scratch repository, with the stand-in java."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.repo = self.tmp / "repo"
        for pack in ("packs/alpha", "packs/beta", "tests/fixtures/valid/example"):
            (self.repo / pack).mkdir(parents=True)
            (self.repo / pack / "pack.yaml").write_text("pack_version: 1.0.0\n")
        (self.repo / "packs" / "README.md").write_text("not a pack\n")
        bad = self.repo / "tests" / "fixtures" / "invalid" / "bad"
        bad.mkdir(parents=True)
        (bad / "pack.yaml").write_text("pack_version: nope\n")
        (bad / "expected-code").write_text("pack-doctor: pack_version_invalid\n")
        self.java = self.tmp / "java"
        self.java.write_text(STUB)
        self.java.chmod(0o755)
        self.jar = self.tmp / "pack-doctor.jar"
        self.jar.write_bytes(b"stub")

    def run_gate(self, plan: dict) -> subprocess.CompletedProcess:
        plan_file = self.tmp / "plan.json"
        plan_file.write_text(json.dumps(plan))
        env = dict(os.environ, STUB_PLAN=str(plan_file))
        return subprocess.run([sys.executable, str(SCRIPT), "--jar", str(self.jar), "--java", str(self.java),
                               "--root", str(self.repo), "--report-dir", str(self.tmp / "report")],
                              capture_output=True, text=True, env=env, check=False)

    def test_green_when_the_set_is_clean_and_every_invalid_fixture_is_refused_as_named(self) -> None:
        done = self.run_gate({"set": {"exit": 0, "names": "auto"}, "bad": REFUSED})
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        # Each run's --report YAML is kept with its stderr, outside every pack.
        for name in ("packs.yaml", "packs.stderr.txt", "invalid-bad.yaml", "invalid-bad.stderr.txt"):
            self.assertTrue((self.tmp / "report" / name).is_file(), name)

    def test_the_set_is_every_pack_and_valid_fixture_validated_with_round_trip_and_full(self) -> None:
        record = self.tmp / "argv.txt"
        self.java.write_text(STUB.replace("answer = plan.get", "open(%r, 'a').write(repr(sys.argv[1:]) + chr(10))\n"
                                          "answer = plan.get" % str(record), 1))
        self.run_gate({"set": {"exit": 0, "names": "auto"}, "bad": REFUSED})
        runs = [eval(line) for line in record.read_text().splitlines()]  # noqa: S307 (our own repr)
        set_run = next(argv for argv in runs if argv.count("--pack") > 1)
        self.assertEqual(set_run[:3], ["-jar", str(self.jar.resolve()), "validate"])
        self.assertIn("--round-trip", set_run)
        self.assertIn("--full", set_run)
        given = sorted(Path(set_run[i + 1]).relative_to(self.repo).as_posix()
                       for i, arg in enumerate(set_run) if arg == "--pack")
        self.assertEqual(given, ["packs/alpha", "packs/beta", "tests/fixtures/valid/example"])
        self.assertTrue(all(argv[2] == "validate" and "--round-trip" in argv and "--full" in argv for argv in runs))

    def test_a_pack_directory_without_a_pack_yaml_cannot_be_left_out_unseen(self) -> None:
        (self.repo / "packs" / "gamma").mkdir()
        (self.repo / "packs" / "gamma" / "pack.yml").write_text("misnamed\n")
        done = self.run_gate({"set": {"exit": 0, "names": "auto"}, "bad": REFUSED})
        self.assertEqual(done.returncode, 2, done.stdout)
        self.assertIn("gamma", done.stdout)

    def test_the_set_run_exiting_2_fails_the_gate(self) -> None:
        done = self.run_gate({"set": {"exit": 2, "stderr": "pack-doctor: cannot write the report\n"}, "bad": REFUSED})
        self.assertEqual(done.returncode, 1, done.stdout + done.stderr)
        self.assertIn("exited 2", done.stdout)

    def test_the_set_refused_with_the_curation_codes_fails_the_gate(self) -> None:
        done = self.run_gate({"set": {"exit": 1, "names": "auto", "codes": ["artifact_schema_error"]}, "bad": REFUSED})
        self.assertEqual(done.returncode, 1, done.stdout + done.stderr)
        self.assertIn("artifact_schema_error", done.stdout)

    def test_an_invalid_fixture_that_passes_fails_the_gate(self) -> None:
        done = self.run_gate({"set": {"exit": 0, "names": "auto"}, "bad": {"exit": 0, "names": "auto"}})
        self.assertEqual(done.returncode, 1, done.stdout + done.stderr)

    def test_the_fixture_is_judged_without_its_expected_code(self) -> None:
        # pack-doctor does not model expected-code, so a fixture carrying it would be red for that file alone.
        record = self.tmp / "seen.txt"
        stub = STUB.replace("answer = plan.get", "open(%r, 'a').write(repr(sorted(os.listdir(packs[0]))) + chr(10)) "
                            "if len(packs) == 1 else None\nanswer = plan.get" % str(record), 1)
        self.java.write_text(stub)
        self.run_gate({"set": {"exit": 0, "names": "auto"}, "default": {"exit": 2}})
        self.assertEqual(record.read_text().strip(), "['pack.yaml']")

    def test_a_report_dir_inside_a_pack_is_refused_before_anything_is_made_there(self) -> None:
        plan_file = self.tmp / "plan.json"
        plan_file.write_text(json.dumps({"set": {"exit": 0, "names": "auto"}, "bad": REFUSED}))
        inside = self.repo / "packs" / "alpha" / "report"
        done = subprocess.run([sys.executable, str(SCRIPT), "--jar", str(self.jar), "--java", str(self.java),
                               "--root", str(self.repo), "--report-dir", str(inside)],
                              capture_output=True, text=True, env=dict(os.environ, STUB_PLAN=str(plan_file)), check=False)
        self.assertEqual(done.returncode, 2, done.stdout)
        self.assertIn("must lie outside every pack", done.stdout)
        self.assertFalse(inside.exists())

    def test_a_missing_jar_cannot_run_and_fails(self) -> None:
        self.jar.unlink()
        done = self.run_gate({"set": {"exit": 0, "names": "auto"}})
        self.assertEqual(done.returncode, 2)


class JarScript(unittest.TestCase):
    """The two jar scripts on a release pin, with stand-in git and curl: what they run is what the lock pins."""

    COMMIT = "c" * 40
    # script, the lock key holding its jar's digest, the jar it prints
    SCRIPTS = (("charter_pack_doctor_jar.sh", "pack_doctor_sha256", "pack-doctor-1.0.0.jar"),
               ("charter_service_jar.sh", "jar_sha256", "spec-kitty-charter-service-1.0.0.jar"))
    RELEASE = "https://github.com/spec-kitty/spec-kitty-charter/releases/download/service-v1.0.0/"

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.repo = self.tmp / "repo"
        (self.repo / "scripts" / "ci").mkdir(parents=True)
        for name in ("charter_pack_doctor_jar.sh", "charter_service_jar.sh", "charter_release_asset.sh", "charter_lock.py"):
            shutil.copy2(ROOT / "scripts" / "ci" / name, self.repo / "scripts" / "ci" / name)
        self.jar_bytes = b"the pinned jar"
        import hashlib
        self.digest = hashlib.sha256(self.jar_bytes).hexdigest()
        self.bin = self.tmp / "bin"
        self.bin.mkdir()
        # curl writes the served bytes to --output (and may then fail); git ls-remote answers the tag's refs.
        (self.bin / "curl").write_text("#!/bin/sh\necho \"$*\" > \"$URL_LOG.args\"\nwhile [ $# -gt 0 ]; do [ \"$1\" = --output ] && out=\"$2\"; "
                                       "url=\"$1\"; shift; done\necho \"$url\" > \"$URL_LOG\"\n"
                                       "printf %s \"$SERVED\" > \"$out\"\n"
                                       "[ -z \"$CURL_EXIT\" ] || exit \"$CURL_EXIT\"\n")
        # An annotated tag lists its tag object, then its commit as `refs/tags/<tag>^{}`; a lightweight tag only its commit.
        (self.bin / "git").write_text(
            "#!/bin/sh\nt=refs/tags/service-v1.0.0\n"
            "if [ -n \"$TAG_OBJECT\" ]; then printf '%s\\t%s\\n%s\\t%s^{}\\n' \"$TAG_OBJECT\" $t \"$TAGGED\" $t\n"
            "else printf '%s\\t%s\\n' \"$TAGGED\" $t; fi\n")
        for tool in ("curl", "git"):
            (self.bin / tool).chmod(0o755)

    def run_script(self, script: str, key: str, *, digest: str, tagged: str, served: bytes,
                   curl_exit: int = 0, tag_object: str = "") -> subprocess.CompletedProcess:
        digests = {"pack_doctor_sha256": "a" * 64, "jar_sha256": "a" * 64, key: digest}
        (self.repo / "charter.lock.yaml").write_text(
            f"commit: {self.COMMIT}\nrelease_tag: service-v1.0.0\njar_sha256: {digests['jar_sha256']}\n"
            f"pack_doctor_sha256: {digests['pack_doctor_sha256']}\n")
        env = dict(os.environ, PATH=f"{self.bin}{os.pathsep}{os.environ['PATH']}", TAGGED=tagged, TAG_OBJECT=tag_object,
                   SERVED=served.decode(), URL_LOG=str(self.tmp / "url"), CURL_EXIT=str(curl_exit or ""))
        return subprocess.run(["bash", str(self.repo / "scripts" / "ci" / script), str(self.tmp / "work")],
                              capture_output=True, text=True, env=env, check=False)

    def test_the_pinned_jar_is_printed(self) -> None:
        for script, key, jar in self.SCRIPTS:
            with self.subTest(script=script):
                done = self.run_script(script, key, digest=self.digest, tagged=self.COMMIT, served=self.jar_bytes)
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(done.stdout.splitlines(), [str(self.tmp / "work" / jar)])
                # The release of the pinned tag, by name: never a floating "latest".
                self.assertEqual((self.tmp / "url").read_text().strip(), self.RELEASE + jar)
                # Over https only, redirects included: a downgrade to http is never followed.
                arguments = (self.tmp / "url.args").read_text()
                self.assertIn("--proto =https", arguments)
                self.assertIn("--proto-redir =https", arguments)

    def test_a_jar_with_another_digest_is_refused_and_no_path_is_printed(self) -> None:
        for script, key, jar in self.SCRIPTS:
            with self.subTest(script=script):
                done = self.run_script(script, key, digest=self.digest, tagged=self.COMMIT, served=b"some other jar")
                self.assertNotEqual(done.returncode, 0)
                self.assertEqual(done.stdout, "")
                self.assertIn("refusing to run it", done.stderr)
                self.assertEqual(list((self.tmp / "work").iterdir()), [])  # the unverified download is gone

    def test_a_failed_download_leaves_nothing_in_the_work_dir(self) -> None:
        for script, key, jar in self.SCRIPTS:
            with self.subTest(script=script):
                done = self.run_script(script, key, digest=self.digest, tagged=self.COMMIT, served=b"half a jar",
                                       curl_exit=22)
                self.assertNotEqual(done.returncode, 0)
                self.assertEqual(done.stdout, "")
                self.assertEqual(list((self.tmp / "work").iterdir()), [])  # neither the jar nor a partial file

    def test_a_tag_that_points_elsewhere_than_the_lock_commit_is_refused(self) -> None:
        other = "d" * 40
        # (what the tag's commit is, the annotated tag object's own sha or "" for a lightweight tag, accepted)
        cases = {"lightweight tag elsewhere": (other, "", False),
                 "annotated tag whose commit is the lock's": (self.COMMIT, other, True),
                 "annotated tag whose object is the lock's sha but whose commit is elsewhere": (other, self.COMMIT, False)}
        for script, key, jar in self.SCRIPTS:
            for name, (tagged, tag_object, accepted) in cases.items():
                with self.subTest(script=script, tag=name):
                    done = self.run_script(script, key, digest=self.digest, tagged=tagged, tag_object=tag_object,
                                           served=self.jar_bytes)
                    if accepted:
                        self.assertEqual(done.returncode, 0, done.stderr)
                        shutil.rmtree(self.tmp / "work")  # the next case starts with an empty work dir
                        continue
                    self.assertNotEqual(done.returncode, 0)
                    self.assertEqual(done.stdout, "")
                    self.assertIn("names two charters", done.stderr)
                    self.assertFalse((self.tmp / "work").exists() and list((self.tmp / "work").iterdir()))  # no download


#: The codes the set run over this checkout may carry until the curation lands (#345 item 7, #350): the inline
#: ``anti_patterns`` blocks, the file-less ``anti_pattern`` nodes, their knock-on substep delegations, and the round
#: trip's knock-ons. WP08 (the curation) and WP09 (the restamp) clear them; the problem code wrapping them is
#: ``validation_failed``.
CURATION_CODES = {"validation_failed", "artifact_schema_error", "drg_schema_error", "substep_delegation_unresolved",
                  "round_trip_red", "round_trip_written_unpaired"}


@unittest.skipUnless(os.environ.get("PACK_DOCTOR_JAR"), "PACK_DOCTOR_JAR names no pack-doctor jar")
class RealPackDoctor(unittest.TestCase):
    """Against the real jar of the pin (the Charter service validation job sets PACK_DOCTOR_JAR)."""

    checkout: subprocess.CompletedProcess | None = None

    @staticmethod
    def gate(repo: Path) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(SCRIPT), "--jar", os.environ["PACK_DOCTOR_JAR"], "--root", str(repo)],
                              capture_output=True, text=True, check=False)

    @classmethod
    def gate_over_this_checkout(cls) -> subprocess.CompletedProcess:
        if cls.checkout is None:
            cls.checkout = cls.gate(ROOT)  # one run, read by the two tests below
        return cls.checkout

    def test_every_invalid_fixture_is_refused_as_its_expected_code_says(self) -> None:
        # The five fixtures (case_variant and pack_version_invalid since #343), beside one valid pack so the set passes.
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            shutil.copytree(ROOT / "tests" / "fixtures" / "valid" / "example-pack", repo / "packs" / "example-pack")
            shutil.copytree(ROOT / "tests" / "fixtures" / "invalid", repo / "tests" / "fixtures" / "invalid")
            done = self.gate(repo)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        for fixture in sorted((ROOT / "tests" / "fixtures" / "invalid").iterdir()):
            with self.subTest(fixture=fixture.name):
                self.assertIn(f"ok: pack-doctor refuses invalid fixture {fixture.name} as expected "
                              f"({gate.expected_pack_doctor(fixture)})", done.stdout)

    def test_the_set_report_parses_and_holds_only_the_curation_codes(self) -> None:
        packs = gate.pack_dirs(ROOT / "packs") + gate.pack_dirs(ROOT / "tests" / "fixtures" / "valid")
        with tempfile.TemporaryDirectory() as tmp:
            result = gate.run(gate.java_command(None), Path(os.environ["PACK_DOCTOR_JAR"]), packs,
                              Path(tmp) / "packs.yaml")
        self.assertIn(result.exit_code, (0, 1), result.stderr[-2000:])
        self.assertIsNotNone(result.report)
        self.assertEqual(gate.report_faults(result), [])
        self.assertEqual(list(result.report["checks"])[:1], ["PACK"])
        self.assertLessEqual(gate.codes(result.report), CURATION_CODES, gate.problem_lines(result.report)[:20])

    def test_the_gate_gives_this_checkout_a_verdict(self) -> None:
        # The known red below must be a verdict (exit 0 or 1), never a run that judged nothing (exit 2).
        done = self.gate_over_this_checkout()
        self.assertIn(done.returncode, (0, 1), done.stdout[-4000:])

    @unittest.expectedFailure  # the set's known red: cleared by WP08/WP09, and WP09 removes this marker
    def test_the_gate_passes_this_checkout(self) -> None:
        done = self.gate_over_this_checkout()
        self.assertEqual(done.returncode, 0, done.stdout[-4000:])


if __name__ == "__main__":
    unittest.main()
