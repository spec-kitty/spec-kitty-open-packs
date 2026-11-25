"""charter_pin.py: release ordering, the lock rewrite, the changelog entry and the API commit payload (#253).

No test touches the network: the resolvers are tested only where they refuse input before any call.
"""

from __future__ import annotations

import base64
import json
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts" / "ci"))

import charter_lock  # noqa: E402
import charter_pin  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
COMMIT = "a" * 40
DIGEST = "b" * 64
PACK_DIGEST = "c" * 64


class ReleaseOrder(unittest.TestCase):
    def test_semantic_version_precedence_with_pre_releases(self) -> None:
        ordered = [
            "service-v0.1.0-1", "service-v0.1.0-alpha", "service-v0.1.0-alpha.1", "service-v0.1.0-rc.1",
            "service-v0.1.0-rc.2", "service-v0.1.0-rc.10", "service-v0.1.0", "service-v0.1.1-rc.1",
            "service-v0.2.0", "service-v0.10.0", "service-v1.0.0",
        ]
        self.assertEqual(sorted(reversed(ordered), key=charter_pin.precedence), ordered)

    def test_the_newest_counts_pre_releases_and_ignores_other_tags(self) -> None:
        tags = ["v9.9.9", "service-v0.1.0-rc.1", "service-v0.1.0-rc.2", "cli-v3.0.0", "service-v0.0.9"]
        self.assertEqual(charter_pin.newest(tags), "service-v0.1.0-rc.2")
        self.assertIsNone(charter_pin.newest(["v1.0.0"]))

    def test_hyphenated_pre_release_identifiers_are_tracked(self) -> None:
        self.assertEqual(charter_pin.newest(["service-v1.0.0-rc-1", "service-v0.9.0"]), "service-v1.0.0-rc-1")
        self.assertTrue(charter_lock.RELEASE_TAG.fullmatch("service-v1.0.0-rc-1"))
        self.assertLess(charter_pin.precedence("service-v1.0.0-rc-1"), charter_pin.precedence("service-v1.0.0"))

    def test_a_tag_outside_the_service_line_is_refused(self) -> None:
        with self.assertRaises(charter_pin.PinError):
            charter_pin.precedence("v0.1.0")


class NewestRelease(unittest.TestCase):
    def run_main(self, current: str, tags: list[str]) -> dict[str, str]:
        lock = {"commit": COMMIT, "release_tag": current, "jar_sha256": DIGEST if current else "",
                "pack_doctor_sha256": DIGEST if current else ""}
        out = io.StringIO()
        with mock.patch.object(charter_lock, "read", return_value=lock), \
             mock.patch.object(charter_pin, "release_tags", return_value=tags), redirect_stdout(out):
            self.assertEqual(charter_pin.main(["newest-release"]), 0)
        return dict(line.split("=", 1) for line in out.getvalue().splitlines())

    def test_newer_only_when_later_than_the_lock(self) -> None:
        tags = ["service-v0.1.0-rc.1", "service-v0.1.0-rc.2"]
        self.assertEqual(self.run_main("service-v0.1.0-rc.1", tags)["newer"], "true")
        self.assertEqual(self.run_main("service-v0.1.0-rc.2", tags)["newer"], "false")
        self.assertEqual(self.run_main("service-v0.1.0", tags)["newer"], "false")

    def test_a_main_pin_is_never_replaced_by_the_release_track(self) -> None:
        result = self.run_main("", ["service-v0.1.0-rc.2"])
        self.assertEqual((result["tag"], result["newer"]), ("service-v0.1.0-rc.2", "false"))


class AtOrPast(unittest.TestCase):
    def run_main(self, current: str, tag: str) -> int:
        lock = {"commit": COMMIT, "release_tag": current, "jar_sha256": DIGEST if current else "",
                "pack_doctor_sha256": DIGEST if current else ""}
        with mock.patch.object(charter_lock, "read", return_value=lock):
            return charter_pin.main(["at-or-past", tag])

    def test_the_lock_settles_a_release_it_reached_or_passed(self) -> None:
        self.assertEqual(self.run_main("service-v0.2.0", "service-v0.2.0"), 0)
        self.assertEqual(self.run_main("service-v0.2.0", "service-v0.2.0-rc.1"), 0)
        self.assertEqual(self.run_main("service-v0.2.0-rc.1", "service-v0.2.0"), 1)
        self.assertEqual(self.run_main("", "service-v0.2.0"), 1)


