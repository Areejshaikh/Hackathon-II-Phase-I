---
description: Provides filtering, searching, and sorting capabilities for todo tasks.
responsibilities:
  - Filter tasks by status (pending, complete, etc.)
  - Search tasks by title or description
  - Sort tasks by various criteria (date, priority, etc.)
  - Support compound filters and complex queries
rules:
  - Filters are read-only operations
  - Return subsets without modifying original data
  - Support case-insensitive search
scope:
  - Used by: todo-search-sort-agent, todo-cli-ui-agent
---

## User Input

```text
$ARGUMENTS
```

## Implementation Requirements

Implement a skill that provides filtering, searching, and sorting capabilities.

### Requirements

1. **Filter by Status**:
   - pending, in_progress, complete, blocked
   - Multiple statuses at once (OR logic)
   - Inverse filter (NOT status)

2. **Search**:
   - Search in title and description
   - Case-insensitive matching
   - Partial match support
   - Search by tags/labels

3. **Sort**:
   - By creation date (asc/desc)
   - By due date (asc/desc)
   - By priority (high to low, low to high)
   - By title (alphabetical)
   - By status (custom order)

4. **Compound Queries**:
   - Combine filters with AND/OR logic
   - Date range filters
   - Priority range filters
   - Tag-based filtering

### Output

Return structured results with:
- Filtered/sorted task list
- Original task count vs result count
- Applied filters summary
- Pagination info if applicable
