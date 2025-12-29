# State Manager Agent API Contract

**Agent**: `todo-state-manager`
**Purpose**: In-memory tasks, ID generation, mutations
**State**: In-memory list of Task objects

## Interface

### Initialize

```python
def initialize_state(initial_tasks: list[Task] = None) -> None:
    """
    Initialize or reset the in-memory state.

    Args:
        initial_tasks: Optional list of tasks to load (from storage)
    """
```

### Add Task

```python
def add_task(title: str, description: str = None,
             priority: str = None, tags: list[str] = None) -> Task:
    """
    Create and add a new task.

    Args:
        title: Task title (required)
        description: Task description (optional)
        priority: "low", "medium", or "high" (optional)
        tags: List of tags (optional)

    Returns:
        The newly created Task object

    Raises:
        ValueError: If title is empty or invalid
    """
```

### Get Task

```python
def get_task(task_id: int) -> Task | None:
    """
    Retrieve a task by ID.

    Args:
        task_id: The task ID to find

    Returns:
        Task object if found, None otherwise
    """
```

### List Tasks

```python
def list_tasks() -> list[Task]:
    """
    Get all tasks.

    Returns:
        List of all tasks (unsorted, use search_sort_agent for sorting)
    """
```

### Update Task

```python
def update_task(task_id: int, title: str = None, description: str = None,
                priority: str = None, tags: list[str] = None) -> Task | None:
    """
    Update an existing task (not status - use toggle_status for that).

    Args:
        task_id: The task ID to update
        title: New title (optional)
        description: New description (optional)
        priority: New priority (optional)
        tags: New tags list (optional)

    Returns:
        Updated Task object if found, None otherwise

    Raises:
        ValueError: If title is empty
    """
```

### Toggle Task Status

```python
def toggle_task_status(task_id: int) -> Task | None:
    """
    Toggle task status between pending and completed.

    Args:
        task_id: The task ID to toggle

    Returns:
        Updated Task object if found, None otherwise
    """
```

### Complete Task

```python
def complete_task(task_id: int) -> Task | None:
    """
    Set task status to completed.

    Args:
        task_id: The task ID to complete

    Returns:
        Updated Task object if found, None otherwise
    """
```

### Delete Task

```python
def delete_task(task_id: int) -> Task | None:
    """
    Delete a task by ID.

    Args:
        task_id: The task ID to delete

    Returns:
        Deleted Task object if found, None otherwise
    """
```

### Get Next ID

```python
def get_next_id() -> int:
    """
    Generate the next available task ID.

    Returns:
        New unique ID (max existing ID + 1)
    """
```

## State Management

### In-Memory Store

```python
# Singleton state (module-level)
_tasks: list[Task] = []
_next_id: int = 1
_dirty: bool = False  # Flag for auto-save
```

### Auto-Save Pattern

```python
# After any mutation, set dirty flag
def add_task(...) -> Task:
    task = Task(...)
    _tasks.append(task)
    _dirty = True
    _next_id = max(_next_id, task.id + 1)
    return task

# Storage agent polls dirty flag or state manager calls save
def mark_clean():
    _dirty = False

def needs_save() -> bool:
    return _dirty
```

## Error Taxonomy

| Error | Condition | User Message | Recovery |
|-------|-----------|--------------|----------|
| TaskNotFoundError | task_id not found | "Task {id} not found" | Verify ID, try list |
| ValueError | Invalid input (empty title) | "Title cannot be empty" | Re-enter title |
| DuplicateIDError | ID collision (shouldn't happen) | "Internal error" | Restart app |

## Example Usage

```python
from agents.state_manager import (
    initialize_state, add_task, get_task,
    list_tasks, update_task, delete_task,
    toggle_task_status
)

# Initialize with loaded tasks
initialize_state(loaded_tasks)

# Add a task
task = add_task("Buy milk", priority="high", tags=["shopping"])

# Update
updated = update_task(task.id, description="Whole milk only")

# Toggle status
completed = toggle_task_status(task.id)

# Delete
deleted = delete_task(task.id)
```
