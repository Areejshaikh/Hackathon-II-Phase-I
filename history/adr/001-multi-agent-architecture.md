# ADR-001: Multi-Agent Architecture for CLI Todo Application

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-30
- **Feature:** todo-app
- **Context:** The Phase-I CLI Todo Application requires a clean, extensible architecture that demonstrates how AI can be used as a Product Architect. The application must support incremental feature addition (i18n, voice commands, recurring tasks) without destabilizing core functionality. The spec requires a strict multi-agent architecture with single responsibility principle.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Defines entire codebase structure
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - MVC, monolith, layered considered
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects all components and interactions
-->

## Decision

The system will implement a strict multi-agent architecture with centralized orchestration through a Main Agent. Each agent has a single, well-defined responsibility and communicates through well-defined interfaces only via the Main Agent.

**Core Agents (Required):**
- **Main Agent** (`todo-main-agent`): Orchestrates flow, manages application lifecycle, coordinates all other agents, maintains global app_state
- **State Manager** (`todo-state-manager`): Manages in-memory task collection, handles ID generation, enforces state transitions
- **Storage Agent** (`todo-storage-agent`): Handles all file I/O for `tasks.json`, performs JSON serialization/deserialization
- **CLI UI Agent** (`todo-cli-ui-agent`): Renders all terminal output using `rich`, handles user input and command parsing
- **Search Sort Agent** (`todo-search-sort-agent`): Implements search, filter, and sort logic without accessing storage directly

**Optional Agents (Architected but implemented progressively):**
- **I18n Agent** (`todo-i18n-agent`): Provides translations for English/Urdu, manages RTL/LTR text direction
- **Voice Agent** (`todo-voice-agent`): Handles speech-to-text for one-shot voice commands with fallback to text
- **Advanced Agent** (`todo-advanced-agent`): Manages recurring tasks, due dates, reminders, task dependencies

**Architecture Rules:**
1. No agent may bypass the Main Agent
2. All inter-agent communication flows through the Main Agent
3. Agents cannot directly access each other's internal state
4. Each agent has a single responsibility
5. Optional features must not break core flows
6. State is maintained in-memory by State Manager and persisted by Storage Agent

## Consequences

### Positive

- **Maintainability**: Single responsibility per agent enables independent development and testing of each component
- **Extensibility**: Adding new features (i18n, voice, recurring tasks) creates new agents without modifying existing ones
- **Testability**: Each agent can be unit tested in isolation with clear interfaces
- **Parallel Development**: Multiple agents can be developed and tested independently
- **Clear Boundaries**: Well-defined interfaces prevent coupling and side effects
- **Progressive Enhancement**: Optional agents (i18n, voice) are architected from the start but not over-engineered
- **Demonstrates AI as Product Architect**: Multi-agent architecture showcases how AI can architect systems

### Negative

- **Initial Complexity**: More files and boilerplate compared to a simple monolithic script
- **Learning Curve**: Developers must understand agent coordination and interface contracts
- **Communication Overhead**: All inter-agent communication flows through Main Agent, adding indirectness
- **Over-engineering Risk**: For a simple CLI todo app, agents may feel like over-engineering
- **Debugging Complexity**: Tracing execution flow across multiple agents can be more difficult
- **Orchestrator Bottleneck**: Main Agent becomes central coordinator that could become complex

## Alternatives Considered

### Alternative 1: Monolithic MVC Architecture
**Components**: Single application with Model (data), View (CLI output), Controller (logic) layers

**Why Rejected:**
- Tightly coupled layers make it harder to add optional features (i18n, voice) without affecting core
- Less demonstrative of AI as Product Architect
- Progressive enhancement would require more refactoring
- Single responsibility is harder to enforce with broader layers

### Alternative 2: Functional Decomposition with Modules
**Components**: Independent modules for storage, UI, search, state with direct imports

**Why Rejected:**
- Direct imports create coupling between modules
- No central orchestration makes it harder to enforce architecture rules
- Harder to demonstrate agent-based design pattern
- Less clear separation between interface and implementation

### Alternative 3: Plugin-based Architecture
**Components**: Core plugin system with dynamic loading of feature plugins

**Why Rejected:**
- Overkill for a CLI application with known agents
- Dynamic loading adds complexity without clear benefits
- Harder to test and debug
- Performance overhead not justified for known agent set

### Alternative 4: Event-Driven Architecture
**Components**: Agents communicate via event bus without central orchestrator

**Why Rejected:**
- For a CLI app, event bus adds unnecessary complexity
- Harder to reason about execution flow and sequencing
- More difficult to test (event ordering and timing)
- Constitution requires central orchestration via Main Agent

## References

- Feature Spec: [specs/todo-app/spec.md](../../specs/todo-app/spec.md)
- Implementation Plan: [specs/todo-app/plan.md](../../specs/todo-app/plan.md)
- Data Model: [specs/todo-app/data-model.md](../../specs/todo-app/data-model.md)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- Agent Contracts: [specs/todo-app/contracts/](../../specs/todo-app/contracts/)
- Related ADRs: None
- Evaluator Evidence: [history/prompts/todo-app/006-create-spec-file.spec.prompt.md](../prompts/todo-app/006-create-spec-file.spec.prompt.md)
