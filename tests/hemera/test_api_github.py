import json
from os import environ as os_environ
from unittest.mock import MagicMock, patch

import azure.functions as func
import requests_mock

from github import main as github_api


def test_github_api_environment_variables_not_set(test_request: func.HttpRequest):
    """Test github_api when environment variables are not set."""
    os_environ.pop("SLACK_API_TOKEN", None)

    test = github_api(req=test_request)
    assert test.get_body().decode() == "Error: Environment variable not set."
    assert test.status_code == 400


def test_github_api_value_not_found():
    """Test github_api when a value is not found in a dictionary."""
    test = github_api(
        req=func.HttpRequest(
            method="POST",
            url="/",
            headers={},
            params={},
            route_params={},
            body=json.dumps({}).encode("utf-8"),
        )
    )

    assert test.get_body().decode() == "Error: Value not found in HemeraHttpRequest."
    assert test.status_code == 400


@patch("slack_sdk.web.client.WebClient.api_call")
def test_github_api_message_sent_to_slack_successfully(
    api_call: MagicMock,
    test_request: func.HttpRequest,
):
    """Test github_api when the message is sent to Slack successfully."""
    with requests_mock.Mocker() as m:
        m.post("http://fakeurl.com", text="OK")

        test = github_api(req=test_request)

        api_call.assert_called_once_with(
            "chat.postMessage",
            json={
                "channel": "fake_channel",
                "text": (
                    "username reopened a pull_request\n"
                    "<http://fakeurl.com|17: PR title>\n"
                    "Target branch: master; Source branch: branch_name\n"
                    "Repository: username/repository_name\n"
                    "Created by Hemera v0.0.0"
                ),
            },
        )

        assert test.get_body().decode() == "Automation executed successfully."
        assert test.status_code == 200


def test_github_api_username_not_allowed(test_request: func.HttpRequest):
    """Test github_api when the username is not allowed."""
    os_environ["PR_AUTHOR_FILTER"] = "fake_username"

    test = github_api(req=test_request)
    assert test.get_body().decode() == "Error: Unauthorized user."
    assert test.status_code == 400


def test_github_event_not_supported_error(incorrect_github_event_header: dict):
    """Test github_api when the event is not supported."""
    test = github_api(
        req=func.HttpRequest(
            method="POST",
            url="/",
            headers=incorrect_github_event_header,
            params={},
            route_params={},
            body=json.dumps({}).encode("utf-8"),
        )
    )
    assert test.get_body().decode() == "Error: GitHub event not supported."
    assert test.status_code == 400
