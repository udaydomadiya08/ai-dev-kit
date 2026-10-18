"""
Minimal Python CLI entrypoint.
"""

from __future__ import annotations

import argparse
import sys


def format_greeting(name: str) -> str:
    cleaned = name.strip()
    if not cleaned:
        return "Hello, World!"
    return f"Hello, {cleaned}!"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sample CLI Starter")
    parser.add_argument("--name", default="World", help="Name to greet")
    args = parser.parse_args(argv)
    print(format_greeting(args.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
