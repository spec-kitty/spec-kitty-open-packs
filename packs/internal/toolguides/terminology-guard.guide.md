# Terminology Guard

## Overview

The terminology guard is the repository's vocabulary check: a gate that scans active
files for terms the project has retired or superseded. It enforces canonical naming at
the commit level. If a retired term reappears in prose or code, CI fails and the change
is rejected before merge.

Each repository names its own check. Find it in the repository's charter or contributor
docs (for example CONTRIBUTING). It can be a script, a test or a lint rule, and it reads
the canonical terms from the repository's glossary.

## When to use

Before pushing any change to user-facing prose, docs or doctrine. The check may run only
in a CI shard that your local default test run skips, so run it explicitly before you
push.

## Usage

Run the command the repository's docs give for its vocabulary check, from the
repository root. Two common shapes:

```bash
python3 scripts/ci/<vocabulary-check>.py
pytest <path-to-terminology-test> -q
```

## Understanding Failure Output

A failure names the retired term, the canonical replacement where the check knows one,
and each file and line where the term was found. The list of retired terms lives in the
check itself or in the glossary it reads; the check's docs say which.

## How to Fix

Reword the prose to use the canonical term. Do **not** add a suppression, an exemption,
or a skip. The guard exists to prevent exemption creep.

Most such checks are plain fixed-string scans. They do not know about Markdown
structure, code fences or inline backticks. A retired term inside a code block or in
backtick-quoted prose **still trips the guard** if the file is scanned.

To refer to a retired term by name without tripping the guard, use meta-language in
place of the literal string: for example "the superseded selector term" or "the retired
status wording". A check often builds its own term list from string fragments for the
same reason.

The check's own docs name the paths it excludes, such as historical mission snapshots or
immutable decision records. Everything else it scans is in force.
