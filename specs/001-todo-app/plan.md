# Implementation Plan: Todo Console App

**Branch**: `001-todo-app` | **Date**: 2025-12-27 | **Spec**: `specs/001-todo-app/spec.md`
**Input**: Feature specification from `/specs/001-todo-app/spec.md`
**Constitution**: `.specify/memory/constitution.md` v1.0.0

## Summary

A command-line todo application implementing five core operations (add, view, update, delete, mark complete) through an interactive menu-driven interface. The application uses in-memory storage exclusively, implemented with Python 3.13+ standard library only. Architecture follows clean separation of concerns with distinct layers for models, storage, commands, and CLI handling.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Standard library only (dataclasses, typing)
**Storage**: In-memory dictionary-based storage (no persistence)
**Testing**: Manual testing via CLI interaction (no testing framework required per scope)
**Target Platform**: Cross-platform console/terminal
**Project Type**: Single project with src/ layout
**Performance Goals**: Response within 1 second, handles 100+ tasks
**Constraints**: No third-party packages, no file I/O, no persistence
**Scale/Scope**: Single-user, session-based, 5 features only

## Constitution Check

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Simplicity First | PASS | Minimal module structure, no unnecessary abstractions |
| II. Standard Library Only | PASS | No dependencies in pyproject.toml |
| III. In-Memory Storage Only | PASS | Dictionary-based TaskStore class, no file I/O |
| IV. CLI-Only Interface | PASS | Menu-driven input()/print() interface |
| V. Five Features Only | PASS | Add, View, Update, Delete, Mark Complete only |
| VI. Type Safety & Documentation | PLANNED | All modules/functions will have type hints and docstrings |
| VII. Clean Code Structure | PASS | src/ layout, separated concerns, dataclass model |

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-app/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (architecture plan)
└── tasks.md             # Implementation tasks (to be created)
```

### Source Code (repository root)

```text
src/
└── todo/
    ├── __init__.py          # Package marker with version
    ├── __main__.py          # Entry point: python -m todo
    ├── models.py            # Task dataclass definition
    ├── storage.py           # In-memory TaskStore class
    ├── commands.py          # Business logic for 5 operations
    └── cli.py               # Menu display, input handling, main loop

pyproject.toml               # UV project configuration (update required)
```

**Structure Decision**: Single project with src/ layout. Four modules within the `todo` package separate concerns clearly: models (data), storage (state management), commands (business logic), and cli (user interface). This provides testability and maintainability without over-engineering.

---

## High-Level Architecture

### Architectural Style: Layered Architecture

```
+---------------------------------------------------+
|                    CLI Layer                       |
|                   (cli.py)                         |
|  - Menu display and formatting                     |
|  - User input capture and validation               |
|  - Output formatting and error messages            |
|  - Main application loop                           |
+---------------------------------------------------+
                        |
                        | calls
                        v
+---------------------------------------------------+
|                 Commands Layer                     |
|                 (commands.py)                      |
|  - Business logic for each operation              |
|  - Input validation rules                          |
|  - Operation orchestration                         |
|  - Result/error generation                         |
+---------------------------------------------------+
                        |
                        | uses
                        v
+---------------------------------------------------+
|                 Storage Layer                      |
|                 (storage.py)                       |
|  - Task collection management                      |
|  - CRUD operations on tasks                        |
|  - ID generation and tracking                      |
+---------------------------------------------------+
                        |
                        | stores
                        v
+---------------------------------------------------+
|                  Model Layer                       |
|                 (models.py)                        |
|  - Task dataclass definition                       |
|  - Data structure contracts                        |
+---------------------------------------------------+
```

### Design Rationale

1. **Layered separation**: Each layer has a single responsibility and communicates only with adjacent layers
2. **Dependency direction**: Higher layers depend on lower layers, never the reverse
3. **No circular dependencies**: CLI -> Commands -> Storage -> Models
4. **Testability**: Each layer can be tested independently by mocking dependencies
5. **Simplicity**: Only 4 modules, no abstract base classes, no factories

---

## Component Specifications

### 1. Models Layer (`src/todo/models.py`)

**Responsibility**: Define the Task data structure as the single source of truth for task attributes.

**Public Interface**:
- `Task` (dataclass): Immutable task representation

**Task Dataclass Specification**:
```
@dataclass
class Task:
    id: int              # Unique identifier, auto-generated, never reused
    title: str           # Required, non-empty
    description: str     # Optional, defaults to empty string
    completed: bool      # Defaults to False
