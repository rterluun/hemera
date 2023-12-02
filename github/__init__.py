from logging import getLogger
from os import getenv as os_getenv
import azure.functions as func
from slack_sdk.errors import SlackApiError
from hemera.http_request_handler import convert_http_request_to_dict
from hemera.notifications import (
    send_slack_message,
    convert_http_request_dict_to_slack_message,
)

LOGGER = getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    LOGGER.info("Python HTTP trigger function processed a request.")

    try:
        http_request_dict = convert_http_request_to_dict(req=req, logger=LOGGER)
        message = convert_http_request_dict_to_slack_message(
            http_request_dict=http_request_dict, logger=LOGGER
        )
    except KeyError:
        return func.HttpResponse(
            "Unable to convert HTTP request to Slack message", status_code=400
        )

    try:
        send_slack_message(
            slack_api_token=os_getenv("SLACK_API_TOKEN"),
            channel=os_getenv("SLACK_CHANNEL"),
            message=message,
            logger=LOGGER,
        )
    except SlackApiError:
        return func.HttpResponse("Error sending Slack message", status_code=400)

    return func.HttpResponse("Message sent to Slack successfully.", status_code=200)
