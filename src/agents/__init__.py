# src/agents/__init__.py

from src.agents.storage_agent import load_tasks, save_tasks, ensure_file_exists
from src.agents.state_manager import (
    initialize_state,
    add_task,
    get_task,
    list_tasks,
    update_task,
    toggle_task_status,
    complete_task,
    delete_task,
    get_next_id,
)
from src.agents.search_sort_agent import (
    search_tasks,
    filter_tasks,
    search_and_filter,
    sort_tasks,
    process_tasks,
)
from src.agents.cli_ui_agent import (
    display_welcome,
    display_main_menu,
    display_tasks_table,
    display_task_details,
    display_success,
    display_error,
    display_warning,
    display_info,
    display_empty_state,
    display_goodbye,
    prompt_task_id,
    prompt_confirmation,
    prompt_add_task,
    prompt_update_task,
    prompt_search,
    prompt_filters,
    prompt_sort,
)

__all__ = [
    # storage
    "load_tasks",
    "save_tasks",
    "ensure_file_exists",
    # state
    "initialize_state",
    "add_task",
    "get_task",
    "list_tasks",
    "update_task",
    "toggle_task_status",
    "complete_task",
    "delete_task",
    "get_next_id",
    # search/sort
    "search_tasks",
    "filter_tasks",
    "search_and_filter",
    "sort_tasks",
    "process_tasks",
    # cli-ui
    "display_welcome",
    "display_main_menu",
    "display_tasks_table",
    "display_task_details",
    "display_success",
    "display_error",
    "display_warning",
    "display_info",
    "display_empty_state",
    "display_goodbye",
    "prompt_task_id",
    "prompt_confirmation",
    "prompt_add_task",
    "prompt_update_task",
    "prompt_search",
    "prompt_filters",
    "prompt_sort",
]
