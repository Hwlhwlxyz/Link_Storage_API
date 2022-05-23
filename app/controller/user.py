from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.configuration.auth import oauth2_scheme, get_current_user
from app.configuration.database import get_db
from app.model.user import User

import app.service.document
import app.service.user

ROUTER = APIRouter()


@ROUTER.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


class InputUser(BaseModel):
    username: str
    email: str
    password: str


@ROUTER.post("/")
def create_new_user(input_user: InputUser, db: Session = Depends(get_db)):
    # db_user = User.get_user(db, email=input_user.username)

    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    new_user = app.service.user.create_user(db, input_user.username, input_user.email, input_user.password)
    print(new_user)
    return new_user


@ROUTER.get("/all")
def get_all_users(db: Session = Depends(get_db)):
    users = app.service.user.get_all_users(db)
    print(users)
    return users


class InputUserWithId(BaseModel):
    id: int
    username: str
    email: str
    password: str


@ROUTER.post("/edit")
def create_new_user(input_user: InputUserWithId, db: Session = Depends(get_db)):
    # db_user = User.get_user(db, email=input_user.username)

    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    new_user = app.service.user.edit_user(db, input_user.id, input_user.username, input_user.email, input_user.password)
    print(new_user)
    return new_user


@ROUTER.get("/userid/{user_id}")
async def read_users_me(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    print(current_user)
    print(user_id)
    response = app.service.user.get_one_user(db, user_id)
    print(response)
    print(type(response))
    response.hashed_password = None
    return response

# @ROUTER.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
