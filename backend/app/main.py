from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.api import patients, encounters, timeline

# Import models so SQLAlchemy registers them before create_all
import app.models.patient  # noqa: F401
import app.models.encounter  # noqa: F401
import app.models.clinical_event  # noqa: F401
import app.models.audit_log  # noqa: F401


@asynccontextmanager
async def lifespan(application: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="AuditCare Timeline API",
    description="Backend API for the AI4Devs final project.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(encounters.router)
app.include_router(timeline.router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "auditcare-timeline-api",
        "version": "0.1.0",
    }


@app.get("/")
def root():
    return {
        "message": "AuditCare Timeline API",
        "docs": "/docs",
    }
