# Task Instruction: Documentation Maintenance

## Objective
Guide an AI coding agent to maintain accurate, concise, and up-to-date documentation alongside code changes.

---

## 1. Documentation Integrity
1. **Synchronize with Code**: Whenever public APIs, CLI arguments, or configuration options change, update corresponding documentation in the same change set.
2. **Preserve Existing Context**: Preserve existing docstrings, technical rationale, and explanatory notes unless they are rendered factually incorrect.
3. **Verify Code Examples**: Ensure all code snippets, CLI examples, and quick-start commands shown in READMEs or guides work as written.

## 2. Structure and Clarity
1. **Concise & Direct**: Focus on actionable guidance, architecture decisions, and non-obvious rationale rather than narrating line-by-line what the code does.
2. **Use Clear Visual Formats**: Use GitHub-flavored markdown, code fencing with syntax highlighting, tables for structured data, and mermaid diagrams for architectural flows.
3. **Keep Links Working**: Verify that relative markdown file links point to files that actually exist.
