from logging import Logger, getLogger

import azure.functions as func

from hemera.datatypes import HttpRequest

LOGGER = getLogger(__name__)


def convert_http_request_headers(req: func.HttpRequest) -> dict:
    """Convert an Azure Functions HTTP request's headers to a dictionary."""
    return dict(req.headers)


def convert_http_request_body(req: func.HttpRequest) -> dict:
    """Convert an Azure Functions HTTP request's body to a dictionary."""
    return dict(req.get_json())


def convert_http_request(
    req: func.HttpRequest,
    logger: Logger = LOGGER,
) -> HttpRequest:
    """Convert an Azure Functions HTTP request to a hemera.types.HttpRequest dictionary."""

    http_request = HttpRequest(
        header=convert_http_request_headers(req=req),
        body=convert_http_request_body(req=req),
    )

    logger.debug(f"Converted HTTP request to dictionary: {http_request}")

    return http_request
