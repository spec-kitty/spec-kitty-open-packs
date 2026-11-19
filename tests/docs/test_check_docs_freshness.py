"""The docs freshness gate (#297) fails a changed authored page with a stale `updated:`, and only that.

Each test builds a throwaway git repository with commits at fixed author dates, so the verdicts do not
depend on today's date or on this repository's history. Run with::

    python3 -m unittest discover -s tests/docs
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

_PATH = Path(__file__).resolve().parents[2] / "scripts" / "docs" / "check_docs_freshness.py"
_spec = importlib.util.spec_from_file_location("check_docs_freshness", _PATH)
assert _spec and _spec.loader
fresh = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = fresh
_spec.loader.exec_module(fresh)


def page(updated: str | None, extra: str = "") -> str:
    lines = ["---", "title: A page", "description: A page.", "doc_status: active"]
    if updated is not None:
        lines.append(f"updated: '{updated}'")
    lines.extend(extra.splitlines())
    return "\n".join([*lines, "---", "# A page", "", "Body.", ""])


class Repo:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.git("init", "-q", "-b", "main")

    def git(self, *args: str, date: str | None = None) -> str:
        env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
               "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"}
        if date:
            env["GIT_AUTHOR_DATE"] = f"{date}T12:00:00+00:00"
            # A committer date later than the author date, as after a rebase: the gate must read the author date.
            env["GIT_COMMITTER_DATE"] = "2030-01-01T12:00:00+00:00"
        result = subprocess.run(["git", "-c", "commit.gpgsign=false", *args], cwd=self.root, env=env,
                                check=True, capture_output=True, text=True)
        return result.stdout.strip()

    def commit(self, files: dict[str, str | None], date: str) -> str:
        for path, text in files.items():
            target = self.root / path
            if text is None:
                target.unlink()
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", f"change {date}", date=date)
        return self.git("rev-parse", "HEAD")


class ChangedPagesGate(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Repo(Path(self._tmp.name))
        self.base = self.repo.commit({
            "docs/guides/old.md": page("2026-01-01"),
            "docs/other.md": page("2026-01-01"),
        }, "2026-01-01")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def check(self) -> list[str]:
        return fresh.check_changed(self.repo.root, self.base, "HEAD")

    def test_a_changed_page_whose_date_moved_with_it_passes(self) -> None:
        self.repo.commit({"docs/guides/old.md": page("2026-03-02")}, "2026-03-02")
        self.assertEqual(self.check(), [])

    def test_a_changed_page_whose_date_did_not_move_fails(self) -> None:
        self.repo.commit({"docs/guides/old.md": page("2026-01-01") + "More.\n"}, "2026-03-02")
        problems = self.check()
        self.assertEqual(len(problems), 1)
        self.assertIn("docs/guides/old.md", problems[0])
        self.assertIn("2026-03-02", problems[0])

    def test_a_later_commit_to_the_same_page_needs_the_date_moved_again(self) -> None:
        self.repo.commit({"docs/guides/old.md": page("2026-03-02")}, "2026-03-02")
        self.repo.commit({"docs/guides/old.md": page("2026-03-02") + "Typo fix.\n"}, "2026-03-05")
        self.assertEqual(len(self.check()), 1)

    def test_a_new_page_without_a_date_fails(self) -> None:
        self.repo.commit({"docs/new.md": page(None)}, "2026-03-02")
        self.assertIn("no valid `updated:`", self.check()[0])

    def test_an_unchanged_stale_page_is_not_judged(self) -> None:
        # docs/other.md stays at 2026-01-01; only the changed page is gated, so no baseline is needed.
        self.repo.commit({"docs/guides/old.md": page("2026-03-02")}, "2026-03-02")
        self.assertEqual(self.check(), [])

    def test_a_generated_page_is_left_to_the_drift_gate(self) -> None:
        generated = page("2026-01-01", "generated:\n  by: scripts/docs/gen_pack_reference.py")
        self.repo.commit({"docs/packs/x.md": generated}, "2026-03-02")
        self.assertEqual(self.check(), [])

    def test_a_deleted_page_and_a_non_markdown_file_are_ignored(self) -> None:
        self.repo.commit({"docs/other.md": None, "docs/_meta/sections.yaml": "version: 1\n"}, "2026-03-02")
        self.assertEqual(self.check(), [])

    def test_main_advancing_after_the_branch_point_does_not_judge_mains_pages(self) -> None:
        self.repo.git("checkout", "-q", "-b", "topic")
        self.repo.commit({"docs/guides/old.md": page("2026-03-02")}, "2026-03-02")
        self.repo.git("checkout", "-q", "main")
        main_tip = self.repo.commit({"docs/other.md": page("2026-01-01") + "Stale on main.\n"}, "2026-03-03")
        self.repo.git("checkout", "-q", "topic")
        self.assertEqual(fresh.check_changed(self.repo.root, main_tip, "HEAD"), [])

    def test_a_non_ascii_page_name_is_judged(self) -> None:
        self.repo.commit({"docs/café.md": page("2026-01-01")}, "2026-03-02")
        self.assertEqual(len(self.check()), 1)

    def test_a_date_later_than_the_commit_fails(self) -> None:
        self.repo.commit({"docs/guides/old.md": page("2027-01-01")}, "2026-03-02")
        self.assertIn("later than", self.check()[0])

    def test_a_hyphenated_branch_name_resolves(self) -> None:
        self.repo.git("branch", "feat-x", self.base)
        self.assertEqual(fresh.check_changed(self.repo.root, "feat-x", "HEAD"), [])

    def test_a_revision_git_could_read_as_an_option_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            fresh.check_changed(self.repo.root, "--output=/tmp/x", "HEAD")
        with redirect_stdout(io.StringIO()):
            code = fresh.main(["--base=--all", "--repo-root", str(self.repo.root)])
        self.assertEqual(code, 2)

    def test_the_command_exits_one_on_a_stale_page(self) -> None:
        self.repo.commit({"docs/guides/old.md": page("2026-01-01") + "More.\n"}, "2026-03-02")
        with redirect_stdout(io.StringIO()):
            code = fresh.main(["--base", self.base, "--repo-root", str(self.repo.root)])
        self.assertEqual(code, 1)


class StalenessReport(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Repo(Path(self._tmp.name))
        self.repo.commit({
            "docs/guides/guide.md": page("2026-01-01"),                      # 100 days: past 90
            "docs/architecture/adr/adr.md": page("2026-01-01"),              # 100 days: within 365
            "docs/reference.md": page("2025-01-01"),                         # past 180
            "docs/durable.md": page("2020-01-01").replace("active", "durable"),
            "docs/packs/gen.md": page("2020-01-01", "generated:\n  by: x"),
        }, "2026-01-01")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_it_lists_pages_past_their_tier_oldest_first(self) -> None:
        lines = fresh.stale_pages(self.repo.root, dt.date(2026, 4, 11))
        self.assertEqual([line.split(":")[0] for line in lines], ["docs/reference.md", "docs/guides/guide.md"])

    def test_it_lists_a_future_date(self) -> None:
        self.repo.commit({"docs/future.md": page("2027-01-01")}, "2026-01-02")
        lines = fresh.stale_pages(self.repo.root, dt.date(2026, 1, 3))
        self.assertTrue(any("docs/future.md" in line and "future" in line for line in lines))

    def test_it_never_fails(self) -> None:
        with redirect_stdout(io.StringIO()):
            code = fresh.main(["--report", "--today", "2030-01-01", "--repo-root", str(self.repo.root)])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
