"""Task class definition."""

import uuid


class Task:
    """A task."""

    def __init__(self, title: str, *, task_id: str | None = None, done: bool = False) -> None:
        self.id = task_id or str(uuid.uuid4()).replace("-", "")
        self.title = title or "Untitled"
        self.done = done
