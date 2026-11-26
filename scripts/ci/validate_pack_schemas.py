#!/usr/bin/env python3
"""Validate Charter Pack files against the JSON Schemas of spec-kitty-charter.

The charter repository owns the pack shapes (``contracts/packs/schemas/*.schema.json``)
and says which file gets which schema (``contracts/packs/file-kinds.yaml``). This script
mirrors that mapping: it classifies every file of a pack by the ``files``, ``exclusions``,
``retired`` and ``payloads`` rules, then a root case variant of a ruled file (refused under that rule,
FR-022) and last the ``ignored`` fallback (Markdown nothing models, left out, not held), validates
YAML files against their schema, and reads
Markdown files (the pack document ``README.md``, guides, mission-step prompts, guidelines and prompt fragments) into the
charter's Markdown model ``{frontmatter?, title?, preamble, sections}`` before validating
that model against the rule's structure schema.

It fails closed. Exit status:

* 0  every pack is valid and every ``--expect-invalid`` pack has schema violations;
* 1  a schema violation or a retired-layout file in a pack, or an ``--expect-invalid``
     pack that came out clean;
* 2  the gate cannot judge: unloadable contract or schema, a file of a known kind with no
     schema mapping, a pack with zero files checked, or an unreadable file.

A pack's manifest is the charter's: pack-doctor judges its hashes (``manifest_stale``) and its membership
(``manifest_membership``), and ``pack-doctor remediate <pack>`` writes it (#347, #348). This script derives,
restamps and verifies no manifest; it only reports a declared graph node that a manifest does not list (#182), a
house rule: ``manifest_membership`` derives its lists from the files a pack holds, so it misses a node no file
declares. An unlisted file is ``manifest_membership``'s alone (decision 01M8BMA8).

Needs ``pyyaml`` and ``jsonschema`` (Draft 2020-12). The contract is fetched from the
pinned charter commit (``charter.lock.yaml``) unless ``--contract DIR`` (a directory holding
``file-kinds.yaml`` and ``schemas/``) or ``$CHARTER_CONTRACT_DIR`` is given.
"""

from __future__ import annotations

import argparse
import difflib
import functools
import json
import os
import re
import sys
import tempfile
import unicodedata
import urllib.request
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

sys.path.insert(0, str(Path(__file__).resolve().parent))
import charter_lock  # noqa: E402

CHARTER_REPOSITORY = "spec-kitty/spec-kitty-charter"
# The commit of spec-kitty-charter whose contracts/packs/ this repository validates against is the
# `commit` of charter.lock.yaml at the repository root, the one pin of every charter check (the
# charter service job reads the same file). Read by `charter_commit()`, which fails closed unless it is
# 40 lowercase hex characters; never a branch.
CONTRACT_PATH = "contracts/packs"
SCHEMA_NAME_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]*")

#: File-name tokens (``<id>.<token>.yaml``) of kinds the contract must map to a schema.
KNOWN_KIND_TOKENS = frozenset(
    {
        "directive", "tactic", "styleguide", "toolguide", "paradigm", "procedure",
        "agent", "asset", "glossary", "skill", "mission-type",
        "step-enhancement", "graph", "routing-catalog",
    }
)  # fmt: skip

EXIT_OK, EXIT_INVALID, EXIT_GATE = 0, 1, 2
#: Graph-node kinds a manifest does not list (#182 residual, #194). ``action`` is graph-only: no file backs it.
#: Mission types and templates are exempt here and judged by pack-doctor's ``manifest_membership`` instead. An
#: ``anti_pattern`` node is no longer exempt (#348 (f)). Of any other kind, a node no file of the pack declares must be
#: a constituent (``unlisted_nodes``); a node a file declares is pack-doctor's ``manifest_membership``. A new kind fails
#: closed until it is listed here.
MANIFEST_EXEMPT_NODE_KINDS = frozenset({"action", "template", "mission_type"})
#: The node kind of an artifact kind whose URN token differs from it (contracts/packs/file-kinds.yaml at the pin): a
#: glossary is the glossary context ``glossary_context:<id>`` (charter ADR-0053 decision 13). Any other artifact
#: kind is its own node kind.
NODE_KIND_BY_ARTIFACT_KIND = {"glossary": "glossary_context"}
#: The remedy a manifest finding names: the charter's own writer restamps and re-derives a pack's manifest (#347).
REMEDIATE_COMMAND = "pack-doctor remediate"


class GateError(Exception):
    """The validator cannot judge; the run must fail (exit 2)."""


def charter_commit() -> str:
    """The pinned charter commit, read from ``charter.lock.yaml``; a missing or malformed pin is a GateError."""
    try:
        return charter_lock.read()["commit"]
    except charter_lock.LockError as exc:
        raise GateError(f"charter.lock.yaml: {exc}") from exc


# --------------------------------------------------------------------------- contract


@dataclass(frozen=True)
class Rule:
    regex: re.Pattern[str]
    match: str
    schema: str | None = None
    content_form: str = "yaml"
    reason: str = ""


@dataclass
class Contract:
    files: list[Rule]
    exclusions: list[Rule]
    retired: list[Rule]
    payloads: list[Rule]
    #: The last-resort ``ignored`` rules (#451), matched case-insensitively; ``regex`` is the folded glob. Python's
    #: ``str.lower`` folds Unicode where Java's CASE_INSENSITIVE folds ASCII only; the pin's one rule (``**/*.md``) is
    #: ASCII, so the two cannot differ on it.
    ignored: list[Rule] = field(default_factory=list)
    validators: dict[str, Draft202012Validator] = field(default_factory=dict)


def glob_to_regex(glob: str) -> re.Pattern[str]:
    """``*`` within one segment, ``**/`` zero or more whole segments, the rest literal."""
    out, i = [], 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif glob[i] == "*":
            out.append("[^/]*")
            i += 1
        else:
            out.append(re.escape(glob[i]))
            i += 1
    return re.compile("".join(out) + r"\Z")


def _rules(table: dict[str, Any], section: str, *, folded: bool = False) -> list[Rule]:
    rules = []
    for entry in table.get(section) or []:
        rules.append(
            Rule(
                regex=glob_to_regex(entry["match"].lower() if folded else entry["match"]),
                match=entry["match"],
                schema=entry.get("schema"),
                content_form=entry.get("content_form", "yaml"),
                reason=str(entry.get("reason", "")).strip(),
            )
        )
    return rules


def load_contract(contract_dir: Path) -> Contract:
    """Read ``file-kinds.yaml`` and load every schema it names; fail closed on any gap."""
    table_path = contract_dir / "file-kinds.yaml"
    try:
        table = yaml.safe_load(table_path.read_text(encoding="utf-8"))
        contract = Contract(
            files=_rules(table, "files"),
            exclusions=_rules(table, "exclusions"),
            retired=_rules(table, "retired"),
            payloads=_rules(table, "payloads"),
            ignored=_rules(table, "ignored", folded=True),
        )
    except (OSError, yaml.YAMLError, KeyError, TypeError, AttributeError) as exc:
        raise GateError(f"cannot read {table_path}: {exc!r}") from exc
    if not contract.files:
        raise GateError(f"{table_path} has no `files` rules")
    for rule in contract.files:
        name = rule.schema
        if not name:
            raise GateError(f"files rule {rule.match!r} names no schema")
        if name in contract.validators:
            continue
        if not SCHEMA_NAME_PATTERN.fullmatch(name):
            raise GateError(f"files rule {rule.match!r} names an invalid schema {name!r}")
        schemas_dir = (contract_dir / "schemas").resolve()
        schema_path = (schemas_dir / f"{name}.schema.json").resolve()
        if schema_path.parent != schemas_dir:
            raise GateError(f"schema {name!r} resolves outside {schemas_dir}")
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # noqa: BLE001 - any failure to load a schema is a gate failure
            raise GateError(f"cannot load schema {schema_path}: {exc!r}") from exc
        contract.validators[name] = Draft202012Validator(schema)
    return contract


