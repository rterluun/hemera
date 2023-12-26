from logging import Logger, getLogger

import azure.functions as func

from hemera.dataclasses import HttpRequest

LOGGER = getLogger(__name__)


def convert_http_request_headers(req: func.HttpRequest) -> dict:
    """Convert an Azure Functions HTTP request's headers to a dictionary.

    Args:
        req (func.HttpRequest): The Azure Functions HTTP request.

    Returns:
        dict: The Azure Functions HTTP request's headers as a dictionary.
    """
    return dict(req.headers)


def convert_http_request_body(req: func.HttpRequest) -> dict:
    """Convert an Azure Functions HTTP request's body to a dictionary.

    Args:
        req (func.HttpRequest): The Azure Functions HTTP request.

    Returns:
        dict: The Azure Functions HTTP request's body as a dictionary.
    """
    return dict(req.get_json())


def convert_http_request(
    req: func.HttpRequest,
    logger: Logger = LOGGER,
) -> HttpRequest:
    """Convert an Azure Functions HTTP request to a dictionary.

    Args:
        req (func.HttpRequest): The Azure Functions HTTP request.
        logger (Logger, optional): The logger. Defaults to LOGGER.

    Returns:
        HttpRequest: The Azure Functions HTTP request as a HttpRequest dataclass.
    """

    http_request = HttpRequest(
        header=convert_http_request_headers(req=req),
        body=convert_http_request_body(req=req),
    )

    logger.debug(f"Converted HTTP request to dictionary: {http_request}")

    return http_request
