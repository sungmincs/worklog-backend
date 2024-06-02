from datetime import datetime

from pydantic import BaseModel


class Note(BaseModel):
    title: str


class NoteId(BaseModel):
    id: str


class NoteRecord(NoteId, Note):
    created_date: datetime
    updated_date: datetime
