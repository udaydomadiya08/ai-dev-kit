# Product Specification: Universal AI Dev Kit (UDK)

**Document Version:** 1.0.0  
**Status:** Approved Architectural Baseline  
**Project Slug:** `universal-ai-dev-kit`  
**Command Line Binary:** `udk`  

---

## 1. Product Mission & Vision

The **Universal AI Dev Kit** (`universal-ai-dev-kit` / `udk`) is an open-source, vendor-neutral toolkit that equips software development repositories with a rigorous, verifiable engineering foundation for AI coding agents. 

Rather than relying on unvetted prompt snippets, ad-hoc system instructions, or proprietary IDE formats, UDK provides:
1. **A canonical, versioned single source of truth** for engineering principles, architectural boundaries, coding standards, and safety invariants.
2. **Deterministic adapters** that compile this canonical knowledge into native configurations for leading AI coding agents (including `AGENTS.md`, Claude Code, Google Antigravity, Cursor, OpenCode, and Codex).
3. **Modular domain profiles** (Python, Web, Desktop, Mobile, AI/ML, Research) providing contextual guidelines without forcing unrelated stacks onto projects.
4. **Reusable, verifiable development skills** (debugging, test planning, security review, etc.) formatted according to standard agent skill specifications.
5. **A safe, non-destructive CLI** for initializing, inspecting, validating, updating, and removing AI development configurations.

---

## 2. Intended Users & Personas

1. **Individual Builders & Open-Source Maintainers**:
   * Need consistent engineering discipline (testing, changelogs, safe refactoring) applied by AI agents without writing custom prompts for each contributor's editor.
2. **Engineering Organizations & Tech Leads**:
   * Need organization-wide architectural and security guardrails enforced across diverse IDEs (some developers use Cursor, others use Claude Code or Antigravity).
3. **Students & Researchers**:
   * Need rigorous reproducibility standards, experiment logging, and safe execution boundaries without getting locked into a commercial LLM subscription.

---

## 3. Primary Workflows

### 3.1 Project Initialization (`udk init`)
* Developer runs `udk init` (or with options like `--profile python --agent claude-code`).
* UDK detects existing project files (e.g. `pyproject.toml`, `package.json`), proposes appropriate profiles and adapters.
* UDK displays a diff/plan of files to be created.
* Upon confirmation (or automatically in `--non-interactive` mode), generates canonical resources and target agent configurations.
* Records state and cryptographic hashes into `.udk/manifest.json`.

### 3.2 Health Check & Audit (`udk doctor`)
* Verifies environment prerequisites, detects broken references, missing files, or out-of-sync generated configs.

### 3.3 Rule & Config Validation (`udk validate`)
* Validates schema compliance of `.udk/manifest.json`, checks `SKILL.md` frontmatter validity, tests for broken file links, and scans for unmanaged drift or path traversal vulnerabilities.

### 3.4 Safe Updates (`udk update` / `udk diff`)
* When toolkit rules or canonical templates are updated, `udk diff` shows exact changes.
* `udk update` regenerates target configs while preserving user-customized sections.

### 3.5 Clean Removal (`udk remove`)
* Reliably removes files managed by UDK using `.udk/manifest.json`.
* Halts and requests authorization if a managed file was edited by the user, and never touches unmanaged user source code.

---

## 4. Non-Goals

1. **Not a Model Provider or LLM Proxy**: UDK does not host models, bill for tokens, or proxy API keys.
2. **Not an IDE or Chat Interface**: UDK configures existing editors and CLI agents rather than building an alternative UI.
3. **Not an Unsupervised Autonomous Daemon**: UDK does not run in the background executing arbitrary shell commands without user oversight.
4. **Not a Proprietary Lock-in Ecosystem**: All output files are plain text Markdown and standard config formats that function even if UDK is uninstalled.

---

## 5. Functional Requirements

