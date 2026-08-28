# Sources and provenance

## Official sources

| Source | URL | Role |
|---|---|---|
| ARLIS — Legal Information System of the Republic of Armenia | https://www.arlis.am | Official consolidated legal texts (Armenian). The authoritative text for every encoding. |
| State Revenue Committee (SRC) | https://www.src.am | Tax Code publication, declaration administration, taxpayer guidance. |
| Ministry of Finance | https://minfin.am | State budget execution reports (revenue actuals). |
| ArmStat — Statistical Committee | https://armstat.am | National accounts, ILCS microdata, register-based wage statistics (calibration side, see PolicyEngine/microcosm#814). |
| Official gazette (Pashtonakan Teghekagir) via ARLIS | https://www.arlis.am | Promulgation records for effective-date provenance. |

## Language rule

The authoritative text is the Armenian (hy) consolidated version. English
translations (including any SRC-published translation of the Tax Code) are
working aids for scoping and review; encodings ground in the Armenian text via
corpus `citation_path`, and proofs are verbatim substrings of the resolved
Armenian provision. Non-English encoding has org precedent (rulespec-dk,
rulespec-de, rulespec-be).

## Provenance rule

No provision may be cited by an encoding until it exists in axiom-corpus, or
the official source snapshot lands alongside with URL, retrieval date, and sha
provenance (TheAxiomFoundation/.github#39, rule 7). No `extract-am-*` path
exists in axiom-corpus today; the ingestion tooling for ARLIS snapshots is a
charter work item.

## Priority instruments (v1 slice)

Verified against secondary sources during scoping (2026-08-28); each requires
the primary Armenian text in corpus before encoding. Secondary-source values
below are worklist scaffolding only — never encodable values.

1. **Tax Code of the Republic of Armenia** (adopted 2016, in force 2018,
   as amended) — personal income tax: flat rate on salary and civil-contract
   income (20% since 1 Jan 2023 via legislated phase-down), schedular rates by
   income type (dividends 5%, royalties 10%, rental 10% plus surcharge above
   AMD 60m/yr, deposit interest 10%), exempt ("deductible") income including
   state pensions and benefits; mortgage-interest refund; social-expense
   credits; universal income declaration obligations.
2. **Law on Funded Pensions** — mandatory funded contribution: 5% of gross
   below AMD 500,000/month, else 10% minus AMD 25,000, base capped at
   AMD 1,125,000/month.
3. **Law on the health insurance contribution** (in force 25 Dec 2025) —
   AMD 4,800/month for gross salary AMD 200,001–500,000, AMD 10,800 above;
   self-employed schedule.
4. **Law on stamp duty for the servicemen's insurance fund** (Dec 2025
   restructure) — AMD 1,000/month up to AMD 1,000,000 gross, AMD 15,000 above.
5. **Law on state benefits** — family living standards enhancement benefit
   (basic AMD 18,000/month plus per-child supplements), childbirth grants,
   child-care benefits.
6. **Law on state pensions** — old-age pension formula, retirement age 63.
