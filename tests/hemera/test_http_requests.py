import azure.functions as func

from hemera.http_request_handler import (
    convert_http_request_body_to_dict,
    convert_http_request_headers_to_dict,
    convert_http_request_to_dict,
)


def test_get_http_request_headers(test_request: func.HttpRequest) -> None:
    assert convert_http_request_headers_to_dict(req=test_request) == {
        "x-forwarded-proto": "http",
        "content-type": "application/json",
    }


def test_convert_http_request_body_to_dict(test_request: func.HttpRequest) -> None:
    assert convert_http_request_body_to_dict(req=test_request) == {
        "action": "opened",
        "number": 1,
        "pull_request": {"url": "http://fakeurl.com", "id": 123456789},
    }


def test_convert_http_request_to_dict(test_request: func.HttpRequest) -> None:
    assert convert_http_request_to_dict(req=test_request) == {
        "header": {"x-forwarded-proto": "http", "content-type": "application/json"},
        "body": {
            "action": "opened",
            "number": 1,
            "pull_request": {"url": "http://fakeurl.com", "id": 123456789},
        },
    }
