# Task Instruction: Code Review & Quality Assurance

## Objective
Guide an AI coding agent to perform disciplined code reviews of changes before merging or concluding tasks.

---

## 1. Review Dimensions
1. **Correctness & Logic**: Does the code accurately solve the specified problem without subtle off-by-one errors, infinite loops, or resource leaks?
2. **Architecture & Scope**: Does the change respect established modular boundaries? Does it stay within the agreed scope without gratuitous refactoring?
3. **Security & Input Validation**: Are user inputs sanitized? Are filesystem operations protected against path traversal? Are secrets properly excluded?
4. **Performance & Complexity**: Are algorithmic complexities reasonable? Are there unnecessary database queries or repetitive disk IO operations?
5. **Testing & Coverage**: Are new code paths accompanied by automated tests? Do edge case and failure tests exist?

## 2. Review Checklist
* [ ] All tests pass cleanly without deprecation warnings.
* [ ] No commented-out dead code or abandoned debug statements (`print()`, `console.log`).
* [ ] Error handling provides helpful diagnostic messages.
* [ ] Documentation, docstrings, and changelogs are updated where relevant.
* [ ] Git diff contains only changes strictly necessary for the task.
