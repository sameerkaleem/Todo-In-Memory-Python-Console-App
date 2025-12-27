# Tasks: Todo Console App

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)
**Constitution Reference**: `.specify/memory/constitution.md` v1.0.0
**Created**: 2025-12-27

## Summary

| Category | Count |
|----------|-------|
| **Total Tasks** | 32 |
| **Setup Tasks** | 4 |
| **Foundational Tasks** | 4 |
| **User Story Tasks** | 20 |
| **Polish Tasks** | 4 |

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Exact file paths included in all descriptions

## Path Conventions

- **Project layout**: `src/todo/` at repository root (per constitution)
- **Entry point**: `python -m todo`
- **No tests directory**: Manual testing via CLI interaction (per scope)

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create directory structure and initialize Python package

- [x] T001 Create `src/todo/` directory structure at `C:\Users\HP\Desktop\todo_app\todo_console_app\src\todo\`
  - **Verification**: Directory exists and is empty

- [x] T002 [P] Create package marker `src/todo/__init__.py` with `__version__ = "0.1.0"`
  - **Verification**: `import todo` works in Python REPL, `todo.__version__` returns "0.1.0"

- [x] T003 [P] Create entry point `src/todo/__main__.py` with placeholder that prints "Todo App starting..."
  - **Verification**: `python -m todo` prints "Todo App starting..."

- [x] T004 Update `pyproject.toml` for src/ layout with hatchling build backend
  - **Verification**: `uv run python -m todo` executes without import errors

**Checkpoint**: Project structure ready - `python -m todo` runs without errors

---

## Phase 2: Foundational (Core Components)

**Purpose**: Core infrastructure that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [FOUND] Create Task dataclass in `src/todo/models.py`
  - Define: `id: int`, `title: str`, `description: str = ""`, `completed: bool = False`
  - Include module docstring explaining Task entity
  - Include class docstring with field descriptions
  - **Verification**: `Task(id=1, title="Test", description="", completed=False)` instantiates correctly

- [x] T006 [FOUND] Create TaskStore class in `src/todo/storage.py`
  - Implement `__init__()`: Initialize `_tasks: dict[int, Task]` and `_next_id: int = 1`
  - Implement `add(task: Task) -> None`: Store task in dictionary
  - Implement `get(task_id: int) -> Task | None`: Return task or None
  - Implement `get_all() -> list[Task]`: Return all tasks as list
  - Implement `delete(task_id: int) -> bool`: Remove task, return success
  - Implement `next_id() -> int`: Return and increment ID counter
  - Include full type hints and docstrings
  - **Verification**: Can add task, retrieve by ID, get all, delete, IDs never reuse

- [x] T007 [FOUND] Create command functions skeleton in `src/todo/commands.py`
  - Define function signatures with type hints (no implementation yet):
    - `add_task(store: TaskStore, title: str, description: str) -> tuple[bool, str]`
    - `view_tasks(store: TaskStore) -> str`
    - `update_task(store: TaskStore, task_id: int, new_title: str | None, new_desc: str | None) -> tuple[bool, str]`
    - `delete_task(store: TaskStore, task_id: int) -> tuple[bool, str]`
    - `toggle_complete(store: TaskStore, task_id: int) -> tuple[bool, str]`
  - Return placeholder messages for now
  - **Verification**: All functions callable, return correct types

- [x] T008 [FOUND] Create CLI skeleton in `src/todo/cli.py`
  - Define `main()` function that creates TaskStore and enters loop
  - Define `display_menu()` that prints the menu (per spec format)
  - Define placeholder handlers that print "Not implemented"
  - Wire menu choice "6" to exit with "Goodbye!"
  - **Verification**: `python -m todo` shows menu, option 6 exits cleanly

**Checkpoint**: Foundation complete - menu displays, exit works, all modules import correctly

---

## Phase 3: User Story 1 - View All Tasks (Priority: P1)

**Goal**: Users can see all tasks at a glance to understand what needs to be done

**Independent Test**: Start app, select "View Tasks" (option 2) - shows empty list message or task list

**Spec Reference**: US1 acceptance scenarios

### Implementation for User Story 1

- [x] T009 [US1] Implement `view_tasks()` in `src/todo/commands.py`
  - Return "No tasks found." if store.get_all() is empty
  - Format each task: `ID: {id} | [{status}] {title}\n      Description: {description}`
  - Use checkmark symbols per spec
  - **Verification**: Empty store returns "No tasks found.", populated store returns formatted list

- [x] T010 [US1] Implement `handle_view()` in `src/todo/cli.py`
  - Call `view_tasks(store)` and print result
  - **Verification**: Menu option 2 displays tasks or "No tasks found."

**Checkpoint**: View functionality complete - can see empty message, ready for tasks to display

---

## Phase 4: User Story 2 - Add New Task (Priority: P1)

**Goal**: Users can add tasks with title and optional description

**Independent Test**: Add task "Buy groceries" with description, verify it appears in task list

**Spec Reference**: US2 acceptance scenarios

### Implementation for User Story 2

- [x] T011 [US2] Implement `add_task()` in `src/todo/commands.py`
  - Validate title is not empty or whitespace-only
  - Return `(False, "Title cannot be empty.")` if validation fails
  - Generate ID via `store.next_id()`
  - Create Task instance and call `store.add(task)`
  - Return `(True, f"Task added successfully. (ID: {id})")`
  - **Verification**: Empty title rejected, valid title creates task with auto-incremented ID

- [x] T012 [US2] Implement `handle_add()` in `src/todo/cli.py`
  - Prompt "Enter title: " and capture input
  - Prompt "Enter description (optional): " and capture input
  - Call `add_task(store, title, description)`
  - Print success or error message from return tuple
  - **Verification**: Menu option 1 prompts correctly, task added appears in view

**Checkpoint**: Add + View complete - MVP data entry and display functional

---

## Phase 5: User Story 3 - Mark Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task completion status to track progress

**Independent Test**: Add task, toggle status, verify status indicator changes

**Spec Reference**: US3 acceptance scenarios

### Implementation for User Story 3

- [x] T013 [US3] Implement `toggle_complete()` in `src/todo/commands.py`
  - Retrieve task via `store.get(task_id)`
  - Return `(False, f"Task with ID {task_id} not found.")` if None
  - Toggle `task.completed` boolean
  - Return appropriate message based on new state

- [x] T014 [US3] Implement `get_task_id()` helper in `src/todo/cli.py`
  - Prompt "Enter task ID: " and capture input
  - Validate input is numeric
  - Return `int` on success, `None` on invalid input
  - Print "Please enter a valid number." on invalid input
  - **Verification**: "abc" returns None with error, "1" returns 1

- [x] T015 [US3] Implement `handle_toggle()` in `src/todo/cli.py`
  - Call `get_task_id()` to get validated ID
  - If None, return (re-display menu)
  - Call `toggle_complete(store, task_id)`
  - Print result message
  - **Verification**: Menu option 5 toggles task status, invalid ID shows error

**Checkpoint**: Core functionality complete - add, view, and toggle working

---

## Phase 6: User Story 4 - Update Task (Priority: P3)

**Goal**: Users can modify task title or description

**Independent Test**: Add task, update title, verify change persists in view

**Spec Reference**: US4 acceptance scenarios

### Implementation for User Story 4

- [x] T016 [US4] Implement `update_task()` in `src/todo/commands.py`
  - Retrieve task via `store.get(task_id)`
  - Return `(False, f"Task with ID {task_id} not found.")` if None
  - If `new_title` is provided (non-empty), update `task.title`
  - If `new_desc` is provided (not None), update `task.description`
  - Return `(True, "Task updated successfully.")`
  - **Verification**: Update title only preserves description, update both works

- [x] T017 [US4] Implement `handle_update()` in `src/todo/cli.py`
  - Call `get_task_id()` to get validated ID
  - If None, return
  - Prompt "Enter new title (or press Enter to keep): "
  - Prompt "Enter new description (or press Enter to keep): "
  - Pass empty string as None for unchanged fields
  - Call `update_task()` and print result
  - **Verification**: Menu option 3 updates task, Enter key preserves values

**Checkpoint**: Update functionality complete - full CRUD minus delete

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can remove tasks to keep list clean

**Independent Test**: Add task, delete it, verify it no longer appears in view

**Spec Reference**: US5 acceptance scenarios

### Implementation for User Story 5

- [x] T018 [US5] Implement `delete_task()` in `src/todo/commands.py`
  - Call `store.delete(task_id)`
  - If False (task not found), return `(False, f"Task with ID {task_id} not found.")`
  - If True, return `(True, "Task deleted successfully.")`
  - **Verification**: Existing ID deleted, non-existent ID shows error

- [x] T019 [US5] Implement `handle_delete()` in `src/todo/cli.py`
  - Call `get_task_id()` to get validated ID
  - If None, return
  - Call `delete_task(store, task_id)`
  - Print result message
  - **Verification**: Menu option 4 deletes task, task no longer in view

**Checkpoint**: All five core features complete - CRUD operations functional

---

## Phase 8: User Story 6 - Application Lifecycle (Priority: P1)

**Goal**: Clear menu interface with graceful exit and error handling

**Independent Test**: Start app, verify menu displays, test invalid input handling, exit cleanly

**Spec Reference**: US6 acceptance scenarios

### Implementation for User Story 6

- [x] T020 [US6] Finalize menu loop in `src/todo/cli.py` `main()` function
  - Continuous loop until exit selected
  - Display menu after each operation
  - Route choices 1-6 to appropriate handlers
  - **Verification**: Menu re-displays after each operation

- [x] T021 [US6] Implement invalid menu choice handling in `src/todo/cli.py`
  - For choices not in "1"-"6", print "Invalid option. Please try again."
  - Re-display menu
  - **Verification**: "7", "abc", "" all show error and re-prompt

- [x] T022 [US6] Implement KeyboardInterrupt handling in `src/todo/cli.py`
  - Wrap main loop in try/except KeyboardInterrupt
  - Print "Goodbye!" and exit cleanly
  - **Verification**: Ctrl+C exits with goodbye message, no stack trace

- [x] T023 [US6] Implement EOFError handling in `src/todo/cli.py`
  - Handle EOFError in same try/except block
  - Print "Goodbye!" and exit cleanly
  - **Verification**: EOF condition exits gracefully

**Checkpoint**: Application lifecycle complete - robust menu handling

---

## Phase 9: Polish (Cross-Cutting Verification)

**Purpose**: Final verification and edge case handling

- [x] T024 Verify all modules have complete docstrings
  - Check `models.py`, `storage.py`, `commands.py`, `cli.py`
  - Module-level, class-level, and function-level docstrings present
  - **Verification**: Each file has docstrings per PEP 257

- [x] T025 Verify all functions have complete type hints
  - All parameters typed
  - All return types specified
  - Use `| None` syntax (Python 3.10+)
  - **Verification**: Type checker (if available) reports no issues

- [x] T026 Integration test: Full user workflow
  - Add 3 tasks with varying descriptions
  - View all tasks (verify format)
  - Mark one complete (verify status change)
  - Update one task (verify preservation of unchanged fields)
  - Delete one task (verify removal)
  - Exit (verify goodbye message)
  - **Verification**: All operations work in sequence without errors

- [x] T027 Edge case verification
  - Empty title rejection on add
  - Whitespace-only title rejection on add
  - Non-existent ID handling for update/delete/toggle
  - Non-numeric ID input handling
  - Empty task list view message
  - **Verification**: All edge cases produce correct error messages

**Checkpoint**: Application complete and verified

---

## Dependencies & Execution Order

### Phase Dependencies (Strict)

```
Phase 1 (Setup) ─────────────────────┐
                                     │
                                     ▼
