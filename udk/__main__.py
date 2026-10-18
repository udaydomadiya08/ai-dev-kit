"""
Executable module entrypoint for python -m udk.
"""

import sys

from udk.cli import main

if __name__ == "__main__":
    sys.exit(main())
