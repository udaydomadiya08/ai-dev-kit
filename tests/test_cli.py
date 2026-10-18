"""
End-to-end integration tests for UDK CLI subcommands.
Tests init, dry-run, list, diff, update, validate, doctor, and safe removal.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from udk.cli import main


def test_cli_help(capsys):
    with pytest.raises(SystemExit) as excinfo:
        main(["--help"])
    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "Universal AI Dev Kit" in captured.out
    assert "init" in captured.out
    assert "validate" in captured.out


def test_cli_list(capsys):
    ret = main(["list", "all"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "agents-md" in captured.out
    assert "claude-code" in captured.out
    assert "python" in captured.out
    assert "debugging" in captured.out


def test_cli_init_dry_run(tmp_path: Path, capsys):
    ret = main(
        [
            "init",
            "--path",
            str(tmp_path),
            "--profile",
            "python",
            "--agent",
            "agents-md",
            "--dry-run",
        ]
    )
    assert ret == 0
    captured = capsys.readouterr()
    assert "[Dry-run]" in captured.out
    assert not (tmp_path / "AGENTS.md").exists()


def test_cli_init_and_validate(tmp_path: Path, capsys):
    # Initialize python profile with agents-md adapter
    ret = main(
        ["init", "--path", str(tmp_path), "--profile", "python", "--agent", "agents-md"]
    )
    assert ret == 0
    assert (tmp_path / "AGENTS.md").is_file()
    assert (tmp_path / ".udk" / "manifest.json").is_file()

    # Validate passes
    ret_val = main(["validate", "--path", str(tmp_path)])
    assert ret_val == 0
    captured = capsys.readouterr()
    assert "Validation PASSED" in captured.out


def test_cli_diff_and_update(tmp_path: Path, capsys):
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

    # Diff with no changes
    ret_diff = main(["diff", "--path", str(tmp_path)])
    assert ret_diff == 0

    # Modify AGENTS.md
    target = tmp_path / "AGENTS.md"
    target.write_text("Modified by developer\n", encoding="utf-8")

    # Diff should show modified
    ret_diff2 = main(["diff", "--path", str(tmp_path)])
    assert ret_diff2 == 0
    captured = capsys.readouterr()
    assert "MODIFIED" in captured.out

    # Update without force should be blocked
    ret_up = main(["update", "--path", str(tmp_path)])
    assert ret_up == 1

    # Update with force should succeed
    ret_up_force = main(["update", "--path", str(tmp_path), "--force"])
    assert ret_up_force == 0


def test_cli_safe_remove_preserves_user_files(tmp_path: Path):
    main(
        ["init", "--path", str(tmp_path), "--profile", "python", "--agent", "agents-md"]
    )

    # Create a user file
    user_file = tmp_path / "my_script.py"
    user_file.write_text("print('user code')\n", encoding="utf-8")

    # Remove UDK
    ret_rm = main(["remove", "--path", str(tmp_path)])
    assert ret_rm == 0

    # Managed file deleted
    assert not (tmp_path / "AGENTS.md").exists()
    assert not (tmp_path / ".udk").exists()

    # User file remains intact!
    assert user_file.is_file()
    assert user_file.read_text(encoding="utf-8") == "print('user code')\n"


def test_cli_doctor(tmp_path: Path, capsys):
    main(
        ["init", "--path", str(tmp_path), "--profile", "python", "--agent", "agents-md"]
    )
    ret = main(["doctor", "--path", str(tmp_path)])
    assert ret == 0
    captured = capsys.readouterr()
    assert "Python Version" in captured.out
    assert "Manifest Integrity" in captured.out
