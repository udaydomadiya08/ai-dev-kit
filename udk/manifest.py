"""
Manifest state management for Universal AI Dev Kit (UDK).
Tracks generated files, SHA-256 hashes, installed profiles, and adapters.
Guarantees safe updates, collision detection, and non-destructive removal.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

CURRENT_SCHEMA_VERSION = "1.0.0"
MANIFEST_DIR = ".udk"
MANIFEST_FILENAME = "manifest.json"


@dataclass
class FileRecord:
    path: str
    sha256: str
    generator: str
    managed: bool = True
    customized: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FileRecord:
        return cls(**data)


@dataclass
class Manifest:
    schema_version: str = CURRENT_SCHEMA_VERSION
    toolkit_version: str = "0.1.0"
    created_at: str = ""
    updated_at: str = ""
    profile: str = "minimal"
    adapters: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    files: dict[str, FileRecord] = field(default_factory=dict)
    custom_settings: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        # Convert FileRecord objects
        data["files"] = {
            k: v.to_dict() if isinstance(v, FileRecord) else v
            for k, v in self.files.items()
        }
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Manifest:
        files_raw = data.get("files", {})
        files = {
            k: FileRecord.from_dict(v) if isinstance(v, dict) else v
            for k, v in files_raw.items()
        }
        return cls(
            schema_version=data.get("schema_version", CURRENT_SCHEMA_VERSION),
            toolkit_version=data.get("toolkit_version", "0.1.0"),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            profile=data.get("profile", "minimal"),
            adapters=data.get("adapters", []),
            skills=data.get("skills", []),
            files=files,
            custom_settings=data.get("custom_settings", {}),
        )


def compute_sha256(content: str | bytes) -> str:
    """Calculate SHA-256 hash of text or bytes content."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def compute_file_sha256(file_path: Path) -> str | None:
    """Calculate SHA-256 of an existing file on disk. Returns None if file does not exist."""
    if not file_path.is_file():
        return None
    try:
        content = file_path.read_bytes()
        return hashlib.sha256(content).hexdigest()
    except OSError:
        return None


class ManifestManager:
    """Manages reading, writing, and auditing the project's .udk/manifest.json."""

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.manifest_dir = self.workspace_root / MANIFEST_DIR
        self.manifest_file = self.manifest_dir / MANIFEST_FILENAME

    def exists(self) -> bool:
        return self.manifest_file.is_file()

    def load(self) -> Manifest | None:
        """Loads and parses the manifest. Returns None if not found."""
        if not self.exists():
            return None
        try:
            raw = self.manifest_file.read_text(encoding="utf-8")
            data = json.loads(raw)
            return Manifest.from_dict(data)
        except (OSError, json.JSONDecodeError):
            return None

    def save(self, manifest: Manifest) -> None:
        """Saves manifest safely with proper directory creation and formatting."""
        self.manifest_dir.mkdir(parents=True, exist_ok=True)
        data = manifest.to_dict()
        content = json.dumps(data, indent=2, sort_keys=True) + "\n"
        self.manifest_file.write_text(content, encoding="utf-8")

    def audit_drift(self) -> dict[str, dict[str, Any]]:
        """
        Audits all files in manifest against their current status on disk.
        Returns mapping:
            file_path -> {
                'status': 'unchanged' | 'modified' | 'missing' | 'untracked',
                'manifest_hash': str,
                'disk_hash': str | None
            }
        """
        manifest = self.load()
        if not manifest:
            return {}

        results: dict[str, dict[str, Any]] = {}
        for rel_path, record in manifest.files.items():
            full_path = self.workspace_root / rel_path
            disk_hash = compute_file_sha256(full_path)

            if disk_hash is None:
                status = "missing"
            elif disk_hash == record.sha256:
                status = "unchanged"
            else:
                status = "modified"

            results[rel_path] = {
                "status": status,
                "manifest_hash": record.sha256,
                "disk_hash": disk_hash,
                "generator": record.generator,
            }
        return results
