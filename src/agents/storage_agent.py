"""Storage agent for JSON file persistence.

Provides functions for:
- load_tasks(): Load tasks from JSON file
- save_tasks(): Save tasks with atomic write
- ensure_file_exists(): Create empty tasks file if needed
"""
import json
from pathlib import Path
from datetime import datetime, timezone
from src.models import Task


TASKS_PATH = Path("tasks.json")


def ensure_file_exists(path: Path) -> None:
    """Create tasks.json with empty collection if it doesn't exist.

    Args:
        path: Path to the tasks.json file.
    """
    if path.exists():
        return

    initial_data = {
        "tasks": [],
        "version": 1,
        "last_modified": datetime.now(timezone.utc).isoformat() + "Z"
    }

    # Create parent directories if they don't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(initial_data, f, indent=2)


def load_tasks(path: Path) -> list[Task]:
    """Load all tasks from JSON file.

    Args:
        path: Path to tasks.json file.

    Returns:
        List of Task objects, empty list if file doesn't exist.
    """
    if not path.exists():
        return []

    with open(path, "r") as f:
        data = json.load(f)

    tasks = []
    for task_data in data.get("tasks", []):
        tasks.append(Task.from_dict(task_data))

    return tasks


def save_tasks(tasks: list[Task], path: Path) -> None:
    """Save all tasks to JSON file with atomic write.

    Args:
        tasks: List of Task objects to save.
        path: Path to tasks.json file.
    """
    # Create parent directories if they don't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # Create temp file for atomic write
    temp_path = path.with_suffix(".tmp")

    data = {
        "tasks": [task.to_dict() for task in tasks],
        "version": 1,
        "last_modified": datetime.now(timezone.utc).isoformat() + "Z"
    }

    # Write to temp file
    with open(temp_path, "w") as f:
        json.dump(data, f, indent=2)

    # Atomic replace
    temp_path.replace(path)
