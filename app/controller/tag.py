from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.configuration.database import get_db

import app.service.tag

ROUTER = APIRouter()


class InputTag(BaseModel):
    userid: int
    document_id: int
    name: str

@ROUTER.post('/')
def all_documents(tag:InputTag, db: Session = Depends(get_db)):
    response = app.service.tag.add_tag(db, tag.userid, tag.document_id, tag.name)
    print(response)
    print(response.id, response.document_id)
    return response