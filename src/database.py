'''
This module has the database
instance.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* sqlalchemy
'''

# Import system libs
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# Import custom libs
from .env import Enviroment as Env

#######################################

engine = create_engine( Env.DATABASE_URL,
    connect_args={"check_same_thread": False} )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --------------------
@contextmanager
def SessionManager():
    ''' This seems to be the correct way to access the DataBase outside
    from the routes. To use it do: `with database.SessionManager() as db:`\n
    Ref. https://github.com/tiangolo/fastapi/issues/4588\n
    return `db` (SessionLocal): Database session.\n
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# --------------------

# --------------------
def get_db():
    ''' Database state in the dependency function. This is a
    method needed by FastAPI that is used along with `Depends`
    class in routes.\n
    return `db` (SessionLocal): Database session.\n
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# --------------------