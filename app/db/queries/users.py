from app.db import Product
from app.db.base import (
    Session
)
from app.db.models import (
    User
)
from app.validation.pydantic_classes import email_str_validator


def is_email_in_db(email: email_str_validator) -> bool:
    with Session() as session:
        email = session.query(User).filter_by(email=email).one_or_none()
        if not email:
            return False
        return True


def register_user(username: str, password: str, email: email_str_validator) -> None:
    with Session() as session:
        user = session.query(User).filter_by(username=username.lower()).one_or_none()

        if user:
            raise ValueError("User already exists")
        elif is_email_in_db(email=email):
            raise ValueError("This email already registered")

        user = User(username=username.lower(), password=password, email=email)
        session.add(user)
        session.commit()


def get_password_by_username(username: str) -> User.password:
    with Session() as session:
        user = session.query(User).filter_by(username=username.lower()).one_or_none()

        if not user:
            raise ValueError('User not found')

        return user.password


def get_user_by_username(username: str) -> User.to_dict:
    with Session() as session:
        user = session.query(User).filter_by(username=username.lower()).one_or_none()

        if not user:
            raise ValueError('User not found')

        return user.to_dict()

def get_user_by_id(user_id: int):
    with Session() as session:
        user = session.query(User).filter_by(id=user_id).one_or_none()

        if not user:
            raise ValueError('User not found')

        return user.to_dict()


def add_product_user(
    user_id: int,
    product: Product
) -> None:
    with Session() as session:
        user = session.query(User).filter_by(id=user_id).one_or_none()

        if not user:
            raise ValueError('User not found')

        user.products.append(product)
        session.add(user)
        session.commit()


def remove_product_user(
    user_id: int,
    product_id: int
) -> None:
    with Session() as session:
        user = session.query(User).filter_by(id=user_id).one_or_none()

        if not user:
            raise ValueError('User not found')

        for product in user.products:
            if product.id == product_id:
                user.products.remove(product)
