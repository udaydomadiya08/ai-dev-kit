---
name: "doc_maintenance"
description: "Keep technical documentation, READMEs, diagrams, and code comments synchronized with implementation changes."
version: "1.0.0"
tags: ["documentation", "maintenance", "clarity"]
---

# Skill: Documentation Maintenance

## 1. Purpose
Maintain high-quality, truthful, and synchronized documentation across guides, architecture references, and README files alongside code changes.

## 2. When to Use
* Modifying public APIs, CLI commands, or options.
* Adding new adapters, profiles, or skills.
* Releasing a new version or completing a milestone.

## 3. When NOT to Use
* Pure internal refactorings that preserve all interfaces and behavior identically.

## 4. Required Inputs
* Code diff or summary of new capabilities.
* Existing documentation in `README.md` and `docs/`.

## 5. Expected Outputs
* Updated documentation files with accurate command syntax and examples.
* Synchronized `CHANGELOG.md` entries following Keep a Changelog standards.
* Validated relative markdown links and code fences.

## 6. Repeatable Procedure
1. **Identify Drift**: Compare CLI `--help` output and function signatures against documented examples.
2. **Update Guides**: Modify relevant guides in `docs/` (e.g. `GETTING_STARTED.md`, `COMPATIBILITY.md`).
3. **Verify Links & Syntax**: Ensure all internal relative markdown links resolve to existing files.
4. **Update Changelog**: Add human-readable entry to `CHANGELOG.md` under `[Unreleased]` or target version.
5. **Sanity Check Examples**: Execute every documented command in a clean terminal to ensure copy-paste reliability.

## 7. Safety Boundaries
* Never document planned features as currently working.
* Do not delete architectural rationale or decision history when updating guides.

## 8. Verification Criteria
* All code snippets in README and documentation run successfully.
* All markdown links pass link integrity checks.

## 9. Example
* Added `--dry-run` flag to `udk init`: Verified that `README.md` and `docs/PRODUCT_SPECIFICATION.md` demonstrate the flag accurately.

## 10. Known Limitations
* Visual documentation (e.g. screenshots) requires manual review when UI layouts change.
