# Universal AI Dev Kit (`udk`)

> A production-quality, open-source foundation for AI-assisted software development across coding agents, languages, and IDEs.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-active_development-green.svg)](#)

---

## 1. What Problem Does It Solve?

AI coding assistants (Claude Code, Cursor, Google Antigravity, OpenCode, Codex, GitHub Copilot) are transforming software engineering. However, adopting them across repositories and teams creates new challenges:
* **Fragmented Configurations:** Every tool invents its own instruction format (`CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.agents/rules/`, `opencode.json`). Teams waste time copying and manually maintaining conflicting rules.
* **Vague Prompt Snippets vs. Verifiable Engineering:** Ad-hoc prompts say "write clean code" without providing executable verification, regression prevention, or clear boundaries for destructive actions.
* **Vendor Lock-In:** Workflows built for one editor break when a team member uses a different agent.
* **Silent Overwrites & Messy Cleanup:** Scaffolding tools often blindly overwrite local files with no drift detection, rollback, or safe removal.

**Universal AI Dev Kit (`udk`)** solves this by establishing a **single canonical source of truth** for engineering principles, task instructions, and modular skills. It deterministically compiles these into native configurations for any supported AI coding agent, tracks file ownership with cryptographic manifests, and verifies configurations with automated quality checks.

---

## 2. Who Is It For?

* **Individual Developers & Builders:** Bootstrap any project with battle-tested AI instructions, safe defaults, and structured workflows in seconds.
* **Open-Source Maintainers:** Ensure all external contributors using AI follow the repository's architecture, test suites, and PR standards.
* **Engineering Teams & Tech Leads:** Enforce universal architectural boundaries, security policies, and testing standards across heterogeneous developer environments (Cursor, Claude Code, Antigravity, etc.).
* **Researchers & Students:** Standardize reproducible research, experiment logging, and metric reporting without requiring commercial API subscriptions.

---

## 3. How Does It Differ From a Collection of Prompt Templates?

| Feature | Generic Prompt Templates | Universal AI Dev Kit (`udk`) |
| :--- | :--- | :--- |
| **Source of Truth** | Duplicated across multiple markdown files | **Single canonical source** compiled into target configs |
| **Agent Support** | Hardcoded to one tool format | **Multi-adapter engine** (AGENTS.md, Claude, Cursor, Antigravity, OpenCode) |
| **File Safety** | Overwrites files blindly | **Manifest-backed state tracking (`.udk/manifest.json`)** with drift detection |
| **Verification** | None; manual visual check | **Automated validation engine** (`udk validate`, `udk doctor`) |
| **Modular Profiles** | One-size-fits-all huge prompt | **Domain profiles** (Python, Web, Desktop, Mobile, AI/ML, Research) |
| **Skill Standards** | Freeform text instructions | **Standardized `SKILL.md` format** with inputs, outputs, safety & checks |
| **Removal & Updates** | Manual file hunting | **Clean, non-destructive updates and removal** (`udk update`, `udk remove`) |

---

## 4. Current Status & Supported Agents

UDK distinguishes between verified implementation tiers (see [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md)):

* **AGENTS.md Standard** (`AGENTS.md`): Fully Tested Integration (Tier 1)
* **Google Antigravity** (`.agents/`, `skills/`, `rules/`, `GEMINI.md`): Fully Tested Integration (Tier 1)
* **Anthropic Claude Code** (`CLAUDE.md`, `.claude/`): Validated Configuration Generation (Tier 2)
* **Cursor IDE** (`.cursorrules`, `.cursor/rules/*.mdc`): Validated Configuration Generation (Tier 2)
* **OpenCode** (`opencode.json`, `.opencode/`): Validated Configuration Generation (Tier 2)
* **Generic Markdown Export** (`ai_context.md`): Universal Export (Tier 4)

---

## 5. Installation & Quick Start

### 5.1 Installation
Requires Python 3.9 or newer.

```bash
# Clone the repository
git clone https://github.com/udaydomadiya08/ai-dev-kit.git
cd ai-dev-kit

# Install locally in editable mode
pip install -e .
```

You can also run directly without installing:
```bash
python3 -m udk --help
```

### 5.2 Initialize a Project in 30 Seconds

```bash
# Navigate to your project
cd /path/to/my-project

# Initialize with detected profile and default AGENTS.md adapter
udk init

# Or explicitly select profile and agent adapters:
udk init --profile python --agent claude-code --agent cursor

# Preview what will be created without modifying disk:
udk init --profile web --dry-run
```

### 5.3 Validate and Check Health

```bash
# Verify configuration syntax, skill metadata, and references
udk validate

# Run a complete diagnostic health check
udk doctor
```

### 5.4 Update or Safely Remove

```bash
# Inspect pending updates from toolkit
udk diff

# Apply updates safely (preserves modified files)
udk update

# Cleanly remove toolkit files when needed
udk remove
```

---

## 6. Project Architecture Overview

```
universal-ai-dev-kit/
├── udk/                         # Core Python package & CLI
│   ├── canonical/               # Canonical knowledge source of truth
│   │   ├── core/                # Universal principles, safety & engineering rules
│   │   ├── instructions/        # Task-specific guides (planning, testing, debugging)
│   │   ├── profiles/            # Domain profiles (python, web, ai_ml, etc.)
│   │   └── skills/              # Reusable standardized skills (SKILL.md)
│   ├── adapters/                # Compilers for target agent formats
│   ├── generator/               # Deterministic rendering pipeline
│   ├── validator/               # Schema, drift, security & link validator
│   ├── manifest.py              # Cryptographic manifest manager (.udk/manifest.json)
│   ├── detector.py              # Heuristics for project stack discovery
│   └── cli.py                   # Command-line interface
├── tests/                       # Automated test suite (unit, integration, security)
└── docs/                        # Complete architecture and developer guides
```

---

## 7. Extending UDK

* **Creating a Skill:** See [docs/CREATING_A_SKILL.md](docs/CREATING_A_SKILL.md). Skills use the standard `SKILL.md` format with YAML frontmatter.
* **Adding a Profile:** See [docs/CREATING_A_PROFILE.md](docs/CREATING_A_PROFILE.md). Profiles combine relevant instructions and skills for a stack.
* **Adding an Agent Adapter:** See [docs/ADDING_AN_ADAPTER.md](docs/ADDING_AN_ADAPTER.md). Subclass `AgentAdapter` and implement `generate()`.

---

## 8. Current Limitations

* **Agent Sandboxing:** UDK rules guide agent planning and prevent accidental mistakes, but true sandboxing (preventing arbitrary network/disk access) requires containerization or OS-level controls.
* **Model Differences:** Agents differ in reasoning quality. UDK ensures consistent instructions, but agent execution depends on the underlying LLM's capabilities.

---

## 9. Contributing & Open Source Governance

We welcome contributions! Please see:
* [CONTRIBUTING.md](CONTRIBUTING.md) — Guidelines for code, tests, and documentation.
* [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — Community standards.
* [SECURITY.md](SECURITY.md) — Vulnerability reporting policy.

---

## 10. License

Licensed under the [Apache License, Version 2.0](LICENSE).
