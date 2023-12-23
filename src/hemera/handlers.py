from logging import Logger, getLogger

from hemera.homeautomation import send_request_to_homeautomation_webhook
from hemera.slack import create_slack_message, send_slack_message

LOGGER = getLogger(__name__)


class AutomationHandler:
    """
    A class to handle automation tasks such as sending messages to Slack and triggering home automation webhooks.
    """

    def __init__(
        self,
        slack_api_token: str,
        slack_channel: str,
        homeautomation_webhook: str,
        logger: Logger = LOGGER,
    ):
        """
        Initialize an instance of the AutomationHandler class.

        Args:
            slack_api_token (str): The API token for Slack.
            slack_channel (str): The Slack channel to send messages to.
            homeautomation_webhook (str): The webhook URL for the home automation system.
            logger (Logger, optional): The logger to use. Defaults to LOGGER.
        """
        self.slack_api_token = slack_api_token
        self.slack_channel = slack_channel
        self.homeautomation_webhook = homeautomation_webhook
        self.logger = logger
        self.message: str = ""

    def _create_slack_message(
        self,
        http_request_dict: dict,
    ):
        """
        Create a Slack message based on the given HTTP request dictionary.

        Args:
            http_request_dict (dict): The HTTP request dictionary to create the Slack message from.
        """
        self.message = create_slack_message(
            http_request_dict=http_request_dict,
            logger=self.logger,
        )

    def _send_slack_message(self):
        """
        Send a Slack message using the Slack API token, channel, and message stored in this instance.
        """
        send_slack_message(
            slack_api_token=self.slack_api_token,
            channel=self.slack_channel,
            message=self.message,
            logger=self.logger,
        )

    def _send_request_to_homeautomation_webhook(self):
        """
        Send a request to the home automation webhook using the webhook URL and message stored in this instance.
        """
        send_request_to_homeautomation_webhook(
            homeautomation_webhook=self.homeautomation_webhook,
            message=self.message,
            logger=self.logger,
        )

    def handle_request(
        self,
        http_request_dict: dict,
    ):
        """
        Handle an HTTP request by creating a Slack message from the request dictionary,
        sending the Slack message, and sending a request to the home automation webhook.

        Args:
            http_request_dict (dict): The HTTP request dictionary to create the Slack message from.
        """
        self._create_slack_message(http_request_dict)
        self._send_slack_message()
        self._send_request_to_homeautomation_webhook()
