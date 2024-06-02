import os

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_healthcheck(test_client: AsyncClient) -> None:
    """
    Test health endpoint
    """
    r = await test_client.get("/health")
    assert r.status_code == 200
    assert r.json().get("health") == "OK"

    os.environ["IMAGE_TAG"] = "my-awesome-version"
    r = await test_client.get("/health")
    assert r.json().get("imageTag") == "my-awesome-version"
