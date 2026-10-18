"""
Automated unit tests for UDK Profile management and independent selection.
"""

from __future__ import annotations

from pathlib import Path

from udk.generator.engine import GeneratorEngine
from udk.profiles import (
    get_available_profile_ids,
    get_profile,
    list_profiles,
)

EXPECTED_PROFILES = [
    "python",
    "web",
    "desktop",
    "mobile",
    "ai-ml",
    "research",
    "minimal",
]


def test_all_expected_profiles_registered():
    profile_ids = get_available_profile_ids()
    for pid in EXPECTED_PROFILES:
        assert pid in profile_ids, f"Profile '{pid}' is not registered"

    all_profiles = list_profiles()
    assert len(all_profiles) >= len(EXPECTED_PROFILES)
    for p in all_profiles:
        assert p.id
        assert p.name
        assert p.description
        assert p.file_globs
        assert len(p.conventions) > 0


def test_independent_profile_generation(tmp_path: Path):
    """Verify that every profile generates valid configurations independently."""
    engine = GeneratorEngine(workspace_root=tmp_path)

    for pid in EXPECTED_PROFILES:
        profile = get_profile(pid)
        assert profile is not None

        plan = engine.plan(
            adapter_ids=["agents-md", "cursor"],
            profile_name=pid,
        )

        assert len(plan) >= 2
        paths = [item.path for item in plan]
        assert "AGENTS.md" in paths
        assert ".cursorrules" in paths

        # Find AGENTS.md content
        agents_item = next(item for item in plan if item.path == "AGENTS.md")
        assert profile.name in agents_item.content or pid in agents_item.content
