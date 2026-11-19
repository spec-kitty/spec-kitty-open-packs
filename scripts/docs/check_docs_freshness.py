#!/usr/bin/env python3
"""Check the `updated:` date of authored docs pages (#297).

The project charter lists "docs freshness" among its fail-closed gates. This script has two modes.

``--base <rev>`` (the gate): every authored page under ``docs/`` that the change adds, modifies or
renames between ``<rev>`` and ``--head`` must carry an ``updated:`` date no older than the author
date of the last commit that touched it. It exits 1 on a stale or missing date. Only changed pages
are judged, so no baseline is needed and existing pages cannot flood it.

``--report`` (advisory): lists authored pages whose ``updated:`` is older than the threshold for
their tier, following writing's ``docs-freshness-sla`` styleguide (guides 90 days, ADRs 365 days,
anything else 180 days). Pages with ``doc_status`` ``durable``, ``superseded`` or ``deprecated`` are
exempt. It always exits 0.

An authored page is a Markdown file under ``docs/`` whose frontmatter has no ``generated:`` key.
``scripts/docs/gen_pack_reference.py`` marks every page it writes with that key, and the
generated-content drift gate covers those pages.

The author date (``git log --format=%as``), not the committer date, is compared: a rebase keeps the
author date, so rebasing a pull request onto a newer ``main`` does not make its pages stale. The
date is in the author's own timezone, the day they would write into ``updated:``.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

DOCS = "docs"

#: Staleness thresholds in days, by path prefix; the first match wins (docs-freshness-sla).
TIERS: tuple[tuple[str, int], ...] = (
    ("docs/guides/", 90),
    ("docs/architecture/adr/", 365),
    ("", 180),
)

#: A revision as this script accepts it: a commit SHA or a ref name such as HEAD or origin/main. It
#: cannot start with "-", so git never reads it as an option.
REVISION = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/~^]{0,199}")

#: doc_status values the staleness report never flags.
EXEMPT_STATUSES = frozenset({"durable", "superseded", "deprecated"})


@dataclass(frozen=True)
class Page:
    path: str
    frontmatter: dict | None

    @property
    def generated(self) -> bool:
        return bool(self.frontmatter) and "generated" in self.frontmatter

    @property
    def updated(self) -> dt.date | None:
        value = (self.frontmatter or {}).get("updated")
        if isinstance(value, dt.datetime):
            return value.date()
        if isinstance(value, dt.date):
            return value
        if isinstance(value, str):
            try:
                return dt.date.fromisoformat(value.strip())
            except ValueError:
                return None
        return None


def read_frontmatter(text: str) -> dict | None:
    """The YAML between a leading ``---`` line and the next one, or None when there is none."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            try:
                data = yaml.safe_load("\n".join(lines[1:index]))
            except yaml.YAMLError:
                return None
            return data if isinstance(data, dict) else None
    return None


def read_page(root: Path, path: str) -> Page:
    return Page(path, read_frontmatter((root / path).read_text(encoding="utf-8")))


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout


def resolve_commit(root: Path, rev: str) -> str:
    """The commit SHA a revision names. Refuses a value git could read as an option, so a revision
    given on the command line never reaches git as anything but a revision."""
    match = REVISION.fullmatch(rev or "")
    if match is None:
        raise ValueError(f"not a revision: {rev!r}")
    sha = git(root, "rev-parse", "--verify", "--quiet", "--end-of-options", f"{match.group(0)}^{{commit}}").strip()
    if len(sha) not in (40, 64) or any(c not in "0123456789abcdef" for c in sha):
        raise ValueError(f"not a commit: {rev!r}")
    return sha


def changed_pages(root: Path, base: str, head: str) -> list[str]:
    """Markdown files under docs/ added, copied, modified or renamed from the merge base of base and head."""
    out = git(root, "diff", "--name-only", "--diff-filter=ACMR", "--no-renames", f"{base}...{head}", "--", DOCS)
    return sorted(p for p in out.splitlines() if p.endswith(".md"))


def last_author_date(root: Path, head: str, path: str) -> dt.date:
    return dt.date.fromisoformat(git(root, "log", "-1", "--format=%as", head, "--", path).strip())


def check_changed(root: Path, base: str, head: str) -> list[str]:
    """One message per changed authored page whose updated: is missing or older than its last commit."""
    base, head = resolve_commit(root, base), resolve_commit(root, head)
    problems = []
    for path in changed_pages(root, base, head):
        page = read_page(root, path)
        if page.generated:
            continue
        committed = last_author_date(root, head, path)
        if page.updated is None:
            problems.append(f"{path}: no valid `updated:` date in the frontmatter (last commit {committed})")
        elif page.updated < committed:
            problems.append(f"{path}: `updated: '{page.updated}'` is older than its last commit ({committed})")
    return problems


def threshold(path: str) -> int:
    return next(days for prefix, days in TIERS if path.startswith(prefix))


def stale_pages(root: Path, today: dt.date) -> list[str]:
    """One line per authored page older than its tier's threshold, oldest first."""
    found = []
    for file in sorted((root / DOCS).rglob("*.md")):
        if file.is_symlink():
            continue
        path = file.relative_to(root).as_posix()
        page = read_page(root, path)
        if page.generated or str((page.frontmatter or {}).get("doc_status", "")) in EXEMPT_STATUSES:
            continue
        limit = threshold(path)
        if page.updated is None:
            found.append((dt.date.min, f"{path}: no valid `updated:` date"))
        elif (today - page.updated).days > limit:
            found.append((page.updated, f"{path}: updated {page.updated}, {(today - page.updated).days} days ago (threshold {limit})"))
    return [line for _, line in sorted(found)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--base", help="judge the pages changed since this revision's merge base with --head")
    mode.add_argument("--report", action="store_true", help="list pages past their staleness threshold (never fails)")
    parser.add_argument("--head", default="HEAD", help="the revision under review (default HEAD)")
    parser.add_argument("--today", type=dt.date.fromisoformat, default=None, help="the report's reference date (default today, UTC)")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args(argv)
    root = args.repo_root

    if args.report:
        today = args.today or dt.datetime.now(dt.timezone.utc).date()
        lines = stale_pages(root, today)
        print(f"{len(lines)} authored page(s) past their staleness threshold (advisory, as of {today}).")
        for line in lines:
            print(f"  {line}")
        return 0

    try:
        problems = check_changed(root, args.base, args.head)
    except (ValueError, subprocess.CalledProcessError) as error:
        print(f"Cannot resolve the revisions to compare: {error}")
        return 2
    if problems:
        print("Changed docs pages with a stale `updated:` date. Set it to the day you verified the page:")
        for line in problems:
            print(f"  {line}")
        return 1
    print("Every changed authored docs page carries a current `updated:` date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
