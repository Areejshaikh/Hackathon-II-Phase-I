---
id: "002"
title: "Phase-I CLI Todo Application Specification"
stage: "spec"
date: "2025-12-30"
surface: "agent"
model: "sonnet-4-5-20250929"
feature: "todo-app"
branch: "master"
user: "local_user"
command: "/sp.specify"
labels: ["specification", "cli", "todo-app", "phase-i"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "none (specification provided in prompt)"
tests:
  - "none (pending implementation)"
---

## Prompt

# sp.specify
**Title: Phase-I CLI Todo Application Specification**

---

### 1. PROJECT OVERVIEW
Phase-I delivers a **pure CLI Todo app** in Python with JSON persistence (`tasks.json`), colorful terminal UI, and strict multi-agent architecture.

**Goal:** Simple, beginner-friendly, extensible Todo manager demonstrating spec-driven, agent-based development.

**Compliant with:** `sp.constitution`
**Out of Scope:** Web/API, GUI, databases, cloud sync, advanced features (due dates, subtasks, etc.).

---

### 2. FEATURES

#### Must Implement
1. **Add Task**
   - Required: title
   - Optional: description, priority (`low`/`medium`/`high`), tags (list)
   - Auto ID (incremental), default status: `pending`

2. **List Tasks**
   - Colorful table/list showing ID, title, status, priority, tags, description preview

3. **View Task** – Full details by ID

4. **Update Task** – Edit title, description, priority, tags (not status)

5. **Complete Task** – Toggle status (`pending` ↔ `completed`) by ID

6. **Delete Task** – By ID, with confirmation

7. **Search & Filter**
   - Keyword search (title/description)
   - Filter by status, priority, tags
   - Combined filters supported

8. **Sort Tasks**
   - By ID (default), priority, creation order

9. **Main Menu**
   - Numbered, colorful interactive menu for all commands
   - Graceful quit (auto-save)

10. **Persistence**
    - Load `tasks.json` on start (handle missing file)
    - Save after every change

#### Optional (Architect Only)
11. Internationalization prep (easy string localization, Urdu placeholder)
12. Voice command placeholders

---

### 3. NON-FUNCTIONAL REQUIREMENTS
- CLI only (no GUI/web/API)
- Colorful output via `rich` (preferred):
  - Cyan: headers/titles
  - Yellow: menus/warnings
  - Green: success
  - Red: errors
  - Blue: info
- User-friendly prompts, clear errors, confirmations for deletions
- Fast (<10k tasks), robust error handling
- Auto-save on mutations and exit

---

### 4. DATA MODEL (`tasks.json` → list of dicts)
```json
{
  "id": int,                     // unique, never reused
  "title": str,                  // required
  "description": str | null,     // optional
  "status": "pending" | "completed",
  "priority": "low" | "medium" | "high" | null,
  "tags": [str] | null           // optional
}
```
Next ID: `max(ID) + 1` or tracked in state.

---

### 5. AGENT ARCHITECTURE (Required)
- **todo-main-agent**: Orchestrates flow, main loop, delegates
- **todo-state-manager**: In-memory tasks, ID generation, mutations
- **todo-storage-agent**: Load/save `tasks.json` only
- **todo-cli-ui-agent**: All rendering & input (uses `rich`)
- **todo-search-sort-agent**: Search, filter, sort logic

Clear boundaries — agents communicate via functions/messages only.
Optional (architected): `todo-i18n-agent`, `todo-voice-agent`

---

### 6. CLI FLOW
Startup → load tasks → main menu loop:
1. Add    2. List    3. View    4. Update    5. Complete    6. Delete    7. Search/Filter    8. Quit

---

### 7. ACCEPTANCE CRITERIA
- All required features work end-to-end
- `tasks.json` is single source of truth
- Colors follow spec
- Code complies with `sp.constitution` (structure, standards, constraints)
- Runs via `uv run src/main.py`

This concise specification is the contract for Phase-I. All work must align with it and `sp.constitution`.

## Response snapshot

Received and recorded comprehensive Phase-I specification for CLI Todo Application including:
- 10 required features (Add, List, View, Update, Complete, Delete, Search/Filter, Sort, Main Menu, Persistence)
- Data model with JSON schema (id, title, description, status, priority, tags)
- 5 required agents (main, state-manager, storage, cli-ui, search-sort)
- Color scheme requirements using `rich` library
- TDD workflow requirement (Red-Green-Refactor)
- Entry point: `uv run src/main.py`

## Outcome

- ✅ Impact: Phase-I specification recorded for CLI Todo Application with 10 required features and 5-agent architecture
- 🧪 Tests: Pending - TDD cycle to begin with `/sp.plan` and `/sp.tasks`
- 📁 Files: `history/prompts/todo-app/002-phase-i-cli-todo-application-specification.spec.prompt.md`
- 🔁 Next prompts: `/sp.plan` to create architecture plan, then `/sp.tasks` for implementation tasks
- 🧠 Reflection: Specification is comprehensive and aligned with constitution principles. Multi-agent architecture, JSON persistence, and colorful CLI output are clearly defined. Ready for architectural planning.

## Evaluation notes (flywheel)

- Failure modes observed: "none"
- Graders run and results (PASS/FAIL): "N/A"
- Prompt variant (if applicable): "none"
- Next experiment (smallest change to try): "none"
