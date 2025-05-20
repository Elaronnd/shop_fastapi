import jwt
from datetime import datetime, timedelta, timezone
from typing import Union
from fastapi import HTTPException, status, WebSocketException, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config.config import SECRET_KEY, ALGORITHM, STATUS_CODE, STATUS_CODE_WEBSOCKET
from app.db.queries import get_user_by_username
from app.validation.pydantic_classes import UserData

security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: HTTPAuthorizationCredentials = Security(security)) -> UserData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    try:
        user = get_user_by_username(username=username)
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))
    return UserData(
        username=user.get("username"),
        email=user.get("email"),
        password=user.get("password"),
        products=user.get("products", [])
    )


def get_current_user_ws(
    token: str = Query(..., title="JWT token", description="Your JWT token without \"Bearer\"")
) -> UserData:
    credentials_exception = WebSocketException(
        code=1008,
        reason="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    try:
        user = get_user_by_username(username=username)
    except ValueError as error:
        raise WebSocketException(code=STATUS_CODE_WEBSOCKET.get(str(error).lower()), reason=str(error))
    return UserData(
        username=user.get("username"),
        email=user.get("email"),
        password=user.get("password"),
        products=user.get("products", [])
    )
