"""CLI context."""

import logging

from tasks.app_config import AppConfig, load_app_config
from tasks.cli.utils import is_valid_json_file_path
from tasks.core import Tasks

logger = logging.getLogger()


class ContextObject:
    """CLI context object.

    An instance of this class is shared between all CLI comands
    via a `typer.Context.obj`.

    This is a central place to handle app-wide operations
    like loading app configuration, initializing
    entity repositories, etc.
    """

    _config: AppConfig
    _tasks: Tasks

    @property
    def config(self) -> AppConfig:
        """Get :class:`AppConfig` instance."""
        if getattr(self, "_config", None) is None:
            self._config = load_app_config()
        return self._config

    @property
    def tasks(self) -> Tasks:
        """Get :class:`Tasks` instance for currently selected list."""
        if getattr(self, "_tasks", None) is None:
            config = self.config
            valid, error = is_valid_json_file_path(config.active_list)

            if not valid:
                logger.warning(f"Path: {config.active_list} is not a valid json file: {error}")

            self._tasks = Tasks(config.active_list)

        return self._tasks
