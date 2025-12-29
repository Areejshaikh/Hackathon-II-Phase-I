"""Main agent for orchestrating the CLI Todo application.

Handles the main menu loop and delegates to other agents.
"""
from pathlib import Path
from src.models import TaskStatus
from src.agents import (
    load_tasks,
    save_tasks,
    initialize_state,
    add_task,
    get_task,
    list_tasks,
    update_task,
    toggle_task_status,
    complete_task,
    delete_task,
    process_tasks,
    display_welcome,
    display_tasks_table,
    display_task_details,
    display_success,
    display_error,
    display_warning,
    display_goodbye,
    display_main_menu,
    prompt_task_id,
    prompt_confirmation,
    prompt_add_task,
    prompt_update_task,
    prompt_search,
    prompt_filters,
    prompt_sort,
)


TASKS_PATH = Path("tasks.json")


def main():
    """Main entry point for the Todo CLI application."""
    # Load tasks from storage
    tasks = load_tasks(TASKS_PATH)
    initialize_state(tasks)

    while True:
        try:
            choice = display_main_menu()

            if choice == 1:
                handle_add()
            elif choice == 2:
                handle_list()
            elif choice == 3:
                handle_view()
            elif choice == 4:
                handle_update()
            elif choice == 5:
                handle_complete()
            elif choice == 6:
                handle_delete()
            elif choice == 7:
                handle_search_filter()
            elif choice == 8:
                handle_quit()
                break
        except KeyboardInterrupt:
            handle_quit()
            break
        except Exception as e:
            display_error(f"An error occurred: {e}")


def handle_add():
    """Add a new task."""
    task_data = prompt_add_task()

    if not task_data["title"]:
        display_warning("Task cancelled - title is required.")
        return

    task = add_task(
        title=task_data["title"],
        description=task_data["description"],
        priority=task_data["priority"],
        tags=task_data["tags"],
    )

    # Save after mutation
    save_tasks(list_tasks(), TASKS_PATH)
    display_success(f"Task added successfully! (ID: {task.id})")


def handle_list():
    """List all tasks."""
    tasks = list_tasks()
    display_tasks_table(tasks)


def handle_view():
    """View a single task."""
    task_id = prompt_task_id("Enter task ID to view")
    task = get_task(task_id)

    if task is None:
        display_error(f"Task {task_id} not found.")
        return

    display_task_details(task)


def handle_update():
    """Update a task."""
    task_id = prompt_task_id("Enter task ID to update")
    task = get_task(task_id)

    if task is None:
        display_error(f"Task {task_id} not found.")
        return

    task_data = prompt_update_task(task)

    updated = update_task(
        task_id,
        title=task_data["title"],
        description=task_data["description"],
        priority=task_data["priority"],
        tags=task_data["tags"],
    )

    if updated:
        save_tasks(list_tasks(), TASKS_PATH)
        display_success(f"Task {task_id} updated.")
    else:
        display_error(f"Failed to update task {task_id}.")


def handle_complete():
    """Complete a task."""
    task_id = prompt_task_id("Enter task ID to complete")
    task = get_task(task_id)

    if task is None:
        display_error(f"Task {task_id} not found.")
        return

    if task.status == TaskStatus.COMPLETED:
        display_warning(f"Task {task_id} is already completed.")
        return

    completed = complete_task(task_id)

    if completed:
        save_tasks(list_tasks(), TASKS_PATH)
        display_success(f"Task {task_id} marked as completed!")
    else:
        display_error(f"Failed to complete task {task_id}.")


def handle_delete():
    """Delete a task with confirmation."""
    task_id = prompt_task_id("Enter task ID to delete")
    task = get_task(task_id)

    if task is None:
        display_error(f"Task {task_id} not found.")
        return

    display_warning(f"Delete task '{task.title}'?")

    if not prompt_confirmation("Are you sure"):
        display_info("Deletion cancelled.")
        return

    deleted = delete_task(task_id)

    if deleted:
        save_tasks(list_tasks(), TASKS_PATH)
        display_success(f"Task {task_id} deleted.")
    else:
        display_error(f"Failed to delete task {task_id}.")


def handle_search_filter():
    """Search and filter tasks."""
    query = prompt_search()
    filters = prompt_filters()

    # Get all tasks
    all_tasks = list_tasks()

    # Process tasks through search/filter/sort pipeline
    results = process_tasks(
        all_tasks,
        query=query if query else None,
        status=filters.get("status"),
        priority=filters.get("priority"),
        tags=filters.get("tags"),
    )

    if results:
        # Offer to sort
        sort_by, reverse = prompt_sort()
        results = process_tasks(
            results,
            sort_by=sort_by,
            reverse=reverse,
        )

    display_tasks_table(results)


def handle_quit():
    """Quit the application with auto-save."""
    save_tasks(list_tasks(), TASKS_PATH)
    display_goodbye()
