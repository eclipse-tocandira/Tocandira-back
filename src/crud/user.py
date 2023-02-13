'''
This module holds the functions to
access the User Table\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* sqlalchemy
'''

# Import system libs
from sqlalchemy.orm import Session
from passlib.context import CryptContext


# Import custom libs
from .. import models
from ..user_auth import schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#######################################

class Tuser:
    ''' Class with CRUD methods to access the User table.\n
    '''
    # --------------------
    @staticmethod
    def authenticate_user(db:Session, username: str, password: str):
        ''' Check if the user exists in the database. \n
        `db` (Session): Database session instance. \n
        `username` (str): Name passed by user. \n
        `password` (str): Password passed by user. \n
        return `user` (src.models.User): Database user. \n
        '''
        user = Tuser.get_by_name(db, name=username)
        if not user:
            return False
        if not Tuser.verify_password(password, user.password):
            return False
        return user
    # --------------------
    
    # --------------------
    @staticmethod
    def get_password_hash(password: str):
        ''' Creating a mask for the password. \n
        `password` (str): Password that will be hashed. \n
        return `hashed_password` (str): Password hash. \n
        '''
        hashed_password = pwd_context.hash(password)
        return hashed_password
    # --------------------

    # --------------------
    @staticmethod
    def verify_password(password: str, hashed_password: str):
        ''' Checking if a password mask is valid. \n
        `password` (str): password you want to verify. \n
        `hashed_password` (str): password saved in database. \n
        return `verification` (bool): Password verification result. \n
        '''
        verification = pwd_context.verify(password, hashed_password)
        return verification
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
        new_user.password = Tuser.get_password_hash(new_user.password)
        db_user = models.User(name=new_user.name, password=new_user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    # --------------------
