# Release Process: Universal AI Dev Kit

This document describes the release engineering procedure for **Universal AI Dev Kit** (`udk`).

---

## 1. Release Principles

* **Semantic Versioning (SemVer 2.0.0)**: Releases strictly follow `MAJOR.MINOR.PATCH`.
* **Honest Verification**: No version is tagged or published unless all automated unit, integration, and security tests pass with 100% success rate on clean working trees.
* **No Unsolicited Releases**: Release tags and package publishing are executed only with explicit authorization.

---

## 2. Pre-Release Audit Checklist

1. **Working Tree Cleanliness**:
   * Run `git status` to ensure zero unexpected untracked files or uncommitted changes.
2. **Execute Automated Test Suite**:
   ```bash
   pytest -v --cov=udk tests/
   ```
   * Confirm 100% test pass rate.
   * Verify coverage meets quality standards.
3. **Format & Lint Verification**:
   ```bash
   ruff check .
   mypy udk
   ```
4. **Update Documentation & Changelog**:
   * Ensure `CHANGELOG.md` documents all new adapters, skills, fixes, and architectural decisions under the new version header.
   * Verify all relative links in `docs/` and `README.md`.
5. **Version Bump**:
   * Bump version in `pyproject.toml` and `udk/__init__.py`.

---

## 3. Packaging and Distribution Verification

1. **Build Distribution Artifacts**:
   ```bash
   python -m pip install --upgrade build
   python -m build
   ```
2. **Verify Wheel in Clean Environment**:
   ```bash
   python -m venv /tmp/udk_test_env
   /tmp/udk_test_env/bin/pip install dist/*.whl
   /tmp/udk_test_env/bin/udk --help
   /tmp/udk_test_env/bin/udk list all
   rm -rf /tmp/udk_test_env
   ```

---

## 4. Tagging and Publishing

Upon explicit authorization:
```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```
CI/CD workflows will build and publish verified packages to PyPI and GitHub Releases.
