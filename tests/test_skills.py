"""
Automated validation of all canonical skills.
Ensures all 12 required skills exist, contain standard YAML frontmatter,
and provide complete, structured procedures and safety boundaries.
"""

from __future__ import annotations

from pathlib import Path

from udk.generator.engine import GeneratorEngine

REQUIRED_SKILLS = [
    "research",
    "requirements",
    "exploration",
    "architecture_review",
    "incremental_impl",
    "debugging",
    "test_planning",
    "code_review",
    "security_review",
    "doc_maintenance",
    "dependency_review",
    "release_prep",
]

REQUIRED_SECTIONS = [
    "Purpose",
    "When to Use",
    "When NOT to Use",
    "Required Inputs",
    "Expected Outputs",
    "Repeatable Procedure",
    "Safety Boundaries",
    "Verification Criteria",
    "Example",
    "Known Limitations",
]


def test_all_canonical_skills_present_and_valid():
    engine = GeneratorEngine(workspace_root=Path("."))
    skills = engine.load_canonical_skills()

    # Verify all 12 skills are found
    for skill_name in REQUIRED_SKILLS:
        assert skill_name in skills, f"Missing required canonical skill: {skill_name}"
        data = skills[skill_name]
        meta = data["metadata"]
        content = data["content"]

        # Check frontmatter fields
        assert "name" in meta, f"Skill '{skill_name}' missing frontmatter 'name'"
        assert "description" in meta, (
            f"Skill '{skill_name}' missing frontmatter 'description'"
        )
        assert len(meta["description"]) > 10, (
            f"Skill '{skill_name}' description is too short"
        )
        assert "tags" in meta, f"Skill '{skill_name}' missing frontmatter 'tags'"
        assert isinstance(meta["tags"], list), (
            f"Skill '{skill_name}' tags must be a list"
        )

        # Check mandatory sections in content
        for sec in REQUIRED_SECTIONS:
            assert f"## {sec}" in content or f"{sec}" in content, (
                f"Skill '{skill_name}' is missing section '{sec}'"
            )
