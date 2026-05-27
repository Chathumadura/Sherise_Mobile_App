from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..security import get_current_user

router = APIRouter(prefix="/courses", tags=["Career & Skills"])

@router.get("", response_model=list[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Course).order_by(models.Course.id.desc()).all()

@router.post("", response_model=schemas.CourseOut, status_code=201)
def create_course(payload: schemas.CourseIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    course = models.Course(owner_id=current_user.id, **payload.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.put("/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: int, payload: schemas.CourseIn, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    course = db.query(models.Course).filter_by(id=course_id, owner_id=current_user.id).first()
    if not course:
        raise HTTPException(404, "Course not found or not owned by you")
    for k, v in payload.model_dump().items():
        setattr(course, k, v)
    db.commit()
    db.refresh(course)
    return course

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    course = db.query(models.Course).filter_by(id=course_id, owner_id=current_user.id).first()
    if not course:
        raise HTTPException(404, "Course not found or not owned by you")
    db.delete(course)
    db.commit()
    return {"message": "Course deleted"}
