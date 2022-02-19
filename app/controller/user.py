from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session


from app.configuration.auth import oauth2_scheme, get_current_user
from app.configuration.database import get_db
from app.model.user import User

import app.service.document
import app.service.user


ROUTER = APIRouter()

@ROUTER.get('/profile')
def user():
    return {"user": "Hello World"}


@ROUTER.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@ROUTER.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

class InputUser(BaseModel):
    username: str
    email: str
    password: str

@ROUTER.post("/users/")
def create_new_user(input_user: InputUser, db: Session = Depends(get_db)):
    # db_user = User.get_user(db, email=input_user.username)

    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    new_user = app.service.user.create_user(db, input_user.username, input_user.email, input_user.password)
    print(new_user)
    return new_user

@ROUTER.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    users = app.service.user.get_all_users(db)
    print(users)
    return users


# @ROUTER.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
