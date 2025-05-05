from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from app.config.config import SECRET_KEY, ALGORITHM, STATUS_CODE
from app.db.models import User
from app.db.queries import get_user_by_username


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    try:
        user = get_user_by_username(username=username)
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))
    return User(id=user.get("id"),
                username=user.get("username"),
                email=user.get("email"),
                password=user.get("password"),
                products=user.get("products")
    )
