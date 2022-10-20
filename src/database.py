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

# Import custom libs
from .env import Enviroment as Env

#######################################

engine = create_engine( Env.DATABASE_URL,
    connect_args={"check_same_thread": False} )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
