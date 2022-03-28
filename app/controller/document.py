from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.configuration.database import get_db

import app.service.document

ROUTER = APIRouter()


@ROUTER.get('/all')
def all_documents(userid, db: Session = Depends(get_db)):
    response = app.service.document.get_all_documents(db, userid)
    print(response)
    return response


@ROUTER.get('/search')
def search_documents(userid, keyword: str, db: Session = Depends(get_db)):
    response = app.service.document.search_documents(db, userid, keyword)
    print(response)
    return response


class InputDocument(BaseModel):
    userid: str
    title: str
    url: str
    description: str


@ROUTER.post('/')
def add_document(input_document: InputDocument, db: Session = Depends(get_db)):
    print(InputDocument)
    response = None
    response = app.service.document.add_document(db, input_document.userid, input_document.title, input_document.url,
                                                 input_document.description)
    print(response)
    return response


class InputUpdateDocument(BaseModel):
    id: str
    userid: str
    title: str
    url: str
    description: str


@ROUTER.patch('/')
def update_document(input_document: InputUpdateDocument, db: Session = Depends(get_db)):
    response = app.service.document.update_document(db, input_document.userid, input_document.id, input_document.title,
                                                    input_document.url, input_document.description)
    print(response)
    return response

@ROUTER.delete('/{document_id}')
def update_document(document_id: int, db: Session = Depends(get_db)):
    # TODO get userid
    userid = None
    response = app.service.document.delete_document(db, userid, document_id)
    print(response)
    return response
