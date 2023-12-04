import json

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
