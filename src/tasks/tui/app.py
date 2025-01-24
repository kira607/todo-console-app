"""Main TUI application class."""

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from tasks.core import Task as Task
from tasks.core import Tasks

from .tasks_list import TasksList


class TasksApp(App):
    """A Textual app to manage tasks."""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("a", "add_task", "Add a new task"),
        ("q", "quit_app", "Quit the application"),
    ]

    tasks: Tasks

    def __init__(self, tasks: Tasks) -> None:
        super().__init__()
        self.tasks = tasks

    def compose(self) -> ComposeResult:
        """Compose widget."""
        tasks_list = TasksList()
        tasks_list.tasks = {task.id: task for task in self.tasks}
        yield Header()
        yield tasks_list
        yield Footer()

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"

    def action_add_task(self) -> None:
        """Add a new task."""
        self.query_one("TasksList").add_task()  # type: ignore

    def action_quit_app(self) -> None:
        """Quit the application."""
        self.exit(message="Exited!")
