from pydantic import EmailStr

from fastapi import  (
    HTTPException
)

from app.db.base import (
    Session
)

from app.db.models import (
    User
)

def register_user(username: str, password: str, email: EmailStr) -> None:
    with Session() as session:
        user = session.query(User).filter_by(username=username).one_or_none()

        if user:
            raise HTTPException(status_code=409, detail='User already exists')

        user = User(username=username, password=password, email=email)
        session.add(user)
        session.commit()

def login_user(username: str, password: str) -> bool:
    with Session() as session:
        user = session.query(User).filter_by(username=username).one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        if user.password != password:
            raise HTTPException(status_code=400, detail='Invalid password')

        return True

def get_user_by_username(username: str) -> dict:
    with Session() as session:
        user = session.query(User).filter_by(username=username).one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    return user.to_dict()



