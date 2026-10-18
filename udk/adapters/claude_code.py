"""
Adapter for Anthropic Claude Code.
Generates a concise, highly focused CLAUDE.md file formatted for Claude Code's
context window conventions and command structure.
"""

from __future__ import annotations

from pathlib import Path

from udk.adapters.base import AgentAdapter, Diagnostic, GenerationContext


class ClaudeCodeAdapter(AgentAdapter):
    @property
    def id(self) -> str:
        return "claude-code"

    @property
    def name(self) -> str:
        return "Claude Code (CLAUDE.md)"

    @property
    def description(self) -> str:
        return "Generates root CLAUDE.md optimized for the Anthropic Claude Code CLI."

    def supported_artifacts(self) -> list[str]:
        return ["CLAUDE.md"]

    def generate(self, context: GenerationContext) -> dict[str, str]:
        lines: list[str] = [self.banner()]

        lines.append(f"# CLAUDE.md — {context.project_name}\n")
        lines.append(
            f"This repository uses **Universal AI Dev Kit** with the **{context.profile_name}** profile.  \n"
            "Claude Code must adhere to these commands, architectural boundaries, and safety invariants.\n"
        )

        # Commands Section (Claude Code prioritizes command references)
        p_data = context.profile_data
        commands = p_data.get("commands", {})
        if commands:
            lines.append("## Build, Test, and Lint Commands\n")
            for purpose, cmd in sorted(commands.items()):
                lines.append(f"- **{purpose.capitalize()}**: `{cmd}`")
            lines.append("")

        # Safety & Non-Negotiable Boundaries
        lines.append("## Safety Invariants & Boundaries\n")
        lines.append(
            "- Never print, expose, or commit secrets, `.env` files, API keys, or private tokens."
        )
        lines.append(
            "- Do not execute destructive filesystem commands (`rm -rf`, destructive resets) without confirmation."
        )
        lines.append("- Never write or touch files outside the project workspace.")
        lines.append(
            "- Do not install unreviewed packages or add unsolicited external dependencies."
        )
        lines.append("")

        # Core Engineering Rules
        lines.append("## Core Engineering Principles\n")
        lines.append(
            "- **Read Before Write**: Always inspect existing code and imports before making changes."
        )
        lines.append(
            "- **Minimal Coherent Edits**: Avoid gratuitous formatting, unsolicited refactoring, or touching unrelated files."
        )
        lines.append(
            "- **Deterministic Verification**: Run automated tests after every edit; never report code works without running tests."
        )
        lines.append(
            "- **Explicit Types & Error Handling**: Avoid bare excepts; handle empty collections, timeouts, and edge cases."
        )
        lines.append("")

        # Project Conventions
        conventions = p_data.get("conventions", [])
        if conventions:
            lines.append("## Code Style & Project Conventions\n")
            for conv in conventions:
                lines.append(f"- {conv}")
            lines.append("")

        # Workflow Instructions
        lines.append("## Operational Workflow\n")
        lines.append(
            "1. **Inspect**: Read target files, existing tests, and project dependencies."
        )
        lines.append("2. **Plan**: Outline changes and identify potential regressions.")
        lines.append(
            "3. **Execute**: Make targeted changes matching repository conventions."
        )
        lines.append(
            "4. **Verify**: Execute the test command above and verify the git diff before completing."
        )
        lines.append("")

        return {"CLAUDE.md": "\n".join(lines).strip() + "\n"}

    def validate(self, workspace_root: Path) -> list[Diagnostic]:
        diagnostics = super().validate(workspace_root)
        target = workspace_root / "CLAUDE.md"
        if target.is_file():
            content = target.read_text(encoding="utf-8")
            if "Build, Test, and Lint Commands" not in content:
                diagnostics.append(
                    Diagnostic(
                        severity="warning",
                        file_path="CLAUDE.md",
                        message="CLAUDE.md is missing command section.",
                        code="MISSING_COMMANDS",
                    )
                )
        return diagnostics
