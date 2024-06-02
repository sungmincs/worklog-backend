import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio
unknown_record_id = "1234567890abcdef1234abcd"


async def test_create_todo(test_client: AsyncClient) -> None:
    """
    Test creating a new todo record
    """
    r = await test_client.post(
        "/api/v1/todos", json={"title": "my todo item", "completed": True}
    )
    assert r.status_code == 200
    assert r.json().get("id")

    r = await test_client.post("/api/v1/todos", json={"completed": False})
    assert r.status_code == 422

    r = await test_client.post("/api/v1/todos", json={"title": "my todo item"})
    assert r.status_code == 200


async def test_get_todos(test_client: AsyncClient) -> None:
    """
    Test retrieving todo records
    """
    r = await test_client.get("/api/v1/todos")
    assert r.status_code == 200
    resp = r.json()
    assert resp

    todo_id = resp[0].get("id")
    r = await test_client.get(f"/api/v1/todos/{todo_id}")
    assert r.status_code == 200

    # This record ID shouldn't exist
    r = await test_client.get(f"/api/v1/todos/{unknown_record_id}")
    assert r.status_code == 404


async def test_update_todo(test_client: AsyncClient) -> None:
    """
    Test updating a todo
    """
    # Get all Todos
    r = await test_client.get("/api/v1/todos")
    assert r.status_code == 200
    results = r.json()
    assert results

    # Update a Todo
    todo_id = results[0].get("id")
    r = await test_client.put(
        f"/api/v1/todos/{todo_id}",
        json={"title": "my updated todo task", "completed": True},
    )
    assert r.status_code == 200

    # Unknown Todo ID
    r = await test_client.put(
        f"/api/v1/todos/{unknown_record_id}",
        json={"title": "my updated todo task", "completed": True},
    )
    assert r.status_code == 404


async def test_delete_todo(test_client: AsyncClient) -> None:
    """
    Test deleting a todo
    """
    # Get all Todos
    r = await test_client.get("/api/v1/todos")
    assert r.status_code == 200
    results = r.json()
    assert results

    # Delete a Todo
    todo_id = results[0].get("id")
    r = await test_client.delete(
        f"/api/v1/todos/{todo_id}",
    )
    assert r.status_code == 200

    # Unknown Todo ID
    r = await test_client.delete(
        f"/v1/todos/{unknown_record_id}",
    )
    assert r.status_code == 404
