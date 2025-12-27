"""Command-line interface for the todo application.

This module handles all user interaction including menu display, input capture,
output formatting, and the main application loop.
"""

from todo.commands import (
    add_task,
    delete_task,
    toggle_complete,
    update_task,
    view_tasks,
)
from todo.storage import TaskStore


def display_menu() -> None:
    """Display the main menu options."""
    print("========== TODO APP ==========")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete")
    print("6. Exit")
    print("==============================")


def get_task_id() -> int | None:
    """Prompt for and validate a task ID.

    Returns:
        The validated task ID as int, or None if input was invalid.
    """
    try:
        user_input = input("Enter task ID: ")
        return int(user_input)
    except ValueError:
        print("Please enter a valid number.")
        return None


def handle_add(store: TaskStore) -> None:
    """Handle the Add Task operation.

    Args:
        store: The TaskStore instance to add the task to.
    """
    title = input("Enter title: ")
    description = input("Enter description (optional): ")

    success, message = add_task(store, title, description)
    print(message)


def handle_view(store: TaskStore) -> None:
    """Handle the View Tasks operation.

    Args:
        store: The TaskStore instance to retrieve tasks from.
    """
    result = view_tasks(store)
    print(result)


def handle_update(store: TaskStore) -> None:
    """Handle the Update Task operation.

    Args:
        store: The TaskStore instance containing the task.
    """
    task_id = get_task_id()
    if task_id is None:
        return

    new_title = input("Enter new title (or press Enter to keep): ")
    new_desc = input("Enter new description (or press Enter to keep): ")

    # Convert empty strings to None for "keep existing" behavior
    title_arg = new_title if new_title else None
    desc_arg = new_desc if new_desc else None

    success, message = update_task(store, task_id, title_arg, desc_arg)
    print(message)


def handle_delete(store: TaskStore) -> None:
    """Handle the Delete Task operation.

    Args:
        store: The TaskStore instance containing the task.
    """
    task_id = get_task_id()
    if task_id is None:
        return

    success, message = delete_task(store, task_id)
    print(message)


def handle_toggle(store: TaskStore) -> None:
    """Handle the Mark Complete operation.

    Args:
        store: The TaskStore instance containing the task.
    """
    task_id = get_task_id()
    if task_id is None:
        return

    success, message = toggle_complete(store, task_id)
    print(message)


def main() -> None:
    """Main application entry point.

    Creates the TaskStore and runs the interactive menu loop
    until the user chooses to exit.
    """
    store = TaskStore()

    try:
        while True:
            display_menu()
            choice = input("Enter your choice: ")

            if choice == "1":
                handle_add(store)
            elif choice == "2":
                handle_view(store)
            elif choice == "3":
                handle_update(store)
            elif choice == "4":
                handle_delete(store)
            elif choice == "5":
                handle_toggle(store)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

            print()  # Blank line before next menu display

    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
