import pytest

from hemera.exceptions import HemeraError
from hemera.types import HemeraHttpRequest, HemeraMetadata


def test_hemera_http_request_exceptions():
    http_request = HemeraHttpRequest()

    with pytest.raises(HemeraError, match="Value not found in HemeraHttpRequest."):
        _ = http_request.username

    with pytest.raises(HemeraError, match="Value not found in HemeraHttpRequest."):
        _ = http_request.action

    with pytest.raises(HemeraError, match="Value not found in HemeraHttpRequest."):
        _ = http_request.repository


def test_hemera_meta_data_exceptions():
    hemera_meta_data = HemeraMetadata()

    with pytest.raises(HemeraError, match="Value not found in HemeraMetadata."):
        _ = hemera_meta_data.core
