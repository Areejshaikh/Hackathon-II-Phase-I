# Phase-I CLI Todo Application

A pure CLI Todo application in Python with multi-agent architecture, JSON persistence, and TDD-driven development.

## Features

- **Multi-Agent Architecture**: 7 specialized agents (5 core + 2 optional)
- **JSON Persistence**: Tasks stored in `tasks.json` with atomic writes
- **Colorful CLI Interface**: Built with `rich` library for beautiful terminal output
- **TDD Workflow**: Red-Green-Refactor cycle ensures code quality
- **Urdu/English Support**: Optional language toggle with RTL formatting
- **Voice Commands**: Experimental one-shot speech-to-text mode

## Installation

### Prerequisites

- Python 3.11+
- UV package manager

### Setup

```bash
# Clone repository
git clone https://github.com/Areejshaikh/Hackathon-II-Phase-I.git
cd Hackathon-II-Phase-I

# Install dependencies with UV
uv sync

# Run the application
uv run todo
```

## Usage

### Basic Commands

```bash
# Add a task
todo add "Buy groceries" --priority high --tags shopping

# List all tasks
todo list

# List tasks with filters
todo list --status pending --priority high

# View task details
todo view 1

# Update a task
todo update 1 --priority medium

# Mark task as complete
todo complete 1

# Mark task as pending
todo uncomplete 1

# Delete a task
todo delete 1

# Search tasks
todo search "groceries"

# Change language
todo lang ur  # Urdu
todo lang en  # English

# Voice command (experimental)
todo voice "add buy milk"

# Exit
todo exit
```

## Project Structure

```
src/
├── main.py              # Entry point
├── models/
│   └── task.py          # Task data model
├── agents/
│   ├── main_agent.py    # Orchestrator
│   ├── state_manager.py # In-memory state
│   ├── storage_agent.py # File I/O
│   ├── cli_ui_agent.py  # Terminal UI
│   ├── search_sort_agent.py # Search/Sort
│   ├── i18n_agent.py    # Internationalization
│   └── voice_agent.py   # Voice commands
└── utils/
    └── helpers.py       # Utilities

tests/
├── unit/               # Unit tests
└── integration/        # Integration tests

tasks.json              # Persistent task storage
```

## Architecture

### Agents

- **Main Agent**: Orchestrates all operations, manages application lifecycle
- **State Manager**: Manages in-memory task collection and state transitions
- **Storage Agent**: Handles JSON persistence with atomic writes
- **CLI UI Agent**: Renders terminal output and handles user input
- **Search Sort Agent**: Implements search, filter, and sort logic
- **I18n Agent**: Provides translations and RTL/LTR support
- **Voice Agent**: Handles speech-to-text with fallback to text

### TDD Workflow

1. **RED**: Write test, verify it FAILS
2. **GREEN**: Write minimal code to pass test
3. **REFACTOR**: Improve code while keeping tests green
4. **COMMIT**: Save progress

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run unit tests only
uv run pytest tests/unit/

# Run integration tests only
uv run pytest tests/integration/

# Run specific test
uv run pytest tests/unit/test_task_model.py -v
```

### Code Quality

```bash
# Format code
uv run ruff format src/ tests/

# Lint code
uv run ruff check src/ tests/
```

## Roadmap

### Phase I (Current) - Foundation
- [x] Multi-agent architecture
- [x] JSON persistence
- [x] Basic CRUD operations
- [x] Search and filter
- [ ] Urdu/English language toggle
- [ ] Voice command mode

### Phase II (Future) - Advanced Features
- Recurring tasks
- Task dependencies
- Advanced reminders

## Documentation

- [Specification](specs/todo-app/spec.md)
- [Implementation Plan](specs/todo-app/plan.md)
- [Tasks](specs/todo-app/tasks.md)
- [ADR - Multi-Agent Architecture](history/adr/001-multi-agent-architecture.md)

## License

MIT

## Contributing

This project follows spec-driven development (SDD) methodology. All changes must:
1. Follow TDD workflow (tests first)
2. Pass all existing tests
3. Maintain 80%+ code coverage
4. Adhere to [constitution](.specify/memory/constitution.md)
