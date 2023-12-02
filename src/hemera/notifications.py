from logging import getLogger, Logger
from typing import Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.web.slack_response import SlackResponse


LOGGER = getLogger(__name__)


def convert_http_request_dict_to_slack_message(
    http_request_dict: dict,
    logger: Logger = LOGGER,
) -> str:
    """Convert an Azure Functions HTTP request dictionary to a Slack message."""
    logger.info("Converting HTTP request dictionary to Slack message.")

    try:
        action = http_request_dict["body"]["action"]
        pull_request_url = http_request_dict["body"]["pull_request"]["html_url"]
        pull_request_number = http_request_dict["body"]["pull_request"]["number"]
        return f"Action: {action}, Pull request URL: {pull_request_url}, Pull request Number: {pull_request_number}"
    except KeyError:
        logger.info("Key not found in HTTP request dictionary")
        raise KeyError("Key not found in HTTP request dictionary")


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
