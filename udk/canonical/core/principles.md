# Core Principles: Universal AI Dev Kit

These principles are mandatory baseline invariants for any AI coding agent operating within this project.

---

## 1. Requirement Understanding Before Coding
* **Analyze the Ask**: Fully clarify the user's objective, constraints, and acceptance criteria before modifying or creating code.
* **Identify Gaps**: If an instruction is genuinely underspecified or high-risk, outline the trade-offs or inspect existing project conventions to deduce the intended behavior.
* **Do Not Guess Invariants**: Verify existing architectural decisions, schemas, and configurations rather than hallucinating APIs or interfaces.

## 2. Inspect Existing Code Before Modifying
* **Read Before Write**: Always read the existing implementation, imports, and surrounding comments before editing a file.
* **Trace Call Paths**: Follow callers and callees to understand the blast radius of changes.
* **Match Project Idioms**: Respect the established naming styles, directory organization, error handling patterns, and formatting conventions of the codebase.

## 3. Architecture Preservation & Minimal Coherent Changes
* **Preserve Design Integrity**: Do not perform unsolicited architectural refactorings or introduce new paradigms when fixing a specific bug or adding a localized feature.
* **Make Minimal Coherent Edits**: Avoid gratuitous whitespace churn, unrelated formatting alterations, or rewriting whole files when changing a few lines.
* **Atomic Scope**: Keep changes focused strictly on the requested task. Do not touch unrelated modules or tests.

## 4. Clear Interfaces & Edge Cases
* **Explicit Contracts**: Design modular functions with explicit arguments, clear return types, and documented exceptions.
* **Handle Boundaries**: Explicitly handle empty inputs, nulls, zero values, network timeouts, file missing states, and permission errors.
* **Fail Fast & Informatively**: Provide descriptive error messages that identify the failed operation and suggest remediation.

## 5. Verifiable Behavior & Regression Prevention
* **Executable Proof**: Never claim code works without running automated tests, linter checks, or executable verification scripts.
* **Test Regressions**: When fixing a bug, write a reproduction test that fails before the fix and passes afterward.
* **Report Honestly**: Report exact test command outputs, pass/fail counts, and known limitations. Never fabricate test results.
