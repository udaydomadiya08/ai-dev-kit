# Troubleshooting Guide: Universal AI Dev Kit

This guide addresses common questions, error messages, and recovery procedures when using **Universal AI Dev Kit** (`udk`).

---

## 1. Common Errors and Solutions

### Error: `CONFLICTS DETECTED: Existing files were modified or conflict with targets`
* **Cause**: You ran `udk init` or `udk update`, but an existing file (like `AGENTS.md` or `.cursorrules`) was modified by hand or existed before UDK was initialized.
* **Resolution**:
  1. Inspect changes with `udk diff`.
  2. If you want to overwrite your local file with the standard template, pass `--force`:
     ```bash
     udk init --force
     ```
  3. If you want to keep your manual edits, back up the file or merge changes manually.

---

### Error: `Security Violation: Path escapes workspace boundary`
* **Cause**: An adapter, skill, or CLI flag attempted to write or reference a file path that resolves outside the project directory (e.g. `../../etc`).
* **Resolution**: Ensure all target paths are relative and reside strictly inside the repository. UDK strictly prevents path traversal for safety.

---

### Warning: `Managed file is missing from workspace`
* **Cause**: A file tracked by `.udk/manifest.json` was deleted manually from disk.
* **Resolution**: Run `udk update` to regenerate the missing file, or run `udk remove` if you wish to uninstall UDK from the project.

---

### Error: `Unknown profile 'xyz'` or `Unknown agent adapter 'xyz'`
* **Cause**: Typo or unsupported profile/adapter ID.
* **Resolution**: Check available options with:
  ```bash
  udk list profiles
  udk list agents
  ```

---

## 2. Diagnostic Health Check (`udk doctor`)

If you encounter unexpected behavior, run the built-in diagnostic tool:
```bash
udk doctor
```
It automatically inspects:
* Python version compatibility (>= 3.9)
* Git repository status
* Manifest integrity and JSON structure
* Filesystem security sanitization
