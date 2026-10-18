# Instruction Hierarchy and Precedence Resolution

**Document Version:** 1.0.0  
**Scope:** Definition of instruction precedence, layering, and conflict resolution across AI coding agents.

---

## 1. The Five Instruction Layers

When an AI coding agent acts on a codebase, it operates under multiple sources of instruction. The Universal AI Dev Kit defines a formal five-tier hierarchy:

```
[Layer 1: Safety & Permission Constraints]   (Highest Precedence - Invariant)
                    │
                    ▼
[Layer 2: Task-Specific User Requirements]  (Current prompt / goal)
                    │
                    ▼
[Layer 3: Project-Specific Instructions]    (Repository rules, profile, AGENTS.md)
                    │
                    ▼
[Layer 4: Directory / Module Guidance]      (Scoped sub-tree rules, .cursor/rules/)
                    │
                    ▼
[Layer 5: Universal Toolkit Defaults]       (Baseline principles & engineering standards)
```

---

## 2. Precedence Rules & Conflict Resolution

1. **Safety Constraints Always Override**:
   * Safety invariants (no secret exfiltration, no destructive filesystem operations outside project root, no unvetted arbitrary script execution) are non-negotiable.
   * If a user prompt or project rule instructs an agent to print an API key or execute `rm -rf /`, the agent **must refuse** and cite the safety boundary.

2. **Explicit Task Instructions Override Project Defaults**:
   * If the current user prompt requests: *"Implement without external dependencies"*, this overrides a project-level suggestion that mentions third-party libraries.

3. **Project / Profile Rules Override Universal Defaults**:
   * Universal defaults provide general best practices (e.g., standard testing conventions).
   * Project profile rules (e.g. `python.yaml` requiring `pytest`, or `web.yaml` requiring `vitest`) specialize and take precedence over generic defaults.

4. **Directory-Scoped Rules Specialize Subtrees**:
   * Where supported (e.g. Cursor MDC rules with `globs: frontend/**` or sub-directory `AGENTS.md`), rules apply specifically to files matching that path pattern.

5. **Reporting & Resolving Ambiguities**:
   * When two instructions at the same layer directly contradict each other (e.g. one instruction says "use tabs" and another says "use spaces"), the agent must inspect existing code to match the prevailing convention or request brief clarification.

---

## 3. Agent-Specific Precedence Alignment

| Agent | Native Hierarchy Behavior | UDK Adapter Mapping Strategy |
| :--- | :--- | :--- |
| **AGENTS.md** | Reads root `AGENTS.md`; optionally loads subfolder `AGENTS.md`. | Compiles Universal Principles -> Project Profile Rules -> Task Guidelines into distinct, sequential markdown sections with clear precedence headers. |
| **Claude Code** | Prioritizes `CLAUDE.md` in root; system instructions in environment. | Compiles core principles and commands into concise, high-priority sections in `CLAUDE.md`. |
| **Antigravity** | System prompt -> Global customizations -> Workspace rules (`rules/`) -> Task prompt. | Generates discrete `rules/` markdown files, `skills/*/SKILL.md`, and references in `GEMINI.md`. |
| **Cursor** | `.cursorrules` (legacy) or `.cursor/rules/*.mdc` (scoped with globs). | Emits modular `.cursor/rules/` with explicit `globs:` metadata and `alwaysApply:` settings. |
| **OpenCode** | Root `opencode.json` defining agents, tools, and profiles. | Generates `opencode.json` and `.opencode/` structured manifests. |
