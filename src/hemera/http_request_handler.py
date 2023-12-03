from logging import getLogger, Logger
import azure.functions as func

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
