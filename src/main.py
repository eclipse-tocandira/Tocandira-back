'''
This module executes the Backend
of the configuration tool.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
'''

# Import system libs
from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Import custom libs
from .env import Enviroment as Env
from . import models
from .crud import Tuser
from .database import SessionManager, engine
# from .user_create import routes as usr_routes
from .user_authentication import schemas as auth_schemas
from .user_authentication import routes as auth_routes


#######################################

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check for users and create a default one if it is empty
with SessionManager() as db:
    if (len(Tuser.get_all(db))==0):
        admin_usr = auth_schemas.UserCreate(name='admin', password='admin')
        Tuser.create(db,admin_usr)

root = f"/{Env.API_NAME}/{Env.API_VERSION}"

# Application Routes 
app.add_api_route(root+"/login",
    methods=["GET"], response_model=auth_schemas.LoginSucesso,
    endpoint=auth_routes.authentication)

