"""
End-to-End Demonstration Workflows for Universal AI Dev Kit (UDK).
Exercises three realistic sample projects:
1. Python CLI starter with Claude Code & AGENTS.md
2. Web application starter with Cursor
3. AI/ML research starter with Google Antigravity
Verifies initialization, validation, test execution, drift detection, and update safety.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from udk.cli import main


def copy_template(template_name: str, dest_dir: Path) -> None:
    src_dir = Path(__file__).parent.parent / "udk" / "templates" / template_name
    assert src_dir.is_dir(), f"Template {template_name} directory not found"
    for item in src_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, dest_dir / item.name)
        elif item.is_dir():
            shutil.copytree(item, dest_dir / item.name)


def test_e2e_python_cli_workflow(tmp_path: Path):
    # 1. Setup workspace with Python CLI starter
    copy_template("python_cli", tmp_path)
    assert (tmp_path / "main.py").is_file()
    assert (tmp_path / "tests" / "test_main.py").is_file()

    # 2. Initialize UDK with python profile and claude-code + agents-md
    ret = main(
        [
            "init",
            "--path",
            str(tmp_path),
            "--profile",
            "python",
            "--agent",
            "claude-code",
            "--agent",
            "agents-md",
        ]
    )
    assert ret == 0
    assert (tmp_path / "CLAUDE.md").is_file()
    assert (tmp_path / "AGENTS.md").is_file()

    # 3. Validate configuration
    ret_val = main(["validate", "--path", str(tmp_path)])
    assert ret_val == 0

    # 4. Run application tests
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.returncode == 0
    assert "passed" in res.stdout

    # 5. Simulate customization & drift
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text("Custom instructions added by developer.\n", encoding="utf-8")

    # 6. Check diff detects modification
    ret_diff = main(["diff", "--path", str(tmp_path)])
    assert ret_diff == 0

    # 7. Update halts on modified file
    ret_up = main(["update", "--path", str(tmp_path)])
    assert ret_up == 1
    # File is preserved
    assert (
        claude_md.read_text(encoding="utf-8")
        == "Custom instructions added by developer.\n"
    )


def test_e2e_web_app_workflow(tmp_path: Path):
    # 1. Setup workspace with web starter
    copy_template("web_minimal", tmp_path)
    assert (tmp_path / "index.html").is_file()
    assert (tmp_path / "app.js").is_file()

    # 2. Initialize with web profile and cursor adapter
    ret = main(
        [
            "init",
            "--path",
            str(tmp_path),
            "--profile",
            "web",
            "--agent",
            "cursor",
        ]
    )
    assert ret == 0
    assert (tmp_path / ".cursorrules").is_file()
    assert (tmp_path / ".cursor" / "rules" / "web.mdc").is_file()

    # 3. Validate
    ret_val = main(["validate", "--path", str(tmp_path)])
    assert ret_val == 0


def test_e2e_aiml_research_workflow(tmp_path: Path):
    # 1. Setup workspace with AI/ML starter
    copy_template("ai_ml_starter", tmp_path)
    assert (tmp_path / "evaluate.py").is_file()

    # 2. Initialize with ai-ml profile and antigravity adapter
    ret = main(
        [
            "init",
            "--path",
            str(tmp_path),
            "--profile",
            "ai-ml",
            "--agent",
            "antigravity",
        ]
    )
    assert ret == 0
    assert (tmp_path / "GEMINI.md").is_file()
    assert (tmp_path / ".agents" / "rules" / "engineering_rules.md").is_file()
    assert (tmp_path / ".agents" / "skills" / "debugging" / "SKILL.md").is_file()

    # 3. Validate
    ret_val = main(["validate", "--path", str(tmp_path)])
    assert ret_val == 0

    # 4. Execute evaluation pipeline
    res = subprocess.run(
        [sys.executable, "evaluate.py", "--seed", "42"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.returncode == 0
    assert "Accuracy:" in res.stdout
