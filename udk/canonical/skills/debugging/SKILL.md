---
name: "debugging"
description: "Isolate software defects systematically through reproduction, evidence gathering, root-cause analysis, and minimal fixes."
version: "1.0.0"
tags: ["debugging", "troubleshooting", "investigation"]
---

# Skill: Debugging and Root-Cause Analysis

## 1. Purpose
Diagnose, isolate, and eliminate software defects using systematic scientific debugging rather than trial-and-error edits.

## 2. When to Use
* An automated test fails.
* A user reports a bug, unexpected exception, or crash.
* System behavior deviates from documented specification.

## 3. When NOT to Use
* Developing clean-sheet features where no defect exists.

## 4. Required Inputs
* Error message, stack trace, or failure description.
* Reproduction command or input conditions.
* Relevant source files and environment details.

## 5. Expected Outputs
* Isolated root cause explanation backed by code evidence.
* Automated regression test that fails before the fix and passes after.
* Minimal targeted patch addressing the defect.

## 6. Repeatable Procedure
1. **Evidence Collection**: Record exact error text, line numbers, call stack, and inputs.
2. **Deterministic Reproduction**: Create an isolated minimal test script or test case that reliably triggers the bug.
3. **Hypothesis Formulation**: Formulate a hypothesis explaining why the bug occurs under those specific conditions.
4. **Execution Tracing**: Trace the variable state and control flow leading to the point of failure.
5. **Root-Cause Confirmation**: Confirm the mechanism of failure (e.g. state mutation, missing key in dictionary, off-by-one).
6. **Minimal Targeted Patch**: Apply the smallest coherent fix addressing the root cause.
7. **Regression Test Verification**: Verify the reproduction test now passes, followed by the entire test suite.

## 7. Safety Boundaries
* Never apply random code modifications ("shotgun debugging") in hopes that a test passes.
* Do not silence errors with bare `try/except: pass`.

## 8. Verification Criteria
* Regression test fails on unfixed code and passes cleanly on patched code.
* No existing tests are broken.

## 9. Example
* **Bug**: Manifest hash mismatch on Windows due to CRLF vs LF differences.
* **Reproduction**: Write test asserting hash equality across line endings.
* **Fix**: Normalize line endings to LF before hashing.
* **Verification**: Test passes on both Windows and Unix line endings.

## 10. Known Limitations
* Intermittent race conditions or network-dependent bugs require mock harnesses to achieve deterministic reproduction.
