'''
This module executes the Backend
of the configuration tool.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
'''

# Import system libs
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import custom libs
from .env import Enviroment as Env
from . import models, schemas
from .crud import Tuser
from .database import SessionManager, engine
from .user_management import routes as usr_routes

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
        admin_usr = schemas.UserCreate(name='admin',password='admin')
        Tuser.create(db,admin_usr)

root = f"/{Env.API_NAME}/{Env.API_VERSION}"

# Application Routes 
app.add_api_route(root+"/user/",
    methods=["POST"], response_model=schemas.User,
    endpoint=usr_routes.create_user )

app.add_api_route(root+"/users/",
    methods=["GET"], response_model=List[schemas.User],
    endpoint=usr_routes.read_user_range )

app.add_api_route(root+"/user_name/{user_name}",
    methods=["GET"], response_model=schemas.User,
    endpoint=usr_routes.read_user_name )

app.add_api_route(root+"/user_id/{user_id}",
    methods=["GET"], response_model=schemas.User,
    endpoint=usr_routes.read_user_id )

app.add_api_route(root,
    methods=["GET"], response_model=None,
    endpoint=usr_routes.read_helloworld )
