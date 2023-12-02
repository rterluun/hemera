from logging import getLogger, Logger
import azure.functions as func
from typing import Literal

LOGGER = getLogger(__name__)


def convert_http_request_headers_to_dict(req: func.HttpRequest) -> dict:
    """Convert an Azure Functions HTTP request's headers to a dictionary."""
    return dict(req.headers)


def convert_http_request_body_to_dict(req: func.HttpRequest) -> dict:
    """Convert an Azure Functions HTTP request's body to a dictionary."""
    return dict(req.get_json())


def convert_http_request_to_dict(
    req: func.HttpRequest,
    logger: Logger = LOGGER,
) -> dict:
    """Convert an Azure Functions HTTP request to a dictionary."""

    http_request_dict = {
        "header": convert_http_request_headers_to_dict(req=req),
        "body": convert_http_request_body_to_dict(req=req),
    }

    logger.info(f"Converted HTTP request to dictionary: {http_request_dict}")

    return http_request_dict


def get_value_from_http_request_dict(
    http_request_dict: dict,
    key: Literal["header", "body"],
    prop: str,
    logger: Logger = LOGGER,
) -> str:
    """Get a value from an Azure Functions HTTP request dictionary."""
    logger.info(f"Getting value for key {key} and property {prop}")

    try:
        return http_request_dict[key][prop]
    except KeyError:
        logger.info(f"Key {key} not found in HTTP request dictionary")
        raise KeyError(f"Key {key} not found in HTTP request dictionary")
