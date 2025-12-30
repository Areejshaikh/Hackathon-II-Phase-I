# Implementation Plan: todo-app

**Branch**: `master` | **Date**: 2025-12-30 | **Spec**: [specs/todo-app/spec.md](../specs/todo-app/spec.md)
**Input**: Feature specification from `/specs/todo-app/spec.md` + User's 10-step execution roadmap

## Summary

Phase-I delivers a pure CLI Todo application in Python with:
- JSON persistence (`tasks.json`) as single source of truth
- Colorful terminal UI using `rich` library
- Strict multi-agent architecture with 7 agents (5 core + 2 optional)
- TDD workflow (Red-Green-Refactor cycle)
- Urdu/English language toggle support
- Experimental one-shot voice command mode

The implementation follows spec-driven development (SDD) methodology with clear agent boundaries, in-memory state management, and zero-boilerplate mindset.

**Target Repository**: https://github.com/Areejshaikh/Hackathon-II-Phase-I

---

## Technical Context

**Language/Version**: Python 3.13+ (use `python --version` to verify)
**Package Manager**: UV (MUST use UV, no pip, no poetry)
**Primary Dependencies**:
- `rich` - Colorful terminal output and tables
- `json` - Persistence (stdlib)
- `uuid` - ID generation (stdlib)
**Storage**: `tasks.json` file in repository root (JSON format)
**Testing**: pytest (pytest for unit/integration tests)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single CLI application
**Performance Goals**: <10k tasks, instant operations (<100ms)
**Constraints**: CLI only, no web/API, no database, UV required
**Scale/Scope**: Single user, local persistence

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| Multi-Agent Architecture | Modular agents with single responsibilities | OK | 7 agents defined (5 core + 2 optional) |
| In-Memory First + JSON Persistence | In-memory operations with JSON persistence | OK | Specified in data model |
| Test-First Development (NON-NEGOTIABLE) | TDD: Tests -> Fail -> Implement | OK | Red-Green-Refactor cycle required |
| CLI-First Interface | Colored output, keyboard nav support | OK | Rich library specified |
| Progressive Enhancement | Core first, advanced later | OK | i18n/voice architected but not implemented |
| Observability | Structured logging, actionable errors | PENDING | Will implement in Phase 1 |
| Project Structure | `.claude/`, `src/`, `tasks.json`, `pyproject.toml` | PENDING | Need to create `src/` structure |

---

## 10-Step Execution Roadmap

### Step 1 — Project Initialization (UV)

**Goal**: Establish clean, reproducible project base

**Actions**:
- Initialize project using `uv init`
- Enforce Python 3.13+ in pyproject.toml
- Generate `pyproject.toml` with dependencies
- Create base folders:
  - `src/`
  - `specs/`
  - `.claude/agents/`
  - `.claude/skills/`
  - `tests/`

**Outcome**: Clean, reproducible project base

---

### Step 2 — Constitution & Specs Lock

**Goal**: Prevent scope creep and freeze architectural rules

**Actions**:
- Ensure finalized documents are in place:
  - `.specify/memory/constitution.md`
  - `specs/todo-app/spec.md`
  - `history/adr/001-multi-agent-architecture.md`
- Verify no conflicting architectural decisions
- Document non-negotiable boundaries

**Outcome**: Clear non-negotiable boundaries

---

### Step 3 — Agent Creation

**Goal**: Responsibility clearly divided

**Actions**: Create agents via prompts (in `.claude/agents/`):
1. `todo-main-agent` - Orchestrates flow, manages lifecycle, coordinates all other agents
2. `todo-state-manager` - Manages in-memory task collection, ID generation, state transitions
3. `todo-storage-agent` - Handles all file I/O for `tasks.json`, JSON serialization
4. `todo-cli-ui-agent` - Renders terminal output using `rich`, handles user input and parsing
5. `todo-search-sort-agent` - Implements search, filter, sort logic without storage access
6. `todo-i18n-agent` - Provides English/Urdu translations, manages RTL/LTR direction
7. `todo-voice-agent` - Handles one-shot voice commands with fallback to text

**Constraints**:
- Each agent has single responsibility
- No agent bypasses Main Agent
- Communication flows only through Main Agent

