"""Main TUI application class."""

from pathlib import Path

from textual import on
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Grid, HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Input,
    Label,
    Static,
)

from tasks.core import Task, Tasks


class TaskTitleInputScreen(ModalScreen[str]):
    """Task title input screen."""

    def __init__(self, task_id: str | None = None) -> None:
        super().__init__()
        self.task_id = task_id
        self.tasks: Tasks = self.app.tasks  # type: ignore
        self.input = Input(value=None, placeholder="Type a task title...")

    def compose(self) -> ComposeResult:  # noqa: D102
        task = self.tasks.get(self.task_id) if self.task_id else None
        if task:
            self.input.value = task.title
        yield Grid(
            Label("Input a new name for task:"),
            self.input,
            Button("Cancel", variant="error", id="cancel"),
            Button("Submit", variant="success", id="submit"),
        )

    @on(Input.Submitted)
    @on(Button.Pressed, "#submit")
    def submit_input(self) -> None:  # noqa: D102
        self.app.notify(f'Task title changed: "{self.input.value}"')
        self.dismiss(self.input.value)

    @on(Button.Pressed, "#cancel")
    def cancel_input(self) -> None:  # noqa: D102
        self.app.notify("Task editing canceled", severity="warning")
        self.dismiss(None)


class TasksListItem(Static):
    """A tasks list item widget."""

    DEFAULT_CSS = """
    HorizontalGroup {
        content-align: center middle;
    }
    Button {
        align-horizontal: right;
    }
    """

    def __init__(self, task_id: str) -> None:
        super().__init__()
        self.task_id = task_id
        self.tasks: Tasks = self.app.tasks  # type: ignore

    def compose(self) -> ComposeResult:  # noqa: D102
        # tasks: Tasks = self.app.tasks  # type: ignore
        task: Task = self.tasks.get(self.task_id)
        yield HorizontalGroup(
            Checkbox(value=task.done, id="check"),
            Label(f"[b]{task.title}[/b]"),
            Button("Edit :pen:", id="edit"),
            Button("Delete :wastebasket:", variant="error", id="delete"),
        )

    @on(Button.Pressed, "#delete")
    def delete_task(self) -> None:  # noqa: D102
        self.tasks.delete(self.task_id)
        self.remove()

    @on(Button.Pressed, "#edit")
    def edit_task_title(self) -> None:  # noqa: D102
        def handle_title_change(result: str | None) -> None:
            if result is None or result == "":
                self.app.notify("A task cannot have an empty title!", severity="error")
                return
            task = self.tasks.get(self.task_id)
            task.title = result
            self.tasks.update(task)
            self.app.notify("Task title updated!")
            self.refresh()

        self.app.push_screen(
            TaskTitleInputScreen(self.task_id),
            handle_title_change,
        )

    @on(Checkbox.Changed, "#check")
    def change_task_state(self) -> None:  # noqa: D102
        task = self.tasks.get(self.task_id)
        task.done = not task.done
        self.tasks.update(task)


class TasksApp(App):
    """A Textual app to manage tasks."""

    # CSS_PATH = Path(Path(__file__).parent, "tasksapp.tcss").resolve().__str__()
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("a", "add_task", "Add a new task"),
    ]

    def __init__(self, tasks: Tasks) -> None:
        super().__init__()
        self.tasks = tasks
        self.tasks_list = []

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        self.tasks_list = [TasksListItem(task.id) for task in self.tasks]
        yield VerticalScroll(*self.tasks_list)
        yield Footer()
        # yield Hello()

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"

    def action_add_task(self) -> None:
        """Add a new task."""
        def handle_task_input(result: str | None) -> None:
            if result is None or result == "":
                self.app.notify("A task cannot have an empty title!", severity="error")
                return
            task_id = self.tasks.add(result)
            self.tasks_list.append(TasksListItem(task_id))
            self.app.notify("Created a new task!")
            self.refresh()

        self.push_screen(TaskTitleInputScreen(), handle_task_input)
