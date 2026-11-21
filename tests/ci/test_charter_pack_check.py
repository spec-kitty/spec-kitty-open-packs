"""The pack-check gate (#252): charter's whole-pack check, run from the pinned release, judged fail-closed.

Most tests drive ``scripts/ci/charter_pack_check.py`` with a stand-in ``java`` that answers as pack-check would, so
they run anywhere. ``RealPackCheck`` runs the real jar when ``PACK_CHECK_JAR`` names one; the ``Charter service
validation`` job sets it to the jar of the pin, so the charter#624 case is proven against the real release there.
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

import charter_pack_check as gate  # noqa: E402

SCRIPT = ROOT / "scripts" / "ci" / "charter_pack_check.py"
ALL_CHECKS = ["PACK", "CLOSURE", "ROUND_TRIP"]


def report(names: list[str], *, problems: list | None = None, checks: list[str] | None = None,
           skipped: list | None = None) -> dict:
    document = {"checks": checks or ALL_CHECKS,
                "packs": [{"name": name, "level": "org", "path": f"./packs/{name}"} for name in names],
                "problems": problems or []}
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

    def test_exit_2_fails_closed_and_names_charter_624(self) -> None:
        # R32: until charter#624 lands, a crash is a failure of the gate, never an infrastructure skip.
        failures = self.judge(2, None, "Exception in thread main java.lang.IllegalArgumentException: bad version\n")
        self.assertTrue(failures)
        self.assertIn("exited 2", failures[0])
        self.assertIn("spec-kitty-charter#624", failures[0])
        self.assertTrue(any("IllegalArgumentException" in line for line in failures))

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

    def test_a_skipped_or_missing_check_fails(self) -> None:
        self.assertTrue(self.judge(0, report(["a", "b"], checks=["PACK", "ROUND_TRIP"])))
        skipped = [{"check": "CLOSURE", "reason": "no facts"}]
        self.assertTrue(self.judge(0, report(["a", "b"], skipped=skipped)))

    def test_a_pack_left_out_or_added_fails(self) -> None:
        self.assertTrue(self.judge(0, report(["a"])))
        self.assertTrue(self.judge(0, report(["a", "b", "c"])))

    def test_a_warning_other_than_file_not_held_fails(self) -> None:
        # driftTest, which this replaces, failed on every load warning; file_not_held stays a notice here because the
        # schema pass owns the stray-file rule (#249).
        stderr = "warning: b: prompt_slot_not_empty missions/x/prompt.md: legacy text in a slot\n"
        failures = self.judge(0, report(["a", "b"]), stderr)
        self.assertTrue(any("prompt_slot_not_empty" in line for line in failures))

    def test_a_warning_in_a_format_the_gate_cannot_read_fails(self) -> None:
        # A later pin that changes the warning format must not let every warning pass unread.
        for line in ("WARNING: b: prompt_slot_not_empty x", "warning[b]: prompt_slot_not_empty x", "warning: no code"):
            with self.subTest(line=line):
                self.assertTrue(self.judge(0, report(["a", "b"]), line + "\n"))

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

    def test_failed_expects_exactly_the_charter_624_crash(self) -> None:
        # The charter#624 tripwire: once pack-check reports the fault instead of crashing, `failed` no longer matches
        # and the fixture must name the code pack-check then gives. A usage or I/O failure, a report, or another crash
        # (each also exit 2) must not pass for it.
        def judge(exit_code: int, document: dict | None, stderr: str) -> list[str]:
            return gate.judge_invalid(gate.Result(exit_code=exit_code, report=document, stderr=stderr), "failed")
        self.assertEqual(judge(2, None, CRASH_624), [])
        self.assertTrue(judge(2, None, "usage: pack-check (--config-root <dir> | --pack <dir> ...)"))
        self.assertTrue(judge(2, None, "pack-check: internal error: java.io.UncheckedIOException: disk"))
        self.assertTrue(judge(2, None, "pack-check: internal error: java.lang.NullPointerException: pack_version"))
        self.assertTrue(judge(2, report(["x"]), CRASH_624))
        self.assertTrue(judge(1, report(["x"], problems=[problem("validation_failed")]), CRASH_624))
        self.assertTrue(judge(0, report(["x"]), ""))

    def test_a_crash_is_never_taken_for_an_expected_code(self) -> None:
        self.assertTrue(self.judge(2, None, "retired"))


CRASH_624 = ("pack-check: internal error: java.lang.IllegalStateException: the resolver takes only well-formed "
             "descriptors, and pack.yaml of bad: pack_version 'nope' is not a PEP 440 version\n"
             "\tat ai.speckitty.charter.packs.domain.PackCompositionResolver.compose(PackCompositionResolver.java:367)\n")


class CommandFor(unittest.TestCase):
    """The run's argument vector is built from checked values only (SonarCloud S8701/S8705)."""

    def test_only_existing_files_and_resolved_pack_directories_reach_the_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            java, jar, pack = root / "java", root / "pack-check.jar", root / "packs" / "a"
            java.write_text("#!/bin/sh\n")
            java.chmod(0o755)
            jar.write_bytes(b"jar")
            pack.mkdir(parents=True)
            relative = Path(os.path.relpath(pack))
            command = gate.command_for(str(java), jar, [relative])
            self.assertEqual(command, [str(java.resolve()), "-jar", str(jar.resolve()), "--pack", str(pack.resolve()),
                                       "--round-trip"])
            for bad_java, bad_jar, bad_pack in ((str(root / "nope"), jar, pack), (str(jar), jar, pack),
                                                (str(java), root / "x.zip", pack), (str(java), jar, root / "missing"),
                                                (str(java), jar, Path("--config-root"))):
                with self.subTest(java=bad_java, jar=bad_jar, pack=bad_pack), self.assertRaises(gate.GateError):
                    gate.command_for(bad_java, bad_jar, [bad_pack])


