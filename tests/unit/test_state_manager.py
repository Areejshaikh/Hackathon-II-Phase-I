"""Unit tests for state_manager module.

Tests cover:
- initialize_state() - State initialization
- add_task() - Task creation with auto-ID
- get_next_id() - ID generation
- get_task() - Task retrieval by ID
- list_tasks() - List all tasks
"""
import pytest
from src.models.task import Task, TaskStatus, TaskPriority
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


class TestInitializeState:
    """Tests for initialize_state() function."""

    def test_initialize_empty_state(self):
        """Should initialize with empty task list."""
        initialize_state([])

        result = list_tasks()
        assert result == []

    def test_initialize_with_tasks(self):
        """Should initialize with provided tasks."""
        tasks = [
            Task(id=1, title="Task 1", status=TaskStatus.PENDING),
            Task(id=2, title="Task 2", status=TaskStatus.COMPLETED),
        ]

        initialize_state(tasks)

        result = list_tasks()
        assert len(result) == 2
        assert result[0].title == "Task 1"
        assert result[1].title == "Task 2"

    def test_reset_state(self):
        """Should replace existing state with new tasks."""
        # Add some tasks first
        initialize_state([Task(id=1, title="Old", status=TaskStatus.PENDING)])

        # Reset with new tasks
        initialize_state([
            Task(id=10, title="New 1", status=TaskStatus.PENDING),
            Task(id=20, title="New 2", status=TaskStatus.PENDING),
        ])

        result = list_tasks()
        assert len(result) == 2
        assert result[0].id == 10


class TestGetNextId:
    """Tests for get_next_id() function."""

    def test_first_id_is_1(self):
        """First task should get ID 1."""
        initialize_state([])

        result = get_next_id()

        assert result == 1

    def test_id_after_single_task(self):
        """ID should be max + 1 after adding a task."""
        initialize_state([Task(id=1, title="Task", status=TaskStatus.PENDING)])

        result = get_next_id()

        assert result == 2

    def test_id_after_multiple_tasks(self):
        """ID should be max + 1 after adding multiple tasks."""
        initialize_state([
            Task(id=1, title="Task 1", status=TaskStatus.PENDING),
            Task(id=2, title="Task 2", status=TaskStatus.PENDING),
            Task(id=5, title="Task 3", status=TaskStatus.PENDING),
        ])

        result = get_next_id()

        assert result == 6

    def test_id_after_deletion(self):
        """ID should not reuse deleted task IDs."""
        initialize_state([
            Task(id=1, title="Task 1", status=TaskStatus.PENDING),
            Task(id=2, title="Task 2", status=TaskStatus.PENDING),
        ])
        delete_task(1)

        result = get_next_id()

        assert result == 3


