from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..security import get_current_user

router = APIRouter(prefix="/mentors", tags=["Mentors"])

@router.get("", response_model=list[schemas.MentorOut])
def list_mentors(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Mentor).order_by(models.Mentor.id.desc()).all()

@router.post("", response_model=schemas.MentorOut, status_code=201)
def create_mentor(payload: schemas.MentorIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    mentor = models.Mentor(owner_id=current_user.id, **payload.model_dump())
    db.add(mentor)
    db.commit()
    db.refresh(mentor)
    return mentor

@router.put("/{mentor_id}", response_model=schemas.MentorOut)
def update_mentor(mentor_id: int, payload: schemas.MentorIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    mentor = db.query(models.Mentor).filter_by(id=mentor_id, owner_id=current_user.id).first()
    if not mentor:
        raise HTTPException(404, "Mentor not found or not owned by you")
    for k, v in payload.model_dump().items():
        setattr(mentor, k, v)
    db.commit()
    db.refresh(mentor)
    return mentor

@router.delete("/{mentor_id}")
def delete_mentor(mentor_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    mentor = db.query(models.Mentor).filter_by(id=mentor_id, owner_id=current_user.id).first()
    if not mentor:
        raise HTTPException(404, "Mentor not found or not owned by you")
    db.delete(mentor)
    db.commit()
    return {"message": "Mentor deleted"}
