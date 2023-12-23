from logging import Logger, getLogger

import azure.functions as func

from hemera.exceptions import ValueNotFoundInDictError

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

    logger.debug(f"Converted HTTP request to dictionary: {http_request_dict}")

    return http_request_dict


def get_username_from_http_request_dict(
    http_request_dict: dict,
    logger: Logger = LOGGER,
) -> str:
    """
    Get the username from an HTTP request dictionary.

    Args:
        http_request_dict (dict): The HTTP request dictionary to get the username from.

    Returns:
        str: The username.
    """
    try:
        username = http_request_dict["body"]["sender"]["login"]
        logger.debug(f"Got username from HTTP request dictionary: {username}")
        return username
    except Exception as e:
        logger.error(f"Username not found in dictionary: {e}")
        raise ValueNotFoundInDictError from e
