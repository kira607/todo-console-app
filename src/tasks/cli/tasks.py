"""CLI Module to manage tasks in currently selected list."""

import logging

import typer
from rich.console import Console

from tasks.core import TasksList
from tasks.tui import TasksApp

console = Console()
logger = logging.getLogger()
tasks_cli = typer.Typer(
    help="Simple todo CLI app.",
    invoke_without_command=True,
    no_args_is_help=True,
)


@tasks_cli.command("help")
def cli_help(ctx: typer.Context) -> None:
    """Show this help message."""
    print(ctx.parent.get_help())  # type: ignore


@tasks_cli.command("tui")
def cli_tui(ctx: typer.Context) -> None:
    """Open a TUI application."""
    tasks: TasksList = ctx.obj.tasks
    TasksApp(tasks).run()


@tasks_cli.command("ls")
def list_tasks(ctx: typer.Context) -> None:
    """List all tasks."""
    tasks: TasksList = ctx.obj.tasks
    console.print(f"[bold]{tasks.title}[/bold]")
    for task in tasks:
        done = "X" if task.done else " "
        print(f"[{done}] {task.title}")
    print("-------------")
    print(f"{len(tasks)} items")


@tasks_cli.command("add")
def add_task(
    ctx: typer.Context,
    title: str = typer.Option(
        "",
        "--title",
        "-t",
        help="Immediatly add a title to a task",
    ),
) -> None:
    """Add a new task to a task list."""
    tasks: TasksList = ctx.obj.tasks
    if not title:
        title = input("Add task title: ")
    tasks.add(title)


@tasks_cli.command("pick")
def pick_task(ctx: typer.Context) -> None:
    """Pick a task for editing."""
    tasks: TasksList = ctx.obj.tasks

    if len(tasks) == 0:
        print("No tasks")
        return

    for i, task in enumerate(tasks):
        done = "X" if task.done else " "
        print(f"[{i}]: [{done}] {task.title}")

    try:
        index = input("Pick a task number (q to quit): ")
        if index == "q":
            return
        index = int(index)  # type: ignore
        task = tasks.at(index)  # type: ignore
        if task is None:
            raise ValueError(index)
    except ValueError:
        print("Invalid task number")
        return

    action = input("[d]elete / [e]dit title / [c]hange done: ")

    if action == "d":
        message = f"Deleted: {task.title}"
        tasks.delete(task.id)
        print(message)
        return

    if action == "e":
        new_title = input("New task title: ")
        message = f"Changed title: {task.title} -> {new_title}"
        task.title = new_title
        tasks.update(task)
        print(message)
        return

    if action == "c":
        task.done = not task.done
        not_ = "" if task.done else "not "
        message = f"Task {not_}done: {task.title}"
        tasks.update(task)
        print(message)
        return

    print("Invalid action")
