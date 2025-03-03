"""Task form modal screen."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label

from tasks.core import TasksList


class TaskFormModal(ModalScreen[str]):
    """Task title input screen."""

    DEFAULT_CSS = """
    TaskFormModal {
        align: center middle;
    }

    TaskFormModal > Container {
        width: auto;
        height: auto;
    }

    TaskFormModal > Container > Label {
        width: 100%;
        content-align-horizontal: center;
        margin-top: 1;
    }

    TaskFormModal > Container > Horizontal {
        width: auto;
        height: auto;
    }

    TaskFormModal > Container > Horizontal > Button {
        margin: 2 4;
    }
    """

    def __init__(self, task_id: str | None = None) -> None:
        super().__init__()
        self.task_id = task_id
        self.tasks: TasksList = self.app.tasks  # type: ignore
        self.input = Input(value=None, placeholder="Enter a task title...")

    def compose(self) -> ComposeResult:  # noqa: D102
        task = self.tasks.get(self.task_id) if self.task_id else None
        if task:
            self.input.value = task.title
        with Container():
            yield Label("Input a new name for task:")
            yield self.input
            with Horizontal():
                yield Button("Cancel", variant="error", id="cancel")
                yield Button("Submit", variant="success", id="submit")

    @on(Input.Submitted)
    @on(Button.Pressed, "#submit")
    def submit_input(self) -> None:  # noqa: D102
        self.dismiss(self.input.value)

    @on(Button.Pressed, "#cancel")
    def cancel_input(self) -> None:  # noqa: D102
        self.dismiss(None)