class ExpectedCode(unittest.TestCase):
    def test_two_pack_check_lines_are_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "expected-code").write_text("pack-check: retired\npack-check: failed\n")
            with self.assertRaises(gate.GateError):
                gate.expected_pack_check(Path(tmp))

    def test_the_pack_check_line_is_read_and_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp)
            (fixture / "expected-code").write_text("# note\ncomposition: x  # c\npack-check: retired  # why\n")
            self.assertEqual(gate.expected_pack_check(fixture), "retired")
            (fixture / "expected-code").write_text("composition: x\n")
            with self.assertRaises(gate.GateError):
                gate.expected_pack_check(fixture)
            (fixture / "expected-code").write_text("pack-check: Not A Code\n")
            with self.assertRaises(gate.GateError):
                gate.expected_pack_check(fixture)

    def test_every_invalid_fixture_names_its_pack_check_code(self) -> None:
        fixtures = sorted(path for path in (ROOT / "tests" / "fixtures" / "invalid").iterdir() if path.is_dir())
        self.assertTrue(fixtures)
        for fixture in fixtures:
            with self.subTest(fixture=fixture.name):
                self.assertTrue(gate.expected_pack_check(fixture))

    def test_the_malformed_pack_version_fixture_is_otherwise_well_formed(self) -> None:
        # Only the version is wrong, so the gate's red comes from the version and nothing else.
        fixture = ROOT / "tests" / "fixtures" / "invalid" / "malformed-pack-version"
        descriptor = (fixture / "pack.yaml").read_text(encoding="utf-8")
        self.assertIn("pack_version: not-a-version", descriptor)
        self.assertEqual(gate.expected_pack_check(fixture), "failed")


