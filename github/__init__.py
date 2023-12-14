from logging import getLogger
from os import getenv as os_getenv

import azure.functions as func

from hemera.exceptions import EnvironmentVariableNotSetError, HemeraError
from hemera.homeautomation import run_homeautomation_webhook
from hemera.http_request_handler import convert_http_request_to_dict
from hemera.notifications import select_fields_for_slack_message, send_slack_message

LOGGER = getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    LOGGER.info("Python HTTP trigger function processed a request.")
    slack_api_token = os_getenv("SLACK_API_TOKEN")
    slack_channel = os_getenv("SLACK_CHANNEL")
    homeautomation_webhook = os_getenv("HOMEAUTOMATION_WEBHOOK")

    try:
        if (
            not slack_api_token or not slack_channel or not homeautomation_webhook
        ):  # Check if environment variables are set
            raise EnvironmentVariableNotSetError

        http_request_dict = convert_http_request_to_dict(
            req=req,
            logger=LOGGER,
        )

        message = select_fields_for_slack_message(
            http_request_dict=http_request_dict,
            logger=LOGGER,
        )

        send_slack_message(
            slack_api_token=slack_api_token,
            channel=slack_channel,
            message=message,
            logger=LOGGER,
        )

        run_homeautomation_webhook(
            homeautomation_webhook=homeautomation_webhook,
            message=message,
            logger=LOGGER,
        )

    except HemeraError as e:
        return func.HttpResponse(f"Error: {e}", status_code=400)

    return func.HttpResponse("Message sent to Slack successfully.", status_code=200)
