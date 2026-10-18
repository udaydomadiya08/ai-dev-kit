"""
Agent adapters package for Universal AI Dev Kit.
"""

from udk.adapters.base import AgentAdapter, Diagnostic, GenerationContext
from udk.adapters.registry import (
    get_adapter,
    get_available_adapter_ids,
    list_adapters,
)

__all__ = [
    "AgentAdapter",
    "Diagnostic",
    "GenerationContext",
    "get_adapter",
    "get_available_adapter_ids",
    "list_adapters",
]
