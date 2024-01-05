from logging import Logger, getLogger
from typing import Any, List

import azure.functions as func

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
        """Initialize an instance of the HemeraHttpRequest class.

        Args:
            req (HttpRequest, optional): The HTTP request. Defaults to HttpRequest(header={}, body={}).
        """
        self.req = req
        self.metadata = HemeraMetadata._from_runtime()

    @classmethod
    def from_azure_functions_http_request(
        cls,
        req: func.HttpRequest,
        logger: Logger = LOGGER,
    ) -> "HemeraHttpRequest":
        """Create an instance of the HemeraHttpRequest class from an Azure
        Functions HTTP request.

        Args:
            req (func.HttpRequest): The Azure Functions HTTP request.
            logger (Logger, optional): The logger. Defaults to LOGGER.

        Returns:
            HemeraHttpRequest: An instance of the HemeraHttpRequest class.
        """
        return cls(
            req=convert_http_request(
                req=req,
                logger=logger,
            ),
        )

    def _get_property_value(self, source: str, keys: List[str]) -> Any:
        """Return the value of a property.

        Args:
            source (str): The source of the property. Either "header" or "body".
            keys (List[str]): The keys to access the property.

        Raises:
            ValueNotFoundInHemeraHttpRequest: When the value of the property is not found.

        Returns:
            Any: The value of the property.
        """
        try:
            value = getattr(self.req, source)
            for key in keys:
                value = value[key]
            return value
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e

    @property
    def username(self) -> str:
        """Return the username."""
        return self._get_property_value(
            source="body", keys=["pull_request", "user", "login"]
        )
        # Fields that contains a username:
        # body["pull_request"]["user"]["login"]
        # body["pull_request"]["head"]["user"]["login"]
        # body["pull_request"]["head"]["repo"]["owner"]["login"]
        # body["pull_request"]["base"]["user"]["login"]
        # body["pull_request"]["base"]["repo"]["owner"]["login"]
        # body["repository"]["owner"]["login"]
        # body["sender"]["login"]

    @property
    def action(self) -> object:
        """Return the action."""
        return self._get_property_value(source="body", keys=["action"])

    @property
    def repository(self) -> str:
        """Return the repository name."""
        return self._get_property_value(source="body", keys=["repository", "full_name"])
        # Fields that contains a repository name:
        # body["pull_request"]["head"]["repo"]["full_name"]
        # body["pull_request"]["base"]["repo"]["full_name"]
        # body["repository"]["full_name"]

    @property
    def githubevent(self) -> str:
        """Return the GitHub event."""
        return self._get_property_value(source="header", keys=["x-github-event"])

    @property
    def pullrequesturl(self) -> str:
        """Return the pull request URL."""
        return self._get_property_value(
            source="body", keys=["pull_request", "html_url"]
        )

    @property
    def pullrequestnumber(self) -> str:
        """Return the pull request number."""
        return self._get_property_value(source="body", keys=["pull_request", "number"])
        # Fields that contains a pull request number:
        # body["pull_request"]["number"]
        # body["number"]

    @property
    def pullrequesttitle(self) -> str:
        """Return the pull request title."""
        return self._get_property_value(source="body", keys=["pull_request", "title"])

    @property
    def pullrequesttargetbranch(self) -> str:
        """Return the pull request target branch."""
        return self._get_property_value(
            source="body", keys=["pull_request", "base", "ref"]
        )

    @property
    def pullrequestsourcebranch(self) -> str:
        """Return the pull request source branch."""
        return self._get_property_value(
            source="body", keys=["pull_request", "head", "ref"]
        )
