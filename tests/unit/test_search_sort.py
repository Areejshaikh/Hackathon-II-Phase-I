"""Unit tests for search_sort_agent module.

Tests cover:
- search_tasks() - Keyword search in title/description
- filter_tasks() - Filter by status, priority, tags
- sort_tasks() - Sort by ID, priority, created, title
- process_tasks() - Combined search/filter/sort
"""
import pytest
from datetime import datetime
from src.models.task import Task, TaskStatus, TaskPriority
from src.agents.search_sort_agent import (
    search_tasks,
    filter_tasks,
    search_and_filter,
    sort_tasks,
    process_tasks,
)


def make_task(task_id, title, status="pending", priority=None, tags=None,
              description=None, created_at=None, updated_at=None):
    """Helper to create test tasks."""
    return Task(
        id=task_id,
        title=title,
        status=TaskStatus(status),
        priority=TaskPriority(priority) if priority else None,
        tags=tags,
        description=description,
        created_at=created_at or datetime.utcnow(),
        updated_at=updated_at or datetime.utcnow(),
    )


class TestSearchTasks:
    """Tests for search_tasks() function."""

    def test_search_finds_title_match(self):
        """Should find tasks matching keyword in title."""
        tasks = [
            make_task(1, "Buy groceries"),
            make_task(2, "Finish report"),
            make_task(3, "Buy supplies"),
        ]

        result = search_tasks(tasks, "buy")

        assert len(result) == 2
        ids = {t.id for t in result}
        assert ids == {1, 3}

    def test_search_finds_description_match(self):
        """Should find tasks matching keyword in description."""
        tasks = [
            make_task(1, "Task 1", description="Buy milk and eggs"),
            make_task(2, "Task 2", description="Finish the report"),
            make_task(3, "Task 3", description="Go shopping"),
        ]

        result = search_tasks(tasks, "report")

        assert len(result) == 1
        assert result[0].id == 2

    def test_search_case_insensitive(self):
        """Search should be case-insensitive."""
        tasks = [
            make_task(1, "BUY GROCERIES"),
            make_task(2, "buy groceries"),
            make_task(3, "Buy Groceries"),
        ]

        result = search_tasks(tasks, "buy groceries")

        assert len(result) == 3

    def test_search_empty_query(self):
        """Empty query should return all tasks."""
        tasks = [
            make_task(1, "Task 1"),
            make_task(2, "Task 2"),
        ]

        result = search_tasks(tasks, "")

        assert len(result) == 2

    def test_search_no_matches(self):
        """Should return empty list when no matches."""
        tasks = [
            make_task(1, "Task 1"),
            make_task(2, "Task 2"),
        ]

        result = search_tasks(tasks, "xyz")

        assert result == []


