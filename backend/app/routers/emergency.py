from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..security import get_current_user

router = APIRouter(prefix="/emergency-contacts", tags=["Safety & Emergency Contacts"])

@router.get("", response_model=list[schemas.EmergencyContactOut])
def list_contacts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.EmergencyContact).filter_by(user_id=current_user.id).order_by(models.EmergencyContact.is_primary.desc(), models.EmergencyContact.id.desc()).all()

@router.post("", response_model=schemas.EmergencyContactOut, status_code=201)
def create_contact(payload: schemas.EmergencyContactIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    contact = models.EmergencyContact(user_id=current_user.id, **payload.model_dump())
    if payload.is_primary:
        db.query(models.EmergencyContact).filter_by(user_id=current_user.id).update({"is_primary": False})
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

@router.put("/{contact_id}", response_model=schemas.EmergencyContactOut)
def update_contact(contact_id: int, payload: schemas.EmergencyContactIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    contact = db.query(models.EmergencyContact).filter_by(id=contact_id, user_id=current_user.id).first()
    if not contact:
        raise HTTPException(404, "Emergency contact not found")
    if payload.is_primary:
        db.query(models.EmergencyContact).filter_by(user_id=current_user.id).update({"is_primary": False})
    for k, v in payload.model_dump().items():
        setattr(contact, k, v)
    db.commit()
    db.refresh(contact)
    return contact

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    contact = db.query(models.EmergencyContact).filter_by(id=contact_id, user_id=current_user.id).first()
    if not contact:
        raise HTTPException(404, "Emergency contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Emergency contact deleted"}
