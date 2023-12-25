from logging import Logger, getLogger

from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse

from hemera.exceptions import SlackApiError, ValueNotFoundInHemeraHttpRequest
from hemera.types import HemeraHttpRequest

LOGGER = getLogger(__name__)


def create_slack_message(
    hemera_http_request: HemeraHttpRequest,
    logger: Logger = LOGGER,
) -> str:
    """Convert an Azure Functions HTTP request to a Slack message."""
    logger.info("Converting HTTP request dictionary to Slack message.")

    try:
        return (
            f"The following action [{hemera_http_request.action}] "
            f"was performed on the repository: {hemera_http_request.repository}\n"
            f"The action was performed by: {hemera_http_request.username}"
        )
    except Exception as e:
        logger.error(f"Value not found in HemeraHttpRequest: {e}")
        raise ValueNotFoundInHemeraHttpRequest from e


def send_slack_message(
    slack_api_token: str,
    channel: str,
    message: str,
    logger: Logger = LOGGER,
) -> SlackResponse:
    """Send a message to a Slack channel."""
    try:
        client = WebClient(token=slack_api_token)
        response = client.chat_postMessage(channel=channel, text=message)
        return response
    except Exception as e:
        logger.error(f"Error sending message to Slack: {e}")
        raise SlackApiError from e