**Outcome**: Responsibility clearly divided

---

### Step 4 — Skills Declaration

**Goal**: Agents become executable

**Actions**: Declare skills in `.claude/skills/`:
- `task_crud_skill` - Add, update, delete tasks
- `storage_skill` - Load/save tasks.json
- `cli_rendering_skill` - Color output using rich
- `search_filter_sort_skill` - Search, filter, sort logic
- `language_skill` - Urdu/English toggle
- `voice_command_skill` - One-shot voice input
- `uv_bootstrap_skill` - UV project initialization

**Outcome**: Agents become executable

---

### Step 5 — Core Feature Implementation (Stable Base)

**Goal**: Fully working MVP

**Actions**: Implement Basic Level features only:
1. **Add Task**: `todo add "<title>" [--priority <low|medium|high>] [--tags <tag1,tag2>]`
2. **View Tasks**: `todo list [--status <pending|completed>] [--priority <low|medium|high>]`
3. **Update Task**: `todo update <id> [--title <new-title>] [--description <desc>] [--priority <prio>]`
4. **Delete Task**: `todo delete <id>`
5. **Mark Complete**: `todo complete <id>`
6. **Mark Pending**: `todo uncomplete <id>`
7. **Exit**: `todo exit` or Ctrl+C

**Rules**:
- `tasks.json` sync after every change
- No breaking changes allowed later
- All operations must persist atomically

**Implementation Order** (per TDD):
1. Write tests for Storage Agent -> Fail -> Implement Storage Agent
2. Write tests for State Manager -> Fail -> Implement State Manager
3. Write tests for Search Sort Agent -> Fail -> Implement Search Sort Agent
4. Write tests for CLI UI Agent -> Fail -> Implement CLI UI Agent
5. Write tests for Main Agent -> Fail -> Implement Main Agent
6. Write integration tests -> Fail -> Wire all agents together

**Outcome**: Fully working MVP

---

### Step 6 — Intermediate Features (Safe Extension)

**Goal**: Feature-rich but stable app

**Actions**: Add without touching core logic:
1. **Priority Support**: Filter and sort by priority
2. **Tags Support**: Attach tags to tasks, filter by tags
3. **Search**: Keyword search across titles and descriptions
4. **Filtering**: Filter by status, priority, tags
5. **Sorting**: Sort by priority, created date, updated date

**Rule**:
> Extend via agents & skills, never by modifying core flows

**Implementation Order** (per TDD):
1. Extend Search Sort Agent with search, filter, sort logic
2. Extend CLI UI Agent to display tags and priority
3. Update Main Agent to pass new CLI arguments to Search Sort Agent

**Outcome**: Feature-rich but stable app

---

### Step 7 — Language Toggle Integration

**Goal**: Urdu & English supported safely

**Actions**:
1. Add CLI option: `todo lang <en|ur>`
2. Implement I18n Agent with translation dictionary
3. Handle RTL text direction for Urdu
4. Re-render full CLI text on language change
5. Persist language preference in session-level state

**Rules**:
> Language change MUST NOT affect task data or logic
> All prompts and messages must be translatable

**Implementation Order** (per TDD):
1. Write tests for I18n Agent (translations, RTL/LTR)
2. Implement I18n Agent with translation dictionary
3. Update CLI UI Agent to request translations from I18n Agent
4. Update Main Agent to maintain language state
5. Write integration tests for language toggle flow

**Outcome**: Urdu & English supported safely

---

### Step 8 — Voice Command Mode Integration

**Goal**: Experimental feature, no instability

**Actions**:
1. Add CLI option: `todo voice <command>` (one-shot mode)
2. Open microphone once
3. Listen to one command
4. Convert to text (speech-to-text)
5. Close immediately
6. Execute command and return results
7. Fallback to text input if voice unavailable

**Rules**:
> No background listening, no continuous mode
> Voice is optional with graceful fallback

**Dependencies** (optional, install only if available):
- SpeechRecognition library for speech-to-text

