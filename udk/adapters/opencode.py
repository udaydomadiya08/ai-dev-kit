"""
Adapter for OpenCode.
Generates root opencode.json and .opencode/ instructions structure.
"""

from __future__ import annotations

import json
from pathlib import Path

from udk.adapters.base import AgentAdapter, Diagnostic, GenerationContext


class OpenCodeAdapter(AgentAdapter):
    @property
    def id(self) -> str:
        return "opencode"

    @property
    def name(self) -> str:
        return "OpenCode (opencode.json)"

    @property
    def description(self) -> str:
        return "Generates opencode.json and .opencode/ workspace instructions."

    def supported_artifacts(self) -> list[str]:
        return [
            "opencode.json",
            ".opencode/instructions.md",
            ".opencode/safety.md",
        ]

    def generate(self, context: GenerationContext) -> dict[str, str]:
        artifacts: dict[str, str] = {}

        # 1. opencode.json manifest
        config = {
            "$schema": "https://opencode.ai/schema.json",
            "name": context.project_name,
            "version": "1.0.0",
            "profile": context.profile_name,
            "toolkit": {
                "name": "Universal AI Dev Kit",
                "version": context.toolkit_version,
            },
            "instructions": [
                ".opencode/instructions.md",
                ".opencode/safety.md",
            ],
            "commands": context.profile_data.get("commands", {}),
            "conventions": context.profile_data.get("conventions", []),
        }
        artifacts["opencode.json"] = json.dumps(config, indent=2) + "\n"

        # 2. .opencode/instructions.md
        inst_lines = [
            self.banner(),
            f"# {context.project_name} — OpenCode Instructions\n\n",
            "## Core Engineering Principles\n",
            context.principles.strip(),
            "\n\n## Development Workflow\n",
            context.workflow.strip(),
        ]
        artifacts[".opencode/instructions.md"] = "".join(inst_lines).strip() + "\n"

        # 3. .opencode/safety.md
        safety_lines = [
            self.banner(),
            "# OpenCode Safety & Security Policies\n\n",
            context.safety.strip(),
        ]
        artifacts[".opencode/safety.md"] = "".join(safety_lines).strip() + "\n"

        return artifacts

    def validate(self, workspace_root: Path) -> list[Diagnostic]:
        diagnostics = super().validate(workspace_root)
        config_path = workspace_root / "opencode.json"
        if config_path.is_file():
            try:
                data = json.loads(config_path.read_text(encoding="utf-8"))
                if "name" not in data or "instructions" not in data:
                    diagnostics.append(
                        Diagnostic(
                            severity="error",
                            file_path="opencode.json",
                            message="opencode.json missing required 'name' or 'instructions' fields.",
                            code="INVALID_OPENCODE_SCHEMA",
                        )
                    )
            except json.JSONDecodeError as err:
                diagnostics.append(
                    Diagnostic(
                        severity="error",
                        file_path="opencode.json",
                        message=f"opencode.json contains invalid JSON: {err}",
                        code="JSON_DECODE_ERROR",
                    )
                )
        return diagnostics
