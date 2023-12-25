from importlib.metadata import version

from hemera.exceptions import SoftwareVerionsNotFoundError


def get_software_versions(distribution):
    """Return the version of the software."""
    try:
        return {distribution: version(distribution)}
    except Exception as e:
        raise SoftwareVerionsNotFoundError from e
