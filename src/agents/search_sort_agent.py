"""Search-sort agent for task search, filter, and sort operations.

Provides functions for:
- search_tasks() - Keyword search in title/description
- filter_tasks() - Filter by status, priority, tags
- search_and_filter() - Combined search and filter
- sort_tasks() - Sort by ID, priority, created, title
- process_tasks() - Complete search/filter/sort pipeline
"""
from typing import Optional
from src.models import Task, TaskStatus, TaskPriority


# Priority order for sorting (high value = higher priority)
PRIORITY_ORDER = {
    TaskPriority.HIGH: 3,
    TaskPriority.MEDIUM: 2,
    TaskPriority.LOW: 1,
    None: 0,
}


def search_tasks(tasks: list[Task], query: str) -> list[Task]:
    """Search tasks by keyword in title and description.

    Args:
        tasks: List of tasks to search.
        query: Search keyword (case-insensitive).

    Returns:
        List of matching tasks.
    """
    if not query:
        return list(tasks)

    query_lower = query.lower()

    matching = []
    for task in tasks:
        # Search in title
        if query_lower in task.title.lower():
            matching.append(task)
            continue

        # Search in description
        if task.description and query_lower in task.description.lower():
            matching.append(task)

    return matching


def filter_tasks(
    tasks: list[Task],
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[list[str]] = None,
) -> list[Task]:
    """Filter tasks by criteria.

    Args:
        tasks: List of tasks to filter.
        status: Filter by "pending" or "completed" (optional).
        priority: Filter by "low", "medium", or "high" (optional).
        tags: Filter by tags (task must have ALL specified tags) (optional).

    Returns:
        List of matching tasks.
    """
    filtered = list(tasks)

    # Filter by status
    if status:
        filtered = [t for t in filtered if t.status.value == status]

    # Filter by priority
    if priority:
        filtered = [t for t in filtered if t.priority and t.priority.value == priority]

    # Filter by tags (AND logic - must have ALL specified tags)
    if tags:
        filtered = [
            t for t in filtered
            if t.tags and all(tag in t.tags for tag in tags)
        ]

    return filtered


def search_and_filter(
    tasks: list[Task],
    query: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[list[str]] = None,
) -> list[Task]:
    """Search and filter combined.

    Args:
        tasks: List of tasks.
        query: Search keyword (optional).
        status: Filter by status (optional).
        priority: Filter by priority (optional).
        tags: Filter by tags (optional).

    Returns:
        List of matching, filtered tasks.
    """
    # First filter
    result = list(tasks)

    # Then search
    if query:
        result = search_tasks(result, query)

    # Then filter
    if status or priority or tags:
        result = filter_tasks(result, status=status, priority=priority, tags=tags)

    return result


def sort_tasks(tasks: list[Task], by: str = "id", reverse: bool = False) -> list[Task]:
    """Sort tasks by specified criteria.

    Args:
        tasks: List of tasks to sort.
        by: Sort field - "id", "priority", "created", "title".
        reverse: Reverse order (descending if True).

    Returns:
        Sorted list of tasks.
    """
    sorted_tasks = list(tasks)

    if by == "id":
        sorted_tasks.sort(key=lambda t: t.id, reverse=reverse)
    elif by == "priority":
        sorted_tasks.sort(
            key=lambda t: PRIORITY_ORDER.get(t.priority, 0),
            reverse=reverse,
        )
    elif by == "created":
        sorted_tasks.sort(key=lambda t: t.created_at, reverse=reverse)
    elif by == "title":
        sorted_tasks.sort(key=lambda t: t.title.lower(), reverse=reverse)
    else:
        # Default to ID
        sorted_tasks.sort(key=lambda t: t.id, reverse=reverse)

    return sorted_tasks


def process_tasks(
    tasks: list[Task],
    query: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[list[str]] = None,
    sort_by: str = "id",
    reverse: bool = False,
) -> list[Task]:
    """Complete search, filter, and sort pipeline.

    Args:
        tasks: List of tasks.
        query: Search keyword (optional).
        status: Filter by status (optional).
        priority: Filter by priority (optional).
        tags: Filter by tags (optional).
        sort_by: Sort field (default: "id").
        reverse: Reverse order (default: False).

    Returns:
        Processed list of tasks.
    """
    # Search and filter
    result = search_and_filter(
        tasks,
        query=query,
        status=status,
        priority=priority,
        tags=tags,
    )

    # Sort
    result = sort_tasks(result, by=sort_by, reverse=reverse)

    return result
