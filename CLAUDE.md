# Claude Code Rules

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Guidance for Claude Code in Spec-Kit Plus Workflow

This file serves as the primary instruction set for Claude (or any Claude-based coding agent) when working on this project using the Spec-Kit Plus spec-driven development process.

## Project Overview
You are building a **command-line Todo In-Memory Python Console App** that stores tasks entirely in memory (no persistence to disk).

Core features (all must be implemented):
- Add Task
- Delete Task
- Update Task
- View Task List
- Mark as Complete (toggle completion status)

## Mandatory Constraints (Constitution)

### Development Methodology
This project follows Spec-Driven Development using:
- Spec-Kit Plus
- Claude Code

- Claude must work in the following strict order:
sp.constitution
sp.specify
sp.plan
sp.tasks
sp.implementation

⚠️ Do not skip or merge steps.
Each phase must be completed and validated before moving to the next.

## Always adhere strictly to these rules:
- Use **only the Python standard library** – no third-party packages.
- Project managed with **UV** (virtual environment and dependency management).
- Target **Python 3.13+**.
- Follow **clean code principles**: readable, modular, well-named, simple.
- Storage:
  In-memory only
  No files, databases, or persistence of any kind
- Interface:
  Console / terminal interaction only
  No GUI or web components
- Scope Control:
  Implement only the five required features
  Do not add optional or “nice-to-have” features
  No external frameworks

## Clean Code Requirements, All generated code must:
- Follow clean code principles
- Use clear and descriptive naming
- Be modular and readable
- Separate concerns (CLI, logic, models)
- Avoid unnecessary complexity
- Avoid global mutable state when possible

- Use **src layout** project structure (preferred):
todo_console_app/
├── src/
│   ├── main.py          # Application entry point
│   ├── models.py        # Task data model
│   ├── storage.py       # In-memory task storage
│   ├── commands.py      # Task operations (add, delete, update, etc.)
│   └── cli.py           # CLI input/output handling
├── pyproject.toml
├── README.md
└── CLAUDE.md

## Feature Behavior Rules:
## Task Model
Each task must include:
  Unique identifier
  Title
  Optional description
  Completion status (completed: bool)

## Add Task:
  Prompt user for task details
  Store task in memory
  Confirm success

## Delete Task:
  Identify task by ID
  Remove it from memory
  Handle invalid IDs gracefully

## Update Task:
  Allow modification of title and/or description
  Validate task existence

## View Tasks:
  Display all tasks
  Show completion status clearly

## Mark as Complete:
  Toggle task completion state
  Confirm updated status

## Error Handling Expectations:
### Claude must:
  Validate all user input
  Provide clear error messages
  Never crash on invalid input
  Keep the CLI responsive and understandable

- Entry point: runnable via `python -m todo`.
- Use **dataclasses** for the `Task` model.
- Task fields (minimum):
- `id`: int (auto-incrementing)
- `title`: str (required)
- `description`: str (optional, can be empty)
- `completed`: bool (default False)
- Full **type hints** on all functions, methods, and variables.
- Comprehensive **docstrings** (module, class, function level).
- Follow **PEP 8** and modern Python best practices.
- Prioritize **simplicity and readability** over clever or over-engineered solutions.
- Do **not** add unsolicited features (e.g., due dates, priorities, categories, sorting, file persistence).

## Workflow Instructions for Claude
You will be guided through Spec-Kit Plus phases in this order:

1. **/constitution** → Read and internalize `constitution.md`.
2. **/specify** → Produce `spec.md` with precise user stories and acceptance criteria (no code).
3. **/plan** → Produce `plan.md` with architecture, component breakdown, and project structure.
4. **/tasks** → Produce `tasks.md` with atomic, sequential, verifiable tasks.
5. **/implement** → Implement task-by-task, exactly in order.

### During Implementation Phase
- Implement **one task at a time**.
- Create or modify **only the files specified** in the current task.
- After each task, verify manually (run the app where possible) before proceeding.
- Output changes **file-by-file** with clear explanations.
- Never skip or combine tasks unless explicitly instructed.
- If something is ambiguous, ask for clarification rather than assuming extra features.

### CLI Design Expectations
- Interactive REPL-style loop.
- Clear menu or command-based interface (e.g., display options, accept numbered input or typed commands).
- Graceful handling of invalid inputs (re-prompt instead of crash).
- Command to exit the app cleanly (e.g., "quit", "exit", or menu option).

### Example Task Model (for reference only – implement per spec/plan)
```python
from dataclasses import dataclass

@dataclass
class Task:
  id: int
  title: str
  description: str = ""
  completed: bool = False
```

### Final Success Criteria
When complete, running:
python -m todo

## Output Expectations:

### During sp.implementation, Claude must:
  Produce complete, runnable code
  Include a clear entry point
  Provide UV-based run instructions
  Keep comments concise and helpful

### must launch a fully functional interactive console application that:
  Allows adding tasks (title required, description optional)
  Lists all tasks with ID, title, completion status, and description
  Supports updating title/description of a task by ID
  Supports deleting a task by ID
  Supports toggling completion status by ID
  Handles all edge cases gracefully
  Exits cleanly on user command

All code must be clean, fully typed, well-documented, and 100% compliant with the constitution, specification, plan, and tasks.
Adhere rigorously to this guidance at every step. Do not deviate.