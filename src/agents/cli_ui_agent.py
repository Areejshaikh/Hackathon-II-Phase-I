"""CLI UI agent for colorful terminal output.

Provides functions for:
- display_* - Output functions (welcome, table, details, messages)
- prompt_* - User input functions

Uses 'rich' library for colorful output:
- Cyan: Headers/titles
- Yellow: Menus/warnings
- Green: Success
- Red: Errors
- Blue: Info
"""
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
from rich import print as rprint
from src.models import Task, TaskStatus
from src.agents.state_manager import list_tasks


# Custom theme with specified colors
console = Console()


def display_welcome() -> None:
    """Display welcome message and task count."""
    tasks = list_tasks()
    count = len(tasks)

    title = Text("Todo CLI - Welcome!", style="bold cyan")
    subtitle = Text(f"Tasks loaded: {count}", style="blue")

    panel = Panel.fit(
        Text.assemble(title, "\n", subtitle),
        title="[cyan]Todo CLI[/cyan]",
        border_style="cyan",
    )
    console.print(panel)


def display_main_menu() -> int:
    """Display the numbered main menu.

    Returns:
        User's menu choice (1-9).
    """
    display_welcome()

    menu = Table(show_header=False, box=None, padding=0)
    menu.add_row("[yellow]1.[/yellow] [cyan]Add Task[/cyan]")
    menu.add_row("[yellow]2.[/yellow] [cyan]List Tasks[/cyan]")
    menu.add_row("[yellow]3.[/yellow] [cyan]View Task[/cyan]")
    menu.add_row("[yellow]4.[/yellow] [cyan]Update Task[/cyan]")
    menu.add_row("[yellow]5.[/yellow] [cyan]Complete Task[/cyan]")
    menu.add_row("[yellow]6.[/yellow] [cyan]Delete Task[/cyan]")
    menu.add_row("[yellow]7.[/yellow] [cyan]Search/Filter[/cyan]")
    menu.add_row("[yellow]8.[/yellow] [cyan]Change Language (English / اردو)[/cyan]")
    menu.add_row("[yellow]9.[/yellow] [cyan]Voice Command Mode (Experimental)[/cyan]")
    menu.add_row("[yellow]10.[/yellow] [cyan]Quit[/cyan]")

    panel = Panel.fit(
        menu,
        title="[yellow]Main Menu[/yellow]",
        border_style="yellow",
    )
    console.print(panel)

    while True:
        try:
            choice = console.input("[cyan]Enter your choice [1-10]: [/cyan]")
            if choice in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
                return int(choice)
            console.print("[red]Invalid choice. Please enter 1-10.[/red]")
        except (KeyboardInterrupt, EOFError):
            return 10


def display_tasks_table(tasks: list[Task], show_description: bool = False) -> None:
    """Display tasks in a colorful table.

    Args:
        tasks: List of tasks to display.
        show_description: Include description column (default: False).
    """
    if not tasks:
        display_empty_state("No tasks found. Add a task to get started!")
        return

    table = Table(
        title="[cyan]Your Tasks[/cyan]",
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
        row_styles=["", "dim"],
    )

    table.add_column("ID", justify="right", style="cyan", width=4)
    table.add_column("Title", style="white")
    table.add_column("Status", style="green" if tasks and tasks[0].status == TaskStatus.COMPLETED else "yellow")
    table.add_column("Priority", justify="center")
    table.add_column("Tags", justify="left")

    if show_description:
        table.add_column("Description", style="blue")

    for task in tasks:
        # Status color
        if task.status == TaskStatus.COMPLETED:
            status_style = "[green]Completed[/green]"
        else:
            status_style = "[yellow]Pending[/yellow]"

        # Priority color
        priority = task.priority.value if task.priority else "-"
        if task.priority and task.priority.value == "high":
            priority = "[red]High[/red]"
        elif task.priority and task.priority.value == "medium":
            priority = "[yellow]Medium[/yellow]"
        elif task.priority and task.priority.value == "low":
            priority = "[blue]Low[/blue]"

        # Tags
        tags = ", ".join(task.tags) if task.tags else "-"

        row = [
            str(task.id),
            task.title,
            status_style,
            priority,
            f"[blue]{tags}[/blue]" if tags != "-" else "-",
        ]

        if show_description:
            row.append(task.description or "-")

        table.add_row(*row)

    console.print(table)


