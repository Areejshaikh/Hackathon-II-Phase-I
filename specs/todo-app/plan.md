# Implementation Plan: todo-app

**Branch**: `master` | **Date**: 2025-12-30 | **Spec**: [Phase-I CLI Todo Application Specification](history/prompts/todo-app/002-phase-i-cli-todo-application-specification.spec.prompt.md)
**Input**: Feature specification captured in PHR 002

## Summary

Phase-I delivers a pure CLI Todo application in Python with:
- JSON persistence (`tasks.json`) as single source of truth
- Colorful terminal UI using `rich` library
- Strict multi-agent architecture with 5 core agents
- TDD workflow (Red-Green-Refactor cycle)

The implementation follows spec-driven development (SDD) methodology with clear agent boundaries and in-memory state management.

## Technical Context

**Language/Version**: Python 3.11+ (use `python --version` to verify)
**Primary Dependencies**:
- `rich` - Colorful terminal output and tables
- `json` - Persistence (stdlib)
- `uuid` - ID generation (stdlib)
**Storage**: `tasks.json` file in repository root (JSON format)
**Testing**: pytest (pytest for unit/integration tests)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single CLI application
**Performance Goals**: <10k tasks, instant operations (<100ms)
**Constraints**: CLI only, no web/API, no database
**Scale/Scope**: Single user, local persistence

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| Multi-Agent Architecture | Modular agents with single responsibilities | ✅ | 5 agents defined in spec |
| In-Memory First + JSON Persistence | In-memory operations with JSON persistence | ✅ | Specified in data model |
| Test-First Development (NON-NEGOTIABLE) | TDD: Tests → Fail → Implement | ✅ | Red-Green-Refactor cycle required |
| CLI-First Interface | Colored output, keyboard nav support | ✅ | Rich library specified |
| Progressive Enhancement | Core first, advanced later | ✅ | i18n/voice architected but not implemented |
| Observability | Structured logging, actionable errors | ⚠️ | Will implement in Phase 1 |
| Project Structure | `.claude/`, `src/`, `tasks.json`, `pyproject.toml` | ⚠️ | Need to create `src/` structure |

## Project Structure

### Documentation (this feature)

```text
specs/todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (this plan)
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py              # Entry point: uv run src/main.py
├── models/
│   └── task.py          # Task data model
├── agents/
│   ├── __init__.py
│   ├── main_agent.py    # Orchestrates flow, main loop
│   ├── state_manager.py # In-memory tasks, ID generation
│   ├── storage_agent.py # Load/save tasks.json
│   ├── cli_ui_agent.py  # All rendering & input (uses rich)
│   └── search_sort_agent.py # Search, filter, sort logic
└── utils/
    ├── __init__.py
    └── helpers.py       # Utility functions

tasks.json               # Persistent task storage
pyproject.toml           # Python project configuration
tests/
├── unit/
│   ├── test_task_model.py
│   ├── test_state_manager.py
│   ├── test_storage_agent.py
│   └── test_search_sort.py
└── integration/
    └── test_cli_flow.py
```

**Structure Decision**: Single Python project with modular agent architecture. Source structure follows constitution with `src/models/`, `src/agents/`, and `src/utils/`. Tests mirror source structure with unit and integration tests.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None yet | - | - |

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

### Unknowns (NEEDS CLARIFICATION)

None - all technical decisions resolved from specification.

## Phase 1: Design Outputs

### Data Model

See `data-model.md` for complete entity definitions, validation rules, and state transitions.

### API Contracts

See `contracts/` directory for internal agent APIs and CLI interface contracts.

### Quick Start

See `quickstart.md` for development setup, testing, and running instructions.

## Next Steps

1. **Run `/sp.tasks`** to generate testable implementation tasks
2. **Follow TDD cycle**: Write tests → Verify they fail → Implement → Verify they pass → Refactor
3. **Update agent context** by running the update-agent-context.ps1 script
4. **Implement agents in order**: storage → state-manager → search-sort → cli-ui → main
5. **Run `/sp.analyze`** before marking feature complete to verify constitution compliance

---

**Plan Created**: 2025-12-30
**Status**: Ready for `/sp.tasks`
