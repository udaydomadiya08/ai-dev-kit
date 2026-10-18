---
name: "test_planning"
description: "Design comprehensive test suites covering unit logic, integration boundaries, failure modes, and security invariants."
version: "1.0.0"
tags: ["testing", "qa", "verification"]
---

# Skill: Test Planning and Execution

## 1. Purpose
Formulate and execute a disciplined testing strategy combining unit, integration, and failure-mode tests to ensure software reliability and prevent regressions.

## 2. When to Use
* Implementing new CLI commands, adapters, or validator rules.
* Refactoring existing core logic.
* Setting up automated CI pipelines.

## 3. When NOT to Use
* Pure documentation edits that do not alter executable code or schemas.

## 4. Required Inputs
* Target module, class, or CLI interface to be tested.
* Documented acceptance criteria and boundary constraints.

## 5. Expected Outputs
* Comprehensive test file (e.g. `tests/test_<feature>.py`).
* Test execution output reporting passes, durations, and coverage.

## 6. Repeatable Procedure
1. **Define Test Categories**:
   * Unit tests: Isolated function testing with mocked or deterministic inputs.
   * Integration tests: Filesystem and multi-module interaction using temporary directories (`tmp_path`).
   * Edge-case tests: Boundary conditions (empty strings, missing keys, nonexistent files).
   * Negative tests: Invalid inputs, schema violations, permission errors.
2. **Implement Fixtures**: Set up clean, reusable test fixtures that clean up after themselves.
3. **Execute Runner**: Run `pytest -v` or language equivalent.
4. **Evaluate Diagnostics**: If failures occur, inspect the failure report, fix the defect, and re-run.
5. **Coverage Assessment**: Verify that critical error branches and boundary guards are executed.

## 7. Safety Boundaries
* Never run tests against live production databases or the developer's personal home directory.
* Always isolate filesystem writes to temporary directories (`tmp_path`).

## 8. Verification Criteria
* All tests pass cleanly without deprecation warnings or unhandled exceptions.
* Execution time remains fast (< 1s for unit suites).

## 9. Example
* Testing `udk remove`: Test verifies that managed files are removed while unmanaged user files in the same directory are preserved intact.

## 10. Known Limitations
* Performance benchmarking and stress tests require separate configurations from rapid unit tests.
