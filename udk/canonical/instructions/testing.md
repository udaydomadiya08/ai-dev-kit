# Task Instruction: Test Planning & Execution

## Objective
Guide an AI coding agent to design, implement, and run meaningful automated tests.

---

## 1. Test Strategy & Structure
1. **Pyramid Distribution**: Favor fast, deterministic unit tests for business logic; use integration tests for boundaries (IO, filesystem, APIs); keep end-to-end tests focused on critical paths.
2. **Deterministic & Isolated**: Tests must not rely on shared global state, network availability, or external cloud services unless explicitly designed as integration tests.
3. **Use Temporary Directories**: Any test performing file or disk modifications must use temporary sandbox directories (e.g. `tmp_path` in pytest) and clean them up automatically.

## 2. Test Coverage & Edge Cases
1. **Happy Path**: Verify standard inputs produce expected outputs.
2. **Negative Scenarios**: Verify that invalid inputs, malformed configurations, or missing files raise expected exceptions with clear diagnostic messages.
3. **Boundary Values**: Test zero values, empty collections, maximum limits, and unusual characters (e.g. Unicode, special characters, whitespace).

## 3. Test Execution & Reporting
1. Run the test suite using standard test runners (`pytest`, `npm test`, etc.).
2. Record and report actual test output (e.g., `42 passed, 0 failed in 1.23s`).
3. If tests fail, diagnose and fix the failure rather than disabling or skipping the test.
