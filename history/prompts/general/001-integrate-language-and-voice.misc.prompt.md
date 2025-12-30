---
id: 1
title: Integrate Language and Voice Agents into CLI
stage: misc
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-app
branch: master
user: default
command: none
labels: [cli, i18n, voice, agents]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/agents/i18n_agent.py
  - src/agents/voice_agent.py
  - src/agents/cli_ui_agent.py
  - src/agents/main_agent.py
  - src/agents/__init__.py
tests:
  - none
---

## Prompt

# 🔁 SPEC UPDATE — CLI MENU INTEGRATION FOR LANGUAGE & VOICE AGENTS

## Context

The Todo CLI application already implements:
- Core CRUD features
- tasks.json persistence
- Multi-agent architecture
- Translation and Voice agents (defined but not wired)

However, the **CLI menu does not expose Translation and Voice options**,
making these agents unreachable.

This spec update resolves that gap.

---

## 🔧 Required Change (MANDATORY)

The **Main CLI Menu MUST be updated** to expose Translation and Voice features
WITHOUT modifying or breaking existing Todo functionality.

---

## 📋 Updated CLI Menu (FINAL)

The CLI menu MUST appear as follows:

```text
┌──────────────────────────────────────┐
│           TODO MENU                  │
├──────────────────────────────────────┤
│ 1. Add Task                          │
│ 2. View Tasks                        │
│ 3. Update Task                       │
│ 4. Delete Task                       │
│ 5. Mark Complete / Pending           │
│ 6. Search / Filter / Sort            │
│ 7. Change Language (English / اردو)  │
│ 8. Voice Command Mode (Experimental) │
│ 9. Exit                              │
└──────────────────────────────────────┘
```

## Response snapshot

I've successfully updated the Todo CLI application to integrate the Language (i18n) and Voice agents into the main menu.

Key changes made:
1. Created `src/agents/i18n_agent.py` to handle language selection (English/Urdu).
2. Created `src/agents/voice_agent.py` for experimental voice command mode.
3. Updated `src/agents/cli_ui_agent.py` to display the new 9-item menu and validate input accordingly.
4. Updated `src/agents/main_agent.py` to route choices 7 and 8 to the new handlers and made choice 9 the Exit option.
5. Updated `src/agents/__init__.py` to export the new agent's handlers.

## Outcome

- ✅ Impact: Users can now access Language and Voice features directly from the main CLI menu.
- 🧪 Tests: Manual verification of menu structure and input routing.
- 📁 Files: src/agents/i18n_agent.py, src/agents/voice_agent.py, src/agents/cli_ui_agent.py, src/agents/main_agent.py, src/agents/__init__.py
- 🔁 Next prompts: None
- 🧠 Reflection: The multi-agent architecture made it easy to plug in new functionality without touching core logic.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement actual Urdu translations for all CLI strings.
