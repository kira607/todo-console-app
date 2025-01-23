"""Main TUI application class."""

from pathlib import Path

from textual.app import App, ComposeResult, RenderResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Footer, Header, Label

from tasks.core import Task, Tasks


class TasksListItem(HorizontalGroup):
    """A tasks list item widget."""

    task = reactive(Task(""))

    def compose(self) -> ComposeResult:
        yield Checkbox()
        yield Label()
        yield Button("Edit")
        yield Button("Delete :wastebasket:", variant="error")


class Hello(Widget):
    """Hello widget."""

    def render(self) -> RenderResult:  # noqa: D102
        return "Hello, [b]World![/b]"


class TasksApp(App):
    """A Textual app to manage stopwatches."""

    CSS_PATH = Path(Path(__file__).parent, "tasksapp.tcss").resolve().__str__()
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def __init__(self, tasks: Tasks, *args, **kwargs) -> None:  # type: ignore
        self.tasks = tasks
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        task_items = [TasksListItem() for task in self.tasks]
        yield VerticalScroll(*task_items)
        # yield Hello()

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"
