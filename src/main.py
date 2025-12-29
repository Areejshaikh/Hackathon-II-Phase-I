"""Main entry point for the Todo CLI application.

Usage:
    python src/main.py
    or
    uv run src/main.py
"""
from pathlib import Path
from src.agents.main_agent import main


if __name__ == "__main__":
    main()
