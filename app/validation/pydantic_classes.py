from typing import Union
from pydantic import BaseModel, Field, EmailStr

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
    email: EmailStr = Field(..., title="Email", description="Your email address")

class User(Register):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class Product(BaseModel):
    name: str = Field(..., title="Name", description="Name of product", min_length=2, max_length=35)
    description: str = Field(..., title="Description", description="description of product", min_length=10, max_length=1000)
    price: int = Field(..., title="Price", description="price of product", ge=1, le=1000000)
