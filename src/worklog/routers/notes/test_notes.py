import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio
unknown_record_id = "1234567890abcdef1234abcd"


async def test_create_note(test_client: AsyncClient) -> None:
    """
    Test creating a new note record
    """
    r = await test_client.post("/api/v1/notes", json={"title": "my note item"})
    assert r.status_code == 200
    assert r.json().get("id")

    r = await test_client.post("/api/v1/notes", json={"invalidField": "foo"})
    assert r.status_code == 422

    r = await test_client.post("/api/v1/notes", json={"title": "my note item"})
    assert r.status_code == 200


async def test_get_notes(test_client: AsyncClient) -> None:
    """
    Test retrieving note records
    """
    r = await test_client.get("/api/v1/notes")
    assert r.status_code == 200
    resp = r.json()
    assert resp

    note_id = resp[0].get("id")
    r = await test_client.get(f"/api/v1/notes/{note_id}")
    assert r.status_code == 200

    # This record ID shouldn't exist
    r = await test_client.get(f"/api/v1/notes/{unknown_record_id}")
    assert r.status_code == 404


async def test_update_note(test_client: AsyncClient) -> None:
    """
    Test updating a note
    """
    # Get all notes
    r = await test_client.get("/api/v1/notes")
    assert r.status_code == 200
    results = r.json()
    assert results

    # Update a note
    note_id = results[0].get("id")
    r = await test_client.put(
        f"/api/v1/notes/{note_id}",
        json={"title": "my updated note task"},
    )
    assert r.status_code == 200

    r = await test_client.get(f"/api/v1/notes/{note_id}")
    assert r.status_code == 200
    assert r.json().get("title") == "my updated note task"

    # Unknown note ID
    r = await test_client.put(
        f"/api/v1/notes/{unknown_record_id}",
        json={"title": "my updated note task"},
    )
    assert r.status_code == 404


async def test_delete_note(test_client: AsyncClient) -> None:
    """
    Test deleting a note
    """
    # Get all notes
    r = await test_client.get("/api/v1/notes")
    assert r.status_code == 200
    results = r.json()
    assert results

    # Delete a note
    note_id = results[0].get("id")
    r = await test_client.delete(
        f"/api/v1/notes/{note_id}",
    )
    assert r.status_code == 200

    # Unknown note ID
    r = await test_client.delete(
        f"/v1/notes/{unknown_record_id}",
    )
    assert r.status_code == 404
