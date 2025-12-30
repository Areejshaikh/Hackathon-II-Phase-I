---
description: Handles persistence and file I/O operations for todo tasks.
responsibilities:
  - Save tasks to persistent storage (JSON file)
  - Load tasks from storage on startup
  - Handle file I/O errors gracefully
  - Ensure data consistency between memory and disk
rules:
  - Use atomic writes to prevent data corruption
  - Handle missing/corrupt files gracefully
  - Support backup/restore operations
scope:
  - Used by: todo-storage-agent
---

## User Input

```text
$ARGUMENTS
```

## Implementation Requirements

Implement a skill that handles persistence and file I/O for todo tasks.

### Requirements

1. **Save Tasks**:
   - Write tasks array to JSON file
   - Use atomic write (write to temp file, then rename)
   - Handle permission and disk space errors

2. **Load Tasks**:
   - Read tasks from JSON file on startup
   - Handle missing file (return empty array)
   - Handle corrupt/invalid JSON gracefully
   - Validate loaded data structure

3. **Backup/Restore**:
   - Create timestamped backups before writes
   - Restore from backup if write fails
   - List available backups

4. **Data Validation**:
   - Validate task structure before save
   - Handle schema mismatches
   - Log errors with context

### Output

Return structured results with:
- Operation success/failure status
- Loaded task data or error details
- Backup information when applicable