def display_task_details(task: Task) -> None:
    """Display full details of a single task.

    Args:
        task: Task object to display.
    """
    # Status color
    if task.status == TaskStatus.COMPLETED:
        status = "[green]Completed[/green]"
    else:
        status = "[yellow]Pending[/yellow]"

    # Priority color
    priority = task.priority.value if task.priority else "None"

    # Tags
    tags = ", ".join(task.tags) if task.tags else "None"

    details = Text()
    details.append(f"ID: ", style="cyan")
    details.append(str(task.id), style="white")
    details.append("\nTitle: ", style="cyan")
    details.append(task.title, style="white")

    if task.description:
        details.append("\nDescription: ", style="cyan")
        details.append(task.description, style="blue")

    details.append("\nStatus: ", style="cyan")
    details.append(status)
    details.append("\nPriority: ", style="cyan")
    if task.priority and task.priority.value == "high":
        details.append(priority, style="red")
    elif task.priority and task.priority.value == "medium":
        details.append(priority, style="yellow")
    elif task.priority and task.priority.value == "low":
        details.append(priority, style="blue")
    else:
        details.append(priority)

    details.append("\nTags: ", style="cyan")
    details.append(tags, style="blue")
    details.append("\nCreated: ", style="cyan")
    details.append(task.created_at.isoformat() + "Z", style="white")
    details.append("\nUpdated: ", style="cyan")
    details.append(task.updated_at.isoformat() + "Z", style="white")

    panel = Panel.fit(
        details,
        title=f"[cyan]Task #{task.id}[/cyan]",
        border_style="cyan",
    )
    console.print(panel)


def display_success(message: str) -> None:
    """Display success message in green.

    Args:
        message: Success message.
    """
    console.print(f"[green]OK[/green] {message}")


def display_error(message: str) -> None:
    """Display error message in red.

    Args:
        message: Error message.
    """
    console.print(f"[red]ERROR[/red] {message}")


def display_warning(message: str) -> None:
    """Display warning message in yellow.

    Args:
        message: Warning message.
    """
    console.print(f"[yellow]WARNING[/yellow] {message}")


def display_info(message: str) -> None:
    """Display info message in blue.

    Args:
        message: Info message.
    """
    console.print(f"[blue]INFO[/blue] {message}")


def display_empty_state(message: str) -> None:
    """Display message when no tasks match criteria.

    Args:
        message: Empty state message.
    """
    panel = Panel.fit(
        Text(message, style="yellow"),
        title="[yellow]Empty[/yellow]",
        border_style="yellow",
    )
    console.print(panel)


def display_goodbye() -> None:
    """Display goodbye message on exit."""
    panel = Panel.fit(
        Text("Goodbye! Tasks saved.", style="bold green"),
        title="[green]Todo CLI[/green]",
        border_style="green",
    )
    console.print(panel)


def prompt_task_id(prompt: str = "Enter task ID") -> int:
    """Prompt user for a task ID.

    Args:
        prompt: Custom prompt message.

    Returns:
        Task ID as integer.
    """
    while True:
        try:
            result = console.input(f"[cyan]{prompt}: [/cyan]")
            task_id = int(result)
            if task_id > 0:
                return task_id
            console.print("[red]Please enter a positive number.[/red]")
        except (KeyboardInterrupt, EOFError):
            raise
        except ValueError:
            console.print("[red]Please enter a valid number.[/red]")


def prompt_confirmation(message: str) -> bool:
    """Prompt user for yes/no confirmation.

    Args:
        message: Confirmation message.

    Returns:
        True for yes, False for no.
    """
    while True:
        try:
            result = console.input(f"[yellow]{message} (y/n): [/yellow]").lower()
            if result in ("y", "yes"):
                return True
            elif result in ("n", "no"):
                return False
            console.print("[yellow]Please enter y or n.[/yellow]")
        except (KeyboardInterrupt, EOFError):
            return False


