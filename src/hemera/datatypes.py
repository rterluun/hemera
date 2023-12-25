from dataclasses import dataclass
from typing import Dict


@dataclass
class HttpRequest:
    """Dataclass for HTTP request data."""

    header: Dict[str, str]
    body: Dict[str, object]


@dataclass
class Metadata:
    """Dataclass for Hemera metadata."""

    python: Dict[str, str]
