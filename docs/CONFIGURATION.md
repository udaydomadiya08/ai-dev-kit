# Configuration & Manifest Reference: Universal AI Dev Kit

This document explains configuration management, file ownership tracking, and the manifest schema in **Universal AI Dev Kit** (`udk`).

---

## 1. Configuration Philosophy

UDK follows two foundational configuration principles:
1. **Single Canonical Source of Truth**: All rules, workflows, and skills are maintained in canonical format and compiled deterministically into target files.
2. **Explicit File Ownership & Drift Tracking**: Generated files are tracked with SHA-256 hashes in `.udk/manifest.json`. The toolkit never silently overwrites developer modifications.

---

## 2. Manifest Schema (`.udk/manifest.json`)

When you run `udk init`, UDK creates `.udk/manifest.json` in your repository root.

### Example Manifest
```json
{
  "schema_version": "1.0.0",
  "toolkit_version": "0.1.0",
  "profile": "python",
  "adapters": [
    "agents-md",
    "claude-code"
  ],
  "skills": [
    "debugging",
    "test_planning",
    "incremental_impl"
  ],
  "files": {
    "AGENTS.md": {
      "path": "AGENTS.md",
      "sha256": "4a7f92b...",
      "generator": "agents-md",
      "managed": true,
      "customized": false
    },
    "CLAUDE.md": {
      "path": "CLAUDE.md",
      "sha256": "8c31e0a...",
      "generator": "claude-code",
      "managed": true,
      "customized": false
    }
  },
  "custom_settings": {}
}
```

### Schema Fields
* `schema_version`: String SemVer of the manifest structure (currently `1.0.0`).
* `toolkit_version`: Version of UDK used to generate the configurations.
* `profile`: Active domain profile ID (e.g. `python`, `web`).
* `adapters`: Array of active agent adapter IDs.
* `skills`: Array of included canonical skills.
* `files`: Map of relative file paths to `FileRecord` metadata:
  * `path`: Relative path from project root.
  * `sha256`: SHA-256 hash of generated content.
  * `generator`: ID of adapter that created the file.
  * `managed`: Boolean indicating whether UDK owns and updates the file.
  * `customized`: Boolean flag set if drift was reconciled.

---

## 3. Drift Detection and Updates

* **`udk diff`**: Inspects disk files against recorded hashes. Reports each file as `UNCHANGED`, `MODIFIED`, or `MISSING`.
* **`udk update`**: Re-compiles configurations from updated canonical templates:
  * If a file is **unchanged**, it is cleanly updated to the latest template version.
  * If a file was **modified** by the user, update halts with a `CONFLICT` warning to protect developer customizations.
  * Running `udk update --force` explicitly permits overwriting modified files.
