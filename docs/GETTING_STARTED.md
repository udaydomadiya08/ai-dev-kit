# Getting Started with Universal AI Dev Kit (`udk`)

Welcome to the **Universal AI Dev Kit**! This guide takes you from zero to a fully initialized, verified project in under two minutes.

---

## 1. Prerequisites

* **Python**: Version 3.9 or newer (Python 3.11+ recommended).
* **Git**: Initialized in your project.
* Any supported AI coding agent or editor:
  * AGENTS.md compatible tools
  * Anthropic Claude Code
  * Google Antigravity
  * Cursor IDE
  * OpenCode

---

## 2. Installation

Install UDK locally in editable mode or into your preferred Python environment:

```bash
# Clone the repository
git clone https://github.com/udaydomadiya08/ai-dev-kit.git
cd ai-dev-kit

# Install the toolkit CLI
pip install -e .
```

Verify that the CLI is working:
```bash
udk --help
```

---

## 3. Initializing a Project

Navigate to your target project directory:
```bash
cd /path/to/my-project
```

### Automatic Stack Detection
UDK inspects your repository and automatically recommends the appropriate profile (Python, Web, AI/ML, Desktop, Mobile, or Minimal) and detected agent adapters:

```bash
udk init
```

### Specifying Profile and Adapters Explicitly
You can explicitly choose a profile and one or more target agent adapters:

```bash
# Initialize for Python with Claude Code and Cursor
udk init --profile python --agent claude-code --agent cursor

# Initialize a Web project with AGENTS.md
udk init --profile web --agent agents-md

# Preview what files will be created without touching disk
udk init --profile ai-ml --dry-run
```

---

## 4. Validating Your Project

UDK comes with a built-in static validator that checks configuration schemas, skill metadata, link integrity, and drift:

```bash
# Run project validation
udk validate

# Run complete diagnostic health checks
udk doctor
```

---

## 5. Daily Development Workflow

When working with an AI coding agent:
1. Open the repository in your agent or IDE (e.g. `cursor .` or run `claude`).
2. The agent automatically ingests the generated configuration (`AGENTS.md`, `CLAUDE.md`, or `.cursor/rules/`).
3. The agent adheres to your repository's build, test, and lint commands, non-negotiable safety rules, and canonical engineering principles.

---

## 6. Managing Updates and Safe Removal

### Previewing Drift and Updates
```bash
# Check if any managed files have drifted from manifest
udk diff

# Safely update files from toolkit (preserves user customizations)
udk update
```

### Clean Removal
If you ever want to remove UDK files from a project:
```bash
udk remove
```
UDK references `.udk/manifest.json` and deletes **only** the files it created. Your source code, commits, and custom files remain 100% untouched.
