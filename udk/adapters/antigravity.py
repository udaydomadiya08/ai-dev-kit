"""
Adapter for Google Antigravity environment.
Generates .agents/ structure with rules/, skills/, and GEMINI.md.
"""

from __future__ import annotations

from pathlib import Path

from udk.adapters.base import AgentAdapter, Diagnostic, GenerationContext


class AntigravityAdapter(AgentAdapter):
    @property
    def id(self) -> str:
        return "antigravity"

    @property
    def name(self) -> str:
        return "Google Antigravity"

    @property
    def description(self) -> str:
        return (
            "Generates .agents/ workspace structure with rules/, skills/ and GEMINI.md."
        )

    def supported_artifacts(self) -> list[str]:
        return [
            "GEMINI.md",
            ".agents/rules/engineering_rules.md",
            ".agents/rules/safety_rules.md",
        ]

    def generate(self, context: GenerationContext) -> dict[str, str]:
        artifacts: dict[str, str] = {}

        # 1. GEMINI.md in root
        gemini_lines = [
            self.banner(),
            f"# {context.project_name} — Antigravity Agent Guidelines\n",
            f"Configured Profile: **{context.profile_name}** | UDK Version: {context.toolkit_version}\n",
            "## Architecture & Rules Overview\n",
            "This repository uses Universal AI Dev Kit rules located in `.agents/rules/` and modular skills in `.agents/skills/`.\n",
            "### Standard Commands\n",
        ]
        commands = context.profile_data.get("commands", {})
        for purpose, cmd in sorted(commands.items()):
            gemini_lines.append(f"- **{purpose.capitalize()}**: `{cmd}`")
        gemini_lines.append("\n### Safety & Security Policy\n")
        gemini_lines.append(
            "See `.agents/rules/safety_rules.md` for non-negotiable security boundaries.\n"
        )

        artifacts["GEMINI.md"] = "\n".join(gemini_lines).strip() + "\n"

        # 2. .agents/rules/engineering_rules.md
        eng_lines = [
            self.banner(),
            "# Universal Engineering Rules\n",
            context.principles.strip(),
            "\n## Engineering Standards\n",
            context.engineering.strip(),
            "\n## Execution Workflow\n",
            context.workflow.strip(),
        ]
        artifacts[".agents/rules/engineering_rules.md"] = (
            "\n".join(eng_lines).strip() + "\n"
        )

        # 3. .agents/rules/safety_rules.md
        safety_lines = [
            self.banner(),
            "# Workspace Safety & Security Boundaries\n",
            context.safety.strip(),
        ]
        artifacts[".agents/rules/safety_rules.md"] = (
            "\n".join(safety_lines).strip() + "\n"
        )

        # 4. Generate discrete SKILL.md files under .agents/skills/<skill_id>/SKILL.md
        for skill_id, skill_info in sorted(context.skills.items()):
            skill_content = skill_info.get("content", "")
            meta = skill_info.get("metadata", {})
            name = meta.get("name", skill_id)
            desc = meta.get("description", "")
            version = meta.get("version", "1.0.0")
            tags = meta.get("tags", [])
            tag_str = "[" + ", ".join(f'"{t}"' for t in tags) + "]"

            header = (
                "---\n"
                f'name: "{name}"\n'
                f'description: "{desc}"\n'
                f'version: "{version}"\n'
                f"tags: {tag_str}\n"
                "---\n\n"
            )
            rel_path = f".agents/skills/{skill_id}/SKILL.md"
            artifacts[rel_path] = header + self.banner() + skill_content.strip() + "\n"

        return artifacts

    def validate(self, workspace_root: Path) -> list[Diagnostic]:
        diagnostics = super().validate(workspace_root)
        gemini = workspace_root / "GEMINI.md"
        if not gemini.is_file():
            diagnostics.append(
                Diagnostic(
                    severity="warning",
                    file_path="GEMINI.md",
                    message="Antigravity GEMINI.md missing in workspace root.",
                    code="MISSING_GEMINI_MD",
                )
            )
        skills_dir = workspace_root / ".agents" / "skills"
        if skills_dir.is_dir():
            for skill_path in skills_dir.glob("*/SKILL.md"):
                text = skill_path.read_text(encoding="utf-8")
                if not text.startswith("---") and "---" not in text[:150]:
                    diagnostics.append(
                        Diagnostic(
                            severity="error",
                            file_path=str(skill_path.relative_to(workspace_root)),
                            message="SKILL.md missing standard YAML frontmatter header.",
                            code="INVALID_SKILL_FRONTMATTER",
                        )
                    )
        return diagnostics
