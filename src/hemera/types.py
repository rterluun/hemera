from logging import Logger, getLogger

from hemera.datatypes import HttpRequest
from hemera.exceptions import ValueNotFoundInHemeraHttpRequest
from hemera.http_request_handler import convert_http_request

LOGGER = getLogger(__name__)


class HemeraHttpRequest:
    """A class to represent a Hemera HTTP request."""

    def __init__(
        self,
        req: HttpRequest = HttpRequest(header={}, body={}),
    ):
        """Initialize an instance of the HemeraHttpRequest class."""
        self.req = req

    @classmethod
    def from_azure_functions_http_request(
        cls,
        req,
        logger: Logger = LOGGER,
    ):
        """Create an instance of the HemeraHttpRequest class from an Azure Functions HTTP request."""
        return cls(
            req=convert_http_request(
                req=req,
                logger=logger,
            ),
        )

    @property
    def username(self):
        """Return the username of the user who performed the action."""

        try:
            return self.req.body["sender"]["login"]
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e

    @property
    def action(self):
        """Return the action performed on the repository."""
        try:
            return self.req.body["action"]
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e

    @property
    def repository(self):
        """Return the repository name."""
        try:
            return self.req.body["repository"]["full_name"]
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e
