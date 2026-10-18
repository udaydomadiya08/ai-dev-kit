---
name: "security_review"
description: "Audit code, configuration, and dependencies for path traversal, secret exposure, command injection, and permission vulnerabilities."
version: "1.0.0"
tags: ["security", "audit", "safety"]
---

# Skill: Security Review

## 1. Purpose
Identify and remediate potential security vulnerabilities across project source code, configuration files, and external dependencies.

## 2. When to Use
* Preparing a new release or public deployment.
* Adding new file system operations, CLI argument parsing, or shell execution paths.
* Auditing external skills, dependencies, or user-supplied templates.

## 3. When NOT to Use
* Substituting for a full formal third-party penetration test or compliance audit.

## 4. Required Inputs
* Source code, manifests, and configuration files.
* Threat model document (see `docs/PRODUCT_SPECIFICATION.md`).

## 5. Expected Outputs
* Security audit report detailing findings, severity levels (Critical, High, Medium, Low), and remediation steps.
* Automated negative tests validating security boundaries (e.g. path traversal regression tests).

## 6. Repeatable Procedure
1. **Secrets Scan**: Search for high-entropy strings, API keys, private tokens, passwords, and `.env` references.
2. **Filesystem Path Audit**: Verify that all file path resolutions use `resolve()` and check `startswith(project_root)`. Ensure no `..` traversal can escape workspace.
3. **Execution Guardrails**: Confirm that no untrusted input is passed to `eval()`, `exec()`, or unescaped `os.system()` / `subprocess.Popen(shell=True)`.
4. **Dependency Vulnerability Check**: Run `pip-audit`, `npm audit`, or check known CVE databases for reported vulnerabilities in pinned dependencies.
5. **Permission Sandboxing**: Verify that instructions remind users that prompt rules do not replace OS container/permission isolation.

## 7. Safety Boundaries
* Never claim an application is "100% secure" or "guaranteed unhackable".
* Follow responsible disclosure guidelines (see `SECURITY.md`).

## 8. Verification Criteria
* Regression tests verifying path traversal prevention (`../../etc/passwd`) pass and reject unsafe input.
* Zero hardcoded secrets present in repository history or working tree.

## 9. Example
* Identified risk where `--profile ../outside` could read arbitrary filesystem paths. Added validation requiring profile names to match regex `^[a-zA-Z0-9_-]+$`.

## 10. Known Limitations
* Static security review cannot detect zero-day vulnerabilities in host operating system kernels or runtime interpreters.
