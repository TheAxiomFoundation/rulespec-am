from __future__ import annotations

import hashlib
import json
import re
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIRS = ("statutes", "regulations", "policies", "legislation")
AM_BUCKETS = (*CONTENT_DIRS, "programs")
IGNORED_ROOT_DIRS = {
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    # The shared validator checks immutable toolchain repositories out here
    # before running this repository's tests. Tracked paths are rejected by a
    # separate workflow step, so ignoring this transient directory does not
    # weaken the committed layout contract.
    "_axiom",
    "__pycache__",
}
ALLOWED_ROOT_DIRS = {
    ".axiom",
    ".github",
    "am",
    "data",
    "docs",
    "src",
    "tests",
}
ALLOWED_ROOT_FILES = {
    ".gitignore",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "LICENSE",
    "LICENSE-CODE",
    "NOTICE",
    "README.md",
    "known-missing-money-atoms.yaml",
    "known-validation-gaps.yaml",
    "oracle-coverage-pending.yaml",
}


def rulespec_files() -> list[Path]:
    return sorted(
        path
        for bucket in CONTENT_DIRS
        for path in (ROOT / "am" / bucket).rglob("*.yaml")
        if not path.name.endswith(".test.yaml")
    )


def test_only_am_namespace_present() -> None:
    jurisdiction_names = {
        child.name
        for child in ROOT.iterdir()
        if child.is_dir()
        and re.fullmatch(r"[a-z]{2}(?:-[a-z0-9-]+)*", child.name)
        and any((child / marker).is_dir() for marker in CONTENT_DIRS)
    }
    assert jurisdiction_names <= {"am"}


def test_am_content_buckets_exist() -> None:
    for bucket in AM_BUCKETS:
        assert (ROOT / "am" / bucket).is_dir()


def test_root_inventory_is_allowed() -> None:
    directories = {
        child.name
        for child in ROOT.iterdir()
        if child.is_dir() and child.name not in IGNORED_ROOT_DIRS
    }
    files = {
        child.name
        for child in ROOT.iterdir()
        if child.is_file() and child.name != ".git"
    }
    assert not directories - ALLOWED_ROOT_DIRS
    assert not files - ALLOWED_ROOT_FILES


def test_structure_manifest_matches_repository_contract() -> None:
    manifest = yaml.safe_load((ROOT / ".axiom/repository-structure.yaml").read_text())
    assert manifest["version"] == 1
    assert set(manifest["allowed_root_directories"]) == ALLOWED_ROOT_DIRS
    assert set(manifest["allowed_root_files"]) == ALLOWED_ROOT_FILES


def test_no_rulespec_content_before_toolchain_binding() -> None:
    if not (ROOT / ".axiom/toolchain.toml").is_file():
        assert rulespec_files() == []


def test_every_rulespec_has_companion_test() -> None:
    for path in rulespec_files():
        assert path.with_name(path.stem + ".test.yaml").exists()


def test_empty_ratchets_have_current_shapes() -> None:
    validation_gaps = yaml.safe_load((ROOT / "known-validation-gaps.yaml").read_text())
    assert validation_gaps == {"validate_failures": {}}

    missing_money = yaml.safe_load(
        (ROOT / "known-missing-money-atoms.yaml").read_text()
    )
    assert missing_money == {"total_allowed": 0}

    pending = yaml.safe_load((ROOT / "oracle-coverage-pending.yaml").read_text())
    assert pending == {
        "version": 1,
        "issue": "https://github.com/TheAxiomFoundation/rulespec-am/issues/1",
        "ceiling": 0,
        "entries": [],
    }


def test_scoped_indexes() -> None:
    for relative in (
        "data/oracles/oracle-index.json",
        "data/coverage/tax-benefit-source-map.json",
    ):
        payload = json.loads((ROOT / relative).read_text())
        assert payload["jurisdiction"] == "am"


