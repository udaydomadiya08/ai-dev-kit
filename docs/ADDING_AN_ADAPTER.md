# Guide: Adding a New Agent Adapter

This guide explains how to implement, test, and register a new agent adapter in the **Universal AI Dev Kit** (`udk`).

---

## 1. Adapter Architecture Overview

An **Agent Adapter** translates canonical knowledge (principles, engineering standards, workflows, safety invariants) and project profiles into target-specific configuration files expected by an AI agent or editor.

All adapters inherit from `AgentAdapter` in `udk.adapters.base`.

---

## 2. Step-by-Step Implementation

### Step 1: Create the Adapter File
Create a new Python module in `udk/adapters/<my_agent>.py`:

```python
from __future__ import annotations
from pathlib import Path
from typing import Dict, List
from udk.adapters.base import AgentAdapter, Diagnostic, GenerationContext


class MyAgentAdapter(AgentAdapter):
    @property
    def id(self) -> str:
        return "my-agent"  # Unique URL-friendly slug

    @property
    def name(self) -> str:
        return "My Custom Agent"

    @property
    def description(self) -> str:
        return "Generates my-agent.conf for custom coding agent."

    def supported_artifacts(self) -> List[str]:
        return ["my-agent.conf"]

    def generate(self, context: GenerationContext) -> Dict[str, str]:
        lines = [self.banner()]
        lines.append(f"# Configuration for {context.project_name}\n")
        lines.append("## Safety Rules\n")
        lines.append(context.safety.strip() + "\n")
        lines.append("## Principles\n")
        lines.append(context.principles.strip() + "\n")

        # Map profile commands
        commands = context.profile_data.get("commands", {})
        if commands:
            lines.append("## Commands\n")
            for k, v in commands.items():
                lines.append(f"{k} = {v}")

        return {"my-agent.conf": "\n".join(lines).strip() + "\n"}

    def validate(self, workspace_root: Path) -> List[Diagnostic]:
        diagnostics = super().validate(workspace_root)
        target = workspace_root / "my-agent.conf"
        if target.is_file():
            content = target.read_text(encoding="utf-8")
            if "Safety Rules" not in content:
                diagnostics.append(
                    Diagnostic(
                        severity="error",
                        file_path="my-agent.conf",
                        message="my-agent.conf missing mandatory Safety Rules section.",
                    )
                )
        return diagnostics
```

---

## 3. Register the Adapter

Open `udk/adapters/registry.py`:
1. Import your new adapter class:
   ```python
   from udk.adapters.my_agent import MyAgentAdapter
   ```
2. Add the class to `_ADAPTER_CLASSES`:
   ```python
   _ADAPTER_CLASSES: List[Type[AgentAdapter]] = [
       ...
       MyAgentAdapter,
   ]
   ```

---

## 4. Add Automated Tests

Create a test in `tests/test_adapters.py`:
```python
def test_my_agent_adapter(mock_context: GenerationContext):
    adapter = MyAgentAdapter()
    output = adapter.generate(mock_context)
    assert "my-agent.conf" in output
    assert "Safety Rules" in output["my-agent.conf"]
```

Run pytest to verify:
```bash
pytest tests/test_adapters.py
```

---

## 5. Update Documentation

Add the new adapter to:
* `docs/COMPATIBILITY.md` (recording support tier and verified artifacts).
* `README.md` (in the supported agents list).
* `CHANGELOG.md` under `[Unreleased]`.
