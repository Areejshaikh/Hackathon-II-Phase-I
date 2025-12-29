"""Task data model for the CLI Todo application.

Defines:
- TaskStatus: Enum for task status (pending/completed)
- TaskPriority: Enum for task priority (low/medium/high)
- Task: Dataclass representing a single todo item
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration."""

    PENDING = "pending"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    """Task priority enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier (auto-generated, never reused)
        title: Task title (required, 1-200 characters)
        description: Optional task description (max 2000 characters)
        status: Task status (pending or completed, default: pending)
        priority: Optional task priority (low, medium, high)
        tags: Optional list of tags
        created_at: Creation timestamp (auto-generated)
        updated_at: Last update timestamp (auto-generated)
    """

    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    tags: Optional[list[str]] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert Task to JSON-serializable dictionary.

        Returns:
            Dictionary representation suitable for JSON serialization.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value if self.priority else None,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() + "Z",
            "updated_at": self.updated_at.isoformat() + "Z",
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create Task from dictionary.

        Args:
            data: Dictionary with task data.

        Returns:
            New Task instance.
        """
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            status=TaskStatus(data["status"]),
            priority=TaskPriority(data["priority"]) if data.get("priority") else None,
            tags=data.get("tags"),
            created_at=datetime.fromisoformat(data["created_at"].rstrip("Z")),
            updated_at=datetime.fromisoformat(data["updated_at"].rstrip("Z")),
        )

    @staticmethod
    def _now_utc() -> datetime:
        """Get current UTC time."""
        return datetime.utcnow()
