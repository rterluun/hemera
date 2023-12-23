from logging import Logger, getLogger

from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse

from hemera.exceptions import SlackApiError, ValueNotFoundInDictError

LOGGER = getLogger(__name__)


def create_slack_message(
    http_request_dict: dict,
    logger: Logger = LOGGER,
) -> str:
    """
    Convert an Azure Functions HTTP request dictionary to a Slack message.

    Args:
        http_request_dict (dict): The HTTP request dictionary to create the Slack message from.
        logger (Logger, optional): The logger to use. Defaults to LOGGER.

    Returns:
        str: The created Slack message.
    """
    logger.info("Converting HTTP request dictionary to Slack message.")

    try:
        action = http_request_dict["body"]["action"]
        repository = http_request_dict["body"]["repository"]["full_name"]
        user = http_request_dict["body"]["sender"]["login"]
        return (
            f"The following action [{action}] was performed on the repository: {repository}\n"
            f"The action was performed by: {user}"
        )
    except Exception as e:
        logger.error(f"Value not found in dictionary: {e}")
        raise ValueNotFoundInDictError from e


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
