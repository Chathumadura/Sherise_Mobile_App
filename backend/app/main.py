import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pathlib import Path
from .database import Base, engine
from .routers import auth, profile, emergency, sos, community, mentors, courses, legal

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")

app = FastAPI(
    title="SheRise API",
    description="Women empowerment mobile app backend with FastAPI and SQLite",
    version="2.0.0",
)

# Configure CORS
frontend_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", "*").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    detail = [{"loc": list(err["loc"]), "msg": err["msg"]} for err in errors]
    logger.error(f"Validation error: {detail}")
    return JSONResponse(
        status_code=422,
        content={"detail": detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_detail = f"{type(exc).__name__}: {str(exc)}"
    logger.error(f"Unhandled exception: {error_detail}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": error_detail},
    )

# Mount static files
static_dir = Path(__file__).resolve().parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
try:
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
except Exception as e:
    logger.warning(f"Could not mount static files: {e}")

# Include routers
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

@app.get("/health")
def health():
    return {"status": "ok"}
