---
description: Provides core CRUD operations for todo tasks.
responsibilities:
  - Add new task with title and description
  - Update task fields
  - Delete task by ID
  - Toggle task status (complete / pending)
rules:
  - Task IDs must be unique
  - All changes must reflect in memory immediately
  - Validation required for user input
scope:
  - Used by: todo-state-manager
---

## User Input

```text
$ARGUMENTS
```

## Implementation Requirements

Implement a skill that provides core CRUD operations for todo tasks.

### Requirements

1. **Add Task**:
   - Accept title and description
   - Generate unique ID (e.g., UUID or timestamp-based)
   - Validate title is not empty
   - Store in memory with status "pending"

2. **Update Task**:
   - Find task by ID
   - Allow updating title, description, or status
   - Validate task exists before update

3. **Delete Task**:
   - Remove task by ID
   - Handle case where task doesn't exist

4. **Toggle Status**:
   - Switch between "pending" and "complete"
   - Validate task exists

### Output

Return structured results with:
- Success/failure status
- Task data for read operations
- Error messages for failures
