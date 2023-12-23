from logging import Logger, getLogger

from requests import post

from hemera.exceptions import HomeAutomationWebhookError

LOGGER = getLogger(__name__)


def send_request_to_homeautomation_webhook(
    homeautomation_webhook: str,
    message: str,
    logger: Logger = LOGGER,
) -> None:
    """Run the Home Automation webhook."""
    try:
        response = post(
            url=homeautomation_webhook,
            json={
                "message": message,
            },
        )
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Error while running Home Automation webhook: {e}")
        raise HomeAutomationWebhookError from e
