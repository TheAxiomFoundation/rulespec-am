from __future__ import annotations

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
    assert payload["release_candidate"]["status"] == "proposed_not_published"


def test_registry_remains_experimental_during_bootstrap() -> None:
    payload = tomllib.loads((ROOT / ".axiom/registry.toml").read_text())
    assert payload == {"registry": {"app_visibility": "experimental"}}