* **FR-1: Canonical Knowledge Representation**: Must store engineering principles, safety policies, and workflow instructions in modular Markdown files under a central repository directory.
* **FR-2: Target Agent Adapters**: Must provide deterministic compilation from canonical knowledge into:
  * AGENTS.md standard (`AGENTS.md`)
  * Anthropic Claude Code (`CLAUDE.md`, `.claude/`)
  * Google Antigravity (`.agents/`, `rules/`, `skills/`)
  * Cursor IDE (`.cursorrules`, `.cursor/rules/*.mdc`)
  * OpenCode (`opencode.json`, `.opencode/`)
  * Generic Markdown export for custom tools.
* **FR-3: Modular Project Profiles**: Must support independent selection of stack profiles (`python`, `web`, `desktop`, `mobile`, `ai-ml`, `research`, `minimal`).
* **FR-4: Standardized Skills Library**: Must provide a standard library of at least 12 reusable development skills conforming to the `SKILL.md` specification.
* **FR-5: State Manifest Tracking**: Must record installed profiles, adapters, files, and content hashes in `.udk/manifest.json`.
* **FR-6: Non-Destructive Operations**: Must provide dry-run (`--dry-run`), conflict detection, and backup mechanisms before modifying files.
* **FR-7: Drift & Collision Detection**: Must detect when generated files have been modified manually by the user, providing a diff and resolution options.
* **FR-8: Standalone Portability**: Generated instruction files must be readable and functional without requiring the `udk` binary at agent runtime.
* **FR-9: Extensibility via Custom Profiles/Skills**: Users must be able to define custom skills in `.udk/custom_skills/` and have them included in generation.
* **FR-10: Automated Project Detection**: Must inspect workspace indicators (`package.json`, `pyproject.toml`, `Cargo.toml`, etc.) to recommend appropriate profiles.

---

## 6. Non-Functional Requirements

* **NFR-1 (Determinism)**: Given identical canonical source files and options, adapters must produce byte-for-byte identical output across platforms.
* **NFR-2 (Zero Runtime Overhead)**: Core CLI operations (`init`, `validate`, `diff`) must execute in under 200ms on modern hardware without remote network calls.
* **NFR-3 (Minimal Dependencies)**: The core toolkit must use standard library Python (>= 3.10) with zero mandatory compiled dependencies for core functions.
* **NFR-4 (Cross-Platform Compatibility)**: Must fully operate on macOS, Linux, and Windows with proper handling of path separators and line endings.
* **NFR-5 (Test Coverage & Verifiability)**: Core generation, adapters, validation, and CLI commands must be backed by automated unit and integration tests.
* **NFR-6 (Security & Safety)**: Must enforce strict path sanitization, prohibit arbitrary shell execution during validation, and guide agents with explicit safety boundaries.

---

## 7. Threat Model & Security Principles

| Threat Vector | Potential Impact | UDK Architectural Mitigation |
| :--- | :--- | :--- |
| **Path Traversal Attacks** | Malicious skill or profile attempting to write files to `/etc/` or `~/.ssh/`. | Strict path normalization; all target paths verified to reside strictly within target project root. |
| **Untrusted Code Execution** | Skill containing executable scripts run without review. | UDK never automatically executes scripts in skills. Scripts are isolated and explicitly flagged for user inspection. |
| **Secret Exfiltration** | Prompts instructing agents to dump `.env` files or API keys. | Core safety instructions explicitly forbid agents from reading, logging, or transmitting secret files and credentials. |
| **Accidental Data Loss** | Toolkit overwriting existing project documentation or code. | Manifest-driven ownership; file collision checks; automatic diff preview; refusal to overwrite without confirmation. |
| **Agent Hallucination of Permissions** | Agent assuming instructions give it OS root privileges. | Explicit documentation in all generated rules: *Instructions guide agent behavior, but true security boundaries must be enforced by OS permissions and containerization.* |

---

## 8. Versioning & Lifecycle Strategy

* **Semantic Versioning (SemVer 2.0.0)**: Releases follow `MAJOR.MINOR.PATCH`.
  * Major: Breaking changes to canonical schema or manifest structure requiring migration.
  * Minor: New skills, profiles, or adapters added in backward-compatible manner.
  * Patch: Bug fixes, template improvements, and documentation fixes.
* **Manifest Schema Versioning**: The `.udk/manifest.json` file contains a `schema_version` key (`1.0.0`) enabling automated schema migration.
