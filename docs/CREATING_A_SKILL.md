# Guide: Creating a Standard Reusable Skill

This guide explains how to author and publish a new development skill in the **Universal AI Dev Kit** (`udk`).

---

## 1. What Is a Skill?

A **Skill** is a modular, structured capability designed for AI coding agents. Rather than providing vague advice, a skill outlines:
* A precise trigger condition (when to invoke, when NOT to invoke).
* A step-by-step repeatable procedure.
* Explicit safety boundaries.
* Measurable verification criteria.

---

## 2. Standard `SKILL.md` Specification

Every skill lives in its own subdirectory under `udk/canonical/skills/<skill_name>/SKILL.md` and begins with YAML frontmatter:

```markdown
---
name: "skill_name"
description: "A concise, single-sentence summary of what this skill does and when to invoke it."
version: "1.0.0"
tags: ["testing", "workflow", "python"]
---

# Skill: Title of the Skill

## 1. Purpose
Explain the goal of this capability.

## 2. When to Use
* Bulleted list of scenarios when this skill should be activated.

## 3. When NOT to Use
* Bulleted list of scenarios where this skill is inappropriate or overkill.

## 4. Required Inputs
* Necessary information, files, or environment parameters.

## 5. Expected Outputs
* Concrete artifacts produced (e.g. test files, reports, code patches).

## 6. Repeatable Procedure
1. Step-by-step instructions guiding the agent through disciplined execution.
2. Ensure each step has observable checkpoints.

## 7. Safety Boundaries
* Explicit constraints preventing data loss, credential leaks, or unbounded operations.

## 8. Verification Criteria
* How to prove that the skill was executed correctly (e.g. running tests, checking status codes).

## 9. Example
* Realistic walkthrough of a scenario using this skill.

## 10. Known Limitations
* Known edge cases or environments where the skill cannot operate.
```

---

## 3. Automated Validation

After creating your skill, run the automated skill validator test:
```bash
pytest tests/test_skills.py
```
The test suite automatically verifies that:
* YAML frontmatter contains valid `name`, `description`, and `tags`.
* All mandatory sections are present.
* The skill is loadable by the generator engine.
