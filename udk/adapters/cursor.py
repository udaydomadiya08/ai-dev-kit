"""
Adapter for Cursor IDE.
Generates root .cursorrules and modular .cursor/rules/*.mdc files
with glob targeting and YAML frontmatter.
"""

from __future__ import annotations

from pathlib import Path

from udk.adapters.base import AgentAdapter, Diagnostic, GenerationContext


class CursorAdapter(AgentAdapter):
    @property
    def id(self) -> str:
        return "cursor"

    @property
    def name(self) -> str:
        return "Cursor IDE (.cursorrules / .cursor/rules/)"

    @property
    def description(self) -> str:
        return "Generates root .cursorrules and modular .cursor/rules/*.mdc with glob filtering."

    def supported_artifacts(self) -> list[str]:
        return [
            ".cursorrules",
            ".cursor/rules/engineering.mdc",
            ".cursor/rules/safety.mdc",
        ]

    def generate(self, context: GenerationContext) -> dict[str, str]:
        artifacts: dict[str, str] = {}

        # 1. Root .cursorrules (legacy and fast global fallback)
        cursorrules_lines = [
            self.banner(),
            f"# Cursor Rules — {context.project_name}\n",
            f"# Profile: {context.profile_name} | UDK Version: {context.toolkit_version}\n\n",
            "## Safety Guidelines\n",
            "- Never read, print, or commit API keys, secrets, or .env files.\n",
            "- Do not run destructive commands without permission.\n\n",
            "## Core Engineering\n",
            "- Read existing files and imports before modifying.\n",
            "- Make minimal, coherent edits; keep diffs clean.\n",
            "- Run automated test suite to verify changes.\n\n",
            "## Standard Commands\n",
        ]
        commands = context.profile_data.get("commands", {})
        for purpose, cmd in sorted(commands.items()):
            cursorrules_lines.append(f"- {purpose.capitalize()}: {cmd}\n")
        artifacts[".cursorrules"] = "".join(cursorrules_lines).strip() + "\n"

        # 2. .cursor/rules/engineering.mdc
        eng_mdc = (
            "---\n"
            'description: "Universal engineering standards and workflow"\n'
            'globs: "*"\n'
            "alwaysApply: true\n"
            "---\n\n"
            + self.banner()
            + "# Engineering Principles & Workflow\n\n"
            + context.principles.strip()
            + "\n\n## Workflow Loop\n"
            + context.workflow.strip()
            + "\n"
        )
        artifacts[".cursor/rules/engineering.mdc"] = eng_mdc

        # 3. .cursor/rules/safety.mdc
        safety_mdc = (
            "---\n"
            'description: "Workspace safety, security boundaries, and secrets hygiene"\n'
            'globs: "*"\n'
            "alwaysApply: true\n"
            "---\n\n"
            + self.banner()
            + "# Safety and Security Boundaries\n\n"
            + context.safety.strip()
            + "\n"
        )
        artifacts[".cursor/rules/safety.mdc"] = safety_mdc

        # 4. Profile-specific glob rule if conventions exist
        globs_pattern = context.profile_data.get("file_globs", "*")
        profile_rule_name = f".cursor/rules/{context.profile_name}.mdc"
        profile_rule_content = [
            "---\n",
            f'description: "{context.profile_name.capitalize()} development conventions and commands"\n',
            f'globs: "{globs_pattern}"\n',
            "alwaysApply: false\n",
            "---\n\n",
            self.banner(),
            f"# {context.profile_name.capitalize()} Conventions\n\n",
        ]
        conventions = context.profile_data.get("conventions", [])
        for conv in conventions:
            profile_rule_content.append(f"- {conv}\n")

        if commands:
            profile_rule_content.append("\n## Commands\n")
            for purpose, cmd in sorted(commands.items()):
                profile_rule_content.append(f"- {purpose.capitalize()}: `{cmd}`\n")

        artifacts[profile_rule_name] = "".join(profile_rule_content).strip() + "\n"

        return artifacts

    def validate(self, workspace_root: Path) -> list[Diagnostic]:
        diagnostics = super().validate(workspace_root)
        rules_dir = workspace_root / ".cursor" / "rules"
        if rules_dir.is_dir():
            for mdc in rules_dir.glob("*.mdc"):
                content = mdc.read_text(encoding="utf-8")
                if not content.startswith("---"):
                    diagnostics.append(
                        Diagnostic(
                            severity="error",
                            file_path=str(mdc.relative_to(workspace_root)),
                            message="Cursor rule .mdc file missing YAML frontmatter.",
                            code="MISSING_MDC_FRONTMATTER",
                        )
                    )
        return diagnostics
