# rulespec-am

Republic of Armenia RuleSpec encodings and source registry.

This repository is the full-country Armenia RuleSpec workspace. It is intended
to cover the tax, social contribution, and social protection surface — personal
income tax, funded pension contributions, the health insurance contribution,
stamp duties, state benefits, and related eligibility rules — with official
source provenance and comparison references from published fiscal-incidence
studies.

**Status: bootstrap.** No Armenian provisions exist in axiom-corpus yet, so
this repository carries no toolchain binding and no RuleSpec content. The
corpus-first path to strict validation is documented in
`docs/encoding-charter.md`.

## Scope

- `am/{legislation,policies,regulations,statutes}/`: the four atomic RuleSpec
  roots for codes, delegated instruments, and source-grounded policy modules.
- `am/programs/`: declarative axiom-compose ProgramSpecs when a composed
  Armenian program is added. Programs are not atomic `rulespec/v1` modules.
- `src/rulespec_am/`: repository tooling; executable Python never lives under
  `am/programs/`.
- `data/corpus/`: source inventory and provision slices promoted from official
  Armenian source ingestion.
- `data/oracles/`: pinned references to comparison studies and datasets used to
  cross-check Axiom outputs.
- `data/coverage/`: full-country coverage backlog and status.

## Sources

The authoritative legal text is the Armenian consolidated text in ARLIS
(arlis.am), the official legal information system of the Republic of Armenia;
the State Revenue Committee (src.am) publishes the Tax Code and administers
declarations. The source registry and provenance rules are in
`docs/sources-and-provenance.md`.

## Context

Chartered alongside PolicyEngine/microcosm#814 (populace-am): Armenia
participates in the OECD distributional-accounts expert groups without being
able to submit results, and its tax-benefit system — a flat schedular personal
income tax and a small set of contributions and benefits — is among the
smallest encoding surfaces of any country. This repository provides the rules
leg for that build through the Axiom rules engine adapter.
