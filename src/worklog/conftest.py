import pytest
from httpx import AsyncClient

from worklog.main import app


@pytest.fixture()
def test_client() -> AsyncClient:
    """
    Create an instance of the client
    """
    return AsyncClient(app=app, base_url="http://test", follow_redirects=True)
