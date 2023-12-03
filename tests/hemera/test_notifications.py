from unittest.mock import patch, MagicMock
import pytest

from hemera.exceptions import HemeraError

from hemera.notifications import (
    send_slack_message,
    convert_http_request_dict_to_slack_message,
)


@patch("slack_sdk.web.client.WebClient.api_call")
def test_send_slack_message(
    api_call=MagicMock(),
    channel: str = "#channel_name",
    message: str = "some message",
):
    send_slack_message(
        slack_api_token="",
        channel=channel,
        message=message,
    )

    api_call.assert_called_once_with(
        "chat.postMessage", json={"channel": channel, "text": message}
    )


def test_send_slack_message_error():
    pytest.raises(
        HemeraError, send_slack_message, slack_api_token="", channel="", message=""
    )


def test_convert_http_request_dict_to_slack_message(http_request_dict):
    assert (
        convert_http_request_dict_to_slack_message(
            http_request_dict=http_request_dict,
        )
        == "Action: reopened, Pull request URL: http://fakeurl.com, Pull request Number: 17"
    )


def test_convert_http_request_dict_to_slack_message_error():
    pytest.raises(
        HemeraError,
        convert_http_request_dict_to_slack_message,
        http_request_dict={},
    )