class TestAddTask:
    """Tests for add_task() function."""

    def test_add_task_with_title_only(self):
        """Should create task with only required fields."""
        initialize_state([])

        task = add_task("Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.status == TaskStatus.PENDING
        assert task.description is None
        assert task.priority is None
        assert task.tags is None

    def test_add_task_with_all_fields(self):
        """Should create task with all optional fields."""
        initialize_state([])

        task = add_task(
            title="Complete report",
            description="Q4 summary",
            priority=TaskPriority.HIGH,
            tags=["work", "urgent"],
        )

        assert task.id == 1
        assert task.title == "Complete report"
        assert task.description == "Q4 summary"
        assert task.priority == TaskPriority.HIGH
        assert task.tags == ["work", "urgent"]

    def test_add_task_multiple(self):
        """Should auto-increment IDs for multiple tasks."""
        initialize_state([])

        task1 = add_task("Task 1")
        task2 = add_task("Task 2")
        task3 = add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_default_status_pending(self):
        """New tasks should default to pending status."""
        initialize_state([])

        task = add_task("New task")

        assert task.status == TaskStatus.PENDING

    def test_add_task_generates_timestamps(self):
        """New tasks should have auto-generated timestamps."""
        initialize_state([])

        task = add_task("Test task")

        assert task.created_at is not None
        assert task.updated_at is not None

    def test_added_task_is_retrievable(self):
        """Added task should be retrievable via get_task()."""
        initialize_state([])

        added = add_task(" retrievable task")
        retrieved = get_task(added.id)

        assert retrieved is not None
        assert retrieved.id == added.id
        assert retrieved.title == added.title

    def test_added_task_in_list(self):
        """Added task should appear in list_tasks()."""
        initialize_state([])

        add_task("New task")
        result = list_tasks()

        assert len(result) == 1
        assert result[0].title == "New task"


class TestGetTask:
    """Tests for get_task() function."""

    def test_get_existing_task(self):
        """Should return task if ID exists."""
        initialize_state([
            Task(id=1, title="Task 1", status=TaskStatus.PENDING),
            Task(id=2, title="Task 2", status=TaskStatus.PENDING),
        ])

        result = get_task(1)

        assert result is not None
        assert result.id == 1
        assert result.title == "Task 1"

    def test_get_nonexistent_task(self):
        """Should return None if ID doesn't exist."""
        initialize_state([
            Task(id=1, title="Task 1", status=TaskStatus.PENDING),
        ])

        result = get_task(999)

        assert result is None


class TestListTasks:
    """Tests for list_tasks() function."""

    def test_list_empty(self):
        """Should return empty list when no tasks."""
        initialize_state([])

        result = list_tasks()

        assert result == []

    def test_list_all_tasks(self):
        """Should return all tasks."""
        initialize_state([
            Task(id=1, title="Task 1", status=TaskStatus.PENDING),
            Task(id=2, title="Task 2", status=TaskStatus.COMPLETED),
            Task(id=3, title="Task 3", status=TaskStatus.PENDING),
        ])

        result = list_tasks()

        assert len(result) == 3

    def test_list_returns_task_objects(self):
        """Should return actual Task objects."""
        initialize_state([
            Task(id=1, title="Test", status=TaskStatus.PENDING),
        ])

        result = list_tasks()

        assert isinstance(result[0], Task)
        assert result[0].title == "Test"


class TestUpdateTask:
    """Tests for update_task() function."""

    def test_update_title(self):
        """Should update task title."""
        initialize_state([
            Task(id=1, title="Old Title", status=TaskStatus.PENDING),
        ])

        result = update_task(1, title="New Title")

        assert result is not None
        assert result.title == "New Title"

    def test_update_description(self):
        """Should update task description."""
        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.PENDING),
        ])

        result = update_task(1, description="New description")

        assert result is not None
        assert result.description == "New description"

    def test_update_priority(self):
        """Should update task priority."""
        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.PENDING),
        ])

        result = update_task(1, priority="high")

        assert result is not None
        assert result.priority == TaskPriority.HIGH

    def test_update_tags(self):
        """Should update task tags."""
        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.PENDING),
        ])

        result = update_task(1, tags=["work", "urgent"])

        assert result is not None
        assert result.tags == ["work", "urgent"]

    def test_update_multiple_fields(self):
        """Should update multiple fields at once."""
        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.PENDING),
        ])

        result = update_task(
            1,
            title="Updated",
            description="New desc",
            priority="high",
            tags=["new", "tags"],
        )

        assert result.title == "Updated"
        assert result.description == "New desc"
        assert result.priority == TaskPriority.HIGH
        assert result.tags == ["new", "tags"]

    def test_update_nonexistent_task(self):
        """Should return None for nonexistent task."""
        initialize_state([])

        result = update_task(999, title="New Title")

        assert result is None

    def test_update_timestamp_changes(self):
        """Should update timestamp on modification."""
        from datetime import datetime

        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.PENDING,
                 created_at=datetime(2025, 1, 1),
                 updated_at=datetime(2025, 1, 1)),
        ])

        result = update_task(1, title="Updated")

        assert result is not None
        assert result.updated_at > datetime(2025, 1, 1)

    def test_partial_update_preserves_other_fields(self):
        """Should preserve other fields when updating one."""
        initialize_state([
            Task(
                id=1,
                title="Task",
                description="Original desc",
                status=TaskStatus.PENDING,
                priority=TaskPriority.LOW,
                tags=["original"],
            ),
        ])

        result = update_task(1, title="New Title")

        assert result.title == "New Title"
        assert result.description == "Original desc"
        assert result.priority == TaskPriority.LOW
        assert result.tags == ["original"]


