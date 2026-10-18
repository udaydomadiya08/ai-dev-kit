"""
Profile management for Universal AI Dev Kit (UDK).
Loads domain profiles from udk/canonical/profiles/ and provides
metadata, commands, conventions, and recommended skill sets.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Profile:
    id: str
    name: str
    description: str
    file_globs: str = "*"
    commands: dict[str, str] = field(default_factory=dict)
    conventions: list[str] = field(default_factory=list)
    recommended_skills: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "file_globs": self.file_globs,
            "commands": self.commands,
            "conventions": self.conventions,
            "recommended_skills": self.recommended_skills,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Profile:
        return cls(
            id=data.get("id", "unknown"),
            name=data.get("name", "Unknown Profile"),
            description=data.get("description", ""),
            file_globs=data.get("file_globs", "*"),
            commands=data.get("commands", {}),
            conventions=data.get("conventions", []),
            recommended_skills=data.get("recommended_skills", []),
        )


class ProfileRegistry:
    def __init__(self, profiles_dir: Path | None = None):
        if profiles_dir is None:
            self.profiles_dir = Path(__file__).parent / "canonical" / "profiles"
        else:
            self.profiles_dir = profiles_dir
        self._profiles: dict[str, Profile] = {}
        self._load_profiles()

    def _load_profiles(self) -> None:
        if not self.profiles_dir.is_dir():
            return
        for file_path in sorted(self.profiles_dir.glob("*.json")):
            try:
                data = json.loads(file_path.read_text(encoding="utf-8"))
                profile = Profile.from_dict(data)
                self._profiles[profile.id] = profile
                # Also allow lookup with underscore/dash interchangeably
                alt_id = profile.id.replace("-", "_")
                if alt_id != profile.id:
                    self._profiles[alt_id] = profile
            except (OSError, json.JSONDecodeError):
                continue

    def get(self, profile_id: str) -> Profile | None:
        norm = profile_id.strip().lower()
        return self._profiles.get(norm) or self._profiles.get(norm.replace("-", "_"))

    def list_all(self) -> list[Profile]:
        # Return unique by id
        unique_ids = set()
        result = []
        for p in self._profiles.values():
            if p.id not in unique_ids:
                unique_ids.add(p.id)
                result.append(p)
        return sorted(result, key=lambda p: p.id)

    def get_ids(self) -> list[str]:
        return sorted({p.id for p in self._profiles.values()})


_GLOBAL_REGISTRY = ProfileRegistry()


def get_profile(profile_id: str) -> Profile | None:
    return _GLOBAL_REGISTRY.get(profile_id)


def list_profiles() -> list[Profile]:
    return _GLOBAL_REGISTRY.list_all()


def get_available_profile_ids() -> list[str]:
    return _GLOBAL_REGISTRY.get_ids()
