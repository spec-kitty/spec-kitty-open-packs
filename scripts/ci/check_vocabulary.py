#!/usr/bin/env python3
"""Vocabulary guard for pack content: retired names stay out of every pack.

Core (``spec-kitty/spec-kitty``) checks the same rules, but only after a pin bump,
over the synced ``packs/built-in`` and ``packs/internal`` trees
(spec-kitty/spec-kitty#6553). This script runs them here, on every pack, before a
change can reach a pin. Keep the rules in step with core's guards:

* retired doctrine ids -- ``tests/charter_offering/test_retired_ids_absent.py``;
* the renamed ``merge`` command's invocation phrase --
  ``tests/architectural/test_no_legacy_terminology.py`` (``_COMMAND_SURFACE_*``);
* the retired governing glossary surface --
  ``tests/architectural/test_transition_guard_shrink_only.py``.

Stdlib only. It scans the tracked text files under ``packs/``. Run it with::

    python3 scripts/ci/check_vocabulary.py

Exit code 0 when clean, 1 with one ``::error`` line per finding otherwise.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TEXT_SUFFIXES = frozenset({".py", ".yaml", ".yml", ".md", ".json", ".toml", ".txt", ".j2"})


def _any_identifier_form(stem: str) -> re.Pattern[str]:
    """Any use of *stem* as an identifier (not a substring of a longer id)."""
    return re.compile(rf"(?<![\w-]){re.escape(stem)}(?![\w-])")


def _tactic_forms_only(stem: str) -> re.Pattern[str]:
    """Only the tactic-shaped uses of *stem* (its twin id is live)."""
    s = re.escape(stem)
    return re.compile(
        rf"tactic:{s}(?![\w-])"
        rf"|(?<![\w-]){s}\.tactic\.yaml"
        rf"|type:\s*tactic\s*\n\s*(?:name:[^\n]*\n\s*)?id:\s*{s}\s*$",
        re.MULTILINE,
    )


#: Retired doctrine id -> its identifier pattern. ``locality-of-change`` and
#: ``boring-code-review`` count only in tactic form: the directive
#: ``024-locality-of-change`` and the styleguide ``boring-code-review`` are live.
RETIRED_IDS: dict[str, re.Pattern[str]] = {
    "adversarial-squad-cadence": _any_identifier_form("adversarial-squad-cadence"),
    "bug-fixing-checklist": _any_identifier_form("bug-fixing-checklist"),
    "common-docs-curation": _any_identifier_form("common-docs-curation"),
    "behavior-driven-development": _any_identifier_form("behavior-driven-development"),
    "iterative-deepening-review": _any_identifier_form("iterative-deepening-review"),
    "tracker-organisation-workflow": _any_identifier_form("tracker-organisation-workflow"),
    "locality-of-change": _tactic_forms_only("locality-of-change"),
    "boring-code-review": _tactic_forms_only("boring-code-review"),
    "adversarial-evidence-contract": _any_identifier_form("adversarial-evidence-contract"),
}

#: Two ids moved into the internal pack (``iterative-deepening-review`` renamed on
#: the move) and may be named there.
INTERNAL_PACK = "packs/internal/"
MOVED_TO_INTERNAL = frozenset({"iterative-deepening-review", "tracker-organisation-workflow"})

#: Prose that names a retired id *as retired*: (path, stem, exact phrase). The
#: phrase is stripped before scanning, so the file is still scanned for any other
#: mention of the stem, and a row whose phrase is gone is reported as stale.
PROVENANCE_PHRASES: tuple[tuple[str, str, str], ...] = (
    (
        "packs/built-in/procedures/test-first-bug-fixing.procedure.yaml",
        "bug-fixing-checklist",
        "the retired bug-fixing-checklist tactic",
    ),
    # Not in core, which never scans packs/qa: keep this row when syncing with core.
    (
        "packs/qa/PROVENANCE.md",
        "behavior-driven-development",
        "Its old reference, `behavior-driven-development`, was retired",
    ),
)

#: The lane-consolidation command was renamed to ``consolidate``; the old name only
#: reaches a migration-error stub. A real command name is never followed by ``-``
#: or a word character, so ``merge-driver-*`` and prose such as "merges" or
#: "merged" are not matched (spec-kitty/spec-kitty#6570). No baseline: zero today.
#: Identical to core's ``_COMMAND_SURFACE_PHRASE_PATTERN`` on purpose: a looser rule
#: here would pass content that core then fails after a pin bump.
RETIRED_COMMAND = re.compile(r"spec-kitty merge(?![\w-])", re.IGNORECASE)

#: The retired governing glossary surface (core #6553's zero-pin), built from
#: fragments so this file never carries the governing line itself. Stricter than
#: core's marker: a quoted value or a trailing comment is caught too.
_RETIRED_SURFACE_TOKEN = "doc" + "trine"
RETIRED_SURFACE = re.compile(rf"""^\s*(?:-\s*)?surface:\s*(["']?){_RETIRED_SURFACE_TOKEN}\1\s*(?:#.*)?$""")
GLOSSARY_PACK_SUFFIX = ".glossary-pack.yaml"


def _without_provenance(text: str, rel: str) -> str:
    """*text* with this file's provenance phrases blanked out, line breaks kept."""
    for path, _stem, phrase in PROVENANCE_PHRASES:
        if path == rel:
            text = text.replace(phrase, re.sub(r"[^\n]", " ", phrase))
    return text


def retired_ids_in(text: str, rel: str) -> list[str]:
    """Retired ids named in *text* of the file *rel*, after provenance and allowlist."""
    text = _without_provenance(text, rel)
    return [
        stem
        for stem, pattern in RETIRED_IDS.items()
        if pattern.search(text) and not (rel.startswith(INTERNAL_PACK) and stem in MOVED_TO_INTERNAL)
    ]


def _line_of(text: str, needle: re.Pattern[str]) -> int:
    match = needle.search(text)
    return text.count("\n", 0, match.start()) + 1 if match else 1


def findings_in(text: str, rel: str) -> list[tuple[int, str]]:
    """Every (line, message) finding for the file *rel* holding *text*.

    A retired id is reported once per file, at its first mention outside provenance.
    """
    found: list[tuple[int, str]] = []
    scanned = _without_provenance(text, rel)
    for stem in retired_ids_in(text, rel):
        found.append((_line_of(scanned, RETIRED_IDS[stem]), f"names the retired doctrine id '{stem}'"))
    for number, line in enumerate(text.splitlines(), start=1):
        if RETIRED_COMMAND.search(line):
            found.append((number, "names the renamed `merge` command; use `spec-kitty consolidate`"))
        if rel.endswith(GLOSSARY_PACK_SUFFIX) and RETIRED_SURFACE.match(line):
            found.append((number, "declares the retired governing glossary surface"))
    return found


def stale_provenance(texts: dict[str, str]) -> list[str]:
    """Provenance rows whose file or phrase is gone."""
    return [f"{rel}: provenance phrase {phrase!r} is gone; drop the row" for rel, _stem, phrase in PROVENANCE_PHRASES if phrase not in texts.get(rel, "")]


def tracked_pack_files(root: Path = ROOT) -> list[str]:
    """Tracked text files under ``packs/``; never empty."""
    out = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--", "packs"], check=True, capture_output=True).stdout
    files = sorted(p for p in out.decode("utf-8").split("\0") if p and Path(p).suffix in TEXT_SUFFIXES)
    if not files:
        raise SystemExit("::error::no tracked text files under packs/; the scan would be vacuous")
    return files


def main(root: Path = ROOT) -> int:
    texts = {rel: (root / rel).read_text(encoding="utf-8", errors="replace") for rel in tracked_pack_files(root)}
    errors = [f"::error file={rel},line={line}::{rel}:{line} {message}" for rel, text in texts.items() for line, message in findings_in(text, rel)]
    errors += [f"::error::{message}" for message in stale_provenance(texts)]
    for error in errors:
        print(error)
    print(f"vocabulary: {len(texts)} pack file(s) scanned, {len(errors)} finding(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
