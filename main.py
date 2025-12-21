from pydantic import BaseModel

class HelloRequest(BaseModel):
    name: str

from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping():
    return {"message": "pong"}

from fastapi import Body

@app.post("/hello")
def hello(request: HelloRequest):
    return {"message": f"Hello, {request.name}!"}