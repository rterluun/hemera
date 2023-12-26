from unittest.mock import MagicMock, patch

import pytest

from hemera.exceptions import HemeraError
from hemera.handlers import AutomationHandler
from hemera.types import HemeraHttpRequest


@patch("slack_sdk.web.client.WebClient.api_call")
def test_automation_handler_exceptions(api_call=MagicMock()):
    """Test AutomationHandler exceptions."""
    handler = AutomationHandler(
        slack_api_token={},
        slack_channel="",
        homeautomation_webhook="http://fakeurl.com",
    )
    handler.message = "Test message."

    with pytest.raises(HemeraError, match="Error in AutomationHandler class."):
        handler._create_slack_message(hemera_http_request=HemeraHttpRequest())

    with pytest.raises(HemeraError, match="Error in AutomationHandler class."):
        handler._send_slack_message()

    with pytest.raises(HemeraError, match="Error in AutomationHandler class."):
        handler._send_request_to_homeautomation_webhook()

    api_call.assert_not_called()
