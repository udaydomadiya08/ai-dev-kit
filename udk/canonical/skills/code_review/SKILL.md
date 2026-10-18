---
name: "code_review"
description: "Perform structured code reviews assessing logic correctness, style conformance, security hygiene, and test completeness."
version: "1.0.0"
tags: ["review", "quality", "governance"]
---

# Skill: Code Review

## 1. Purpose
Evaluate pull requests or modified working trees against quality, architectural, security, and testing standards before merge or release.

## 2. When to Use
* Concluding a development phase or feature implementation.
* Reviewing an open pull request.
* Auditing third-party contributions.

## 3. When NOT to Use
* In the middle of an experimental prototyping session where code is actively in flux.

## 4. Required Inputs
* Git diff or list of modified/created files.
* Project style guide and architectural rules.

## 5. Expected Outputs
* Systematic review report categorized by Severity (Blocker, Warning, Suggestion).
* Verified checklist of correctness, security, tests, and documentation.

## 6. Repeatable Procedure
1. **Diff Inspection**: Run `git diff` to view every added, modified, or removed line.
2. **Correctness Review**: Check for logic bugs, unhandled exceptions, resource leaks, or missing return values.
3. **Security Audit**: Verify inputs are sanitized; check that no API keys or hardcoded secrets are present.
4. **Style & Convention Check**: Ensure code adheres to project naming conventions and formatting guidelines.
5. **Test Completeness**: Confirm that all new code paths have corresponding tests that actually pass.
6. **Documentation Sync**: Confirm that any modified CLI flags or APIs are reflected in documentation.

## 7. Safety Boundaries
* Do not approve PRs that disable failing tests or lower security guardrails without explicit rationale.

## 8. Verification Criteria
* All tests pass on the reviewed commit.
* Zero blocker-level findings remain unresolved.

## 9. Example
* Review caught an unhandled `JSONDecodeError` when loading a corrupted `manifest.json`. Added try/except block returning descriptive diagnostic error.

## 10. Known Limitations
* Automated code review cannot detect high-level business logic misunderstandings that pass technical tests.
