import pytest

from hemera.exceptions import HemeraError
from hemera.homeautomation import send_request_to_homeautomation_webhook


def test_send_request_to_homeautomation_webhook_error() -> None:
    pytest.raises(
        HemeraError,
        send_request_to_homeautomation_webhook,
        homeautomation_webhook="http://fakeurl.com",
        message="Test message.",
    )
