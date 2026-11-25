# Quickstart: checking the packs with pack-doctor at the pin

Run everything from the repository root. You need Java 25.

```bash
# 1. Obtain the jar for the pin (it builds charter main at the pinned commit; on a release pin it downloads it).
jar="$(scripts/ci/charter_pack_doctor_jar.sh .charter-work)"

# 2. The gate: every pack and valid fixture, with --round-trip --full, plus the invalid fixtures.
python3 scripts/ci/charter_pack_doctor.py --jar "$jar" --report-dir .charter-work/report

# 3. The same check, by hand.
LC_ALL=C.UTF-8 java -jar "$jar" validate $(for p in packs/*/ tests/fixtures/valid/*/; do printf -- '--pack %s ' "${p%/}"; done) \
  --round-trip --full --report .charter-work/report/packs.yaml

# 4. After editing a pack: restamp its manifest in the charter's canonical form.
LC_ALL=C.UTF-8 java -jar "$jar" remediate packs/<pack>

# 5. Mission only: apply and check the anti-pattern curation ledgers.
python3 kitty-specs/pack-doctor-alignment-01M88RH1/curation/apply_curation.py --check
```

Exit codes: `0` valid (warnings allowed), `1` a problem, `2` a usage or I/O failure. Charter's
`docs/guides/check-packs.md` is the reference for the command line and the report.
