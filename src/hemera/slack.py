from logging import getLogger

from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse

from hemera.exceptions import SlackApiError, ValueNotFoundInHemeraHttpRequest
from hemera.types import HemeraHttpRequest

LOGGER = getLogger(__name__)


def create_slack_message(hemera_http_request: HemeraHttpRequest) -> str:
    """Create a Slack message from the HemeraHttpRequest.

    Args:
        hemera_http_request (HemeraHttpRequest): The Hemera HTTP request.

    Raises:
        ValueNotFoundInHemeraHttpRequest: When a value is not found in the HemeraHttpRequest.

    Returns:
        str: The Slack message.
    """
    try:
        return (
            f"The following action [{hemera_http_request.action}] "
            f"was performed on the repository: {hemera_http_request.repository}\n"
            f"The action was performed by: {hemera_http_request.username}\n"
            f"Created by Hemera v{hemera_http_request.metadata.core}"
        )
    except Exception as e:
        raise ValueNotFoundInHemeraHttpRequest from e


def send_slack_message(
    slack_api_token: str,
    channel: str,
    message: str,
) -> SlackResponse:
    """Send a message to Slack.

    Args:
        slack_api_token (str): The Slack API token.
        channel (str): The Slack channel.
        message (str): The message to send.

    Raises:
        SlackApiError: When an error occurs when sending a message to Slack.

    Returns:
        SlackResponse: The Slack response.
    """
    try:
        client = WebClient(token=slack_api_token)
        response = client.chat_postMessage(channel=channel, text=message)
        return response
    except Exception as e:
        raise SlackApiError from e
