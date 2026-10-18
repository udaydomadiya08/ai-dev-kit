"""
Security engine for Universal AI Dev Kit (UDK).
Provides path sanitization against directory traversal, symlink verification,
and secret leakage pattern scanning.
"""

from __future__ import annotations

import os
import re
from pathlib import Path


class SecurityViolationError(PermissionError):
    """Raised when a path or operation violates project isolation boundaries."""


# High-risk secret patterns
SECRET_PATTERNS: list[tuple[str, re.Pattern]] = [
    (
        "Private Key Header",
        re.compile(r"-----BEGIN (?:RSA|EC|OPENSSH|DSA|PGP) PRIVATE KEY-----"),
    ),
    ("AWS Access Key ID", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub Personal Access Token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{36,}\b")),
    (
        "Generic Bearer Secret",
        re.compile(
            r"(?i)(?:api_key|access_token|secret_key|private_key)\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]"
        ),
    ),
]


def assert_safe_path(target_path: Path | str, workspace_root: Path | str) -> Path:
    """
    Normalizes path and strictly asserts that it resolves within workspace_root.
    Raises SecurityViolationError if path attempts traversal outside project boundary.
    """
    ws = Path(workspace_root).resolve()
    target = Path(target_path)

    # If target is relative, resolve it relative to workspace_root
    if not target.is_absolute():
        resolved = (ws / target).resolve()
    else:
        resolved = target.resolve()

    ws_str = str(ws)
    resolved_str = str(resolved)

    # Exact match or child directory/file check
    if resolved_str != ws_str and not resolved_str.startswith(ws_str + os.sep):
        raise SecurityViolationError(
            f"Security Violation: Path '{target_path}' escapes workspace boundary '{ws}'."
        )

    return resolved


def scan_for_secrets(content: str) -> list[str]:
    """Scans text content for high-risk secret patterns."""
    findings: list[str] = []
    for name, pattern in SECRET_PATTERNS:
        matches = pattern.findall(content)
        if matches:
            findings.append(f"Detected potential secret pattern: {name}")
    return findings
