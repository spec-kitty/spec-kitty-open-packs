# Test-Quality Triage (static scan of pytest and JUnit corpora)

## Overview

`test-quality-scan.py` is the static first pass of the
`test-suite-quality-assessment` procedure. It lives in this pack as an asset
(`packs/internal/assets/test-quality-scan.py`), so a run never has to rebuild
it. The file name does not match `test_*.py`, so pytest never collects it.

It **runs no tests**. The Python front end parses `test_*.py` and `*_test.py`
with the standard-library `ast` module. The Java front end discovers
`*Test.java`, `*Tests.java` and `*IT.java` below `src/test/java`, then parses
methods annotated with JUnit 4 or 5 `@Test`, `@ParameterizedTest`,
`@RepeatedTest`, `@TestFactory` or `@TestTemplate`. jqwik `@Property` methods are deliberately
excluded. Java parsing uses the official tree-sitter bindings declared by the
script's exact PEP 723 pins; those imports are lazy, so Python-only scans stay
standard-library only.

The scanner flags the patterns below per test, then ranks files so review
squads read the worst first. Flags have identical codes and weights across
languages where a Java analogue exists.

## Usage

From a Python repository root:

```bash
make test-quality-scan
```

This scans all of `tests/` into `work/test-quality/<today>/`, which is
gitignored. Pass extra flags through `SCAN_ARGS`:

```bash
make test-quality-scan SCAN_ARGS="--paths tests/status tests/consolidation"
make test-quality-scan SCAN_ARGS="--since $(git rev-list -1 --before='48 hours ago' origin/main)"
```

Or call the asset directly through the charter pack asset resolver, which is
the same file:

```bash
python "$(spec-kitty charter pack asset path test-quality-scan)" \
    --out work/test-quality/$(date +%F) [--paths tests/<domain>] [--since <rev>] [--top 25] [--no-git]
```

For Java, use `uv run` so the PEP 723 dependencies resolve automatically:

```bash
uv run "$(spec-kitty charter pack asset path test-quality-scan)" \
    --paths src/test/java --out work/test-quality/$(date +%F)
```

A multi-module Java build can pass its modules or the repository root as the
paths instead. Files count only when their path contains `src/test/java`, and
discovery prunes `build`, `target`, dependency checkouts, VCS metadata and other
generated directories. A plain `python` invocation also works when `tree-sitter==0.25.2` and
`tree-sitter-java==0.23.5` are already installed. If they are missing, Java
scanning stops with an error containing both the `uv run` and `pip install`
remedies when Java paths are passed explicitly. A mixed-tree scan without an
explicit Java path instead prints a warning and skips only the Java files;
Python scanning never asks for the parser packages.

Then hand the ranked ledgers to the review squads:

```bash
spec-kitty dispatch "Run the test-suite-quality-assessment procedure over work/test-quality/$(date +%F)/ledger/<domain>.md"
```

## Options

| Flag | Default | Meaning |
| --- | --- | --- |
| `--paths` | `tests` | Test roots or single files to scan; use `src/test/java` for a standard Java tree |
| `--since REV` | off | Score only tests added or changed since `REV` (window mode) |
| `--out DIR` | `work/test-quality` | Output folder |
| `--top N` | `25` | Files per domain ledger and in the summary |
| `--no-git` | off | Skip git provenance: faster, and works outside a git checkout |

## Outputs

| File | Content |
| --- | --- |
| `summary.md` | One row per domain (files, tests, flagged tests, score, top flags) and the top files overall |
| `files.json` | One row per module: domain, score, flag counts, `added`, `added_by`, `last_touched` |
| `tests.json` | One row per flagged test: file, line, qualified name, flags, score |
| `ledger/<domain>.md` | A review checklist of the domain's top-ranked files, with a `Verdict:` line each |

A Python domain is `tests/<dir>`, except `tests/specify_cli`, which is split one
level deeper because it is too large for one squad. A Java domain is the last
package directory below `src/test/java`: for example,
`service/src/test/java/com/acme/billing/PaymentTest.java` belongs to `billing`.
A class directly below `src/test/java` belongs to `(root)`. An existing ledger
is **never overwritten**, so a stopped review resumes where it left off. To
start a domain again, delete its ledger.

## Flag codes

The review codes (R1 to R9) come from the 2026-09-29 test review. Java uses the
existing weights and omits Python-only detectors that have no clean analogue.

