from unittest.mock import patch, MagicMock

from hemera.notifications import send_slack_message


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
    response = send_slack_message(
        slack_api_token="invalid_token",
        channel="#channel_name",
        message="some message",
    )

    assert response is None
