from logging import Logger, getLogger

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

    @property
    def username(self) -> str:
        """Return the username of the user who performed the action on the
        repository.

        Raises:
            ValueNotFoundInHemeraHttpRequest: When the username of the user
                who performed the action on the repository is not found.

        Returns:
            str: The username of the user who performed the action on the repository.
        """
        try:
            body: dict = self.req.body
            return body["pull_request"]["user"]["login"]
            # Fields that contains a username:
            # body["pull_request"]["user"]["login"]
            # body["pull_request"]["head"]["user"]["login"]
            # body["pull_request"]["head"]["repo"]["owner"]["login"]
            # body["pull_request"]["base"]["user"]["login"]
            # body["pull_request"]["base"]["repo"]["owner"]["login"]
            # body["repository"]["owner"]["login"]
            # body["sender"]["login"]
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e

    @property
    def action(self) -> object:
        """Return the action performed on the repository.

        Raises:
            ValueNotFoundInHemeraHttpRequest: When the action performed on the repository is not found.

        Returns:
            object: The action performed on the repository.
        """
        try:
            body: dict = self.req.body
            return body["action"]
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e

    @property
    def repository(self) -> str:
        """Return the full name of the repository.

        Raises:
            ValueNotFoundInHemeraHttpRequest: When the full name of the repository is not found.

        Returns:
            str: The full name of the repository.
        """
        try:
            body: dict = self.req.body
            return body["repository"]["full_name"]
            # Fields that contains a repository name:
            # body["pull_request"]["head"]["repo"]["full_name"]
            # body["pull_request"]["base"]["repo"]["full_name"]
            # body["repository"]["full_name"]
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e

    @property
    def githubevent(self) -> str:
        """Return the GitHub event type.

        Raises:
            ValueNotFoundInHemeraHttpRequest: When the GitHub event type is not found.

        Returns:
            str: The GitHub event type.
        """
        try:
            header: dict = self.req.header
            return header["x-github-event"]
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e

    @property
    def pullrequesturl(self) -> str:
        """Return the pull request URL.

        Raises:
            ValueNotFoundInHemeraHttpRequest: When the pull request URL is not found.

        Returns:
            str: The pull request URL.
        """
        try:
            body: dict = self.req.body
            return body["pull_request"]["html_url"]
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e

    @property
    def pullrequestnumber(self) -> str:
        """Return the pull request number.

        Raises:
            ValueNotFoundInHemeraHttpRequest: When the pull request number is not found.

        Returns:
            str: The pull request number.
        """
        try:
            body: dict = self.req.body
            return body["pull_request"]["number"]
            # Fields that contains a pull request number:
            # body["pull_request"]["number"]
            # body["number"]
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e

    @property
    def pullrequesttitle(self) -> str:
        """Return the pull request title.

        Raises:
            ValueNotFoundInHemeraHttpRequest: When the pull request title is not found.

        Returns:
            str: The pull request title.
        """
        try:
            body: dict = self.req.body
            return body["pull_request"]["title"]
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e

    @property
    def pullrequesttargetbranch(self) -> str:
        """Return the pull request target branch.

        Raises:
            ValueNotFoundInHemeraHttpRequest: When the pull request target branch is not found.

        Returns:
            str: The pull request target branch.
        """
        try:
            body: dict = self.req.body
            return body["pull_request"]["base"]["ref"]
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e

    @property
    def pullrequestsourcebranch(self) -> str:
        """Return the pull request source branch.

        Raises:
            ValueNotFoundInHemeraHttpRequest: When the pull request source branch is not found.

        Returns:
            str: The pull request source branch.
        """
        try:
            body: dict = self.req.body
            return body["pull_request"]["head"]["ref"]
        except KeyError as e:
            raise ValueNotFoundInHemeraHttpRequest from e
