import json
from urllib.parse import parse_qsl
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

from starlette import status
from starlette.responses import Response, JSONResponse

import app.service.user
from app.configuration.database import get_db
from app.configuration.variables import ACCESS_TOKEN_EXPIRE_MINUTES
from app.model.user import User, create_access_token
from pydantic import BaseModel

ROUTER = APIRouter()

@ROUTER.get('/api')
def health_check():
    return {"base": "Hello World"}


class TokenRequestObject(BaseModel):
    username: str
    password: str

# @ROUTER.post("/token")
# async def login_for_access_token(form_data: TokenRequestObject):
#     print(form_data.username, form_data.password)
#     user_entity = User.get_user(form_data.username)
#     print(User.authenticate_user(form_data.username, form_data.password))
#     if not user_entity:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user_entity.email}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# @ROUTER.post("/token")
# async def login_for_access_token_form(form_data: OAuth2PasswordRequestForm = Depends()):
#     print(form_data.username, form_data.password)
#     user_entity = User.get_user(form_data.username)
#     print(User.authenticate_user(form_data.username, form_data.password))
#     if not user_entity:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user_entity.email}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# https://github.com/tiangolo/fastapi/issues/3327#issuecomment-876489648 # support different content-type
@ROUTER.post("/token", response_class=Response)
async def login_for_access_token_form(request: Request, db: Session = Depends(get_db)):
    value_to_decode = await request.body()
    value = value_to_decode.decode()
    username = None
    password = None
    try:
        json_value = json.loads(value)
        username = json_value['username']
        password = json_value['password']
    except ValueError:
        dict_value = dict(parse_qsl(value))
        username = dict_value['username']
        password = dict_value['password']


    print(username, password)

    user_entity = app.service.user.login_user_check(db, username, password)
    # user_entity = User.get_user(username)
    # print(User.authenticate_user(username, password))
    if not user_entity:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_entity.email}, expires_delta=access_token_expires
    )
    return JSONResponse({"access_token": access_token, "token_type": "bearer", "id": user_entity.id})