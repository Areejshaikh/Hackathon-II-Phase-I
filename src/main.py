"""Main entry point for the Todo CLI application.

Usage:
    python src/main.py
    or
    uv run src/main.py
"""
from pathlib import Path
from src.agents.main_agent import main


if __name__ == "__main__":
    import sys
    import io

    # System-wide UTF-8 encoding for Windows CLI
    if sys.platform == "win32":
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    main()
