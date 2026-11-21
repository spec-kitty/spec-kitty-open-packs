# Data model: Test doctrine 2

New graph nodes and the edges that make them reachable (source --relation--> target). Foundation edges live in its shards; others in the named pack's fragment.

| Node | Kind | Pack | Inbound edges (from activatable artefacts) |
|------|------|------|--------------------------------------------|
| `tests-as-scaffold-not-friction` | paradigm | foundation | DIRECTIVE_041 --refines-->, DIRECTIVE_054 --refines--> |
| `mock-owned-logic-to-pin-a-call-contract` | anti_pattern | foundation | paradigm, DIRECTIVE_054, unfake-an-over-mocked-test, test-boundaries-by-responsibility --rejects--> |
| `assert-on-mock-interactions` | anti_pattern | foundation | paradigm, DIRECTIVE_054, function-over-form-testing --rejects--> |
| `exemplar-slicing-user-registration` | asset | foundation | test-boundaries-by-responsibility, paradigm --suggests--> |
| `exemplar-unfake-an-over-mocked-test` | asset | foundation | unfake-an-over-mocked-test, DIRECTIVE_054 --suggests--> |
| `test-desiderata-checklist` | asset | testing | test-desiderata-and-boundaries, testing-principles --requires-->; foundation::paradigm --suggests--> (testing fragment) |
| `quad-a-test-structure` | asset | testing | quadruple-a-test-format --requires-->; python/java/javascript conventions --requires--> (their fragments) |
| `vertical-skeleton-first` | tactic | planning-analysis | foundation::action software-dev/plan --scope-->, foundation::tactic:product-coherence-review --suggests--> |
| `shared-machine-test-measurement` | tactic | testing | no-parallel-duplicate-test-runs --suggests-->; foundation::action software-dev/implement and review --scope--> |

Invariants: anti-pattern nodes emit no edges; at most one edge per unordered pair per pack; every new edge has `when` (or `reason` on `rejects`).

Glossary terms (foundation `spec-kitty-core`): `tracer-bullet`, `horizontal-slicing`, `spine`, `green-mode`.
