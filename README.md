# rulespec-am

Republic of Armenia RuleSpec encodings and source registry.

This repository is the full-country Armenia RuleSpec workspace. It is intended
to cover the tax, social contribution, and social protection surface — personal
income tax, funded pension contributions, the health insurance contribution,
stamp duties, state benefits, and related eligibility rules — with official
source provenance and comparison references from published fiscal-incidence
studies.

**Status: source-backed bootstrap.** Signed Armenian source scopes now cover
the latest consolidated tax-benefit sources, including scheduled expressions,
and bounded 2024 PIT, funded-pension, and minimum-wage evidence. The immutable
corpus release is proposed but not yet published, so this repository still
carries no toolchain binding and no RuleSpec content. The corpus-first path to
strict validation is documented in `docs/encoding-charter.md`.

## Scope

- `am/{legislation,policies,regulations,statutes}/`: the four atomic RuleSpec
  roots for codes, delegated instruments, and source-grounded policy modules.
- `am/programs/`: declarative axiom-compose ProgramSpecs when a composed
  Armenian program is added. Programs are not atomic `rulespec/v1` modules.
- `src/rulespec_am/`: repository tooling; executable Python never lives under
  `am/programs/`.
- `data/corpus/`: repository-local corpus metadata when a binding is
  published; canonical provisions remain in axiom-corpus.
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
able to submit results. Microcosm now has a diagnostic Armenian frame calibrated
to public aggregates using an imported donor support pool; it does not claim
Armenian household survey microdata. This repository provides the legal-rules
leg through the Axiom rules engine adapter, beginning with a comparatively
compact PIT, contribution, and benefit surface.
