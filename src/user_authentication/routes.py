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
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union
from fastapi.security import OAuth2PasswordBearer


# Import custom libs
from ..database import get_db
from ..crud import Tuser

# Config
SECRET_KEY = "9728256cbc2ecc81e478811a29aa5d0d8ae272b8deaec3c552cbb84b55a74908"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_schema = OAuth2PasswordBearer(tokenUrl='access_token')

#######################################

# NOTE: When documenting the routes, pretend that the `db` argument
#       does not exist. Otherwise it will apear in the
#       route documentation and will look like something that the
#       user shoud pass, but it is handled internaly by FastAPI.

# --------------------
def authentication(username:str, password:str, db:Session=Depends(get_db)):
    ''' Checks if the entered user is validated. \n
    `db` (Session): Database session instance. \n
    `username` (str): Username entered. \n
    `password` (str): Password entered. \n
    return `usr` (JSONResponse): return access token. \n
    '''
    usr = Tuser.authenticate_user(db, username, password)
    if not usr:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usr.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
# --------------------


# --------------------
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
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
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
# --------------------

# --------------------
def token_validation(access_token: str):
    ''' Check if the token is valid \n
    `access_token` (str): token to be verified\n
    return `usr.name` (str): username of the user to whom the token belongs\n
    '''
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM )
    return payload.get('sub')
# --------------------

# --------------------
def obter_usuario_logado(token: str = Depends(oauth2_schema),
                         session: Session = Depends(get_db)):
    ''' Checks if a user is logged in \n
    `token` (str): Token to be validated. \n
    `session` (Session): Database session instance. \n
    return `` (): \n
    '''
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')
    try:
        name = token_validation(token)
    except JWTError:
        raise exception

    if not name:
        raise exception

    usr = Tuser(session).get_by_name(name)

    if not usr:
        raise exception

    return 
# --------------------

                        
