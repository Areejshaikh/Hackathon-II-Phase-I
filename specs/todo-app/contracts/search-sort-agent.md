# Search-Sort Agent API Contract

**Agent**: `todo-search-sort-agent`
**Purpose**: Search, filter, sort logic
**Input**: Task list from state_manager
**Output**: Filtered/sorted task list

## Interface

### Search Tasks

```python
def search_tasks(tasks: list[Task], query: str) -> list[Task]:
    """
    Search tasks by keyword in title and description.

    Args:
        tasks: List of tasks to search
        query: Search keyword (case-insensitive)

    Returns:
        List of matching tasks
    """
```

### Filter Tasks

```python
def filter_tasks(
    tasks: list[Task],
    status: str = None,
    priority: str = None,
    tags: list[str] = None
) -> list[Task]:
    """
    Filter tasks by criteria.

    Args:
        tasks: List of tasks to filter
        status: Filter by "pending" or "completed" (optional)
        priority: Filter by "low", "medium", or "high" (optional)
        tags: Filter by tags (task must have ALL specified tags) (optional)

    Returns:
        List of matching tasks
    """
```

### Combined Search and Filter

```python
def search_and_filter(
    tasks: list[Task],
    query: str = None,
    status: str = None,
    priority: str = None,
    tags: list[str] = None
) -> list[Task]:
    """
    Search and filter combined.

    Args:
        tasks: List of tasks
        query: Search keyword (optional)
        status: Filter by status (optional)
        priority: Filter by priority (optional)
        tags: Filter by tags (optional)

    Returns:
        List of matching, filtered tasks
    """
```

### Sort Tasks

```python
def sort_tasks(tasks: list[Task], by: str = "id", reverse: bool = False) -> list[Task]:
    """
    Sort tasks by specified criteria.

    Args:
        tasks: List of tasks to sort
        by: Sort field - "id", "priority", "created", "title"
        reverse: Reverse order (descending if True)

    Returns:
        Sorted list of tasks
    """
```

### Search, Filter, and Sort Combined

```python
def process_tasks(
    tasks: list[Task],
    query: str = None,
    status: str = None,
    priority: str = None,
    tags: list[str] = None,
    sort_by: str = "id",
    reverse: bool = False
) -> list[Task]:
    """
    Complete search, filter, and sort pipeline.

    Args:
        tasks: List of tasks
        query: Search keyword (optional)
        status: Filter by status (optional)
        priority: Filter by priority (optional)
        tags: Filter by tags (optional)
        sort_by: Sort field (default: "id")
        reverse: Reverse order (default: False)

    Returns:
        Processed list of tasks
    """
```

## Sort Options

| Sort Field | Description | Priority Order |
|------------|-------------|----------------|
| `"id"` | By task ID (default) | N/A |
| `"priority"` | By priority (high > medium > low) | high > medium > low |
| `"created"` | By creation date (newest first with reverse=True) | N/A |
| `"title"` | Alphabetically by title | N/A |
| `"status"` | By status (pending first, then completed) | pending < completed |

## Priority Mapping

```python
PRIORITY_ORDER = {
    "high": 3,
    "medium": 2,
    "low": 1,
    None: 0  # Tasks without priority
}
```

## Error Taxonomy

| Error | Condition | User Message | Recovery |
|-------|-----------|--------------|----------|
| ValueError | Invalid sort field | "Invalid sort option" | Valid options shown |
| ValueError | Invalid filter value | "Invalid filter value" | Valid options shown |

## Example Usage

```python
from agents.search_sort_agent import (
    search_tasks, filter_tasks, sort_tasks, process_tasks
)

all_tasks = list_tasks()

# Search
results = search_tasks(all_tasks, "groceries")

# Filter by status
pending = filter_tasks(all_tasks, status="pending")

# Filter by priority high
high_priority = filter_tasks(all_tasks, priority="high")

# Filter by multiple tags
tagged = filter_tasks(all_tasks, tags=["work", "urgent"])

# Sort by priority
sorted_by_priority = sort_tasks(all_tasks, by="priority", reverse=True)

# Combined pipeline
results = process_tasks(
    all_tasks,
    query="report",
    status="pending",
    priority="high",
    sort_by="priority",
    reverse=True
)
```
