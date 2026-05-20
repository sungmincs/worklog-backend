import pytest
from httpx import ASGITransport, AsyncClient

from worklog.main import app


@pytest.fixture()
def test_client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test", follow_redirects=True)