def fetch_contract(dest: Path) -> Path:
    """Download file-kinds.yaml and the schemas it names from the pinned charter commit."""
    base = f"https://raw.githubusercontent.com/{CHARTER_REPOSITORY}/{charter_commit()}/{CONTRACT_PATH}"
    headers = {}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"

    def get(relative: str) -> bytes:
        request = urllib.request.Request(f"{base}/{relative}", headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310 - fixed https URL
                return response.read()
        except OSError as exc:
            raise GateError(f"cannot fetch {base}/{relative}: {exc!r}") from exc

    (dest / "schemas").mkdir(parents=True, exist_ok=True)
    table_bytes = get("file-kinds.yaml")
    (dest / "file-kinds.yaml").write_bytes(table_bytes)
    try:
        names = {rule["schema"] for rule in yaml.safe_load(table_bytes)["files"]}
    except (yaml.YAMLError, KeyError, TypeError) as exc:
        raise GateError(f"fetched file-kinds.yaml is unreadable: {exc!r}") from exc
    for name in sorted(names):
        (dest / "schemas" / f"{name}.schema.json").write_bytes(get(f"schemas/{name}.schema.json"))
    return dest


_CONTRACT_CACHE: dict[str, Contract] = {}


def contract_for(contract_dir: Path | None) -> Contract:
    """The contract at ``contract_dir`` (or ``$CHARTER_CONTRACT_DIR``, else the pinned fetch)."""
    chosen = contract_dir or (Path(os.environ["CHARTER_CONTRACT_DIR"]) if os.environ.get("CHARTER_CONTRACT_DIR") else None)
    key = str(chosen or f"pinned:{charter_commit()}")
    if key not in _CONTRACT_CACHE:
        if chosen is None:
            with tempfile.TemporaryDirectory(prefix="charter-contract-") as scratch:
                _CONTRACT_CACHE[key] = load_contract(fetch_contract(Path(scratch)))
        else:
            _CONTRACT_CACHE[key] = load_contract(chosen)
    return _CONTRACT_CACHE[key]


# --------------------------------------------------------------------------- YAML


class YamlRefused(yaml.YAMLError):
    """A document the charter's reader (ParsedYaml) refuses for a guard, not for a syntax error."""


class _Loader(yaml.SafeLoader):
    """Safe loader that keeps timestamps as strings, as JSON Schema sees them, and refuses duplicate keys.

    The charter loads with ``setAllowDuplicateKeys(false)`` (Yaml.java); PyYAML keeps the last value.
    """

    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
        self.flatten_mapping(node)
        seen: set[Any] = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=True)
            try:
                duplicate = key in seen
                seen.add(key)
            except TypeError:  # unhashable key: the base class reports it
                break
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark, f"found duplicate key {key!r}", key_node.start_mark
                )
        return super().construct_mapping(node, deep=deep)


