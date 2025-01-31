"""Various utilities."""

import json
from pathlib import Path
from typing import Any

from rich import print  # noqa: A004
from rich.console import Console
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree


def is_valid_json_file_path(path: Any) -> tuple[bool, str]:  # noqa: ANN401
    """Check if a file at ``path`` is a valid json.

    :param Any path: File path to validate.
    :return bool: True if ``path`` is a path to a valid
        json file, False otherwise.
    """
    try:
        path = Path(path)
    except Exception:
        return False, "Not a path"

    if not path.exists():
        return False, "Not exsists"

    if not path.is_file():
        return False, "Not a file"

    try:
        with path.open("r") as f:
            json.load(f)
        return True, ""
    except Exception:
        return False, "Not a valid json"


# This is taken from: https://github.com/textualize/rich/blob/master/examples/tree.py
def walk_directory(directory: Path, tree: Tree) -> None:
    """Recursively build a Tree with directory contents."""
    # Sort dirs first then by filename
    paths = sorted(
        Path(directory).iterdir(),
        key=lambda path: (path.is_file(), path.name.lower()),
    )
    for path in paths:
        # Remove hidden files
        if path.name.startswith("."):
            continue
        if path.is_dir():
            style = "dim" if path.name.startswith("__") else ""
            branch = tree.add(
                f"[bold magenta]:open_file_folder: [link file://{path}]{escape(path.name)}",
                style=style,
                guide_style=style,
            )
            walk_directory(path, branch)
        else:
            text_filename = Text(path.name, "green")
            text_filename.highlight_regex(r"\..*$", "bold red")
            text_filename.stylize(f"link file://{path}")
            file_size = path.stat().st_size
            text_filename.append(f" ({decimal(file_size)})", "blue")
            icon = "🐍 " if path.suffix == ".py" else "📄 "
            tree.add(Text(icon) + text_filename)


def print_tree(path: Path, console: Console | None = None) -> None:
    """Print files tree for ``path``."""
    tree = Tree(
        f":open_file_folder: [link file://{path}]{path}",
        guide_style="bold bright_blue",
    )
    walk_directory(Path(path), tree)

    if console:
        console.print(tree)
    else:
        print(tree)
