from logging import getLogger
from os import getenv as os_getenv

import azure.functions as func

from hemera.deprecated import (
    DEPRECATEDENVIRIONMENTVARIABLES,
    scan_for_deprecated_env_vars,
)
from hemera.exceptions import (
    EnvironmentVariableNotSetError,
    GithubEventNotSupportedError,
    HemeraError,
    UnauthorizedUserError,
)
from hemera.handlers import AutomationHandler
from hemera.types import HemeraHttpRequest

LOGGER = getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function entry point.

    Args:
        req (func.HttpRequest): The incoming HTTP request.

    Raises:
        EnvironmentVariableNotSetError: When environment variables are not set.
        UnauthorizedUserError: When the user is not whitelisted.

    Returns:
        func.HttpResponse: The outgoing HTTP response.
    """
    LOGGER.info("Python HTTP trigger function processed a request.")

    slack_api_token = os_getenv("SLACK_API_TOKEN")
    slack_channel = os_getenv("SLACK_CHANNEL")
    homeautomation_webhook = os_getenv("HOMEAUTOMATION_WEBHOOK")
    pr_author_filter = os_getenv("PR_AUTHOR_FILTER") or os_getenv("ALLOWED_USERNAME")

    try:
        scan_for_deprecated_env_vars(
            deprecated_env_vars=DEPRECATEDENVIRIONMENTVARIABLES, logger=LOGGER
        )

        if (
            not slack_api_token
            or not slack_channel
            or not homeautomation_webhook
            or not pr_author_filter
        ):
            raise EnvironmentVariableNotSetError

        hemera_http_request = HemeraHttpRequest.from_azure_functions_http_request(
            req=req, logger=LOGGER
        )

        if hemera_http_request.githubevent != "pull_request":
            raise GithubEventNotSupportedError

        if hemera_http_request.username != pr_author_filter:
            raise UnauthorizedUserError

        automation_handler = AutomationHandler(
            slack_api_token=slack_api_token,
            slack_channel=slack_channel,
            homeautomation_webhook=homeautomation_webhook,
            logger=LOGGER,
        )

        automation_handler.handle_request(hemera_http_request=hemera_http_request)

    except HemeraError as e:
        LOGGER.error("Error: %s", e)
        return func.HttpResponse(f"Error: {e}", status_code=400)

    LOGGER.info("Python HTTP trigger function executed successfully.")
    return func.HttpResponse("Automation executed successfully.", status_code=200)
