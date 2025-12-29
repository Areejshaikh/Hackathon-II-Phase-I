# Data Model: Phase-I CLI Todo Application

## Entities

### Task

The core entity representing a single todo item.

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| `id` | int | Yes | Auto-generated | Unique, never reused |
| `title` | str | Yes | - | 1-200 characters |
| `description` | str | null | null | Max 2000 characters |
| `status` | str | Yes | `"pending"` | `"pending"` or `"completed"` |
| `priority` | str | null | null | `"low"`, `"medium"`, or `"high"` |
| `tags` | list[str] | null | null | List of non-empty strings |
| `created_at` | str | Yes | Auto-generated | ISO 8601 format |
| `updated_at` | str | Yes | Auto-generated | ISO 8601 format |

### TaskCollection

Wrapper entity for persistence.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tasks` | list[Task] | Yes | List of all tasks |
| `version` | int | Yes | Schema version (for future migrations) |
| `last_modified` | str | Yes | ISO 8601 timestamp |

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TaskCollection",
  "type": "object",
  "required": ["tasks", "version", "last_modified"],
  "properties": {
    "tasks": {
      "type": "array",
      "items": { "$ref": "#/definitions/Task" }
    },
    "version": { "type": "integer", "const": 1 },
    "last_modified": { "type": "string", "format": "date-time" }
  },
  "definitions": {
    "Task": {
      "type": "object",
      "required": ["id", "title", "status", "created_at", "updated_at"],
      "properties": {
        "id": { "type": "integer", "minimum": 1 },
        "title": { "type": "string", "minLength": 1, "maxLength": 200 },
        "description": { "type": ["string", "null"], "maxLength": 2000 },
        "status": { "type": "string", "enum": ["pending", "completed"] },
        "priority": { "type": ["string", "null"], "enum": ["low", "medium", "high"] },
        "tags": {
          "type": ["array", "null"],
          "items": { "type": "string", "minLength": 1 },
          "uniqueItems": true
        },
        "created_at": { "type": "string", "format": "date-time" },
        "updated_at": { "type": "string", "format": "date-time" }
      }
    }
  }
}
```

## Example Data

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread, butter",
      "status": "pending",
      "priority": "high",
      "tags": ["shopping", "home"],
      "created_at": "2025-12-30T10:00:00Z",
      "updated_at": "2025-12-30T10:00:00Z"
    },
    {
      "id": 2,
      "title": "Finish report",
      "description": null,
      "status": "completed",
      "priority": "medium",
      "tags": ["work"],
      "created_at": "2025-12-29T08:00:00Z",
      "updated_at": "2025-12-30T14:30:00Z"
    }
  ],
  "version": 1,
  "last_modified": "2025-12-30T14:30:00Z"
}
```

## State Transitions

### Task Status

```
pending <---> completed
```

A task can only be in one state at a time. The status is toggled via the "Complete Task" feature.

### Task Lifecycle

```
[Created] --> [Updated] --> [Completed/Deleted]
```

## Validation Rules

1. **Title**: Required, 1-200 characters
2. **Description**: Optional, max 2000 characters if provided
3. **Priority**: Optional, one of: low, medium, high
4. **Tags**: Optional, list of unique non-empty strings
5. **ID**: Unique within collection, never reused after deletion
6. **Timestamps**: Auto-generated on create/update, ISO 8601 format

## Python Model Class

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class Task:
    id: int
    title: str
    status: TaskStatus = TaskStatus.PENDING
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    tags: Optional[list[str]] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
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
        """Create Task from dict."""
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
```

## Persistence Format

The `tasks.json` file contains:

```json
{
  "tasks": [...],
  "version": 1,
  "last_modified": "2025-12-30T14:30:00Z"
}
```

**Note**: The outer wrapper (`tasks`, `version`, `last_modified`) allows for future schema evolution without breaking existing data.
