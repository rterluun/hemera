from unittest.mock import MagicMock, patch

import pytest

from hemera.exceptions import HemeraError
from hemera.slack import create_slack_message, send_slack_message
from hemera.types import HemeraHttpRequest


@patch("slack_sdk.web.client.WebClient.api_call")
def test_send_slack_message(
    api_call=MagicMock(),
    channel: str = "#channel_name",
    message: str = "some message",
):
    """Test send_slack_message."""
    send_slack_message(
        slack_api_token="",
        channel=channel,
        message=message,
    )

    api_call.assert_called_once_with(
        "chat.postMessage", json={"channel": channel, "text": message}
    )


@patch("slack_sdk.web.client.WebClient.api_call")
def test_send_slack_message_error(api_call=MagicMock()):
    """Test send_slack_message error."""
    with pytest.raises(HemeraError, match="Error sending message to Slack."):
        _ = send_slack_message(slack_api_token={}, channel="", message="")

    api_call.assert_not_called()


def test_create_slack_message(hemera_http_request):
    """Test create_slack_message."""
    expected_message = (
        "username reopened a pull_request\n"
        "<http://fakeurl.com|17: PR title>\n"
        "Target branch: master; Source branch: branch_name\n"
        "Repository: username/repository_name\n"
        "Created by Hemera v0.0.0"
    )
    assert (
        create_slack_message(hemera_http_request=hemera_http_request)
        == expected_message
    )


def test_create_slack_message_error():
    """Test create_slack_message error."""
    pytest.raises(
        HemeraError,
        create_slack_message,
        hemera_http_request=HemeraHttpRequest(),
    )
