"""
Unit tests for Python starter template.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root containing main.py is on sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

try:
    from main import format_greeting
except ImportError:
    from udk.templates.python_cli.main import format_greeting


def test_format_greeting():
    assert format_greeting("Alice") == "Hello, Alice!"
    assert format_greeting("") == "Hello, World!"
    assert format_greeting("   ") == "Hello, World!"
