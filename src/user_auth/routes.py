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
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Union

# Import custom libs
from ..crud import Tuser
from ..database import get_db
from ..env import Enviroment as Env
from .schemas import LoginData, LoginSucess, SafeUserCreate, UserCreate, User, UserPasswordChange

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
    
    success = LoginSucess(name=usr.name, is_admin=usr.is_admin,
        change_password=usr.change_password, access_token=access_token,
        token_type="Bearer")
    
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

# --------------------
def check_token(usr:str=Depends(_check_valid_token)):
    ''' A dummy route to check the token validation.\n
    return `True`: In case of unauthorized access the exception
    will be raised as `HTTP_401_UNAUTHORIZED` when processing the
    header.\n
    '''
    return(True)
# --------------------

# --------------------
def create_user(new_user: SafeUserCreate , logged_username: _check_valid_token=Depends(),db: Session=Depends(get_db)):
    ''' Create a new user. Only the admin user can create a new user. \n
    `new_user`(schemas.SafeUserCreate): The new user's data, including 
    name, password and change_password (which indicates if the user should change his password) \n
    return (schemas.User): Returns the data of the created user. \n
    '''

    logged_user = Tuser.get_by_name(db, name=logged_username)
    if logged_user.is_admin:
        try:
            user_exists = bool(Tuser.get_by_name(db, name=new_user.name))
            if not user_exists:
                new_user_not_admin = UserCreate(name=new_user.name,
                                                is_admin=False,
                                                change_password=new_user.change_password,
                                                password=new_user.password)
                new_user_response = Tuser.create(db, new_user_not_admin)
                return User(name=new_user_response.name, 
                            is_admin=new_user_response.is_admin,
                            change_password=new_user_response.change_password,
                            id=new_user_response.id)
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="The username already exists")
        except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail='Failed to create User')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Your user does not have permission to create new users')
# --------------------

# --------------------
def change_password(new_usr_pwd: UserPasswordChange ,logged_username: _check_valid_token=Depends(),db: Session=Depends(get_db)):
    ''' Change user password. The admin can change any user's password. 
    Other users can only change their own passwords. \n
    `new_usr_pwd` (schemas.UserPasswordChange): The username whose password will be changed and the new password. \n
    return (bool): Returns true if the password was changed. \n
    '''
    logged_user = Tuser.get_by_name(db, name=logged_username)
    if logged_username == new_usr_pwd.name or logged_user.is_admin:
        try:
            Tuser.change_password(db, new_usr_pwd.name, new_usr_pwd.new_password)
            return(True)
        except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail='Failed to change password')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='You do not have permission to change this user password')
# --------------------

# --------------------
def delete_user(username: str, logged_username: _check_valid_token=Depends(), db: Session=Depends(get_db)):
    ''' Delete a user. Only the admin can delete users. \n
    `username` (string): The user name that will be deleted.\n
    return (bool): Returns true if the user was deleted. \n
    '''
    logged_user = Tuser.get_by_name(db, name=logged_username)
    if logged_user.is_admin:
        if (username=='admin'):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Main Admin user can not be removed')
        try:
            num = Tuser.delete(db, username)
            if num > 0: 
                return True
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail='User not found')
        except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail='Failed to delete user')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You do not have permission to delete users')
# --------------------

# --------------------
def get_user_list(logged_username: _check_valid_token=Depends(), db: Session=Depends(get_db)):
    '''Get the list of users. Only the admin can access this list. \n
    return `users` (list): The list of Users in the application.\n
    '''
    logged_user = Tuser.get_by_name(db, name=logged_username)
    if logged_user.is_admin:
        try:
            usr_list = Tuser.get_all(db)
            users = []
            for usr in usr_list:
                users.append(User(name=usr.name, is_admin=usr.is_admin,
                    change_password=usr.change_password, id=usr.id))
            return(users)
        
        except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail='Failed to delete user')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='You do not have permission to delete users')
# --------------------