| Code | Weight | Python pattern | Java pattern | Rubric |
| --- | ---: | --- | --- | --- |
| `no-assertion` | 5 | No `assert`, `raises`, assert-like call or local asserting helper | No `assert*`, `assertThat`, `assertThrows`, `fail`, `verify` or `andExpect`; calls to asserting helpers in the same class are exempt | R1 vacuous |
| `weak-only-assert` | 4 | The only assert is `True` or `x is not None` | The only check is `assertTrue(true)`, `assertNotNull` or AssertJ `isNotNull` | R1 vacuous |
| `type-only-assert` | 3 | The only assert is `isinstance`, `callable` or `hasattr` | The only oracle is `assertInstanceOf`/`isInstanceOf`, unchecked `assertThrows`, `@Test(expected=...)`, or try/fail/catch | R1 vacuous |
| `broad-raises` | 3 | `pytest.raises(Exception)` | `Exception`, `Throwable` or `RuntimeException` in `assertThrows`, `expected`, or try/fail/catch | R1 vacuous |
| `literal-source-scan` | 3 | Reads source text and asserts a substring | Not ported | R4 literal scan |
| `line-number-pin` | 3 | Asserts a `file.py:NN` location | Not ported | R6 line pin |
| `over-mocking` | 2 | Four or more patches or mocks in one test | Four or more `mock`, `when` or `@Mock` occurrences; class fields count only when the test references them | R2 over-mock |
| `private-attr` | 2 | Three or more private attributes read | Not ported | R3 implementation-coupled |
| `fake-short-ulid` | 2 | A `mission_id` that is not a 26-character ULID | Not ported | R7 fabricated data |
| `sleep`, `wallclock` | 2 | A real sleep, or an unfrozen clock | `Thread.sleep`, or a no-argument `now()` call on a known `java.time` type | R9 non-deterministic |
| `interaction-assert` | 1 | Asserts on mock calls | `verify`, `verifyNoInteractions` or `InOrder` | R3 implementation-coupled |
| `skip-or-xfail` | 1 | A skip or xfail that is not a platform or tool guard | `@Disabled`, `@Ignore` or `Assumptions.assume*` | masked defect candidate |
| `long-test`, `many-asserts` | 1 | More than 80 lines, or 15 or more asserts | More than 80 lines, or 15 or more assert calls | R8 multi-behaviour |
| `vague-name` | 1 | The name promises nothing (`test_basic`, `test_1`) | Equivalent names such as `test1` and `testBasic` | R8 unclear |
| `provenance-tokens` | 1 | WP, FR or T ids, or issue numbers, in the name or docstring | The same tokens in the method name | development-assist lens |
| `unparseable` | 1 | A Python syntax error | A Java tree with parser errors | parser coverage candidate |

For Java, a type check does not become `type-only-assert` when another assertion
checks behaviour. This includes additional JUnit assertions, an asserted
`assertThrows` result, AssertJ `hasMessage*`, `hasCause*`, `hasRootCause*`,
`satisfies`, `extracting` and `isInstanceOfSatisfying` chains. ArchUnit
`ArchRule.check(...)` is an oracle. A broad catch whose `fail` runs only when
the body unexpectedly raises is a does-not-raise contract, not a type or broad
exception finding. These are source-level heuristics, not type-resolved Java
analysis.

## Shallow clones

Provenance comes from one `git log` pass over the top-level directory of each
scanned root. Renames are followed, including a move in from a sibling
directory, so `added` names the commit that created the file, not the one that
last renamed it; a move in from outside that top-level directory still reads as
an add. On a shallow clone, the graft point stands in for the `added` date of
older files. Deepen the clone (`git fetch --deepen=<n>` or `--unshallow`) when
the development-assist lens matters.

## Known limitations

Every flag is a candidate, not a verdict:

- `no-assertion` fires on a test that delegates to a helper the front end cannot recognize. Java recognizes asserting helpers only in the same class, not on an enclosing class of a nested test.
- `weak-only-assert` fires on "passes strict validation" tests, where the call under test raises on failure. The assert is then only a formality.
- `provenance-tokens` fires on legitimate issue-pinned regression tests. It only feeds the development-assist lens, and it weighs the least.
- Java source cannot always reveal an inferred exception type or the implementation behind a fluent assertion. Review the captured exception and the complete assertion chain before acting.
- `unparseable` can mean unsupported syntax rather than a broken test. Check the grammar version before treating it as a product finding.

The opposite also holds: an unflagged test is not proven good. The scanner
cannot see a self-constructed oracle or a new gate stubbed out of an old
harness. Those need a read and a planted break, as the procedure describes.
