---
description: Manages task state transitions and lifecycle for todo items.
responsibilities:
  - Handle task state transitions (pending -> complete, etc.)
  - Validate state transitions are allowed
  - Track state history for undo/redo support
  - Manage task dependencies and blocking states
rules:
  - Only valid transitions allowed
  - State changes are immediate and atomic
  - History preserved for audit trail
scope:
  - Used by: todo-state-manager, todo-cli-ui-agent
---

## User Input

```text
$ARGUMENTS
```

## Implementation Requirements

Implement a skill that manages task state transitions and lifecycle.

### Requirements

1. **State Transitions**:
   - pending -> in_progress
   - in_progress -> pending (cancel)
   - in_progress -> complete
   - pending -> complete (direct)
   - Any state -> blocked
   - blocked -> pending

2. **Validation**:
   - Check if transition is valid before executing
   - Validate required fields are present
   - Check task exists before transition

3. **State History**:
   - Track previous states with timestamps
   - Support undo/redo operations
   - Store who made the change

4. **Dependencies**:
   - Mark tasks as blocked when dependencies unmet
   - Auto-complete when dependencies satisfied
   - Detect circular dependencies

### Output

Return structured results with:
- New state after transition
- Previous state for undo
- Transition success/failure with reason
- Dependency status if applicable
