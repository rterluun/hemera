from logging import Logger, getLogger

from hemera.exceptions import HemeraError
from hemera.homeautomation import send_request_to_homeautomation_webhook
from hemera.slack import create_slack_message, send_slack_message
from hemera.types import HemeraHttpRequest

LOGGER = getLogger(__name__)


class AutomationHandler:
    """Class to handle automation."""

    def __init__(
        self,
        slack_api_token: str,
        slack_channel: str,
        homeautomation_webhook: str,
        logger: Logger = LOGGER,
    ):
        """Initialize an instance of the AutomationHandler class.

        Args:
            slack_api_token (str): The Slack API token.
            slack_channel (str): The Slack channel.
            homeautomation_webhook (str): The Home Automation webhook.
            logger (Logger, optional): The logger. Defaults to LOGGER.
        """
        self.slack_api_token = slack_api_token
        self.slack_channel = slack_channel
        self.homeautomation_webhook = homeautomation_webhook
        self.logger = logger
        self.message: str = ""

    def _create_slack_message(
        self,
        hemera_http_request: HemeraHttpRequest,
    ):
        """Create a Slack message from the HemeraHttpRequest and store it in.

        Args:
            hemera_http_request (HemeraHttpRequest): The Hemera HTTP request.
        """
        self.logger.info("Creating Slack message.")
        try:
            self.message = create_slack_message(hemera_http_request=hemera_http_request)
        except HemeraError as e:
            self.logger.error("Error creating Slack message, %s", e)

    def _send_slack_message(self):
        """Send the Slack message stored in this instance."""
        self.logger.info("Sending Slack message.")
        try:
            send_slack_message(
                slack_api_token=self.slack_api_token,
                channel=self.slack_channel,
                message=self.message,
            )
        except HemeraError as e:
            self.logger.error("Error sending Slack message, %s", e)

    def _send_request_to_homeautomation_webhook(self):
        """Send a request to the Home Automation webhook."""
        self.logger.info("Sending request to Home Automation webhook.")

        try:
            send_request_to_homeautomation_webhook(
                homeautomation_webhook=self.homeautomation_webhook,
                message=self.message,
            )
        except HemeraError as e:
            self.logger.error("Error sending request to Home Automation webhook, %s", e)

    def handle_request(
        self,
        hemera_http_request: HemeraHttpRequest,
    ):
        """Handle a request.

        Args:
            hemera_http_request (HemeraHttpRequest): The Hemera HTTP request.
        """
        self.logger.info("Handling request.")
        self._create_slack_message(hemera_http_request=hemera_http_request)
        self._send_slack_message()
        self._send_request_to_homeautomation_webhook()
