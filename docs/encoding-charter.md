# Encoding charter

Chartered 2026-08-28 alongside PolicyEngine/microcosm#814 (populace-am).
Armenia is the rules leg of a Microcosm country build: a diagnostic household
frame calibrated to public demographic, household, and employment aggregates
from an imported donor support pool, with this repository supplying the
tax-benefit rules through the Axiom rules engine adapter ("a new country adds
coverage, not adapter code" — rulespec-nz precedent).

## Why Armenia

- Smallest encoding surface of any country in the org so far: one flat
  schedular PIT, two payroll-adjacent contributions, one stamp duty, a small
  benefit set.
- Public aggregate controls allow an open calibration layer even though the
  diagnostic currently has no Armenian unit-record survey base.
- Institutional demand is documented: Armenia sits in the OECD EG DNA and
  EG DHW expert groups without being able to submit distributional results.

## Sequence (corpus-first, strict from day one of content)

1. **Source snapshots.** Retrieve the priority instruments (see
   `docs/sources-and-provenance.md`) from ARLIS as dated, sha-hashed snapshots.
   The initial core and bounded 2024 evidence snapshots are complete.
2. **Corpus ingestion.** Use the ARLIS ingestion path in axiom-corpus; land
   snapshots with signed ingest manifests from a clean root checkout. Corpus
   PRs merge-commit, never squash. The first two scopes landed in
   axiom-corpus#628 and #629.
3. **Release cut.** Publish an immutable signed `am-rulespec-*` corpus release
   from corpus main. `am-rulespec-2026-08-30` was signed and registered by
   axiom-corpus#630, then publicly mirrored for consumer validation. It was
   deliberately not activated into the production serving map.
4. **Toolchain binding.** Dedicated gated PR adding `.axiom/toolchain.toml`
   (release name, content sha, waiver-set sha) and the shared SHA-pinned
   validate workflow. Never combined with content changes.
5. **Supervised encoding.** Encode the v1 slice through the supervised encoder
   with encoding manifests; companion tests assign every local `#input` fact
   including FALSE facts; proofs are verbatim substrings of the resolved
   Armenian provision.
6. **Oracle comparison.** Cross-check against the pinned references in
   `data/oracles/oracle-index.json` (CEQ and World Bank fiscal-incidence
   numbers as bands; there is no incumbent engine and no parity gate).

## v1 slice (scope of the first encoding campaign)

Personal income tax (flat + schedular rates, exempt income), funded pension
contribution, health insurance contribution, servicemen's insurance stamp duty,
family living standards enhancement benefit, old-age pension amount, the
mortgage-interest refund, and the declaration social credits. Everything else
is backlog in `data/coverage/`.

## Out of scope for v1

- Wealth-side rules (no wealth data exists downstream to exercise them).
- VAT/excise/CIT (indirect and corporate surfaces come after the household
  slice proves out).
- Any claim of certification: complete ≠ certified; certification claims and
  external announcements are maintainer-gated.

## Open items

- [x] ARLIS snapshot tooling in axiom-corpus
- [x] Initial core and bounded 2024 evidence ingestion with signed manifests
- [x] Sign, register, and publicly mirror `am-rulespec-2026-08-30` (not activated)
- [x] Toolchain-binding PR (dedicated, gated)
- [ ] Supervised encoder campaign for the v1 slice
- [ ] Oracle band extraction from CEQ WP 43 (2017), World Bank PIT-reform
      microsimulation (2019), World Bank fiscal-incidence report (2025)
