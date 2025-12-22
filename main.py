from fastapi import FastAPI

from pydantic import BaseModel

import models
from database import engine

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