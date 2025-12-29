# Storage Agent API Contract

**Agent**: `todo-storage-agent`
**Purpose**: Load/save `tasks.json` only
**Persistence**: JSON file in repository root

## Interface

### Load Tasks

```python
def load_tasks(path: Path) -> list[Task]:
    """
    Load all tasks from JSON file.

    Args:
        path: Path to tasks.json file

    Returns:
        List of Task objects, empty list if file doesn't exist

    Raises:
        FileNotFoundError: If path doesn't exist (shouldn't happen - create empty file)
        json.JSONDecodeError: If file contains invalid JSON
        PermissionError: If file cannot be read
    """
```

### Save Tasks

```python
def save_tasks(tasks: list[Task], path: Path) -> None:
    """
    Save all tasks to JSON file with atomic write.

    Args:
        tasks: List of Task objects to save
        path: Path to tasks.json file

    Raises:
        PermissionError: If file cannot be written
        OSError: For other file system errors
    """
```

### Ensure File Exists

```python
def ensure_file_exists(path: Path) -> None:
    """
    Create tasks.json with empty collection if it doesn't exist.

    Args:
        path: Path to tasks.json file
    """
```

## File Format

See `../data-model.md` for the complete JSON schema.

## Error Taxonomy

| Error | Status Code | User Message | Recovery |
|-------|-------------|--------------|----------|
| FileNotFoundError | N/A (create file) | "Created new tasks file" | Auto-create |
| JSONDecodeError | N/A | "Invalid tasks file - backup created" | Backup + recreate |
| PermissionError | N/A | "Permission denied - check file permissions" | User action required |
| OSError | N/A | "Unable to save tasks" | Retry or user action |

## Example Usage

```python
from pathlib import Path
from agents.storage_agent import load_tasks, save_tasks

TASKS_PATH = Path("tasks.json")

# Load on startup
tasks = load_tasks(TASKS_PATH)

# Save after mutations
save_tasks(tasks, TASKS_PATH)
```
