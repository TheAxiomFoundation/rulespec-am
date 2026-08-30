# rulespec-am Agent Notes

> ⚠️ **Single source of truth for agent instructions.**
> `CLAUDE.md` and `GEMINI.md` both reference this file. Edit here, not in copies.

This repo stores Republic of Armenia RuleSpec source registry materials, oracle
references, and encoded policy rules.

## Status: source-backed bootstrap (pre-strict)

The first Armenian legal sources are in axiom-corpus as two signed ingest
scopes: the tax-benefit core (`axiom-corpus#628`) and a bounded 2024 evidence
pack (`axiom-corpus#629`). The proposed `am-rulespec-2026-08-30` selector is
still unpublished, so this repository intentionally has **no
`.axiom/toolchain.toml` binding and no RuleSpec content**. The remaining
sequence is corpus publication → a dedicated gated toolchain/workflow PR →
supervised encoding. See `docs/encoding-charter.md`. Until the binding lands,
no RuleSpec content may be added under `am/**`.

## Do

- Treat the scope as full-country coverage, not a demo slice.
- Prefer official Republic of Armenia sources for legal provenance: ARLIS
  (arlis.am, the official legal information system) and the State Revenue
  Committee (src.am). The authoritative text is the Armenian (hy) consolidated
  text; translations are working aids, never the encoded source.
- Use oracle references as comparison fixtures, not as legal authority.
- Keep oracle references pinned in `data/oracles/oracle-index.json`.
- Cite only official source snapshots that have landed in axiom-corpus with
  URL, retrieval date, sha provenance, and signed ingest manifests. The ARLIS
  adapter exists; extend it in axiom-corpus when a required expression is
  absent instead of inventing or hand-copying a source.
- Preserve the temporal-coverage distinction in
  `data/coverage/tax-benefit-source-map.json`: the funded-pension evidence spans
  2024 continuously, while the 2024 Tax Code evidence contains only Q1 and
  year-end endpoints.
- Add atomic RuleSpec under `am/legislation/`, `am/policies/`,
  `am/regulations/`, or `am/statutes/` with companion `.test.yaml` files —
  through the supervised encoder with encoding manifests only, once the
  toolchain is bound.
- Add only declarative `.yaml` ProgramSpecs under `am/programs/`; keep Python
  tooling under `src/rulespec_am/`.
- Keep large source payloads outside Git unless they are small, necessary
  official extracts.
- Read TheAxiomFoundation/.github#39 before opening any PR here.

## Do Not

- Migrate OpenFisca or PolicyEngine code mechanically as RuleSpec.
- Treat secondary summaries, commercial tax guides, oracle model code, or the
  research notes in `docs/` as canonical law — they are worklist scaffolding;
  every encoded value comes from the official Armenian text in corpus.
- Hand-write or hand-edit RuleSpec content; content changes carry encoding
  manifests from the supervised encoder.
- Hand-copy statute text into RuleSpec without a corpus `citation_path`.
- Add repository-root content trees, `.yml` aliases, symlinks, Python program
  implementations, generated formula artifacts, or standalone YAML fixtures.
- Touch `.axiom/toolchain.toml`, workflow pins, or CODEOWNERS in a feature PR —
  dedicated gated PRs only.
- Edit a dirty `axiom-encode` checkout owned by another agent.
