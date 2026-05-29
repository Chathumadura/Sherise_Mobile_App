from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..security import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.Token, status_code=201)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        exists = db.query(models.User).filter(models.User.email == payload.email.lower()).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email already registered")
        user = models.User(name=payload.name.strip(), email=payload.email.lower(), hashed_password=get_password_hash(payload.password))
        db.add(user)
        db.commit()
        db.refresh(user)
        profile = models.Profile(user_id=user.id, full_name=user.name)
        db.add(profile)
        db.commit()
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "name": user.name, "email": user.email}}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.LoginIn, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == payload.email.lower()).first()
        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        if not user.is_active:
            raise HTTPException(status_code=403, detail="This account is deactivated")
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "name": user.name, "email": user.email}}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    try:
        return current_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/deactivate")
def deactivate(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        current_user.is_active = False
        db.commit()
        return {"message": "Account deactivated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
