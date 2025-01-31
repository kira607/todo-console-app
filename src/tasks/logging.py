"""Logging utilities."""  # noqa: A005

import logging

from rich.logging import RichHandler

# Logging cheat-sheet
# -------------------
# 50: Crit
# 40: Err
# 30: Warn
# 20: Info
# 10: Debug
# 0: Not set


def setup_logging(level: int) -> None:
    """Set up root logger depending on verbosity."""
    base_level = 40
    level = base_level - (level * 10)
    level = level if level > 10 else logging.DEBUG
    logging.basicConfig(
        format="%(message)s",
        datefmt="[%X]",
        level=level,
        handlers=[RichHandler(rich_tracebacks=True)],
    )
