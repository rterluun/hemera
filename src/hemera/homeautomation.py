from logging import getLogger

from requests import post

from hemera.exceptions import HomeAutomationWebhookError

LOGGER = getLogger(__name__)


def send_request_to_homeautomation_webhook(
    homeautomation_webhook: str,
    message: str,
) -> None:
    """Send a request to the Home Automation webhook.

    Args:
        homeautomation_webhook (str): The Home Automation webhook.
        message (str): The message to send.

    Raises:
        HomeAutomationWebhookError: When an error occurs when running the Home Automation webhook.
    """
    try:
        response = post(
            url=homeautomation_webhook,
            json={
                "message": message,
            },
            timeout=5,
        )
        response.raise_for_status()
    except Exception as e:
        raise HomeAutomationWebhookError from e
