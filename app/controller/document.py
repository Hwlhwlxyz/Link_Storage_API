from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.configuration.database import get_db

import app.service.document

ROUTER = APIRouter()

@ROUTER.get('/all')
def all_documents():
    return {"user": "Hello World"}

@ROUTER.post('/find')
def all_documents(userid, db: Session = Depends(get_db)):
    response = app.service.document.get_all_documents(db, userid)
    print(response)
    return response

class InputDocument(BaseModel):
    user_id: int
    url: str
    description: str

@ROUTER.post('/')
def add_document(input_document: InputDocument, db: Session = Depends(get_db)):
    response = app.service.document.add_document(db, input_document.user_id, input_document.url, input_document.description)
    return response