STUB = textwrap.dedent("""\
    #!/usr/bin/env python3
    # A stand-in for `java -jar pack-check.jar`: answers from the JSON plan in $STUB_PLAN, keyed by whether the
    # run is the set run (more than one --pack) or names a fixture directory.
    import json, os, sys
    plan = json.load(open(os.environ["STUB_PLAN"]))
    packs = [sys.argv[i + 1] for i, arg in enumerate(sys.argv) if arg == "--pack"]
    key = "set" if len(packs) > 1 else os.path.basename(packs[0].rstrip("/"))
    answer = plan.get(key, plan.get("default"))
    if answer.get("names") == "auto":
        answer["stdout"] = json.dumps({"checks": ["PACK", "CLOSURE", "ROUND_TRIP"], "problems": [],
            "packs": [{"name": os.path.basename(p.rstrip("/")), "level": "org", "path": p} for p in packs]})
    sys.stdout.write(answer.get("stdout", ""))
    sys.stderr.write(answer.get("stderr", ""))
    sys.exit(answer["exit"])
    """)


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
        (bad / "expected-code").write_text("pack-check: failed\n")
        self.java = self.tmp / "java"
        self.java.write_text(STUB)
        self.java.chmod(0o755)
        self.jar = self.tmp / "pack-check.jar"
        self.jar.write_bytes(b"stub")

    def run_gate(self, plan: dict) -> subprocess.CompletedProcess:
        plan_file = self.tmp / "plan.json"
        plan_file.write_text(json.dumps(plan))
        env = dict(os.environ, STUB_PLAN=str(plan_file))
        return subprocess.run([sys.executable, str(SCRIPT), "--jar", str(self.jar), "--java", str(self.java),
                               "--root", str(self.repo), "--report-dir", str(self.tmp / "report")],
                              capture_output=True, text=True, env=env, check=False)

    def test_green_when_the_set_is_clean_and_every_invalid_fixture_is_refused_as_named(self) -> None:
        done = self.run_gate({"set": {"exit": 0, "names": "auto"}, "bad": {"exit": 2, "stderr": CRASH_624}})
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertTrue((self.tmp / "report" / "packs.json").is_file())

    def test_the_set_is_every_pack_and_valid_fixture_with_the_round_trip(self) -> None:
        record = self.tmp / "argv.txt"
        self.java.write_text(STUB.replace("answer = plan.get", "open(%r, 'a').write(repr(sys.argv[1:]) + chr(10))\n"
                                          "answer = plan.get" % str(record), 1))
        self.run_gate({"set": {"exit": 0, "names": "auto"}, "bad": {"exit": 2, "stderr": CRASH_624}})
        runs = [eval(line) for line in record.read_text().splitlines()]  # noqa: S307 (our own repr)
        set_run = next(argv for argv in runs if argv.count("--pack") > 1)
        self.assertIn("--round-trip", set_run)
        given = sorted(Path(set_run[i + 1]).relative_to(self.repo).as_posix()
                       for i, arg in enumerate(set_run) if arg == "--pack")
        self.assertEqual(given, ["packs/alpha", "packs/beta", "tests/fixtures/valid/example"])
        self.assertTrue(all("--round-trip" in argv for argv in runs))

    def test_a_pack_directory_without_a_pack_yaml_cannot_be_left_out_unseen(self) -> None:
        (self.repo / "packs" / "gamma").mkdir()
        (self.repo / "packs" / "gamma" / "pack.yml").write_text("misnamed\n")
        done = self.run_gate({"set": {"exit": 0, "names": "auto"}, "bad": {"exit": 2, "stderr": CRASH_624}})
        self.assertEqual(done.returncode, 2, done.stdout)
        self.assertIn("gamma", done.stdout)

    def test_the_set_run_crashing_with_exit_2_fails_the_gate(self) -> None:
        # The red-first case of R32: a malformed pack_version among the packs crashes rc.3 with exit 2.
        done = self.run_gate({"set": {"exit": 2, "stderr": CRASH_624}, "bad": {"exit": 2, "stderr": CRASH_624}})
        self.assertEqual(done.returncode, 1, done.stdout + done.stderr)
        self.assertIn("spec-kitty-charter#624", done.stdout)

    def test_an_invalid_fixture_that_passes_fails_the_gate(self) -> None:
        done = self.run_gate({"set": {"exit": 0, "names": "auto"}, "bad": {"exit": 0, "names": "auto"}})
        self.assertEqual(done.returncode, 1, done.stdout + done.stderr)

    def test_the_fixture_is_judged_without_its_expected_code(self) -> None:
        # pack-check does not model expected-code, so a fixture carrying it would be red for that file alone.
        record = self.tmp / "seen.txt"
        stub = STUB.replace("answer = plan.get", "open(%r, 'a').write(repr(sorted(os.listdir(packs[0]))) + chr(10)) "
                            "if len(packs) == 1 else None\nanswer = plan.get" % str(record), 1)
        self.java.write_text(stub)
        self.run_gate({"set": {"exit": 0, "names": "auto"}, "default": {"exit": 2}})
        self.assertEqual(record.read_text().strip(), "['pack.yaml']")

    def test_a_missing_jar_cannot_run_and_fails(self) -> None:
        self.jar.unlink()
        done = self.run_gate({"set": {"exit": 0, "names": "auto"}})
        self.assertEqual(done.returncode, 2)


