import pytest

from hemera.exceptions import HemeraError
from hemera.homeautomation import run_homeautomation_webhook


def test_run_homeautomation_webhook_error() -> None:
    pytest.raises(
        HemeraError,
        run_homeautomation_webhook,
        homeautomation_webhook="http://fakeurl.com",
        message="Test message.",
    )
