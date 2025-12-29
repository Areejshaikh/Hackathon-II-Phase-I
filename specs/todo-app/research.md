# Research: Phase-I CLI Todo Application

## Overview

This document consolidates research findings for the Phase-I CLI Todo Application implementation.

## Technology Decisions

### 1. Rich Library for CLI UI

**Decision**: Use `rich` library for colorful terminal output

- **Decision**: `rich`
- **Rationale**:
  - Cross-platform support (Windows, macOS, Linux)
  - Rich feature set: tables, panels, progress bars, syntax highlighting
  - Active maintenance and good documentation
  - Pure Python, no system dependencies
- **Alternatives considered**:
  - `colorama`: Limited features, mainly just colors
  - `blessed`: Older, less actively maintained
  - `inquirer`: More for interactive prompts, less for display

**Installation**: `pip install rich`

### 2. JSON Persistence Strategy

**Decision**: Single `tasks.json` file with auto-save on mutations

- **Decision**: JSON file persistence
- **Rationale**:
  - Human-readable format for easy debugging
  - Simple backup/restore (just copy the file)
  - No external dependencies (stdlib `json`)
  - Works well for <10k tasks (specified performance goal)
- **Alternatives considered**:
  - SQLite: Overkill for single-user CLI, adds dependency
  - YAML: Less common, requires additional library
  - pickle: Not human-readable, security concerns

**File location**: Repository root as `tasks.json`

### 3. In-Memory State Management

**Decision**: Load all tasks into memory on startup, persist on every mutation

- **Decision**: Full in-memory with auto-save
- **Rationale**:
  - Instant operations (<100ms target)
  - Simple CRUD implementation
  - Easy state queries for filtering/sorting
  - Atomic writes with exception handling
- **Alternatives considered**:
  - Lazy loading: Slower per-operation, complex caching
  - Direct file I/O: No atomicity, race conditions possible
  - Database: Over-engineering for this scope

### 4. ID Generation Strategy

**Decision**: Auto-increment based on max existing ID

- **Decision**: `max(id) + 1`
- **Rationale**:
  - Simple and deterministic
  - Never reuses IDs (avoids confusion)
  - Works well for single-user scenario
- **Alternatives considered**:
  - UUID: Overkill, makes URLs/task references longer
  - Auto-increment with counter file: Extra complexity
  - Timestamp-based: Potential collisions, not sequential

### 5. Agent Communication Pattern

**Decision**: Direct function calls between agents (not message passing)

- **Decision**: Function-based communication
- **Rationale**:
  - Simpler for Python CLI application
  - Clear interface boundaries defined in spec
  - No serialization/deserialization overhead
  - Python's native function call pattern
- **Alternatives considered**:
  - Message queue (e.g., Redis): Overkill for single process
  - Async message passing: Complex, not needed for CLI

## Best Practices

### CLI Application Design

1. **Startup**: Load state, show welcome, enter main loop
2. **Input**: Clear prompts, validation feedback, default values
3. **Output**: Color-coded by message type (success=green, error=red)
4. **Error Handling**: Graceful degradation, helpful messages
5. **Exit**: Auto-save, clean shutdown message

### TDD in Python CLI

1. Write failing test for a feature
2. Implement minimal code to pass test
3. Refactor while keeping tests green
4. Repeat for each feature

### JSON File Operations

```python
# Load with error handling
def load_tasks(path):
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)

# Save with atomic write
def save_tasks(tasks, path):
    temp = path.with_suffix('.tmp')
    with open(temp, 'w') as f:
        json.dump(tasks, f, indent=2)
    temp.replace(path)
```

## References

- Rich library documentation: https://rich.readthedocs.io/
- Python JSON module: https://docs.python.org/3/library/json.html
- TDD methodology: Test-Driven Development by Kent Beck