class ReleaseListing(unittest.TestCase):
    def test_every_page_is_read_and_drafts_are_left_out(self) -> None:
        first = [{"tag_name": f"service-v0.0.{n}", "draft": False} for n in range(99)]
        first.append({"tag_name": "service-v9.0.0", "draft": True})
        second = [{"tag_name": "service-v0.1.0-rc.1", "draft": False, "prerelease": True}]
        pages = {1: first, 2: second}
        def fake(url: str, *, api: bool) -> bytes:
            self.assertTrue(api)
            page = int(url.rsplit("page=", 1)[1])
            return json.dumps(pages[page]).encode()
        with mock.patch.object(charter_pin, "_request", side_effect=fake):
            tags = charter_pin.release_tags()
        self.assertNotIn("service-v9.0.0", tags)
        self.assertEqual(charter_pin.newest(tags), "service-v0.1.0-rc.1")

    def test_an_annotated_tag_peels_to_its_commit(self) -> None:
        refs = {"refs/tags/service-v1.0.0": "1" * 40, "refs/tags/service-v1.0.0^{}": "2" * 40}
        with mock.patch.object(charter_pin, "ls_remote", return_value=refs):
            self.assertEqual(charter_pin.tag_commit("service-v1.0.0"), "2" * 40)
        with mock.patch.object(charter_pin, "ls_remote", return_value={"refs/tags/service-v1.0.0": "1" * 40}):
            self.assertEqual(charter_pin.tag_commit("service-v1.0.0"), "1" * 40)

    def test_the_digest_asset_must_name_the_jar(self) -> None:
        good = f"{DIGEST}  spec-kitty-charter-service-1.0.0.jar\n".encode()
        with mock.patch.object(charter_pin, "_request", return_value=good):
            self.assertEqual(charter_pin.jar_digest("service-v1.0.0"), DIGEST)
        for text in (f"{DIGEST}  other.jar\n", "not-a-digest  spec-kitty-charter-service-1.0.0.jar\n", ""):
            with self.subTest(text=text), mock.patch.object(charter_pin, "_request", return_value=text.encode()), \
                 self.assertRaises(charter_pin.PinError):
                charter_pin.jar_digest("service-v1.0.0")

    def test_the_pack_doctor_digest_comes_from_its_own_asset_and_must_name_its_jar(self) -> None:
        # #345: the gate's pack-doctor jar is pinned by the digest the release's pack-doctor-<version>.jar.sha256 states.
        urls = []
        def fake(url: str, *, api: bool) -> bytes:
            urls.append(url)
            return f"{PACK_DIGEST}  pack-doctor-1.0.0.jar\n".encode()
        with mock.patch.object(charter_pin, "_request", side_effect=fake):
            self.assertEqual(charter_pin.jar_digest("service-v1.0.0", charter_pin.PACK_DOCTOR_JAR), PACK_DIGEST)
        self.assertEqual(urls, ["https://github.com/spec-kitty/spec-kitty-charter/releases/download/service-v1.0.0/"
                                "pack-doctor-1.0.0.jar.sha256"])
        with mock.patch.object(charter_pin, "_request",
                               return_value=f"{PACK_DIGEST}  spec-kitty-charter-service-1.0.0.jar\n".encode()), \
             self.assertRaises(charter_pin.PinError):
            charter_pin.jar_digest("service-v1.0.0", charter_pin.PACK_DOCTOR_JAR)

    def test_resolve_release_emits_both_digests_and_a_release_without_pack_doctor_cannot_resolve(self) -> None:
        def fake(url: str, *, api: bool) -> bytes:
            if url.endswith("/pack-doctor-1.0.0.jar.sha256"):
                return f"{PACK_DIGEST}  pack-doctor-1.0.0.jar\n".encode()
            return f"{DIGEST}  spec-kitty-charter-service-1.0.0.jar\n".encode()
        out = io.StringIO()
        with mock.patch.object(charter_pin, "_request", side_effect=fake), \
             mock.patch.object(charter_pin, "tag_commit", return_value=COMMIT), redirect_stdout(out):
            self.assertEqual(charter_pin.main(["resolve-release", "service-v1.0.0"]), 0)
        values = dict(line.split("=", 1) for line in out.getvalue().splitlines())
        self.assertEqual(values, {"commit": COMMIT, "release_tag": "service-v1.0.0", "jar_sha256": DIGEST,
                                  "pack_doctor_sha256": PACK_DIGEST})
        def missing(url: str, *, api: bool) -> bytes:
            if "pack-doctor" in url:
                raise charter_pin.PinError("404")
            return fake(url, api=api)
        with mock.patch.object(charter_pin, "_request", side_effect=missing), \
             mock.patch.object(charter_pin, "tag_commit", return_value=COMMIT), redirect_stdout(io.StringIO()), \
             redirect_stderr(io.StringIO()):
            self.assertEqual(charter_pin.main(["resolve-release", "service-v1.0.0"]), 2)


