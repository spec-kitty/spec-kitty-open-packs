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
        lock = {"commit": COMMIT, "release_tag": current, "jar_sha256": DIGEST if current else ""}
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
        lock = {"commit": COMMIT, "release_tag": current, "jar_sha256": DIGEST if current else ""}
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
        charter_pin.write_lock(COMMIT, "service-v9.0.0-rc.1", DIGEST)
        self.assertEqual(charter_lock.read(self.lock),
                         {"commit": COMMIT, "release_tag": "service-v9.0.0-rc.1", "jar_sha256": DIGEST})
        charter_pin.write_lock(COMMIT, "", "")
        self.assertEqual(charter_lock.read(self.lock), {"commit": COMMIT, "release_tag": "", "jar_sha256": ""})
        kept = [line for line in self.lock.read_text(encoding="utf-8").splitlines() if line.startswith("#")]
        self.assertEqual(kept, comments)

    def test_a_malformed_pin_is_refused_and_the_file_is_left_alone(self) -> None:
        before = self.lock.read_text(encoding="utf-8")
        for commit, tag, digest in (("main", "", ""), (COMMIT, "v1.0.0", DIGEST), (COMMIT, "service-v1.0.0", ""),
                                    (COMMIT, "service-v1.0.0", "x" * 64)):
            with self.subTest(commit=commit, tag=tag, digest=digest), self.assertRaises(charter_pin.PinError):
                charter_pin.write_lock(commit, tag, digest)
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


class Cli(unittest.TestCase):
    def test_an_unresolvable_target_exits_2_with_an_annotation(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            self.assertEqual(charter_pin.main(["resolve-ref", "a;b"]), 2)
        self.assertIn("::error::charter_pin.py resolve-ref", err.getvalue())


if __name__ == "__main__":
    unittest.main()