def prompt_add_task() -> dict:
    """Prompt user for new task details.

    Returns:
        Dict with keys: title, description, priority, tags.
    """
    title = ""
    while not title.strip():
        try:
            title = console.input("[cyan]Enter task title: [/cyan]").strip()
            if not title:
                console.print("[red]Title cannot be empty.[/red]")
        except (KeyboardInterrupt, EOFError):
            return {"title": "", "description": None, "priority": None, "tags": None}

    try:
        description = console.input("[cyan]Enter description (optional): [/cyan]").strip()
        description = description if description else None
    except (KeyboardInterrupt, EOFError):
        description = None

    try:
        priority_input = console.input(
            "[cyan]Priority (low/medium/high) [medium]: [/cyan]"
        ).strip().lower()
        priority = priority_input if priority_input in ("low", "medium", "high") else "medium"
    except (KeyboardInterrupt, EOFError):
        priority = "medium"

    try:
        tags_input = console.input("[cyan]Tags (comma-separated, optional): [/cyan]").strip()
        tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else None
    except (KeyboardInterrupt, EOFError):
        tags = None

    return {
        "title": title,
        "description": description,
        "priority": priority,
        "tags": tags,
    }


def prompt_update_task(task: Task) -> dict:
    """Prompt user for updated task details (with current values as defaults).

    Args:
        task: Current task to update.

    Returns:
        Dict with keys: title, description, priority, tags.
    """
    # Title
    try:
        title_input = console.input(
            f"[cyan]Enter new title [{task.title}]: [/cyan]"
        ).strip()
        title = title_input if title_input else task.title
    except (KeyboardInterrupt, EOFError):
        title = task.title

    # Description
    current_desc = task.description or ""
    try:
        desc_input = console.input(
            f"[cyan]Enter new description [{current_desc}]: [/cyan]"
        ).strip()
        description = desc_input if desc_input else current_desc
        description = description if description else None
    except (KeyboardInterrupt, EOFError):
        description = task.description

    # Priority
    current_priority = task.priority.value if task.priority else "none"
    try:
        priority_input = console.input(
            f"[cyan]Priority (low/medium/high/none) [{current_priority}]: [/cyan]"
        ).strip().lower()
        if priority_input == "none":
            priority = None
        else:
            priority = priority_input if priority_input in ("low", "medium", "high") else (
                task.priority.value if task.priority else "medium"
            )
    except (KeyboardInterrupt, EOFError):
        priority = task.priority.value if task.priority else None

    # Tags
    current_tags = ", ".join(task.tags) if task.tags else ""
    try:
        tags_input = console.input(
            f"[cyan]Tags (comma-separated, optional) [{current_tags}]: [/cyan]"
        ).strip()
        if tags_input:
            tags = [t.strip() for t in tags_input.split(",") if t.strip()]
        else:
            tags = task.tags
    except (KeyboardInterrupt, EOFError):
        tags = task.tags

    return {
        "title": title,
        "description": description,
        "priority": priority,
        "tags": tags,
    }


def prompt_search() -> str:
    """Prompt user for search keyword.

    Returns:
        Search query string.
    """
    try:
        return console.input("[cyan]Enter search keyword: [/cyan]").strip()
    except (KeyboardInterrupt, EOFError):
        return ""


def prompt_filters() -> dict:
    """Prompt user for filter criteria.

    Returns:
        Dict with keys: status, priority, tags (any may be None).
    """
    filters = {}

    # Status filter
    try:
        status_input = console.input(
            "[cyan]Filter by status (pending/completed/empty for none): [/cyan]"
        ).strip().lower()
        if status_input in ("pending", "completed"):
            filters["status"] = status_input
    except (KeyboardInterrupt, EOFError):
        pass

    # Priority filter
    try:
        priority_input = console.input(
            "[cyan]Filter by priority (low/medium/high/empty for none): [/cyan]"
        ).strip().lower()
        if priority_input in ("low", "medium", "high"):
            filters["priority"] = priority_input
    except (KeyboardInterrupt, EOFError):
        pass

    return filters


def prompt_sort() -> tuple[str, bool]:
    """Prompt user for sort options.

    Returns:
        Tuple of (sort_field, reverse).
    """
    try:
        sort_input = console.input(
            "[cyan]Sort by (id/priority/created/title): [/cyan]"
        ).strip().lower()
        sort_by = sort_input if sort_input in ("id", "priority", "created", "title") else "id"

        reverse_input = console.input(
            "[cyan]Reverse order? (y/n) [n]: [/cyan]"
        ).strip().lower()
        reverse = reverse_input in ("y", "yes")

        return sort_by, reverse
    except (KeyboardInterrupt, EOFError):
        return "id", False
