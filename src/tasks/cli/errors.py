"""Custom errors."""


class CLIError(Exception):
    """Base CLI error."""

    message: str
    advice: str
    rc: int


class NoActiveListError(CLIError):
    """No list is set as active."""

    message = "No active list selected"
    advice = "Set active list using [code]tasks lists select[/code]"
    rc = 0


class NoTasksListsError(CLIError):
    """There are no tasks lists."""

    message = "There are no tasks lists"
    advice = "Add a new tasks list using [code]tasks lists new[/code]"
    rc = 0
