---
description: Renders terminal-based UI for todo application with menus and visual feedback.
responsibilities:
  - Display interactive menus with keyboard navigation
  - Render task lists in formatted tables
  - Show colored output for status indicators
  - Display progress spinners and loading states
  - Handle pagination for long task lists
rules:
  - Support ANSI color codes for terminals
  - Handle terminal resizing gracefully
  - Provide clear visual feedback for all actions
  - Accessible output (support no-color mode)
scope:
  - Used by: todo-cli-ui-agent
---

## User Input

```text
$ARGUMENTS
```

## Implementation Requirements

Implement a skill that renders terminal-based UI for the todo application.

### Requirements

1. **Main Menu**:
   - Add task, List tasks, Update task, Delete task
   - Filter/sort options, Settings, Exit
   - Arrow key navigation with highlight
   - Enter to select, Escape to go back

2. **Task List Display**:
   - Formatted table with columns (ID, Status, Title, Due Date)
   - Truncate long titles with ellipsis
   - Pagination for large lists (page 1/5, etc.)
   - Empty state message when no tasks

3. **Status Indicators**:
   - [ ] Pending - White/Gray
   - [x] Complete - Green
   - [!] Blocked - Red/Yellow
   - [>] In Progress - Blue
   - Use icons or colored text

4. **Input Prompts**:
   - Clear prompt messages
   - Validation feedback
   - Confirmation dialogs (Y/n)
   - Cancel/ESC to abort

5. **Loading States**:
   - Spinner animation during operations
   - Progress bar for bulk operations
   - Success/error toast messages
   - Clear operation status messages

6. **Color Scheme**:
   - High priority: Red
   - Medium priority: Yellow
   - Low priority: Green
   - Complete: Dimmed/Grayed out
   - Support --no-color flag

### Output

Return structured results with:
- User selection/action
- Formatted display data
- Input values collected
- UI state for continued interaction
