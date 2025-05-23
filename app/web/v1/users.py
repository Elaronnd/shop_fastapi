from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from app.db.queries import get_password_by_username, register_user
from app.utils.jwt_user import create_access_token, get_current_user
from app.validation.pydantic_classes import (
    Login,
    UserData,
    Register,
    Token, UserResponse
)
from app.config.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    STATUS_CODE
)

users_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@users_router.post("/users/register", response_model=Token, tags=["v1/user"])
async def register(user: Register):
    password_hash = pwd_context.hash(user.password.lower())
    try:
        register_user(username=user.username.lower(), password=password_hash, email=user.email)
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username.lower()}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@users_router.post("/users/login", response_model=Token, tags=["v1/user"])
async def login(user: Login):
    try:
        user_password = get_password_by_username(username=user.username.lower())
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))

    if not pwd_context.verify(user.password.lower(), user_password):
        raise HTTPException(status_code=400, detail='Invalid password')

    access_token = create_access_token(data={"sub": user.username.lower()})
    return Token(access_token=access_token, token_type="bearer")


@users_router.get("/users/profile", response_model=UserResponse, tags=["v1/user"])
async def read_users_me(current_user: UserData = Depends(get_current_user)):
    return UserResponse(
        username=current_user.username,
        email=current_user.email,
        products=current_user.products
    )
