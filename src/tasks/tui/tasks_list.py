"""Tasks list."""

from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Button

from tasks.core import Task
from tasks.core import TasksList as TasksListRepo

from .task_form_modal import TaskFormModal
from .tasks_list_item import TasksListItem


class TasksList(Widget):
    """A widget that displays a list of tasks."""

    DEFAULT_CSS = """
    TasksList > VerticalScroll > Button {
        align: center top;
    }
    #add_task {
        align: center top;
    }
    """

    tasks: reactive[dict[str, Task]] = reactive(dict, recompose=True)

    def compose(self) -> ComposeResult:
        """Compose widget."""
        with VerticalScroll():
            yield from [TasksListItem(t.id, t.title, t.done) for t in self.tasks.values()]
            yield Button("+", variant="success", id="add_task")

    @on(Button.Pressed, "#add_task")
    def add_task(self) -> None:
        """Add a new task to the list.

        This will open a TaskFormModal.
        """

        def handle_task_input(result: str | None) -> None:
            if result is None:
                self.app.notify("Canceled", severity="warning")
                return

            if result == "":
                self.app.notify("A task cannot have an empty title!", severity="error")
                return

            task_id = self.app.tasks.add(result)  # type: ignore
            self.tasks[task_id] = self.app.tasks.get(task_id)  # type: ignore
            self.mutate_reactive(TasksList.tasks)
            self.app.notify("Created a new task!")
            # self.refresh()

        self.app.push_screen(TaskFormModal(), handle_task_input)

    def on_tasks_list_item_deleted(self, event: TasksListItem.Deleted) -> None:
        """Remove a task when TasksListItem emited a Delete message."""
        tasks: TasksListRepo = self.app.tasks  # type: ignore
        task = tasks.get(event.task_id)
        self.app.notify(f"Task deleted: '{task.title}'")
        del self.tasks[event.task_id]
        tasks.delete(event.task_id)
        self.mutate_reactive(TasksList.tasks)

    def on_tasks_list_item_state_changed(self, event: TasksListItem.StateChanged) -> None:
        """Change the state of a task when TasksListItem emited a StateChanged message."""
        tasks: TasksListRepo = self.app.tasks  # type: ignore
        task = tasks.get(event.task_id)
        task.done = not task.done
        tasks.update(task)
        self.tasks[event.task_id] = task
        self.mutate_reactive(TasksList.tasks)

    def on_tasks_list_item_title_changed(self, event: TasksListItem.TitleChanged) -> None:
        """Change the title of a task when TasksListItem emited a TitleChanged message."""
        tasks: TasksListRepo = self.app.tasks  # type: ignore
        task = self.tasks[event.task_id]
        task.title = event.new_title
        tasks.update(task)
        self.mutate_reactive(TasksList.tasks)
