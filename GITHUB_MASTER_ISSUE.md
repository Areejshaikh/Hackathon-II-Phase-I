## Phase-I CLI Todo Application - 85 Implementation Tasks

**Total Tasks**: 85
**Phases**: 13
**User Stories**: 10
**Target**: Fully functional CLI Todo App with multi-agent architecture

---

## 📋 Overview

This master issue tracks all implementation tasks for building a CLI-based Todo Application using a **multi-agent architecture**. The application demonstrates how AI can be used as a Product Architect to evolve software from simple systems to complex, extensible platforms.

### Key Features
- **Multi-Agent Architecture**: 7 agents (5 core + 2 optional)
- **JSON Persistence**: `tasks.json` as single source of truth
- **TDD Workflow**: Red-Green-Refactor cycle (NON-NEGOTIABLE per constitution)
- **Urdu/English Toggle**: RTL/LTR support
- **Voice Commands**: Experimental one-shot mode

### Repository
- **URL**: https://github.com/Areejshaikh/Hackathon-II-Phase-I
- **Branch**: master

---

## 📚 References

- **[Spec](specs/todo-app/spec.md)** - Feature specification with user stories and requirements
- **[Plan](specs/todo-app/plan.md)** - 10-step execution roadmap and architecture decisions
- **[Tasks](specs/todo-app/tasks.md)** - Detailed task list with dependencies
- **[ADR](history/adr/001-multi-agent-architecture.md)** - Multi-agent architecture decision
- **[Constitution](.specify/memory/constitution.md)** - Project principles and governance

---

## 🚀 Execution Strategy

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|------------|--------|
| Phase 1: Setup | None | Phase 2 |
| Phase 2: Foundational | Phase 1 | All User Stories (3-12) |
| Phase 3-12: User Stories | Phase 2 | Phase 13 |
| Phase 13: Polish | All User Stories | None |

### Recommended Execution Order

1. ✅ **Phase 1: Setup** (4 tasks) - Project initialization
2. 🔴 **Phase 2: Foundational** (13 tasks) - Core infrastructure
   - **CRITICAL**: This phase blocks all user stories
3. 📝 **Phase 3: User Story 1 - Add Task** (8 tasks)
4. 📋 **Phase 4: User Story 2 - List Tasks** (7 tasks)
5. 👁 **Phase 5: User Story 3 - View Task** (6 tasks)
6. ✏️ **Phase 6: User Story 4 - Update Task** (5 tasks)
7. ✅ **Phase 7: User Story 5 - Complete Task** (6 tasks)
8. 🗑️ **Phase 8: User Story 6 - Delete Task** (4 tasks)
9. 🔍 **Phase 9: User Story 7 - Search & Filter** (10 tasks)
10. 📊 **Phase 10: User Story 8 - Sort Tasks** (6 tasks)
11. 🎛️ **Phase 11: User Story 9 - Main Menu** (4 tasks)
12. 💾 **Phase 12: User Story 10 - Persistence** (6 tasks)
13. ✨ **Phase 13: Polish & Validation** (7 tasks)

### TDD Workflow (MANDATORY)

For **each task**, follow this cycle:
1. 🔴 **RED**: Write test, verify it FAILS
2. 🟢 **GREEN**: Write minimal code to pass test
3. 🟡 **REFACTOR**: Improve code while keeping tests green
4. 💾 **COMMIT**: Save progress

---

## ✅ Phase 1: Setup (4 tasks) - [ ] Phase 1 Complete

**Goal**: Project initialization and basic structure. All tasks are independent and can run in parallel.

- [ ] **T001**: Create project directory structure per plan.md: `src/models/`, `src/agents/`, `src/utils/`, `tests/unit/`, `tests/integration/`
- [ ] **T002**: Initialize `pyproject.toml` with Python 3.11+, rich dependency, and pytest for testing
- [ ] **T003** [P]: Create `src/__init__.py`, `src/models/__init__.py`, `src/agents/__init__.py`, `src/utils/__init__.py`
- [ ] **T004** [P]: Create `tests/__init__.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py`

