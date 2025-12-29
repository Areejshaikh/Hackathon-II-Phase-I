"""Integration tests for CLI UI and end-to-end flows.

Tests cover:
- display_tasks_table() - Colorful task listing
- display_task_details() - Single task view
- display_welcome() - Welcome message
- Empty state handling
- Main menu flow
"""
import pytest
from io import StringIO
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.models.task import Task, TaskStatus, TaskPriority
from src.agents.state_manager import initialize_state, add_task
from src.agents.cli_ui_agent import (
    display_welcome,
    display_tasks_table,
    display_task_details,
    display_success,
    display_error,
    display_warning,
    display_info,
    display_empty_state,
    display_goodbye,
    display_main_menu,
)


class TestDisplayWelcome:
    """Tests for display_welcome() function."""

    def test_display_welcome_outputs_message(self):
        """Should print welcome message."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_welcome()

            output = mock_stdout.getvalue()
            assert "Todo CLI" in output or "Welcome" in output

    def test_display_welcome_shows_task_count(self):
        """Should show current task count."""
        initialize_state([])

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_welcome()

            output = mock_stdout.getvalue()
            assert "0" in output or "no" in output.lower()

    def test_display_welcome_with_tasks(self):
        """Should show task count with actual tasks."""
        initialize_state([
            Task(id=1, title="Task 1", status=TaskStatus.PENDING),
            Task(id=2, title="Task 2", status=TaskStatus.COMPLETED),
        ])

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_welcome()

            output = mock_stdout.getvalue()
            assert "2" in output


class TestDisplayTasksTable:
    """Tests for display_tasks_table() function."""

    def test_display_empty_table(self):
        """Should handle empty task list."""
        initialize_state([])

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_tasks_table([])

            output = mock_stdout.getvalue()
            assert "no" in output.lower() or "empty" in output.lower() or "0" in output

    def test_display_single_task(self):
        """Should display a single task in table format."""
        task = Task(
            id=1,
            title="Test Task",
            status=TaskStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_tasks_table([task])

            output = mock_stdout.getvalue()
            assert "1" in output
            assert "Test Task" in output
            assert "pending" in output.lower()

    def test_display_multiple_tasks(self):
        """Should display multiple tasks."""
        tasks = [
            Task(
                id=1,
                title="Task 1",
                status=TaskStatus.PENDING,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
            Task(
                id=2,
                title="Task 2",
                status=TaskStatus.COMPLETED,
                priority=TaskPriority.HIGH,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
        ]

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_tasks_table(tasks)

            output = mock_stdout.getvalue()
            assert "1" in output
            assert "2" in output
            assert "Task 1" in output
            assert "Task 2" in output
            assert "pending" in output.lower()
            assert "completed" in output.lower()
            assert "high" in output.lower()

    def test_display_task_with_tags(self):
        """Should display tasks with tags."""
        task = Task(
            id=1,
            title="Tagged Task",
            status=TaskStatus.PENDING,
            tags=["work", "urgent"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_tasks_table([task])

            output = mock_stdout.getvalue()
            assert "Tagged Task" in output
            assert "work" in output.lower() or "urgent" in output.lower()

    def test_table_has_columns(self):
        """Table should have ID, Title, Status columns."""
        task = Task(
            id=42,
            title="Column Test",
            status=TaskStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_tasks_table([task])

            output = mock_stdout.getvalue()
            assert "42" in output  # ID
            assert "Column Test" in output  # Title


class TestDisplayTaskDetails:
    """Tests for display_task_details() function."""

    def test_display_task_all_fields(self):
        """Should display all task fields."""
        task = Task(
            id=1,
            title="Full Task",
            description="This is a description",
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.HIGH,
            tags=["work"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_task_details(task)

            output = mock_stdout.getvalue()
            assert "1" in output
            assert "Full Task" in output
            assert "This is a description" in output
            assert "completed" in output.lower()
            assert "high" in output.lower()
            assert "work" in output.lower()

    def test_display_minimal_task(self):
        """Should display task with minimal fields."""
        task = Task(
            id=1,
            title="Minimal Task",
            status=TaskStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_task_details(task)

            output = mock_stdout.getvalue()
            assert "1" in output
            assert "Minimal Task" in output


class TestDisplayMessages:
    """Tests for display_* message functions."""

    def test_display_success_green(self):
        """display_success should output success message."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_success("Operation completed")

            output = mock_stdout.getvalue()
            assert "Operation completed" in output

    def test_display_error_red(self):
        """display_error should output error message."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_error("Something went wrong")

            output = mock_stdout.getvalue()
            assert "Something went wrong" in output

    def test_display_warning_yellow(self):
        """display_warning should output warning message."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_warning("Be careful")

            output = mock_stdout.getvalue()
            assert "Be careful" in output

    def test_display_info_blue(self):
        """display_info should output info message."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_info("For your information")

            output = mock_stdout.getvalue()
            assert "For your information" in output

    def test_display_empty_state(self):
        """display_empty_state should handle no results."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_empty_state("No tasks found")

            output = mock_stdout.getvalue()
            assert "No tasks found" in output


class TestDisplayGoodbye:
    """Tests for display_goodbye() function."""

    def test_display_goodbye(self):
        """Should display goodbye message."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            display_goodbye()

            output = mock_stdout.getvalue()
            assert "bye" in output.lower() or "goodbye" in output.lower() or "quit" in output.lower()


class TestDisplayMainMenu:
    """Tests for display_main_menu() function."""

    def test_main_menu_has_options(self):
        """Menu should have numbered options."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            with patch("builtins.input", return_value="8"):
                result = display_main_menu()

            output = mock_stdout.getvalue()
            # Should have menu text and options
            assert "1" in output or "Add" in output or "Menu" in output

    def test_main_menu_returns_choice(self):
        """Should return user choice."""
        with patch("builtins.input", return_value="3"):
            result = display_main_menu()

            assert result == 3
