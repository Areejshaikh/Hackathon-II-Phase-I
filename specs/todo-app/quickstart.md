# Quickstart: Phase-I CLI Todo Application

## Prerequisites

- Python 3.11 or higher
- `uv` package manager (recommended) or `pip`

## Installation

### Using uv (Recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize Python project
uv init

# Add rich dependency
uv add rich

# Install development dependencies
uv add --dev pytest pytest-cov
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install rich pytest pytest-cov
```

## Project Structure

```
src/
├── main.py              # Entry point
├── models/
│   └── task.py          # Task data model
├── agents/
│   ├── __init__.py
│   ├── main_agent.py    # Orchestrates flow
│   ├── state_manager.py # State management
│   ├── storage_agent.py # JSON persistence
│   ├── cli_ui_agent.py  # CLI rendering
│   └── search_sort_agent.py # Search/filter/sort
└── utils/
    └── helpers.py

tests/
├── unit/
└── integration/

tasks.json               # Created on first run
pyproject.toml
```

## Development Setup

### 1. Verify Python Version

```bash
python --version
# Expected: Python 3.11+
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_task_model.py
```

### 4. Run the Application

```bash
# Using uv
uv run src/main.py

# Using Python directly
python src/main.py
```

## Color Scheme

The application uses `rich` with the following color scheme:

| Element | Color | Usage |
|---------|-------|-------|
| Headers/Titles | Cyan | Section headers, task titles |
| Menus/Warnings | Yellow | Menu options, warning messages |
| Success | Green | Confirmation messages, completed tasks |
| Errors | Red | Error messages, deletion confirmations |
| Info | Blue | Informational messages, help text |

## CLI Flow

1. **Startup**: Load `tasks.json` (create if missing)
2. **Main Menu**: Numbered options with color coding
3. **Operation**: User selects option, enters data
4. **Feedback**: Color-coded response
5. **Loop**: Return to main menu or quit

### Main Menu Options

```
1. Add Task
2. List Tasks
3. View Task
4. Update Task
5. Complete Task
6. Delete Task
7. Search/Filter
8. Quit
```

## Testing Strategy

### Test Pyramid

```
        /\
       /  \
      /    \     Integration Tests (few)
     /------\
    /        \   Unit Tests (many)
   /__________\
```

### Unit Tests

- `test_task_model.py`: Task data model validation
- `test_state_manager.py`: State mutations, ID generation
- `test_storage_agent.py`: JSON load/save operations
- `test_search_sort.py`: Search, filter, sort logic

### Integration Tests

- `test_cli_flow.py`: Full user journey tests

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest tests/unit/test_task_model.py::TestTaskModel::test_task_creation

# Watch mode (requires pytest-watch)
ptw
```

## First Run

```bash
$ uv run src/main.py

╭────────────────────────────────────────╮
│         Todo CLI - Welcome!            │
╰────────────────────────────────────────╯

Tasks loaded: 0

╭────────────────────────────────────────╮
│  Main Menu                             │
╰────────────────────────────────────────╮
1. Add Task
2. List Tasks
3. View Task
4. Update Task
5. Complete Task
6. Delete Task
7. Search/Filter
8. Quit

Enter your choice [1-8]: _
```

## Common Issues

### Issue: `tasks.json` not found

**Solution**: The application creates `tasks.json` automatically on first run.

### Issue: Colors not displaying

**Solution**:
- Ensure terminal supports ANSI colors
- On Windows, `rich` handles this automatically
- Try: `rich.reconfigure(force_terminal=True)`

### Issue: Tests failing

**Solution**:
- Ensure all dependencies are installed: `uv sync`
- Check Python version: `python --version`
- Run tests with verbose output: `pytest -v`

## Next Steps

1. Run the application: `uv run src/main.py`
2. Try adding a task: Select option 1
3. List tasks: Select option 2
4. Complete a task: Select option 5
5. Run tests: `pytest`
