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

Two rules are this repository's own. The first (spec-kitty/spec-kitty-open-packs#202): an
``applies_to_languages`` entry names a language, never a runtime or platform family
such as ``jvm``. The charter matches the field as a free string with no family alias,
so a ``jvm`` tag silently filters the artifact out of a ``languages: [java]`` project.

The second (spec-kitty/spec-kitty-open-packs#233): pack prose never states how strictly a
directive binds ("advisory in v1", "this is advisory guidance", "binding charter content").
The level is the directive's ``enforcement:`` field, read as the pack-supplied default, and
the adopting charter decides the level that applies (core spec-kitty#5207)
(``docs/architecture/adr/2026-11-18-1-directive-enforcement-is-a-pack-supplied-default.md``;
``term:spec-kitty-core/enforcement-level``). The rule matches phrases, never single words, so
an npm *advisory* or a *mandatory* report field stays legal. It closes the explicit phrasings
that recurred (on ``main`` before #233 it hit 30 of the files the sweep changed); a claim made
with one bare word ("the mandatory output", "binding rules" in another shape) is left to
review, because those words have legitimate senses. A phrase wrapped across two lines counts.

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
        "packs/testing/procedures/test-first-bug-fixing.procedure.yaml",  # moved from built-in by #73
        "bug-fixing-checklist",
        "the retired bug-fixing-checklist tactic",
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
RETIRED_SURFACE = re.compile(rf"""^\s*(?:-\s*)?name:\s*(["']?){_RETIRED_SURFACE_TOKEN}\1\s*(?:#.*)?$""")
#: A glossary context file (charter ADR-0049); a term's surface form is its ``name``.
GLOSSARY_SUFFIX = ".glossary.yaml"

#: #233: phrasings that state a directive's own level, criticality or gate posture, in a
#: directive or in content that cites one. Phrases only; each was checked against the
#: other senses that stay legal (npm advisories and an ``advisory:`` key, dependency or
#: data *binding*, mandatory report fields, the glossary's enforcement tiers, runtime gates
#: such as analyze, format versions such as ``qa-traceability/v1``).
#: What follows a level word when it is not the level: "mandatory reading", "required by" (activation), "rules binding
#: at startup" (a framework's binding). Each pattern names the continuations it spares instead of demanding the end
#: of a clause, so "these rules are mandatory for every mission" stays a level claim (#304).
_NOT_THE_LEVEL = r"(?!\s+reading\b)"

SELF_BINDING: tuple[re.Pattern[str], ...] = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\badvisory\s+(?:in|at\s+the\s+[\w-]+\s+level\s+in)\s+(?:v|version\s*)\d",
        r"\b(?:this|the)\s+directive\s+is\s+(?:(?:strictly|purely|merely|only)\s+)?"
        r"(?:advisory|required(?!\s+by\b)|mandatory|binding|lenient|non-blocking)\b",
        r"\b(?:this|the)\s+(?:rule|guidance)\s+is\s+(?:advisory|mandatory|binding)\b" + _NOT_THE_LEVEL,
        r"\b(?:these|the|its|all)\s+(?:rules|directives)\s+are\s+(?:advisory|mandatory|binding|non-negotiable)\b"
        + _NOT_THE_LEVEL,
        r"\b(?:directive|rule)s?\s+(?:is|are)\s+(?:non-negotiable|a\s+hard\s+gate)\b",
        r"\bnon-negotiable\s+(?:rule|directive|policy)\b",
        r"\bthis\s+is\s+(?:advisory|not\s+a\s+recommendation)\b",
        r"\badvisory-only\s+(?:directive|rule|guidance|tactic|procedure|styleguide)s?\b",
        r"\bnot\s+a\s+runtime\s+gate\b",
        r"\bbinding\s+charter\s+content\b",
        r"\badvisory\s+posture\b",
        r"\benforcement\s+`(?:required|advisory|lenient-adherence)`",
        # Within one clause (no . ; :) and at most 120 characters apart; "rules binding at startup" is a framework's.
        r"\bmakes?\b[^.;:]{0,120}?\brules?\s+binding\b(?!\s+(?:at\s+startup|the|a|an)\b)",
        r"\brules?\s+that\s+\S+\s+makes?\s+binding\b",
        r"\bdirective'?s?\s+binding\s+rules?\b",
        # "is advisory context" states the level; "the advisory context menu" does not (#304).
        r"\b(?:is|as)\s+advisory\s+context\b",
        r"\bremains?\s+advisory\b",
        r"\bhard\s+validation\s+gate\b",
        r"\blenient-adherence\s+[a-z]",
        r"\.\s+advisory(?:\s+in\s+v\d)?:\s+[^.]*\b(?:gates?|transition)\b",
    )
)
_ENFORCEMENT_FIELD = re.compile(r"^\s*enforcement:")
_LEAD = re.compile(r"^\s*(?:[-#>]\s*)*")
#: A Markdown heading (unindented, so an indented YAML comment still continues a wrapped line).
_HEADING = re.compile(r"^#{1,6}\s")
#: A next line that is not a continuation: a heading, or (also inside a blockquote) a list item (- * + 1. 1)) or an
#: enforcement field. Judged on the raw line, before emphasis is stripped, so a ``*`` bullet is still a bullet.
_STARTS_SOMETHING_NEW = re.compile(r"^(?:#{1,6}\s|\s*(?:>\s*)*(?:(?:[-*+]|\d+[.)])\s|enforcement:))")
#: ``_`` or ``__`` used as emphasis around a word, not inside one (snake_case and __dunder__ inside words stay).
_EMPHASIS = re.compile(r"(?<![^\W_])_+(?=[^\W_])|(?<=[^\W_])_+(?![^\W_])")


def self_binding_in(text: str) -> list[tuple[int, str]]:
    """(line, phrase) for every line that states a directive's level in prose (#233).

    Pack YAML and Markdown wrap at about 80 columns, so a phrase may straddle a line break, and what follows a level
    word on the next line can decide whether it is the level ("mandatory" / "reading for reviewers"). Each line is
    therefore judged joined to the next one (#304, WP04 review); a phrase is reported on the line where it starts.
    Markdown emphasis (``*``, and ``_`` around a word) is ignored. A line is not joined to a blank line, a list item, a
    heading or an ``enforcement:`` field, and a heading is not joined to the next line: those start something new.
    """
    raw = text.splitlines()
    lines = [_EMPHASIS.sub("", line.replace("*", "")) for line in raw]
    found: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if _ENFORCEMENT_FIELD.match(line):
            continue
        head = line.rstrip()
        joined = head
        following = raw[index + 1] if index + 1 < len(raw) else ""
        if following and not _HEADING.match(raw[index]) and not _STARTS_SOMETHING_NEW.match(following):
            joined = f"{head} {_LEAD.sub('', lines[index + 1])}"
        for pattern in SELF_BINDING:
            match = pattern.search(joined)
            if match and match.start() < len(head):
                found.append((index + 1, " ".join(match.group(0).split())))
                break
    return found


#: Runtime and platform families that are not language names (#202). The charter
#: compares ``applies_to_languages`` entries as plain strings, so a family tag never
#: matches a project's ``languages``.
RUNTIME_FAMILIES = frozenset({"jvm", "dotnet", "clr", "beam", "node", "nodejs"})
_LANGUAGES_KEY = re.compile(r"^(?P<indent>[ \t]*)applies_to_languages:(?P<rest>.*)$")
_BLOCK_ITEM = re.compile(r"^\s*-\s*(?P<value>[^#\s]+)")


def _unquoted(value: str) -> str:
    return value.strip().strip("'\"").lower()


def family_languages_in(text: str) -> list[tuple[int, str]]:
    """(line, value) for every ``applies_to_languages`` entry that names a runtime family.

    Reads both the flow form (``[java, jvm]``) and the block form (``- jvm`` lines that
    follow the key, indented at least as deep). Prose that merely mentions ``jvm`` is
    not an entry and is not reported. Line-based by design (stdlib only): a flow list
    split over several lines, a quoted key or a key inside a list item is not read.
    No pack uses those forms.
    """
    found: list[tuple[int, str]] = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        key = _LANGUAGES_KEY.match(line)
        if not key:
            continue
        rest = key.group("rest").split("#", 1)[0].strip()
        if rest.startswith("["):
            for value in rest.strip("[]").split(","):
                if _unquoted(value) in RUNTIME_FAMILIES:
                    found.append((index + 1, _unquoted(value)))
            continue
        indent = len(key.group("indent"))
        for offset, item in enumerate(lines[index + 1 :], start=index + 2):
            if not item.strip() or item.lstrip().startswith("#"):
                continue
            match = _BLOCK_ITEM.match(item)
            if not match or len(item) - len(item.lstrip()) < indent:
                break
            if _unquoted(match.group("value")) in RUNTIME_FAMILIES:
                found.append((offset, _unquoted(match.group("value"))))
    return found


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
        if rel.endswith(GLOSSARY_SUFFIX) and RETIRED_SURFACE.match(line):
            found.append((number, "declares the retired governing glossary surface"))
    for number, phrase in self_binding_in(text):
        shown = phrase if len(phrase) <= 48 else f"{phrase[:45]}..."
        found.append((number, f"states a directive's level in prose ({shown!r}); set the enforcement field "
                              "instead (term:spec-kitty-core/enforcement-level)"))
    if rel.endswith((".yaml", ".yml")):
        for number, family in family_languages_in(text):
            found.append((number, f"applies_to_languages names the runtime family '{family}'; name the language (for example java, kotlin)"))
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