class TestToggleTaskStatus:
    """Tests for toggle_task_status() function."""

    def test_toggle_pending_to_completed(self):
        """Should toggle pending task to completed."""
        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.PENDING),
        ])

        result = toggle_task_status(1)

        assert result is not None
        assert result.status == TaskStatus.COMPLETED

    def test_toggle_completed_to_pending(self):
        """Should toggle completed task to pending."""
        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.COMPLETED),
        ])

        result = toggle_task_status(1)

        assert result is not None
        assert result.status == TaskStatus.PENDING

    def test_toggle_nonexistent_task(self):
        """Should return None for nonexistent task."""
        initialize_state([])

        result = toggle_task_status(999)

        assert result is None

    def test_toggle_updates_timestamp(self):
        """Should update timestamp when toggling."""
        from datetime import datetime

        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.PENDING,
                 created_at=datetime(2025, 1, 1),
                 updated_at=datetime(2025, 1, 1)),
        ])

        result = toggle_task_status(1)

        assert result is not None
        assert result.updated_at > datetime(2025, 1, 1)

    def test_toggle_idempotent(self):
        """Toggling twice should return to original state."""
        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.PENDING),
        ])

        toggle_task_status(1)
        result = toggle_task_status(1)

        assert result is not None
        assert result.status == TaskStatus.PENDING


class TestCompleteTask:
    """Tests for complete_task() function."""

    def test_complete_pending_task(self):
        """Should mark pending task as completed."""
        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.PENDING),
        ])

        result = complete_task(1)

        assert result is not None
        assert result.status == TaskStatus.COMPLETED

    def test_complete_already_completed(self):
        """Should handle already completed task."""
        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.COMPLETED),
        ])

        result = complete_task(1)

        assert result is not None
        assert result.status == TaskStatus.COMPLETED

    def test_complete_nonexistent_task(self):
        """Should return None for nonexistent task."""
        initialize_state([])

        result = complete_task(999)

        assert result is None

    def test_complete_updates_timestamp(self):
        """Should update timestamp when completing."""
        from datetime import datetime

        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.PENDING,
                 created_at=datetime(2025, 1, 1),
                 updated_at=datetime(2025, 1, 1)),
        ])

        result = complete_task(1)

        assert result is not None
        assert result.updated_at > datetime(2025, 1, 1)


class TestDeleteTask:
    """Tests for delete_task() function."""

    def test_delete_existing_task(self):
        """Should delete existing task."""
        initialize_state([
            Task(id=1, title="Task 1", status=TaskStatus.PENDING),
            Task(id=2, title="Task 2", status=TaskStatus.PENDING),
        ])

        result = delete_task(1)

        assert result is not None
        assert result.title == "Task 1"
        assert len(list_tasks()) == 1

    def test_delete_nonexistent_task(self):
        """Should return None for nonexistent task."""
        initialize_state([
            Task(id=1, title="Task", status=TaskStatus.PENDING),
        ])

        result = delete_task(999)

        assert result is None
        assert len(list_tasks()) == 1

    def test_delete_updates_next_id(self):
        """Deleting should not affect next_id calculation."""
        initialize_state([
            Task(id=1, title="Task 1", status=TaskStatus.PENDING),
            Task(id=2, title="Task 2", status=TaskStatus.PENDING),
        ])

        delete_task(1)

        # Next ID should still be 3 (max was 2, +1 = 3)
        assert get_next_id() == 3
