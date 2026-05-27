from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship as orm_relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(160), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = orm_relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    emergency_contacts = orm_relationship("EmergencyContact", back_populates="user", cascade="all, delete-orphan")
    sos_alerts = orm_relationship("SOSAlert", back_populates="user", cascade="all, delete-orphan")
    posts = orm_relationship("CommunityPost", back_populates="user", cascade="all, delete-orphan")
    mentors = orm_relationship("Mentor", back_populates="owner", cascade="all, delete-orphan")
    courses = orm_relationship("Course", back_populates="owner", cascade="all, delete-orphan")
    complaints = orm_relationship("Complaint", back_populates="user", cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String(120), nullable=False)
    phone = Column(String(20), default="")
    address = Column(String(255), default="")
    bio = Column(Text, default="")
    occupation = Column(String(120), default="")
    profile_photo = Column(String(255), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = orm_relationship("User", back_populates="profile")

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(120), nullable=False)
    relationship = Column(String(80), nullable=False)
    phone = Column(String(20), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = orm_relationship("User", back_populates="emergency_contacts")

class SOSAlert(Base):
    __tablename__ = "sos_alerts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(String(40), default="Triggered")
    created_at = Column(DateTime, default=datetime.utcnow)
    user = orm_relationship("User", back_populates="sos_alerts")

class CommunityPost(Base):
    __tablename__ = "community_posts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(160), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(80), default="General")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = orm_relationship("User", back_populates="posts")

class Mentor(Base):
    __tablename__ = "mentors"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(120), nullable=False)
    expertise = Column(String(120), nullable=False)
    email = Column(String(160), nullable=False)
    phone = Column(String(20), default="")
    description = Column(Text, default="")
    availability = Column(String(120), default="Weekdays")
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = orm_relationship("User", back_populates="mentors")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(160), nullable=False)
    category = Column(String(100), nullable=False)
    provider = Column(String(120), default="SheRise")
    instructor = Column(String(120), default="")
    description = Column(Text, default="")
    duration = Column(String(60), default="")
    level = Column(String(60), default="Beginner")
    image_url = Column(Text, default="")
    progress = Column(Integer, default=0)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = orm_relationship("User", back_populates="courses")

class Complaint(Base):
    __tablename__ = "complaints"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(160), nullable=False)
    description = Column(Text, nullable=False)
    complaint_type = Column(String(80), nullable=False)
    status = Column(String(40), default="Submitted")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = orm_relationship("User", back_populates="complaints")
