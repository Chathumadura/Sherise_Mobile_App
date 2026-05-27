from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .database import Base, engine
from .routers import auth, profile, emergency, sos, community, mentors, courses, legal

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SheRise API",
    description="Women empowerment mobile app backend with FastAPI and SQLite",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
