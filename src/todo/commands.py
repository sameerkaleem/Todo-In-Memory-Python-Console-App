"""Business logic for todo operations.

This module contains the five core command functions for the todo application:
add_task, view_tasks, update_task, delete_task, and toggle_complete.
"""

from todo.models import Task
from todo.storage import TaskStore


def add_task(store: TaskStore, title: str, description: str) -> tuple[bool, str]:
    """Add a new task to the store.

    Args:
        store: The TaskStore instance to add the task to.
        title: The task title (must not be empty or whitespace-only).
        description: Optional task description.

    Returns:
        A tuple of (success: bool, message: str).
    """
    # Validate title is not empty or whitespace-only
    if not title or not title.strip():
        return (False, "Title cannot be empty.")

    # Generate ID and create task
    task_id = store.next_id()
    task = Task(id=task_id, title=title.strip(), description=description)
    store.add(task)

    return (True, f"Task added successfully. (ID: {task_id})")


def view_tasks(store: TaskStore) -> str:
    """Format all tasks for display.

    Args:
        store: The TaskStore instance to retrieve tasks from.

    Returns:
        Formatted string of all tasks, or "No tasks found." if empty.
    """
    tasks = store.get_all()

    if not tasks:
        return "No tasks found."

    lines = []
    for task in tasks:
        # Use ASCII fallback for Windows console compatibility
        status = "X" if task.completed else " "
        lines.append(f"ID: {task.id} | [{status}] {task.title}")
        lines.append(f"      Description: {task.description}")
        lines.append("")  # Empty line between tasks

    return "\n".join(lines).rstrip()


def update_task(
    store: TaskStore,
    task_id: int,
    new_title: str | None,
    new_desc: str | None,
) -> tuple[bool, str]:
    """Update an existing task's title and/or description.

    Args:
        store: The TaskStore instance containing the task.
        task_id: The ID of the task to update.
        new_title: New title (None or empty to keep existing).
        new_desc: New description (None to keep existing, empty string to clear).

    Returns:
        A tuple of (success: bool, message: str).
    """
    task = store.get(task_id)

    if task is None:
        return (False, f"Task with ID {task_id} not found.")

    # Update title if provided and non-empty
    if new_title and new_title.strip():
        task.title = new_title.strip()

    # Update description if provided (allow empty string to clear)
    if new_desc is not None:
        task.description = new_desc

    return (True, "Task updated successfully.")


def delete_task(store: TaskStore, task_id: int) -> tuple[bool, str]:
    """Delete a task from the store.

    Args:
        store: The TaskStore instance containing the task.
        task_id: The ID of the task to delete.

    Returns:
        A tuple of (success: bool, message: str).
    """
    if store.delete(task_id):
        return (True, "Task deleted successfully.")

    return (False, f"Task with ID {task_id} not found.")


def toggle_complete(store: TaskStore, task_id: int) -> tuple[bool, str]:
    """Toggle a task's completion status.

    Args:
        store: The TaskStore instance containing the task.
        task_id: The ID of the task to toggle.

    Returns:
        A tuple of (success: bool, message: str).
    """
    task = store.get(task_id)

    if task is None:
        return (False, f"Task with ID {task_id} not found.")

    # Toggle the completed status
    task.completed = not task.completed

    if task.completed:
        return (True, "Task marked as complete.")
    else:
        return (True, "Task marked as incomplete.")