Phase 2 (Foundational) ──────────────┼───────────────────────────────┐
                                     │                               │
        ┌────────────────────────────┼───────────────────────────────┤
        │                            │                               │
        ▼                            ▼                               ▼
Phase 3 (US1: View)           Phase 4 (US2: Add)             Phase 8 (US6: Lifecycle)
        │                            │                               │
        │                            │                               │
        └────────────┬───────────────┘                               │
                     │                                               │
                     ▼                                               │
              Phase 5 (US3: Toggle) ─────────────────────────────────┤
                     │                                               │
        ┌────────────┴────────────┐                                  │
        ▼                         ▼                                  │
Phase 6 (US4: Update)     Phase 7 (US5: Delete)                      │
        │                         │                                  │
        └────────────┬────────────┘                                  │
                     │                                               │
                     └───────────────────────────────────────────────┤
                                                                     │
                                                                     ▼
                                                        Phase 9 (Polish)
```

### Task Dependencies Within Phases

| Task | Depends On | Reason |
|------|------------|--------|
| T001 | None | First task |
| T002 | T001 | Directory must exist |
| T003 | T001 | Directory must exist |
| T004 | T002, T003 | Package files must exist |
| T005 | T004 | Project must be runnable |
| T006 | T005 | Needs Task class |
| T007 | T006 | Needs TaskStore class |
| T008 | T007 | Needs commands skeleton |
| T009 | T007 | Implements command function |
| T010 | T008, T009 | Needs CLI skeleton and command |
| T011 | T007 | Implements command function |
| T012 | T008, T011 | Needs CLI skeleton and command |
| T013 | T007 | Implements command function |
| T014 | T008 | CLI helper function |
| T015 | T014, T013 | Needs helper and command |
| T016 | T007 | Implements command function |
| T017 | T014, T016 | Needs helper and command |
| T018 | T007 | Implements command function |
| T019 | T014, T018 | Needs helper and command |
| T020-T023 | T010, T012, T015, T017, T019 | All handlers must exist |
| T024-T027 | All above | Final verification |

### Parallel Execution Opportunities

**Phase 1 Parallel Group**:
- T002 and T003 can run in parallel (after T001)

**Phase 2 Parallel Group**:
- None - sequential dependency chain

**User Story Parallel Groups (after T014 is complete)**:
- T016 and T018 can run in parallel (both only need T007)
- T017 and T019 can run in parallel (after their respective commands)

**Phase 8 Parallel Group**:
- T022 and T023 can run in parallel (independent error handlers)

**Phase 9 Parallel Group**:
- T024 and T025 can run in parallel (documentation checks)

---

## MVP Scope Recommendation

### Minimum Viable Product (Phases 1-4)

For a working demonstration, complete:

1. **Phase 1**: Setup (T001-T004)
2. **Phase 2**: Foundational (T005-T008)
3. **Phase 3**: User Story 1 - View (T009-T010)
4. **Phase 4**: User Story 2 - Add (T011-T012)

**MVP Deliverable**: Users can add tasks and view them. Menu displays and exit works.

**Time Estimate**: 2-3 hours

### Full Implementation (All Phases)

Complete all phases for full feature set per specification.

**Time Estimate**: 4-6 hours

---

## Execution Notes

### Critical Path

The critical path runs through:
T001 -> T002 -> T004 -> T005 -> T006 -> T007 -> T008 -> T009/T011 -> remaining features

### Risk Callouts

1. **Unicode symbols**: If terminal doesn't support checkmarks, may need fallback to `[X]/[ ]`
2. **Input edge cases**: Whitespace-only validation requires `.strip()` before length check
3. **ID handling**: Ensure `next_id()` is called before creating Task, not after

### Commit Strategy

Recommended commit points:
- After Phase 1: "chore: Initialize todo package structure"
- After Phase 2: "feat: Add foundational models and storage"
- After Phase 4: "feat: Implement add and view tasks"
- After Phase 7: "feat: Complete CRUD operations"
- After Phase 9: "chore: Final polish and verification"

---

## Verification Checklist

Before marking complete, verify:

- [x] `python -m todo` launches application
- [x] Menu displays correctly with all 6 options
- [x] Add task with title and description works
- [x] View shows tasks with correct format
- [x] Toggle changes completion status indicator
- [x] Update preserves unchanged fields
- [x] Delete removes task from view
- [x] Exit prints "Goodbye!"
- [x] Invalid menu input shows error
- [x] Invalid ID input shows error
- [x] Empty title shows error
- [x] Non-existent ID shows "Task with ID X not found."
- [x] Ctrl+C exits gracefully
- [x] All code has type hints
- [x] All code has docstrings
