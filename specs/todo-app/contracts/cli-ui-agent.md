# CLI UI Agent API Contract

**Agent**: `todo-cli-ui-agent`
**Purpose**: All rendering and input (uses `rich`)
**Output**: stdout for results, stderr for errors

## Colors

The agent uses `rich` with the following color scheme:

| Element | Color | Usage |
|---------|-------|-------|
| Headers/Titles | Cyan | Section headers, task titles |
| Menus/Warnings | Yellow | Menu options, warning messages |
| Success | Green | Confirmation messages, completed tasks |
| Errors | Red | Error messages, deletion confirmations |
| Info | Blue | Informational messages, help text |

## Interface

### Display Welcome

```python
def display_welcome() -> None:
    """Display welcome message and task count."""
```

### Display Main Menu

```python
def display_main_menu() -> int:
    """
    Display the numbered main menu.

    Returns:
        User's menu choice (1-8)
    """
```

### Display Tasks Table

```python
def display_tasks_table(tasks: list[Task], show_description: bool = False) -> None:
    """
    Display tasks in a colorful table.

    Args:
        tasks: List of tasks to display
        show_description: Include description column (default: False)
    """
```

### Display Task Details

```python
def display_task_details(task: Task) -> None:
    """
    Display full details of a single task.

    Args:
        task: Task object to display
    """
```

### Prompt for Task Creation

```python
def prompt_add_task() -> dict:
    """
    Prompt user for new task details.

    Returns:
        Dict with keys: title, description, priority, tags
    """
```

### Prompt for Task Update

```python
def prompt_update_task(task: Task) -> dict:
    """
    Prompt user for updated task details (with current values as defaults).

    Args:
        task: Current task to update

    Returns:
        Dict with keys: title, description, priority, tags
    """
```

### Prompt for Task ID

```python
def prompt_task_id(prompt: str = "Enter task ID") -> int:
    """
    Prompt user for a task ID.

    Args:
        prompt: Custom prompt message

    Returns:
        Task ID as integer
    """
```

### Prompt for Confirmation

```python
def prompt_confirmation(message: str) -> bool:
    """
    Prompt user for yes/no confirmation.

    Args:
        message: Confirmation message

    Returns:
        True for yes, False for no
    """
```

### Prompt for Search

```python
def prompt_search() -> str:
    """
    Prompt user for search keyword.

    Returns:
        Search query string
    """
```

### Prompt for Filters

```python
def prompt_filters() -> dict:
    """
    Prompt user for filter criteria.

    Returns:
        Dict with keys: status, priority, tags (any may be None)
    """
```

### Prompt for Sort

```python
def prompt_sort() -> tuple[str, bool]:
    """
    Prompt user for sort options.

    Returns:
        Tuple of (sort_field, reverse)
    """
```

### Display Success

```python
def display_success(message: str) -> None:
    """
    Display success message in green.

    Args:
        message: Success message
    """
```

### Display Error

```python
def display_error(message: str) -> None:
    """
    Display error message in red.

    Args:
        message: Error message
    """
```

### Display Warning

```python
def display_warning(message: str) -> None:
    """
    Display warning message in yellow.

    Args:
        message: Warning message
    """
```

### Display Info

```python
def display_info(message: str) -> None:
    """
    Display info message in blue.

    Args:
        message: Info message
    """
```

### Display Empty State

```python
def display_empty_state(message: str) -> None:
    """
    Display message when no tasks match criteria.

    Args:
        message: Empty state message
    """
```

### Display Goodbye

```python
def display_goodbye() -> None:
    """Display goodbye message on exit."""
```

## Error Taxonomy

| Error | Condition | Display | Recovery |
|-------|-----------|---------|----------|
| InvalidMenuChoice | Non-1-8 input | Error + re-prompt | Re-prompt |
| InvalidTaskID | Non-integer or not found | Error + re-prompt | Re-prompt |
| EmptyTitle | Empty title submitted | Error + re-prompt | Re-prompt |
| ConfirmationDenied | User says no to delete | Warning | Abort action |

## Example Usage

```python
from agents.cli_ui_agent import (
    display_welcome, display_main_menu, display_tasks_table,
    display_task_details, display_success, display_error,
    prompt_add_task, prompt_task_id, prompt_confirmation
)

# Show welcome
display_welcome()

# Get menu choice
choice = display_main_menu()

# Display tasks
display_tasks_table(tasks)

# Display single task
display_task_details(task)

# Get new task input
task_data = prompt_add_task()

# Confirm deletion
if prompt_confirmation(f"Delete task {task_id}?"):
    delete_task(task_id)
    display_success("Task deleted")
else:
    display_warning("Deletion cancelled")
```

## Rich Components Used

- `Console`: Main console for output
- `Table`: Task listing
- `Panel`: Task details
- `Prompt`: User input
- `Text`: Colored text
- `Rule`: Section separators
- `Status`: Loading indicators
