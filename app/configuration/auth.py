import json

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError

import app.service
from app.configuration.database import get_db
from app.configuration.variables import jwt_values
from app.model.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_values["SECRET_KEY"], algorithms=jwt_values['ALGORITHM'])
        user_info_str: str = payload.get("sub")
        user_info_json = json.loads(user_info_str)
        print("user_info_json:", user_info_json)
        print(token, payload)
        username = user_info_json['name']
        user_id = user_info_json['id']
        if username is None:
            print("exception")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials, username is None.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_entity = app.service.user.get_one_user(next(get_db()), user_id)
        if user_entity.username != username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials, username is not correct.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        print('user_entity:', user_entity)
    except ExpiredSignatureError:  # expired token
        raise HTTPException(status_code=403, detail="token has been expired")
    except JWTError:
        print("JWTError")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials, JWTError.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # user = User.get_user(token_data)
    # print(token)
    # print(token_data)
    # user = app.service.user.get_user(token_data)
    # if user is None:
    #     raise credentials_exception
    user_entity = User()
    user_entity.id = user_id
    user_entity.username = username
    return user_entity

# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
