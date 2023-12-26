from importlib.metadata import version

from hemera.dataclasses import PythonVersion
from hemera.exceptions import SoftwareVerionsNotFoundError


def get_software_versions(distribution: str) -> PythonVersion:
    """Get the software versions.

    Args:
        distribution (str): The distribution.

    Raises:
        SoftwareVerionsNotFoundError: When the software versions are not found.

    Returns:
        PythonVersion: The software versions.
    """
    try:
        return PythonVersion(package={distribution: version(distribution)})
    except Exception as e:
        raise SoftwareVerionsNotFoundError from e