class ResolveRef(unittest.TestCase):
    def test_a_full_commit_is_taken_as_is_without_a_call(self) -> None:
        with mock.patch.object(charter_pin, "ls_remote", side_effect=AssertionError("no call")):
            self.assertEqual(charter_pin.resolve_ref(COMMIT), COMMIT)

    def test_shell_and_revision_syntax_is_refused_before_any_call(self) -> None:
        with mock.patch.object(charter_pin, "ls_remote", side_effect=AssertionError("no call")):
            for ref in ("x;rm -rf /", "main..dev", "-upload-pack=x", "a b", "$(id)", "HEAD~1", "main^{}", ""):
                with self.subTest(ref=ref), self.assertRaises(charter_pin.PinError):
                    charter_pin.resolve_ref(ref)

    def test_a_branch_wins_over_a_tag_and_a_pull_ref_is_looked_up_as_such(self) -> None:
        refs = {"refs/heads/main": "1" * 40, "refs/tags/main": "2" * 40, "refs/pull/7/head": "3" * 40}
        with mock.patch.object(charter_pin, "ls_remote", side_effect=lambda *names: {n: refs[n] for n in names if n in refs}):
            self.assertEqual(charter_pin.resolve_ref("main"), "1" * 40)
            self.assertEqual(charter_pin.resolve_ref("pull/7/head"), "3" * 40)
            with self.assertRaises(charter_pin.PinError):
                charter_pin.resolve_ref("missing")


