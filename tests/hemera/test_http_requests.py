import azure.functions as func

from hemera.datatypes import HttpRequest
from hemera.http_request_handler import (
    convert_http_request,
    convert_http_request_body,
    convert_http_request_headers,
)
from tests.hemera.resources.http_request_data import BODY, HEADER


def test_get_http_request_headers(test_request: func.HttpRequest) -> None:
    assert convert_http_request_headers(req=test_request) == HEADER


def test_convert_http_request_body(test_request: func.HttpRequest) -> None:
    assert convert_http_request_body(req=test_request) == BODY


def test_convert_http_request(test_request: func.HttpRequest) -> None:
    assert convert_http_request(req=test_request) == HttpRequest(
        header=HEADER, body=BODY
    )
