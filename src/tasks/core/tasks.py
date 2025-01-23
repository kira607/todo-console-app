"""Tasks list handler."""

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any, override

from .task import Task


class TaskEncoder(json.JSONEncoder):
    """Json encoder for a ``Task`` class."""

    @override
    def default(self, o: Any) -> dict[str, str | bool]:
        if isinstance(o, Task):
            return {"id": o.id, "title": o.title, "done": o.done}
        return super().default(o)


class Tasks:
    """Handler of a tasks list stored in a json file."""

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.tasks: dict[str, Task] = {}
        self._load()

    def at(self, index: int) -> Task | None:
        """Get a task by index.

        :param int index: Task index.
        :return Task | None: Task instance if exists, None otherwise.
        """
        if index >= len(self.tasks) or index < 0:
            return None
        return list(self.tasks.values())[index]

    def get(self, task_id: str) -> Task:
        """Get a task by task."""
        return self.tasks[task_id]

    def add(self, title: str) -> str:
        """Add a new task.

        :param Task task: A task to add.
        :return str: Id of a new task.
        """
        task = Task(title)
        task_id = task.id
        self.tasks[task_id] = task
        self._save()
        return task_id

    def delete(self, task_id: str) -> None:
        """Delete a task by id.

        If a task with a given id does not exist
        nothing happens.

        :param str task_id: Id of a task for deletion.
        """
        try:
            del self.tasks[task_id]
        except KeyError:
            return
        self._save()

    def update(self, task: Task) -> None:
        """Update a task."""
        self.tasks[task.id] = task
        self._save()

    def __iter__(self) -> Iterator[Task]:  # noqa: D105
        return iter(self.tasks.values())

    def __len__(self) -> int:  # noqa: D105
        return len(self.tasks)

    def _load(self) -> None:
        """Load tasks list from a file."""
        with self.path.open("r") as f:
            raw_text = f.read()

        if raw_text == "":
            self.tasks = {}
            return

        data: dict[str, dict] = json.loads(raw_text)
        self.tasks = {k: Task(v["title"], task_id=v["id"], done=v["done"]) for k, v in data.items()}

    def _save(self) -> None:
        """Save current tasks list to a file."""
        with self.path.open("w") as f:
            json.dump(self.tasks, f, indent=4, cls=TaskEncoder)
