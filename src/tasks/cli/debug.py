"""CLI module for debugging."""

import logging
import shutil

import rich
import rich.prompt
import typer

from tasks.app_config import CONFIG_DIR, CONFIG_FILE_PATH, DATA_DIR, DEFAULT_LIST_PATH
from tasks.cli.utils import print_tree

logger = logging.getLogger()
console = rich.console.Console()

debug_cli = typer.Typer(
    help="Debug commands for CLI. For development only.",
    invoke_without_command=True,
    no_args_is_help=True,
)


@debug_cli.command("help")
def cli_help(ctx: typer.Context) -> None:
    """Show this help message."""
    print(ctx.parent.get_help())  # type: ignore


@debug_cli.command("config")
def debug_config(ctx: typer.Context) -> None:
    """View configuration file path."""
    console.print(f"Config file path: {CONFIG_FILE_PATH}")
    console.print(f"Default tasks list file path: {DEFAULT_LIST_PATH}")


@debug_cli.command("logging")
def debug_logging() -> None:
    """Test logging."""
    logger.debug("SHOW DEBUG")
    logger.info("SHOW INFO")
    logger.warning("SHOW WARNING")
    logger.error("SHOW ERROR")
    logger.critical("SHOW CRITICAL")


@debug_cli.command("clean")
def clean(ctx: typer.Context, force: bool = typer.Option(False, "-y")) -> None:
    """Clean app configuration.

    Removes configuration file and a default tasks list.
    """
    if not force:
        console.print(
            "[yellow]WARNING[/yellow]: This action will "
            "[bold]permanently[/bold] delete [red]all configuration files[/red] "
            "and [red]all of user data[/red]."
        )
        result = rich.prompt.Prompt.ask(
            "Continue?",
            console=console,
            choices=["y", "n"],
        )
        if result != "y":
            console.print("Aborted")
            return

    if CONFIG_DIR.exists():
        print_tree(CONFIG_DIR)
        shutil.rmtree(CONFIG_DIR)
        console.print(f"Configurations folder and all of its contents [red]deleted[/red]: {CONFIG_DIR}")

    if DATA_DIR.exists():
        print_tree(DATA_DIR)
        shutil.rmtree(DATA_DIR)
        console.print(f"User data folder and all of its contents [red]deleted[/red]: {DEFAULT_LIST_PATH}")

    console.print("App data is cleaned")