**Implementation Order** (per TDD):
1. Write tests for Voice Agent (with mocked speech input)
2. Implement Voice Agent with speech-to-text fallback
3. Update Main Agent to handle voice command input
4. Write integration tests for voice command flow
5. Test on supported platforms (Windows, macOS, Linux)

**Outcome**: Experimental feature, no instability

---

### Step 9 — Regression Check (CRITICAL)

**Goal**: Project stability guaranteed

**Actions**: Verify all core functionality still works:
1. **CRUD Tests**: Add, list, update, delete, complete, uncomplete all pass
2. **Persistence Check**: `tasks.json` not corrupted after all operations
3. **CLI Stability**: No crashes on any command, including edge cases
4. **Optional Agents**: I18n and Voice agents don't break core app
5. **Cross-Platform**: Test on Windows, macOS, Linux (or CI verifies)

**Test Cases** (from spec.md):
- Create task with ID 1 in empty list
- Update task and verify persistence
- Delete task and verify ID never reused
- Toggle complete/uncomplete status
- Search and filter operations
- Language toggle (en -> ur)
- Voice command (with fallback)

**Outcome**: Project stability guaranteed

---

### Step 10 — GitHub Push

**Goal**: Clean, working code pushed to repository

**Actions**:
1. Run all tests and ensure 80%+ coverage
2. Run `/sp.analyze` to verify constitution compliance
3. Commit with meaningful message following commit conventions
4. Push to `https://github.com/Areejshaikh/Hackathon-II-Phase-I`
5. Verify CI/CD passes (if configured)
6. Tag release (v0.1.0)

**Commit Message Template**:
```
feat: Implement Phase-I CLI Todo Application with multi-agent architecture

- Implement 7 agents (5 core + 2 optional)
- Add CRUD operations for tasks
- Implement search, filter, sort
- Support Urdu/English language toggle
- Add experimental voice command mode
- Achieve 80%+ test coverage
- Follow constitution principles

Refs: #specs/todo-app
```

**Outcome**: Clean, working code to GitHub

---

## Project Structure

### Documentation (this feature)

```
specs/todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```
src/
├── main.py              # Entry point: uv run src/main.py
├── models/
│   ├── __init__.py
│   └── task.py          # Task data model with to_dict/from_dict
├── agents/
│   ├── __init__.py
│   ├── main_agent.py    # Orchestrates flow, main loop, app_state
│   ├── state_manager.py # In-memory tasks, ID generation, state transitions
│   ├── storage_agent.py # Load/save tasks.json, atomic writes
│   ├── cli_ui_agent.py  # All rendering & input (uses rich)
│   ├── search_sort_agent.py # Search, filter, sort logic
│   ├── i18n_agent.py    # English/Urdu translations, RTL/LTR
│   └── voice_agent.py   # One-shot speech-to-text with fallback
└── utils/
    ├── __init__.py
    ├── __main__.py      # CLI entry point for uv script
    └── helpers.py       # Utility functions

.claude/
├── agents/              # Agent definitions (Claude Code format)
│   ├── todo-main-agent.md
│   ├── todo-state-manager.md
│   ├── todo-storage-agent.md
│   ├── todo-cli-ui-agent.md
│   ├── todo-search-sort-agent.md
│   ├── todo-i18n-agent.md
│   └── todo-voice-agent.md
└── skills/              # Skill definitions
    ├── task_crud_skill.md
    ├── storage_skill.md
    ├── cli_rendering_skill.md
    ├── search_filter_sort_skill.md
    ├── language_skill.md
    ├── voice_command_skill.md
    └── uv_bootstrap_skill.md

tasks.json               # Persistent task storage
pyproject.toml           # Python project configuration
tests/
├── unit/
│   ├── test_task_model.py
│   ├── test_state_manager.py
│   ├── test_storage_agent.py
│   ├── test_search_sort.py
│   ├── test_cli_ui_agent.py
│   ├── test_i18n_agent.py
│   └── test_voice_agent.py
└── integration/
    ├── test_cli_flow.py
    ├── test_language_toggle.py
    └── test_voice_commands.py
