# rulespec-am Agent Notes

> ⚠️ **Single source of truth for agent instructions.**
> `CLAUDE.md` and `GEMINI.md` both reference this file. Edit here, not in copies.

This repo stores Republic of Armenia RuleSpec source registry materials, oracle
references, and encoded policy rules.

## Status: bootstrap (pre-strict)

No Armenian provisions exist in axiom-corpus yet, so this repository has **no
`.axiom/toolchain.toml` binding and no RuleSpec content**. The sequence is
corpus-first: official source snapshots → corpus ingestion with signed manifests
→ an immutable signed `am-rulespec-*` release → a dedicated gated PR that adds
the toolchain binding and the shared validate workflow → supervised encoding.
See `docs/encoding-charter.md`. Until the toolchain lands, no `am/**` content
may be added.

## Do

- Treat the scope as full-country coverage, not a demo slice.
- Prefer official Republic of Armenia sources for legal provenance: ARLIS
  (arlis.am, the official legal information system) and the State Revenue
  Committee (src.am). The authoritative text is the Armenian (hy) consolidated
  text; translations are working aids, never the encoded source.
- Use oracle references as comparison fixtures, not as legal authority.
- Keep oracle references pinned in `data/oracles/oracle-index.json`.
- Land official source snapshots in axiom-corpus with URL, retrieval date, and
  sha provenance before any encoding cites them. No `extract-am-*` ingestion
  path exists in axiom-corpus yet; building one is a charter work item — do not
  invent or assume one.
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
