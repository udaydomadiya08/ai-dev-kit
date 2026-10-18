"""
Tests for UDK Generator Engine: dry-run, plan, conflict detection, and manifest updates.
"""

from __future__ import annotations

from pathlib import Path

from udk.generator.engine import GeneratorEngine
from udk.manifest import ManifestManager


def test_generator_plan_and_dry_run(tmp_path: Path):
    engine = GeneratorEngine(workspace_root=tmp_path)
    plan = engine.plan(adapter_ids=["agents-md", "claude-code"], profile_name="minimal")

    # Verify dry-run: no files written to disk yet
    assert not (tmp_path / "AGENTS.md").exists()
    assert not (tmp_path / "CLAUDE.md").exists()
    assert len(plan) == 2
    assert all(item.action == "create" for item in plan)


def test_generator_apply_and_manifest(tmp_path: Path):
    engine = GeneratorEngine(workspace_root=tmp_path)
    plan = engine.plan(adapter_ids=["agents-md", "claude-code"], profile_name="minimal")
    written = engine.apply(
        plan, profile_name="minimal", adapter_ids=["agents-md", "claude-code"]
    )

    assert len(written) == 2
    assert (tmp_path / "AGENTS.md").is_file()
    assert (tmp_path / "CLAUDE.md").is_file()

    # Verify manifest was created
    mgr = ManifestManager(tmp_path)
    manifest = mgr.load()
    assert manifest is not None
    assert manifest.profile == "minimal"
    assert "AGENTS.md" in manifest.files
    assert "CLAUDE.md" in manifest.files


def test_generator_conflict_detection_on_user_edit(tmp_path: Path):
    engine = GeneratorEngine(workspace_root=tmp_path)
    plan = engine.plan(adapter_ids=["agents-md"], profile_name="minimal")
    engine.apply(plan, profile_name="minimal", adapter_ids=["agents-md"])

    # Simulate developer customizing AGENTS.md
    agents_file = tmp_path / "AGENTS.md"
    agents_file.write_text("Custom user modifications here.\n", encoding="utf-8")

    # Run plan again without force - should detect conflict!
    plan2 = engine.plan(adapter_ids=["agents-md"], profile_name="minimal", force=False)
    assert len(plan2) == 1
    assert plan2[0].action == "conflict"
    assert "modified by user" in plan2[0].reason

    # Run plan with force=True - should allow update
    plan_forced = engine.plan(
        adapter_ids=["agents-md"], profile_name="minimal", force=True
    )
    assert plan_forced[0].action == "update"
