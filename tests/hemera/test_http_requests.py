import azure.functions as func

from hemera.http_request_handler import (
    convert_http_request_body_to_dict,
    convert_http_request_headers_to_dict,
    convert_http_request_to_dict,
    get_username_from_http_request_dict,
)
from tests.hemera.resources.http_request_data import BODY, HEADER


def test_get_http_request_headers(test_request: func.HttpRequest) -> None:
    assert convert_http_request_headers_to_dict(req=test_request) == HEADER


def test_convert_http_request_body_to_dict(test_request: func.HttpRequest) -> None:
    assert convert_http_request_body_to_dict(req=test_request) == BODY


def test_convert_http_request_to_dict(test_request: func.HttpRequest) -> None:
    assert convert_http_request_to_dict(req=test_request) == {
        "header": HEADER,
        "body": BODY,
    }


def test_get_username_from_http_request_dict(http_request_dict: dict) -> None:
    assert (
        get_username_from_http_request_dict(http_request_dict=http_request_dict)
        == "username"
    )
