"""CLI context."""

import logging

from tasks.app_config import AppConfig, load_app_config
from tasks.cli.errors import NoActiveListError
from tasks.cli.utils import is_valid_json_file_path
from tasks.core import TasksList

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
    _tasks: TasksList

    @property
    def config(self) -> AppConfig:
        """Get :class:`AppConfig` instance."""
        if getattr(self, "_config", None) is None:
            self._config = load_app_config()
        return self._config

    @property
    def tasks(self) -> TasksList:
        """Get :class:`Tasks` instance for currently selected list.

        :raises NoActiveListError: Active tasks list is not set.
        :return TasksList: A tasks list handler.
        """
        config = self.config

        if config.active_list is None:
            raise NoActiveListError()

        if getattr(self, "_tasks", None) is None:
            valid, error = is_valid_json_file_path(config.active_list)

            if not valid:
                logger.warning(f"Path: {config.active_list} is not a valid json file: {error}")

            self._tasks = TasksListWidget(config.active_list)

        return self._tasks
