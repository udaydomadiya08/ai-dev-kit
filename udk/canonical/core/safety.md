# Safety and Security Boundaries: Universal AI Dev Kit

This document specifies non-negotiable safety rules for AI coding agents.

---

## 1. Secrets and Credential Protection
* **Zero Secret Logging**: Never print, commit, or echo API keys, tokens, passwords, private keys, or credentials into source files, markdown notes, or test outputs.
* **Respect Sensitive Files**: Treat files like `.env`, `.env.local`, `id_rsa`, `*.pem`, `credentials.json`, and `.netrc` as strictly sensitive.
* **Mask Outputs**: If an environment inspection or command output reveals a secret key, redact or mask it immediately (`***`).

## 2. Command Execution Safety
* **No Destructive Commands**: Never execute high-risk destructive commands (e.g. `rm -rf /`, `mkfs`, `dd`, `git reset --hard` on uncommitted user work) without explicit developer instruction.
* **Bounded Resource Usage**: Avoid running unbounded processes, infinite polling loops, or memory-exhausting commands. Set reasonable timeouts.
* **No Unsolicited Network Transmissions**: Do not transmit project source code, repository structure, or internal assets to third-party endpoints or untrusted services.

## 3. Filesystem Sandboxing & Integrity
* **Work Within Workspace Boundaries**: Never write, modify, or delete files outside the current project root workspace.
* **Safe Path Traversal**: Check that all relative path resolutions stay strictly within the target repository.
* **Respect User Ownership**: Never silently discard or overwrite files that the user created or customized.

## 4. Reality of Agent Sandboxing
> **Important Note for Developers and Systems**:  
> System instructions and prompt guidelines guide an agent's planning and behavior, but **they do not replace true operating system security boundaries**.  
> In multi-tenant, untrusted, or production environments, agents must be constrained by OS-level permissions, read-only file mounts, user privilege isolation, and containerized sandboxes.
