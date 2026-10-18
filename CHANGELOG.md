# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-18

### Added
- **Canonical Knowledge System**: Universal core engineering principles, instructions, and safety rules.
- **Multi-Agent Adapters**: Deterministic configuration generators for AGENTS.md, Anthropic Claude Code (`CLAUDE.md`), Google Antigravity (`.agents/`), Cursor IDE (`.cursorrules`, `.cursor/rules/`), OpenCode (`opencode.json`), and generic Markdown export.
- **Domain Profiles**: Modular profiles for Python, Web, Desktop, Mobile, AI/ML, and Research.
- **Standardized Skills Library**: 12 core development skills conforming to the `SKILL.md` specification with repeatable procedures, safety boundaries, and verification criteria.
- **CLI Engine (`udk`)**: Full command-line interface supporting `init`, `list`, `validate`, `doctor`, `update`, `diff`, and `remove`.
- **Manifest Tracking**: Cryptographic SHA-256 state tracking in `.udk/manifest.json` ensuring safe non-destructive updates, collision detection, and clean removals.
- **Quality & Security Engine**: Built-in path traversal safeguards, frontmatter schema validation, reference integrity checks, and configuration drift detection.
- **Comprehensive Test Suite**: Automated unit, integration, fixture, safety, and CLI tests.

### Fixed
- **Template Test Import Resolution**: Added static analysis fallbacks in starter template test harnesses (`test_eval.py`, `test_main.py`) to prevent `ModuleNotFoundError` when analyzed directly in IDE environments.
- **Ruff & Pyright Compliance**: Resolved all type-annotation deprecations (`UP006`, `UP035`) and added `[tool.pyright]` configuration for seamless IDE language server resolution.
