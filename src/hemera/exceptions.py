class HemeraError(Exception):
    """Base class for all Hemera errors."""


class ValueNotFoundInHemeraHttpRequest(HemeraError):
    """Raised when a value is not found in a dictionary."""

    def __init__(self):
        raise HemeraError("Value not found in HemeraHttpRequest.")


class SlackApiError(HemeraError):
    """Raised when an error occurs when sending a message to Slack."""

    def __init__(self):
        raise HemeraError("Error sending message to Slack.")


class EnvironmentVariableNotSetError(HemeraError):
    """Raised when an environment variable is not set."""

    def __init__(self):
        raise HemeraError("Environment variable not set.")


class HomeAutomationWebhookError(HemeraError):
    """Raised when an error occurs when running the Home Automation webhook."""

    def __init__(self):
        raise HemeraError("Error running Home Automation webhook.")


class UnauthorizedUserError(HemeraError):
    """Raised when an unauthorized user attempts to run the Home Automation
    webhook."""

    def __init__(self):
        raise HemeraError("Unauthorized user.")


class SoftwareVerionsNotFoundError(HemeraError):
    """Raised when the software versions are not found."""

    def __init__(self):
        raise HemeraError("Software versions not found.")


class ValueNotFoundInHemeraMetadata(HemeraError):
    """Raised when a value is not found in a dictionary."""

    def __init__(self):
        raise HemeraError("Value not found in HemeraMetadata.")


class AutomationHandlerException(HemeraError):
    """Raised when an error occurs in the AutomationHandler class."""

    def __init__(self):
        raise HemeraError("Error in AutomationHandler class.")


class GithubEventNotSupportedError(HemeraError):
    """Raised when a GitHub event is not supported."""

    def __init__(self):
        raise HemeraError("GitHub event not supported.")


class EnvironmentVariableDeprecatedError(HemeraError):
    """Raised when an environment variable is deprecated."""

    def __init__(self, env_var_name: str):
        super().__init__(f"Environment variable {env_var_name} is deprecated.")
