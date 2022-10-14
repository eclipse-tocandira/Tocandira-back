from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session


from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, new_user=new_user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100,
               db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/search_name/{user_name}", response_model=schemas.User)
def read_user_name(db: Session = Depends(get_db), user_name=str):
    name_user = crud.get_user_by_name(db, name=user_name)
    if name_user is None:
        raise HTTPException(status_code=404, detail="Name not found")
    return name_user


@app.get("/search_id/{user_id}", response_model=schemas.User)
def read_user_id(db: Session = Depends(get_db), user_id=int):
    id_user = crud.get_user_by_id(db, user_id=user_id)
    if id_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return id_user


@app.post("/messages/", response_model=schemas.Message)
def create_message(new_message: schemas.MessageCreate,
                   db: Session = Depends(get_db)):
    return crud.create_message(db=db, new_message=new_message)


@app.get("/messages/", response_model=List[schemas.Message])
def read_messages(skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db)):
    messages = crud.get_messages(db, skip=skip, limit=limit)
    return messages


@app.get("/search_messages/{message_message}", response_model=schemas.Message)
def read_user_massage(db: Session = Depends(get_db),
                      message_message=str):
    db_messages = crud.get_messages_by_massage(db, message=message_message)
    if db_messages is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_messages


@app.get("/search_content/{message_content}", response_model=schemas.Message)
def read_user_content(db: Session = Depends(get_db),
                      message_content=str):
    db_content = crud.get_messages_by_content(db, content=message_content)
    if db_content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

@app.get("/api")
async def root():
    return {"Message": "Hello World"} 