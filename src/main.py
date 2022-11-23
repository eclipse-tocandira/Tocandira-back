'''
This module executes the Backend
of the configuration tool.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
'''

# Import system libs
from typing import List
from fastapi import FastAPI, Depends, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Import custom libs
from . import database
from .env import Enviroment as Env
from .crud import Tuser
from .database import SessionManager, engine
from .user_authentication import schemas as auth_schemas
from .user_authentication import routes as auth_routes
from .plc_data import schemas as plc_schemas
from .plc_data import routes as plc_routes


#######################################

database.Base.metadata.create_all(bind=engine)

oauth2_schema = OAuth2PasswordBearer(tokenUrl='access_token')

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
    methods=["POST"], response_model=auth_schemas.LoginSucesso,
    endpoint=auth_routes.authentication)

app.add_api_route(root+"/hello",
    methods=["POST"], response_model=str,
    endpoint=auth_routes.hello_word)

app.add_api_route(root+"/protocol_defaults",
    methods=["GET"], response_model=plc_schemas.simpleList,
    endpoint=plc_routes.get_protocol_defaults)

app.add_api_route(root+"/datasource_defaults/{prot_name}",
    methods=["GET"], response_model=plc_schemas.dataSourceInfo,
    endpoint=plc_routes.get_datasource_defaults)

app.add_api_route(root+"/datasource",
    methods=["POST"], response_model=plc_schemas.dataSource,
    endpoint=plc_routes.create_datasource)

app.add_api_route(root+"/datasource/{ds_name}",
    methods=["GET"], response_model=plc_schemas.dataSource,
    endpoint=plc_routes.get_datasource_by_name)

app.add_api_route(root+"/datasources",
    methods=["GET"], response_model=List[plc_schemas.dataSource],
    endpoint=plc_routes.get_datasources)