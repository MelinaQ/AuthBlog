from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostOut
from app.core.security import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/")
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_post = Post(
        title=post.title,
        content=post.content,
        owner_id=current_user.id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "id": new_post.id,
        "title": new_post.title,
        "content": new_post.content,
        "owner_id": new_post.owner_id,
    }

@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post: 
        raise HTTPException(status_code=404, detail="Post not found")
    
    return post