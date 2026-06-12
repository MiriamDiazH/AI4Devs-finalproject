from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.clinical_event import ClinicalEvent
from app.repositories.encounter_repository import EncounterRepository
from app.repositories.event_repository import EventRepository
from app.repositories.patient_repository import PatientRepository
from app.schemas.encounter import EncounterCreate, EncounterResponse
from app.schemas.event import ClinicalEventResponse
from app.services.extraction_service import ExtractionService

router = APIRouter(prefix="/encounters", tags=["encounters"])


@router.post("", response_model=EncounterResponse, status_code=201)
def create_encounter(data: EncounterCreate, db: Session = Depends(get_db)):
    patient = PatientRepository(db).get(data.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return EncounterRepository(db).create(data)


@router.get("/patient/{patient_id}", response_model=list[EncounterResponse])
def list_patient_encounters(patient_id: str, db: Session = Depends(get_db)):
    patient = PatientRepository(db).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return EncounterRepository(db).list_by_patient(patient_id)


@router.post("/{encounter_id}/extract-events", response_model=list[ClinicalEventResponse])
def extract_events(encounter_id: str, db: Session = Depends(get_db)):
    encounter = EncounterRepository(db).get(encounter_id)
    if not encounter:
        raise HTTPException(status_code=404, detail="Encounter not found")

    raw_events = ExtractionService().extract_from_note(
        patient_id=encounter.patient_id,
        encounter_id=encounter.id,
        note_text=encounter.note_text,
    )

    events = [
        ClinicalEvent(
            encounter_id=encounter.id,
            patient_id=encounter.patient_id,
            category=e.get("category", "other"),
            title=e.get("title", ""),
            description=e.get("description", ""),
            source_quote=e.get("sourceQuote", ""),
            confidence=float(e.get("confidence", 0.0)),
            event_date=e.get("eventDate"),
        )
        for e in raw_events
    ]

    return EventRepository(db).create_bulk(events)
