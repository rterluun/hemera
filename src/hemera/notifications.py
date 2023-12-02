from logging import getLogger, Logger
from typing import Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web.slack_response import SlackResponse


LOGGER = getLogger(__name__)


def send_slack_message(
    slack_api_token: str,
    channel: str,
    message: str,
    logger: Logger = LOGGER,
) -> Optional[SlackResponse]:
    """Send a message to a Slack channel."""
    try:
        client = WebClient(token=slack_api_token)
        response = client.chat_postMessage(channel=channel, text=message)
        return response
    except SlackApiError as e:
        logger.error(f"Error sending Slack message: {e.response['error']}")
        return None