---

## 🔴 Phase 2: Foundational (13 tasks) - [ ] Phase 2 Complete

**Goal**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundational (RED phase - must fail)

- [ ] **T005** [P]: Write unit test for Task dataclass serialization in `tests/unit/test_task_model.py`
- [ ] **T006** [P]: Write unit test for Task dataclass deserialization in `tests/unit/test_task_model.py`
- [ ] **T007** [P]: Write unit test for Task validation (title required, priority enum) in `tests/unit/test_task_model.py`
- [ ] **T008** [P]: Write unit test for storage_agent load_tasks in `tests/unit/test_storage_agent.py`
- [ ] **T009** [P]: Write unit test for storage_agent save_tasks with atomic write in `tests/unit/test_storage_agent.py`

### Implementation for Foundational

- [ ] **T010** [P]: Create TaskStatus enum in `src/models/task.py` (pending, completed values)
- [ ] **T011** [P]: Create TaskPriority enum in `src/models/task.py` (low, medium, high values)
- [ ] **T012** [P]: Create Task dataclass in `src/models/task.py` with all fields and validation
- [ ] **T013** [P]: Implement Task.to_dict() method in `src/models/task.py`
- [ ] **T014** [P]: Implement Task.from_dict() classmethod in `src/models/task.py`
- [ ] **T015** [P]: Create storage_agent module with load_tasks() in `src/agents/storage_agent.py`
- [ ] **T016** [P]: Implement save_tasks() with atomic write in `src/agents/storage_agent.py`
- [ ] **T017** [P]: Implement ensure_file_exists() in `src/agents/storage_agent.py`

**✅ Checkpoint**: Foundation ready - Task model and storage working. User story implementation can now begin.

---

## 📝 Phase 3: User Story 1 - Add Task (8 tasks) - [ ] US1 Complete

**Goal**: Users can create new tasks with title (required), description (optional), priority (optional), and tags (optional). Auto-ID generation and default pending status.

**Independent Test**: Run `pytest tests/unit/test_state_manager.py::test_add_task` - can add a task and retrieve it by ID.

### Tests for User Story 1 (RED phase - must fail)

- [ ] **T018** [P] [US1]: Write unit test for state_manager add_task in `tests/unit/test_state_manager.py`
- [ ] **T019** [P] [US1]: Write unit test for auto-ID generation in `tests/unit/test_state_manager.py`
- [ ] **T020** [P] [US1]: Write unit test for default task status in `tests/unit/test_state_manager.py`

### Implementation for User Story 1

- [ ] **T021** [US1]: Implement initialize_state() in `src/agents/state_manager.py`
- [ ] **T022** [US1]: Implement get_next_id() in `src/agents/state_manager.py`
- [ ] **T023** [US1]: Implement add_task() with validation in `src/agents/state_manager.py`
- [ ] **T024** [US1]: Implement list_tasks() in `src/agents/state_manager.py`
- [ ] **T025** [US1]: Implement get_task() in `src/agents/state_manager.py`

**✅ Checkpoint**: US1 complete - Task creation, ID generation, and retrieval working. Run integration test.

---

## 📋 Phase 4: User Story 2 - List Tasks (7 tasks) - [ ] US2 Complete

**Goal**: Display all tasks in a colorful table showing ID, title, status, priority, tags, and description preview.

**Independent Test**: Add 3 tasks with different priorities, run list - all 3 appear in table.

### Tests for User Story 2 (RED phase - must fail)

- [ ] **T026** [P] [US2]: Write integration test for cli_ui display_tasks_table in `tests/integration/test_cli_flow.py`
- [ ] **T027** [P] [US2]: Write test for empty task list display in `tests/integration/test_cli_flow.py`

### Implementation for User Story 2

- [ ] **T028** [US2]: Implement display_welcome() in `src/agents/cli_ui_agent.py`
- [ ] **T029** [US2]: Implement display_tasks_table() using rich.Table in `src/agents/cli_ui_agent.py`
- [ ] **T030** [US2]: Implement display_success() in `src/agents/cli_ui_agent.py` (green color)
- [ ] **T031** [US2]: Implement display_error() in `src/agents/cli_ui_agent.py` (red color)
- [ ] **T032** [US2]: Implement display_info() in `src/agents/cli_ui_agent.py` (blue color)

