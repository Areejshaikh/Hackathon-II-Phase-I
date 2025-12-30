---
description: Handles advanced todo features including recurring tasks, due dates, reminders, and scheduling.
responsibilities:
  - Create and manage recurring tasks (daily, weekly, monthly, custom)
  - Set and track due dates on tasks
  - Configure time-based reminders and notifications
  - Handle overdue task detection and escalation
  - Schedule tasks for specific dates and times
  - Support task prioritization (high, medium, low)
  - Manage task categories and tags
rules:
  - Recurring tasks auto-generate next occurrence
  - Reminders trigger based on configured times
  - Overdue tasks highlighted in UI
  - Timezone-aware scheduling
scope:
  - Used by: todo-advanced-agent
---

## User Input

```text
$ARGUMENTS
```

## Implementation Requirements

Implement a skill that handles advanced todo features.

### Requirements

1. **Recurring Tasks**:
   - Daily (every N days)
   - Weekly (specific weekdays)
   - Monthly (specific day of month)
   - Quarterly, yearly
   - Custom interval (every N hours/minutes)
   - End date or occurrence count limit
   - Skip weekends option

2. **Due Dates**:
   - Set due date on task creation
   - Update due date
   - Clear due date
   - Sort by due date
   - Due soon (within 24h) highlighting

3. **Reminders/Notifications**:
   - Set reminder time before due date
   - Multiple reminders per task
   - Configurable notification methods
   - Snooze reminder option
   - Dismiss reminder

4. **Overdue Handling**:
   - Detect overdue tasks automatically
   - Mark as overdue in status
   - Overdue count in dashboard
   - Escalation rules (notify after N days)
   - Bulk overdue report

5. **Prioritization**:
   - High, Medium, Low priority levels
   - Sort by priority
   - Visual indicators in UI
   - Priority-based filtering

6. **Scheduling**:
   - Schedule task for specific date/time
   - Recurring schedule support
   - Timezone configuration
   - Best time suggestions
   - Calendar view integration

### Output

Return structured results with:
- Task with all advanced fields
- Next occurrence date for recurring tasks
- Reminder status and trigger times
- Overdue status if applicable
- Priority level indicator
