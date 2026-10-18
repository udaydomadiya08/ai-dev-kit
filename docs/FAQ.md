# Frequently Asked Questions (FAQ)

---

## 1. What exactly does Universal AI Dev Kit do?
UDK gives developers a vendor-neutral, single source of truth for AI agent engineering rules, workflows, domain profiles, and reusable skills. Instead of maintaining separate, drifting configuration files for Cursor, Claude Code, Antigravity, and AGENTS.md, UDK compiles canonical rules deterministically into each target format.

---

## 2. Does UDK call remote AI APIs or cost money to run?
**No.** UDK is 100% offline, local, and open-source (Apache-2.0). It requires zero API tokens, runs with standard library Python, and makes no network requests during initialization or validation.

---

## 3. Can I customize the rules for my specific repository?
**Yes.** You can customize the active profile (e.g. adding custom commands or conventions in `.udk/manifest.json` or custom profiles), or edit the generated files directly. If you edit files directly, UDK tracks your changes and will never overwrite them during updates unless you explicitly pass `--force`.

---

## 4. Does UDK support monorepos?
**Yes.** You can run `udk init --path ./packages/backend --profile python` and `udk init --path ./packages/frontend --profile web` to establish scoped rules in distinct subdirectories.

---

## 5. How does UDK prevent AI coding agents from doing harmful things?
Every configuration compiled by UDK embeds non-negotiable Layer 1 Safety Invariants:
* Zero secret logging (protecting `.env`, tokens, private keys).
* Workspace boundaries (preventing edits outside project root).
* Bounded non-destructive commands.
* Explicit notice that prompt instructions guide planning, but operating system isolation (containers, user permissions) must enforce hard security boundaries.

---

## 6. How do I contribute a new adapter or skill?
See our guides:
* [Adding an Adapter](ADDING_AN_ADAPTER.md)
* [Creating a Skill](CREATING_A_SKILL.md)
* [Creating a Profile](CREATING_A_PROFILE.md)
* [Contributing Guide](../CONTRIBUTING.md)
