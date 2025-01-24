"""Tasks list item."""

from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Button, Checkbox, Label, Static

from .task_form_modal import TaskFormModal


class TasksListItem(Static):
    """A tasks list item widget."""

    DEFAULT_CSS = """
    .spacer {
        width: 1fr;
    }
    """

    class Deleted(Message):
        """Task has been deleted."""

        def __init__(self, task_id: str) -> None:
            self.task_id = task_id
            super().__init__()

    class StateChanged(Message):
        """Task state has been changed."""

        def __init__(self, task_id: str) -> None:
            self.task_id = task_id
            super().__init__()

    class TitleChanged(Message):
        """Task title has been changed."""

        def __init__(self, task_id: str, new_title: str) -> None:
            self.task_id = task_id
            self.new_title = new_title
            super().__init__()

    task_id: str
    done: reactive[bool] = reactive(False)
    title: reactive[str] = reactive("")

    def __init__(self, task_id: str, title: str, done: bool) -> None:
        super().__init__()
        self.task_id = task_id
        self.done = done
        self.title = title

    def compose(self) -> ComposeResult:  # noqa: D102
        with HorizontalGroup():
            yield Checkbox(value=self.done, id="checkbox")
            yield Label(f"[b]{self.title}[/b]", id="title")
            yield Static("", classes="spacer")
            yield Button(":pen:  Edit", id="edit")
            yield Button(":wastebasket:  Delete", variant="error", id="delete")

    @on(Button.Pressed, "#delete")
    def delete_task(self) -> None:
        """Delete task."""
        self.post_message(self.Deleted(self.task_id))

    @on(Button.Pressed, "#edit")
    def edit_task_title(self) -> None:  # noqa: D102
        def handle_title_change(result: str | None) -> None:
            if result is None:
                self.app.notify("Canceled", severity="warning")
                return

            if result == "":
                self.app.notify("A task cannot have an empty title!", severity="error")
                return

            self.post_message(self.TitleChanged(self.task_id, result))

        self.app.push_screen(
            TaskFormModal(self.task_id),
            handle_title_change,
        )

    @on(Checkbox.Changed, "#checkbox")
    def change_task_state(self) -> None:  # noqa: D102
        """Change task state."""
        self.post_message(self.StateChanged(self.task_id))
