'''
This module contais the schemas
expected in HTTP responses.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* pydantic
'''

# Import system libs
from pydantic import BaseModel

#######################################
class Mensagem(BaseModel):
    mensagem: str


class LoginData(BaseModel):
    username: str
    password: str

class LoginSucesso(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True