```

**Structure Decision**: Single Python project with modular agent architecture. Source structure follows constitution with `src/models/`, `src/agents/`, and `src/utils/`. Agent definitions in `.claude/agents/` for Claude Code orchestration. Tests mirror source structure with unit and integration tests.

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None yet | - | - |

---

## Phase 0: Research & Decisions

### Resolved Decisions

1. **Rich Library for CLI UI**
   - Decision: Use `rich` library for colorful terminal output
   - Rationale: Cross-platform, well-maintained, supports tables/panels/progress
   - Alternatives considered: `colorama` (less features), `blessed` (older)

2. **JSON Persistence**
   - Decision: Single `tasks.json` file in repository root
   - Rationale: Human-readable, easy backup/restore, no DB required
   - Alternatives considered: SQLite (overkill), YAML (less common)

3. **In-Memory State**
   - Decision: Load all tasks into memory on startup
   - Rationale: Instant operations, simple CRUD, auto-save on mutations
   - Alternatives considered: Lazy loading (slower), direct file I/O (no atomicity)

4. **Auto-Increment ID**
   - Decision: `max(id) + 1` for new task IDs
   - Rationale: Simple, deterministic, never reuses IDs
   - Alternatives considered: UUID (overkill for single-user), GUID (Windows-specific)

5. **UV Package Manager**
   - Decision: Use UV for Python package management
   - Rationale: Fast, modern, deterministic dependency resolution
   - Alternatives considered: pip (slower, less deterministic), poetry (more complex)

6. **Multi-Agent Architecture**
   - Decision: 7 agents with centralized Main Agent orchestration
   - Rationale: Clear separation of concerns, enables independent development/testing
   - Alternatives considered: Monolithic MVC, functional modules, event-driven
   - Documented in ADR-001: [history/adr/001-multi-agent-architecture.md](../../history/adr/001-multi-agent-architecture.md)

### Unknowns (NEEDS CLARIFICATION)

None - all technical decisions resolved from specification.

---

## Phase 1: Design Outputs

### Data Model

See `data-model.md` for complete entity definitions, validation rules, and state transitions.

### API Contracts

See `contracts/` directory for internal agent APIs and CLI interface contracts:
- `contracts/storage-agent.md` - Storage Agent interface
- `contracts/state-manager.md` - State Manager interface
- `contracts/search-sort-agent.md` - Search/Sort Agent interface
- `contracts/cli-ui-agent.md` - CLI UI Agent interface
- `contracts/main-agent.md` - Main Agent interface

### Quick Start

See `quickstart.md` for development setup, testing, and running instructions.

---

## Next Steps

1. **Run `/sp.tasks`** to generate testable implementation tasks with TDD workflow
2. **Initialize UV project** following Step 1
3. **Follow TDD cycle**: Write tests -> Verify they fail -> Implement -> Verify they pass -> Refactor
4. **Create agents in `.claude/agents/`** following Step 3
5. **Declare skills in `.claude/skills/`** following Step 4
6. **Implement agents in order**: storage -> state-manager -> search-sort -> cli-ui -> main -> i18n -> voice
7. **Run regression checks** following Step 9
8. **Run `/sp.analyze`** before marking feature complete to verify constitution compliance
9. **Push to GitHub** following Step 10

---

## Dependencies

### Python Dependencies (from pyproject.toml)

```toml
[project]
name = "todo-app"
version = "0.1.0"
description = "A pure CLI Todo application in Python with JSON persistence"
requires-python = ">=3.13"
dependencies = [
    "rich>=13.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "SpeechRecognition>=3.10.0",  # Optional, for voice commands
]

[project.scripts]
todo = "src.main:main"
```

### Development Dependencies
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `SpeechRecognition>=3.10.0` - Optional, for voice commands

### External Dependencies
- None (offline-first, no network calls required for core features)

---

## Testing Strategy

### Unit Tests
- Each agent has dedicated unit tests in `tests/unit/`
- Mock external dependencies (file system, speech recognition)
- Target 80%+ code coverage

### Integration Tests
- End-to-end CLI flows in `tests/integration/`
- Test all user scenarios from spec.md
- Cross-platform compatibility tests

### Test Execution
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_storage_agent.py
```

---

**Plan Created**: 2025-12-30
**Status**: Ready for `/sp.tasks`
**Last Updated**: 2025-12-30
