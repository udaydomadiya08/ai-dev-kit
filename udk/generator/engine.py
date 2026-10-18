"""
Deterministic generation engine for Universal AI Dev Kit (UDK).
Coordinates canonical knowledge loading, profile resolution, adapter execution,
dry-run preview generation, conflict detection, and manifest updates.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from udk.adapters.base import GenerationContext
from udk.adapters.registry import get_adapter
from udk.manifest import (
    FileRecord,
    Manifest,
    ManifestManager,
    compute_file_sha256,
    compute_sha256,
)


@dataclass
class PlanItem:
    path: str
    action: str  # "create", "update", "conflict", "unchanged"
    content: str
    sha256: str
    generator: str
    reason: str = ""


class GeneratorEngine:
    def __init__(self, workspace_root: Path, canonical_root: Path | None = None):
        self.workspace_root = workspace_root.resolve()
        if canonical_root is None:
            self.canonical_root = Path(__file__).parent.parent / "canonical"
        else:
            self.canonical_root = canonical_root.resolve()
        self.manifest_manager = ManifestManager(self.workspace_root)

    def load_canonical_text(self, rel_path: str) -> str:
        """Loads a canonical markdown file from the canonical directory."""
        target = self.canonical_root / rel_path
        if not target.is_file():
            return ""
        return target.read_text(encoding="utf-8")

    def load_canonical_instructions(self) -> dict[str, str]:
        """Loads all task instructions from canonical/instructions/*.md."""
        inst_dir = self.canonical_root / "instructions"
        instructions: dict[str, str] = {}
        if inst_dir.is_dir():
            for f in sorted(inst_dir.glob("*.md")):
                key = f.stem
                instructions[key] = f.read_text(encoding="utf-8")
        return instructions

    def load_canonical_skills(self) -> dict[str, dict[str, Any]]:
        """Loads all canonical skills from canonical/skills/*/SKILL.md."""
        skills_dir = self.canonical_root / "skills"
        skills: dict[str, dict[str, Any]] = {}
        if not skills_dir.is_dir():
            return skills

        for skill_folder in sorted(skills_dir.iterdir()):
            if not skill_folder.is_dir():
                continue
            skill_file = skill_folder / "SKILL.md"
            if not skill_file.is_file():
                continue

            raw_text = skill_file.read_text(encoding="utf-8")
            metadata, body = self._parse_frontmatter(raw_text)
            skill_id = skill_folder.name
            skills[skill_id] = {
                "metadata": metadata,
                "content": body,
                "path": str(skill_file),
            }
        return skills

    def _parse_frontmatter(self, text: str) -> tuple[dict[str, Any], str]:
        """Extracts YAML-style frontmatter headers from markdown."""
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            return {}, text

        frontmatter_lines = []
        body_lines = []
        in_frontmatter = True
        for line in lines[1:]:
            if in_frontmatter:
                if line.strip() == "---":
                    in_frontmatter = False
                    continue
                frontmatter_lines.append(line)
            else:
                body_lines.append(line)

        meta: dict[str, Any] = {}
        for f_line in frontmatter_lines:
            if ":" in f_line:
                k, v = f_line.split(":", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if v.startswith("[") and v.endswith("]"):
                    # Basic inline list parse
                    items = [
                        i.strip().strip('"').strip("'")
                        for i in v[1:-1].split(",")
                        if i.strip()
                    ]
                    meta[k] = items
                else:
                    meta[k] = v

        return meta, "\n".join(body_lines).strip()

    def build_context(
        self,
        project_name: str | None = None,
        profile_name: str = "minimal",
        profile_data: dict[str, Any] | None = None,
        selected_skills: list[str] | None = None,
    ) -> GenerationContext:
        """Constructs complete GenerationContext from canonical sources."""
        p_name = project_name or self.workspace_root.name or "project"
        if profile_data is None:
            from udk.profiles import get_profile

            prof = get_profile(profile_name)
            p_data = prof.to_dict() if prof else {}
        else:
            p_data = profile_data

        principles = self.load_canonical_text("core/principles.md")
        engineering = self.load_canonical_text("core/engineering.md")
        workflow = self.load_canonical_text("core/workflow.md")
        safety = self.load_canonical_text("core/safety.md")
        instructions = self.load_canonical_instructions()
        all_skills = self.load_canonical_skills()

        # Filter skills if specified
        if selected_skills is not None:
            active_skills = {
                k: v for k, v in all_skills.items() if k in selected_skills
            }
        else:
            active_skills = all_skills

        return GenerationContext(
            workspace_root=self.workspace_root,
            project_name=p_name,
            profile_name=profile_name,
            profile_data=p_data,
            principles=principles,
            engineering=engineering,
            workflow=workflow,
            safety=safety,
            instructions=instructions,
            skills=active_skills,
        )

    def plan(
        self,
        adapter_ids: list[str],
        profile_name: str = "minimal",
        profile_data: dict[str, Any] | None = None,
        selected_skills: list[str] | None = None,
        force: bool = False,
    ) -> list[PlanItem]:
        """
        Produces a deterministic plan of all file operations.
        Performs conflict detection against existing files and manifest records.
        """
        context = self.build_context(
            profile_name=profile_name,
            profile_data=profile_data,
            selected_skills=selected_skills,
        )

        existing_manifest = self.manifest_manager.load()
        existing_files = existing_manifest.files if existing_manifest else {}

        plan_items: list[PlanItem] = []
        seen_paths: set[str] = set()

        for a_id in adapter_ids:
            adapter = get_adapter(a_id)
            if not adapter:
                continue

            generated_files = adapter.generate(context)
            for rel_path, content in generated_files.items():
                if rel_path in seen_paths:
                    continue
                seen_paths.add(rel_path)

                full_path = self.workspace_root / rel_path
                new_hash = compute_sha256(content)

                if not full_path.exists():
                    action = "create"
                    reason = "New file to be created"
                else:
                    disk_hash = compute_file_sha256(full_path)
                    if disk_hash == new_hash:
                        action = "unchanged"
                        reason = "File is up to date"
                    elif rel_path in existing_files:
                        recorded_hash = existing_files[rel_path].sha256
                        if disk_hash == recorded_hash:
                            action = "update"
                            reason = "Managed file updated from toolkit"
                        else:
                            if force:
                                action = "update"
                                reason = "File modified by user, overwrite forced"
                            else:
                                action = "conflict"
                                reason = (
                                    "File modified by user since last UDK generation"
                                )
                    else:
                        if force:
                            action = "create"
                            reason = "Pre-existing unmanaged file, overwrite forced"
                        else:
                            action = "conflict"
                            reason = "Pre-existing unmanaged file conflicts with target"

                plan_items.append(
                    PlanItem(
                        path=rel_path,
                        action=action,
                        content=content,
                        sha256=new_hash,
                        generator=adapter.id,
                        reason=reason,
                    )
                )

        return sorted(plan_items, key=lambda i: i.path)

    def apply(
        self,
        plan_items: list[PlanItem],
        profile_name: str,
        adapter_ids: list[str],
        skills: list[str] | None = None,
    ) -> list[str]:
        """
        Applies plan items to disk.
        Returns list of actually written or updated file paths.
        Updates .udk/manifest.json with new file records.
        """
        written_paths: list[str] = []
        manifest = self.manifest_manager.load() or Manifest()
        manifest.profile = profile_name
        manifest.adapters = adapter_ids
        manifest.skills = skills or []

        for item in plan_items:
            if item.action in ("create", "update"):
                full_path = self.workspace_root / item.path

                # Security check: assert path does not escape workspace
                resolved = full_path.resolve()
                if not str(resolved).startswith(str(self.workspace_root)):
                    raise PermissionError(
                        f"Security violation: path traversal detected '{item.path}'"
                    )

                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(item.content, encoding="utf-8")
                written_paths.append(item.path)

                manifest.files[item.path] = FileRecord(
                    path=item.path,
                    sha256=item.sha256,
                    generator=item.generator,
                    managed=True,
                    customized=False,
                )
            elif item.action == "unchanged":
                # Ensure it's tracked in manifest
                if item.path not in manifest.files:
                    manifest.files[item.path] = FileRecord(
                        path=item.path,
                        sha256=item.sha256,
                        generator=item.generator,
                        managed=True,
                        customized=False,
                    )

        self.manifest_manager.save(manifest)
        return written_paths
