'''
This module hold the endpoints for the 
user_management feature.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
* sqlalchemy
'''

# Import system libs
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union

# Import custom libs
from ..crud import Tuser
from ..database import get_db
from ..env import Enviroment as Env
from .schemas import LoginData

#######################################

# XXX: The `oauth2_schema` needs to know the login route,
#       so upon changing the login route on `main.py` file,
#       remember to change the `tokenUrl` below to match
oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{Env.API_NAME}"+"/login")

# NOTE: When documenting the routes, pretend that the `db` argument
#       does not exist. Otherwise it will apear in the
#       route documentation and will look like something that the
#       user shoud pass, but it is handled internaly by FastAPI.

# --------------------
def authentication(user: LoginData=Depends(), db:Session=Depends(get_db)):
    ''' Checks if the entered user is validated. \n
    `user` (LoginData): Username and Password fields.\n
    return `success` (JSONResponse): Return the access token and type. \n
    '''
    usr = Tuser.authenticate_user(db, user.username, user.password)
    if not usr:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(Env.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = _create_access_token(
        data={"usr": usr.name}, expires_delta=access_token_expires
    )
    success = {"access_token": access_token, "token_type": "Bearer"}
    return(success)
# --------------------

# --------------------
def _create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    ''' Create access token. \n
    `data` (dict): Dictionary with the user identification
    for which the token was generated. \n
    `expires_delta` (Union): Token expiration time. \n
    return `encoded_jwt` (str): access token. \n
    '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": datetime.timestamp(expire)})
    encoded_jwt = jwt.encode(to_encode, Env.SECRET_KEY, algorithm=Env.ALGORITHM)
    return encoded_jwt
# --------------------

# --------------------
def _check_valid_token(token:str=Depends(oauth2_schema)):
    ''' Checks if a user is logged in \n
    `token` (str): Token to be validated. \n
    return `usrname` (str): Name of the logged user.\n
    '''
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Not logged in')
    try:
        payload = jwt.decode(token, Env.SECRET_KEY, algorithms=Env.ALGORITHM )
        usrname = payload.get('usr')
        if usrname is None:
            raise exception
        if payload.get('exp')<datetime.timestamp(datetime.utcnow()):
            raise exception
    except JWTError:
        raise exception

    # TODO: Returns a new token instead of the user
    #       doing this will refresh the token at every
    #       successful request. And this should be better
    #       for the user experience.

    return(usrname)
# --------------------