class JarScript(unittest.TestCase):
    """The two jar scripts on a release pin, with stand-in git and curl: what they run is what the lock pins."""

    COMMIT = "c" * 40
    # script, the lock key holding its jar's digest, the jar it prints
    SCRIPTS = (("charter_pack_check_jar.sh", "pack_check_sha256", "pack-check-1.0.0.jar"),
               ("charter_service_jar.sh", "jar_sha256", "spec-kitty-charter-service-1.0.0.jar"))
    RELEASE = "https://github.com/spec-kitty/spec-kitty-charter/releases/download/service-v1.0.0/"

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.repo = self.tmp / "repo"
        (self.repo / "scripts" / "ci").mkdir(parents=True)
        for name in ("charter_pack_check_jar.sh", "charter_service_jar.sh", "charter_release_asset.sh", "charter_lock.py"):
            shutil.copy2(ROOT / "scripts" / "ci" / name, self.repo / "scripts" / "ci" / name)
        self.jar_bytes = b"the pinned jar"
        import hashlib
        self.digest = hashlib.sha256(self.jar_bytes).hexdigest()
        self.bin = self.tmp / "bin"
        self.bin.mkdir()
        # curl writes the served bytes to --output (and may then fail); git ls-remote answers the tag's refs.
        (self.bin / "curl").write_text("#!/bin/sh\nwhile [ $# -gt 0 ]; do [ \"$1\" = --output ] && out=\"$2\"; "
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
        digests = {"pack_check_sha256": "a" * 64, "jar_sha256": "a" * 64, key: digest}
        (self.repo / "charter.lock.yaml").write_text(
            f"commit: {self.COMMIT}\nrelease_tag: service-v1.0.0\njar_sha256: {digests['jar_sha256']}\n"
            f"pack_check_sha256: {digests['pack_check_sha256']}\n")
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


@unittest.skipUnless(os.environ.get("PACK_CHECK_JAR"), "PACK_CHECK_JAR names no pack-check jar")
class RealPackCheck(unittest.TestCase):
    """Against the real jar of the pin (the Charter service validation job sets PACK_CHECK_JAR)."""

    FIXTURE = ROOT / "tests" / "fixtures" / "invalid" / "malformed-pack-version"

    def test_a_malformed_pack_version_among_the_packs_fails_the_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            shutil.copytree(ROOT / "tests" / "fixtures" / "valid" / "example-pack", repo / "packs" / "example-pack")
            shutil.copytree(ROOT / "tests" / "fixtures" / "invalid" / "malformed-pack-version",
                            repo / "packs" / "malformed-pack-version", ignore=shutil.ignore_patterns("expected-code"))
            # The real invalid fixtures, so the only red is the set's.
            shutil.copytree(ROOT / "tests" / "fixtures" / "invalid", repo / "tests" / "fixtures" / "invalid")
            done = subprocess.run([sys.executable, str(SCRIPT), "--jar", os.environ["PACK_CHECK_JAR"],
                                   "--root", str(repo)], capture_output=True, text=True, check=False)
        output = done.stdout + done.stderr
        self.assertEqual(done.returncode, 1, output)
        # Holds before and after charter#624: the set fails on the malformed version, and the invalid fixture is
        # refused as its expected-code says. Only the fixture's 'pack-check:' line changes when #624 is fixed.
        self.assertNotIn("::error::pack-check: invalid fixture", done.stdout)
        self.assertIn("ok: pack-check refuses invalid fixture malformed-pack-version as expected", done.stdout)
        if gate.expected_pack_check(self.FIXTURE) == gate.FAILED:
            self.assertIn(gate.CRASH_ISSUE, done.stdout)  # still the crash, so the gate must name it


if __name__ == "__main__":
    unittest.main()
