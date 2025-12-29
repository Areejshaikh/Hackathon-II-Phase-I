"""State manager agent for in-memory task state.

Provides functions for:
- initialize_state() - Initialize or reset state
- add_task() - Create new tasks with auto-ID
- get_task() - Retrieve task by ID
- list_tasks() - List all tasks
- update_task() - Update task fields
- toggle_task_status() - Toggle pending/completed
- complete_task() - Mark task as completed
- delete_task() - Delete task by ID
- get_next_id() - Generate next available ID
"""
from typing import Optional
from src.models import Task, TaskStatus, TaskPriority


# Module-level state (singleton pattern)
_tasks: list[Task] = []
_next_id: int = 1


def initialize_state(initial_tasks: Optional[list[Task]] = None) -> None:
    """Initialize or reset the in-memory state.

    Args:
        initial_tasks: Optional list of tasks to load (from storage).
    """
    global _tasks, _next_id
    _tasks = list(initial_tasks) if initial_tasks else []
    _next_id = 1
    if _tasks:
        _next_id = max(task.id for task in _tasks) + 1


def get_next_id() -> int:
    """Generate the next available task ID.

    Returns:
        New unique ID (max existing ID + 1).
    """
    return _next_id


def add_task(
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[list[str]] = None,
) -> Task:
    """Create and add a new task.

    Args:
        title: Task title (required).
        description: Task description (optional).
        priority: "low", "medium", or "high" (optional).
        tags: List of tags (optional).

    Returns:
        The newly created Task object.
    """
    global _next_id

    task = Task(
        id=_next_id,
        title=title,
        description=description,
        status=TaskStatus.PENDING,
        priority=TaskPriority(priority) if priority else None,
        tags=tags,
    )

    _tasks.append(task)
    _next_id = task.id + 1

    return task


def get_task(task_id: int) -> Optional[Task]:
    """Retrieve a task by ID.

    Args:
        task_id: The task ID to find.

    Returns:
        Task object if found, None otherwise.
    """
    for task in _tasks:
        if task.id == task_id:
            return task
    return None


def list_tasks() -> list[Task]:
    """Get all tasks.

    Returns:
        List of all tasks (unsorted).
    """
    return list(_tasks)


def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[list[str]] = None,
) -> Optional[Task]:
    """Update an existing task (not status).

    Args:
        task_id: The task ID to update.
        title: New title (optional).
        description: New description (optional).
        priority: New priority (optional).
        tags: New tags list (optional).

    Returns:
        Updated Task object if found, None otherwise.
    """
    task = get_task(task_id)
    if task is None:
        return None

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if priority is not None:
        task.priority = TaskPriority(priority)
    if tags is not None:
        task.tags = tags

    task.updated_at = task._now_utc()

    return task


def toggle_task_status(task_id: int) -> Optional[Task]:
    """Toggle task status between pending and completed.

    Args:
        task_id: The task ID to toggle.

    Returns:
        Updated Task object if found, None otherwise.
    """
    task = get_task(task_id)
    if task is None:
        return None

    if task.status == TaskStatus.PENDING:
        task.status = TaskStatus.COMPLETED
    else:
        task.status = TaskStatus.PENDING

    task.updated_at = task._now_utc()
    return task


def complete_task(task_id: int) -> Optional[Task]:
    """Set task status to completed.

    Args:
        task_id: The task ID to complete.

    Returns:
        Updated Task object if found, None otherwise.
    """
    task = get_task(task_id)
    if task is None:
        return None

    task.status = TaskStatus.COMPLETED
    task.updated_at = task._now_utc()
    return task


def delete_task(task_id: int) -> Optional[Task]:
    """Delete a task by ID.

    Args:
        task_id: The task ID to delete.

    Returns:
        Deleted Task object if found, None otherwise.
    """
    task = get_task(task_id)
    if task is None:
        return None

    _tasks.remove(task)
    return task