class WriteLock(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.lock = self.tmp / "charter.lock.yaml"
        shutil.copyfile(ROOT / "charter.lock.yaml", self.lock)
        patcher = mock.patch.object(charter_lock, "LOCK_FILE", self.lock)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_a_release_pin_and_a_main_pin_read_back_and_keep_the_comments(self) -> None:
        comments = [line for line in self.lock.read_text(encoding="utf-8").splitlines() if line.startswith("#")]
        charter_pin.write_lock(COMMIT, "service-v9.0.0-rc.1", DIGEST, PACK_DIGEST)
        self.assertEqual(charter_lock.read(self.lock),
                         {"commit": COMMIT, "release_tag": "service-v9.0.0-rc.1", "jar_sha256": DIGEST,
                          "pack_doctor_sha256": PACK_DIGEST})
        charter_pin.write_lock(COMMIT, "", "", "")
        self.assertEqual(charter_lock.read(self.lock),
                         {"commit": COMMIT, "release_tag": "", "jar_sha256": "", "pack_doctor_sha256": ""})
        kept = [line for line in self.lock.read_text(encoding="utf-8").splitlines() if line.startswith("#")]
        self.assertEqual(kept, comments)

    def test_a_malformed_pin_is_refused_and_the_file_is_left_alone(self) -> None:
        before = self.lock.read_text(encoding="utf-8")
        for commit, tag, digest, pack_doctor in (
                ("main", "", "", ""), (COMMIT, "v1.0.0", DIGEST, PACK_DIGEST), (COMMIT, "service-v1.0.0", "", ""),
                (COMMIT, "service-v1.0.0", "x" * 64, PACK_DIGEST), (COMMIT, "service-v1.0.0", DIGEST, ""),
                (COMMIT, "service-v1.0.0", DIGEST, "x" * 64), (COMMIT, "", "", PACK_DIGEST)):
            with self.subTest(commit=commit, tag=tag, digest=digest, pack_doctor=pack_doctor), \
                 self.assertRaises(charter_pin.PinError):
                charter_pin.write_lock(commit, tag, digest, pack_doctor)
        self.assertEqual(self.lock.read_text(encoding="utf-8"), before)


class Changelog(unittest.TestCase):
    def write(self, text: str) -> Path:
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        path = tmp / "CHANGELOG.md"
        path.write_text(text, encoding="utf-8")
        return path

    def test_the_entry_is_first_under_unreleased_changed_and_the_page_is_dated(self) -> None:
        path = self.write("---\nupdated: '2026-01-01'\n---\n# Changelog\n\n## [Unreleased]\n\n### ✨ Added\n\n- a\n\n"
                          "### 🔄 Changed\n\n- older\n\n## [0.1.0] - 2026-01-01\n\n### 🔄 Changed\n\n- released\n")
        charter_pin.changelog_entry("service-v0.2.0", COMMIT, "service-v0.1.0", "2026-11-18", path)
        text = path.read_text(encoding="utf-8")
        self.assertIn("updated: '2026-11-18'", text)
        unreleased = text.split("## [0.1.0]")[0]
        self.assertIn("### 🔄 Changed\n\n- **The packs are pinned to charter release `service-v0.2.0`**", unreleased)
        self.assertLess(unreleased.index("service-v0.2.0"), unreleased.index("- older"))
        self.assertIn(COMMIT, unreleased)
        self.assertEqual(text.split("## [0.1.0]")[1].count("service-v0.2.0"), 0)

    def test_a_missing_changed_heading_is_made_inside_unreleased(self) -> None:
        path = self.write("---\nupdated: '2026-01-01'\n---\n## [Unreleased]\n\n### ✨ Added\n\n- a\n\n## [0.1.0]\n")
        charter_pin.changelog_entry("service-v0.2.0", COMMIT, "", "2026-11-18", path)
        unreleased = path.read_text(encoding="utf-8").split("## [0.1.0]")[0]
        self.assertIn("### 🔄 Changed\n\n- **The packs are pinned", unreleased)

    def test_the_repository_changelog_takes_the_entry(self) -> None:
        path = self.write(charter_pin.CHANGELOG.read_text(encoding="utf-8"))
        charter_pin.changelog_entry("service-v0.2.0", COMMIT, "service-v0.1.0-rc.1", "2026-11-18", path)
        self.assertIn("service-v0.2.0", path.read_text(encoding="utf-8").split("\n## [")[1])


class CommitPayload(unittest.TestCase):
    def test_it_carries_every_changed_deleted_and_new_file(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        git = lambda *args: subprocess.run(["git", "-c", "commit.gpgsign=false", *args], cwd=tmp, check=True,  # noqa: E731
                                           capture_output=True, text=True).stdout.strip()
        git("init", "-q")
        (tmp / "keep.txt").write_text("a\n", encoding="utf-8")
        (tmp / "gone.txt").write_text("b\n", encoding="utf-8")
        git("add", ".")
        git("-c", "user.name=t", "-c", "user.email=t@example.invalid", "commit", "-qm", "base")
        head = git("rev-parse", "HEAD")
        (tmp / "keep.txt").write_text("changed\n", encoding="utf-8")
        (tmp / "gone.txt").unlink()
        (tmp / "new.txt").write_text("derived\n", encoding="utf-8")  # a manifest the re-derivation created
        with mock.patch.object(charter_pin, "ROOT", tmp):
            payload = charter_pin.commit_payload("charter/x", head, "headline", "body")
        self.assertEqual(payload["expectedHeadOid"], head)
        self.assertEqual(payload["fileChanges"]["deletions"], [{"path": "gone.txt"}])
        added = {entry["path"]: base64.b64decode(entry["contents"]) for entry in payload["fileChanges"]["additions"]}
        self.assertEqual(added, {"keep.txt": b"changed\n", "new.txt": b"derived\n"})
        git("reset", "-q", "--hard")
        git("clean", "-qfd")
        with mock.patch.object(charter_pin, "ROOT", tmp), self.assertRaises(charter_pin.PinError):
            charter_pin.commit_payload("charter/x", head, "headline", "body")


#: A stand-in ``java`` for ``java -jar <jar> remediate <pack>...``: records its argv and working directory in
#: $JAVA_LOG and answers each pack as rewritten, or exits $JAVA_EXIT with a refusal.
FAKE_JAVA = """#!/usr/bin/env python3
import json, os, sys
open(os.environ["JAVA_LOG"], "w").write(json.dumps({"argv": sys.argv[1:], "cwd": os.getcwd(),
                                                     "lc_all": os.environ.get("LC_ALL")}))
code = int(os.environ.get("JAVA_EXIT", "0"))
if code:
    print("packs/alpha: refused: pack.yaml: pack_version_invalid", file=sys.stderr)
    sys.exit(code)
for pack in sys.argv[4:]:
    print(f"{pack}: rewritten" if pack.endswith("alpha") else f"{pack}: unchanged", file=sys.stderr)
print("{}")
"""


class Rederive(unittest.TestCase):
    """#347: ``apply`` restamps every pack with the pinned jar's ``remediate``, not the schema pass's derivation."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        for pack in ("packs/alpha", "packs/beta", "tests/fixtures/valid/example"):
            (self.tmp / pack).mkdir(parents=True)
            (self.tmp / pack / "pack.yaml").write_text("pack_version: 1.0.0\n")
        (self.tmp / "packs" / "notes").mkdir()  # no pack.yaml: not a pack
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        (bin_dir / "java").write_text(FAKE_JAVA)
        (bin_dir / "java").chmod(0o755)
        self.log = self.tmp / "java.json"
        self.env = {"PATH": f"{bin_dir}:{os_environ()['PATH']}", "JAVA_LOG": str(self.log), "LC_ALL": "C"}
        self.ran: list[tuple[str, ...]] = []
        for patcher in (mock.patch.object(charter_pin, "ROOT", self.tmp),
                        mock.patch.object(charter_pin, "_run", side_effect=lambda *c: self.ran.append(c)),
                        mock.patch.dict("os.environ", self.env)):
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_remediate_runs_once_over_every_pack_from_the_root_under_a_utf8_locale(self) -> None:
        with redirect_stderr(io.StringIO()) as err:
            charter_pin.rederive("/jars/pack-doctor.jar")
        seen = json.loads(self.log.read_text())
        self.assertEqual(seen["argv"], ["-jar", "/jars/pack-doctor.jar", "remediate", "packs/alpha", "packs/beta",
                                        "tests/fixtures/valid/example"])
        self.assertEqual(Path(seen["cwd"]).resolve(), self.tmp.resolve())
        self.assertEqual(seen["lc_all"], "C.UTF-8")
        self.assertIn("packs/alpha: rewritten", err.getvalue())
        self.assertIn("packs/beta: unchanged", err.getvalue())
        # The schema pass no longer derives manifests: the digests and the pack pages follow remediate.
        self.assertEqual([c[1:] for c in self.ran], [("scripts/ci/pack_digest.py", "--update"),
                                                     ("scripts/docs/gen_pack_reference.py",)])
        self.assertFalse(any("validate_pack_schemas.py" in part for command in self.ran for part in command))

    def test_a_failing_remediate_fails_the_derive_and_prints_its_output(self) -> None:
        with mock.patch.dict("os.environ", {"JAVA_EXIT": "1"}), redirect_stderr(io.StringIO()) as err, \
             self.assertRaises(charter_pin.PinError) as raised:
            charter_pin.rederive("/jars/pack-doctor.jar")
        self.assertIn("remediate exited 1", str(raised.exception))
        self.assertIn("pack_version_invalid", err.getvalue())
        self.assertEqual(self.ran, [])  # nothing after a refused restamp

    def test_a_pack_without_an_outcome_line_fails_the_derive(self) -> None:
        (self.tmp / "bin" / "java").write_text(FAKE_JAVA.replace('f"{pack}: rewritten" if pack.endswith("alpha") else ', ""
                                                                 ).replace('f"{pack}: unchanged"', '"nothing"'))
        with redirect_stderr(io.StringIO()), self.assertRaises(charter_pin.PinError) as raised:
            charter_pin.rederive("/jars/pack-doctor.jar")
        self.assertIn("no outcome", str(raised.exception))


def os_environ() -> dict:
    import os
    return dict(os.environ)


class Cli(unittest.TestCase):
    def test_an_unresolvable_target_exits_2_with_an_annotation(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            self.assertEqual(charter_pin.main(["resolve-ref", "a;b"]), 2)
        self.assertIn("::error::charter_pin.py resolve-ref", err.getvalue())


if __name__ == "__main__":
    unittest.main()