**✅ Checkpoint**: US2 complete - Tasks display in colorful table format.

---

## 👁 Phase 5: User Story 3 - View Task (6 tasks) - [ ] US3 Complete

**Goal**: Display full details of a single task by ID.

**Independent Test**: Add task with all fields, view by ID, all fields visible.

### Tests for User Story 3 (RED phase - must fail)

- [ ] **T033** [P] [US3]: Write test for cli_ui display_task_details in `tests/integration/test_cli_flow.py`
- [ ] **T034** [P] [US3]: Write test for prompt_task_id validation in `tests/integration/test_cli_flow.py`

### Implementation for User Story 3

- [ ] **T035** [US3]: Implement prompt_task_id() in `src/agents/cli_ui_agent.py`
- [ ] **T036** [US3]: Implement display_task_details() using rich.Panel in `src/agents/cli_ui_agent.py`
- [ ] **T037** [US3]: Implement display_warning() in `src/agents/cli_ui_agent.py` (yellow color)
- [ ] **T038** [US3]: Implement display_empty_state() in `src/agents/cli_ui_agent.py`

**✅ Checkpoint**: US3 complete - Can view individual task details.

---

## ✏️ Phase 6: User Story 4 - Update Task (5 tasks) - [ ] US4 Complete

**Goal**: Edit task title, description, priority, and tags (not status). Updates timestamp.

**Independent Test**: Create task, update title and priority, verify changes persist.

### Tests for User Story 4 (RED phase - must fail)

- [ ] **T039** [P] [US4]: Write unit test for state_manager update_task in `tests/unit/test_state_manager.py`
- [ ] **T040** [P] [US4]: Write unit test for update_task timestamp in `tests/unit/test_state_manager.py`
- [ ] **T041** [US4]: Write test for prompt_update_task in `tests/integration/test_cli_flow.py`

### Implementation for User Story 4

- [ ] **T042** [US4]: Implement update_task() in `src/agents/state_manager.py`
- [ ] **T043** [US4]: Implement prompt_update_task() in `src/agents/cli_ui_agent.py`

**✅ Checkpoint**: US4 complete - Task fields can be updated with validation.

---

## ✅ Phase 7: User Story 5 - Complete Task (6 tasks) - [ ] US5 Complete

**Goal**: Toggle task status between pending and completed by ID.

**Independent Test**: Create pending task, complete it, verify status changes to completed.

### Tests for User Story 5 (RED phase - must fail)

- [ ] **T044** [P] [US5]: Write unit test for state_manager toggle_task_status in `tests/unit/test_state_manager.py`
- [ ] **T045** [P] [US5]: Write unit test for state_manager complete_task in `tests/unit/test_state_manager.py`
- [ ] **T046** [US5]: Write test for toggle status timestamp update in `tests/unit/test_state_manager.py`

### Implementation for User Story 5

- [ ] **T047** [US5]: Implement toggle_task_status() in `src/agents/state_manager.py`
- [ ] **T048** [US5]: Implement complete_task() in `src/agents/state_manager.py`

**✅ Checkpoint**: US5 complete - Task status can be toggled between pending/completed.

---

## 🗑️ Phase 8: User Story 6 - Delete Task (4 tasks) - [ ] US6 Complete

**Goal**: Delete task by ID with user confirmation.

**Independent Test**: Create 2 tasks, delete 1, verify only 1 remains.

### Tests for User Story 6 (RED phase - must fail)

- [ ] **T049** [P] [US6]: Write unit test for state_manager delete_task in `tests/unit/test_state_manager.py`
- [ ] **T050** [US6]: Write test for prompt_confirmation in `tests/integration/test_cli_flow.py`

### Implementation for User Story 6

