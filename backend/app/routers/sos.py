from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..security import get_current_user

router = APIRouter(prefix="/sos", tags=["SOS Emergency"])

@router.post("", response_model=schemas.SOSOut, status_code=201)
def trigger_sos(payload: schemas.SOSIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    contacts = db.query(models.EmergencyContact).filter_by(user_id=current_user.id).count()
    if contacts == 0:
        raise HTTPException(400, "Please add at least one emergency contact before triggering SOS")
    sos = models.SOSAlert(user_id=current_user.id, **payload.model_dump())
    db.add(sos)
    db.commit()
    db.refresh(sos)
    return sos

@router.get("", response_model=list[schemas.SOSOut])
def list_sos(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.SOSAlert).filter_by(user_id=current_user.id).order_by(models.SOSAlert.id.desc()).all()

@router.put("/{sos_id}/resolve", response_model=schemas.SOSOut)
def resolve_sos(sos_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    sos = db.query(models.SOSAlert).filter_by(id=sos_id, user_id=current_user.id).first()
    if not sos:
        raise HTTPException(404, "SOS alert not found")
    sos.status = "Resolved"
    db.commit()
    db.refresh(sos)
    return sos
