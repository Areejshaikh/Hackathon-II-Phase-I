# Tasks: todo-app

**Input**: Design documents from `/specs/todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/
**TDD Mode**: YES - Tests MUST be written and FAIL before implementation (per constitution)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing. Constitution mandates Red-Green-Refactor cycle for all features.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US10)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure. All tasks here are independent and can run in parallel.

- [ ] T001 Create project directory structure per plan.md: src/models/, src/agents/, src/utils/, tests/unit/, tests/integration/
- [ ] T002 Initialize pyproject.toml with Python 3.11+, rich dependency, and pytest for testing
- [ ] T003 [P] Create src/__init__.py, src/models/__init__.py, src/agents/__init__.py, src/utils/__init__.py
- [ ] T004 [P] Create tests/__init__.py, tests/unit/__init__.py, tests/integration/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented. This includes the Task model (used by all stories) and Storage agent (used by all mutations).

**CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundational (RED phase - must fail)

- [ ] T005 [P] Write unit test for Task dataclass serialization in tests/unit/test_task_model.py
- [ ] T006 [P] Write unit test for Task dataclass deserialization in tests/unit/test_task_model.py
- [ ] T007 [P] Write unit test for Task validation (title required, priority enum) in tests/unit/test_task_model.py
- [ ] T008 [P] Write unit test for storage_agent load_tasks in tests/unit/test_storage_agent.py
- [ ] T009 [P] Write unit test for storage_agent save_tasks with atomic write in tests/unit/test_storage_agent.py

### Implementation for Foundational

- [ ] T010 Create TaskStatus enum in src/models/task.py (pending, completed values)
- [ ] T011 [P] Create TaskPriority enum in src/models/task.py (low, medium, high values)
- [ ] T012 [P] Create Task dataclass in src/models/task.py with all fields and validation
- [ ] T013 [P] Implement Task.to_dict() method in src/models/task.py
- [ ] T014 [P] Implement Task.from_dict() classmethod in src/models/task.py
- [ ] T015 Create storage_agent module with load_tasks() in src/agents/storage_agent.py
- [ ] T016 [P] Implement save_tasks() with atomic write in src/agents/storage_agent.py
- [ ] T017 [P] Implement ensure_file_exists() in src/agents/storage_agent.py

**Checkpoint**: Foundation ready - Task model and storage working. User story implementation can now begin.

---

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks with title (required), description (optional), priority (optional), and tags (optional). Auto-ID generation and default pending status.

**Independent Test**: Run `pytest tests/unit/test_state_manager.py::test_add_task` - can add a task and retrieve it by ID.

### Tests for User Story 1 (RED phase - must fail)

- [ ] T018 [P] [US1] Write unit test for state_manager add_task in tests/unit/test_state_manager.py
- [ ] T019 [P] [US1] Write unit test for auto-ID generation in tests/unit/test_state_manager.py
- [ ] T020 [P] [US1] Write unit test for default task status in tests/unit/test_state_manager.py

### Implementation for User Story 1

- [ ] T021 [US1] Implement initialize_state() in src/agents/state_manager.py
- [ ] T022 [US1] Implement get_next_id() in src/agents/state_manager.py
- [ ] T023 [US1] Implement add_task() with validation in src/agents/state_manager.py
- [ ] T024 [US1] Implement list_tasks() in src/agents/state_manager.py
- [ ] T025 [US1] Implement get_task() in src/agents/state_manager.py

**Checkpoint**: US1 complete - Task creation, ID generation, and retrieval working. Run integration test.

---

## Phase 4: User Story 2 - List Tasks (Priority: P2)

**Goal**: Display all tasks in a colorful table showing ID, title, status, priority, tags, and description preview.

**Independent Test**: Add 3 tasks with different priorities, run list - all 3 appear in table.

### Tests for User Story 2 (RED phase - must fail)

- [ ] T026 [P] [US2] Write integration test for cli_ui display_tasks_table in tests/integration/test_cli_flow.py
- [ ] T027 [P] [US2] Write test for empty task list display in tests/integration/test_cli_flow.py

### Implementation for User Story 2

- [ ] T028 [US2] Implement display_welcome() in src/agents/cli_ui_agent.py
- [ ] T029 [US2] Implement display_tasks_table() using rich.Table in src/agents/cli_ui_agent.py
- [ ] T030 [US2] Implement display_success() in src/agents/cli_ui_agent.py (green color)
- [ ] T031 [US2] Implement display_error() in src/agents/cli_ui_agent.py (red color)
- [ ] T032 [US2] Implement display_info() in src/agents/cli_ui_agent.py (blue color)

**Checkpoint**: US2 complete - Tasks display in colorful table format.

---

## Phase 5: User Story 3 - View Task (Priority: P3)

**Goal**: Display full details of a single task by ID.

**Independent Test**: Add task with all fields, view by ID, all fields visible.

### Tests for User Story 3 (RED phase - must fail)

- [ ] T033 [P] [US3] Write test for cli_ui display_task_details in tests/integration/test_cli_flow.py
- [ ] T034 [P] [US3] Write test for prompt_task_id validation in tests/integration/test_cli_flow.py

### Implementation for User Story 3

- [ ] T035 [US3] Implement prompt_task_id() in src/agents/cli_ui_agent.py
- [ ] T036 [US3] Implement display_task_details() using rich.Panel in src/agents/cli_ui_agent.py
- [ ] T037 [US3] Implement display_warning() in src/agents/cli_ui_agent.py (yellow color)
- [ ] T038 [US3] Implement display_empty_state() in src/agents/cli_ui_agent.py

**Checkpoint**: US3 complete - Can view individual task details.

---

## Phase 6: User Story 4 - Update Task (Priority: P4)

**Goal**: Edit task title, description, priority, and tags (not status). Updates timestamp.

**Independent Test**: Create task, update title and priority, verify changes persist.

### Tests for User Story 4 (RED phase - must fail)

- [ ] T039 [P] [US4] Write unit test for state_manager update_task in tests/unit/test_state_manager.py
- [ ] T040 [P] [US4] Write unit test for update_task timestamp in tests/unit/test_state_manager.py
- [ ] T041 [P] [US4] Write test for prompt_update_task in tests/integration/test_cli_flow.py

### Implementation for User Story 4

- [ ] T042 [US4] Implement update_task() in src/agents/state_manager.py
- [ ] T043 [US4] Implement prompt_update_task() in src/agents/cli_ui_agent.py

**Checkpoint**: US4 complete - Task fields can be updated with validation.

---

## Phase 7: User Story 5 - Complete Task (Priority: P5)

**Goal**: Toggle task status between pending and completed by ID.

**Independent Test**: Create pending task, complete it, verify status changes to completed.

### Tests for User Story 5 (RED phase - must fail)

- [ ] T044 [P] [US5] Write unit test for state_manager toggle_task_status in tests/unit/test_state_manager.py
- [ ] T045 [P] [US5] Write unit test for state_manager complete_task in tests/unit/test_state_manager.py
- [ ] T046 [P] [US5] Write test for toggle status timestamp update in tests/unit/test_state_manager.py

### Implementation for User Story 5

- [ ] T047 [US5] Implement toggle_task_status() in src/agents/state_manager.py
- [ ] T048 [US5] Implement complete_task() in src/agents/state_manager.py

**Checkpoint**: US5 complete - Task status can be toggled between pending/completed.

---

## Phase 8: User Story 6 - Delete Task (Priority: P6)

**Goal**: Delete task by ID with user confirmation.

**Independent Test**: Create 2 tasks, delete 1, verify only 1 remains.

### Tests for User Story 6 (RED phase - must fail)

- [ ] T049 [P] [US6] Write unit test for state_manager delete_task in tests/unit/test_state_manager.py
- [ ] T050 [P] [US6] Write test for prompt_confirmation in tests/integration/test_cli_flow.py

### Implementation for User Story 6

- [ ] T051 [US6] Implement delete_task() in src/agents/state_manager.py
- [ ] T052 [US6] Implement prompt_confirmation() in src/agents/cli_ui_agent.py

**Checkpoint**: US6 complete - Tasks can be deleted with confirmation.

---

## Phase 9: User Story 7 - Search & Filter (Priority: P7)

**Goal**: Search by keyword (title/description), filter by status, priority, tags. Combined filters supported.

**Independent Test**: Create 5 tasks with various priorities/statuses, filter by priority=high, only high priority tasks shown.

### Tests for User Story 7 (RED phase - must fail)

- [ ] T053 [P] [US7] Write unit test for search_tasks in tests/unit/test_search_sort.py
- [ ] T054 [P] [US7] Write unit test for filter_tasks by status in tests/unit/test_search_sort.py
- [ ] T055 [P] [US7] Write unit test for filter_tasks by priority in tests/unit/test_search_sort.py
- [ ] T056 [P] [US7] Write unit test for filter_tasks by tags in tests/unit/test_search_sort.py
- [ ] T057 [P] [US7] Write unit test for combined search_and_filter in tests/unit/test_search_sort.py

### Implementation for User Story 7

- [ ] T058 [US7] Implement search_tasks() in src/agents/search_sort_agent.py
- [ ] T059 [US7] Implement filter_tasks() in src/agents/search_sort_agent.py
- [ ] T060 [US7] Implement search_and_filter() in src/agents/search_sort_agent.py
- [ ] T061 [US7] Implement prompt_search() in src/agents/cli_ui_agent.py
- [ ] T062 [US7] Implement prompt_filters() in src/agents/cli_ui_agent.py

**Checkpoint**: US7 complete - Tasks can be searched and filtered.

---

## Phase 10: User Story 8 - Sort Tasks (Priority: P8)

**Goal**: Sort tasks by ID (default), priority, or creation order.

**Independent Test**: Create 3 tasks, sort by priority, verify order is high > medium > low.

### Tests for User Story 8 (RED phase - must fail)

- [ ] T063 [P] [US8] Write unit test for sort_tasks by ID in tests/unit/test_search_sort.py
- [ ] T064 [P] [US8] Write unit test for sort_tasks by priority in tests/unit/test_search_sort.py
- [ ] T065 [P] [US8] Write unit test for sort_tasks reverse order in tests/unit/test_search_sort.py

### Implementation for User Story 8

- [ ] T066 [US8] Implement sort_tasks() in src/agents/search_sort_agent.py
- [ ] T067 [US8] Implement process_tasks() (combined search/filter/sort) in src/agents/search_sort_agent.py
- [ ] T068 [US8] Implement prompt_sort() in src/agents/cli_ui_agent.py

**Checkpoint**: US8 complete - Tasks can be sorted by multiple criteria.

---

## Phase 11: User Story 9 - Main Menu (Priority: P9)

**Goal**: Interactive numbered menu (1-8) for all commands with colorful display. Graceful quit with auto-save.

**Independent Test**: Run app, see menu, select each option, verify correct handler is called.

### Tests for User Story 9 (RED phase - must fail)

- [ ] T069 [P] [US9] Write integration test for main menu display in tests/integration/test_cli_flow.py
- [ ] T070 [P] [US9] Write integration test for menu navigation loop in tests/integration/test_cli_flow.py

### Implementation for User Story 9

- [ ] T071 [US9] Implement display_main_menu() in src/agents/cli_ui_agent.py
- [ ] T072 [US9] Implement display_goodbye() in src/agents/cli_ui_agent.py

**Checkpoint**: US9 complete - Interactive main menu working.

---

## Phase 12: User Story 10 - Persistence (Priority: P10)

**Goal**: Load tasks.json on start, save after every change. Auto-save on exit.

**Independent Test**: Add task, quit, restart app, task still exists.

### Tests for User Story 10 (RED phase - must fail)

- [ ] T073 [P] [US10] Write integration test for load on startup in tests/integration/test_cli_flow.py
- [ ] T074 [P] [US10] Write integration test for save on mutation in tests/integration/test_cli_flow.py
- [ ] T075 [P] [US10] Write integration test for save on exit in tests/integration/test_cli_flow.py

### Implementation for User Story 10

- [ ] T076 [US10] Integrate storage_agent into state_manager for auto-save
- [ ] T077 [US10] Implement main() entry point with load in src/main.py
- [ ] T078 [US10] Implement save on exit in src/main.py

**Checkpoint**: US10 complete - Tasks persist across app restarts.

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories. Integration testing and validation.

- [ ] T079 [P] Run all unit tests: pytest tests/unit/ -v
- [ ] T080 [P] Run all integration tests: pytest tests/integration/ -v
- [ ] T081 [P] Verify pyproject.toml has correct entry point: uv run src/main.py
- [ ] T082 Verify Color scheme compliance per spec (cyan headers, yellow menus, green success, red errors, blue info)
- [ ] T083 Run /sp.analyze to verify constitution compliance
- [ ] T084 Update CLAUDE.md with completed feature
- [ ] T085 Create tasks.json sample file for documentation

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|------------|--------|
| Setup (1) | None | Foundational |
| Foundational (2) | Setup | All User Stories |
| User Stories (3-12) | Foundational | Polish |
| Polish (13) | All User Stories | None |

### User Story Dependencies

- **US1 (Add)**: Can start after Foundational - No dependencies on other stories
- **US2 (List)**: Depends on US1 (needs tasks to list)
- **US3 (View)**: Depends on US1 (needs tasks to view)
- **US4 (Update)**: Depends on US1 (needs tasks to update)
- **US5 (Complete)**: Depends on US1 (needs tasks to complete)
- **US6 (Delete)**: Depends on US1 (needs tasks to delete)
- **US7 (Search)**: Depends on US1 (needs tasks to search)
- **US8 (Sort)**: Depends on US1 (needs tasks to sort)
- **US9 (Menu)**: Can start after US2-US8 handlers exist
- **US10 (Persistence)**: Depends on all mutation stories (US1, US4, US5, US6)

### Recommended Execution Order

1. Phase 1: Setup (can do in any order marked [P])
2. Phase 2: Foundational (T005-T017 in sequence)
3. US1 (Add Task) - Foundation for everything
4. US2 (List) + US3 (View) - Can run in parallel after US1
5. US4 (Update) + US5 (Complete) - Can run in parallel after US1
6. US6 (Delete) - After US1
7. US7 (Search) + US8 (Sort) - Can run in parallel after US1
8. US9 (Menu) - After core handlers exist
9. US10 (Persistence) - After all mutation stories
10. Phase 13: Polish

---

## Parallel Opportunities

### Within Phase 1 (Setup)
- T001, T002, T003, T004 all can run in parallel

### Within Phase 2 (Foundational)
- T005-T009 (tests) can run in parallel
- T010-T014 (Task model) can run in parallel
- T015-T017 (storage) can run in parallel after T010-T014

### Within Each User Story
- Tests for a story (marked [P]) can run in parallel
- Model components can run in parallel
- Different user stories can be worked on in parallel after Foundational

### Recommended Parallel Strategy

```
Developer A: Complete Phase 1 + Foundational
Developer B: US1 + US2 (after Foundational)
Developer C: US3 + US4 (after Foundational)
Developer D: US5 + US6 (after Foundational)
...
```

---

## Implementation Strategy

### MVP First (Core CRUD)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete US1: Add Task
4. Complete US2: List Tasks
5. **STOP and VALIDATE**: Basic task management working
6. Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 + US2 → Basic CRUD (demoable!)
3. Add US3 + US4 → Full CRUD (demoable!)
4. Add US5 + US6 → Status management (demoable!)
5. Add US7 + US8 → Search/Sort (demoable!)
6. Add US9 + US10 → Complete app

### TDD Workflow (CONSTITUTION MANDATED)

For each task:
1. **RED**: Write test, verify it FAILS
2. **GREEN**: Write minimal code to pass test
3. **REFACTOR**: Improve code while keeping tests green
4. **COMMIT**: Save progress

---

## Test Summary

| Category | Test Files | Coverage |
|----------|------------|----------|
| Unit Tests | test_task_model.py, test_state_manager.py, test_storage_agent.py, test_search_sort.py | Core logic |
| Integration Tests | test_cli_flow.py | End-to-end user journeys |
| Total Test Count | 8 test files | ~40-50 test cases expected |

---

## Notes

- **[P] tasks** = different files, no dependencies - can run in parallel
- **[Story] label** = maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **TDD is NON-NEGOTIABLE** per constitution - write tests first!
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
