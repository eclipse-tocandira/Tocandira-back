'''
This module contais the schemas
expected in HTTP responses.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* pydantic
* fastapi
'''

# Import system libs
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm

#######################################

class LoginData(OAuth2PasswordRequestForm):
    pass

class UserBase(BaseModel):
    name: str
    is_admin: bool
    change_password: bool

class LoginSucess(UserBase):
    access_token: str
    token_type: str

class SafeUserCreate(BaseModel):
    name: str
    change_password: bool
    password: str

class UserPasswordChange(BaseModel):
    name: str
    new_password: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
