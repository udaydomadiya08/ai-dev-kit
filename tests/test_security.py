"""
Security and failure-mode tests for Universal AI Dev Kit (UDK).
Tests path traversal prevention, secret leakage detection, and filesystem isolation.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from udk.generator.engine import GeneratorEngine, PlanItem
from udk.validator.security import (
    SecurityViolationError,
    assert_safe_path,
    scan_for_secrets,
)


def test_assert_safe_path_valid(tmp_path: Path):
    child = tmp_path / "valid_child.txt"
    resolved = assert_safe_path(child, tmp_path)
    assert resolved == child.resolve()

    rel_child = "sub/folder/file.md"
    resolved_rel = assert_safe_path(rel_child, tmp_path)
    assert resolved_rel == (tmp_path / rel_child).resolve()


def test_assert_safe_path_traversal_attempts(tmp_path: Path):
    # Attempt to escape via relative parent traversal
    with pytest.raises(SecurityViolationError):
        assert_safe_path("../../outside.txt", tmp_path)

    with pytest.raises(SecurityViolationError):
        assert_safe_path(tmp_path / "sub" / ".." / ".." / "etc" / "passwd", tmp_path)

    # Attempt to target an absolute outside directory
    with pytest.raises(SecurityViolationError):
        assert_safe_path(Path("/etc/hosts"), tmp_path)


def test_scan_for_secrets():
    # Private key
    secret_text = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA0...\n-----END RSA PRIVATE KEY-----"
    findings = scan_for_secrets(secret_text)
    assert len(findings) > 0
    assert "Private Key Header" in findings[0]

    # AWS Key
    aws_text = "export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE"
    findings_aws = scan_for_secrets(aws_text)
    assert len(findings_aws) > 0
    assert "AWS Access Key ID" in findings_aws[0]

    # Clean text
    clean_text = "def hello(): return 'clean code without keys'"
    assert len(scan_for_secrets(clean_text)) == 0


def test_generator_blocks_traversal_on_apply(tmp_path: Path):
    engine = GeneratorEngine(workspace_root=tmp_path)
    malicious_item = PlanItem(
        path="../../malicious_escape.txt",
        action="create",
        content="malicious payload",
        sha256="dummy",
        generator="test",
    )
    with pytest.raises((PermissionError, SecurityViolationError)):
        engine.apply(
            [malicious_item], profile_name="minimal", adapter_ids=["agents-md"]
        )
