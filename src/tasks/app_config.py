"""Application configuration."""

import logging
from pathlib import Path

import platformdirs
from pydantic import BaseModel, ValidationError

from tasks import APP_NAME

logger = logging.getLogger()


class AppConfig(BaseModel):
    """Application global configuration."""

    active_list: Path | None
    task_lists: list[Path]


CONFIG_DIR = platformdirs.user_config_path(APP_NAME, False)
"""Place where configuration files are stored."""

DATA_DIR = platformdirs.user_data_path(APP_NAME, False)
"""Place where user data is stored."""

CONFIG_FILE_PATH = Path(CONFIG_DIR, "config.json")
"""App configuration file path."""

DEFAULT_LIST_PATH = Path(platformdirs.user_data_path(APP_NAME, False), "default.json")
"""Default tasks list file path."""

DEFAULT_CONFIG = f"""{{
    "active_list": "{DEFAULT_LIST_PATH.as_posix()}",
    "task_lists": [
        "{DEFAULT_LIST_PATH.as_posix()}"
    ]
}}
"""
"""Default configuration json string."""


def _default_setup() -> AppConfig:
    """Set up default configuration.

    Creates a configuration file and a default tasks list file,
    including all nessesary folders and subfolders.

    :return AppConfig: An :class:`AppConfig` instance with default configuration.
    """
    # Touch config file and default tasks list
    CONFIG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE_PATH.touch()
    DEFAULT_LIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_LIST_PATH.touch()

    # Fill app config with default values
    with CONFIG_FILE_PATH.open("w") as f:
        f.write(DEFAULT_CONFIG)

    # Fill default list with something
    # This is needed to pass file validity check
    with DEFAULT_LIST_PATH.open("w") as f:
        f.write('{"title": "Default", "tasks": {}}')

    # Return default configuration
    return AppConfig.model_validate_json(DEFAULT_CONFIG)


def load_app_config() -> AppConfig:
    """Load app configuration."""
    config_file_path = CONFIG_FILE_PATH

    # Create config file if not exists and fill it with default configuration
    if not config_file_path.exists():
        logger.debug("Config file does not exist. Creating a new one...")
        return _default_setup()

    with config_file_path.open("r") as f:
        config_file_data = f.read()

    if config_file_data == "":
        logger.warning("Config file is empty. Filling it with default values...")
        return _default_setup()

    try:
        return AppConfig.model_validate_json(config_file_data)
    except ValidationError:
        logger.warning("Config file is corrupted, overwriting with the default config")
        return _default_setup()


def save_app_config(config: AppConfig) -> None:
    """Save app config to a file."""
    with CONFIG_FILE_PATH.open("w") as f:
        f.write(config.model_dump_json(indent=4))