class TestFilterTasks:
    """Tests for filter_tasks() function."""

    def test_filter_by_status_pending(self):
        """Should filter by pending status."""
        tasks = [
            make_task(1, "Task 1", status="pending"),
            make_task(2, "Task 2", status="completed"),
            make_task(3, "Task 3", status="pending"),
        ]

        result = filter_tasks(tasks, status="pending")

        assert len(result) == 2
        ids = {t.id for t in result}
        assert ids == {1, 3}

    def test_filter_by_status_completed(self):
        """Should filter by completed status."""
        tasks = [
            make_task(1, "Task 1", status="pending"),
            make_task(2, "Task 2", status="completed"),
            make_task(3, "Task 3", status="pending"),
        ]

        result = filter_tasks(tasks, status="completed")

        assert len(result) == 1
        assert result[0].id == 2

    def test_filter_by_priority_high(self):
        """Should filter by high priority."""
        tasks = [
            make_task(1, "Task 1", priority="high"),
            make_task(2, "Task 2", priority="medium"),
            make_task(3, "Task 3", priority="high"),
        ]

        result = filter_tasks(tasks, priority="high")

        assert len(result) == 2
        ids = {t.id for t in result}
        assert ids == {1, 3}

    def test_filter_by_priority_low(self):
        """Should filter by low priority."""
        tasks = [
            make_task(1, "Task 1", priority="high"),
            make_task(2, "Task 2", priority="low"),
            make_task(3, "Task 3", priority="medium"),
        ]

        result = filter_tasks(tasks, priority="low")

        assert len(result) == 1
        assert result[0].id == 2

    def test_filter_by_tags_single(self):
        """Should filter by single tag."""
        tasks = [
            make_task(1, "Task 1", tags=["work"]),
            make_task(2, "Task 2", tags=["personal"]),
            make_task(3, "Task 3", tags=["work", "urgent"]),
        ]

        result = filter_tasks(tasks, tags=["work"])

        assert len(result) == 2
        ids = {t.id for t in result}
        assert ids == {1, 3}

    def test_filter_by_tags_multiple(self):
        """Should filter by multiple tags (AND logic)."""
        tasks = [
            make_task(1, "Task 1", tags=["work"]),
            make_task(2, "Task 2", tags=["work", "urgent"]),
            make_task(3, "Task 3", tags=["personal"]),
            make_task(4, "Task 4", tags=["urgent"]),
        ]

        result = filter_tasks(tasks, tags=["work", "urgent"])

        assert len(result) == 1
        assert result[0].id == 2

    def test_filter_combined_status_and_priority(self):
        """Should filter by multiple criteria."""
        tasks = [
            make_task(1, "Task 1", status="pending", priority="high"),
            make_task(2, "Task 2", status="completed", priority="high"),
            make_task(3, "Task 3", status="pending", priority="low"),
        ]

        result = filter_tasks(tasks, status="pending", priority="high")

        assert len(result) == 1
        assert result[0].id == 1

    def test_filter_no_matches(self):
        """Should return empty list when no matches."""
        tasks = [
            make_task(1, "Task 1", status="pending"),
            make_task(2, "Task 2", status="pending"),
        ]

        result = filter_tasks(tasks, status="completed")

        assert result == []

    def test_filter_returns_all_when_no_criteria(self):
        """Should return all tasks when no filter criteria."""
        tasks = [
            make_task(1, "Task 1"),
            make_task(2, "Task 2"),
        ]

        result = filter_tasks(tasks)

        assert len(result) == 2


class TestSearchAndFilter:
    """Tests for search_and_filter() function."""

    def test_search_and_filter_combined(self):
        """Should combine search and filter."""
        tasks = [
            make_task(1, "Buy groceries", status="pending", tags=["shopping"]),
            make_task(2, "Buy medicine", status="completed", tags=["health"]),
            make_task(3, "Grocery shopping", status="pending", tags=["shopping"]),
        ]

        result = search_and_filter(tasks, query="buy", status="pending")

        assert len(result) == 1
        assert result[0].id == 1


