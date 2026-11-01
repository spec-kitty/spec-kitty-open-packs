"""A small evaluator for GitHub Actions expressions, for property tests over the parsed workflows.

It covers the subset the workflows here use: literals, context paths (with the `.*` object filter),
`! == != && ||`, parentheses, and the functions `contains`, `startsWith`, `endsWith`, `format`,
`always`, `success`, `failure`, `cancelled`. Within that subset it follows GitHub's semantics:
`&&`/`||` return an operand and short-circuit, names and string comparison ignore case, a missing
property is null, mixed-type `==` compares as numbers, and an `if` without a status function implies
`success() &&`. Anything outside the subset raises, so a workflow cannot silently outgrow it.

`strict_event=True` turns a read of a missing `github.event.*` property into an error, so a test can
prove an expression never reads a payload field the event lacks unless a guard short-circuits first.
"""

from __future__ import annotations

import json
import re
from typing import Any

_TOKEN = re.compile(
    r"\s*(?:"
    r"(?P<num>-?\d+(?:\.\d+)?)"
    r"|(?P<str>'(?:[^']|'')*')"
    r"|(?P<op>==|!=|&&|\|\||[!().,\[\]*])"
    r"|(?P<name>[A-Za-z_][A-Za-z0-9_-]*)"
    r")"
)

_MISSING = object()


class ExpressionError(Exception):
    """The expression is malformed, or (strict mode) it read a missing event property."""


def _tokenize(text: str) -> list[tuple[str, str]]:
    tokens, pos = [], 0
    text = text.strip()
    while pos < len(text):
        match = _TOKEN.match(text, pos)
        if not match or match.end() == pos:
            raise ExpressionError(f"cannot tokenize {text[pos:]!r} in {text!r}")
        kind = match.lastgroup
        tokens.append((kind, match.group(kind)))
        pos = match.end()
    return tokens


def _truthy(value: Any) -> bool:
    if value is None or value is False:
        return False
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value != 0
    if isinstance(value, str):
        return value != ""
    return True


def _coerce_number(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip()) if value.strip() else 0.0
        except ValueError:
            return float("nan")
    return float("nan")


def _equal(left: Any, right: Any) -> bool:
    if isinstance(left, str) and isinstance(right, str):
        return left.lower() == right.lower()
    if type(left) is type(right):
        return left == right
    if isinstance(left, (dict, list)) or isinstance(right, (dict, list)):
        return left is right
    return _coerce_number(left) == _coerce_number(right)


def _to_string(value: Any) -> str:
    if value is None:
        return ""
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return str(value)