```

**Dependencies**: None (foundation layer)

**Collaborators**: Used by storage.py and commands.py

**Design Decisions**:
- Use `@dataclass` decorator per constitution requirement
- Fields are mutable to allow in-place updates (simpler than creating new instances)
- No validation logic in model; validation belongs in commands layer

---

### 2. Storage Layer (`src/todo/storage.py`)

**Responsibility**: Manage the collection of tasks in memory with CRUD operations and ID generation.

**Public Interface**:
- `TaskStore` (class): Singleton-like task collection manager

**TaskStore Class Specification**:

| Method | Purpose | Input | Output |
|--------|---------|-------|--------|
| `__init__()` | Initialize empty store | None | None |
| `add(task: Task) -> None` | Add task to collection | Task | None |
| `get(task_id: int) -> Task or None` | Retrieve task by ID | int | Task or None |
| `get_all() -> list[Task]` | Retrieve all tasks | None | list[Task] |
| `delete(task_id: int) -> bool` | Remove task by ID | int | bool (success) |
| `next_id() -> int` | Generate next unique ID | None | int |

**Internal State**:
- `_tasks: dict[int, Task]` - Dictionary mapping ID to Task
- `_next_id: int` - Counter for ID generation (starts at 1)

**Dependencies**: models.py (Task)

**Collaborators**: Used by commands.py

**Design Decisions**:
- Dictionary storage for O(1) lookup by ID
- ID counter persists across deletions (IDs never reused per spec)
- No thread safety required (single-user per assumptions)
- Store manages ID assignment, not the Task itself

---

### 3. Commands Layer (`src/todo/commands.py`)

**Responsibility**: Implement business logic for each of the five operations with input validation and result generation.

**Public Interface**:

| Function | Purpose | Input | Output |
|----------|---------|-------|--------|
| `add_task(store, title, description)` | Create and store new task | TaskStore, str, str | tuple[bool, str] |
| `view_tasks(store)` | Format all tasks for display | TaskStore | str |
| `update_task(store, task_id, new_title, new_desc)` | Modify existing task | TaskStore, int, str or None, str or None | tuple[bool, str] |
| `delete_task(store, task_id)` | Remove task from store | TaskStore, int | tuple[bool, str] |
| `toggle_complete(store, task_id)` | Toggle task completion status | TaskStore, int | tuple[bool, str] |

**Return Convention**:
- All mutating operations return `tuple[bool, str]`: (success_flag, message)
- `view_tasks` returns formatted string directly (no failure state)

**Validation Rules**:
- Title cannot be empty or whitespace-only
- Task ID must exist for update/delete/toggle operations

**Dependencies**: storage.py (TaskStore), models.py (Task)

**Collaborators**: Used by cli.py

**Design Decisions**:
- Functions, not classes (simplicity per constitution)
- Store passed as parameter (dependency injection for testability)
- Return tuples for consistent success/message handling
- No exceptions for expected errors; use return values

---

### 4. CLI Layer (`src/todo/cli.py`)

**Responsibility**: Handle all user interaction including menu display, input capture, output formatting, and main loop control.

**Public Interface**:

| Function | Purpose |
|----------|---------|
| `main()` | Entry point, runs main loop |
| `display_menu()` | Print menu options |
| `get_menu_choice() -> str` | Get and validate menu selection |
| `handle_add(store)` | Prompt for task details, call add_task |
| `handle_view(store)` | Call view_tasks, display results |
| `handle_update(store)` | Prompt for ID and updates, call update_task |
| `handle_delete(store)` | Prompt for ID, call delete_task |
| `handle_toggle(store)` | Prompt for ID, call toggle_complete |
| `get_task_id() -> int or None` | Get and validate numeric ID input |

**Menu Structure** (per spec):
```
========== TODO APP ==========
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Exit
==============================
Enter your choice:
```

**Dependencies**: commands.py (all command functions), storage.py (TaskStore)

**Collaborators**: Entry point; no other modules depend on it

**Design Decisions**:
- Single `main()` function as entry point
- Helper functions for each menu option (keeps main loop clean)
- Input validation at CLI layer for type conversion (str -> int)
- Graceful handling of Ctrl+C via try/except KeyboardInterrupt
- Graceful handling of EOF via try/except EOFError

---

### 5. Package Initialization (`src/todo/__init__.py`)

**Responsibility**: Mark directory as Python package, expose version.

**Contents**:
- `__version__: str` - Package version string

---

### 6. Entry Point (`src/todo/__main__.py`)

**Responsibility**: Enable `python -m todo` execution.

**Contents**:
- Import and call `main()` from cli module

---

## Data Flow Diagrams

### Flow 1: Add Task

```
User Input               CLI Layer                Commands Layer           Storage Layer
    |                        |                          |                       |
    |  "1" (Add Task)        |                          |                       |
    |----------------------->|                          |                       |
    |                        |  display_menu()          |                       |
    |                        |  get_menu_choice()       |                       |
    |                        |                          |                       |
    |  "Buy groceries"       |                          |                       |
    |----------------------->|  handle_add()            |                       |
    |                        |  input("Enter title: ")  |                       |
    |                        |                          |                       |
    |  "Milk, eggs, bread"   |                          |                       |
    |----------------------->|  input("Enter desc: ")   |                       |
    |                        |------------------------->|                       |
    |                        |  add_task(store,         |                       |
    |                        |    title, desc)          |                       |
    |                        |                          |  validate title       |
    |                        |                          |  (non-empty)          |
    |                        |                          |---------------------->|
    |                        |                          |  store.next_id()      |
    |                        |                          |<----------------------|
    |                        |                          |  id = 1               |
    |                        |                          |---------------------->|
    |                        |                          |  store.add(Task(...)) |
    |                        |<-------------------------|                       |
    |                        |  (True, "Task added      |                       |
    |                        |   successfully. (ID: 1)")|                       |
    |<-----------------------|                          |                       |
    |  print(message)        |                          |                       |
```

### Flow 2: View Tasks

```
User Input               CLI Layer                Commands Layer           Storage Layer
    |                        |                          |                       |
    |  "2" (View Tasks)      |                          |                       |
    |----------------------->|                          |                       |
    |                        |  handle_view()           |                       |
    |                        |------------------------->|                       |
    |                        |  view_tasks(store)       |                       |
    |                        |                          |---------------------->|
    |                        |                          |  store.get_all()      |
    |                        |                          |<----------------------|
    |                        |                          |  [Task(...), ...]     |
    |                        |<-------------------------|                       |
    |                        |  formatted string        |                       |
    |<-----------------------|                          |                       |
    |  print(task list)      |                          |                       |
```

### Flow 3: Update Task

```
User Input               CLI Layer                Commands Layer           Storage Layer
    |                        |                          |                       |
    |  "3" (Update Task)     |                          |                       |
    |----------------------->|                          |                       |
    |                        |  handle_update()         |                       |
    |  "1" (task ID)         |                          |                       |
    |----------------------->|  get_task_id()           |                       |
    |                        |  (validates numeric)     |                       |
    |  "New title"           |                          |                       |
    |----------------------->|  input("new title: ")    |                       |
    |  "" (keep desc)        |                          |                       |
    |----------------------->|  input("new desc: ")     |                       |
    |                        |------------------------->|                       |
    |                        |  update_task(store,      |                       |
    |                        |    1, "New title", None) |                       |
    |                        |                          |---------------------->|
    |                        |                          |  store.get(1)         |
    |                        |                          |<----------------------|
    |                        |                          |  Task(...)            |
    |                        |                          |  (update in place)    |
    |                        |<-------------------------|                       |
    |                        |  (True, "Task updated    |                       |
    |                        |   successfully.")        |                       |
    |<-----------------------|                          |                       |
    |  print(message)        |                          |                       |
```

### Flow 4: Delete Task

```
User Input               CLI Layer                Commands Layer           Storage Layer
    |                        |                          |                       |
    |  "4" (Delete Task)     |                          |                       |
    |----------------------->|                          |                       |
    |                        |  handle_delete()         |                       |
    |  "1" (task ID)         |                          |                       |
    |----------------------->|  get_task_id()           |                       |
    |                        |------------------------->|                       |
    |                        |  delete_task(store, 1)   |                       |
    |                        |                          |---------------------->|
    |                        |                          |  store.delete(1)      |
    |                        |                          |<----------------------|
    |                        |                          |  True                 |
    |                        |<-------------------------|                       |
    |                        |  (True, "Task deleted    |                       |
    |                        |   successfully.")        |                       |
    |<-----------------------|                          |                       |
    |  print(message)        |                          |                       |
```

### Flow 5: Toggle Complete

```
User Input               CLI Layer                Commands Layer           Storage Layer
    |                        |                          |                       |
    |  "5" (Mark Complete)   |                          |                       |
    |----------------------->|                          |                       |
    |                        |  handle_toggle()         |                       |
    |  "1" (task ID)         |                          |                       |
    |----------------------->|  get_task_id()           |                       |
    |                        |------------------------->|                       |
    |                        |  toggle_complete(        |                       |
    |                        |    store, 1)             |                       |
    |                        |                          |---------------------->|
    |                        |                          |  store.get(1)         |
    |                        |                          |<----------------------|
    |                        |                          |  Task(completed=False)|
    |                        |                          |  task.completed=True  |
    |                        |<-------------------------|                       |
    |                        |  (True, "Task marked     |                       |
    |                        |   as complete.")         |                       |
    |<-----------------------|                          |                       |
    |  print(message)        |                          |                       |
```

### Error Flow: Invalid ID

```
User Input               CLI Layer                Commands Layer           Storage Layer
    |                        |                          |                       |
    |  "4" (Delete Task)     |                          |                       |
    |----------------------->|                          |                       |
    |  "99" (invalid ID)     |                          |                       |
    |----------------------->|  get_task_id() -> 99     |                       |
    |                        |------------------------->|                       |
    |                        |  delete_task(store, 99)  |                       |
    |                        |                          |---------------------->|
    |                        |                          |  store.delete(99)     |
    |                        |                          |<----------------------|
    |                        |                          |  False                |
    |                        |<-------------------------|                       |
    |                        |  (False, "Task with ID   |                       |
    |                        |   99 not found.")        |                       |
    |<-----------------------|                          |                       |
    |  print(error message)  |                          |                       |
```

---

## Layer Contracts

### CLI Layer Contract

**Receives**:
- Raw string input from `input()` calls
- Return values from command functions (tuples or strings)

**Produces**:
- Formatted output strings via `print()`
- Validated, typed arguments for command functions

**Errors Raised**:
- None (all errors handled internally with user-friendly messages)

**Must Never Know About**:
- How tasks are stored internally (dictionary vs list)
- Task ID generation strategy
- Internal Task object structure (only uses return messages)

### Commands Layer Contract

**Receives**:
- `TaskStore` instance
- Validated primitive values (str, int)

**Produces**:
- `tuple[bool, str]` for mutating operations
- `str` for view operation

**Errors Raised**:
- None (returns failure tuples instead)

**Must Never Know About**:
- How input was gathered (CLI specifics)
- How output will be displayed
- Menu structure or user prompts

### Storage Layer Contract

**Receives**:
- `Task` objects for storage
- `int` IDs for lookups

**Produces**:
- `Task` objects or `None` for lookups
- `list[Task]` for get_all
- `bool` for delete success
- `int` for next_id

**Errors Raised**:
- None (returns None/False for missing items)

**Must Never Know About**:
- Business rules (title validation, etc.)
- User interface concerns
- Why operations are being performed

### Models Layer Contract

**Receives**: N/A (data definition only)

**Produces**:
- `Task` dataclass instances

**Errors Raised**: N/A

**Must Never Know About**:
- Storage mechanism
- Business rules
- User interface

---

## Implementation Order

Implementation should proceed in dependency order (bottom-up):

### Phase 1: Foundation (No Dependencies)

1. **`src/todo/__init__.py`** - Package marker
   - Create empty file with `__version__` string
   - Acceptance: `import todo` works without error

2. **`src/todo/models.py`** - Task dataclass
   - Define Task with id, title, description, completed
   - Acceptance: Can instantiate Task(1, "Test", "", False)

### Phase 2: Storage (Depends on Models)

3. **`src/todo/storage.py`** - TaskStore class
   - Implement TaskStore with all methods
   - Acceptance: Can add, get, delete tasks; IDs auto-increment

### Phase 3: Business Logic (Depends on Storage, Models)

4. **`src/todo/commands.py`** - Command functions
   - Implement all five command functions
   - Acceptance: Each function returns correct tuple/string

### Phase 4: User Interface (Depends on Commands, Storage)

5. **`src/todo/cli.py`** - CLI handling
   - Implement menu, handlers, main loop
   - Acceptance: Menu displays, all options work correctly

6. **`src/todo/__main__.py`** - Entry point
   - Import and call main()
   - Acceptance: `python -m todo` launches application

### Phase 5: Configuration Update

7. **`pyproject.toml`** - Project configuration update
   - Add package discovery for src/ layout
   - Add project metadata
   - Acceptance: `uv run python -m todo` works

---

## pyproject.toml Configuration

The existing pyproject.toml needs updates for src/ layout:

```toml
[project]
name = "todo-console-app"
version = "0.1.0"
description = "A simple command-line todo application"
readme = "README.md"
requires-python = ">=3.13"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/todo"]
```

**Note**: Using hatchling as build backend is standard for UV projects. No runtime dependencies per constitution.

---

## Error Handling Strategy

### CLI Layer Error Handling

| Error Type | Handling | User Message |
|------------|----------|--------------|
| Invalid menu choice | Re-display menu | "Invalid option. Please try again." |
| Non-numeric ID | Re-prompt | "Please enter a valid number." |
| KeyboardInterrupt | Exit gracefully | "Goodbye!" |
| EOFError | Exit gracefully | "Goodbye!" |

### Commands Layer Error Handling

| Error Type | Handling | Return Value |
|------------|----------|--------------|
| Empty title | Reject add | (False, "Title cannot be empty.") |
| Task not found | Report failure | (False, "Task with ID X not found.") |

### No Exceptions Philosophy

Per constitution's simplicity principle, we use return values instead of exceptions for expected error conditions. Exceptions are reserved for truly unexpected situations (which are handled at CLI layer boundaries).

---

## Output Formatting

### Task Display Format (per spec)

```
ID: 1 | [X] Buy groceries
      Description: Milk, eggs, bread

ID: 2 | [ ] Clean room
      Description:
```

Where:
- `[X]` indicates completed (or use checkmark as per spec)
- `[ ]` indicates incomplete (or use X mark as per spec)
- Empty description still shows "Description:" line for consistency

### Success/Error Messages (per spec)

All messages match spec exactly:
- "Task added successfully. (ID: X)"
- "Task updated successfully."
- "Task deleted successfully."
- "Task marked as complete." / "Task marked as incomplete."
- "Task with ID X not found."
- "No tasks found."
- "Title cannot be empty."
- "Please enter a valid number."
- "Invalid option. Please try again."
- "Goodbye!"

---

## Complexity Tracking

No constitution violations requiring justification. All complexity is minimal and justified:

| Design Element | Justification |
|---------------|---------------|
| 4 modules | Minimum for proper separation of concerns per VII |
| TaskStore class | Encapsulates mutable state per VII prohibition on global state |
| Return tuples | Simple alternative to exceptions, maintains clarity |

---

## Quality Checklist

- [x] Every component has exactly one reason to change
- [x] No circular dependencies exist between modules
- [x] Testing strategy is clear (manual CLI interaction per scope)
- [x] Data flow is traceable from input to output
- [x] Error handling boundaries are explicit
- [x] The plan matches the approved specification exactly
- [x] No unnecessary abstractions or patterns are introduced
- [x] Constitution compliance verified for all 7 principles

---

## Follow-ups and Risks

1. **Unicode compatibility**: Some terminals may not render checkmarks. Consider fallback to `[X]/[ ]` if issues arise.

2. **Input buffer**: No explicit handling for paste operations with multiple lines. Acceptable per simplicity principle.

3. **Memory limits**: No explicit cap on task count. Acceptable per spec (handles 100+ tasks).

---

## Architectural Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Project layout | src/ layout | Constitution requirement |
| Data model | @dataclass | Constitution requirement |
| Storage | Dictionary | O(1) lookup, simple, sufficient |
| Error handling | Return tuples | Simpler than exceptions, explicit |
| Module structure | 4 modules | Minimum for clean separation |
| ID generation | Auto-increment, never reuse | Spec requirement |
| State management | Class encapsulation | Constitution prohibition on global mutable state |
