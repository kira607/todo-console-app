"""A wiring of CLI modules into a CLI app."""

import logging
import sys
import traceback

import typer
from rich.console import Console

from tasks import APP_NAME, APP_VERSION
from tasks.logging import setup_logging

from .context import ContextObject
from .debug import debug_cli
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
    logger.debug(f"{verbose=}")

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
    logger.critical("FATAL ERROR! This is a bug, please report it.")
    sys.exit(rc)


def run_cli() -> None:
    """Run CLI application."""
    try:
        tasks_cli.callback()(root_callback)
        tasks_cli.add_typer(debug_cli, name="debug")
        return tasks_cli()
    except Exception as err:
        clean_terminate(err)


if __name__ == "__main__":
    run_cli()
