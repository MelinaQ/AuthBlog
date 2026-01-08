from fastapi import FastAPI

from app.database import Base, engine

from app.routers import auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}