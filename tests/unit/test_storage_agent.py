"""Unit tests for storage_agent module.

Tests cover:
- load_tasks() - Loading tasks from JSON file
- save_tasks() - Saving tasks with atomic write
- ensure_file_exists() - Creating empty tasks file
"""
import pytest
import json
import tempfile
import os
from pathlib import Path
from datetime import datetime
from src.models.task import Task, TaskStatus, TaskPriority
from src.agents.storage_agent import load_tasks, save_tasks, ensure_file_exists


class TestEnsureFileExists:
    """Tests for ensure_file_exists() function."""

    def test_creates_empty_tasks_file(self, tmp_path):
        """Should create tasks.json with empty collection if not exists."""
        tasks_file = tmp_path / "tasks.json"

        ensure_file_exists(tasks_file)

        assert tasks_file.exists()
        content = json.loads(tasks_file.read_text())
        assert content["tasks"] == []
        assert content["version"] == 1

    def test_does_not_overwrite_existing(self, tmp_path):
        """Should not overwrite existing valid tasks file."""
        tasks_file = tmp_path / "tasks.json"
        existing_data = {
            "tasks": [{"id": 1, "title": "Existing", "status": "pending",
                      "created_at": "2025-12-30T10:00:00Z", "updated_at": "2025-12-30T10:00:00Z"}],
            "version": 1,
            "last_modified": "2025-12-30T10:00:00Z"
        }
        tasks_file.write_text(json.dumps(existing_data))

        ensure_file_exists(tasks_file)

        content = json.loads(tasks_file.read_text())
        assert len(content["tasks"]) == 1
        assert content["tasks"][0]["title"] == "Existing"


class TestLoadTasks:
    """Tests for load_tasks() function."""

    def test_returns_empty_list_for_missing_file(self, tmp_path):
        """Should return empty list if file doesn't exist."""
        tasks_file = tmp_path / "nonexistent.json"

        result = load_tasks(tasks_file)

        assert result == []

    def test_returns_empty_list_for_empty_file(self, tmp_path):
        """Should return empty list for empty tasks array."""
        tasks_file = tmp_path / "tasks.json"
        data = {
            "tasks": [],
            "version": 1,
            "last_modified": "2025-12-30T10:00:00Z"
        }
        tasks_file.write_text(json.dumps(data))

        result = load_tasks(tasks_file)

        assert result == []

    def test_loads_single_task(self, tmp_path):
        """Should load and deserialize a single task."""
        tasks_file = tmp_path / "tasks.json"
        data = {
            "tasks": [{
                "id": 1,
                "title": "Test Task",
                "description": "Description",
                "status": "pending",
                "priority": "high",
                "tags": ["test"],
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z"
            }],
            "version": 1,
            "last_modified": "2025-12-30T10:00:00Z"
        }
        tasks_file.write_text(json.dumps(data))

        result = load_tasks(tasks_file)

        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].title == "Test Task"
        assert result[0].description == "Description"
        assert result[0].status == TaskStatus.PENDING
        assert result[0].priority == TaskPriority.HIGH
        assert result[0].tags == ["test"]

    def test_loads_multiple_tasks(self, tmp_path):
        """Should load and deserialize multiple tasks."""
        tasks_file = tmp_path / "tasks.json"
        data = {
            "tasks": [
                {
                    "id": 1,
                    "title": "Task 1",
                    "status": "pending",
                    "created_at": "2025-12-30T10:00:00Z",
                    "updated_at": "2025-12-30T10:00:00Z"
                },
                {
                    "id": 2,
                    "title": "Task 2",
                    "status": "completed",
                    "created_at": "2025-12-30T11:00:00Z",
                    "updated_at": "2025-12-30T12:00:00Z"
                },
            ],
            "version": 1,
            "last_modified": "2025-12-30T12:00:00Z"
        }
        tasks_file.write_text(json.dumps(data))

        result = load_tasks(tasks_file)

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2
        assert result[1].status == TaskStatus.COMPLETED

    def test_loads_tasks_with_null_optional_fields(self, tmp_path):
        """Should handle tasks with null optional fields."""
        tasks_file = tmp_path / "tasks.json"
        data = {
            "tasks": [{
                "id": 1,
                "title": "Minimal Task",
                "status": "pending",
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z"
            }],
            "version": 1,
            "last_modified": "2025-12-30T10:00:00Z"
        }
        tasks_file.write_text(json.dumps(data))

        result = load_tasks(tasks_file)

        assert len(result) == 1
        assert result[0].description is None
        assert result[0].priority is None
        assert result[0].tags is None


