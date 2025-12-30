# Todo CLI Constitution

## Core Principles

### I. Multi-Agent Architecture
The system MUST employ a modular multi-agent architecture where each agent has a single, well-defined responsibility. Agents communicate through well-defined interfaces and cannot directly access each other's internal state. This ensures maintainability, testability, and extensibility.

**Rationale**: Separating concerns allows independent development and testing of each component. Adding new features becomes easier when each agent can be extended without affecting others.

### II. In-Memory First with JSON Persistence
The system MUST operate primarily on in-memory data structures for performance, with JSON files serving as the authoritative persistence layer. All state changes MUST be immediately reflected in memory and asynchronously persisted to disk.

**Rationale**: In-memory operations provide instant feedback for CLI interactions. JSON persistence ensures human-readable storage, easy debugging, and simple backup/restore operations without requiring external database infrastructure.

### III. Test-First Development (NON-NEGOTIABLE)
TDD MUST be followed: Tests written → User approved → Tests fail → Then implement. The Red-Green-Refactor cycle is strictly enforced for all new features. Each agent MUST have comprehensive unit tests before integration.

**Rationale**: Tests serve as living documentation and prevent regressions. Writing tests first ensures the implementation is testable by design and meets the specified requirements.

### IV. CLI-First Interface
Every feature MUST be accessible via command-line interface. The CLI MUST provide clear, colored output with keyboard navigation support. Text-based interaction protocols MUST be followed: stdin/args → stdout for results, stderr for errors.

**Rationale**: CLI tools are portable, scriptable, and developer-friendly. A text-based interface ensures the tool works in any terminal and can be automated through scripts.

### V. Progressive Enhancement
Advanced features (voice commands, i18n, recurring tasks) MUST be architected from the start but not over-engineered. Core functionality MUST be complete and stable before advanced features are implemented. Each phase builds incrementally on the previous.

**Rationale**: YAGNI (You Aren't Gonna Need It) principles prevent premature complexity. Starting simple and adding features incrementally reduces risk and ensures each addition is justified by actual user need.

### VI. Observability and Debugging
The system MUST provide structured logging for all operations. Error messages MUST be actionable and include context. All file I/O operations MUST report success/failure with clear status indicators.

**Rationale**: CLI tools often run in automation where logs are the only visibility. Clear logging enables troubleshooting without requiring interactive debugging sessions.

## Project Structure

The codebase MUST follow this structure:

```text
.claude/
├── agents/              # Agent definitions (todo-main-agent, etc.)
└── skills/              # Skill definitions (task_crud_skill, etc.)

src/
├── main.py              # Entry point
├── models/              # Data models (Task, etc.)
├── agents/              # Agent implementations
└── utils/               # Utility functions

tasks.json               # Persistent task storage (JSON format)
pyproject.toml           # Python project configuration
```

**Rationale**: This structure separates concerns between configuration/agents (`.claude/`), source code (`src/`), and data (`tasks.json`). It enables clean imports and clear module boundaries.

## Phase Definition

### Phase I: Foundation
- In-memory task storage with JSON file persistence
- Multi-agent architecture with specialized agents
- CLI interface with colored output
- Basic CRUD operations: add, list, update, delete, toggle status
- Task filtering and search capabilities
- Simple priority and due date support

### Phase II: Advanced Features
- Recurring tasks (daily, weekly, monthly)
- Advanced reminders and notifications
- Task dependencies and blocking states
- Enhanced scheduling capabilities

### Phase III: Internationalization
- Multi-language support with focus on Urdu
- RTL text direction for Urdu/Arabic
- Locale-specific date/number formatting
- User-selectable language preferences

### Phase IV: Voice Commands
- Speech recognition integration
- Voice-based task creation and management
- Text-to-speech feedback
- Multi-language voice support

**Rationale**: Phased development ensures each major feature set is complete and stable before adding complexity. This approach minimizes technical debt and allows user feedback to shape future phases.

## Governance

This constitution supersedes all other development practices. All pull requests and code reviews MUST verify compliance with these principles.

**Amendment Procedure**:
1. Changes MUST be documented with clear rationale
2. Breaking changes to agent interfaces require migration plan
3. Version bumps follow semantic versioning: MAJOR for principle changes, MINOR for additions, PATCH for clarifications

**Compliance**: The `/sp.analyze` command MUST verify constitution compliance before features are marked complete. Complexity that violates these principles MUST be justified in the plan document.

**Guidance**: Use `.claude/commands/` for runtime development guidance and agent-specific instructions.

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
