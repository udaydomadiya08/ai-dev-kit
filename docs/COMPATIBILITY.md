# Compatibility Matrix: Universal AI Dev Kit (UDK)

**Document Version:** 1.0.0  
**Status:** Living Specification  

---

## 1. Compatibility Taxonomy

To uphold Product Principle 2.8 (*Honest Compatibility*), UDK strictly classifies target agents and platforms into five verified support tiers:

1. **Tier 1 — Fully Tested Integration**:
   Configuration syntax, file locations, directory hierarchies, and live agent interpretation have been exercised and verified end-to-end.
2. **Tier 2 — Validated Configuration Generation**:
   Configurations are generated deterministically according to official published specifications, validated against structural schemas and file conventions, and tested in automated CI test suites.
3. **Tier 3 — Documented but Untested Compatibility**:
   Conventions conform to community documentation or published format guidelines, but end-to-end execution has not been verified in a live agent session.
4. **Tier 4 — Generic Export Support**:
   Exported as standard markdown or JSON; can be ingested by any LLM or agent supporting arbitrary text guidelines.
5. **Tier 5 — Unsupported Functionality**:
   Capabilities known to be incompatible with the target agent's current architecture (e.g. attempting to run MCP servers on agents that only support static markdown instructions).

---

## 2. Target Agent Compatibility Matrix

| Agent / Target | Support Tier | Primary Output Artifacts | Automated Schema / Syntax Validation | Live Agent Session Verified |
| :--- | :--- | :--- | :--- | :--- |
| **AGENTS.md Standard** | **Tier 1** (Fully Tested) | `AGENTS.md` | Yes (Markdown heading structure) | Yes |
| **Google Antigravity** | **Tier 1** (Fully Tested) | `.agents/`, `skills/*/SKILL.md`, `rules/`, `GEMINI.md` | Yes (YAML frontmatter + schema) | Yes |
| **Anthropic Claude Code** | **Tier 2** (Validated Gen) | `CLAUDE.md`, `.claude/` | Yes (Markdown format & structure) | Documented convention |
| **Cursor IDE** | **Tier 2** (Validated Gen) | `.cursorrules`, `.cursor/rules/*.mdc` | Yes (YAML frontmatter + glob check) | Documented convention |
| **OpenCode** | **Tier 2** (Validated Gen) | `opencode.json`, `.opencode/` | Yes (JSON Schema + layout check) | Documented convention |
| **OpenAI Codex / ChatGPT Projects** | **Tier 3** (Documented) | `AGENTS.md`, `.codex/` | Yes (Markdown structure) | Documented convention |
| **Generic LLM / Custom CLI** | **Tier 4** (Generic Export) | `ai_context.md`, `INSTRUCTIONS.md` | Yes (Pure Markdown) | N/A (Universal) |

---

## 3. Supported Operating Systems & Python Runtimes

### Operating Systems
* **macOS (Darwin arm64 & x86_64)**: Fully supported and tested.
* **Linux (Ubuntu / Debian / Alpine / Fedora)**: Supported (POSIX file path handling and permissions).
* **Windows (10/11 x64)**: Supported (explicit handling of `\` vs `/` and CRLF normalization).

### Python Runtimes
* **Python 3.10**: Minimum supported version.
* **Python 3.11**: Primary development and testing version.
* **Python 3.12**: Supported.
* **Python 3.13**: Supported.

---

## 4. Feature Support Matrix by Adapter

| Capability | AGENTS.md | Claude Code | Google Antigravity | Cursor | OpenCode | Generic Export |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Core Principles** | Yes | Yes | Yes | Yes | Yes | Yes |
| **Workflow Instructions** | Yes | Yes | Yes | Yes | Yes | Yes |
| **File-Glob Scoped Rules** | No (Global) | No (Global) | Yes | Yes (`globs:`) | Yes | No (Global) |
| **Standardized Skills** | Embedded | Inlined | `.agents/skills/` | Inlined | `.opencode/` | Embedded |
| **MCP Tool Manifests** | No | Optional | `mcp_config.json` | Future | `opencode.json` | No |
| **Dry-Run & Drift Check** | Yes | Yes | Yes | Yes | Yes | Yes |

---

## 5. Known Limitations & Non-Representable Features

1. **Glob-Scoped Rules on Flat Markdown Agents**:
   * *Limitation*: AGENTS.md and Claude Code read single root markdown files (`AGENTS.md` and `CLAUDE.md`).
   * *Resolution*: UDK compiles profile-specific rules into clearly labeled markdown sections rather than silently dropping them.
2. **Dynamic Tool Execution**:
   * *Limitation*: Plain markdown instructions cannot force a tool to execute a command; they can only guide the agent's planning.
   * *Resolution*: True permission controls must be applied at the host/container/IDE level.
