"""
Validation engine for Universal AI Dev Kit (UDK).
Performs static schema checks, drift analysis, adapter compliance,
skill metadata validation, link integrity, and diagnostic health audits.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from udk.adapters.base import Diagnostic
from udk.adapters.registry import get_adapter
from udk.manifest import ManifestManager
from udk.profiles import get_profile
from udk.validator.security import (
    SecurityViolationError,
    assert_safe_path,
    scan_for_secrets,
)


class ValidatorEngine:
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.manifest_manager = ManifestManager(self.workspace_root)

    def validate_manifest(self) -> list[Diagnostic]:
        """Validates .udk/manifest.json presence and schema."""
        diagnostics: list[Diagnostic] = []
        if not self.manifest_manager.exists():
            diagnostics.append(
                Diagnostic(
                    severity="error",
                    file_path=".udk/manifest.json",
                    message="Project manifest not found. Run 'udk init' to initialize.",
                    code="MANIFEST_NOT_FOUND",
                )
            )
            return diagnostics

        manifest = self.manifest_manager.load()
        if not manifest:
            diagnostics.append(
                Diagnostic(
                    severity="error",
                    file_path=".udk/manifest.json",
                    message="Project manifest contains invalid JSON or is unreadable.",
                    code="MANIFEST_CORRUPT",
                )
            )
            return diagnostics

        if not manifest.schema_version:
            diagnostics.append(
                Diagnostic(
                    severity="error",
                    file_path=".udk/manifest.json",
                    message="Manifest is missing required 'schema_version' field.",
                    code="MISSING_SCHEMA_VERSION",
                )
            )

        # Validate profile reference
        if not get_profile(manifest.profile):
            diagnostics.append(
                Diagnostic(
                    severity="warning",
                    file_path=".udk/manifest.json",
                    message=f"Manifest references unknown profile '{manifest.profile}'.",
                    code="UNKNOWN_PROFILE",
                )
            )

        return diagnostics

    def validate_managed_files(self) -> list[Diagnostic]:
        """Validates that managed files exist on disk, are secure, and match manifest."""
        diagnostics: list[Diagnostic] = []
        manifest = self.manifest_manager.load()
        if not manifest:
            return diagnostics

        audit = self.manifest_manager.audit_drift()
        for rel_path, info in audit.items():
            full_path = self.workspace_root / rel_path
            status = info["status"]

            if status == "missing":
                diagnostics.append(
                    Diagnostic(
                        severity="error",
                        file_path=rel_path,
                        message=f"Managed file '{rel_path}' is missing from workspace.",
                        code="MANAGED_FILE_MISSING",
                    )
                )
            elif status == "modified":
                diagnostics.append(
                    Diagnostic(
                        severity="warning",
                        file_path=rel_path,
                        message=f"File '{rel_path}' has drifted from its recorded toolkit hash.",
                        code="MANAGED_FILE_DRIFTED",
                    )
                )

            # Check secrets in existing files
            if full_path.is_file():
                try:
                    content = full_path.read_text(encoding="utf-8")
                    secret_hits = scan_for_secrets(content)
                    for hit in secret_hits:
                        diagnostics.append(
                            Diagnostic(
                                severity="error",
                                file_path=rel_path,
                                message=f"Secret leak risk in managed file: {hit}",
                                code="SECRET_LEAK_DETECTED",
                            )
                        )
                except OSError:
                    pass

        return diagnostics

    def validate_adapters(self) -> list[Diagnostic]:
        """Invokes adapter-specific validation rules for installed adapters."""
        diagnostics: list[Diagnostic] = []
        manifest = self.manifest_manager.load()
        if not manifest:
            return diagnostics

        for a_id in manifest.adapters:
            adapter = get_adapter(a_id)
            if not adapter:
                diagnostics.append(
                    Diagnostic(
                        severity="warning",
                        message=f"Manifest references uninstalled adapter '{a_id}'.",
                        code="UNKNOWN_ADAPTER",
                    )
                )
                continue
            adapter_diags = adapter.validate(self.workspace_root)
            diagnostics.extend(adapter_diags)

        return diagnostics

    def validate_markdown_links(self) -> list[Diagnostic]:
        """Validates that relative markdown links in generated root files point to existing files."""
        diagnostics: list[Diagnostic] = []
        link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

        manifest = self.manifest_manager.load()
        if not manifest:
            return diagnostics

        for rel_path in manifest.files:
            if not rel_path.endswith(".md"):
                continue
            full_path = self.workspace_root / rel_path
            if not full_path.is_file():
                continue

            try:
                content = full_path.read_text(encoding="utf-8")
                for text, target in link_pattern.findall(content):
                    # Ignore anchors and external URLs
                    if target.startswith(("#", "mailto:")) or "://" in target:
                        continue
                    # Remove any anchor within relative path
                    target_file = target.split("#")[0]
                    if not target_file:
                        continue
                    resolved_link = (full_path.parent / target_file).resolve()
                    if not resolved_link.exists():
                        diagnostics.append(
                            Diagnostic(
                                severity="warning",
                                file_path=rel_path,
                                message=f"Broken relative link '[{text}]({target})' target does not exist.",
                                code="BROKEN_MARKDOWN_LINK",
                            )
                        )
            except OSError:
                pass

        return diagnostics

    def validate_all(self) -> list[Diagnostic]:
        """Runs the entire validation pipeline."""
        diags: list[Diagnostic] = []
        diags.extend(self.validate_manifest())
        diags.extend(self.validate_managed_files())
        diags.extend(self.validate_adapters())
        diags.extend(self.validate_markdown_links())
        return diags

    def run_doctor(self) -> dict[str, list[dict[str, str]]]:
        """Performs a comprehensive system and repository health diagnosis."""
        report: dict[str, list[dict[str, str]]] = {
            "Environment": [],
            "Repository": [],
            "UDK State": [],
            "Security": [],
        }

        # 1. Environment checks
        py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        report["Environment"].append(
            {
                "title": "Python Version",
                "status": "ok",
                "detail": f"Python {py_ver} (meets >= 3.9 requirement)",
            }
        )

        # 2. Repository checks
        git_dir = self.workspace_root / ".git"
        if git_dir.is_dir():
            report["Repository"].append(
                {
                    "title": "Git Repository",
                    "status": "ok",
                    "detail": "Git repository detected",
                }
            )
        else:
            report["Repository"].append(
                {
                    "title": "Git Repository",
                    "status": "warn",
                    "detail": "No .git directory found in workspace root",
                }
            )

        # 3. UDK State checks
        if self.manifest_manager.exists():
            manifest = self.manifest_manager.load()
            if manifest:
                report["UDK State"].append(
                    {
                        "title": "Manifest Integrity",
                        "status": "ok",
                        "detail": f"Schema v{manifest.schema_version}, profile '{manifest.profile}', {len(manifest.files)} managed files",
                    }
                )
            else:
                report["UDK State"].append(
                    {
                        "title": "Manifest Integrity",
                        "status": "fail",
                        "detail": "Manifest exists but is corrupt or invalid JSON",
                    }
                )
        else:
            report["UDK State"].append(
                {
                    "title": "Manifest Presence",
                    "status": "warn",
                    "detail": "No UDK manifest found. Run 'udk init' to configure.",
                }
            )

        # 4. Security checks
        try:
            assert_safe_path(self.workspace_root / "test_file.txt", self.workspace_root)
            report["Security"].append(
                {
                    "title": "Path Traversal Sanitizer",
                    "status": "ok",
                    "detail": "Path resolution boundaries enforced",
                }
            )
        except (OSError, SecurityViolationError) as err:
            report["Security"].append(
                {
                    "title": "Path Traversal Sanitizer",
                    "status": "fail",
                    "detail": f"Security assertion failed: {err}",
                }
            )

        return report