_Loader.yaml_implicit_resolvers = {
    key: [(tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

#: The guards of the charter's ParsedYaml: collections nested at most this deep, and a document that
#: expands (a shared, aliased node counted each time it is reached) to at most this many nodes.
MAX_DEPTH = 200
MAX_NODES = 100_000


def _nested_too_deeply(text: str) -> bool:
    """Whether the parser's events nest collections deeper than MAX_DEPTH; the event stream is not recursive."""
    depth = 0
    try:
        for event in yaml.parse(text, Loader=_Loader):
            if isinstance(event, yaml.CollectionStartEvent):
                depth += 1
                if depth > MAX_DEPTH:
                    return True
            elif isinstance(event, yaml.CollectionEndEvent):
                depth -= 1
    except yaml.YAMLError:
        return False  # the loader reports a syntax error in the parser's own words
    return False


def _problem(value: Any, depth: int, path: set[int], nodes: list[int]) -> str | None:
    """The first reason a loaded document cannot be validated (ParsedYaml.problem), or ``None``."""
    nodes[0] += 1
    if nodes[0] > MAX_NODES:
        return "the document is too large"
    if not isinstance(value, (dict, list)):
        plain = value is None or isinstance(value, (str, int, float, bool))
        return None if plain else "a value is not a string, a number, a boolean or null"
    if depth >= MAX_DEPTH:
        return "the document is nested too deeply"
    if id(value) in path:
        return "the document contains itself"
    path.add(id(value))
    try:
        if isinstance(value, dict):
            if not all(isinstance(key, str) for key in value):
                return "a mapping key is not a string"
            children: Any = value.values()
        else:
            children = value
        for child in children:
            if (problem := _problem(child, depth + 1, path, nodes)) is not None:
                return problem
        return None
    finally:
        path.discard(id(value))


def load_yaml(text: str) -> Any:
    """Load one YAML document through the charter's guards; raises ``yaml.YAMLError`` when it is refused."""
    if _nested_too_deeply(text):
        raise YamlRefused("the document is nested too deeply")
    document = yaml.load(text, Loader=_Loader)  # noqa: S506 - SafeLoader subclass
    if (problem := _problem(document, 0, set(), [0])) is not None:
        raise YamlRefused(problem)
    return document


# --------------------------------------------------------------------------- manifest

MANIFEST_NAME = "pack-manifest.yaml"


# House rule (not a charter rule): the #182 residual, kept by decision 01M8BMA8. Pack-doctor's manifest_membership
# compares a manifest's lists with those derived from the files the pack holds, so it does not catch a graph node
# that no file declares (RealPackDoctor pins that the jar accepts one). Only such a node is named here: an unlisted
# file, or the node of a file, is manifest_membership's alone (the Python unlisted_constituents, a strict subset of
# it, is retired).
def unlisted_nodes(
    manifest: dict[str, Any], nodes: set[tuple[str, str]], file_backed: set[tuple[str, str]] | frozenset = frozenset()
) -> list[str]:
    """The declared graph nodes of a pack that no file of the pack declares (``file_backed``: the ``(kind, id)`` its
    files hold) and that its manifest does not list as constituents (#182 residual), sorted ``kind:id``; nodes of an
    exempt kind (``MANIFEST_EXEMPT_NODE_KINDS``) are not held to it."""
    listed = {
        (NODE_KIND_BY_ARTIFACT_KIND.get(entry.get("kind"), entry.get("kind")), entry.get("id"))
        for entry in manifest.get("constituents") or []
        if isinstance(entry, dict)
    }
    return sorted(
        f"{kind}:{node_id}"
        for kind, node_id in nodes
        if kind not in MANIFEST_EXEMPT_NODE_KINDS and (kind, node_id) not in listed | file_backed
    )


# --------------------------------------------------------------------------- Markdown model

# The scanner's patterns are matched whole (Java Matcher.matches). Java's `.` stops at \n, \r, U+0085,
# U+2028 and U+2029, Python's only at \n, so the class spells Java's out.
_SETEXT = re.compile(r" {0,3}(?:=+|-+)[ \t]*")
_CLOSING = re.compile(r"(?:#+|[^\n\r\x85\u2028\u2029]*[ \t]#+)")
_NOT_WHITESPACE = frozenset("\u00a0\u2007\u202f")  # no-break spaces: Zs, but not Java whitespace


def _java_whitespace(char: str) -> bool:
    """Java's Character.isWhitespace, which String.isBlank and strip use (not Python's str.isspace)."""
    if char in "\t\n\x0b\x0c\r\x1c\x1d\x1e\x1f":
        return True
    return char not in _NOT_WHITESPACE and unicodedata.category(char) in {"Zs", "Zl", "Zp"}


def _blank(text: str) -> bool:
    return all(map(_java_whitespace, text))


def _strip(text: str) -> str:
    start, end = 0, len(text)
    while start < end and _java_whitespace(text[start]):
        start += 1
    while end > start and _java_whitespace(text[end - 1]):
        end -= 1
    return text[start:end]


class MarkdownRefused(Exception):
    def __init__(self, line: int, reason: str) -> None:
        super().__init__(f"line {line}: {reason}")


def _spaces(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _run(text: str, char: str) -> int:
    return len(text) - len(text.lstrip(char)) if text.startswith(char) else 0


def _fence_opener(line: str) -> tuple[str, int] | None:
    rest = line[_spaces(line):]
    if not rest or rest[0] not in "`~":
        return None
    marker, length = rest[0], _run(rest, rest[0])
    if length < 3 or (marker == "`" and "`" in rest[length:]):
        return None
    return marker, length


def _heading(text: str, number: int) -> tuple[int, str] | None:
    indent = _spaces(text)
    if indent > 3:
        return None
    rest = text[indent:]
    level = _run(rest, "#")
    if level == 0 or level > 6:
        return None
    after = rest[level:]
    if after and after[0] not in " \t":
        return None
    if level > 2:
        return None
    name = "an H1" if level == 1 else "an H2"
    if indent:
        raise MarkdownRefused(number, f"{name} indented by {indent} spaces is ambiguous; start it at column 0")
    if _blank(after):
        raise MarkdownRefused(number, "an empty heading is ambiguous")
    if after[0] == "\t":
        raise MarkdownRefused(number, f"{name} separated from its text by a tab is ambiguous")
    title = _strip(after)
    if _CLOSING.fullmatch(title):
        raise MarkdownRefused(number, f"{name} with a closing # sequence is ambiguous")
    return level, title


def _thematic_break(text: str) -> bool:
    indent = _spaces(text)
    if indent > 3 or indent == len(text) or text[indent] not in "-*_":
        return False
    marker, count = text[indent], 0
    for char in text[indent:]:
        if char == marker:
            count += 1
        elif char not in " \t":
            return False
    return count >= 3


def _deeper_heading(text: str) -> bool:
    if _spaces(text) > 3:
        return False
    rest = text[_spaces(text):]
    level = _run(rest, "#")
    return 2 < level <= 6 and (len(rest) == level or rest[level] in " \t")


def _trimmed(lines: list[str]) -> str:
    start, end = 0, len(lines)
    while start < end and _blank(lines[start]):
        start += 1
    while end > start and _blank(lines[end - 1]):
        end -= 1
    return "\n".join(lines[start:end])


def parse_markdown(text: str) -> dict[str, Any]:
    """Read Markdown into the charter's model (MarkdownCodec): refuses what the codec refuses."""
    if not text:
        return {"preamble": "", "sections": []}
    if text[0] == "﻿":
        raise MarkdownRefused(1, "a byte order mark is not admitted")
    if "\r" in text:
        raise MarkdownRefused(text[: text.index("\r")].count("\n") + 1, "a carriage return is not admitted")
    lines = text.split("\n")
    if text.endswith("\n"):
        lines.pop()
    model: dict[str, Any] = {}
    start = 0
    if lines[0] == "---":
        try:
            end = lines.index("---", 1)
        except ValueError:
            raise MarkdownRefused(1, "unterminated frontmatter: no closing --- line") from None
        raw = "\n".join(lines[1:end])
        try:
            front = {} if _blank(raw) else load_yaml(raw + "\n")
        except yaml.YAMLError as exc:
            raise MarkdownRefused(1, f"frontmatter is not valid YAML: {exc}") from exc
        if not isinstance(front, dict) or not all(isinstance(key, str) for key in front):
            raise MarkdownRefused(1, "frontmatter must be a YAML mapping with string keys")
        model["frontmatter"] = front
        start = end + 1

    preamble: list[str] = []
    current = preamble
    titles: list[str] = []
    bodies: list[list[str]] = []
    title_line, any_block = 0, False
    fence: tuple[str, int, int] | None = None
    under_paragraph = False
    for offset, line in enumerate(lines[start:]):
        number = start + offset + 1
        if fence:
            stripped = line[_spaces(line):]
            if _run(stripped, fence[0]) >= fence[1] and not stripped[_run(stripped, fence[0]):].strip(" "):
                fence = None
            current.append(line)
            under_paragraph = False
            continue
        opened = _fence_opener(line)
        if opened:
            fence = (*opened, number)
            current.append(line)
            any_block = True
            under_paragraph = False
            continue
        if _blank(line):
            current.append(line)
            under_paragraph = False
            continue
        heading = _heading(line, number)
        if heading:
            level, title = heading
            under_paragraph = False
            if level == 1:
                if "title" in model:
                    raise MarkdownRefused(number, f"a second H1 (the first is at line {title_line})")
                if any_block:
                    raise MarkdownRefused(number, "an H1 that is not the first block")
                model["title"], title_line = title, number
            else:
                current = []
                titles.append(title)
                bodies.append(current)
            any_block = True
            continue
        if under_paragraph and _SETEXT.fullmatch(line):
            raise MarkdownRefused(number, "a setext heading underline is ambiguous; use an ATX heading or a blank line")
        current.append(line)
        any_block = True
        under_paragraph = not _thematic_break(line) and not _deeper_heading(line)
    if fence:
        raise MarkdownRefused(fence[2], f"unclosed fence opened at line {fence[2]}")
    model["preamble"] = _trimmed(preamble)
    model["sections"] = [{"title": t, "content": _trimmed(b)} for t, b in zip(titles, bodies, strict=True)]
    return model


# --------------------------------------------------------------------------- prompt slots and fragments (ADR-0066)

SLOT_ID = re.compile(r"[a-z][a-z0-9-]*:[a-z][a-z0-9-]*")
_HTML_COMMENT = re.compile(r"<!--(.*?)-->", re.DOTALL)
_SLOT_COMMENT = re.compile(r"\s*(\S+):(start|end)\s*")
_SLOT_LIKE = re.compile(r":(?:start|end)\b")


def _prompt_slot_problem(line: int, detail: str, code: str = "prompt_slot_malformed") -> str:
    return f"{code} at line {line}: {detail}"


def prompt_slot_violations(text: str, *, require_empty: bool) -> list[str]:
    """The declaration checks of ADR-0066 decisions 2 and 8 for one base prompt.

    All prompts get the well-formedness checks. Only a descriptor at schema_version 1.0
    switches on ``prompt_slot_not_empty``; an unversioned descriptor keeps the legacy
    gate-marker behavior without a shim.
    """
    problems: list[str] = []
    declared: set[str] = set()
    open_slots: list[tuple[str, int, int]] = []
    for comment in _HTML_COMMENT.finditer(text):
        body = comment.group(1)
        match = _SLOT_COMMENT.fullmatch(body)
        line = text.count("\n", 0, comment.start()) + 1
        if match is None:
            if _SLOT_LIKE.search(body):
                problems.append(_prompt_slot_problem(line, f"malformed slot marker {comment.group(0)!r}"))
            continue
        slot_id, marker = match.groups()
        if SLOT_ID.fullmatch(slot_id) is None:
            problems.append(_prompt_slot_problem(line, f"invalid slot id {slot_id!r}"))
            continue
        if marker == "start":
            if slot_id in declared:
                problems.append(_prompt_slot_problem(line, f"slot {slot_id!r} is declared more than once"))
            declared.add(slot_id)
            if open_slots:
                problems.append(_prompt_slot_problem(line, f"slot {slot_id!r} nests inside {open_slots[-1][0]!r}"))
            open_slots.append((slot_id, line, comment.end()))
            continue
        if not open_slots:
            problems.append(_prompt_slot_problem(line, f"slot {slot_id!r} ends before it starts"))
            continue
        open_id, start_line, content_start = open_slots.pop()
        if open_id != slot_id:
            problems.append(_prompt_slot_problem(line, f"slot {slot_id!r} closes open slot {open_id!r} from line {start_line}"))
            continue
        if require_empty and text[content_start:comment.start()].strip():
            problems.append(_prompt_slot_problem(start_line, f"slot {slot_id!r} must contain only whitespace", "prompt_slot_not_empty"))
    for slot_id, line, _ in open_slots:
        problems.append(_prompt_slot_problem(line, f"slot {slot_id!r} has no end marker"))
    return problems


def declared_prompt_slots(text: str) -> set[str]:
    """Ids whose well-formed start marker occurs in a base prompt (compose-time use)."""
    slots = set()
    for comment in _HTML_COMMENT.finditer(text):
        match = _SLOT_COMMENT.fullmatch(comment.group(1))
        if match is not None and match.group(2) == "start" and SLOT_ID.fullmatch(match.group(1)):
            slots.add(match.group(1))
    return slots


def prompt_fragment_violations(text: str) -> list[str]:
    """Refuse slot markers in raw fragment Markdown, which its structure schema cannot see."""
    problems = []
    for comment in _HTML_COMMENT.finditer(text):
        if _SLOT_LIKE.search(comment.group(1)):
            line = text.count("\n", 0, comment.start()) + 1
            problems.append(f"prompt_fragment_invalid at line {line}: a fragment cannot declare or fill a slot")
    return problems


# --------------------------------------------------------------------------- validation


@dataclass
class PackReport:
    pack: str
    checked: int = 0
    skipped: int = 0
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    #: (pack-relative path, title, message) of R38 lint findings: a stray file that looks like a misspelled companion,
    #: or an artifact naming a companion the pack lacks. Annotations only, never a failure.
    suspects: list[tuple[str, str, str]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.violations


def _short(message: str, limit: int = 300) -> str:
    return message if len(message) <= limit else message[: limit - 3] + "..."


@functools.lru_cache(maxsize=None)
def _folded_regex(glob: str) -> re.Pattern[str]:
    """``glob`` in lower case, compiled once: matched against a path folded the same way."""
    return glob_to_regex(glob.lower())


def _exact(contract: Contract, relative: str, *, folded: bool = False) -> tuple[str, Rule | None]:
    """``files``, ``exclusions``, ``retired``, then ``payloads``: the first rule that matches, as written or folded;
    except that a ``retired`` rule beats a ``files`` rule that also matches, unless an ``exclusions`` rule matches too
    (the contract's classifier-cases rule 1: ``core/mission_step_contract.graph.yaml`` is retired, not a graph shard)."""
    path = relative.lower() if folded else relative

    def first(rules: list[Rule]) -> Rule | None:
        return next((rule for rule in rules if (_folded_regex(rule.match) if folded else rule.regex).match(path)), None)

    file_rule, excluded, retired = first(contract.files), first(contract.exclusions), first(contract.retired)
    if retired is not None and excluded is None:
        return "retired", retired
    for kind, rule in (("file", file_rule), ("excluded", excluded), ("retired", retired),
                       ("payload", first(contract.payloads))):
        if rule is not None:
            return kind, rule
    return "unmodelled", None


ROOT_FILE = re.compile(r"\*/([^*/]+)")


def kind_mapped(contract: Contract, token: str) -> bool:
    """Whether a ``files`` rule of the contract maps ``<id>.<token>.yaml`` files anywhere.

    A known kind no rule maps means the contract lost a mapping the mirror expects: the gate cannot judge. A file of a
    mapped kind that its rule does not reach (charter #554: a ``*.graph.yaml`` below the pack root, where only root
    shards are read; a ``step-enhancement`` outside ``missions/*/enhancements/``) is merely ``unmodelled`` (a warning).

    Any ``files`` rule ending in ``.<token>.yaml`` counts, however narrow: a contract that kept only a narrow one
    reports the files it no longer reaches as ``unmodelled`` warnings instead of "cannot judge"."""
    return any(rule.match.endswith(f".{token}.yaml") for rule in contract.files)


# Kept, not retired with the rules pack-doctor judges (#348 comment 3): the schema pass needs it to pick each file's
# schema, and the kept house rules read through it: unlisted_nodes (via held_artifacts), the agent-profile reference
# rules (via held_artifacts and profile_references), and charter_service_check.py's file_not_held policy.
def classify(contract: Contract, relative: str) -> tuple[str, Rule | None]:
    """The charter's classification of a path relative to the directory holding the packs.

    As ``PackFileKind.classify`` does at the pin: the exact rules first; then a root file that differs only in
    letter case from a root-anchored ``files`` or ``retired`` rule's file (``Readme.md``, ``PROVENANCE.MD``),
    refused as ``retired`` under that rule (FR-022); then the first ``ignored`` rule, matched case-insensitively,
    unless a ``files``, ``retired`` or ``payloads`` rule takes the path in another letter case (``a.guide.MD``).
    What is left is ``unmodelled``: the charter refuses it at registration (up to charter #554) or leaves it out
    with a ``file_not_held`` warning (since); this repository warns it the same way (#309)."""
    kind, rule = _exact(contract, relative)
    if kind != "unmodelled":
        return kind, rule
    folded = relative.lower()
    for candidate in (*contract.files, *contract.retired):
        root = ROOT_FILE.fullmatch(candidate.match)
        if root and _folded_regex(candidate.match).match(folded):
            return "retired", Rule(candidate.regex, candidate.match, reason=f"differs only in letter case from '{root.group(1)}'")
    if _exact(contract, relative, folded=True)[0] in ("unmodelled", "excluded"):
        for candidate in contract.ignored:
            if candidate.regex.match(folded):
                return "ignored", candidate
    return "unmodelled", None


#: The one policy for files the charter leaves out of a pack without refusing them (``file_not_held``, #451).
#: A file an ``exclusions`` rule names is left out by the contract's own decision, and passes. A file only the
#: ``ignored`` fallback takes passes silently when it matches one of these globs: orientation notes, a ``README.md`` at
#: any depth (the root one is the pack document and is held). Any other (a note, a misplaced guide, prompt or skill
#: body, which nothing serves) is warned as ``file_not_held``: operator ruling R34 (#331) lets authors keep notes and
#: logs in a pack, so a stray file never fails. A skill body its skill's ``body_path`` names is held as a companion
#: (``companion_claims``), so it never reaches the fallback. Globs match like the contract's, case-sensitively.
NOT_HELD_ALLOWANCES = tuple(glob_to_regex(glob) for glob in ("**/README.md",))
#: A fixture's own file, never pack content (``tests/fixtures/invalid/*/expected-code``).
FIXTURE_FILES = frozenset({"expected-code"})


#: Skill bodies are companions by ``body_path``, not by a ``files`` rule, but conventionally end in ``.skill.md``.
BODY_COMPANION_TOKENS = frozenset({"skill"})
COMPANION_RULE = re.compile(r"\*\.([a-z][a-z0-9-]*)\.md$")
#: How close a misnamed suffix, or a stray file's name, must be to count as a probable misspelling (R38).
MAX_SUFFIX_DISTANCE = 2
#: A companion token this long takes MAX_SUFFIX_DISTANCE edits; a shorter one one edit; SHORT_TOKEN or shorter no substitution.
LONG_TOKEN = 10
SHORT_TOKEN = 5
MIN_NAME_SIMILARITY = 0.8


def companion_tokens(contract: Contract) -> set[str]:
    """The ``<token>`` of every companion suffix ``*.<token>.md`` the contract's ``files`` rules model, plus ``skill``."""
    return {m.group(1) for rule in contract.files if (m := COMPANION_RULE.search(rule.match))} | BODY_COMPANION_TOKENS


def _distance(a: str, b: str) -> int:
    """The optimal-string-alignment edit distance: insertions, deletions, substitutions, adjacent transpositions."""
    rows = [list(range(len(b) + 1))]
    for i, ca in enumerate(a, start=1):
        row = [i]
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            value = min(rows[-1][j] + 1, row[j - 1] + 1, rows[-1][j - 1] + cost)
            if i > 1 and j > 1 and ca == b[j - 2] and a[i - 2] == cb:
                value = min(value, rows[-2][j - 2] + 1)
            row.append(value)
        rows.append(row)
    return rows[-1][-1]


def suffix_suggestion(name: str, tokens: set[str]) -> str | None:
    """The companion name ``name`` was probably meant to have, or None.

    ``<stem>.<token>.<ext>`` is a suspect when ``<ext>`` is ``md`` in any letter case and ``<token>`` is within
    ``MAX_SUFFIX_DISTANCE`` edits (case-insensitively) of a companion token, without already being exactly that
    token with a lowercase ``md``. A name with fewer than three dotted parts is never a suspect."""
    parts = name.split(".")
    if len(parts) < 3 or parts[-1].lower() != "md" or not parts[0]:
        return None
    token = parts[-2]
    lowered = token.lower()
    best = min(sorted(tokens), key=lambda t: _distance(lowered, t))
    distance = _distance(lowered, best)
    # Short tokens are close to ordinary words (slide, suite, still): one edit at most, and for five letters or fewer
    # no plain substitution (a same-length change that is not a transposition). Longer tokens allow two edits.
    allowed = MAX_SUFFIX_DISTANCE if len(best) >= LONG_TOKEN else 1
    if distance > allowed:
        return None
    if distance and len(best) <= SHORT_TOKEN and len(lowered) == len(best) and sorted(lowered) != sorted(best):
        return None
    if token == best and parts[-1] == "md":
        return None
    return ".".join([*parts[:-2], best, "md"])


def missing_references(pack_dir: Path, contract: Contract) -> dict[str, tuple[str, str]]:
    """Every companion a held YAML artifact names in a ``*_path`` key (relative to the artifact, or to the pack root as
    a DRG fragment node's ``body_path`` is) that the pack lacks,
    as ``{pack-relative path: (artifact, key)}``. A path that leaves the pack is not a companion and is skipped."""
    root = pack_dir.resolve()
    missing: dict[str, tuple[str, str]] = {}

    def walk(node: Any, artifact: Path, relative: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(key, str) and key.endswith("_path") and isinstance(value, str) and value:
                    try:  # an overlong name, a NUL byte or a symlink loop: not judged by this lint, never fatal
                        # Relative to the artifact (a skill's body_path, a step's prompt_path), or to the pack root
                        # (a DRG fragment node's body_path): missing only when neither holds it.
                        target = (artifact.parent / value).resolve()
                        if target.is_relative_to(root) and not target.exists() and not (root / value).exists():
                            missing.setdefault(target.relative_to(root).as_posix(), (relative, key))
                    except (OSError, ValueError, RuntimeError):
                        continue
                else:
                    walk(value, artifact, relative)
        elif isinstance(node, list):
            for item in node:
                walk(item, artifact, relative)

    for path in sorted(pack_dir.rglob("*.yaml")):
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(pack_dir).as_posix()
        kind, rule = classify(contract, f"{pack_dir.name}/{relative}")
        if kind == "file" and rule is not None and rule.schema:
            walk(_load_or_none(path), path, relative)
    return missing


MISSPELLED = "Possible misspelled companion"
MISSING = "Missing companion"


def misspelled_companions(pack_dir: Path, contract: Contract, stray: list[str]) -> list[tuple[str, str, str]]:
    """The R38 lint findings of one pack, as (pack-relative path, title, message).

    Every artifact that names a companion the pack lacks is annotated, which also covers a stem typo that still
    matches a ``files`` rule (``implemnet.prompt.md``). A stray file beside such a missing companion, with a similar
    name, is annotated as its probable misspelling; else a stray file whose suffix is close to a companion suffix.
    Annotations only: R34 keeps every stray file a warning, and pack-doctor refuses a missing companion."""
    missing = missing_references(pack_dir, contract)
    tokens = companion_tokens(contract)
    found = [(artifact, MISSING, f"{artifact} names {meant} as {key}, and no such file exists; pack-doctor refuses the "
                                 "pack with '<ref>: missing'.")
             for meant, (artifact, key) in sorted(missing.items())]
    for inside in stray:
        parent, _, name = inside.rpartition("/")
        near = [(difflib.SequenceMatcher(None, name.lower(), m.rpartition("/")[2].lower()).ratio(), m)
                for m in missing if m.rpartition("/")[0] == parent]
        near = [(ratio, m) for ratio, m in near if ratio >= MIN_NAME_SIMILARITY]
        if near:
            _, meant = max(near)
            artifact, key = missing[meant]
            found.append((inside, MISSPELLED, f"{inside} is not held; did you mean {meant}? {artifact} names it as "
                                              f"{key}, and no such file exists: rename the file or fix {key}."))
            continue
        suggestion = suffix_suggestion(name, tokens)
        if suggestion:
            meant = f"{parent}/{suggestion}" if parent else suggestion
            found.append((inside, MISSPELLED, f"{inside} is not held; did you mean {meant}? Its suffix is close to a "
                                              "companion the charter models; a misnamed companion is not served."))
    return found


def is_invalid_fixture(pack_dir: Path) -> bool:
    """Whether ``pack_dir`` is an invalid fixture (``…/fixtures/invalid/<name>``), whose ``expected-code`` is its own."""
    parent = pack_dir.resolve().parent
    return parent.name == "invalid" and parent.parent.name == "fixtures"


def not_held_allowed(relative: str) -> bool:
    """Whether ``relative`` (``<pack>/<path>``), which only the ``ignored`` fallback takes, may be carried unheld."""
    return any(allowed.match(relative) for allowed in NOT_HELD_ALLOWANCES)


def companion_claims(pack_dir: Path, contract: Contract) -> set[str]:
    """The pack-relative files a skill claims as its body (``body_path``, relative to the skill file).

    The charter removes companion files before it classifies the rest (``WholePackStore``), so a claimed body is held
    whatever its name or suffix and never falls to ``ignored`` or ``unmodelled``. A path that leaves the pack claims
    nothing."""
    claims: set[str] = set()
    root = pack_dir.resolve()
    for path in sorted(pack_dir.rglob("*.yaml")):
        if path.is_symlink() or not path.is_file():
            continue
        _, rule = classify(contract, f"{pack_dir.name}/{path.relative_to(pack_dir).as_posix()}")
        if rule is None or rule.schema != "skill":
            continue
        document = _load_or_none(path)
        body = document.get("body_path") if isinstance(document, dict) else None
        if not isinstance(body, str):
            continue
        try:  # a NUL byte, an overlong name or a symlink loop claims nothing (the schema pass judges the skill)
            target = (path.parent / body).resolve()
        except (OSError, ValueError, RuntimeError):
            continue
        if target.is_relative_to(root):
            claims.add(target.relative_to(root).as_posix())
    return claims


def _step_enhancement_violations(path: Path, document: dict[str, Any]) -> list[str]:
    """Fragment addressing rules that JSON Schema cannot express over companion files."""
    problems = []
    expected_id = path.name.removesuffix(".step-enhancement.yaml")
    if document.get("id") != expected_id:
        problems.append(f"prompt_fragment_invalid: enhancement id {document.get('id')!r} is not its file stem {expected_id!r}")
    entries = document.get("prompt_fragments")
    seen: set[str] = set()
    for index, entry in enumerate(entries if isinstance(entries, list) else []):
        if not isinstance(entry, dict):
            continue
        slot = entry.get("slot")
        if isinstance(slot, str):
            if slot in seen:
                problems.append(f"prompt_fragment_invalid: enhancement names slot {slot!r} more than once")
            seen.add(slot)
        companion = entry.get("path")
        if isinstance(companion, str) and not (path.parent / companion).is_file():
            problems.append(f"prompt_fragment_invalid at /prompt_fragments/{index}/path: companion {companion!r} does not exist beside the enhancement")
    return problems


def validate_pack(pack_dir: Path, contract: Contract) -> PackReport:
    """Validate every file of one pack directory; violations are sorted and path-relative.

    A manifest's hashes and its full membership are pack-doctor's (``manifest_stale``, ``manifest_membership``) and
    ``pack-doctor remediate`` writes it (#347): only an unlisted graph node is reported here (a house rule)."""
    if not pack_dir.is_dir():
        raise GateError(f"{pack_dir} is not a directory")
    report = PackReport(pack=pack_dir.name)
    descriptor = _load_or_none(pack_dir / "pack.yaml")
    require_empty_slots = isinstance(descriptor, dict) and descriptor.get("schema_version") == "1.0"
    manifest: dict[str, Any] | None = None
    payloads: set[str] = set()
    sidecars: list[tuple[str, str]] = []
    claimed = companion_claims(pack_dir, contract)
    fixture = is_invalid_fixture(pack_dir)
    stray: list[str] = []
    for path in sorted(pack_dir.rglob("*")):
        inside = path.relative_to(pack_dir).as_posix()
        relative = f"{pack_dir.name}/{inside}"
        if path.is_symlink():  # a file or a directory; not followed, so a link cannot smuggle files in or out
            report.violations.append(f"{relative}: symlink: a pack holds regular files and directories only")
            continue
        if not path.is_file():
            if not path.is_dir():
                report.violations.append(f"{relative}: not a regular file or directory")
            continue
        kind, rule = classify(contract, relative)
        if kind == "retired" and rule is not None:
            report.violations.append(f"{relative}: retired layout: {rule.reason}")
            continue
        if kind == "payload" and inside.startswith("assets/"):
            payloads.add(inside.removeprefix("assets/"))
        if kind in ("ignored", "unmodelled") and inside in claimed:
            report.skipped += 1  # a skill's body: held as its companion
            continue
        if kind != "file" or rule is None:
            tokens = path.name.rsplit(".", 2)
            if (kind == "unmodelled" and path.suffix == ".yaml" and len(tokens) == 3 and tokens[1] in KNOWN_KIND_TOKENS
                    and not kind_mapped(contract, tokens[1])):
                raise GateError(f"{relative}: a `{tokens[1]}` file has no schema mapping in file-kinds.yaml")
            if kind == "unmodelled" and not (fixture and inside in FIXTURE_FILES):
                # Charter #554 ruling Q1: warned as file_not_held, not held and not judged further (#309). The
                # charter's whole-pack round trip (OpenPacksDriftTest) still names it, so the pack set stays free.
                report.warnings.append(f"{relative}: file_not_held: not held (no pack file kind models this file)")
                stray.append(inside)
                report.skipped += 1
                continue
            if kind == "ignored" and rule is not None and not not_held_allowed(relative):
                # Operator ruling R34 (#331): a stray file in a pack warns, it does not fail; authors may keep notes.
                report.warnings.append(f"{relative}: file_not_held: not held ({rule.match}: {rule.reason})")
                stray.append(inside)
                report.skipped += 1
                continue
            report.skipped += 1
            continue
        validator = contract.validators.get(rule.schema or "")
        if validator is None:
            raise GateError(f"{relative}: rule {rule.match!r} names schema {rule.schema!r}, which is not loaded")
        try:
            # Bytes, not read_text: universal newlines would turn a CR into LF before the Markdown
            # reader could refuse it, as the charter does.
            text = path.read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise GateError(f"{relative}: unreadable: {exc!r}") from exc
        report.checked += 1
        try:
            document = parse_markdown(text) if rule.content_form == "markdown" else load_yaml(text)
        except (yaml.YAMLError, MarkdownRefused) as exc:
            report.violations.append(f"{relative}: not readable as {rule.content_form}: {_short(str(exc))}")
            continue
        errors = sorted(validator.iter_errors(document), key=lambda e: (list(map(str, e.absolute_path)), e.message))
        for error in errors:
            where = "/" + "/".join(str(part) for part in error.absolute_path)
            report.violations.append(f"{relative}: {rule.schema} schema at {where}: {_short(error.message)}")
        if rule.schema == "mission-step-prompt":
            for problem in prompt_slot_violations(text, require_empty=True):
                if problem.startswith("prompt_slot_not_empty") and not require_empty_slots:
                    report.warnings.append(f"{relative}: {problem}; an unversioned descriptor keeps this legacy block, descriptor 1.0 refuses it")
                else:
                    report.violations.append(f"{relative}: {problem}")
        elif rule.schema == "prompt-fragment":
            report.violations += [f"{relative}: {problem}" for problem in prompt_fragment_violations(text)]
        elif rule.schema == "step-enhancement" and isinstance(document, dict):
            report.violations += [f"{relative}: {problem}" for problem in _step_enhancement_violations(path, document)]
        if inside == MANIFEST_NAME and rule.schema == "pack-manifest" and not errors:
            manifest = document
        if rule.schema == "asset" and isinstance(document, dict) and isinstance(document.get("path"), str):
            sidecars.append((relative, document["path"]))
        # The charter's rule (spec pack-level-files FR-003): a preset's id is its file stem.
        if rule.schema == "preset" and isinstance(document, dict) and "id" in document and document["id"] != path.stem:
            report.violations.append(f"{relative}: preset id {document['id']!r} is not its file stem {path.stem!r}")
    # A pack with pack-level files (its README.md document, a manifest) needs its descriptor even when
    # judged alone. A pack with no descriptor at all is refused when the packs are checked together.
    if not (pack_dir / "pack.yaml").is_file() and any((pack_dir / n).is_file() for n in ("README.md", MANIFEST_NAME)):
        report.violations.append(
            f"{pack_dir.name}/pack.yaml: missing: a pack with a README.md or a {MANIFEST_NAME} needs its descriptor"
        )
    # The charter's SidecarPayloads rule: a sidecar names, exactly, an asset payload the pack holds.
    report.violations += [f"{file}: payload assets/{named} does not exist" for file, named in sidecars if named not in payloads]
    if manifest is not None:
        report.violations += [
            f"{pack_dir.name}/{MANIFEST_NAME}: incomplete manifest: graph node {node} is not a constituent; "
            f"declare it in a file the pack holds, or drop the node, then run `{REMEDIATE_COMMAND} {pack_dir}`"
            for node in unlisted_nodes(manifest, declared_nodes(pack_dir), held_artifacts(pack_dir, contract))
        ]
    if report.checked == 0:
        raise GateError(f"{pack_dir}: no pack file was checked; the gate would prove nothing")
    report.suspects = misspelled_companions(pack_dir, contract, stray)
    return report


# --------------------------------------------------------------------------- cross-pack house rules


#: A fragment kind plural that is not its node kind plus ``s`` (the contract's ``fragment_kinds``).
NODE_KIND_BY_PLURAL = {"glossaries": "glossary_context"}


def _singular(kind: str) -> str:
    """``directives`` -> ``directive``: fragments name kinds in the plural, URNs in the singular; ``glossaries`` ->
    ``glossary_context``, the glossary's node kind."""
    return NODE_KIND_BY_PLURAL.get(kind, kind.removesuffix("s"))


def _schema_node_kind(schema: str) -> str:
    """The node kind an artifact file of ``schema`` declares: the schema name with ``_`` for ``-``, through
    ``NODE_KIND_BY_ARTIFACT_KIND``."""
    kind = schema.replace("-", "_")
    return NODE_KIND_BY_ARTIFACT_KIND.get(kind, kind)


def _load_or_none(path: Path) -> Any:
    try:
        return load_yaml(path.read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None  # the per-pack validation already reports an unreadable file


#: Schemas of the artifact files whose ``id`` is a declaration of a node kind (the schema name with
#: ``-`` for ``_`` is the kind, through ``NODE_KIND_BY_ARTIFACT_KIND``): ``qa-001.directive.yaml`` declares
#: ``directive:QA_001`` and ``qa-glossary.glossary.yaml`` declares ``glossary_context:qa-glossary``.
ARTIFACT_SCHEMAS = frozenset(
    {
        "directive", "tactic", "styleguide", "toolguide", "paradigm", "procedure",
        "agent-profile", "anti-pattern", "asset", "glossary", "skill",
        "step-enhancement", "routing-catalog",
    }
)  # fmt: skip


def declared_nodes(pack_dir: Path, contract: Contract | None = None) -> set[tuple[str, str]]:
    """The ``(kind, id)`` pairs a pack declares: the nodes of its ``drg/fragment.yaml`` (``kind``
    plural, ``id``), of its root ``*.graph.yaml`` files (``urn``) and, given the contract, the
    ``id`` of each artifact file it classifies (kind from the file's schema). A file and a node of
    the same pack for one id are one declaration."""
    found: set[tuple[str, str]] = set()
    if contract is not None:
        for path in sorted(pack_dir.rglob("*.yaml")):
            if path.is_symlink() or not path.is_file():
                continue
            _, rule = classify(contract, f"{pack_dir.name}/{path.relative_to(pack_dir).as_posix()}")
            if rule is None or rule.schema not in ARTIFACT_SCHEMAS:
                continue
            document = _load_or_none(path)
            if isinstance(document, dict) and isinstance(document.get("id"), str):
                found.add((_schema_node_kind(rule.schema), document["id"]))
    fragment = _load_or_none(pack_dir / "drg" / "fragment.yaml")
    for node in (fragment.get("nodes") or []) if isinstance(fragment, dict) else []:
        if isinstance(node, dict) and isinstance(node.get("id"), str) and isinstance(node.get("kind"), str):
            found.add((_singular(node["kind"]), node["id"]))
    for graph_file in sorted(pack_dir.glob("*.graph.yaml")):
        graph = _load_or_none(graph_file)
        for node in (graph.get("nodes") or []) if isinstance(graph, dict) else []:
            urn = node.get("urn") if isinstance(node, dict) else None
            if isinstance(urn, str) and ":" in urn:
                kind, _, node_id = urn.partition(":")
                found.add((kind, node_id))
    return found


#: A template's id is its path: ``templates/<path>``, or ``<type>/<path>`` under a mission type.
TEMPLATE_PATH = re.compile(r"(?:missions/([^/]+)/)?templates/(.+)")


def held_artifacts(pack_dir: Path, contract: Contract | None) -> set[tuple[str, str]]:
    """The ``(kind, id)`` pairs a pack holds, in the charter's sense (``compositionFacts``): its
    artifact files (an anti-pattern's ``anti_patterns/<id>.anti-pattern.yaml`` among them) and the terms of its
    glossaries (``term``, ``<context-id>/<term-id>``: never declared, the target of a ``vocabulary`` edge). A node
    without a file, an ``anti_pattern`` node included, is held by nobody (charter ``check-packs.md``: "An anti-pattern
    is held only by its file"; #348 (f))."""
    held: set[tuple[str, str]] = set()
    for path in sorted(pack_dir.rglob("*")) if contract is not None else []:
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(pack_dir).as_posix()
        category, rule = classify(contract, f"{pack_dir.name}/{relative}")
        template = TEMPLATE_PATH.fullmatch(relative) if category == "payload" else None
        if template:
            held.add(("template", "/".join(part for part in template.groups() if part)))
        elif rule is not None and rule.schema in ARTIFACT_SCHEMAS | {"mission-type"}:
            document = _load_or_none(path)
            artifact_id = document.get("profile-id", document.get("id")) if isinstance(document, dict) else None
            if isinstance(artifact_id, str):
                held.add((_schema_node_kind(rule.schema), artifact_id))
                if rule.schema == "glossary":
                    held.update(
                        ("term", f"{artifact_id}/{term['id']}")
                        for term in document.get("terms") or []
                        if isinstance(term, dict) and isinstance(term.get("id"), str)
                    )
    return held


def split_qualifier(reference: str) -> tuple[str | None, str]:
    """``<pack>::<rest>`` as ``(pack, rest)``; a bare reference as ``(None, reference)``."""
    qualifier, separator, rest = reference.partition("::")
    return (qualifier, rest) if separator else (None, reference)


def graph_edges(pack_dir: Path) -> Iterator[tuple[Path, dict[str, Any]]]:
    """Every edge dictionary in a pack's DRG fragment and root graph documents, in stable order."""
    for graph in [pack_dir / "drg" / "fragment.yaml", *sorted(pack_dir.glob("*.graph.yaml"))]:
        document = _load_or_none(graph)
        for edge in (document.get("edges") or []) if isinstance(document, dict) else []:
            if isinstance(edge, dict):
                yield graph, edge


#: The agent-profile reference fields, the kind each names and the key an entry is keyed by:
#: ``directive-references`` entries carry a ``code`` (``QA_001``), the others an ``id``.
#: Together with ``collaboration.operating-procedures`` (plain strings naming procedures) these
#: are the selection data ADR-0064 keeps out of the graph; charter ADR-0053 decision 7 writes a
#: reference to another pack's artifact as ``<pack>::<id>`` in them.
PROFILE_REFERENCE_FIELDS = frozenset(
    {
        ("directive-references", "directive", "code"),
        ("tactic-references", "tactic", "id"),
        ("styleguide-references", "styleguide", "id"),
        ("toolguide-references", "toolguide", "id"),
    }
)


def _reference_keys(kind: str, reference: str) -> tuple[tuple[str, str], ...]:
    """The ``held`` keys a profile reference of ``kind`` names. A directive's code is its id
    (``QA_001``) or — built-in's convention — the number after ``DIRECTIVE_`` in its id: the
    code ``010`` names ``DIRECTIVE_010``."""
    return ((kind, reference), (kind, f"DIRECTIVE_{reference}")) if kind == "directive" else ((kind, reference),)


def profile_references(pack_dir: Path, contract: Contract | None) -> Iterator[tuple[str, str, str]]:
    """``(file, kind, reference)`` for every artifact an agent profile of ``pack_dir`` names
    in its directive-, tactic-, styleguide- and toolguide-references (a directive by its
    ``code``, the others by their ``id``) and in its collaboration operating-procedures. A
    reference is bare when it names the profile's own pack and ``<pack>::<id>`` when it names
    another pack's (charter ADR-0053 decision 7). Only files the contract classifies as agent
    profiles are read; without a contract none are."""
    for path in sorted(pack_dir.rglob("*.agent.yaml")) if contract is not None else []:
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(pack_dir).as_posix()
        _, rule = classify(contract, f"{pack_dir.name}/{relative}")
        if rule is None or rule.schema != "agent-profile":
            continue
        document = _load_or_none(path)
        if not isinstance(document, dict):
            continue
        file = f"{pack_dir.name}/{relative}"
        for field, kind, key in sorted(PROFILE_REFERENCE_FIELDS):
            for entry in document.get(field) or []:
                if isinstance(entry, dict) and isinstance(entry.get(key), str):
                    yield file, kind, entry[key]
        collaboration = document.get("collaboration")
        procedures = collaboration.get("operating-procedures") if isinstance(collaboration, dict) else None
        for procedure in procedures if isinstance(procedures, list) else []:
            if isinstance(procedure, str):
                yield file, "procedure", procedure


def _depends_on(pack: Path, descriptors: dict[Path, dict[str, Any]], by_id: dict[str, Path]) -> list[Path]:
    """The packs ``pack``'s ``depends_on`` names that resolve to a configured pack, in the order
    written; an unknown id names none."""
    entries = descriptors[pack].get("depends_on")
    targets = []
    for entry in entries if isinstance(entries, list) else []:
        pack_id = entry.get("pack_id") if isinstance(entry, dict) else None
        target = by_id.get(pack_id) if isinstance(pack_id, str) else None
        if target is not None:
            targets.append(target)
    return targets


def _depends_on_closure(pack: Path, descriptors: dict[Path, dict[str, Any]], by_id: dict[str, Path]) -> set[Path]:
    """The pack and every pack it reaches through ``depends_on``, which names packs by ``pack_id``."""
    reached, pending = {pack}, [pack]
    while pending:
        for target in _depends_on(pending.pop(), descriptors, by_id):
            if target not in reached:
                reached.add(target)
                pending.append(target)
    return reached


def _descriptors(pack_dirs: list[Path]) -> dict[Path, dict[str, Any]]:
    loaded = {pack: _load_or_none(pack / "pack.yaml") for pack in pack_dirs}
    return {pack: document if isinstance(document, dict) else {} for pack, document in loaded.items()}


def profile_reference_violations(
    pack_dirs: list[Path], held: dict[Path, set[tuple[str, str]]], contract: Contract | None = None
) -> list[str]:
    """Agent-profile references, judged like edge ends (charter ADR-0053 decision 7): a bare id held
    only by another pack, or by no pack at all (which resolves to no artifact), is refused; a reference
    qualified with the profile's own pack is refused, because references inside one pack stay bare; a
    qualified one must name a pack of the closure that holds it.

    Every part is kept. Two are house rules by open-packs' call (charter ``research/rule-coverage.md`` row 6): the
    bare reference no pack holds and the reference qualified with the profile's own pack. #348 lists the other three
    (the bare reference only another pack holds, the qualifier outside the closure, the named pack not holding it) as
    judged by pack-doctor at ``REFERENCES``; at the pin it does not judge any of them, so they stay until it does (C-003,
    the charter's answer is the rule; see the comment on each branch). The composition rules the charter does make
    (descriptors, ``depends_on``, graph edge ends) are not repeated here."""
    descriptors = _descriptors(pack_dirs)
    by_id = {d["pack_id"]: pack for pack, d in descriptors.items() if isinstance(d.get("pack_id"), str)}
    by_name = {d["name"]: pack for pack, d in descriptors.items() if isinstance(d.get("name"), str)}
    violations: list[str] = []
    for pack in pack_dirs:
        closure = _depends_on_closure(pack, descriptors, by_id)
        for file, kind, reference in profile_references(pack, contract):
            qualifier, ref_id = split_qualifier(reference)
            keys = _reference_keys(kind, ref_id)
            if qualifier is None:
                holder = next((other.name for other, nodes in held.items() if any(key in nodes for key in keys)), None)
                if holder is None:
                    # House rule (not a charter rule): the charter accepts a bare reference that no pack holds (charter
                    # research/rule-coverage.md row 6, the same family as the unheld bare DRG endpoint, DIV-007);
                    # open-packs refuses it by its own call (#348).
                    violations.append(f"{file}: bare {kind} reference {ref_id!r} resolves to no artifact of any pack")
                elif not any(key in held[pack] for key in keys):
                    # Not yet judged by pack-doctor (WP10 finding): #348 maps this to pack_reference_unqualified at
                    # REFERENCES, but the pinned jar reads only graph edges and guard/glossary relationships as
                    # references (CharterArtifact.writtenReferences), never an agent profile's. Retire it when
                    # RealPackDoctor.test_pack_doctor_does_not_yet_judge_agent_profile_references turns red.
                    violations.append(
                        f"{file}: bare {kind} reference {ref_id!r} is held only by {holder}; qualify it with that pack's name"
                    )
            else:
                named = by_name.get(qualifier)
                # the own pack, named by its descriptor name or by its directory (the natural way
                # a pack qualifies itself, `qa::x` in the pack of packs/qa): references inside
                # one pack stay bare, so no qualifier may name it
                if named is pack or (named is None and qualifier == pack.name):
                    # House rule (not a charter rule): the charter allows a reference qualified with its own pack
                    # (charter research/rule-coverage.md row 6); open-packs keeps references inside one pack bare (#348).
                    violations.append(
                        f"{file}: reference '{qualifier}::{ref_id}' names this profile's own pack; "
                        "references inside one pack stay bare"
                    )
                elif named not in closure:
                    # Not yet judged by pack-doctor (WP10 finding): #348 maps this to pack_reference_pack_missing, which
                    # the pinned jar does not fire for an agent profile's reference (see the bare branch above).
                    violations.append(f"{file}: reference '{qualifier}::{ref_id}' names a pack outside this pack's depends_on closure")
                elif not any(key in held[named] for key in keys):
                    # Not yet judged by pack-doctor (WP10 finding): #348 maps this to pack_reference_artifact_missing,
                    # which the pinned jar does not fire for an agent profile's reference (see the bare branch above).
                    violations.append(f"{file}: reference '{qualifier}::{ref_id}': {qualifier} does not hold {kind} {ref_id!r}")
    return violations


def prompt_fragment_composition_violations(pack_dirs: list[Path]) -> list[str]:
    """Each fragment slot the target step's prompt does not declare, independently of activation (ADR-0066 d8).

    Only the slot is judged here. The target is pack-doctor's (#348): a target step that does not exist is
    ``pack_reference_artifact_missing`` (or ``pack_reference_pack_missing``) at ``REFERENCES``, and a step whose prompt
    cannot be read is ``artifact_schema_error`` at the target's mission type file (``step '<id>' names <prompt path>:
    missing``), so both pass silently here. A target step with no ``prompt_path`` has no prompt (the pinned
    mission-type schema: ``prompt_path`` is "present when the step has a prompt"), so it declares no slot and every fragment aimed at it is refused here. What the charter refuses besides is not repeated either: an enhancement
    without exactly one ``enhances`` edge, and a target that is not ``action:<type>/<step>``.

    Sibling enhancements are deliberately not a conflict. The graph's ``enhances`` edge
    is the only target field; no target or activation key is read from the enhancement.

    This checkout has no mission-step integrity metadata, so it cannot refuse enhancement of a
    locked step. It also reads the target pack's declared prompt directly: prompt overrides that
    drop a slot are a charter-service check, not reproduced here (no pack overrides these prompts).
    """
    descriptors = _descriptors(pack_dirs)
    by_id = {d["pack_id"]: pack for pack, d in descriptors.items() if isinstance(d.get("pack_id"), str)}
    by_name = {document.get("name"): pack for pack, document in descriptors.items() if isinstance(document.get("name"), str)}
    problems: list[str] = []
    for pack in pack_dirs:
        pack_name = descriptors[pack].get("name")
        closure = _depends_on_closure(pack, descriptors, by_id)
        edges = list(graph_edges(pack))
        for enhancement in sorted(pack.glob("missions/*/enhancements/*.step-enhancement.yaml")):
            document = _load_or_none(enhancement)
            fragments = document.get("prompt_fragments") if isinstance(document, dict) else None
            if not isinstance(fragments, list) or not fragments:
                continue
            enhancement_id = document.get("id")
            source = f"step_enhancement:{enhancement_id}"
            targets = []
            for graph, edge in edges:
                qualifier, urn = split_qualifier(edge.get("source", ""))
                if edge.get("relation") == "enhances" and urn == source and (qualifier in (None, pack_name)):
                    targets.append((graph, edge.get("target")))
            file = f"{pack.name}/{enhancement.relative_to(pack).as_posix()}"
            if len(targets) != 1 or not isinstance(targets[0][1], str):
                continue  # the service refuses an enhancement without exactly one enhances edge
            target = targets[0][1]
            qualifier, urn = split_qualifier(target)
            target_pack = pack if qualifier is None else by_name.get(qualifier)
            if qualifier is not None and (target_pack is None or target_pack not in closure):
                continue  # the service refuses a qualifier outside the closure
            kind, _, action = urn.partition(":")
            if kind != "action" or action.count("/") != 1:
                continue  # the service refuses a target that is not action:<type>/<step>
            mission_id, step_id = action.split("/")
            mission_path = target_pack / "missions" / mission_id / f"{mission_id}.mission-type.yaml"
            mission = _load_or_none(mission_path)
            steps = []
            if isinstance(mission, dict):
                steps = [*(mission.get("steps") or []), *(mission.get("on_demand_steps") or [])]
            step = next((item for item in steps if isinstance(item, dict) and item.get("id") == step_id), None)
            if step is None:
                continue  # pack-doctor refuses a target step that does not exist (pack_reference_artifact_missing)
            prompt_path = step.get("prompt_path")
            if prompt_path is None:
                slots: set[str] = set()  # no prompt_path, no prompt (the pinned schema has no default path): no slot
            else:
                prompt = target_pack / "missions" / mission_id / str(prompt_path)
                try:
                    slots = declared_prompt_slots(prompt.read_text(encoding="utf-8"))
                except OSError:
                    continue  # pack-doctor refuses a prompt_path whose file cannot be read (artifact_schema_error)
            # House rule (not a charter rule): C38: the charter refuses an undeclared slot only for a stored activation
            # that has the enhancement in force; open-packs refuses it in every pack, activated or not (#348).
            for index, fragment in enumerate(fragments):
                slot = fragment.get("slot") if isinstance(fragment, dict) else None
                if isinstance(slot, str) and slot not in slots:
                    problems.append(f"{file}: prompt_slot_missing at /prompt_fragments/{index}/slot: target {target!r} declares no slot {slot!r}")
    return problems


# House rule (not a charter rule): the ruling R-s remainder. Pack-doctor does not judge a specializes_from cycle until
# charter epic #636 slices 2-4; retire this when a charter release lists it under REFERENCES (#348). It pools every
# pack's edges, which is stricter than registration's per-closure specialization_cycle.
def specialization_cycle_violations(pack_dirs: list[Path]) -> list[str]:
    """Each cycle among the ``specializes_from`` edges between agent profiles of ``pack_dirs`` (#286; charter ADR-0078
    decision 2: a role's candidates are ranked by their longest in-force chain, so the edges must be acyclic). A
    profile is keyed by its id, its pack qualifier dropped (an id is declared once across levels, which
    ``cross_pack_violations`` checks). Each cycle the depth-first walk meets is reported once, naming its ids in edge
    order from the smallest id: ``a -> b -> a``; every cyclic component yields at least one. A profile may have several
    parents. The edges of all the given packs are pooled on purpose, stricter than the charter's per-closure check:
    two packs that are never composed together still may not close a cycle between them."""
    parents: dict[str, set[str]] = {}
    for pack in pack_dirs:
        for _, edge in graph_edges(pack):
            if edge.get("relation") != "specializes_from":
                continue
            ends = [split_qualifier(edge.get(end))[1] if isinstance(edge.get(end), str) else "" for end in ("source", "target")]
            kinds_ids = [end.partition(":") for end in ends]
            if all(kind == "agent_profile" and node_id for kind, _, node_id in kinds_ids):
                parents.setdefault(kinds_ids[0][2], set()).add(kinds_ids[1][2])
    cycles: set[tuple[str, ...]] = set()
    state: dict[str, int] = {}  # 1 on the current path, 2 done
    for root in sorted(parents):
        if root in state:
            continue
        # An explicit stack, so a long chain cannot exhaust the interpreter's recursion limit.
        path: list[str] = [root]
        pending: list[Iterator[str]] = [iter(sorted(parents.get(root, ())))]
        state[root] = 1
        while pending:
            parent = next(pending[-1], None)
            if parent is None:
                state[path.pop()] = 2
                pending.pop()
            elif state.get(parent) == 1:
                cycle = path[path.index(parent):]
                start = cycle.index(min(cycle))
                cycles.add(tuple(cycle[start:] + cycle[:start]))
            elif parent not in state:
                state[parent] = 1
                path.append(parent)
                pending.append(iter(sorted(parents.get(parent, ()))))
    return [f"specializes_from cycle among agent profiles: {' -> '.join((*cycle, cycle[0]))}" for cycle in sorted(cycles)]


def cross_pack_violations(pack_dirs: list[Path], contract: Contract | None = None) -> list[str]:
    """The house rules across all packs together: what the charter does not judge, by ruling (C-005, ADR-0083
    decision 18; #348). Everything else is pack-doctor's (``validate --round-trip --full``, run by
    ``scripts/ci/charter_pack_doctor.py``): composition, the preset items (``preset_item_undeclared``,
    ``preset_item_not_held``), the graph references and the step enhancements' targets. Kept here:

    * an id declared by two packs of different levels (the same id in two packs of one level is the charter's
      ``pack_sibling_conflict``);
    * a DRG edge endpoint written bare (``<kind>:<id>``) in a pack's fragment that resolves to no node of any pack (a
      qualified endpoint is pack-doctor's ``pack_reference_*``);
    * the agent-profile references of ``profile_reference_violations``;
    * the undeclared prompt-fragment slot of ``prompt_fragment_composition_violations``;
    * a cycle among the agent profiles' ``specializes_from`` edges (``specialization_cycle_violations``).

    Each names its ruling in a comment. With ``contract``, artifact files count as declarations too
    (``declared_nodes``).

    Fails closed (GateError) when no pack declares any node.
    """
    held = {pack: held_artifacts(pack, contract) for pack in pack_dirs}
    levels = {pack: descriptor.get("pack_level") for pack, descriptor in _descriptors(pack_dirs).items()}
    owners: dict[tuple[str, str], list[Path]] = {}
    for pack in pack_dirs:
        for key in declared_nodes(pack, contract):
            owners.setdefault(key, []).append(pack)
    if not owners:
        raise GateError("cross-pack rules: no pack declares any DRG node; the id index is empty and would prove nothing")
    # House rule (not a charter rule): ADR-0053 decision 6: the charter takes an id re-declared at another level as a
    # layer override (C-005, ADR-0083 decision 18); open-packs does not let an org pack re-declare a built-in id.
    violations = [
        f"{kind}:{node_id}: declared by packs of different levels "
        f"({', '.join(sorted(f'{pack.name} [{levels[pack]}]' for pack in packs))}); a pack re-declaring another level's id is not allowed here"
        for (kind, node_id), packs in sorted(owners.items())
        if len({levels[pack] for pack in packs}) > 1
    ]
    for pack in pack_dirs:
        fragment = _load_or_none(pack / "drg" / "fragment.yaml")
        for edge in (fragment.get("edges") or []) if isinstance(fragment, dict) else []:
            if not isinstance(edge, dict):
                continue
            for end in ("source", "target"):
                urn = edge.get(end)
                if not isinstance(urn, str):
                    continue
                qualifier, rest = split_qualifier(urn)
                kind, _, node_id = rest.partition(":")
                # House rule (not a charter rule): DIV-007: the charter accepts a bare edge endpoint that resolves to
                # no node; open-packs refuses it, across every pack given (#348).
                if qualifier is None and (kind, node_id) not in owners and not any((kind, node_id) in nodes for nodes in held.values()):
                    violations.append(
                        f"{pack.name}/drg/fragment.yaml: edge {end} {urn!r} resolves to no node of any pack"
                    )
    return (
        violations
        + profile_reference_violations(pack_dirs, held, contract)
        + specialization_cycle_violations(pack_dirs)
        + prompt_fragment_composition_violations(pack_dirs)
    )


# --------------------------------------------------------------------------- CLI


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("packs", nargs="*", type=Path, help="pack directories that must validate")
    parser.add_argument("--expect-invalid", action="append", default=[], type=Path, metavar="PACK",
                        help="a pack directory that must produce schema violations (non-vacuity)")
    parser.add_argument("--cross-pack", action="store_true",
                        help="also check the given packs together for the house rules, what the charter does not judge "
                             "by ruling: an id re-declared at another level, a bare DRG edge endpoint that resolves to no "
                             "node, a prompt-fragment slot the target prompt does not declare, a specializes_from cycle, "
                             "and two agent-profile references (a bare one no pack holds, one qualified with the "
                             "profile's own pack). Also, until pack-doctor judges them (it does not at the pin), three "
                             "more agent-profile references: a bare one only another pack holds, one outside the "
                             "depends_on closure, one the named pack does not hold. Everything else across packs "
                             "(composition, preset items, graph references, step-enhancement targets, manifests) is "
                             "pack-doctor's: scripts/ci/charter_pack_doctor.py")
    parser.add_argument("--contract", type=Path, help="directory holding file-kinds.yaml and schemas/")
    args = parser.parse_args(argv)
    if not args.packs and not args.expect_invalid:
        parser.error("give at least one pack directory")
    try:
        status = EXIT_OK
        contract = contract_for(args.contract)
        print(f"charter contract: {args.contract or os.environ.get('CHARTER_CONTRACT_DIR') or charter_commit()}; "
              f"{len(contract.validators)} schemas loaded")
        for pack in args.packs:
            report = validate_pack(pack, contract)
            for line in report.warnings:
                print(f"::warning file={pack}::{line}")
            for inside, title, message in report.suspects:  # R38: a PR annotation on the file itself, never a failure
                print(f"::warning file={pack / inside},title={title}::{message}")
            for line in report.violations:
                print(f"::error file={pack}::{line}")
            print(f"{'ok' if report.ok else 'FAIL'}: {pack} ({report.checked} files checked, "
                  f"{report.skipped} not judged: excluded, payload or not held, {len(report.violations)} violations)")
            status = status or (EXIT_OK if report.ok else EXIT_INVALID)
        if args.cross_pack:
            found = cross_pack_violations(args.packs, contract)
            for line in found:
                print(f"::error::cross-pack: {line}")
            print(f"{'ok' if not found else 'FAIL'}: cross-pack rules over {len(args.packs)} packs ({len(found)} violations)")
            status = status or (EXIT_OK if not found else EXIT_INVALID)
        for pack in args.expect_invalid:
            report = validate_pack(pack, contract)
            if report.ok:
                print(f"::error file={pack}::{pack} is an invalid fixture but passed schema validation; the gate is vacuous")
                status = EXIT_INVALID
            else:
                print(f"ok: {pack} fails validation as expected ({len(report.violations)} violations)")
    except GateError as exc:
        print(f"::error::cannot judge, failing closed: {exc}")
        return EXIT_GATE
    return status


if __name__ == "__main__":
    sys.exit(main())
