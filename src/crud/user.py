'''
This module holds the functions to
access the User Table\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* sqlalchemy
'''

# Import system libs
from sqlalchemy.orm import Session

# Import custom libs
from .. import models, schemas

#######################################

class Tuser:
    ''' Class with CRUD methods to access the User table.\n
    '''
    
    # --------------------
    @staticmethod
    def get_by_id(db:Session, user_id:int):
        ''' Query the database for a specific ID.\n
        `db` (Session): Database session instance.\n
        `user_id` (int): User number to search for.\n
        return (Query): The first result of the query.\n
        '''
        return db.query(models.User).filter(models.User.id == user_id).first()
    # --------------------

    # --------------------
    @staticmethod
    def get_by_name(db:Session, name:str):
        ''' Query the database for a specific name.\n
        `db` (Session): Database session instance.\n
        `name` (str): User name to search for.\n
        return (Query): The first result of the query.\n
        '''
        return db.query(models.User).filter(models.User.name == name).first()
    # --------------------

    # --------------------
    @staticmethod
    def get_by_range(db:Session, ini:int=0, end:int=100):
        ''' Query the database to get all user IDs within a range.\n
        `db` (Session): Database session instance.\n
        `ini` (int): Starting user ID.\n
        `end` (int): Last user ID\n
        return (Query): All result of the query.\n
        '''
        return db.query(models.User).offset(ini).limit(end).all()
    # --------------------

    # --------------------
    @staticmethod
    def get_all(db:Session):
        ''' Query the database to get all user IDs.\n
        `db` (Session): Database session instance.\n
        return (Query): All result of the query.\n
        '''
        return db.query(models.User).all()
    # --------------------

    # --------------------
    @staticmethod
    def create(db: Session, new_user: schemas.UserCreate):
        ''' Create a new user in the database.\n
        `db` (Session): Database session instance.\n
        `new_user` (schemas.UserCreate): New user with `.name` and `.password`.\n
        return `db_user` (models.User): The created user data.\n
        '''
        db_user = models.User(name=new_user.name, password=new_user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    # --------------------
