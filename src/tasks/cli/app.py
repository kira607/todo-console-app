"""A wiring of CLI modules into a CLI app."""

import logging
import sys
import traceback

import typer
from rich.console import Console
from rich.markdown import Markdown

from tasks import APP_NAME, APP_VERSION
from tasks.cli.errors import NoActiveListError, NoTasksListsError
from tasks.logging import setup_logging

from .context import ContextObject
from .debug import debug_cli
from .lists import lists_cli
from .tasks import tasks_cli

logger = logging.getLogger()
console = Console()


def root_callback(
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
    setup_logging(verbose)

    if version:
        console.print(f"{APP_NAME} {APP_VERSION}")
        return

    ctx.obj = ContextObject()


def clean_terminate(err: Exception) -> None:
    """Terminate nicely the program depending the exception."""
    user_errors = (
        # PermissionError,
        # FileExistsError,
        # FileNotFoundError,
        # InterruptedError,
        # IsADirectoryError,
        # NotADirectoryError,
        # TimeoutError,
    ) + (
        NoActiveListError,
        NoTasksListsError,
        # yaml.parser.ParserError,
        # sh.ErrorReturnCode,
    )

    if isinstance(err, user_errors):

        # Fetch extra error informations
        rc = int(getattr(err, "rc", getattr(err, "errno", 1)))
        advice = getattr(err, "advice", None)
        console.print(f"[bold red]{err.message}[/bold red]")
        # logger.error(f"MyApp exited with error {err.__class__.__name__} ({rc})")

        if advice:
            console.print(f"[bold blue]Hint[/bold blue]: {advice}")

        # Log error and exit
        # err_name = err.__class__.__name__
        sys.exit(rc)

    # Developper bug catchall
    rc = 255
    logger.error(traceback.format_exc())
    logger.critical("Uncatched error: %s", err.__class__)
    logger.critical("FATAL ERROR! This is a bug, please report it.")
    sys.exit(rc)


def run_cli() -> None:
    """Run CLI application."""
    try:
        tasks_cli.callback()(root_callback)
        tasks_cli.add_typer(debug_cli, name="debug")
        tasks_cli.add_typer(lists_cli, name="lists")
        return tasks_cli()
    except Exception as err:
        clean_terminate(err)


if __name__ == "__main__":
    run_cli()
