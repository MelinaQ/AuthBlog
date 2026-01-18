from pydantic import BaseModel
from app.schemas.user import UserOut
from typing import List

class PostCreate(BaseModel):
    title: str
    content: str

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    owner: UserOut
    
    class Config:
        from_attributes = True
    