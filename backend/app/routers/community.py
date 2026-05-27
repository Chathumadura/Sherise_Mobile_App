from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..security import get_current_user

router = APIRouter(prefix="/posts", tags=["Community Posts"])

@router.get("", response_model=list[schemas.PostOut])
def list_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.CommunityPost).order_by(models.CommunityPost.id.desc()).all()

@router.post("", response_model=schemas.PostOut, status_code=201)
def create_post(payload: schemas.PostIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = models.CommunityPost(user_id=current_user.id, **payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, payload: schemas.PostIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = db.query(models.CommunityPost).filter_by(id=post_id, user_id=current_user.id).first()
    if not post:
        raise HTTPException(404, "Post not found or not owned by you")
    for k, v in payload.model_dump().items():
        setattr(post, k, v)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = db.query(models.CommunityPost).filter_by(id=post_id, user_id=current_user.id).first()
    if not post:
        raise HTTPException(404, "Post not found or not owned by you")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}
