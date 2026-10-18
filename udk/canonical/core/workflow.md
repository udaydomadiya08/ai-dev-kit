# Development Workflow: Universal AI Dev Kit

This document outlines the standard procedural loop for AI-assisted development.

---

## 1. The Inspect-Plan-Execute-Verify Loop

AI coding agents must follow this four-phase operational loop:

```
+------------+       +------------+       +------------+       +------------+
| 1. Inspect | ----> |  2. Plan   | ----> | 3. Execute | ----> | 4. Verify  |
+------------+       +------------+       +------------+       +------------+
      ^                                                              |
      +--------------------------------------------------------------+
                           (Iterate if verification fails)
```

### Step 1: Inspect (Context Discovery)
* Check repository status and git state.
* Locate relevant files, tests, and configuration.
* Inspect existing test commands and build setup.

### Step 2: Plan (Scope Definition)
* Define the minimal set of files to be modified or created.
* Identify potential regression points and edge cases.
* Formulate test criteria before modifying production code.

### Step 3: Execute (Disciplined Implementation)
* Apply minimal, coherent edits matching existing styles.
* Write accompanying unit/integration tests alongside feature code.
* Ensure all new functions, types, and files have clear documentation.

### Step 4: Verify (Executable Validation)
* Run automated test suites (`pytest`, `npm test`, `cargo test`, etc.).
* Run linters and type checkers (`ruff`, `eslint`, `mypy`).
* Test failure conditions, invalid inputs, and boundary conditions.
* Inspect git diff to ensure no unintended modifications or temp files were introduced.

---

## 2. Change Management & Non-Destructive Operation
* **Never Overwrite Without Checks**: Before writing to a file, verify whether it exists and whether it is user-owned.
* **Preserve Unrelated Changes**: Do not revert or touch uncommitted edits in other files.
* **Keep Diffs Clean**: Review git diff before concluding work; remove any debugging prints, scratch files, or test outputs.
