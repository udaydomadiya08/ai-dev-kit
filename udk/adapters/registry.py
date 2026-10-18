"""
Adapter registry for Universal AI Dev Kit (UDK).
Provides registration, lookup, and discovery for all supported agent adapters.
"""

from __future__ import annotations

from udk.adapters.agents_md import AgentsMdAdapter
from udk.adapters.antigravity import AntigravityAdapter
from udk.adapters.base import AgentAdapter
from udk.adapters.claude_code import ClaudeCodeAdapter
from udk.adapters.cursor import CursorAdapter
from udk.adapters.generic import GenericExportAdapter
from udk.adapters.opencode import OpenCodeAdapter

_ADAPTER_CLASSES: list[type[AgentAdapter]] = [
    AgentsMdAdapter,
    ClaudeCodeAdapter,
    AntigravityAdapter,
    CursorAdapter,
    OpenCodeAdapter,
    GenericExportAdapter,
]

_REGISTRY: dict[str, AgentAdapter] = {cls().id: cls() for cls in _ADAPTER_CLASSES}


def get_adapter(adapter_id: str) -> AgentAdapter | None:
    """Retrieve an instantiated adapter by its unique slug ID."""
    return _REGISTRY.get(adapter_id)


def list_adapters() -> list[AgentAdapter]:
    """Return all registered agent adapters sorted by ID."""
    return sorted(_REGISTRY.values(), key=lambda a: a.id)


def get_available_adapter_ids() -> list[str]:
    """Return a list of all valid adapter identifiers."""
    return sorted(_REGISTRY.keys())
