from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from .. import models, schemas
from ..security import get_password_hash, verify_password, create_access_token, get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Registration request: name={payload.name}, email={payload.email}")
    try:
        # Step 1: Check if email exists
        logger.info("Step 1: Checking if email exists...")
        exists = db.query(models.User).filter(models.User.email == payload.email.lower()).first()
        if exists:
            logger.warning(f"Email already registered: {payload.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Step 2: Hash password
        logger.info("Step 2: Hashing password...")
        hashed_pwd = get_password_hash(payload.password)
        logger.info("Password hashed successfully")
        
        # Step 3: Create user
        logger.info("Step 3: Creating user...")
        user = models.User(
            name=payload.name.strip(),
            email=payload.email.lower(),
            hashed_password=hashed_pwd
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User created: {user.id}")
        
        # Step 4: Create profile
        logger.info("Step 4: Creating profile...")
        profile = models.Profile(user_id=user.id, full_name=user.name)
        db.add(profile)
        db.commit()
        logger.info(f"Profile created for user {user.id}")
        
        # Step 5: Create token
        logger.info("Step 5: Creating JWT token...")
        token = create_access_token({"sub": str(user.id)})
        logger.info("Token created successfully")
        
        logger.info(f"Registration successful for {user.email}")
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        error_msg = f"Database integrity error: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        db.rollback()
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"Registration error: {error_msg}", exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@router.post("/login")
def login(payload: schemas.LoginIn, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == payload.email.lower()).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if not user.is_active:
            raise HTTPException(status_code=403, detail="This account is deactivated")
        
        token = create_access_token({"sub": str(user.id)})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"Error during login: {error_msg}", exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@router.get("/me")
def me(current_user: models.User = Depends(get_current_user)):
    try:
        return {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at
        }
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"Error in /me endpoint: {error_msg}", exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)

@router.delete("/deactivate")
def deactivate(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        current_user.is_active = False
        db.commit()
        return {"message": "Account deactivated successfully"}
    except Exception as e:
        db.rollback()
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"Error during deactivation: {error_msg}", exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)
