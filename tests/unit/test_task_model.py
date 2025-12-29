"""Unit tests for Task dataclass model.

Tests cover:
- Serialization (to_dict)
- Deserialization (from_dict)
- Validation (title required, priority enum)
"""
import pytest
from datetime import datetime
from src.models.task import Task, TaskStatus, TaskPriority


class TestTaskStatus:
    """Tests for TaskStatus enum."""

    def test_status_values(self):
        """TaskStatus should have correct string values."""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.COMPLETED.value == "completed"

    def test_status_from_string(self):
        """Should be able to create TaskStatus from string."""
        assert TaskStatus("pending") == TaskStatus.PENDING
        assert TaskStatus("completed") == TaskStatus.COMPLETED


class TestTaskPriority:
    """Tests for TaskPriority enum."""

    def test_priority_values(self):
        """TaskPriority should have correct string values."""
        assert TaskPriority.LOW.value == "low"
        assert TaskPriority.MEDIUM.value == "medium"
        assert TaskPriority.HIGH.value == "high"

    def test_priority_from_string(self):
        """Should be able to create TaskPriority from string."""
        assert TaskPriority("low") == TaskPriority.LOW
        assert TaskPriority("medium") == TaskPriority.MEDIUM
        assert TaskPriority("high") == TaskPriority.HIGH


class TestTaskSerialization:
    """Tests for Task.to_dict() serialization."""

    def test_to_dict_basic(self):
        """Task should serialize to dict with all fields."""
        task = Task(
            id=1,
            title="Test Task",
            status=TaskStatus.PENDING,
        )
        result = task.to_dict()

        assert result["id"] == 1
        assert result["title"] == "Test Task"
        assert result["status"] == "pending"
        assert result["description"] is None
        assert result["priority"] is None
        assert result["tags"] is None

    def test_to_dict_with_all_fields(self):
        """Task with all fields should serialize correctly."""
        now = datetime.utcnow()
        task = Task(
            id=1,
            title="Complete Task",
            description="Full description",
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.HIGH,
            tags=["work", "urgent"],
            created_at=now,
            updated_at=now,
        )
        result = task.to_dict()

        assert result["id"] == 1
        assert result["title"] == "Complete Task"
        assert result["description"] == "Full description"
        assert result["status"] == "completed"
        assert result["priority"] == "high"
        assert result["tags"] == ["work", "urgent"]

    def test_to_dict_iso_format(self):
        """Timestamps should be in ISO format with Z suffix."""
        now = datetime.utcnow()
        task = Task(
            id=1,
            title="Test",
            status=TaskStatus.PENDING,
            created_at=now,
            updated_at=now,
        )
        result = task.to_dict()

        assert result["created_at"].endswith("Z")
        assert result["updated_at"].endswith("Z")

    def test_to_dict_priority_as_string(self):
        """Priority should be serialized as string value, not enum."""
        task = Task(
            id=1,
            title="Test",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
        )
        result = task.to_dict()

        assert result["priority"] == "medium"
        assert isinstance(result["priority"], str)


class TestTaskDeserialization:
    """Tests for Task.from_dict() classmethod."""

    def test_from_dict_basic(self):
        """Should create Task from dict with required fields."""
        data = {
            "id": 1,
            "title": "Test Task",
            "status": "pending",
            "created_at": "2025-12-30T10:00:00Z",
            "updated_at": "2025-12-30T10:00:00Z",
        }
        task = Task.from_dict(data)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.status == TaskStatus.PENDING
        assert task.description is None
        assert task.priority is None
        assert task.tags is None

    def test_from_dict_with_all_fields(self):
        """Should create Task from dict with all fields."""
        data = {
            "id": 1,
            "title": "Complete Task",
            "description": "Full description",
            "status": "completed",
            "priority": "high",
            "tags": ["work", "urgent"],
            "created_at": "2025-12-30T10:00:00Z",
            "updated_at": "2025-12-30T14:30:00Z",
        }
        task = Task.from_dict(data)

        assert task.id == 1
        assert task.title == "Complete Task"
        assert task.description == "Full description"
        assert task.status == TaskStatus.COMPLETED
        assert task.priority == TaskPriority.HIGH
        assert task.tags == ["work", "urgent"]

    def test_from_dict_priority_none(self):
        """Priority should be None when not in dict."""
        data = {
            "id": 1,
            "title": "Test",
            "status": "pending",
            "created_at": "2025-12-30T10:00:00Z",
            "updated_at": "2025-12-30T10:00:00Z",
        }
        task = Task.from_dict(data)

        assert task.priority is None

    def test_roundtrip_preserves_data(self):
        """Serialization + deserialization should preserve all data."""
        original = Task(
            id=42,
            title="Roundtrip Test",
            description="Testing roundtrip",
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.LOW,
            tags=["test"],
        )
        serialized = original.to_dict()
        restored = Task.from_dict(serialized)

        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.description == original.description
        assert restored.status == original.status
        assert restored.priority == original.priority
        assert restored.tags == original.tags


class TestTaskValidation:
    """Tests for Task validation."""

    def test_title_required(self):
        """Task should require a title."""
        with pytest.raises(KeyError):
            Task.from_dict({
                "id": 1,
                "status": "pending",
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z",
            })

    def test_status_required(self):
        """Task should require a status."""
        with pytest.raises(KeyError):
            Task.from_dict({
                "id": 1,
                "title": "Test",
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z",
            })

    def test_invalid_status_raises(self):
        """Invalid status value should raise error."""
        with pytest.raises(ValueError):
            TaskStatus("invalid")

    def test_invalid_priority_raises(self):
        """Invalid priority value should raise error."""
        with pytest.raises(ValueError):
            TaskPriority("invalid")

    def test_created_at_required(self):
        """Task should require created_at timestamp."""
        with pytest.raises(KeyError):
            Task.from_dict({
                "id": 1,
                "title": "Test",
                "status": "pending",
                "updated_at": "2025-12-30T10:00:00Z",
            })

    def test_updated_at_required(self):
        """Task should require updated_at timestamp."""
        with pytest.raises(KeyError):
            Task.from_dict({
                "id": 1,
                "title": "Test",
                "status": "pending",
                "created_at": "2025-12-30T10:00:00Z",
            })


class TestTaskDefaultValues:
    """Tests for Task default values."""

    def test_default_status_is_pending(self):
        """New task should default to pending status."""
        task = Task(id=1, title="Test")

        assert task.status == TaskStatus.PENDING

    def test_default_priority_is_none(self):
        """New task should default to None priority."""
        task = Task(id=1, title="Test")

        assert task.priority is None

    def test_default_tags_is_none(self):
        """New task should default to None tags."""
        task = Task(id=1, title="Test")

        assert task.tags is None

    def test_default_description_is_none(self):
        """New task should default to None description."""
        task = Task(id=1, title="Test")

        assert task.description is None

    def test_default_timestamps(self):
        """New task should have auto-generated timestamps."""
        task = Task(id=1, title="Test")

        assert task.created_at is not None
        assert task.updated_at is not None
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)
