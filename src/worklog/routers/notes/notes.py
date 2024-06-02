from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path

from worklog.db import MONGO_ID_REGEX, db
from worklog.models import NotFoundException

from .models import Note, NoteId, NoteRecord

router = APIRouter()


@router.post("", response_model=NoteId)
async def create_note(payload: Note) -> NoteId:
    """
    Create a new note record
    """
    now = datetime.now(timezone.utc)
    insert_result = await db.notes.insert_one(
        {
            "title": payload.title,
            "created_date": now,
            "updated_date": now,
        }
    )

    return NoteId(id=str(insert_result.inserted_id))


@router.get("", response_model=list[NoteRecord])
async def get_notes() -> list[NoteRecord]:
    """
    Get all note records
    """
    notes: list[NoteRecord] = []
    async for record in db.notes.find():
        notes.append(
            NoteRecord(
                id=str(record["_id"]),
                title=record["title"],
                created_date=record["created_date"],
                updated_date=record["updated_date"],
            )
        )
    return notes


@router.get(
    "/{id}",
    response_model=NoteRecord,
    responses={
        404: {"description": "Note Record Not Found", "model": NotFoundException},
    },
)
async def get_note(
    id: str = Path(description="Note ID", pattern=MONGO_ID_REGEX)
) -> NoteRecord:
    """
    Get a single note record
    """
    record = await db.notes.find_one({"_id": ObjectId(id)})

    if record is None:
        raise HTTPException(status_code=404, detail="Record Not Found")

    return NoteRecord(
        id=str(record["_id"]),
        title=record["title"],
        created_date=record["created_date"],
        updated_date=record["updated_date"],
    )


@router.put(
    "/{id}",
    response_model=NoteId,
    responses={
        404: {"description": "Note Record Not Found", "model": NotFoundException},
    },
)
async def update_notes(
    payload: Note,
    id: str = Path(description="Note ID", pattern=MONGO_ID_REGEX),
) -> NoteId:
    """
    Update a single note record
    """
    now = datetime.now(timezone.utc)
    update_result = await db.notes.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "title": payload.title,
                "updated_date": now,
            }
        },
    )
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Record Not Found")

    return NoteId(id=id)


@router.delete(
    "/{id}",
    response_model=bool,
    responses={
        404: {"description": "Note Record Not Found", "model": NotFoundException},
    },
)
async def delete_note(
    id: str = Path(description="Note ID", pattern=MONGO_ID_REGEX),
) -> bool:
    """
    Delete a single note record
    """
    delete_result = await db.notes.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record Not Found")

    return True
