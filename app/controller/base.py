from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.configuration.variables import ACCESS_TOKEN_EXPIRE_MINUTES
from app.model.user import  fake_hash_password, User, create_access_token

ROUTER = APIRouter()

@ROUTER.get('/api')
def health_check():
    return {"base": "Hello World"}

@ROUTER.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username, form_data.password)
    user_entity = User.get_user(form_data.username)
    print(User.authenticate_user(form_data.username, form_data.password))
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
    return {"access_token": access_token, "token_type": "bearer"}