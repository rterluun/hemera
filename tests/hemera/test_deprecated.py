from os import environ as os_environ

import pytest

from hemera.dataclasses import DeprecatedEnvirionmentVariable
from hemera.deprecated import scan_for_deprecated_env_vars
from hemera.exceptions import HemeraError


def test_scan_for_deprecated_env_vars():
    os_environ["DEPRECATED_ENV_VAR"] = "test"

    with pytest.raises(
        HemeraError, match="Environment variable DEPRECATED_ENV_VAR is deprecated."
    ):
        scan_for_deprecated_env_vars(
            deprecated_env_vars=[
                DeprecatedEnvirionmentVariable(
                    name="DEPRECATED_ENV_VAR",
                    deprecated_in_hemera_version="0.0.0",
                    replacement="NEW_ENV_VAR",
                )
            ]
        )

    os_environ.pop("DEPRECATED_ENV_VAR", None)
