'''
This module holds the functions to
access the Message Table\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* sqlalchemy
'''

# Import system libs
from sqlalchemy.orm import Session

# Import custom libs
from .. import models, schemas

#######################################


class Tmessage:
    ''' Class with CRUD methods to access the Message table.\n
    '''

    # --------------------
    @staticmethod
    def create(db:Session, new_message:schemas.MessageCreate):
        ''' Create a new message in the database.\n
        `db` (Session): Database session instance.\n
        `new_message` (schemas.MessageCreate): New message with
        `.message` and `.content`\n
        return `db_message` (models.Message): The created message data.\n
        '''
        db_message = models.Message(message=new_message.message,
            content=new_message.content)
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    # --------------------

    # --------------------
    @staticmethod
    def get_by_range(db:Session, ini:int=0, end:int=100):
        ''' Query the database to get all message IDs within a range.\n
        `db` (Session): Database session instance.\n
        `ini` (int): Starting user ID.\n
        `end` (int): Last user ID\n
        return (Query): All result of the query.\n
        '''
        return db.query(models.Message).offset(ini).limit(end).all()
    # --------------------

    # --------------------
    @staticmethod
    def get_by_message(db:Session, message:str):
        ''' Query the database for a specific message name.\n
        `db` (Session): Database session instance.\n
        `message` (str): Message name to search for.\n
        return (Query): The first result of the query.\n
        '''
        return db.query(models.Message).filter(
            models.Message.message == message).first()
    # --------------------

    # --------------------
    @staticmethod
    def get_by_content(db:Session, content:str):
        ''' Query the database for a specific message content.\n
        `db` (Session): Database session instance.\n
        `content` (str): Content to search for.\n
        return (Query): The first result of the query.\n
        '''
        return db.query(models.Message).filter(
            models.Message.content == content).first()
    # --------------------
