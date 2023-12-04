from os import environ as os_environ
from unittest.mock import MagicMock, patch

import azure.functions as func

from github import main as github_api


def test_github_api_environment_variables_not_set(test_request: func.HttpRequest):
    test = github_api(req=test_request)
    assert test.get_body().decode() == "Error: Environment variable not set."
    assert test.status_code == 400


@patch("slack_sdk.web.client.WebClient.api_call")
def test_github_api_message_sent_to_slack_successfully(
    api_call: MagicMock,
    test_request: func.HttpRequest,
):
    os_environ["SLACK_API_TOKEN"] = "fake_token"
    os_environ["SLACK_CHANNEL"] = "fake_channel"

    test = github_api(req=test_request)

    api_call.assert_called_once_with(
        "chat.postMessage",
        json={
            "channel": "fake_channel",
            "text": "Action: reopened, Pull request URL: http://fakeurl.com, Pull request Number: 17",
        },
    )

    assert test.get_body().decode() == "Message sent to Slack successfully."
    assert test.status_code == 200

    os_environ.pop("SLACK_API_TOKEN", None)
    os_environ.pop("SLACK_CHANNEL", None)