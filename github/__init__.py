from logging import getLogger
from os import getenv as os_getenv

import azure.functions as func

from hemera.exceptions import (
    EnvironmentVariableNotSetError,
    HemeraError,
    UnauthorizedUserError,
)
from hemera.handlers import AutomationHandler
from hemera.types import HemeraHttpRequest

LOGGER = getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    LOGGER.info("Python HTTP trigger function processed a request.")
    slack_api_token = os_getenv("SLACK_API_TOKEN")
    slack_channel = os_getenv("SLACK_CHANNEL")
    homeautomation_webhook = os_getenv("HOMEAUTOMATION_WEBHOOK")
    allowed_username = os_getenv("ALLOWED_USERNAME")

    try:
        if (
            not slack_api_token
            or not slack_channel
            or not homeautomation_webhook
            or not allowed_username
        ):  # Check if environment variables are set
            raise EnvironmentVariableNotSetError

        hemera_http_request = HemeraHttpRequest.from_azure_functions_http_request(
            req=req, logger=LOGGER
        )

        if hemera_http_request.username != allowed_username:
            raise UnauthorizedUserError

        automation_handler = AutomationHandler(
            slack_api_token=slack_api_token,
            slack_channel=slack_channel,
            homeautomation_webhook=homeautomation_webhook,
            logger=LOGGER,
        )

        automation_handler.handle_request(hemera_http_request=hemera_http_request)

    except HemeraError as e:
        return func.HttpResponse(f"Error: {e}", status_code=400)

    return func.HttpResponse("Message sent to Slack successfully.", status_code=200)
