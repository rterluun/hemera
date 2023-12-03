class HemeraError(Exception):
    """Base class for all Hemera errors."""


class ValueNotFoundInDictError(HemeraError):
    """Raised when a value is not found in a dictionary."""

    def __init__(self):
        raise HemeraError("Value not found in dictionary.")


class SlackApiError(HemeraError):
    """Raised when an error occurs when sending a message to Slack."""

    def __init__(self):
        raise HemeraError("Error sending message to Slack.")


class EnvironmentVariableNotSetError(HemeraError):
    """Raised when an environment variable is not set."""

    def __init__(self):
        raise HemeraError("Environment variable not set.")