- [ ] **T051** [US6]: Implement delete_task() in `src/agents/state_manager.py`
- [ ] **T052** [US6]: Implement prompt_confirmation() in `src/agents/cli_ui_agent.py`

**✅ Checkpoint**: US6 complete - Tasks can be deleted with confirmation.

---

## 🔍 Phase 9: User Story 7 - Search & Filter (10 tasks) - [ ] US7 Complete

**Goal**: Search by keyword (title/description), filter by status, priority, tags. Combined filters supported.

**Independent Test**: Create 5 tasks with various priorities/statuses, filter by priority=high, only high priority tasks shown.

### Tests for User Story 7 (RED phase - must fail)

- [ ] **T053** [P] [US7]: Write unit test for search_tasks in `tests/unit/test_search_sort.py`
- [ ] **T054** [P] [US7]: Write unit test for filter_tasks by status in `tests/unit/test_search_sort.py`
- [ ] **T055** [P] [US7]: Write unit test for filter_tasks by priority in `tests/unit/test_search_sort.py`
- [ ] **T056** [P] [US7]: Write unit test for filter_tasks by tags in `tests/unit/test_search_sort.py`
- [ ] **T057** [P] [US7]: Write unit test for combined search_and_filter in `tests/unit/test_search_sort.py`

### Implementation for User Story 7

- [ ] **T058** [US7]: Implement search_tasks() in `src/agents/search_sort_agent.py`
- [ ] **T059** [US7]: Implement filter_tasks() in `src/agents/search_sort_agent.py`
- [ ] **T060** [US7]: Implement search_and_filter() in `src/agents/search_sort_agent.py`
- [ ] **T061** [US7]: Implement prompt_search() in `src/agents/cli_ui_agent.py`
- [ ] **T062** [US7]: Implement prompt_filters() in `src/agents/cli_ui_agent.py`

**✅ Checkpoint**: US7 complete - Tasks can be searched and filtered.

---

## 📊 Phase 10: User Story 8 - Sort Tasks (6 tasks) - [ ] US8 Complete

**Goal**: Sort tasks by ID (default), priority, or creation order.

**Independent Test**: Create 3 tasks, sort by priority, verify order is high > medium > low.

### Tests for User Story 8 (RED phase - must fail)

- [ ] **T063** [P] [US8]: Write unit test for sort_tasks by ID in `tests/unit/test_search_sort.py`
- [ ] **T064** [P] [US8]: Write unit test for sort_tasks by priority in `tests/unit/test_search_sort.py`
- [ ] **T065** [P] [US8]: Write unit test for sort_tasks reverse order in `tests/unit/test_search_sort.py`

### Implementation for User Story 8

- [ ] **T066** [US8]: Implement sort_tasks() in `src/agents/search_sort_agent.py`
- [ ] **T067** [US8]: Implement process_tasks() (combined search/filter/sort) in `src/agents/search_sort_agent.py`
- [ ] **T068** [US8]: Implement prompt_sort() in `src/agents/cli_ui_agent.py`

**✅ Checkpoint**: US8 complete - Tasks can be sorted by multiple criteria.

---

## 🎛️ Phase 11: User Story 9 - Main Menu (4 tasks) - [ ] US9 Complete

**Goal**: Interactive numbered menu (1-8) for all commands with colorful display. Graceful quit with auto-save.

**Independent Test**: Run app, see menu, select each option, verify correct handler is called.

### Tests for User Story 9 (RED phase - must fail)

- [ ] **T069** [P] [US9]: Write integration test for main menu display in `tests/integration/test_cli_flow.py`
- [ ] **T070** [P] [US9]: Write integration test for menu navigation loop in `tests/integration/test_cli_flow.py`

### Implementation for User Story 9

- [ ] **T071** [US9]: Implement display_main_menu() in `src/agents/cli_ui_agent.py`
- [ ] **T072** [US9]: Implement display_goodbye() in `src/agents/cli_ui_agent.py`

**✅ Checkpoint**: US9 complete - Interactive main menu working.

---

## 💾 Phase 12: User Story 10 - Persistence (6 tasks) - [ ] US10 Complete

