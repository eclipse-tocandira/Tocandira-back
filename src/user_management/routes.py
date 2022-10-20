'''
This module hold the endpoints for the 
user_management feature.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
* sqlalchemy
'''

# Import system libs
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

# Import custom libs
from ..database import get_db
from ..crud import Tuser
from .. import schemas

#######################################

# NOTE: When documenting the routes, pretend that the `db` argument
#       does not exist. Otherwise it will apear in the
#       route documentation and will look like something that the
#       user shoud pass, but it is handled internaly by FastAPI.

# --------------------
def create_user(new_user:schemas.UserCreate, db:Session=Depends(get_db)):
    ''' Creates a new user.\n
    `new_user` (schemas.UserCreate): A new user object.\n
    return `usr` (JSONResponse): A `schemas.User` object
    automatically parsed into an HTTP_OK response.\n
    '''
    usr = Tuser.create(db=db, new_user=new_user)

    if usr==None:
        raise HTTPException(status_code=404, detail="User not created.")

    return(usr)
# --------------------

# --------------------
def read_user_range(ini:int=0, end:int=100, db:Session=Depends(get_db)):
    ''' Get all users within a range of IDs.\n
    `ini` (int): ID to begin the search at.\n
    `end` (int): ID to end the search at.\n
    return `usr` (JSONResponse): A list of `schemas.User`
    objects automatically parsed into an HTTP_OK response.\n
    '''
    usr_list = Tuser.get_by_range(db, ini=ini, end=end)

    if usr_list==None:
        raise HTTPException(status_code=404, detail="No users found in search range.")
    if len(usr_list)==0:
        raise HTTPException(status_code=404, detail="No users found in search range.")

    return(usr_list)
# --------------------

# --------------------
def read_user_name(user_name:str, db:Session=Depends(get_db)):
    ''' Get a user by name.\n
    `user_name` (str): User name to search.\n
    return `usr` (JSONResponse): A `schemas.User` object
    automatically parsed into an HTTP_OK response.\n
    '''
    usr = Tuser.get_by_name(db, name=user_name)

    if (usr==None):
        raise HTTPException(status_code=404, detail=f"User Name '{user_name}' not found.")

    return(usr)
# --------------------

# --------------------
def read_user_id(user_id:int, db:Session=Depends(get_db)):
    ''' Get a user by id.\n
    `user_id` (int): User ID to search.\n
    return `usr` (JSONResponse): A `schemas.User` object
    automatically parsed into an HTTP_OK response.\n
    '''
    usr = Tuser.get_by_id(db, user_id=user_id)

    if (usr==None):
        raise HTTPException(status_code=404, detail=f"User ID '{user_id}' not found.")

    return(usr)
# --------------------

# --------------------
def read_helloworld(db:Session=Depends(get_db)):
    ''' Get a hello world message.\n
    return `usr` (JSONResponse): A dictionary object with
    the form `{'Message':'content'}` object
    automatically parsed into an HTTP_OK response.\n
    '''
    return({"Message": "Hello World from Backend"} )
# --------------------
