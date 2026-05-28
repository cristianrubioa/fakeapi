import pytest

from fakeapi.common.limiter import limiter
from fakeapi.storage import storage


@pytest.fixture(scope="session", autouse=True)
def disable_rate_limits():
    limiter.enabled = False
    yield
    limiter.enabled = True


@pytest.fixture(autouse=True)
def reset_storage():
    storage.clear()
    yield
