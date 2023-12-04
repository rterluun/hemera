from os import environ as os_environ
from unittest.mock import patch, MagicMock
import azure.functions as func
from github import main as github_api


def test_github_api_environment_variables_not_set():
    test = github_api(
        req=func.HttpRequest(
            method="POST",
            url="fake_url",
            headers={},
            params={},
            route_params={},
            body=b"fake_body",
        )
    )
    assert test.get_body().decode() == "Error: Environment variable not set."
    assert test.status_code == 400


@patch("slack_sdk.web.client.WebClient.api_call")
def test_github_api_message_sent_to_slack_successfully(api_call: MagicMock):
    os_environ["SLACK_API_TOKEN"] = "fake_token"
    os_environ["SLACK_CHANNEL"] = "fake_channel"

    test = github_api(
        req=func.HttpRequest(
            method="POST",
            url="fake_url",
            headers={},
            params={},
            route_params={},
            body=b'{"action": "fake_action", "pull_request": {"html_url": "fake_url", "number": "fake_number"}}',
        )
    )

    api_call.assert_called_once_with(
        "chat.postMessage",
        json={
            "channel": "fake_channel",
            "text": "Action: fake_action, Pull request URL: fake_url, Pull request Number: fake_number",
        },
    )

    assert test.get_body().decode() == "Message sent to Slack successfully."
    assert test.status_code == 200

    os_environ.pop("SLACK_API_TOKEN", None)
    os_environ.pop("SLACK_CHANNEL", None)