class TestSortTasks:
    """Tests for sort_tasks() function."""

    def test_sort_by_id_default(self):
        """Should sort by ID (default)."""
        tasks = [
            make_task(3, "Task 3"),
            make_task(1, "Task 1"),
            make_task(2, "Task 2"),
        ]

        result = sort_tasks(tasks, by="id")

        assert result[0].id == 1
        assert result[1].id == 2
        assert result[2].id == 3

    def test_sort_by_id_reverse(self):
        """Should sort by ID in reverse."""
        tasks = [
            make_task(1, "Task 1"),
            make_task(2, "Task 2"),
            make_task(3, "Task 3"),
        ]

        result = sort_tasks(tasks, by="id", reverse=True)

        assert result[0].id == 3
        assert result[1].id == 2
        assert result[2].id == 1

    def test_sort_by_priority(self):
        """Should sort by priority (low > medium > high ascending)."""
        tasks = [
            make_task(1, "Task 1", priority="low"),
            make_task(2, "Task 2", priority="high"),
            make_task(3, "Task 3", priority="medium"),
        ]

        result = sort_tasks(tasks, by="priority")

        # Ascending: low (1) > medium (2) > high (3)
        assert result[0].priority == TaskPriority.LOW
        assert result[1].priority == TaskPriority.MEDIUM
        assert result[2].priority == TaskPriority.HIGH

    def test_sort_by_priority_reverse(self):
        """Should sort by priority reverse (high > medium > low descending)."""
        tasks = [
            make_task(1, "Task 1", priority="low"),
            make_task(2, "Task 2", priority="high"),
            make_task(3, "Task 3", priority="medium"),
        ]

        result = sort_tasks(tasks, by="priority", reverse=True)

        # Descending: high (1) > medium (2) > low (3)
        assert result[0].priority == TaskPriority.HIGH
        assert result[1].priority == TaskPriority.MEDIUM
        assert result[2].priority == TaskPriority.LOW

    def test_sort_by_title(self):
        """Should sort alphabetically by title."""
        tasks = [
            make_task(1, "Charlie"),
            make_task(2, "Alpha"),
            make_task(3, "Bravo"),
        ]

        result = sort_tasks(tasks, by="title")

        assert result[0].title == "Alpha"
        assert result[1].title == "Bravo"
        assert result[2].title == "Charlie"

    def test_sort_by_created(self):
        """Should sort by creation date."""
        t1 = make_task(1, "Task 1", created_at=datetime(2025, 1, 3))
        t2 = make_task(2, "Task 2", created_at=datetime(2025, 1, 1))
        t3 = make_task(3, "Task 3", created_at=datetime(2025, 1, 2))
        tasks = [t1, t2, t3]

        result = sort_tasks(tasks, by="created")

        assert result[0].id == 2  # Jan 1
        assert result[1].id == 3  # Jan 2
        assert result[2].id == 1  # Jan 3

    def test_sort_empty_list(self):
        """Should handle empty list."""
        result = sort_tasks([], by="id")

        assert result == []

    def test_sort_preserves_ids(self):
        """Sort should not change task data, just order."""
        tasks = [
            make_task(1, "Task 1"),
            make_task(2, "Task 2"),
        ]

        result = sort_tasks(tasks, by="id")

        assert result[0].id == 1
        assert result[1].id == 2


class TestProcessTasks:
    """Tests for process_tasks() function."""

    def test_process_search_filter_sort(self):
        """Should combine search, filter, and sort."""
        tasks = [
            make_task(1, "Buy groceries", status="pending", priority="high", tags=["shopping"]),
            make_task(2, "Buy medicine", status="completed", priority="high", tags=["health"]),
            make_task(3, "Grocery shopping", status="pending", priority="low", tags=["shopping"]),
            make_task(4, "Buy report", status="pending", priority="high", tags=["work"]),
        ]

        result = process_tasks(
            tasks,
            query="buy",
            status="pending",
            sort_by="priority",
            reverse=True,
        )

        # Should have 2 results: Task 1 and Task 4 (both "buy" + "pending")
        assert len(result) == 2
        # Both should be high priority, sorted reverse (Task 4 first due to higher ID)
        assert result[0].priority == TaskPriority.HIGH
        assert result[1].priority == TaskPriority.HIGH

    def test_process_empty_result(self):
        """Should handle no matching results."""
        tasks = [
            make_task(1, "Task 1", status="pending"),
            make_task(2, "Task 2", status="pending"),
        ]

        result = process_tasks(
            tasks,
            query="xyz",
            status="pending",
        )

        assert result == []

    def test_process_no_filters(self):
        """Should sort all tasks when no filters."""
        tasks = [
            make_task(3, "Task 3"),
            make_task(1, "Task 1"),
            make_task(2, "Task 2"),
        ]

        result = process_tasks(tasks, sort_by="id")

        assert len(result) == 3
        assert result[0].id == 1
        assert result[1].id == 2
        assert result[2].id == 3
