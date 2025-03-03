"""CLI module to manage tasks lists."""

import json
import logging
from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from tasks.app_config import DATA_DIR, AppConfig, save_app_config
from tasks.cli.errors import NoTasksListsError
from tasks.cli.selector import select_menu
from tasks.cli.utils import is_valid_json_file_path
from tasks.core import TasksList

logger = logging.getLogger()
console = Console()
lists_cli = typer.Typer(
    help="Manage tasks lists.",
    invoke_without_command=True,
)


@lists_cli.callback()
def lists_callback(ctx: typer.Context) -> None:
    """Show tasks lists."""
    if ctx.invoked_subcommand is not None:
        return

    table = Table("Title", "List path", "Number of tasks", "List completion")
    config: AppConfig = ctx.obj.config
    for list_path in config.task_lists:
        tasks = TasksList(list_path)
        title = f"[green]{tasks.title}[/green]" if list_path == ctx.obj.config.active_list else str(tasks.title)
        table.add_row(
            title,
            str(list_path),
            str(len(tasks)),
            f"{tasks.completed_number}/{len(tasks)}",
        )
    table.title = "Tasks lists"
    table.caption = f"{len(config.task_lists)} list(s)"
    console.print(table)


@lists_cli.command("help")
def cli_help(ctx: typer.Context) -> None:
    """Show this help message."""
    print(ctx.parent.get_help())  # type: ignore


@lists_cli.command("active")
def show_active_list(ctx: typer.Context) -> None:
    """Show currently active tasks list."""
    tasks: TasksListWidget = ctx.obj.tasks
    console.print(f"{tasks.title} ([bold]{ctx.obj.config.active_list}[/bold])")


@lists_cli.command("new")
def create_new_list(
    ctx: typer.Context,
    list_title: str,
    set_active: bool = typer.Option(
        False,
        "-a",
        help="Set new list as active after creation",
    ),
) -> None:
    """Create a new tasks list."""
    config: AppConfig = ctx.obj.config
    console.print(f"Creating a new list with a title: {list_title}")
    file_name = "".join(filter(lambda x: str.isalpha(x) or x == " ", list_title)) + ".json"
    file_name = file_name.replace(" ", "_").lower()
    logger.debug(f"file name is {file_name}")
    list_path = Path(DATA_DIR, file_name)
    logger.debug(f"file path is {list_path}")
    if list_path.exists():
        console.print("list already exists")
        return
    list_path.touch()
    list_data = {"title": list_title, "tasks": {}}
    with list_path.open("w") as f:
        json.dump(list_data, f)
    config.task_lists.append(list_path)
    if set_active:
        config.active_list = list_path
    save_app_config(config)
    console.print("list created!")


@lists_cli.command("add")
def add_tasks_list(
    ctx: typer.Context,
    list_path: Path,
    set_active: bool = typer.Option(
        False,
        "-a",
        help="Set new list as active after creation",
    ),
) -> None:
    """Add existing tasks list."""
    config: AppConfig = ctx.obj.config
    list_path = Path(list_path).absolute().resolve()

    # validate path is a json file
    valid, message = is_valid_json_file_path(list_path)
    if not valid:
        console.print(f"Not a valid path: {message}")
        return

    # check if file contents are valid
    try:
        TasksListWidget(list_path)
    except Exception:
        console.print("not a tasks list")
        return

    if list_path in config.task_lists:
        console.print("The list is already added")
        return

    config.task_lists.append(Path(list_path).absolute().resolve())

    if set_active:
        config.active_list = Path(list_path).absolute().resolve()

    save_app_config(config)
    console.print("list added!")



@lists_cli.command("select")
def select_list(ctx: typer.Context) -> None:
    """Select a list to be active."""
    config: AppConfig = ctx.obj.config
    if not config.task_lists:
        raise NoTasksListsError()
    options = [str(p) for p in config.task_lists]
    default = options.index(str(config.active_list)) if config.active_list else -1
    new_active = select_menu(
        options=options,
        prompt="Select new active list",
        default=default,
    )
    if new_active is None:
        console.print("Selection canceled")
        return
    config.active_list = Path(new_active)
    save_app_config(config)
    console.print(f"New active tasks list: {new_active}")


@lists_cli.command("delete")
def delete_list(
    ctx: typer.Context,
    delete: bool = typer.Option(False, "-d", help="Also delete tasks file."),
    force: bool = typer.Option(False, "-f", help="Force the deletion, don't ask for comfirmation"),
) -> None:
    """Delete tasks list from a list of tasks lists."""
    config: AppConfig = ctx.obj.config
    if not config.task_lists:
        raise NoTasksListsError()
    options = [str(p) for p in config.task_lists]
    default = options.index(str(config.active_list)) if config.active_list else -1
    to_delete = select_menu(
        options=options,
        prompt="Select a list for deletion",
        default=default,
    )

    if to_delete is None:
        console.print("Selection canceled")
        return

    if delete and not force:
        console.print("[yellow]WARNING[/yellow]: This action will [bold]permanently[/bold] delete this tasks list.")
        result = Prompt.ask(
            "Continue?",
            console=console,
            choices=["y", "n"],
        )
        if result != "y":
            console.print("Aborted")
            return

    path = Path(to_delete)

    if path == config.active_list:
        config.active_list = None

    config.task_lists.remove(path)
    save_app_config(config)

    if delete:
        path.unlink()

    console.print(f"Tasks list deleted: {to_delete}")
