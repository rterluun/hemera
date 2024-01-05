from logging import Logger, getLogger
from os import environ as os_environ

from hemera.dataclasses import DeprecatedEnvirionmentVariable
from hemera.exceptions import EnvironmentVariableDeprecatedError
from hemera.metadata import get_software_versions

DEPRECATEDENVIRIONMENTVARIABLES = [
    DeprecatedEnvirionmentVariable(
        name="ALLOWED_USERNAME",
        deprecated_in_hemera_version="2.0.0",
        replacement="PR_AUTHOR_FILTER",
    )
]

LOGGER = getLogger(__name__)


def scan_for_deprecated_env_vars(
    deprecated_env_vars: list, logger: Logger = LOGGER
) -> None:
    """Scan for deprecated environment variables.

    Args:
        deprecated_env_vars (list): The deprecated environment variables.
        logger (Logger, optional): The logger. Defaults to LOGGER.

    Raises:
        EnvironmentVariableDeprecatedError: Raised when an environment variable is deprecated.
    """

    hemera_version = get_software_versions(distribution="hemera").package["hemera"]

    for envirionment_variable in deprecated_env_vars:
        if envirionment_variable.name in os_environ:
            logger.warning(
                f"The environment variable {envirionment_variable.name} "
                f"is deprecated in Hemera {envirionment_variable.deprecated_in_hemera_version} "
                f"You should use {envirionment_variable.replacement} instead."
            )
            if hemera_version >= envirionment_variable.deprecated_in_hemera_version:
                raise EnvironmentVariableDeprecatedError(
                    env_var_name=envirionment_variable.name
                )
