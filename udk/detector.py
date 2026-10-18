"""
Workspace heuristic detector for Universal AI Dev Kit (UDK).
Inspects target directories to identify language ecosystems, project types,
existing agent configs, and recommend suitable profiles and adapters.
"""

from __future__ import annotations

from pathlib import Path


def detect_workspace(workspace_root: Path) -> tuple[str, list[str], dict[str, str]]:
    """
    Analyzes a directory to recommend (recommended_profile, recommended_adapters, detected_markers).
    """
    root = workspace_root.resolve()
    markers: dict[str, str] = {}
    recommended_adapters: list[str] = []

    # Check for existing agent markers
    if (root / "AGENTS.md").is_file():
        markers["agents_md"] = "AGENTS.md"
        recommended_adapters.append("agents-md")
    if (root / "CLAUDE.md").is_file() or (root / ".claude").is_dir():
        markers["claude_code"] = "CLAUDE.md / .claude"
        recommended_adapters.append("claude-code")
    if (root / ".agents").is_dir() or (root / "GEMINI.md").is_file():
        markers["antigravity"] = ".agents / GEMINI.md"
        recommended_adapters.append("antigravity")
    if (root / ".cursorrules").is_file() or (root / ".cursor").is_dir():
        markers["cursor"] = ".cursorrules / .cursor"
        recommended_adapters.append("cursor")
    if (root / "opencode.json").is_file() or (root / ".opencode").is_dir():
        markers["opencode"] = "opencode.json"
        recommended_adapters.append("opencode")

    # Default adapter if none detected
    if not recommended_adapters:
        recommended_adapters.append("agents-md")

    # Check for project type markers
    has_pyproject = (root / "pyproject.toml").is_file()
    has_requirements = (root / "requirements.txt").is_file()
    has_setup_py = (root / "setup.py").is_file()
    has_package_json = (root / "package.json").is_file()
    has_cargo = (root / "Cargo.toml").is_file()
    has_pubspec = (root / "pubspec.yaml").is_file()

    # Detect AI/ML markers
    is_aiml = False
    if has_pyproject:
        markers["python"] = "pyproject.toml"
        try:
            content = (root / "pyproject.toml").read_text(encoding="utf-8").lower()
            if any(
                k in content
                for k in [
                    "torch",
                    "tensorflow",
                    "scikit-learn",
                    "transformers",
                    "huggingface",
                ]
            ):
                is_aiml = True
                markers["ai_ml"] = "AI/ML dependencies in pyproject.toml"
        except OSError:
            pass
    elif has_requirements:
        markers["python"] = "requirements.txt"
        try:
            content = (root / "requirements.txt").read_text(encoding="utf-8").lower()
            if any(
                k in content for k in ["torch", "tensorflow", "sklearn", "transformers"]
            ):
                is_aiml = True
                markers["ai_ml"] = "AI/ML dependencies in requirements.txt"
        except OSError:
            pass

    if is_aiml:
        return "ai-ml", recommended_adapters, markers

    if has_pubspec:
        markers["mobile"] = "pubspec.yaml"
        return "mobile", recommended_adapters, markers

    if has_pyproject or has_requirements or has_setup_py:
        return "python", recommended_adapters, markers

    if has_package_json:
        markers["web"] = "package.json"
        try:
            content = (root / "package.json").read_text(encoding="utf-8").lower()
            if "electron" in content or "tauri" in content:
                markers["desktop"] = "electron/tauri in package.json"
                return "desktop", recommended_adapters, markers
        except OSError:
            pass
        return "web", recommended_adapters, markers

    if has_cargo:
        markers["rust"] = "Cargo.toml"
        return "desktop", recommended_adapters, markers

    # Fallback to minimal
    return "minimal", recommended_adapters, markers
