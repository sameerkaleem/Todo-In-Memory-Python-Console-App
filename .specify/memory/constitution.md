<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 → 1.0.0 (initial constitution)
Modified principles: N/A (initial creation)
Added sections:
  - Core Principles (7 principles)
  - Technology Stack
  - Development Workflow
  - Governance
Removed sections: N/A
Templates requiring updates:
  ✅ .specify/templates/plan-template.md (no changes needed - generic template)
  ✅ .specify/templates/spec-template.md (no changes needed - generic template)
  ✅ .specify/templates/tasks-template.md (no changes needed - generic template)
Follow-up TODOs: None
-->

# Todo Console App Constitution

## Core Principles

### I. Simplicity First

All code MUST prioritize simplicity and readability over cleverness or premature optimization.

- Code MUST be understandable by any Python developer without extensive comments
- Functions MUST do one thing and do it well
- Avoid abstractions until they prove necessary (YAGNI principle)
- Prefer explicit code over implicit magic

**Rationale**: A todo app is a simple domain; complexity is a bug, not a feature.

### II. Standard Library Only

The application MUST use only Python standard library modules. No third-party packages are permitted.

- No external dependencies in `pyproject.toml` (dev dependencies for tooling are acceptable)
- All functionality MUST be achievable with built-in Python modules
- This includes: no ORM, no CLI framework, no validation library

**Rationale**: Demonstrates Python fundamentals, ensures portability, and eliminates dependency management overhead.

### III. In-Memory Storage Only

All task data MUST be stored exclusively in memory. No persistence to disk, database, or external storage is permitted.

- Data exists only for the duration of the application session
- No file I/O for task storage (JSON, CSV, SQLite, etc.)
- No database connections
- Application starts with empty task list on each run

**Rationale**: Keeps the application focused on core Python data structures and logic without I/O complexity.

### IV. CLI-Only Interface

The application MUST provide a console-based interactive interface only. No GUI, web, or API interfaces are permitted.

- Interactive REPL-style loop until user exits
- Clear menu or command-based interface
- Text input via `input()`, output via `print()`
- Graceful handling of invalid inputs (re-prompt, don't crash)
- Clean exit command (e.g., "quit", "exit", or menu option)

**Rationale**: Focuses on core Python I/O and control flow without UI framework complexity.

### V. Five Features Only

The application MUST implement exactly these five features—no more, no less:

1. **Add Task**: Create new todo items (title required, description optional)
2. **Delete Task**: Remove tasks by ID
3. **Update Task**: Modify title and/or description of existing tasks
4. **View Task List**: Display all tasks with ID, title, completion status, description
5. **Mark as Complete**: Toggle task completion status

- No additional features (due dates, priorities, categories, sorting, search, persistence, export)
- Each feature MUST be fully functional and handle edge cases gracefully

**Rationale**: Scope control prevents feature creep and keeps the project focused on fundamentals.

### VI. Type Safety & Documentation

All code MUST include comprehensive type hints and documentation.

- Full type hints on all functions, methods, and class attributes
- Module-level docstrings explaining purpose
- Class docstrings explaining responsibility
- Function/method docstrings explaining behavior, parameters, and return values
- Follow Google or NumPy docstring style consistently

**Rationale**: Type hints enable static analysis and IDE support; docstrings ensure maintainability.

### VII. Clean Code Structure

The application MUST follow clean code principles with proper separation of concerns.

- Use `src/` layout for project structure
- Separate modules for: models, storage, commands/logic, CLI handling
- Use `dataclass` for the Task model with fields: `id` (int), `title` (str), `description` (str), `completed` (bool)
- Entry point via `python -m todo` (requires `__main__.py`)
- Follow PEP 8 naming conventions
- Avoid global mutable state where possible

**Rationale**: Modular design enables testing, maintenance, and demonstrates proper Python project structure.

## Technology Stack

The following technology constraints are non-negotiable:

| Component | Requirement |
|-----------|-------------|
| Language | Python 3.13+ |
| Package Manager | UV |
| Dependencies | Standard library only |
| Project Layout | src/ layout |
| Entry Point | `python -m todo` |
| Task Model | `dataclasses.dataclass` |

## Development Workflow

### Code Quality Gates

All code MUST pass these gates before completion:

1. **Syntax**: Valid Python 3.13+ syntax
2. **Type Hints**: All public interfaces fully typed
3. **Docstrings**: All modules, classes, and functions documented
4. **PEP 8**: Follows Python style guidelines
5. **Error Handling**: Invalid input handled gracefully without crashes
6. **Functionality**: All five features working correctly

### Prohibited Patterns

The following are explicitly forbidden:

- Third-party package imports (runtime)
- File/database persistence
- GUI or web frameworks
- Global mutable state for task storage (use class encapsulation)
- Features beyond the five specified
- Complex design patterns (factories, decorators, etc.) unless clearly justified

## Governance

This constitution is the authoritative source for project constraints and principles.

### Authority

- Constitution supersedes all other documentation
- Any conflict with spec, plan, or tasks MUST be resolved in favor of the constitution
- Violations MUST be justified in writing with clear rationale

### Amendment Process

1. Propose change with rationale
2. Document impact on existing artifacts
3. Update version according to semver rules
4. Update dependent templates if affected

### Compliance

- All specs MUST reference constitution for constraint validation
- All plans MUST include Constitution Check section
- All implementations MUST adhere to technology stack and prohibited patterns
- Code review MUST verify principle compliance

**Version**: 1.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27
