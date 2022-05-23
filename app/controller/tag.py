from typing import List

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
def add_tag(tag:InputTag, db: Session = Depends(get_db)):
    response = app.service.tag.add_tag(db, tag.userid, tag.document_id, tag.name)
    print(response)
    print(response.id, response.document_id)
    return response



@ROUTER.get('/document')
def get_tag_list_by_document(userid:int, document_id:int, db: Session = Depends(get_db)):
    response = app.service.tag.get_tag_list(db, userid, document_id)
    return response

class InputTagNameList(BaseModel):
    userid: int
    document_id: int
    name_list: List[str]

@ROUTER.post('/addlist')
def add_tag_list_by_document(input:InputTagNameList, db: Session = Depends(get_db)):
    response = app.service.tag.add_tag_list(db, input.userid, input.document_id, input.name_list)
    return response

@ROUTER.delete('/deletelist')
def delete_tag_list_by_document(input:InputTagNameList, db: Session = Depends(get_db)):
    response = app.service.tag.delete_tag_list(db, input.userid, input.document_id, input.name_list)
    return response

# delete unnecessary tags, and add new tags
@ROUTER.post('/updatelist')
def update_tag_list_by_document(input:InputTagNameList, db: Session = Depends(get_db)):
    response = app.service.tag.update_tag_list(db, input.userid, input.document_id, input.name_list)
    return response
