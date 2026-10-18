# Task Instruction: Planning & Requirements Analysis

## Objective
Guide an AI coding agent to effectively plan a feature, architectural change, or non-trivial task before making code edits.

---

## 1. Context Assessment
1. **Identify the Goal**: State the objective and definition of done in plain terms.
2. **Review Project Context**:
   * Inspect existing architecture and design documents.
   * Review directory structures and module boundaries.
   * Check dependencies and available tooling.
3. **Clarify Ambiguities**:
   * List any assumptions made.
   * If an assumption carries high architectural risk or potential data loss, propose clear options.

## 2. Work Breakdown & Phasing
1. **Divide into Atomic Steps**: Break complex work into coherent, testable phases.
2. **Define Acceptance Criteria**: Every phase must have clear, verifiable pass/fail criteria.
3. **Identify Risks & Regressions**: List existing systems or tests that could break.

## 3. Review Plan Before Modifying Code
1. Ensure the plan minimizes file churn.
2. Ensure the plan preserves existing public interfaces where feasible.
3. Verify that planned libraries and tools comply with the repository's licenses and ecosystem conventions.
