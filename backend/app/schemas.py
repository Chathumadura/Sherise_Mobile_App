from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import re

PHONE_RE = re.compile(r"^[0-9+()\-\s]{7,20}$")

def check_phone(v: str) -> str:
    v = (v or "").strip()
    if v and not PHONE_RE.match(v):
        raise ValueError("Enter a valid phone number")
    return v

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=60)

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    class Config: from_attributes = True

class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class ProfileUpdate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    phone: str = ""
    address: str = Field(default="", max_length=255)
    bio: str = Field(default="", max_length=800)
    occupation: str = Field(default="", max_length=120)
    _phone_ok = field_validator("phone")(check_phone)

class ProfileOut(ProfileUpdate):
    id: int
    user_id: int
    profile_photo: str | None = None
    updated_at: datetime
    class Config: from_attributes = True

class EmergencyContactIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    relationship: str = Field(min_length=2, max_length=80)
    phone: str
    is_primary: bool = False
    _phone_ok = field_validator("phone")(check_phone)

class EmergencyContactOut(EmergencyContactIn):
    id: int
    user_id: int
    created_at: datetime
    class Config: from_attributes = True

class SOSIn(BaseModel):
    message: str = Field(default="I need emergency help", min_length=3, max_length=500)
    latitude: float | None = None
    longitude: float | None = None

class SOSOut(SOSIn):
    id: int
    user_id: int
    status: str
    created_at: datetime
    class Config: from_attributes = True

class PostIn(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    content: str = Field(min_length=5, max_length=2000)
    category: str = Field(default="General", max_length=80)

class PostOut(PostIn):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    class Config: from_attributes = True

class MentorIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    expertise: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = ""
    description: str = Field(default="", max_length=1000)
    availability: str = Field(default="Weekdays", max_length=120)
    _phone_ok = field_validator("phone")(check_phone)

class MentorOut(MentorIn):
    id: int
    owner_id: int
    created_at: datetime
    class Config: from_attributes = True

class CourseIn(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    category: str = Field(min_length=2, max_length=100)
    provider: str = Field(default="SheRise", max_length=120)
    instructor: str = Field(default="", max_length=120)
    description: str = Field(default="", max_length=1200)
    duration: str = Field(default="", max_length=60)
    level: str = Field(default="Beginner", max_length=60)
    image_url: str = Field(default="", max_length=500)
    progress: int = Field(default=0, ge=0, le=100)
    is_premium: bool = False

class CourseOut(CourseIn):
    id: int
    owner_id: int
    created_at: datetime
    class Config: from_attributes = True

class ComplaintIn(BaseModel):
    subject: str = Field(min_length=3, max_length=160)
    description: str = Field(min_length=10, max_length=2000)
    complaint_type: str = Field(min_length=2, max_length=80)
    status: str = Field(default="Submitted", max_length=40)

class ComplaintOut(ComplaintIn):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    class Config: from_attributes = True
