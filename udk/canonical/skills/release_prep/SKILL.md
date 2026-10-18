---
name: "release_prep"
description: "Verify release readiness, audit test suites, update version tags, compile changelogs, and package artifacts safely."
version: "1.0.0"
tags: ["release", "packaging", "operations"]
---

# Skill: Release Preparation

## 1. Purpose
Execute a comprehensive, repeatable release readiness audit ensuring code quality, test verification, documentation completeness, and package integrity before publishing a version.

## 2. When to Use
* Cutting a new release (e.g. `0.1.0`).
* Finalizing a major milestone or release candidate.
* Preparing distribution packages (wheel, sdist).

## 3. When NOT to Use
* Routine daily development commits or experimental branches.

## 4. Required Inputs
* Target release version (SemVer, e.g. `0.1.0`).
* Current git branch and status.
* Full test suite and CI results.

## 5. Expected Outputs
* Validated release package (`dist/`).
* Updated `CHANGELOG.md` with release date and notes.
* Release checklist sign-off report.

## 6. Repeatable Procedure
1. **Clean Tree Verification**: Ensure `git status` has no unexpected untracked files or uncommitted changes.
2. **Execute Full Test Suite**: Run `pytest -v` across all test suites; verify 100% pass rate.
3. **Run Linting & Type Checks**: Run formatting, linting, and typing checks (`ruff`, `mypy`).
4. **Audit Changelog**: Verify all new features and bug fixes since last tag are recorded in `CHANGELOG.md`.
5. **Version Bump**: Update version string in `pyproject.toml` and internal metadata.
6. **Package Verification**: Build distribution packages (`python -m build` or `pip wheel`) and test installation in a clean virtual environment.
7. **Tag & Publish Guidance**: Prepare git tag command (e.g. `git tag -a v0.1.0 -m "Release v0.1.0"`) and verify that release instructions are documented.

## 7. Safety Boundaries
* Never push git tags or publish packages to PyPI automatically without explicit user authorization.
* Do not release with failing or skipped tests.

## 8. Verification Criteria
* Clean virtual environment installs the built package and executes `udk --help` without error.
* All CI workflows pass on all matrix targets.

## 9. Example
* Pre-release audit for `v0.1.0`: Ran full suite of 11+ tests; confirmed zero defects; updated `CHANGELOG.md`; verified `pyproject.toml` metadata.

## 10. Known Limitations
* Publishing permissions (PyPI tokens, GitHub release keys) must be managed securely by the repository owner outside the agent environment.
