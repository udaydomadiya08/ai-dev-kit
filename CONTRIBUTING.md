# Contributing to Universal AI Dev Kit

Thank you for your interest in contributing to **Universal AI Dev Kit** (`udk`)! We are committed to building an open, reproducible, and vendor-neutral foundation for AI-assisted software engineering.

---

## 1. Code of Conduct

All contributors and participants are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to the project maintainers.

---

## 2. Development Setup

### Prerequisites
* Python 3.10, 3.11, or 3.12
* `git`
* `uv` or `pip`

### Initializing Environment
```bash
# Clone the repository
git clone https://github.com/udaydomadiya08/ai-dev-kit.git
cd ai-dev-kit

# Create a virtual environment and install in editable mode with development dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Running Tests and Linters
```bash
# Run pytest suite
pytest

# Run tests with coverage
pytest --cov=udk tests/

# Validate local code format and typing
ruff check .
mypy udk
```

---

## 3. Contribution Workflow

1. **Open an Issue**: For major changes or new adapters/skills, please open an issue first to discuss the scope and rationale.
2. **Branch Naming**: Use descriptive branch names:
   * `feat/add-new-skill-observability`
   * `fix/cursor-glob-parsing`
   * `docs/update-compatibility-matrix`
3. **Write Tests First**:
   * Any new adapter, CLI command, skill validator, or security rule must include automated pytest tests.
   * Regression tests are required for any bug fixes.
4. **Follow Engineering Principles**:
   * Keep modules focused and interfaces explicit.
   * Do not introduce heavy dependencies when standard library features suffice.
   * Ensure cross-platform compatibility (macOS, Linux, Windows).

---

## 4. Submitting a Pull Request

* PR titles should follow Conventional Commits (e.g. `feat: add support for new agent`, `fix: handle crlf in manifest`).
* Fill out the [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md).
* Verify that all CI checks pass locally before opening or updating your PR.
* PRs require at least one approving review from a maintainer.