class TestSaveTasks:
    """Tests for save_tasks() function."""

    def test_saves_tasks_to_file(self, tmp_path):
        """Should save tasks to JSON file."""
        tasks_file = tmp_path / "tasks.json"
        tasks = [
            Task(
                id=1,
                title="Task 1",
                status=TaskStatus.PENDING,
                created_at=datetime.fromisoformat("2025-12-30T10:00:00"),
                updated_at=datetime.fromisoformat("2025-12-30T10:00:00"),
            ),
            Task(
                id=2,
                title="Task 2",
                status=TaskStatus.COMPLETED,
                created_at=datetime.fromisoformat("2025-12-30T11:00:00"),
                updated_at=datetime.fromisoformat("2025-12-30T12:00:00"),
            ),
        ]

        save_tasks(tasks, tasks_file)

        assert tasks_file.exists()
        content = json.loads(tasks_file.read_text())
        assert len(content["tasks"]) == 2
        assert content["tasks"][0]["id"] == 1
        assert content["tasks"][1]["id"] == 2

    def test_saves_with_version(self, tmp_path):
        """Should save with version field."""
        tasks_file = tmp_path / "tasks.json"
        tasks = [
            Task(
                id=1,
                title="Test",
                status=TaskStatus.PENDING,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
        ]

        save_tasks(tasks, tasks_file)

        content = json.loads(tasks_file.read_text())
        assert content["version"] == 1

    def test_saves_with_timestamp(self, tmp_path):
        """Should save with last_modified timestamp."""
        tasks_file = tmp_path / "tasks.json"
        tasks = [
            Task(
                id=1,
                title="Test",
                status=TaskStatus.PENDING,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
        ]

        save_tasks(tasks, tasks_file)

        content = json.loads(tasks_file.read_text())
        assert "last_modified" in content
        assert content["last_modified"].endswith("Z")

    def test_overwrites_existing_file(self, tmp_path):
        """Should overwrite existing file with new data."""
        tasks_file = tmp_path / "tasks.json"
        # Create existing file
        existing_data = {
            "tasks": [{"id": 99, "title": "Old", "status": "pending",
                      "created_at": "2025-12-30T10:00:00Z", "updated_at": "2025-12-30T10:00:00Z"}],
            "version": 1,
            "last_modified": "2025-12-30T10:00:00Z"
        }
        tasks_file.write_text(json.dumps(existing_data))

        # Save new data
        tasks = [
            Task(
                id=1,
                title="New Task",
                status=TaskStatus.PENDING,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
        ]
        save_tasks(tasks, tasks_file)

        content = json.loads(tasks_file.read_text())
        assert len(content["tasks"]) == 1
        assert content["tasks"][0]["title"] == "New Task"

    def test_creates_directories_if_needed(self, tmp_path):
        """Should create parent directories if they don't exist."""
        nested_dir = tmp_path / "nested" / "path"
        tasks_file = nested_dir / "tasks.json"
        tasks = [
            Task(
                id=1,
                title="Test",
                status=TaskStatus.PENDING,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
        ]

        save_tasks(tasks, tasks_file)

        assert tasks_file.exists()

    def test_json_is_formatted(self, tmp_path):
        """Saved JSON should be human-readable (indented)."""
        tasks_file = tmp_path / "tasks.json"
        tasks = [
            Task(
                id=1,
                title="Test",
                status=TaskStatus.PENDING,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            ),
        ]

        save_tasks(tasks, tasks_file)

        content = tasks_file.read_text()
        # Check that it's formatted (contains newlines and indentation)
        assert "\n" in content
        assert "    " in content  # 4-space indentation
