from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, new_user: schemas.UserCreate):
    db_user = models.User(name=new_user.name, password=new_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_message(db: Session,
                   new_message: schemas.MessageCreate):
    db_message = models.Message(message=new_message.message,
                                content=new_message.content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Message).offset(skip).limit(limit).all()


def get_messages_by_massage(db: Session, message: str):
    return db.query(models.Message).filter(
        models.Message.message == message).first()


def get_messages_by_content(db: Session, content: str):
    return db.query(models.Message).filter(
        models.Message.content == content).first()
