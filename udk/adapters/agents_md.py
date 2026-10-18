"""
Adapter for the AGENTS.md standard.
Generates a comprehensive, clean, single-source-of-truth AGENTS.md file
in the project root containing project rules, principles, and skills summaries.
"""

from __future__ import annotations

from pathlib import Path

from udk.adapters.base import AgentAdapter, Diagnostic, GenerationContext


class AgentsMdAdapter(AgentAdapter):
    @property
    def id(self) -> str:
        return "agents-md"

    @property
    def name(self) -> str:
        return "AGENTS.md Standard"

    @property
    def description(self) -> str:
        return (
            "Generates root AGENTS.md conforming to the universal AGENTS.md standard."
        )

    def supported_artifacts(self) -> list[str]:
        return ["AGENTS.md"]

    def generate(self, context: GenerationContext) -> dict[str, str]:
        lines: list[str] = [self.banner()]

        # Title & Metadata
        lines.append(f"# AGENTS.md — {context.project_name}\n")
        lines.append(
            f"> Project engineering guidelines, architectural invariants, and agent workflows.  \n"
            f"> Configured with profile: **{context.profile_name}** | UDK Version: {context.toolkit_version}\n"
        )

        # Profile Overview
        p_data = context.profile_data
        desc = p_data.get("description", "Standard development environment")
        lines.append("## 1. Project Overview & Environment\n")
        lines.append(f"{desc}\n")

        commands = p_data.get("commands", {})
        if commands:
            lines.append("### Standard Commands\n")
            lines.append("| Purpose | Command |")
            lines.append("| :--- | :--- |")
            for purpose, cmd in sorted(commands.items()):
                lines.append(f"| **{purpose.capitalize()}** | `{cmd}` |")
            lines.append("")

        conventions = p_data.get("conventions", [])
        if conventions:
            lines.append("### Project Conventions\n")
            for conv in conventions:
                lines.append(f"* {conv}")
            lines.append("")

        # Core Safety Invariants (Layer 1)
        lines.append("## 2. Safety & Security Invariants (Non-Negotiable)\n")
        lines.append(context.safety.strip())
        lines.append("\n")

        # Core Principles (Layer 5)
        lines.append("## 3. Core Engineering Principles\n")
        lines.append(context.principles.strip())
        lines.append("\n")

        # Development Workflow Loop
        lines.append("## 4. Development Workflow & Verification Loop\n")
        lines.append(context.workflow.strip())
        lines.append("\n")

        # Task Instructions
        if context.instructions:
            lines.append("## 5. Task-Specific Instructions\n")
            for task_name, task_content in sorted(context.instructions.items()):
                title = task_name.replace("_", " ").title()
                lines.append(f"### 5.{lines.count('### 5.') + 1} {title}\n")
                lines.append(task_content.strip())
                lines.append("\n")

        # Skills Summary
        if context.skills:
            lines.append("## 6. Reusable Skills Library\n")
            lines.append("| Skill | Summary | Tags |")
            lines.append("| :--- | :--- | :--- |")
            for skill_id, skill_info in sorted(context.skills.items()):
                meta = skill_info.get("metadata", {})
                name = meta.get("name", skill_id)
                summary = meta.get("description", "")
                tags = ", ".join(meta.get("tags", []))
                lines.append(f"| **{name}** | {summary} | `{tags}` |")
            lines.append("\n")

        return {"AGENTS.md": "\n".join(lines).strip() + "\n"}

    def validate(self, workspace_root: Path) -> list[Diagnostic]:
        diagnostics = super().validate(workspace_root)
        target = workspace_root / "AGENTS.md"
        if target.is_file():
            content = target.read_text(encoding="utf-8")
            if "Safety & Security" not in content:
                diagnostics.append(
                    Diagnostic(
                        severity="error",
                        file_path="AGENTS.md",
                        message="AGENTS.md is missing mandatory 'Safety & Security' section.",
                        code="MISSING_SAFETY_SECTION",
                    )
                )
            if "Core Engineering Principles" not in content:
                diagnostics.append(
                    Diagnostic(
                        severity="warning",
                        file_path="AGENTS.md",
                        message="AGENTS.md is missing 'Core Engineering Principles' section.",
                        code="MISSING_PRINCIPLES",
                    )
                )
        return diagnostics
