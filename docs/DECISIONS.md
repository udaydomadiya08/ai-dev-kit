# Architecture Decision Records (ADRs)

**Project:** Universal AI Dev Kit (`universal-ai-dev-kit`)  
**Status:** Living Record of Architecture Decisions  

---

## ADR-001: Language and Runtime Selection for UDK Engine

### Context
We need an implementation language for the UDK command-line tool, validation engine, and configuration compiler. The tool must run seamlessly across macOS, Linux, and Windows; install easily in developer environments; require minimal maintenance overhead; and feature strong standard library file, hash, and JSON processing.

### Decision
We choose **Python 3.10+** as the primary implementation language for the UDK core.
* Packaging: Standard `pyproject.toml` (PEP 621).
* Zero mandatory runtime dependencies for the core compiler and validation engine.
* Fast execution with standard library (`argparse`, `pathlib`, `hashlib`, `json`, `dataclasses`, `typing`).

### Status
Accepted.

### Consequences
* Developers can install `udk` via `pip install -e .` or run directly with `python3 -m udk`.
* No heavy binary builds or external node daemon required.
* Near-instantaneous execution (< 100ms) for validation and generation.

---

## ADR-002: Canonical Single-Source-of-Truth Architecture

### Context
Different AI coding agents expect instructions in different files and formats (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.agents/skills/`, etc.). If engineering teams manually maintain separate instruction files, rules inevitably drift, contradict each other, and cause inconsistent agent behavior.

### Decision
Maintain all engineering principles, workflow instructions, project profiles, and skills in a **canonical format** inside the toolkit repository. All agent-specific configurations are deterministically compiled from these canonical sources.
* Developers edit the canonical sources or provide project overrides.
* Agent files are generated artifacts marked with clear headers.

### Status
Accepted.

### Consequences
* Eliminates configuration drift.
* Changes to security or testing policies propagate cleanly across all configured agent adapters.

---

## ADR-003: Standard Skill Specification Format (`SKILL.md`)

### Context
Agent skills are reusable workflows. Different tools specify skills in slightly different ways, but the emerging standard uses markdown files with YAML frontmatter specifying `name` and `description`.

### Decision
Adopt the standard `SKILL.md` specification:
```markdown
---
name: skill-name
description: A concise summary of what this skill does and when to invoke it.
version: 1.0.0
tags: [tag1, tag2]
---
# Skill Title
...
```
Skills will contain explicit sections: *Purpose*, *When to Use*, *When Not to Use*, *Required Inputs*, *Expected Outputs*, *Procedure*, *Safety Boundaries*, and *Verification*.

### Status
Accepted.

### Consequences
* Fully compatible with Google Antigravity, OpenCode, and easily embedded or inlined for Claude Code and Cursor.

---

## ADR-004: Manifest State Management and Drift Detection

### Context
Tools that scaffold files often overwrite developer changes or leave orphaned files upon removal. We must guarantee that UDK is safe to adopt and safe to remove.

### Decision
Record all created files, their SHA-256 content hashes, installed profiles, and adapters in `.udk/manifest.json`.
* `udk update` checks the current file hash against the recorded hash. If the user edited a file, UDK marks it as modified and preserves user work.
* `udk remove` strictly deletes files listed in the manifest and warns if files have been modified.

### Status
Accepted.

### Consequences
* Safe-by-default operation.
* Zero risk of silent data loss.

---

## ADR-005: Security Policy & Path Isolation

### Context
Filesystem generators face potential risks from path traversal (e.g. `../../etc/passwd`) or untrusted external skills containing malicious shell scripts.

### Decision
Enforce strict security guardrails:
1. All file paths resolved through `os.path.realpath` and strictly asserted to be within the target project root.
2. The toolkit never automatically executes scripts located inside skills during initialization or validation.
3. Instructions generated for agents explicitly declare that prompt rules guide behavior, but true sandboxing must be enforced by host permissions.

### Status
Accepted.

---

## ADR-006: Deterministic, Offline Compilation

### Context
Some developer tools require calling remote cloud endpoints or running live LLM calls just to generate configuration files or validate project syntax.

### Decision
All generation, profile application, and schema validation must execute 100% locally and offline without requiring network connectivity, API keys, or model inference tokens.

### Status
Accepted.

### Consequences
* Highly reliable in CI/CD pipelines and air-gapped environments.
* Predictable, reproducible test suites.
