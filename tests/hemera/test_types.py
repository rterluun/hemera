import pytest

from hemera.exceptions import HemeraError
from hemera.types import HemeraHttpRequest, HemeraMetadata


def test_hemera_http_request_exceptions():
    """Test HemeraHttpRequest exceptions."""
    http_request = HemeraHttpRequest()

    with pytest.raises(HemeraError, match="Value not found in HemeraHttpRequest."):
        _ = http_request.username

    with pytest.raises(HemeraError, match="Value not found in HemeraHttpRequest."):
        _ = http_request.action

    with pytest.raises(HemeraError, match="Value not found in HemeraHttpRequest."):
        _ = http_request.repository

    with pytest.raises(HemeraError, match="Value not found in HemeraHttpRequest."):
        _ = http_request.pullrequesturl

    with pytest.raises(HemeraError, match="Value not found in HemeraHttpRequest."):
        _ = http_request.pullrequestnumber

    with pytest.raises(HemeraError, match="Value not found in HemeraHttpRequest."):
        _ = http_request.pullrequesttitle

    with pytest.raises(HemeraError, match="Value not found in HemeraHttpRequest."):
        _ = http_request.pullrequesttargetbranch

    with pytest.raises(HemeraError, match="Value not found in HemeraHttpRequest."):
        _ = http_request.pullrequestsourcebranch


def test_hemera_meta_data_exceptions():
    """Test HemeraMetadata exceptions."""
    hemera_meta_data = HemeraMetadata()

    with pytest.raises(HemeraError, match="Value not found in HemeraMetadata."):
        _ = hemera_meta_data.core