def test_source_map_does_not_overstate_2024_tax_code_coverage() -> None:
    payload = json.loads(
        (ROOT / "data/coverage/tax-benefit-source-map.json").read_text()
    )
    instruments = {item["id"]: item for item in payload["instruments"]}
    tax_code = instruments["tax-code"]
    assert tax_code["temporal_coverage"].startswith("bounded_2024_endpoints")
    tax_code_2024 = [
        (item["expression_from"], item["expression_to_exclusive"])
        for item in tax_code["expressions"]
        if item["corpus_scope"].endswith("am-rulespec-source-pack")
    ]
    assert tax_code_2024 == [
        ("2024-01-01", "2024-03-24"),
        ("2024-12-23", "2025-01-01"),
    ]
    assert tax_code_2024[0][1] < tax_code_2024[1][0]

    funded_pensions = instruments["funded-pensions"]
    assert funded_pensions["temporal_coverage"].startswith("continuous_2024")
    funded_pensions_2024 = [
        (item["expression_from"], item["expression_to_exclusive"])
        for item in funded_pensions["expressions"]
        if item["corpus_scope"].endswith("am-rulespec-source-pack")
    ]
    assert funded_pensions_2024 == [
        ("2023-10-13", "2024-03-27"),
        ("2024-03-27", "2024-07-09"),
        ("2024-07-09", "2025-01-01"),
    ]
    assert all(
        left[1] == right[0]
        for left, right in zip(
            funded_pensions_2024[:-1], funded_pensions_2024[1:], strict=True
        )
    )
    assert funded_pensions_2024[0][0] <= "2024-01-01"
    assert funded_pensions_2024[-1][1] == "2025-01-01"
    release = payload["release_candidate"]
    assert release["status"] == "registered_publicly_mirrored_not_activated"
    assert release["content_sha256"] == (
        "19f443c7a9deec74b68ddc031d1c74bb2977753538fe2597d4c655609bc79706"
    )


def test_toolchain_binds_exact_registered_release_and_waiver_set() -> None:
    toolchain = tomllib.loads((ROOT / ".axiom/toolchain.toml").read_text())[
        "toolchain"
    ]
    release = json.loads(
        (ROOT / "data/coverage/tax-benefit-source-map.json").read_text()
    )["release_candidate"]
    assert toolchain == {
        "axiom_corpus_release": release["name"],
        "axiom_corpus_release_content_sha256": release["content_sha256"],
        "validation_waiver_set_sha256": (
            "e8caa37b6c2cf4558bfe10119ff8a6eae587e278ab349508f372e0e408d72b6e"
        ),
    }
    assert toolchain["validation_waiver_set_sha256"] == hashlib.sha256(
        (ROOT / "known-validation-gaps.yaml").read_bytes()
    ).hexdigest()


def test_repository_checks_use_reviewed_strict_pins() -> None:
    workflow = yaml.load(
        (ROOT / ".github/workflows/repository-checks.yml").read_text(),
        Loader=yaml.BaseLoader,
    )
    assert workflow["on"] == {
        "push": {"branches": ["main"]},
        "pull_request": {"branches": ["main"]},
    }
    validate = workflow["jobs"]["validate"]
    assert validate["uses"] == (
        "TheAxiomFoundation/.github/.github/workflows/validate-rulespec.yml@"
        "842c69d6aa62a0d75a4da850fabc3d0df20701d7"
    )
    assert validate["secrets"] == "inherit"
    assert validate["with"] == {
        "axiom-encode-ref": "d248fc99f8713a12a3dfa91348d992f4c58df43b",
        "axiom-rules-engine-ref": (
            "fb735bf47a32a4e8af1ecc144c9a1ab382da984b"
        ),
        "axiom-corpus-ref": "4f57160eb68c5941789ffab2ec991cd007a8c15b",
        "rulespec-us-ref": "0f291b367bf7e15555f9973112278c5cbf221653",
        "validate-roots": "auto",
        "run-generated-guard": "true",
        "guard-programs-root": "false",
    }


def test_registry_remains_experimental_during_encoding() -> None:
    payload = tomllib.loads((ROOT / ".axiom/registry.toml").read_text())
    assert payload == {"registry": {"app_visibility": "experimental"}}
