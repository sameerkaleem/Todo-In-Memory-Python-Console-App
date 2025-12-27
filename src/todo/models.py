"""Task model definition.

This module defines the Task dataclass, which represents a single todo item
with an ID, title, optional description, and completion status.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """A todo task with ID, title, description, and completion status.

    Attributes:
        id: Unique identifier for the task (auto-generated, never reused).
        title: Required task title (non-empty string).
        description: Optional additional details (defaults to empty string).
        completed: Whether the task is done (defaults to False).
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
