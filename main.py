from fastapi import FastAPI

from pydantic import BaseModel

import models
from database import engine

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserCreate, UserOut
from security import hash_password

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class HelloRequest(BaseModel):
    name: str

@app.get("/ping")
def ping():
    return {"message": "pong"}

from fastapi import Body

@app.post("/hello")
def hello(request: HelloRequest):
    return {"message": f"Hello, {request.name}!"}


from database import SessionLocal
from models import User
@app.get("/test-db")
def test_db():
    db = SessionLocal()

    user = User(
        email=f"test{db.query(User).count()+1}@example.com",
        hashed_password="notreallyhashed"
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return {"id": user.id, "email": user.email}

@app.post("/auth/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check whether email existed
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # create new user
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user