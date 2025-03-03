"""Tasks lists manager."""

# TODO: WIP TasksLists class, make it complete.

from pathlib import Path

from pydantic import BaseModel

from .tasks_list import TasksList


class TasksLists(BaseModel):
    """Tasks lists manager."""

    active_list: Path | None
    task_lists: list[Path]

    def __init__(self) -> None:
        pass

    @property
    def active(self) -> TasksList | None:
        if self.active_list:
            return TasksList(self.active_list)
        return None

    def add(self, path: Path, set_active: bool = False) -> None:
        """Add a new tasks list."""
        self.task_lists.append(path)
        if set_active:
            self.active_list = path

    def delete()