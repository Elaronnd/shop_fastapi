from typing import Union, Annotated
from pydantic import BaseModel, Field, EmailStr, BeforeValidator, conlist
from app.config.config import DEFAULT_CATEGORY


def strip_and_lower(v: object) -> str:
    return str(v).strip().lower()


email_str_validator = Annotated[
    EmailStr,
    BeforeValidator(strip_and_lower)
]


class Login(BaseModel):
    username: str = Field(..., min_length=1, max_length=100, title="Username", description="Your username")
    password: str = Field(..., title="Password",
                          description="Must be restricted to, though does not specifically require any of:"
                                      "\nuppercase letters: A-Z"
                                      "\nlowercase letters: a-z"
                                      "\nnumbers: 0-9"
                                      "\nany of the special characters: @#$%^&+="
                                      "\nfrom 5 to 35 characters",
                          pattern=r"[A-Za-z0-9@#$%^&+=]{5,35}")


class Register(Login):
    email: email_str_validator = Field(..., title="Email", description="Your email address")


class UserResponse(BaseModel):
    username: str = Field(..., min_length=1, max_length=100, title="Username", description="Your username")
    email: email_str_validator = Field(..., title="Email", description="Your email address")
    products: list = Field(..., title="Products", description="List of products")


class UserData(UserResponse):
    password: str = Field(..., title="Password", description="Your password in hash")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class ProductData(BaseModel):
    title: str = Field(..., title="Title", description="Title of product", min_length=2, max_length=35)
    description: str = Field(..., title="Description", description="Description of product", min_length=10,
                             max_length=1000)
    price: int = Field(..., title="Price", description="Price of product", ge=0, le=1000000)
    category_id: int = Field(..., title="Category id", description="Id of category title", ge=0,
                             le=len(DEFAULT_CATEGORY))


class ProductResponse(ProductData):
    id: int = Field(..., title="Id", description="Id of product")
    images: conlist(str, max_length=10) = Field(..., title="Images", description="List of urls images")
