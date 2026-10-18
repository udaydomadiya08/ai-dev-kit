# Task Instruction: Incremental Implementation

## Objective
Guide an AI coding agent to implement code changes cleanly, reliably, and with minimal disruption.

---

## 1. Preparation
1. **Target File Inspection**: Read the target file in its entirety before modifying it.
2. **Import Hygiene**: Verify that all new modules, classes, and helper functions are imported cleanly using the project's standard import ordering.
3. **Configuration Check**: Check if changes require updating configuration files or environment variables.

## 2. Code Authoring Rules
1. **Small Coherent Steps**: Write code in logical, functional increments.
2. **Explicit Interfaces**: Declare parameters, return types, and exceptions clearly.
3. **No Unfinished Stubs**: Do not leave `TODO`, `pass`, or `NotImplementedError` placeholders in production paths unless explicitly requested as stubs.
4. **Preserve Existing Documentation**: Keep relevant docstrings and comments intact. Add documentation for any newly introduced functions or classes.

## 3. Post-Implementation Verification
1. Run local linters or syntax checks immediately on the modified files.
2. Ensure no dangling syntax errors, unreferenced variables, or broken imports.
3. Check the git diff for unintended changes.
