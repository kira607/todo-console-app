"""Simple console tasks app."""

import logging
import sys
import traceback
from pathlib import Path

import typer

from tasks import __version__
from tasks.core import Tasks
from tasks.tui import TasksApp

logging.basicConfig(format="%(levelname)8s: %(message)s")
logger = logging.getLogger()


cli_app = typer.Typer(
    help="Simple todo CLI app.",
    invoke_without_command=True,
    no_args_is_help=True,
)


@cli_app.callback()
def root(
    ctx: typer.Context,
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        min=0,
        max=3,
        help="Increase verbosity",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Show version",
    ),
) -> None:
    """Simple todo CLI app."""  # noqa: D401
    # Set logging level
    # -------------------
    # 50: Crit
    # 40: Err
    # 30: Warn
    # 20: Info
    # 10: Debug
    # 0: Not set
    logger = logging.getLogger(None if verbose >= 3 else __package__)
    verbose = 30 - (verbose * 10)
    verbose = verbose if verbose > 10 else logging.DEBUG
    logger.setLevel(level=verbose)

    if version:
        print(__version__)
        return

    win_path = r"C:\Users\kiril\programming\todo-console-app\tasks.json"
    # unix_path = "/home/kleskin/programming/todo-console-app/tasks.json"
    ctx.obj = {
        "tasks": Tasks(Path(win_path)),
    }


@cli_app.command("help")
def cli_help(ctx: typer.Context) -> None:
    """Show this help message."""
    print(ctx.parent.get_help())  # type: ignore


@cli_app.command("logging")
def cli_logging() -> None:
    """Test logging."""
    logger.critical("SHOW CRITICAL")
    logger.error("SHOW ERROR")
    logger.warning("SHOW WARNING")
    logger.info("SHOW INFO")
    logger.debug("SHOW DEBUG")


@cli_app.command("tui")
def cli_tui(ctx: typer.Context) -> None:
    """Open a TUI application."""
    tasks: Tasks = ctx.obj["tasks"]
    TasksApp(tasks).run()


@cli_app.command("list")
@cli_app.command("ls")
def list_tasks(ctx: typer.Context) -> None:
    """List all tasks."""
    tasks: Tasks = ctx.obj["tasks"]
    for task in tasks:
        done = "X" if task.done else " "
        print(f"[{done}] {task.title}")
    print("-------------")
    print(f"{len(tasks)} items")


@cli_app.command("add")
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
    if not title:
        title = input("Add task title: ")
    tasks: Tasks = ctx.obj["tasks"]
    tasks.add(title)


@cli_app.command("pick")
def pick_task(ctx: typer.Context) -> None:
    """Pick a task for editing."""
    tasks: Tasks = ctx.obj["tasks"]

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


def clean_terminate(err: Exception) -> None:
    """Terminate nicely the program depending the exception."""
    user_errors = (
        PermissionError,
        FileExistsError,
        FileNotFoundError,
        InterruptedError,
        IsADirectoryError,
        NotADirectoryError,
        TimeoutError,
    ) + (
        # MyAppException,
        # yaml.parser.ParserError,
        # sh.ErrorReturnCode,
    )

    if isinstance(err, user_errors):

        # Fetch extra error informations
        rc = int(getattr(err, "rc", getattr(err, "errno", 1)))
        advice = getattr(err, "advice", None)
        if advice:
            logger.warning(advice)

        # Log error and exit
        logger.error(err)
        err_name = err.__class__.__name__
        logger.critical("MyApp exited with error %s (%s)", err_name, rc)
        sys.exit(rc)

    # Developper bug catchall
    rc = 255
    logger.error(traceback.format_exc())
    logger.critical("Uncatched error: %s", err.__class__)
    logger.critical("This is a bug, please report it.")
    sys.exit(rc)


def main() -> None:
    """Run CLI application."""
    try:
        return cli_app()
    except Exception as err:
        clean_terminate(err)


if __name__ == "__main__":
    main()
