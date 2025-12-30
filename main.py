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

from security import verify_password, create_access_token
from schemas import Token

from security import get_current_user 

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

@app.post("/auth/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(
        data={"sub": str(db_user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/auth/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user