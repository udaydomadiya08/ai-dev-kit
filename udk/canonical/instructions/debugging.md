# Task Instruction: Debugging & Root-Cause Analysis

## Objective
Guide an AI coding agent to diagnose, isolate, and fix software defects systematically rather than making random edits.

---

## 1. Defect Reproduction
1. **Gather Evidence**: Collect the exact failure symptoms, error logs, tracebacks, and environment conditions.
2. **Reproduce Deterministically**: Write a minimal reproducing script or automated test case that consistently reproduces the failure.
3. **Inspect Actual vs Expected**: Clearly define what should have happened versus what actually occurred.

## 2. Root-Cause Analysis
1. **Formulate Hypotheses**: Develop testable theories based on the evidence (e.g. state mutation, missing validation, off-by-one, type mismatch).
2. **Trace the Failure**: Follow the execution path backward from the point of failure to where the faulty state originated.
3. **Verify the Root Cause**: Confirm that the hypothesis explains all observed symptoms, not just a surface anomaly.

## 3. Minimal Targeted Fix & Verification
1. **Apply the Minimal Fix**: Modify only the code necessary to correct the root cause. Avoid shotgun debugging or altering unrelated code.
2. **Run Reproduction Test**: Verify that the previously failing reproduction test now passes.
3. **Run Full Test Suite**: Execute the broader test suite to confirm that no regressions were introduced.
