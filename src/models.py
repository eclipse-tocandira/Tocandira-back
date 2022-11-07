'''
This module contains the model of 
all database tables\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* sqlalchemy
'''

# Import system libs
from sqlalchemy import Boolean, Column, Integer, String

# Import custom libs
from .database import Base

#######################################

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=True)
