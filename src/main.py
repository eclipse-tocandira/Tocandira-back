'''
This module executes the Backend
of the configuration tool.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* fastapi
* sqlalchemy
'''

# Import system libs
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import custom libs
from .env import Enviroment as Env
from . import models, schemas
from .crud import Tuser, Tmessage
from .database import SessionLocal, SessionManager, engine

#######################################

default_route = f"/{Env.API_NAME}/{Env.API_VERSION}"

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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(default_route+"/users/", response_model=schemas.User)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    return Tuser.create(db=db, new_user=new_user)


@app.get(default_route+"/users/", response_model=List[schemas.User])
def read_users(ini: int = 0, end: int = 100,
               db: Session = Depends(get_db)):
    users = Tuser.get_by_range(db, ini=ini, end=end)
    return users


@app.get(default_route+"/search_name/{user_name}", response_model=schemas.User)
def read_user_name(db: Session = Depends(get_db), user_name=str):
    name_user = Tuser.get_by_name(db, name=user_name)
    if name_user is None:
        raise HTTPException(status_code=404, detail="Name not found")
    return name_user


@app.get(default_route+"/search_id/{user_id}", response_model=schemas.User)
def read_user_id(db: Session = Depends(get_db), user_id=int):
    id_user = Tuser.get_by_id(db, user_id=user_id)
    if id_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return id_user


@app.post(default_route+"/messages/", response_model=schemas.Message)
def create_message(new_message: schemas.MessageCreate,
                   db: Session = Depends(get_db)):
    return Tmessage.create(db=db, new_message=new_message)


@app.get(default_route+"/messages/", response_model=List[schemas.Message])
def read_messages(ini: int = 0, end: int = 100,
                  db: Session = Depends(get_db)):
    messages = Tmessage.get_by_range(db, ini=ini, end=end)
    return messages


@app.get(default_route+"/search_messages/{message_message}", response_model=schemas.Message)
def read_user_massage(db: Session = Depends(get_db),
                      message_message=str):
    db_messages = Tmessage.get_by_message(db, message=message_message)
    if db_messages is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_messages


@app.get(default_route+"/search_content/{message_content}", response_model=schemas.Message)
def read_user_content(db: Session = Depends(get_db),
                      message_content=str):
    db_content = Tmessage.get_by_content(db, content=message_content)
    if db_content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

@app.get(default_route)
async def root():
    return {"Message": "Hello World"} 