class _Parser:
    def __init__(self, text: str, contexts: dict[str, Any], status: dict[str, bool], strict_event: bool):
        self.text = text
        self.tokens = _tokenize(text)
        self.pos = 0
        self.contexts = contexts
        self.status = status
        self.strict_event = strict_event

    # Grammar (lowest precedence first): or -> and -> equality -> unary -> postfix.
    def parse(self) -> Any:
        value = self._or(True)
        if self.pos != len(self.tokens):
            raise ExpressionError(f"unexpected {self.tokens[self.pos][1]!r} in {self.text!r}")
        return value

    def _peek(self) -> str | None:
        return self.tokens[self.pos][1] if self.pos < len(self.tokens) else None

    def _take(self, expected: str | None = None) -> tuple[str, str]:
        if self.pos >= len(self.tokens):
            raise ExpressionError(f"unexpected end of {self.text!r}")
        token = self.tokens[self.pos]
        if expected is not None and token[1] != expected:
            raise ExpressionError(f"expected {expected!r}, got {token[1]!r} in {self.text!r}")
        self.pos += 1
        return token

    # `live` is False on a short-circuited branch: it is parsed, but reads nothing, so strict mode
    # only fires on reads the runner would really make.
    def _or(self, live: bool) -> Any:
        value = self._and(live)
        while self._peek() == "||":
            self._take()
            decided = live and _truthy(value)
            right = self._and(live and not decided)
            if live and not decided:
                value = right
        return value

    def _and(self, live: bool) -> Any:
        value = self._equality(live)
        while self._peek() == "&&":
            self._take()
            decided = live and not _truthy(value)
            right = self._equality(live and not decided)
            if live and not decided:
                value = right
        return value

    def _equality(self, live: bool) -> Any:
        value = self._unary(live)
        while self._peek() in ("==", "!="):
            op = self._take()[1]
            right = self._unary(live)
            value = _equal(value, right) if op == "==" else not _equal(value, right)
        return value

    def _unary(self, live: bool) -> Any:
        if self._peek() == "!":
            self._take()
            return not _truthy(self._unary(live))
        return self._postfix(live)

    def _postfix(self, live: bool) -> Any:
        kind, text = self._take()
        path: list[str] = []
        if kind == "num":
            value: Any = float(text) if "." in text else int(text)
        elif kind == "str":
            value = text[1:-1].replace("''", "'")
        elif text == "(":
            value = self._or(live)
            self._take(")")
        elif kind == "name" and self._peek() == "(":
            value = self._call(text, live)
        elif kind == "name":
            lowered = text.lower()
            if lowered in ("true", "false", "null"):
                return {"true": True, "false": False, "null": None}[lowered]
            path = [text]
            value = next((v for k, v in self.contexts.items() if k.lower() == text.lower()), _MISSING) if live else None
            if live and value is _MISSING:
                raise ExpressionError(f"unknown context {text!r} in {self.text!r}")
        else:
            raise ExpressionError(f"unexpected {text!r} in {self.text!r}")
        filtered = False
        while self._peek() in (".", "["):
            if self._take()[1] == ".":
                key = self._take()[1]
            else:
                key_value = self._or(live)
                self._take("]")
                key = _to_string(key_value)
            if key == "*":
                filtered = True
                value = list(value.values()) if isinstance(value, dict) else (value if isinstance(value, list) else [])
                continue
            path.append(key)
            if not live:
                continue
            if filtered:
                value = [item.get(key) for item in value if isinstance(item, dict)]
            else:
                value = self._get(value, key, path)
        return value if live else None

    def _get(self, value: Any, key: str, path: list[str]) -> Any:
        if isinstance(value, dict):
            for candidate in value:
                if candidate.lower() == key.lower():
                    return value[candidate]
        if self.strict_event and path[:2] == ["github", "event"] and len(path) > 2:
            raise ExpressionError(f"reads missing event property {'.'.join(path)!r} in {self.text!r}")
        return None

    def _call(self, name: str, live: bool) -> Any:
        self._take("(")
        args: list[Any] = []
        while self._peek() != ")":
            args.append(self._or(live))
            if self._peek() == ",":
                self._take()
        self._take(")")
        if not live:
            return None
        fn = name.lower()
        if fn in ("always", "success", "failure", "cancelled"):
            return True if fn == "always" else self.status[fn]
        if fn == "contains":
            haystack, needle = args
            if isinstance(haystack, list):
                return any(_equal(item, needle) for item in haystack)
            return _to_string(needle).lower() in _to_string(haystack).lower()
        if fn == "startswith":
            return _to_string(args[0]).lower().startswith(_to_string(args[1]).lower())
        if fn == "endswith":
            return _to_string(args[0]).lower().endswith(_to_string(args[1]).lower())
        if fn == "format":
            fmt, rest = _to_string(args[0]), args[1:]
            return re.sub(r"\{\{|\}\}|\{(\d+)\}",
                          lambda m: _to_string(rest[int(m.group(1))]) if m.group(1) else m.group(0)[0], fmt)
        raise ExpressionError(f"unsupported function {name!r} in {self.text!r}")


DEFAULT_STATUS = {"success": True, "failure": False, "cancelled": False}


def evaluate(expression: str, contexts: dict[str, Any], *, status: dict[str, bool] | None = None,
             strict_event: bool = False) -> Any:
    """Evaluate one bare expression (no `${{ }}`)."""
    return _Parser(expression, contexts, status or DEFAULT_STATUS, strict_event).parse()


_TEMPLATE = re.compile(r"\$\{\{(.*?)\}\}", re.S)


def render(value: Any, contexts: dict[str, Any], **kwargs: Any) -> Any:
    """Evaluate a workflow field: a string with `${{ }}` parts. A field that is one whole `${{ }}` keeps its type."""
    if not isinstance(value, str):
        return value
    whole = _TEMPLATE.fullmatch(value.strip())
    if whole:
        return evaluate(whole.group(1), contexts, **kwargs)
    return _TEMPLATE.sub(lambda m: _to_string(evaluate(m.group(1), contexts, **kwargs)), value)


def evaluate_if(condition: Any, contexts: dict[str, Any], **kwargs: Any) -> bool:
    """Evaluate a job's or step's `if:`. Without a status function it implies `success() &&`, as on GitHub."""
    if condition is None:
        return _truthy(evaluate("success()", contexts, **kwargs))
    text = ("true" if condition else "false") if isinstance(condition, bool) else str(condition).strip()
    whole = _TEMPLATE.fullmatch(text)
    if whole:
        text = whole.group(1).strip()
    if not re.search(r"\b(always|success|failure|cancelled)\s*\(", text):
        text = f"success() && ({text})"
    return _truthy(evaluate(text, contexts, **kwargs))


def expressions_in(node: Any) -> list[str]:
    """Every `${{ }}` expression inside a parsed workflow node, plus each bare `if:` condition."""
    found: list[str] = []
    if isinstance(node, dict):
        for key, child in node.items():
            if key == "if" and isinstance(child, str) and not _TEMPLATE.search(child):
                found.append(child)
            else:
                found.extend(expressions_in(child))
    elif isinstance(node, list):
        for child in node:
            found.extend(expressions_in(child))
    elif isinstance(node, str):
        found.extend(m.group(1) for m in _TEMPLATE.finditer(node))
    return found
