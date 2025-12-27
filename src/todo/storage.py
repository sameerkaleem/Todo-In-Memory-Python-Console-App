"""In-memory task storage.

This module provides the TaskStore class for managing tasks in memory.
Tasks are stored in a dictionary for O(1) lookup by ID.
"""

from todo.models import Task


class TaskStore:
    """In-memory storage for Task objects.

    Manages a collection of tasks with CRUD operations and ID generation.
    IDs are auto-incremented and never reused after deletion.

    Attributes:
        _tasks: Internal dictionary mapping task IDs to Task objects.
        _next_id: Counter for generating the next unique task ID.
    """

    def __init__(self) -> None:
        """Initialize an empty task store."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task: Task) -> None:
        """Add a task to the store.

        Args:
            task: The Task object to store.
        """
        self._tasks[task.id] = task

    def get(self, task_id: int) -> Task | None:
        """Retrieve a task by its ID.

        Args:
            task_id: The unique identifier of the task.

        Returns:
            The Task object if found, None otherwise.
        """
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        """Retrieve all tasks.

        Returns:
            A list of all Task objects in the store.
        """
        return list(self._tasks.values())

    def delete(self, task_id: int) -> bool:
        """Remove a task by its ID.

        Args:
            task_id: The unique identifier of the task to delete.

        Returns:
            True if the task was found and deleted, False otherwise.
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def next_id(self) -> int:
        """Generate the next unique task ID.

        Returns:
            The next available ID (auto-incremented, never reused).
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id
