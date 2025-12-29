# Main Agent API Contract

**Agent**: `todo-main-agent`
**Purpose**: Orchestrates flow, main loop, delegates to other agents
**Entry Point**: `src/main.py`

## Main Loop

```python
def main():
    """
    Main entry point for the Todo CLI application.

    Flow:
    1. Load tasks from storage
    2. Display welcome message
    3. Enter main menu loop
    4. Handle user choices
    5. Save on exit
    """
```

## CLI Flow

```
Startup → load tasks → main menu loop:
1. Add    2. List    3. View    4. Update    5. Complete    6. Delete    7. Search/Filter    8. Quit
```

## Menu Handlers

### Handle Add

```python
def handle_add() -> None:
    """Add a new task."""
    # 1. Prompt for task details (cli_ui_agent)
    # 2. Create task (state_manager)
    # 3. Save (storage_agent)
    # 4. Display success (cli_ui_agent)
```

### Handle List

```python
def handle_list() -> None:
    """List all tasks."""
    # 1. Get all tasks (state_manager)
    # 2. Display table (cli_ui_agent)
```

### Handle View

```python
def handle_view() -> None:
    """View a single task."""
    # 1. Prompt for task ID (cli_ui_agent)
    # 2. Get task (state_manager)
    # 3. Display details (cli_ui_agent)
```

### Handle Update

```python
def handle_update() -> None:
    """Update a task."""
    # 1. Prompt for task ID (cli_ui_agent)
    # 2. Get task (state_manager)
    # 3. Prompt for updates (cli_ui_agent)
    # 4. Update task (state_manager)
    # 5. Save (storage_agent)
    # 6. Display success (cli_ui_agent)
```

### Handle Complete

```python
def handle_complete() -> None:
    """Complete a task (toggle status)."""
    # 1. Prompt for task ID (cli_ui_agent)
    # 2. Toggle status (state_manager)
    # 3. Save (storage_agent)
    # 4. Display success (cli_ui_agent)
```

### Handle Delete

```python
def handle_delete() -> None:
    """Delete a task with confirmation."""
    # 1. Prompt for task ID (cli_ui_agent)
    # 2. Confirm deletion (cli_ui_agent)
    # 3. Delete task (state_manager)
    # 4. Save (storage_agent)
    # 5. Display success (cli_ui_agent)
```

### Handle Search/Filter

```python
def handle_search_filter() -> None:
    """Search and filter tasks."""
    # 1. Prompt for search query (cli_ui_agent)
    # 2. Prompt for filters (cli_ui_agent)
    # 3. Get all tasks (state_manager)
    # 4. Search and filter (search_sort_agent)
    # 5. Display results (cli_ui_agent)
    # 6. Offer to sort (cli_ui_agent)
```

### Handle Quit

```python
def handle_quit() -> bool:
    """
    Quit the application.

    Returns:
        True to exit, False to stay
    """
    # 1. Save tasks (storage_agent)
    # 2. Display goodbye (cli_ui_agent)
    # 3. Return True to exit
```

## Error Handling

```python
def handle_error(error: Exception) -> None:
    """
    Handle unexpected errors gracefully.

    Args:
        error: The caught exception
    """
    # 1. Log error (for debugging)
    # 2. Display user-friendly message (cli_ui_agent)
    # 3. Continue main loop
```

## Agent Communication

The main agent delegates to other agents:

```
┌─────────────────────────────────────┐
│         main_agent                  │
│    (orchestrates flow)              │
└─────┬─────┬─────┬─────┬─────────────┘
      │     │     │     │
      ▼     ▼     ▼     ▼
┌─────────┬─────────┬──────────────┐
│cli_ui   │state_   │search_sort   │
│_agent   │manager  │_agent        │
└─────────┴─────────┴──────────────┘
                │
                ▼
        ┌──────────────┐
        │storage_agent │
        └──────────────┘
```

## Entry Point

```python
# src/main.py
from agents.main_agent import main

if __name__ == "__main__":
    main()
```

## Example Session

```
$ uv run src/main.py

╭────────────────────────────────────────╮
│         Todo CLI - Welcome!            │
╰────────────────────────────────────────╯

Tasks loaded: 5

╭────────────────────────────────────────╮
│  Main Menu                             │
╰────────────────────────────────────────╮
1. Add Task
2. List Tasks
3. View Task
4. Update Task
5. Complete Task
6. Delete Task
7. Search/Filter
8. Quit

Enter your choice [1-8]: 1

Enter task title: Buy groceries
Enter description (optional): Milk, eggs, bread
Priority (low/medium/high) [medium]:
Tags (comma-separated, optional): shopping, home

✓ Task added successfully!

[returns to main menu]
```
