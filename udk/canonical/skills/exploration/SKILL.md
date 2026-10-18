---
name: "exploration"
description: "Map repository architecture, key entry points, test harnesses, and dependencies safely without modifying files."
version: "1.0.0"
tags: ["exploration", "architecture", "discovery"]
---

# Skill: Repository Exploration

## 1. Purpose
Rapidly analyze an unfamiliar repository or codebase to identify entry points, package manifests, build scripts, test suites, and internal dependencies prior to making changes.

## 2. When to Use
* Initializing UDK in an existing repository.
* Onboarding an AI coding agent to a new project.
* Investigating an unfamiliar subsystem before debugging or refactoring.

## 3. When NOT to Use
* Working in a small, single-file script where all context is already visible.

## 4. Required Inputs
* Workspace root path.
* Optional query focus (e.g. "find where auth tokens are validated").

## 5. Expected Outputs
* Repository inventory: languages, frameworks, package managers, and configuration files.
* Map of primary entry points (`main()`, routers, CLI handlers).
* Confirmed test commands and execution procedures.

## 6. Repeatable Procedure
1. **Root Inspection**: Scan root directory for manifest markers (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `Makefile`, etc.).
2. **Directory Topology**: Identify source directories (`src/`, `lib/`, `pkg/`) vs test directories (`tests/`, `spec/`).
3. **Build & Test Discovery**: Read CI workflows (`.github/workflows/`) to discover how tests and linters are invoked.
4. **Targeted Search**: Use ripgrep or file search to locate core interfaces and entry points.
5. **Document Map**: Summarize discovered architecture and test commands for the active task.

## 7. Safety Boundaries
* Exploration is read-only. Never modify, rename, or delete files during an exploration pass.
* Never read or print sensitive files (`.env`, secrets, private keys).

## 8. Verification Criteria
* Discovered test commands run successfully and exit with verifiable status.
* Identified module paths exist and match current imports.

## 9. Example
* **Target Repo**: Discovers `pyproject.toml` using `setuptools`, tests located in `tests/`, test runner is `pytest`. Concludes `python` profile is appropriate.

## 10. Known Limitations
* Massive monorepos require scoped exploration of relevant sub-packages to avoid context window exhaustion.
