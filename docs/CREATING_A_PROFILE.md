# Guide: Creating a Project Profile

This guide explains how to define, test, and register a new domain profile in the **Universal AI Dev Kit** (`udk`).

---

## 1. What Is a Project Profile?

A **Project Profile** adapts universal engineering standards to a specific tech stack or development domain (e.g. `python`, `web`, `ai-ml`, `rust`, `go`, `mobile`).

A profile configures:
* Standard commands (test, lint, build, dev).
* Domain-specific conventions (style, error handling, conventions).
* File globs for rule targeting (e.g. `*.py` or `*.{ts,tsx}`).
* Recommended skills from the canonical skills library.

---

## 2. Defining a Profile

Profiles are defined in JSON format inside `udk/canonical/profiles/<profile_id>.json`:

```json
{
  "id": "rust",
  "name": "Rust Systems Programming",
  "description": "Configured for idiomatic Rust development with cargo, clippy, and memory safety invariants.",
  "file_globs": "*.rs",
  "commands": {
    "test": "cargo test",
    "lint": "cargo clippy -- -D warnings",
    "build": "cargo build --release",
    "format": "cargo fmt --check"
  },
  "conventions": [
    "Prefer safe abstractions over unsafe blocks; document safety invariants if unsafe is mandatory.",
    "Handle Result and Option types explicitly with match or ?; avoid unwrap() in production paths.",
    "Write unit tests in submodules and integration tests in tests/."
  ],
  "recommended_skills": [
    "debugging",
    "test_planning",
    "architecture_review",
    "security_review"
  ]
}
```

---

## 3. Verifying and Testing

Once you create `udk/canonical/profiles/<profile_id>.json`:
1. Verify it appears in `udk list profiles`:
   ```bash
   udk list profiles
   ```
2. Run automated profile tests:
   ```bash
   pytest tests/test_profiles.py
   ```
3. Test initialization in a temporary directory:
   ```bash
   udk init --path /tmp/test-rust --profile rust --dry-run
   ```
