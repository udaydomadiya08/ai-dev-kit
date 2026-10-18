"""
Comprehensive integration and scenario tests for Universal AI Dev Kit (UDK).
Tests realistic workflows: stack detection, idempotency, malformed manifests,
broken links, and cross-platform path handling.
"""

from __future__ import annotations

from pathlib import Path

from udk.cli import main
from udk.detector import detect_workspace
from udk.manifest import ManifestManager
from udk.validator.engine import ValidatorEngine


def test_scenario_existing_python_project_detection(tmp_path: Path):
    # Setup simulated Python project
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[project]\nname = "my-py-app"\nversion = "0.1.0"\n', encoding="utf-8"
    )

    profile, adapters, markers = detect_workspace(tmp_path)
    assert profile == "python"
    assert "agents-md" in adapters
    assert "python" in markers

    # Run init without specifying profile
    ret = main(["init", "--path", str(tmp_path)])
    assert ret == 0

    manifest = ManifestManager(tmp_path).load()
    assert manifest is not None
    assert manifest.profile == "python"
    assert (tmp_path / "AGENTS.md").is_file()


def test_scenario_existing_web_project_detection(tmp_path: Path):
    # Setup simulated Web project
    pkg = tmp_path / "package.json"
    pkg.write_text(
        '{"name": "my-web-app", "scripts": {"test": "vitest"}}\n', encoding="utf-8"
    )

    profile, _adapters, markers = detect_workspace(tmp_path)
    assert profile == "web"
    assert "web" in markers

    ret = main(["init", "--path", str(tmp_path)])
    assert ret == 0

    manifest = ManifestManager(tmp_path).load()
    assert manifest is not None
    assert manifest.profile == "web"


def test_scenario_init_idempotency(tmp_path: Path, capsys):
    # Run init once
    ret1 = main(
        [
            "init",
            "--path",
            str(tmp_path),
            "--profile",
            "minimal",
            "--agent",
            "agents-md",
        ]
    )
    assert ret1 == 0

    # Run init a second time without changes
    ret2 = main(
        [
            "init",
            "--path",
            str(tmp_path),
            "--profile",
            "minimal",
            "--agent",
            "agents-md",
        ]
    )
    assert ret2 == 0
    captured = capsys.readouterr()
    assert "[=] UNCHANGED" in captured.out


def test_scenario_invalid_arguments(tmp_path: Path, capsys):
    # Unknown profile
    ret1 = main(
        ["init", "--path", str(tmp_path), "--profile", "nonexistent-profile-xyz"]
    )
    assert ret1 == 1
    captured1 = capsys.readouterr()
    assert "Unknown profile" in captured1.err

    # Unknown agent
    ret2 = main(["init", "--path", str(tmp_path), "--agent", "nonexistent-agent-xyz"])
    assert ret2 == 1
    captured2 = capsys.readouterr()
    assert "Unknown agent adapter" in captured2.err


def test_scenario_corrupt_manifest_validation(tmp_path: Path):
    main(["init", "--path", str(tmp_path), "--profile", "minimal"])

    # Corrupt manifest
    manifest_file = tmp_path / ".udk" / "manifest.json"
    manifest_file.write_text("{ broken json ...", encoding="utf-8")

    validator = ValidatorEngine(tmp_path)
    diags = validator.validate_manifest()
    assert any(d.code == "MANIFEST_CORRUPT" for d in diags)


def test_scenario_missing_managed_file_validation(tmp_path: Path):
    main(
        [
            "init",
            "--path",
            str(tmp_path),
            "--profile",
            "minimal",
            "--agent",
            "agents-md",
        ]
    )

    # Delete AGENTS.md
    (tmp_path / "AGENTS.md").unlink()

    validator = ValidatorEngine(tmp_path)
    diags = validator.validate_managed_files()
    assert any(d.code == "MANAGED_FILE_MISSING" for d in diags)
