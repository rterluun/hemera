import json
from os import environ as os_environ

import azure.functions as func
import pytest

from tests.hemera.resources.http_request_data import BODY, HEADER


@pytest.fixture
def test_request():
    return func.HttpRequest(
        method="POST",
        url="http://fakeurl.com",
        headers=HEADER,
        params={},
        route_params={},
        body=json.dumps(BODY).encode("utf-8"),
    )


@pytest.fixture
def http_request_dict():
    return {"header": HEADER, "body": BODY}


@pytest.fixture(autouse=True)
def set_env_vars():
    os_environ["SLACK_API_TOKEN"] = "fake_token"
    os_environ["SLACK_CHANNEL"] = "fake_channel"
    os_environ["HOMEAUTOMATION_WEBHOOK"] = "http://fakeurl.com"
    os_environ["ALLOWED_USERNAME"] = "username"

    yield

    os_environ.pop("SLACK_API_TOKEN", None)
    os_environ.pop("SLACK_CHANNEL", None)
    os_environ.pop("HOMEAUTOMATION_WEBHOOK", None)
    os_environ.pop("ALLOWED_USERNAME", None)
