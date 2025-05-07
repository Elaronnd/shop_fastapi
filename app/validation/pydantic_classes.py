from typing import Union, Annotated
from pydantic import BaseModel, Field, EmailStr, BeforeValidator

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

class UserData(BaseModel):
    username: str = Field(..., min_length=1, max_length=100, title="Username", description="Your username")
    password: str = Field(..., title="Password", description="Your password in hash")
    email: email_str_validator = Field(..., title="Email", description="Your email address")
    products: list = Field(..., title="Products", description="List of products")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class Product(BaseModel):
    name: str = Field(..., title="Name", description="Name of product", min_length=2, max_length=35)
    description: str = Field(..., title="Description", description="description of product", min_length=10, max_length=1000)
    price: int = Field(..., title="Price", description="price of product", ge=1, le=1000000)
