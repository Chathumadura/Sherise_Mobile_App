import os
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pathlib import Path
from .database import Base, engine
from .routers import auth, profile, emergency, sos, community, mentors, courses, legal

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SheRise API",
    description="Women empowerment mobile app backend with FastAPI and SQLite",
    version="2.0.0",
)

frontend_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", "*").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc) or "Internal Server Error"},
    )

static_dir = Path(__file__).resolve().parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(emergency.router)
app.include_router(sos.router)
app.include_router(community.router)
app.include_router(mentors.router)
app.include_router(courses.router)
app.include_router(legal.router)

@app.get("/")
def root():
    return {"message": "SheRise API is running", "docs": "/docs"}
