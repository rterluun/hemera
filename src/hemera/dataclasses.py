from dataclasses import dataclass
from typing import Dict


@dataclass
class HttpRequest:
    """Dataclass for Hemera HTTP request."""

    header: Dict[str, str]
    body: Dict[str, object]


@dataclass
class PythonVersion:
    """Dataclass for Python versions."""

    package: Dict[str, str]


@dataclass
class Metadata:
    """Dataclass for Hemera metadata."""

    python: PythonVersion


@dataclass
class DeprecatedEnvirionmentVariable:
    """Dataclass for deprecated environment variables."""

    name: str
    deprecated_in_hemera_version: str
    replacement: str
