# Security Policy

## 1. Supported Versions

Security updates are applied to the following versions of **Universal AI Dev Kit**:

| Version | Supported |
| :--- | :--- |
| `0.1.x` | :white_check_mark: Yes |
| `< 0.1.0` | :x: No |

---

## 2. Reporting a Vulnerability

The Universal AI Dev Kit team takes the security of our software and our users' repositories seriously. If you believe you have discovered a vulnerability (such as a path traversal flaw, unauthorized file modification, or secret leakage risk), please report it responsibly:

* **Email:** Send your report to `security@universal-ai-dev-kit.org` (or open a private GitHub Security Advisory).
* **Information to Include:**
  * Detailed description of the vulnerability.
  * Steps to reproduce, including any test repository or command arguments.
  * Proof of concept or minimal reproduction script.
  * Potential impact.
* **Response Timeline:**
  * Initial acknowledgment: Within 48 hours.
  * Status update and triage: Within 5 business days.
  * Fix release: Coordinated disclosure with patch release.

Please do not disclose the issue publicly until a fix has been released.

---

## 3. Toolkit Security Guardrails

The Universal AI Dev Kit enforces several intrinsic architectural security measures:
1. **Strict Path Sanitization**: Prevents directory traversal attacks via `..` or absolute paths.
2. **Zero Arbitrary Execution**: Does not automatically run arbitrary executable scripts embedded within skills or profiles during initialization or validation.
3. **Secret Hygiene**: Core instructions actively direct agents to ignore `.env`, secret files, API tokens, and private keys.
4. **Ownership & Non-Destructive Modifiers**: File updates and removals strictly reference manifest-tracked files and never delete unmanaged user data.
