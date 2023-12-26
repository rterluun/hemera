from logging import Logger, getLogger

from hemera.dataclasses import HttpRequest, Metadata, PythonVersion
from hemera.exceptions import (
    ValueNotFoundInHemeraHttpRequest,
    ValueNotFoundInHemeraMetadata,
)
from hemera.http_request_handler import convert_http_request
from hemera.metadata import get_software_versions

LOGGER = getLogger(__name__)


class HemeraMetadata:
    """A class to represent Hemera metadata."""

    def __init__(self, versions: Metadata = Metadata(python=PythonVersion(package={}))):
        """Initialize an instance of the HemeraMetadata class.

        Args:
            versions (Metadata, optional): The versions. Defaults to Metadata(python=PythonVersion(package={})).
        """
        self.versions: Metadata = versions

    @classmethod
    def _from_runtime(cls) -> "HemeraMetadata":
        """Create an instance of the HemeraMetadata class from the runtime.

        Returns:
            HemeraMetadata: An instance of the HemeraMetadata class.
        """
        return cls(versions=Metadata(get_software_versions("hemera")))

    @property
    def core(self) -> str:
        """Return the version of the Hemera core package.

        Raises:
            ValueNotFoundInHemeraMetadata: When the version of the Hemera core package is not found.

        Returns:
            str: The version of the Hemera core package.
        """
        try:
            return self.versions.python.package["hemera"]
        except KeyError as e:
            raise ValueNotFoundInHemeraMetadata from e


class HemeraHttpRequest:
    """A class to represent a Hemera HTTP request."""

    def __init__(
        self,
        req: HttpRequest = HttpRequest(header={}, body={}),
    ):
        """Initialize an instance of the HemeraHttpRequest class."""
        self.req = req
        self.metadata = HemeraMetadata._from_runtime()

    @classmethod
    def from_azure_functions_http_request(
        cls,
        req,
        logger: Logger = LOGGER,
    ):
        """Create an instance of the HemeraHttpRequest class from an Azure
        Functions HTTP request."""
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
