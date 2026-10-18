"""
Generic Markdown export adapter for Universal AI Dev Kit (UDK).
Produces a portable single-file ai_context.md that can be consumed by any
custom LLM, IDE, or agent script.
"""

from __future__ import annotations

from udk.adapters.base import AgentAdapter, GenerationContext


class GenericExportAdapter(AgentAdapter):
    @property
    def id(self) -> str:
        return "generic"

    @property
    def name(self) -> str:
        return "Generic Markdown Export"

    @property
    def description(self) -> str:
        return "Generates portable ai_context.md suitable for any custom LLM or agent."

    def supported_artifacts(self) -> list[str]:
        return ["ai_context.md"]

    def generate(self, context: GenerationContext) -> dict[str, str]:
        lines: list[str] = [self.banner()]

        lines.append(f"# AI Context & Engineering Guidance — {context.project_name}\n")
        lines.append(
            f"Universal AI Dev Kit export. Profile: **{context.profile_name}** | Version: {context.toolkit_version}\n"
        )

        lines.append("## 1. Safety and Security Rules\n")
        lines.append(context.safety.strip())
        lines.append("\n")

        lines.append("## 2. Core Principles\n")
        lines.append(context.principles.strip())
        lines.append("\n")

        lines.append("## 3. Workflow & Verification\n")
        lines.append(context.workflow.strip())
        lines.append("\n")

        commands = context.profile_data.get("commands", {})
        if commands:
            lines.append("## 4. Standard Commands\n")
            for purpose, cmd in sorted(commands.items()):
                lines.append(f"- **{purpose.capitalize()}**: `{cmd}`")
            lines.append("")

        return {"ai_context.md": "\n".join(lines).strip() + "\n"}
