from datetime import timedelta, datetime, timezone
import jwt
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from typing import Union

from app.db.queries import login_user, register_user
from app.utils.jwt_user import create_access_token, get_current_user
from app.validation.pydantic_classes import (
    Login,
    User,
    Register,
    Token,
    TokenData
)
from app.config.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

login_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@login_router.post("/register", response_model=Token)
async def register(user: Register):
    password_hash = pwd_context.hash(user.password)
    register_user(username=user.username, password=password_hash, email=user.email)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@login_router.post("/login", response_model=Token)
async def login(user: Login):
    password_hash = pwd_context.hash(user.password)
    login_user(username=user.username, password=password_hash)

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@login_router.get("/profile", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
