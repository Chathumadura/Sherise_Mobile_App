from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..security import get_current_user

router = APIRouter(prefix="/complaints", tags=["Legal Rights & Complaints"])

LEGAL_RIGHTS = [
    {"title": "Right to Safety", "description": "Every woman has the right to seek protection and emergency help."},
    {"title": "Right to Education", "description": "Women and girls should receive equal access to learning opportunities."},
    {"title": "Right to Work", "description": "Equal opportunity and non-discrimination at work are basic rights."},
    {"title": "Right to Report", "description": "Harassment, abuse, discrimination, or violence can be reported through suitable legal channels."},
]

@router.get("/legal-rights")
def legal_rights(current_user: models.User = Depends(get_current_user)):
    return LEGAL_RIGHTS

@router.get("", response_model=list[schemas.ComplaintOut])
def list_complaints(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Complaint).filter_by(user_id=current_user.id).order_by(models.Complaint.id.desc()).all()

@router.post("", response_model=schemas.ComplaintOut, status_code=201)
def create_complaint(payload: schemas.ComplaintIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    complaint = models.Complaint(user_id=current_user.id, **payload.model_dump())
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint

@router.put("/{complaint_id}", response_model=schemas.ComplaintOut)
def update_complaint(complaint_id: int, payload: schemas.ComplaintIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    complaint = db.query(models.Complaint).filter_by(id=complaint_id, user_id=current_user.id).first()
    if not complaint:
        raise HTTPException(404, "Complaint not found")
    if complaint.status.lower() == "resolved":
        raise HTTPException(400, "Resolved complaints cannot be edited")
    for k, v in payload.model_dump().items():
        setattr(complaint, k, v)
    db.commit()
    db.refresh(complaint)
    return complaint

@router.delete("/{complaint_id}")
def withdraw_complaint(complaint_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    complaint = db.query(models.Complaint).filter_by(id=complaint_id, user_id=current_user.id).first()
    if not complaint:
        raise HTTPException(404, "Complaint not found")
    db.delete(complaint)
    db.commit()
    return {"message": "Complaint withdrawn"}
