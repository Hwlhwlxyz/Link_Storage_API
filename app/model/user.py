import json
from datetime import datetime, timedelta
from typing import Optional


from jose import jwt
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from sqlalchemy.orm import relationship

from ..configuration.database import Base

from ..configuration.variables import jwt_values


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,  unique=True, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    document = relationship('Document')

    def __str__(self):
        return json.dumps({'username': self.username, 'email': self.email})

    @staticmethod
    def get_user(username: str):
        if username == 'test':
            return User(username=username, hashed_password='$2b$12$.dLvFcuDQ3buX.ak5ks2lOVYfoCByRzeeomh1YfVjc80xK96z8c7m', id=1)

    @staticmethod
    def authenticate_user(username: str, password: str):
        print(get_password_hash(password))
        user = User.get_user(username)
        print(user.hashed_password)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def login_check(email: str, hashed_password: str):
        if email == 'test':
            return True
        elif email == 'test1':
            if hashed_password == 'password':
                return True
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_values["SECRET_KEY"], algorithm=jwt_values['ALGORITHM'])
    return encoded_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def verify_password(plain_password, hashed_password):
    verified = False
    try:
        verified = pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        verified = False
    return verified


def get_password_hash(password):
    return pwd_context.hash(password)




