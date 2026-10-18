# Ecosystem Research & Analysis: AI Dev Tooling Standards

**Document Version:** 1.0.0  
**Date Checked:** 2026-10-18  
**Scope:** Canonical instructions, agent conventions, skill specifications, adapter targets, and MCP protocol integration.

---

## 1. Standards and Projects Investigated

### 1.1 AGENTS.md Standard
* **Source/Reference:** [https://github.com/agentsmd/agents.md](https://github.com/agentsmd/agents.md)
* **Status & License:** Public Community Specification / Permissive.
* **Core Convention:**
  * Root file: `AGENTS.md`.
  * Hierarchy: Optional sub-directory `AGENTS.md` files scoped to subtrees.
  * Format: Standard Markdown. Often split into sections: *Project Overview*, *Setup & Build*, *Coding Standards*, *Testing & Verification*, and *Security Guidelines*.
* **Strengths:** Universal, plain text, human-readable, model-agnostic, low cognitive load.
* **Limitations:** Lacks built-in declarative schema for executable tool integrations or hook registries without proprietary extensions.

### 1.2 Anthropic Claude Code (`CLAUDE.md` and Skills)
* **Source/Reference:** [https://github.com/anthropics/claude-code](https://github.com/anthropics/claude-code) / Anthropic Documentation
* **Status & License:** Active official CLI / Commercial & Permissive CLI ecosystems.
* **Core Convention:**
  * Project Instructions: `CLAUDE.md` in repository root (or parent directories). Sub-directories can contain scoped `CLAUDE.md`.
  * Config & State: `.claude/config.json` or `.claude/` for persistent session state.
  * Custom Skills/Commands: Noted in `CLAUDE.md` or `.claude/commands/`.
* **Strengths:** Highly respected by Claude agents; prioritized in context window; focuses on build, lint, test, and style commands.
* **Limitations:** Highly tailored to Claude CLI; proprietary command structures; doesn't natively parse custom agent schema declarations from other vendors.

### 1.3 Google Antigravity
* **Source/Reference:** Built-in IDE & Agent Environment Specifications (`.agents/`, `skills/`, `rules/`, `mcp_config.json`, `hooks.json`).
* **Core Convention:**
  * Workspace root: `.agents/` or root `GEMINI.md` / `AGENTS.md`.
  * Skills directory: `skills/<skill_name>/SKILL.md` containing YAML frontmatter (`name`, `description`) and structured markdown procedures.
  * Rules directory: `rules/*.md` or root instructions.
  * Workflows: `workflows/*.md` for task guides.
  * Tools / MCP: `mcp_config.json` defining MCP servers and environment bindings.
* **Strengths:** Formalized `SKILL.md` format with clear metadata, scoped rules, automated tool discovery, and sidecar workflow support.
* **Limitations:** Specific folder hierarchy (`.agents/skills/...`); requires clean translation when sharing skills with flatter systems.

### 1.4 OpenAI Codex & ChatGPT Coding Projects
* **Source/Reference:** [https://github.com/openai/skills](https://github.com/openai/skills) / OpenAI documentation
* **Core Convention:**
  * System prompt guidance / Workspace guidance: `.codex/` directory, `codex.md` or root `AGENTS.md`.
  * Skills repository conventions: Modular skills with instructions, reference inputs, and scripts.
* **Strengths:** Broad community adoption; clean separation between prompt context and execution scripts.
* **Limitations:** Historically lacked a single uniform file naming standard across all web vs. CLI interfaces until AGENTS.md convergence.

### 1.5 Cursor IDE Rules
* **Source/Reference:** Cursor Documentation & `.cursorrules` / `.cursor/rules/*.mdc`
* **Core Convention:**
  * Legacy: Single root `.cursorrules` plain text file.
  * Modern: `.cursor/rules/<rule-name>.mdc` files containing frontmatter (`description`, `globs`, `alwaysApply`) and markdown body.
* **Strengths:** File glob pattern targeting (e.g., apply `react-rules.mdc` only when editing `*.tsx` files), high adoption among frontend/fullstack developers.
* **Limitations:** Proprietary metadata headers (`globs: *.ts`, `alwaysApply: false`); cannot be consumed raw by terminal CLI agents without adaptation.

### 1.6 OpenCode
* **Source/Reference:** [https://github.com/anomalyco/opencode](https://github.com/anomalyco/opencode)
* **Core Convention:**
  * Configuration: `opencode.json` in workspace root.
  * Agent instructions: `.opencode/` containing task instructions, tools, and profile configurations.
* **Strengths:** Transparent JSON-driven agent orchestration, open-source first.
* **Limitations:** Distinct configuration schema requiring translation from markdown principles.

### 1.7 Model Context Protocol (MCP)
* **Source/Reference:** [https://github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
* **Core Convention:**
  * JSON-RPC 2.0 based protocol over stdio or SSE.
  * Configuration files: `mcp.json` or `mcp_config.json` defining servers: `{"mcpServers": { "<name>": {"command": "...", "args": [...], "env": {...}}}}`.
* **Strengths:** Open standard supported across Claude Code, Antigravity, Cursor, and extensible tooling.
* **Limitations:** Focuses strictly on server/tool execution; does not specify prompt guidelines, coding standards, or skill workflows.

---

## 2. Comparison Matrix

| Standard / Target | Primary Instruction File | Modular Rules / Skills Format | Metadata Format | Glob Scoping Support |
| :--- | :--- | :--- | :--- | :--- |
| **AGENTS.md** | `AGENTS.md` | Nested `AGENTS.md` in subdirs | Markdown Headings | No (Directory hierarchy) |
| **Claude Code** | `CLAUDE.md` | `.claude/commands/` or inline | Plain Markdown | No (Directory hierarchy) |
| **Google Antigravity** | `GEMINI.md` / `AGENTS.md` | `.agents/skills/<name>/SKILL.md` | YAML Frontmatter | Yes (Rule definitions) |
| **Cursor** | `.cursorrules` | `.cursor/rules/*.mdc` | YAML Frontmatter (`globs`) | Yes (`globs: pattern`) |
| **OpenCode** | `opencode.json` | `.opencode/agents/`, `.opencode/skills/` | JSON Configuration | Manifest-based |
| **OpenAI / Generic** | `AGENTS.md` / `codex.md` | `skills/<name>/` | YAML / Markdown | Directory hierarchy |

---

## 3. Reusable Design Ideas Adopted

1. **Canonical Single Source of Truth**:
   * Maintain principles, instructions, and skills in a neutral, highly structured canonical format (`udk/core/`, `udk/instructions/`, `udk/skills/`).
   * Never require developers to manually edit 5 different agent configuration files when an engineering policy changes.
2. **Standard Skill Specification (`SKILL.md`)**:
   * Adopt the standard YAML frontmatter pattern:
     ```markdown
     ---
     name: skill-name
     description: "Clear, single-sentence summary of what the skill accomplishes and when to trigger it."
     version: "1.0.0"
     tags: ["testing", "python"]
     ---
     # Skill Procedure
     ...
     ```
   * This is compatible with Antigravity, OpenCode, and adaptable to Claude Code and Cursor.
3. **Glob-Aware Adapter Generation**:
   * When compiling to Cursor, generate `.cursor/rules/*.mdc` with proper `globs: ...` headers.
   * When compiling to AGENTS.md / CLAUDE.md, concatenate or link relevant sections clearly with identifiable sections.
4. **Deterministic & Reversible Generation**:
   * Generated files must include a machine-readable banner identifying them as managed by UDK, with the generator version and canonical source hash.
   * Developers must be able to eject, customize, or update safely without losing local changes.

---

## 4. Approaches Deliberately Rejected

1. **Heavyweight Agent Runtime / Daemon**:
   * *Rejected*: Building our own Python-based background LLM execution daemon.
   * *Rationale*: Violates product principle 2.4 (Progressive Complexity) and 2.1 (Model Independence). The toolkit's role is to provide the standard engineering foundation and configuration for agents, not to reinvent Claude Code, Cursor, or Antigravity.
2. **Proprietary Configuration Format**:
   * *Rejected*: Inventing a new `.udk-custom-binary` or non-standard syntax.
   * *Rationale*: Open standards, plain markdown, standard YAML frontmatter, and standard JSON are transparent, diff-friendly, and universally understood.
3. **Mandatory MCP Server Requirement**:
   * *Rejected*: Forcing every project to launch an MCP server just to read rules.
   * *Rationale*: Static files (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`) are 100% reliable, zero-latency, and work even in offline/airgapped environments. MCP should be an optional capability module.
4. **Silent Overwriting of Unrecognized Files**:
   * *Rejected*: Blindly replacing existing `AGENTS.md` or `.cursorrules` on `init`.
   * *Rationale*: Safe-by-default engineering requires conflict detection, diff previews, backup creation, or explicit flag requirements (`--force`).

---

## 5. Licensing and Attribution Considerations

* **Toolkit License**: Apache-2.0 is proposed and selected. Permissive, patent-granting, industry-standard for developer toolkits.
* **Third-Party Content**:
  * Any skill conventions or specification structures studied are public technical formats.
  * All markdown instructions, principles, adapter logic, and templates are written originally for this project to maintain clean provenance.
  * No code or copyrighted prose was lifted from proprietary codebases.

---

## 6. Architectural Implications for Universal AI Dev Kit

1. **Core Package (`udk`)**:
   * Lightweight Python package with zero required external runtime dependencies.
   * Modules: `manifest`, `canonical`, `adapters`, `skills`, `profiles`, `validator`, `cli`.
2. **Adapters**:
   * Base class `AgentAdapter` providing `generate()`, `validate()`, `detect()`, and `supported_artifacts()`.
   * Concrete adapters: `AgentsMdAdapter`, `ClaudeCodeAdapter`, `AntigravityAdapter`, `CursorAdapter`, `OpenCodeAdapter`, `GenericExportAdapter`.
3. **State Management**:
   * Stored in `.udk/manifest.json`.
   * Tracks installed profile, selected adapters, generated files, hashes for drift detection, and custom overrides.
