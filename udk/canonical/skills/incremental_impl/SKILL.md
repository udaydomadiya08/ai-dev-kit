---
name: "incremental_impl"
description: "Execute code modifications in small, coherent, verifiable steps with continuous testing."
version: "1.0.0"
tags: ["implementation", "coding", "workflow"]
---

# Skill: Incremental Implementation

## 1. Purpose
Implement software features and fixes in small, testable chunks that keep the build passing at every stage, preventing large unmanageable diffs.

## 2. When to Use
* Writing new modules, functions, classes, or CLI commands.
* Modifying existing logic to support new requirements.
* Applying multi-file code updates.

## 3. When NOT to Use
* Documentation-only updates.

## 4. Required Inputs
* Phased work plan or requirement checklist.
* Existing source code and test suite.

## 5. Expected Outputs
* Working code changes matching established code style.
* New or updated automated unit tests.
* Passing build and test runner output.

## 6. Repeatable Procedure
1. **Target Inspection**: Read the target file completely; identify existing import styles and helper functions.
2. **Write Minimal Code Block**: Implement one logical function, class, or method.
3. **Write Matching Test**: Immediately write a unit test covering the newly written logic.
4. **Execute Verification**: Run the test runner (`pytest`, `vitest`). Fix any syntax errors or test failures immediately.
5. **Git Status & Diff Check**: Inspect git diff to verify no unintended modifications, dead code, or debugging prints remain.
6. **Repeat**: Proceed to the next incremental task.

## 7. Safety Boundaries
* Do not rewrite untouched functions or reformat entire files unrelated to the task.
* Do not introduce dependencies without verifying licensing and environment compatibility.

## 8. Verification Criteria
* Each incremental change passes all automated tests.
* No regressions introduced into previously passing test suites.

## 9. Example
* Adding `validate` command: First implement `validate_schema()`, write `test_validate_schema()`, verify test passes, then wire into CLI router.

## 10. Known Limitations
* Strongly coupled legacy codebases may require interface decoupling before clean incremental testing is possible.