**Goal**: Load tasks.json on start, save after every change. Auto-save on exit.

**Independent Test**: Add task, quit, restart app, task still exists.

### Tests for User Story 10 (RED phase - must fail)

- [ ] **T073** [P] [US10]: Write integration test for load on startup in `tests/integration/test_cli_flow.py`
- [ ] **T074** [P] [US10]: Write integration test for save on mutation in `tests/integration/test_cli_flow.py`
- [ ] **T075** [P] [US10]: Write integration test for save on exit in `tests/integration/test_cli_flow.py`

### Implementation for User Story 10

- [ ] **T076** [US10]: Integrate storage_agent into state_manager for auto-save
- [ ] **T077** [US10]: Implement main() entry point with load in `src/main.py`
- [ ] **T078** [US10]: Implement save on exit in `src/main.py`

**✅ Checkpoint**: US10 complete - Tasks persist across app restarts.

---

## ✨ Phase 13: Polish & Validation (7 tasks) - [ ] Phase 13 Complete

**Goal**: Integration testing, validation, and preparation for deployment.

- [ ] **T079** [P]: Run all unit tests: `pytest tests/unit/ -v`
- [ ] **T080** [P]: Run all integration tests: `pytest tests/integration/ -v`
- [ ] **T081** [P]: Verify pyproject.toml has correct entry point: `uv run src/main.py`
- [ ] **T082**: Verify Color scheme compliance per spec (cyan headers, yellow menus, green success, red errors, blue info)
- [ ] **T083**: Run `/sp.analyze` to verify constitution compliance
- [ ] **T084**: Update CLAUDE.md with completed feature
- [ ] **T085**: Create tasks.json sample file for documentation

**✅ Final Checkpoint**: Phase-I complete - Ready for deployment to GitHub!

---

## 📊 Progress Tracking

### Overall Progress

```
Phase 1: Setup     [0/4] tasks    [░░░░░░░░░░░░░░░░] 0%
Phase 2: Foundational  [0/13] tasks   [░░░░░░░░░░░░░░░░] 0%
Phase 3: US1 - Add    [0/8] tasks    [░░░░░░░░░░░░░░░░] 0%
Phase 4: US2 - List   [0/7] tasks    [░░░░░░░░░░░░░░░░] 0%
Phase 5: US3 - View   [0/6] tasks    [░░░░░░░░░░░░░░░░] 0%
Phase 6: US4 - Update  [0/5] tasks    [░░░░░░░░░░░░░░░░] 0%
Phase 7: US5 - Complete  [0/6] tasks    [░░░░░░░░░░░░░░░░] 0%
Phase 8: US6 - Delete   [0/4] tasks    [░░░░░░░░░░░░░░░░] 0%
Phase 9: US7 - Search   [0/10] tasks   [░░░░░░░░░░░░░░░░] 0%
Phase 10: US8 - Sort   [0/6] tasks    [░░░░░░░░░░░░░░░░] 0%
Phase 11: US9 - Menu   [0/4] tasks    [░░░░░░░░░░░░░░░░] 0%
Phase 12: US10 - Persist [0/6] tasks    [░░░░░░░░░░░░░░░░] 0%
Phase 13: Polish    [0/7] tasks    [░░░░░░░░░░░░░░░░] 0%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: [0/85] tasks    [░░░░░░░░░░░░░░░░] 0%
```

---

## 🎯 Success Criteria

- [ ] All 85 tasks completed
- [ ] All tests passing with 80%+ coverage
- [ ] Multi-agent architecture implemented (7 agents)
- [ ] TDD workflow followed (Red-Green-Refactor)
- [ ] Constitution compliance verified
- [ ] Code pushed to GitHub with clean history

---

## 📝 Notes

- **[P] tasks** = Parallel execution (different files, no dependencies)
- **[Story] label** = Maps task to specific user story for traceability
- **TDD is NON-NEGOTIABLE** per constitution - write tests first!
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently

---

**Last Updated**: 2025-12-30
**Status**: Ready to begin implementation
