# Engineering Standards: Universal AI Dev Kit

This document establishes the technical engineering standards for software developed with AI assistance.

---

## 1. Code Quality & Maintainability
* **Readability Over Cleverness**: Prefer standard, idiomatic code over complex one-liners or esoteric metaprogramming.
* **Separation of Concerns**: Separate business logic, transport/IO layers, data persistence, and CLI presentation.
* **Single Responsibility**: Functions and classes should have a single well-defined purpose.
* **Dependency Minimization**: Favor standard library capabilities before introducing external dependencies. Every new third-party library must be justified by substantial complexity reduction.

## 2. Type Safety & Schema Contracts
* **Explicit Type Annotations**: Use language-appropriate static typing (e.g. Python type hints, TypeScript interfaces, Rust types) on public interfaces, function parameters, and return types.
* **Schema Validation**: Validate external inputs, config files, and JSON/YAML payloads at system boundaries before processing.
* **Strict Null & Error Handling**: Avoid broad catch-all exception blocks (e.g., bare `except:`). Catch specific exceptions and log contextual diagnostics.

## 3. Configuration & State Management
* **Deterministic Configuration**: All configuration options must have sensible defaults and be documented.
* **State Isolation**: Application state must be stored in designated directories or files (e.g. `.udk/manifest.json`), never scattered across arbitrary locations.
* **No Hardcoded Constants**: Environment-specific URLs, credentials, or file paths must not be hardcoded in source code.

## 4. Cross-Platform Compatibility
* **Path Operations**: Always use path-safe libraries (e.g., `pathlib.Path` or `os.path.join`) rather than manual string concatenation with `/` or `\`.
* **Line Endings & Encodings**: Enforce UTF-8 encoding explicitly for all file read and write operations. Handle CRLF / LF line endings cleanly.
* **Portability**: Avoid shell-specific builtins or OS-dependent commands unless wrapped in platform-checking guards.
